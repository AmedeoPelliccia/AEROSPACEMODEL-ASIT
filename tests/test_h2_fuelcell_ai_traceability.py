"""
Tests for H₂/fuel cell/AI cross-domain traceability to T/N domains.

Validates that the three novel technology subdomains declare mandatory
cross_domain_traceability links to their corresponding T/N domains in
T_SUBDOMAIN_LC_ACTIVATION.yaml, per the requirement:

  "For H₂/fuel cell/AI-specific requirements, ensure traceability to
   corresponding T/N domains"

Coverage:
- C2_CIRCULAR_CRYOGENIC_CELLS (H₂/ATA 28) → N_DIGITAL_THREAD_TRACEABILITY
- P_PROPULSION (Fuel Cell/ATA 71) → C2_CIRCULAR_CRYOGENIC_CELLS, N_DIGITAL_THREAD_TRACEABILITY
- I2_INTELLIGENCE (AI/ML/ATA 95-97) → N_AI_GOVERNANCE_ASSURANCE, N_DIGITAL_THREAD_TRACEABILITY
- VAL-007 validation rule present in T_SUBDOMAIN_LC_ACTIVATION.yaml
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
LC_ACTIVATION = REPO_ROOT / "lifecycle" / "T_SUBDOMAIN_LC_ACTIVATION.yaml"


@pytest.fixture(scope="module")
def lc_data() -> dict:
    assert LC_ACTIVATION.exists(), "T_SUBDOMAIN_LC_ACTIVATION.yaml must exist"
    return yaml.safe_load(LC_ACTIVATION.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def subdomains(lc_data: dict) -> dict:
    return lc_data["subdomains"]


# =============================================================================
# C2_CIRCULAR_CRYOGENIC_CELLS — H₂ traceability
# =============================================================================

class TestH2CrossDomainTraceability:
    """C2_CIRCULAR_CRYOGENIC_CELLS must trace to N_DIGITAL_THREAD_TRACEABILITY."""

    def test_c2_has_cross_domain_traceability(self, subdomains: dict):
        assert "cross_domain_traceability" in subdomains["C2_CIRCULAR_CRYOGENIC_CELLS"], \
            "C2_CIRCULAR_CRYOGENIC_CELLS must declare cross_domain_traceability"

    def test_c2_traces_to_n_digital_thread(self, subdomains: dict):
        cdt = subdomains["C2_CIRCULAR_CRYOGENIC_CELLS"]["cross_domain_traceability"]
        assert "N_DIGITAL_THREAD_TRACEABILITY" in cdt, \
            "C2 (H₂) must trace to N_DIGITAL_THREAD_TRACEABILITY for DPP ledger"

    def test_c2_n_digital_thread_has_mandatory_phases(self, subdomains: dict):
        cdt = subdomains["C2_CIRCULAR_CRYOGENIC_CELLS"]["cross_domain_traceability"]
        mandatory = cdt["N_DIGITAL_THREAD_TRACEABILITY"]["mandatory_at"]
        assert isinstance(mandatory, list) and len(mandatory) > 0, \
            "mandatory_at must be a non-empty list"

    def test_c2_n_digital_thread_mandatory_at_lc02(self, subdomains: dict):
        cdt = subdomains["C2_CIRCULAR_CRYOGENIC_CELLS"]["cross_domain_traceability"]
        assert "LC02" in cdt["N_DIGITAL_THREAD_TRACEABILITY"]["mandatory_at"], \
            "DPP registration must be mandatory at LC02 (requirements baseline)"

    def test_c2_n_digital_thread_mandatory_at_lc08(self, subdomains: dict):
        cdt = subdomains["C2_CIRCULAR_CRYOGENIC_CELLS"]["cross_domain_traceability"]
        assert "LC08" in cdt["N_DIGITAL_THREAD_TRACEABILITY"]["mandatory_at"], \
            "DPP registration must be mandatory at LC08 (certification)"

    def test_c2_n_digital_thread_mandatory_at_lc14(self, subdomains: dict):
        cdt = subdomains["C2_CIRCULAR_CRYOGENIC_CELLS"]["cross_domain_traceability"]
        assert "LC14" in cdt["N_DIGITAL_THREAD_TRACEABILITY"]["mandatory_at"], \
            "DPP closure must be mandatory at LC14 (end-of-life)"

    def test_c2_n_digital_thread_link_type(self, subdomains: dict):
        cdt = subdomains["C2_CIRCULAR_CRYOGENIC_CELLS"]["cross_domain_traceability"]
        assert cdt["N_DIGITAL_THREAD_TRACEABILITY"]["link_type"] == "allocates_to"

    def test_c2_n_digital_thread_has_rationale(self, subdomains: dict):
        cdt = subdomains["C2_CIRCULAR_CRYOGENIC_CELLS"]["cross_domain_traceability"]
        rationale = cdt["N_DIGITAL_THREAD_TRACEABILITY"].get("rationale", "")
        assert len(rationale) > 0, "cross_domain_traceability link must include rationale"

    def test_c2_n_digital_thread_path_is_valid(self, subdomains: dict):
        cdt = subdomains["C2_CIRCULAR_CRYOGENIC_CELLS"]["cross_domain_traceability"]
        path = cdt["N_DIGITAL_THREAD_TRACEABILITY"]["path"]
        assert "N-NEURAL_NETWORKS" in path and "D-DIGITAL_THREAD_TRACEABILITY" in path


# =============================================================================
# P_PROPULSION — Fuel Cell traceability
# =============================================================================

class TestFuelCellCrossDomainTraceability:
    """P_PROPULSION must trace to C2_CIRCULAR_CRYOGENIC_CELLS and N_DIGITAL_THREAD_TRACEABILITY."""

    def test_p_has_cross_domain_traceability(self, subdomains: dict):
        assert "cross_domain_traceability" in subdomains["P_PROPULSION"], \
            "P_PROPULSION must declare cross_domain_traceability"

    def test_p_traces_to_c2(self, subdomains: dict):
        cdt = subdomains["P_PROPULSION"]["cross_domain_traceability"]
        assert "C2_CIRCULAR_CRYOGENIC_CELLS" in cdt, \
            "Fuel cell (P) must trace to C2 (H₂ supply interface)"

    def test_p_c2_mandatory_at_lc02(self, subdomains: dict):
        cdt = subdomains["P_PROPULSION"]["cross_domain_traceability"]
        assert "LC02" in cdt["C2_CIRCULAR_CRYOGENIC_CELLS"]["mandatory_at"], \
            "H₂ supply interface ICD must be traced at LC02 (requirements)"

    def test_p_c2_mandatory_at_lc04(self, subdomains: dict):
        cdt = subdomains["P_PROPULSION"]["cross_domain_traceability"]
        assert "LC04" in cdt["C2_CIRCULAR_CRYOGENIC_CELLS"]["mandatory_at"], \
            "H₂ supply interface must be traced at LC04 (design)"

    def test_p_c2_link_type(self, subdomains: dict):
        cdt = subdomains["P_PROPULSION"]["cross_domain_traceability"]
        assert cdt["C2_CIRCULAR_CRYOGENIC_CELLS"]["link_type"] == "derives_from"

    def test_p_c2_has_rationale(self, subdomains: dict):
        cdt = subdomains["P_PROPULSION"]["cross_domain_traceability"]
        rationale = cdt["C2_CIRCULAR_CRYOGENIC_CELLS"].get("rationale", "")
        assert len(rationale) > 0

    def test_p_c2_path_is_valid(self, subdomains: dict):
        cdt = subdomains["P_PROPULSION"]["cross_domain_traceability"]
        path = cdt["C2_CIRCULAR_CRYOGENIC_CELLS"]["path"]
        assert "C2-CIRCULAR_CRYOGENIC_CELLS" in path

    def test_p_traces_to_n_digital_thread(self, subdomains: dict):
        cdt = subdomains["P_PROPULSION"]["cross_domain_traceability"]
        assert "N_DIGITAL_THREAD_TRACEABILITY" in cdt, \
            "Fuel cell (P) must trace to N_DIGITAL_THREAD_TRACEABILITY for DPP ledger"

    def test_p_n_digital_thread_mandatory_at_lc02(self, subdomains: dict):
        cdt = subdomains["P_PROPULSION"]["cross_domain_traceability"]
        assert "LC02" in cdt["N_DIGITAL_THREAD_TRACEABILITY"]["mandatory_at"]

    def test_p_n_digital_thread_mandatory_at_lc08(self, subdomains: dict):
        cdt = subdomains["P_PROPULSION"]["cross_domain_traceability"]
        assert "LC08" in cdt["N_DIGITAL_THREAD_TRACEABILITY"]["mandatory_at"]

    def test_p_n_digital_thread_mandatory_at_lc14(self, subdomains: dict):
        cdt = subdomains["P_PROPULSION"]["cross_domain_traceability"]
        assert "LC14" in cdt["N_DIGITAL_THREAD_TRACEABILITY"]["mandatory_at"]

    def test_p_n_digital_thread_link_type(self, subdomains: dict):
        cdt = subdomains["P_PROPULSION"]["cross_domain_traceability"]
        assert cdt["N_DIGITAL_THREAD_TRACEABILITY"]["link_type"] == "allocates_to"

    def test_p_n_digital_thread_path_is_valid(self, subdomains: dict):
        cdt = subdomains["P_PROPULSION"]["cross_domain_traceability"]
        path = cdt["N_DIGITAL_THREAD_TRACEABILITY"]["path"]
        assert "N-NEURAL_NETWORKS" in path and "D-DIGITAL_THREAD_TRACEABILITY" in path


# =============================================================================
# I2_INTELLIGENCE — AI/ML traceability
# =============================================================================

class TestAICrossDomainTraceability:
    """I2_INTELLIGENCE must trace to N_AI_GOVERNANCE_ASSURANCE and N_DIGITAL_THREAD_TRACEABILITY."""

    def test_i2_has_cross_domain_traceability(self, subdomains: dict):
        assert "cross_domain_traceability" in subdomains["I2_INTELLIGENCE"], \
            "I2_INTELLIGENCE must declare cross_domain_traceability"

    def test_i2_traces_to_n_ai_governance(self, subdomains: dict):
        cdt = subdomains["I2_INTELLIGENCE"]["cross_domain_traceability"]
        assert "N_AI_GOVERNANCE_ASSURANCE" in cdt, \
            "AI/ML (I2) must trace to N_AI_GOVERNANCE_ASSURANCE"

    def test_i2_ai_governance_mandatory_at_lc01(self, subdomains: dict):
        cdt = subdomains["I2_INTELLIGENCE"]["cross_domain_traceability"]
        assert "LC01" in cdt["N_AI_GOVERNANCE_ASSURANCE"]["mandatory_at"], \
            "AI governance must be established at LC01 (concept)"

    def test_i2_ai_governance_mandatory_at_lc02(self, subdomains: dict):
        cdt = subdomains["I2_INTELLIGENCE"]["cross_domain_traceability"]
        assert "LC02" in cdt["N_AI_GOVERNANCE_ASSURANCE"]["mandatory_at"]

    def test_i2_ai_governance_mandatory_at_lc08(self, subdomains: dict):
        cdt = subdomains["I2_INTELLIGENCE"]["cross_domain_traceability"]
        assert "LC08" in cdt["N_AI_GOVERNANCE_ASSURANCE"]["mandatory_at"]

    def test_i2_ai_governance_link_type(self, subdomains: dict):
        cdt = subdomains["I2_INTELLIGENCE"]["cross_domain_traceability"]
        assert cdt["N_AI_GOVERNANCE_ASSURANCE"]["link_type"] == "derives_from"

    def test_i2_ai_governance_has_rationale(self, subdomains: dict):
        cdt = subdomains["I2_INTELLIGENCE"]["cross_domain_traceability"]
        rationale = cdt["N_AI_GOVERNANCE_ASSURANCE"].get("rationale", "")
        assert len(rationale) > 0

    def test_i2_ai_governance_path_is_valid(self, subdomains: dict):
        cdt = subdomains["I2_INTELLIGENCE"]["cross_domain_traceability"]
        path = cdt["N_AI_GOVERNANCE_ASSURANCE"]["path"]
        assert "N-NEURAL_NETWORKS" in path and "A-AI_GOVERNANCE_ASSURANCE" in path

    def test_i2_traces_to_n_digital_thread(self, subdomains: dict):
        cdt = subdomains["I2_INTELLIGENCE"]["cross_domain_traceability"]
        assert "N_DIGITAL_THREAD_TRACEABILITY" in cdt, \
            "AI/ML (I2) must trace to N_DIGITAL_THREAD_TRACEABILITY for DPP ledger"

    def test_i2_n_digital_thread_mandatory_at_lc02(self, subdomains: dict):
        cdt = subdomains["I2_INTELLIGENCE"]["cross_domain_traceability"]
        assert "LC02" in cdt["N_DIGITAL_THREAD_TRACEABILITY"]["mandatory_at"]

    def test_i2_n_digital_thread_mandatory_at_lc05(self, subdomains: dict):
        cdt = subdomains["I2_INTELLIGENCE"]["cross_domain_traceability"]
        assert "LC05" in cdt["N_DIGITAL_THREAD_TRACEABILITY"]["mandatory_at"], \
            "Model training lineage must be registered in DPP at LC05"

    def test_i2_n_digital_thread_mandatory_at_lc08(self, subdomains: dict):
        cdt = subdomains["I2_INTELLIGENCE"]["cross_domain_traceability"]
        assert "LC08" in cdt["N_DIGITAL_THREAD_TRACEABILITY"]["mandatory_at"]

    def test_i2_n_digital_thread_mandatory_at_lc14(self, subdomains: dict):
        cdt = subdomains["I2_INTELLIGENCE"]["cross_domain_traceability"]
        assert "LC14" in cdt["N_DIGITAL_THREAD_TRACEABILITY"]["mandatory_at"]

    def test_i2_n_digital_thread_link_type(self, subdomains: dict):
        cdt = subdomains["I2_INTELLIGENCE"]["cross_domain_traceability"]
        assert cdt["N_DIGITAL_THREAD_TRACEABILITY"]["link_type"] == "allocates_to"

    def test_i2_n_digital_thread_path_is_valid(self, subdomains: dict):
        cdt = subdomains["I2_INTELLIGENCE"]["cross_domain_traceability"]
        path = cdt["N_DIGITAL_THREAD_TRACEABILITY"]["path"]
        assert "N-NEURAL_NETWORKS" in path and "D-DIGITAL_THREAD_TRACEABILITY" in path


# =============================================================================
# VAL-007 validation rule
# =============================================================================

class TestVAL007ValidationRule:
    """VAL-007 cross-domain traceability rule must exist in T_SUBDOMAIN_LC_ACTIVATION.yaml."""

    def test_val007_exists(self, lc_data: dict):
        rule_ids = [r["id"] for r in lc_data["validation_rules"]]
        assert "VAL-007" in rule_ids, "VAL-007 cross-domain traceability rule must exist"

    def test_val007_name(self, lc_data: dict):
        rule = next(r for r in lc_data["validation_rules"] if r["id"] == "VAL-007")
        assert "Cross-Domain" in rule["name"] or "cross" in rule["name"].lower()

    def test_val007_enforcement_is_block(self, lc_data: dict):
        rule = next(r for r in lc_data["validation_rules"] if r["id"] == "VAL-007")
        assert rule["enforcement"] == "block"

    def test_val007_applies_to_c2(self, lc_data: dict):
        rule = next(r for r in lc_data["validation_rules"] if r["id"] == "VAL-007")
        applies = rule.get("applies_to", [])
        assert "C2_CIRCULAR_CRYOGENIC_CELLS" in applies

    def test_val007_applies_to_p(self, lc_data: dict):
        rule = next(r for r in lc_data["validation_rules"] if r["id"] == "VAL-007")
        applies = rule.get("applies_to", [])
        assert "P_PROPULSION" in applies

    def test_val007_applies_to_i2(self, lc_data: dict):
        rule = next(r for r in lc_data["validation_rules"] if r["id"] == "VAL-007")
        applies = rule.get("applies_to", [])
        assert "I2_INTELLIGENCE" in applies


# =============================================================================
# Referenced N-domain directories exist
# =============================================================================

class TestNDomainDirectoriesExist:
    """Referenced N-domain target directories must exist in the repository."""

    N_NEURAL = REPO_ROOT / "OPT-IN_FRAMEWORK" / "N-NEURAL_NETWORKS"

    def test_n_digital_thread_dir_exists(self):
        assert (self.N_NEURAL / "D-DIGITAL_THREAD_TRACEABILITY").is_dir()

    def test_n_ai_governance_dir_exists(self):
        assert (self.N_NEURAL / "A-AI_GOVERNANCE_ASSURANCE").is_dir()

    def test_ata96_dir_exists(self):
        assert (
            self.N_NEURAL / "D-DIGITAL_THREAD_TRACEABILITY" / "ATA_96-TRACEABILITY_DPP_LEDGER"
        ).is_dir()

    def test_ai_governance_assurance_dir_exists(self):
        assert (
            self.N_NEURAL / "A-AI_GOVERNANCE_ASSURANCE" / "ATA_AI_GOVERNANCE_ASSURANCE"
        ).is_dir()
