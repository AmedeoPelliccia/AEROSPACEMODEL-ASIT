"""
Tests for Ampel Protocol Scaling Benchmark

Validates resource accounting, synergy metrics, TRL-4 criteria,
and operational envelope computation across molecular systems.
"""

import pytest

from ASIGT.quantum.ampel_benchmark import (
    AmpelBenchmarkManager,
    BenchmarkResult,
    BenchmarkStatus,
    InitStrategy,
    MolecularSystem,
    NoiseProfile,
    ResourceAccounting,
    ScalingAnalysis,
    REFERENCE_ENERGIES,
    QUBIT_COUNTS,
)


class TestNoiseProfile:
    """Tests for NoiseProfile dataclass."""

    def test_default_noise_profile(self):
        """Test default noise values match IBM Eagle targets."""
        np_profile = NoiseProfile()
        assert np_profile.p1q == 0.01
        assert np_profile.p2q == 0.05
        assert np_profile.readout_error == 0.02

    def test_noise_profile_serialization(self):
        """Test NoiseProfile to_dict round-trip."""
        np_profile = NoiseProfile(p2q=0.07)
        d = np_profile.to_dict()
        assert d["p2q"] == 0.07
        assert "t1_us" in d


class TestResourceAccounting:
    """Tests for ResourceAccounting."""

    def test_cost_estimation(self):
        """Test IBM Quantum cost estimation and serialization."""
        ra = ResourceAccounting(
            total_shots=1_000_000,
            cost_per_shot_usd=0.00001,
        )
        assert ra.estimated_cost_usd == pytest.approx(10.0)
        d = ra.to_dict()
        assert d["cost_per_shot_usd"] == 0.00001
        assert d["estimated_cost_usd"] == pytest.approx(10.0)

    def test_zero_shots_zero_cost(self):
        """Test zero shots yields zero cost."""
        ra = ResourceAccounting()
        assert ra.estimated_cost_usd == 0.0


class TestBenchmarkResult:
    """Tests for BenchmarkResult."""

    def test_chemical_accuracy_flag(self):
        """Test chemical accuracy threshold at 1.6 mHa via actual run."""
        manager = AmpelBenchmarkManager(contract_id="CTR-TEST")
        analysis = manager.run_scaling_test(
            MolecularSystem.H2, p2q=0.01, max_iterations=200
        )
        # At low noise, warm-start should achieve chemical accuracy
        assert analysis.ampel_result is not None
        if analysis.ampel_result.delta_e_mha < 1.6:
            assert analysis.ampel_result.chemical_accuracy_achieved is True
        else:
            assert analysis.ampel_result.chemical_accuracy_achieved is False

    def test_result_serialization(self):
        """Test full result serialization including convergence data."""
        result = BenchmarkResult(
            molecule=MolecularSystem.LIH,
            init_strategy=InitStrategy.AI_WARM_START,
            status=BenchmarkStatus.CONVERGED,
            convergence_history=[-8.5, -8.7, -8.8],
        )
        d = result.to_dict()
        assert d["molecule"] == "lih"
        assert d["init_strategy"] == "ai_warm"
        assert d["status"] == "converged"
        assert d["convergence_history"] == [-8.5, -8.7, -8.8]
        assert d["convergence_len"] == 3
        assert d["convergence_final"] == -8.8


class TestScalingAnalysis:
    """Tests for ScalingAnalysis metrics computation."""

    def _make_paired_results(self):
        """Create a baseline/Ampel result pair."""
        baseline = BenchmarkResult(
            molecule=MolecularSystem.LIH,
            init_strategy=InitStrategy.RANDOM,
            delta_e_mha=42.0,
            status=BenchmarkStatus.CONVERGED,
            run_label="B1",
        )
        baseline.resources.total_executions = 2850

        ampel = BenchmarkResult(
            molecule=MolecularSystem.LIH,
            init_strategy=InitStrategy.AI_WARM_START,
            delta_e_mha=28.0,
            status=BenchmarkStatus.CONVERGED,
            run_label="B2",
        )
        ampel.resources.total_executions = 1820
        return baseline, ampel

    def test_execution_savings_computation(self):
        """Test execution savings percentage calculation."""
        baseline, ampel = self._make_paired_results()
        analysis = ScalingAnalysis(
            molecule=MolecularSystem.LIH,
            p2q=0.05,
            baseline_result=baseline,
            ampel_result=ampel,
        )
        analysis.compute_metrics()
        assert analysis.execution_savings_pct == pytest.approx(36.1, abs=0.5)

    def test_synergy_metric_positive(self):
        """Test beta_x synergy is positive when Ampel outperforms."""
        baseline, ampel = self._make_paired_results()
        analysis = ScalingAnalysis(
            molecule=MolecularSystem.LIH,
            baseline_result=baseline,
            ampel_result=ampel,
        )
        analysis.compute_metrics()
        assert analysis.beta_synergy_mha == pytest.approx(14.0)
        assert analysis.synergy_positive is True

    def test_trl4_criteria_all_pass(self):
        """Test TRL-4 criteria evaluation."""
        baseline, ampel = self._make_paired_results()
        analysis = ScalingAnalysis(
            molecule=MolecularSystem.LIH,
            baseline_result=baseline,
            ampel_result=ampel,
        )
        analysis.compute_metrics()
        criteria = analysis.passes_trl4_criteria()
        assert criteria["savings_above_30pct"] is True
        assert criteria["synergy_positive"] is True
        assert criteria["ampel_converged"] is True
        assert criteria["baseline_converged"] is True

    def test_analysis_requires_both_results(self):
        """Test that compute_metrics raises without paired results."""
        analysis = ScalingAnalysis()
        with pytest.raises(ValueError, match="Both baseline and Ampel"):
            analysis.compute_metrics()


class TestAmpelBenchmarkManager:
    """Tests for the benchmark orchestrator."""

    def test_manager_creation(self):
        """Test manager initialization with contract_id."""
        manager = AmpelBenchmarkManager(
            contract_id="KITDM-CTR-QUANTUM-001"
        )
        assert manager.contract_id == "KITDM-CTR-QUANTUM-001"
        assert len(manager.results) == 0

    def test_manager_requires_contract_id(self):
        """Test that empty contract_id raises ValueError."""
        with pytest.raises(ValueError, match="contract_id is required"):
            AmpelBenchmarkManager(contract_id="")

    def test_run_scaling_test_lih(self):
        """Test full LiH scaling test execution."""
        manager = AmpelBenchmarkManager(contract_id="CTR-TEST")
        analysis = manager.run_scaling_test(
            MolecularSystem.LIH,
            p2q=0.05,
            max_iterations=100,
        )
        assert analysis.synergy_positive is True
        assert analysis.execution_savings_pct > 30.0
        assert len(manager.results) == 2

    def test_run_scaling_test_validates_inputs(self):
        """Test input validation for run_scaling_test."""
        manager = AmpelBenchmarkManager(contract_id="CTR-TEST")
        with pytest.raises(ValueError, match="max_iterations must be > 0"):
            manager.run_scaling_test(MolecularSystem.H2, max_iterations=0)
        with pytest.raises(ValueError, match="shots must be > 0"):
            manager.run_scaling_test(MolecularSystem.H2, shots=-1)
        with pytest.raises(ValueError, match="p2q must be >= 0"):
            manager.run_scaling_test(MolecularSystem.H2, p2q=-0.01)

    def test_scaling_report_generation(self):
        """Test DataFrame report generation."""
        manager = AmpelBenchmarkManager(contract_id="CTR-TEST")
        manager.run_scaling_test(
            MolecularSystem.H2, p2q=0.05, max_iterations=50
        )
        manager.run_scaling_test(
            MolecularSystem.LIH, p2q=0.05, max_iterations=50
        )

        df = manager.generate_scaling_report()
        assert len(df) == 2
        assert "beta_x (mHa)" in df.columns
        assert "TRL-4 Pass" in df.columns

    def test_operational_envelope(self):
        """Test operational envelope with safety-adjusted limits."""
        manager = AmpelBenchmarkManager(contract_id="CTR-TEST")
        manager.run_scaling_test(
            MolecularSystem.LIH, p2q=0.05, max_iterations=50
        )
        manager.run_scaling_test(
            MolecularSystem.LIH, p2q=0.07, max_iterations=50
        )

        envelope = manager.get_operational_envelope()
        assert "lih" in envelope["envelope"]
        assert envelope["safety_margin_pct"] == 15.0
        lih = envelope["envelope"]["lih"]
        # Safety-adjusted values should reflect the safety margin
        factor = 1.0 - envelope["safety_margin_pct"] / 100.0
        assert lih["max_p2q_synergy_adjusted"] == pytest.approx(
            lih["max_p2q_synergy_raw"] * factor, abs=1e-6
        )
        assert lih["max_p2q_savings30_adjusted"] == pytest.approx(
            lih["max_p2q_savings30_raw"] * factor, abs=1e-6
        )

    def test_decision_logging(self):
        """Test EASA-aligned decision traceability with unique event IDs."""
        manager = AmpelBenchmarkManager(contract_id="CTR-001")
        manager.run_scaling_test(
            MolecularSystem.H2, p2q=0.05, max_iterations=50
        )

        assert len(manager._decision_log) >= 2
        assert manager._decision_log[0]["contract_id"] == "CTR-001"
        assert "AMPEL-SCALE-001" in manager._decision_log[0]["requirements"]
        # Each event should have a unique event_id
        assert manager._decision_log[0]["event_id"].startswith("AMPEL-EVT-")
        event_ids = [e["event_id"] for e in manager._decision_log]
        assert len(event_ids) == len(set(event_ids)), "event_ids must be unique"


class TestReferenceData:
    """Tests for molecular reference data consistency."""

    def test_all_molecules_have_reference_energy(self):
        """Verify every MolecularSystem has a reference energy."""
        for mol in MolecularSystem:
            assert mol in REFERENCE_ENERGIES

    def test_all_molecules_have_qubit_count(self):
        """Verify every MolecularSystem has a qubit count."""
        for mol in MolecularSystem:
            assert mol in QUBIT_COUNTS
            assert QUBIT_COUNTS[mol] >= 2

    def test_reference_energies_are_negative(self):
        """All molecular ground-state energies should be negative."""
        for mol, energy in REFERENCE_ENERGIES.items():
            assert energy < 0, f"{mol.value} energy should be negative"
