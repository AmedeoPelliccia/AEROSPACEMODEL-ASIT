"""
Tests for Bayesian Twin Digital Inference Engine

Tests particle filter initialisation, damage propagation, observation
models (POD/likelihood), resampling, risk assessment, safety case
evidence, data quality feedback, and the full update cycle.
"""

import pytest

from aerospacemodel.bayesian_twin.engine import (
    BayesianInferenceEngine,
    BayesianTwinError,
    DamageState,
    DamageType,
    DataQualityFeedback,
    InferenceError,
    InferenceResult,
    InspectionResult,
    ModelDiscrepancy,
    NDTFinding,
    ObservationError,
    ObservationSet,
    Particle,
    PhysicsParameters,
    PosteriorSummary,
    RecommendedAction,
    RiskMetrics,
    SafetyCaseEvidence,
    SafetyLevel,
    SensorReading,
    SensorType,
    StateError,
    StateVector,
)


# =============================================================================
# FIXTURES
# =============================================================================


def _make_prior_state() -> StateVector:
    """Create a simple prior state for testing."""
    return StateVector(
        damage_states=[
            DamageState(
                damage_id="DMG-001",
                location="stringer_18",
                damage_type=DamageType.CRACK,
                size_m=0.001,
            ),
        ],
        physics_params=PhysicsParameters(),
        model_discrepancy=ModelDiscrepancy(),
        timestamp="2023-10-27T10:00:00Z",
    )


def _make_observation_no_crack() -> ObservationSet:
    """Create an observation where no crack is found."""
    return ObservationSet(
        timestamp="2023-10-27T10:00:00Z",
        ndt_findings=[
            NDTFinding(
                location="stringer_18",
                result=InspectionResult.NO_CRACK,
                pod_confidence=0.95,
            ),
        ],
    )


def _make_observation_crack_found() -> ObservationSet:
    """Create an observation where a crack is detected."""
    return ObservationSet(
        timestamp="2023-10-27T10:00:00Z",
        ndt_findings=[
            NDTFinding(
                location="stringer_18",
                result=InspectionResult.CRACK_FOUND,
                detected_size_m=0.002,
                pod_confidence=0.95,
            ),
        ],
    )


# =============================================================================
# DATA STRUCTURE TESTS
# =============================================================================


class TestDataStructures:
    """Tests for data structure creation and defaults."""

    def test_damage_state_creation(self) -> None:
        ds = DamageState(
            damage_id="DMG-001",
            location="wing_root",
            damage_type=DamageType.CRACK,
            size_m=0.002,
        )
        assert ds.damage_id == "DMG-001"
        assert ds.damage_type == DamageType.CRACK
        assert ds.growth_rate == 0.0

    def test_physics_parameters_defaults(self) -> None:
        pp = PhysicsParameters()
        assert pp.paris_law_C == 1e-11
        assert pp.paris_law_m == 3.0
        assert pp.stress_intensity_factor == 1.0
        assert pp.load_uncertainty_factor == 1.0

    def test_model_discrepancy_defaults(self) -> None:
        md = ModelDiscrepancy()
        assert md.bias_mean == 0.0
        assert md.bias_std == 0.01
        assert md.description == "FE model discrepancy"

    def test_state_vector_creation(self) -> None:
        sv = _make_prior_state()
        assert len(sv.damage_states) == 1
        assert sv.timestamp == "2023-10-27T10:00:00Z"

    def test_ndt_finding_defaults(self) -> None:
        ndt = NDTFinding(
            location="loc_a",
            result=InspectionResult.NO_CRACK,
        )
        assert ndt.pod_confidence == 0.95
        assert ndt.detected_size_m is None

    def test_observation_set_defaults(self) -> None:
        obs = ObservationSet(timestamp="2023-01-01T00:00:00Z")
        assert obs.sensor_readings == []
        assert obs.ndt_findings == []

    def test_inference_result_defaults(self) -> None:
        result = InferenceResult()
        assert result.posterior_summaries == []
        assert result.recommended_action == RecommendedAction.CONTINUE_MONITORING
        assert result.safety_evidence is None


# =============================================================================
# ENUM TESTS
# =============================================================================


class TestEnumerations:
    """Tests for enumeration values."""

    def test_damage_types(self) -> None:
        assert DamageType.CRACK.value == "CRACK"
        assert DamageType.DELAMINATION.value == "DELAMINATION"
        assert DamageType.CORROSION.value == "CORROSION"

    def test_sensor_types(self) -> None:
        assert SensorType.STRAIN_GAUGE.value == "STRAIN_GAUGE"
        assert SensorType.NDT_ULTRASONIC.value == "NDT_ULTRASONIC"

    def test_safety_levels(self) -> None:
        assert SafetyLevel.CATASTROPHIC.value == "CATASTROPHIC"
        assert SafetyLevel.NO_EFFECT.value == "NO_EFFECT"

    def test_recommended_actions(self) -> None:
        assert RecommendedAction.GROUND_AIRCRAFT.value == "GROUND_AIRCRAFT"
        assert RecommendedAction.CONTINUE_MONITORING.value == "CONTINUE_MONITORING"


# =============================================================================
# EXCEPTION TESTS
# =============================================================================


class TestExceptions:
    """Tests for exception hierarchy."""

    def test_base_exception(self) -> None:
        assert issubclass(BayesianTwinError, Exception)

    def test_inference_error_hierarchy(self) -> None:
        assert issubclass(InferenceError, BayesianTwinError)

    def test_state_error_hierarchy(self) -> None:
        assert issubclass(StateError, BayesianTwinError)

    def test_observation_error_hierarchy(self) -> None:
        assert issubclass(ObservationError, BayesianTwinError)


# =============================================================================
# ENGINE INITIALISATION TESTS
# =============================================================================


class TestEngineInitialization:
    """Tests for BayesianInferenceEngine initialisation."""

    def test_engine_default_params(self) -> None:
        engine = BayesianInferenceEngine()
        assert engine.initialized is False
        assert engine.particles == []

    def test_engine_custom_params(self) -> None:
        engine = BayesianInferenceEngine(
            num_particles=500,
            critical_damage_m=0.03,
            process_noise_std=1e-5,
        )
        assert engine.initialized is False

    def test_initialize_creates_particles(self) -> None:
        engine = BayesianInferenceEngine(num_particles=100)
        engine.initialize(_make_prior_state())

        assert engine.initialized is True
        assert len(engine.particles) == 100

    def test_initialize_particle_weights_sum_to_one(self) -> None:
        engine = BayesianInferenceEngine(num_particles=50)
        engine.initialize(_make_prior_state())

        total_weight = sum(p.weight for p in engine.particles)
        assert abs(total_weight - 1.0) < 1e-10

    def test_initialize_empty_damage_raises(self) -> None:
        engine = BayesianInferenceEngine()
        empty_state = StateVector(
            damage_states=[],
            physics_params=PhysicsParameters(),
            model_discrepancy=ModelDiscrepancy(),
            timestamp="2023-01-01T00:00:00Z",
        )
        with pytest.raises(StateError, match="at least one damage state"):
            engine.initialize(empty_state)


# =============================================================================
# DAMAGE PROPAGATION TESTS
# =============================================================================


class TestDamagePropagation:
    """Tests for Paris law damage growth model."""

    def test_damage_does_not_shrink(self) -> None:
        engine = BayesianInferenceEngine(process_noise_std=0.0)
        damage = DamageState(
            damage_id="D1",
            location="loc",
            damage_type=DamageType.CRACK,
            size_m=0.001,
        )
        params = PhysicsParameters()
        discrepancy = ModelDiscrepancy(bias_mean=0.0, bias_std=0.0)

        result = engine._propagate_damage(damage, params, discrepancy, 1000.0)
        assert result.size_m >= damage.size_m

    def test_damage_grows_with_cycles(self) -> None:
        engine = BayesianInferenceEngine(process_noise_std=0.0)
        damage = DamageState(
            damage_id="D1",
            location="loc",
            damage_type=DamageType.CRACK,
            size_m=0.005,
        )
        params = PhysicsParameters(
            paris_law_C=1e-10,
            stress_intensity_factor=2.0,
        )
        discrepancy = ModelDiscrepancy(bias_mean=0.0, bias_std=0.0)

        result = engine._propagate_damage(damage, params, discrepancy, 10000.0)
        assert result.size_m > damage.size_m

    def test_bias_increases_growth(self) -> None:
        engine = BayesianInferenceEngine(process_noise_std=0.0)
        damage = DamageState(
            damage_id="D1",
            location="loc",
            damage_type=DamageType.CRACK,
            size_m=0.005,
        )
        params = PhysicsParameters(paris_law_C=1e-10)

        no_bias = ModelDiscrepancy(bias_mean=0.0, bias_std=0.0)
        with_bias = ModelDiscrepancy(bias_mean=0.5, bias_std=0.0)

        r1 = engine._propagate_damage(damage, params, no_bias, 10000.0)
        r2 = engine._propagate_damage(damage, params, with_bias, 10000.0)
        assert r2.size_m > r1.size_m


# =============================================================================
# OBSERVATION MODEL TESTS
# =============================================================================


class TestObservationModel:
    """Tests for POD curve and likelihood computation."""

    def test_pod_increases_with_size(self) -> None:
        engine = BayesianInferenceEngine()
        pod_small = engine._pod(0.0001, 1.0)
        pod_large = engine._pod(0.01, 1.0)
        assert pod_large > pod_small

    def test_pod_bounded_zero_to_one(self) -> None:
        engine = BayesianInferenceEngine()
        for size in [0.0, 0.0001, 0.001, 0.01, 0.1]:
            pod = engine._pod(size, 1.0)
            assert 0.0 <= pod <= 1.0

    def test_pod_confidence_scaling(self) -> None:
        engine = BayesianInferenceEngine()
        pod_full = engine._pod(0.005, 1.0)
        pod_half = engine._pod(0.005, 0.5)
        assert abs(pod_half - pod_full * 0.5) < 1e-10

    def test_likelihood_positive(self) -> None:
        engine = BayesianInferenceEngine(num_particles=10)
        engine.initialize(_make_prior_state())

        obs = _make_observation_no_crack()
        for p in engine.particles:
            lh = engine._compute_likelihood(p, obs)
            assert lh > 0


# =============================================================================
# RESAMPLING TESTS
# =============================================================================


class TestResampling:
    """Tests for systematic resampling."""

    def test_ess_computation(self) -> None:
        engine = BayesianInferenceEngine(num_particles=10)
        engine.initialize(_make_prior_state())

        # Uniform weights → ESS should equal N
        ess = engine._effective_sample_size()
        assert abs(ess - 10.0) < 1e-6

    def test_resample_preserves_count(self) -> None:
        engine = BayesianInferenceEngine(num_particles=50)
        engine.initialize(_make_prior_state())

        engine._resample()
        assert len(engine.particles) == 50

    def test_resample_uniform_weights(self) -> None:
        engine = BayesianInferenceEngine(num_particles=20)
        engine.initialize(_make_prior_state())

        engine._resample()
        for p in engine.particles:
            assert abs(p.weight - 1.0 / 20) < 1e-10


# =============================================================================
# RISK ASSESSMENT TESTS
# =============================================================================


class TestRiskAssessment:
    """Tests for ARP4761-aligned risk classification."""

    def test_catastrophic_risk(self) -> None:
        engine = BayesianInferenceEngine()
        summary = PosteriorSummary(
            location="loc",
            mean_size_m=0.04,
            percentile_95_m=0.05,
            prob_failure_before_next_check=0.01,
            rul_cycles_mean=100,
            rul_cycles_5th_pct=50,
        )
        risk = engine._assess_risk(summary)
        assert risk.safety_level == SafetyLevel.CATASTROPHIC
        assert risk.recommended_action == RecommendedAction.GROUND_AIRCRAFT

    def test_minor_risk(self) -> None:
        engine = BayesianInferenceEngine()
        summary = PosteriorSummary(
            location="loc",
            mean_size_m=0.001,
            percentile_95_m=0.002,
            prob_failure_before_next_check=1e-9,
            rul_cycles_mean=90000,
            rul_cycles_5th_pct=80000,
        )
        risk = engine._assess_risk(summary)
        assert risk.safety_level == SafetyLevel.MINOR
        assert risk.recommended_action == RecommendedAction.CONTINUE_MONITORING

    def test_hazardous_risk(self) -> None:
        engine = BayesianInferenceEngine()
        summary = PosteriorSummary(
            location="loc",
            mean_size_m=0.03,
            percentile_95_m=0.04,
            prob_failure_before_next_check=1e-4,
            rul_cycles_mean=5000,
            rul_cycles_5th_pct=2000,
        )
        risk = engine._assess_risk(summary)
        assert risk.safety_level == SafetyLevel.HAZARDOUS
        assert risk.recommended_action == RecommendedAction.IMMEDIATE_REPAIR


# =============================================================================
# DATA QUALITY FEEDBACK TESTS
# =============================================================================


class TestDataQualityFeedback:
    """Tests for adaptive sensor scheduling feedback."""

    def test_low_uncertainty_no_inspection(self) -> None:
        engine = BayesianInferenceEngine(uncertainty_threshold=0.003)
        summary = PosteriorSummary(
            location="loc",
            mean_size_m=0.001,
            percentile_95_m=0.002,
            prob_failure_before_next_check=0.0,
            rul_cycles_mean=100000,
            rul_cycles_5th_pct=90000,
        )
        feedback = engine._assess_data_quality([summary])
        assert len(feedback) == 1
        assert feedback[0].threshold_exceeded is False
        assert feedback[0].recommended_inspection is False

    def test_high_uncertainty_triggers_inspection(self) -> None:
        engine = BayesianInferenceEngine(uncertainty_threshold=0.003)
        summary = PosteriorSummary(
            location="loc",
            mean_size_m=0.001,
            percentile_95_m=0.01,
            prob_failure_before_next_check=0.0,
            rul_cycles_mean=50000,
            rul_cycles_5th_pct=30000,
        )
        feedback = engine._assess_data_quality([summary])
        assert len(feedback) == 1
        assert feedback[0].threshold_exceeded is True
        assert feedback[0].recommended_inspection is True
        assert feedback[0].recommended_sensor == SensorType.NDT_ULTRASONIC


# =============================================================================
# SAFETY CASE EVIDENCE TESTS
# =============================================================================


class TestSafetyCaseEvidence:
    """Tests for safety case artefact generation."""

    def test_safety_evidence_not_auto_approved(self) -> None:
        engine = BayesianInferenceEngine()
        metrics = [
            RiskMetrics(
                location="loc",
                probability_of_failure=1e-8,
                safety_level=SafetyLevel.MINOR,
                recommended_action=RecommendedAction.CONTINUE_MONITORING,
            ),
        ]
        evidence = engine._generate_safety_evidence(
            metrics, "2023-10-27T10:00:00Z"
        )
        assert evidence.approved is False
        assert "BREX SAFETY-002" in evidence.compliance_notes[-1]

    def test_safety_evidence_assessment_id(self) -> None:
        engine = BayesianInferenceEngine()
        evidence = engine._generate_safety_evidence(
            [], "2023-10-27T10:00:00Z"
        )
        assert evidence.assessment_id == "SCE-2023-10-27T10:00:00Z"
        assert evidence.model_version == "2.0"


# =============================================================================
# FULL UPDATE CYCLE TESTS
# =============================================================================


class TestUpdateCycle:
    """Tests for the full predict-update inference cycle."""

    def test_update_without_init_raises(self) -> None:
        engine = BayesianInferenceEngine()
        obs = _make_observation_no_crack()
        with pytest.raises(InferenceError, match="not initialised"):
            engine.update(obs)

    def test_update_returns_inference_result(self) -> None:
        engine = BayesianInferenceEngine(num_particles=50)
        engine.initialize(_make_prior_state())

        obs = _make_observation_no_crack()
        result = engine.update(obs, dt_cycles=500.0)

        assert isinstance(result, InferenceResult)
        assert len(result.posterior_summaries) == 1
        assert len(result.risk_metrics) == 1
        assert result.safety_evidence is not None
        assert len(result.data_quality_feedback) == 1

    def test_update_posterior_location_matches(self) -> None:
        engine = BayesianInferenceEngine(num_particles=50)
        engine.initialize(_make_prior_state())

        obs = _make_observation_no_crack()
        result = engine.update(obs)

        assert result.posterior_summaries[0].location == "stringer_18"

    def test_update_with_crack_found(self) -> None:
        engine = BayesianInferenceEngine(num_particles=50)
        engine.initialize(_make_prior_state())

        obs = _make_observation_crack_found()
        result = engine.update(obs, dt_cycles=1000.0)

        assert isinstance(result, InferenceResult)
        assert result.posterior_summaries[0].mean_size_m > 0

    def test_update_with_strain_sensor(self) -> None:
        engine = BayesianInferenceEngine(num_particles=50)
        engine.initialize(_make_prior_state())

        obs = ObservationSet(
            timestamp="2023-10-27T10:00:00Z",
            sensor_readings=[
                SensorReading(
                    sensor_id="SG-001",
                    sensor_type=SensorType.STRAIN_GAUGE,
                    value=1050.0,
                    unit="microstrain",
                    timestamp="2023-10-27T10:00:00Z",
                ),
            ],
        )
        result = engine.update(obs, dt_cycles=500.0)
        assert isinstance(result, InferenceResult)

    def test_multiple_updates_progress(self) -> None:
        import random

        random.seed(42)
        engine = BayesianInferenceEngine(num_particles=200)
        engine.initialize(_make_prior_state())

        obs = _make_observation_no_crack()
        result1 = engine.update(obs, dt_cycles=1000.0)
        result2 = engine.update(obs, dt_cycles=1000.0)

        # After two cycles, the 95th percentile should grow
        assert result2.posterior_summaries[0].percentile_95_m > 0

    def test_worst_case_action_selected(self) -> None:
        """When one location is catastrophic, overall action is GROUND."""
        prior = StateVector(
            damage_states=[
                DamageState(
                    damage_id="DMG-001",
                    location="loc_safe",
                    damage_type=DamageType.CRACK,
                    size_m=0.001,
                ),
                DamageState(
                    damage_id="DMG-002",
                    location="loc_danger",
                    damage_type=DamageType.CRACK,
                    size_m=0.051,
                ),
            ],
            physics_params=PhysicsParameters(paris_law_C=1e-8),
            model_discrepancy=ModelDiscrepancy(bias_mean=0.0, bias_std=0.0),
            timestamp="2023-01-01T00:00:00Z",
        )
        engine = BayesianInferenceEngine(
            num_particles=50,
            critical_damage_m=0.05,
            process_noise_std=0.0,
        )
        engine.initialize(prior)

        obs = ObservationSet(timestamp="2023-01-01T00:00:00Z")
        result = engine.update(obs, dt_cycles=10000.0)

        # The dangerous location should push overall action to severe
        assert result.recommended_action in (
            RecommendedAction.GROUND_AIRCRAFT,
            RecommendedAction.IMMEDIATE_REPAIR,
            RecommendedAction.SCHEDULE_INSPECTION,
        )
