"""
Tests for UTTS (Unified Teknia Token System) infrastructure specification.

Validates:
- N-STD-UTTS-01 standard files exist in ASIT/STANDARDS/
- UTTS YAML standard is valid and contains required metadata
- UTTS BREX YAML is valid and contains required rule categories
- ATA 96 directory has UTTS README
- N-NEURAL_NETWORKS documentation references UTTS
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
ASIT_STANDARDS = REPO_ROOT / "ASIT" / "STANDARDS"
UTTS_DIR = ASIT_STANDARDS / "N-STD-UTTS-01"
N_NEURAL = REPO_ROOT / "OPT-IN_FRAMEWORK" / "N-NEURAL_NETWORKS"
ATA96_DIR = N_NEURAL / "D-DIGITAL_THREAD_TRACEABILITY" / "ATA_96-TRACEABILITY_DPP_LEDGER"


# =============================================================================
# UTTS Standard Directory Structure Tests
# =============================================================================


class TestUTTSDirectoryStructure:
    """Tests that UTTS standard directory and files exist."""

    def test_utts_directory_exists(self):
        assert UTTS_DIR.is_dir(), "ASIT/STANDARDS/N-STD-UTTS-01/ must exist"

    def test_utts_readme_exists(self):
        assert (UTTS_DIR / "README.md").exists()

    def test_utts_standard_yaml_exists(self):
        assert (UTTS_DIR / "N-STD-UTTS-01_v0.1.0.yaml").exists()

    def test_utts_brex_yaml_exists(self):
        assert (UTTS_DIR / "N-STD-UTTS-01_BREX.yaml").exists()


# =============================================================================
# UTTS Standard YAML Validation Tests
# =============================================================================


class TestUTTSStandardYAML:
    """Tests that the UTTS standard YAML is valid and contains required content."""

    @pytest.fixture
    def std_data(self) -> dict:
        path = UTTS_DIR / "N-STD-UTTS-01_v0.1.0.yaml"
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    def test_metadata_standard_id(self, std_data: dict):
        assert std_data["metadata"]["standard_id"] == "N-STD-UTTS-01"

    def test_metadata_version(self, std_data: dict):
        assert std_data["metadata"]["version"] == "0.1.0"

    def test_metadata_status(self, std_data: dict):
        assert std_data["metadata"]["status"] == "DRAFT"

    def test_metadata_determinism(self, std_data: dict):
        assert std_data["metadata"]["determinism_level"] == "strict"

    def test_metadata_ata_domain(self, std_data: dict):
        assert std_data["metadata"]["ata_domain"] == "96"

    def test_three_tiers_defined(self, std_data: dict):
        assert len(std_data["tiers"]) == 3

    def test_tier_ids(self, std_data: dict):
        tier_ids = [t["id"] for t in std_data["tiers"]]
        assert "MTL1" in tier_ids
        assert "MTL2" in tier_ids
        assert "MTL3" in tier_ids

    def test_mtl3_ledger_entry_schema(self, std_data: dict):
        mtl3 = next((t for t in std_data["tiers"] if t["id"] == "MTL3"), None)
        assert mtl3 is not None, "Tier MTL3 not found in tiers"
        required = mtl3["ledger_entry_schema"]["required_fields"]
        assert "entry_id" in required
        assert "payload_hash" in required
        assert "previous_hash" in required
        assert "authority_signature" in required

    def test_mtl3_event_types(self, std_data: dict):
        mtl3 = next((t for t in std_data["tiers"] if t["id"] == "MTL3"), None)
        assert mtl3 is not None, "Tier MTL3 not found in tiers"
        events = mtl3["ledger_entry_schema"]["event_types"]
        assert "TOKEN_CREATE" in events
        assert "TRANSFORM_PHI" in events
        assert "BASELINE_FREEZE" in events

    def test_mtl2_phi_operator(self, std_data: dict):
        mtl2 = next((t for t in std_data["tiers"] if t["id"] == "MTL2"), None)
        assert mtl2 is not None, "Tier MTL2 not found in tiers"
        assert mtl2["operator"] == "Φ"

    def test_invariants_exist(self, std_data: dict):
        assert len(std_data["invariants"]["rules"]) == 5

    def test_governance_policies_exist(self, std_data: dict):
        assert len(std_data["governance"]["policies"]) == 4

    def test_compliance_includes_easa(self, std_data: dict):
        assert "EASA Part 21" in std_data["metadata"]["compliance"]

    def test_compliance_includes_eu_ai_act(self, std_data: dict):
        assert "EU AI Act" in std_data["metadata"]["compliance"]

    def test_compliance_includes_gaia_x(self, std_data: dict):
        assert "GAIA-X" in std_data["metadata"]["compliance"]

    def test_decision_states(self, std_data: dict):
        states = std_data["decision_states"]["allowed_states"]
        assert set(states) == {"ALLOW", "HOLD", "REJECT", "ESCALATE"}


# =============================================================================
# UTTS BREX YAML Validation Tests
# =============================================================================


class TestUTTSBrexYAML:
    """Tests that the UTTS BREX YAML is valid and contains required rules."""

    @pytest.fixture
    def brex_data(self) -> dict:
        path = UTTS_DIR / "N-STD-UTTS-01_BREX.yaml"
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    def test_brex_id(self, brex_data: dict):
        assert brex_data["metadata"]["brex_id"] == "N-STD-UTTS-01-BREX-001"

    def test_brex_parent_authority(self, brex_data: dict):
        assert brex_data["metadata"]["parent_authority"] == "ASIT-BREX-MASTER-001"

    def test_structure_rules_exist(self, brex_data: dict):
        assert len(brex_data["structure_rules"]) >= 3

    def test_ledger_rules_exist(self, brex_data: dict):
        assert len(brex_data["ledger_rules"]) >= 4

    def test_transformation_rules_exist(self, brex_data: dict):
        assert len(brex_data["transformation_rules"]) >= 4

    def test_safety_rules_exist(self, brex_data: dict):
        assert len(brex_data["safety_rules"]) >= 3

    def test_safety_rules_escalate_to_stk_saf(self, brex_data: dict):
        for rule in brex_data["safety_rules"]:
            assert rule["escalation_target"] == "STK_SAF"

    def test_escalation_72h_timeout(self, brex_data: dict):
        assert brex_data["escalation_procedures"]["safety_content"]["timeout"] == "72 hours"

    def test_audit_retention(self, brex_data: dict):
        assert "7 years" in brex_data["audit_requirements"]["retention"]


# =============================================================================
# ATA 96 Directory Content Tests
# =============================================================================


class TestATA96DirectoryContent:
    """Tests that ATA 96 directory has UTTS content."""

    def test_ata96_readme_exists(self):
        assert (ATA96_DIR / "README.md").exists()

    @pytest.fixture
    def readme_text(self) -> str:
        return (ATA96_DIR / "README.md").read_text(encoding="utf-8")

    def test_readme_references_utts(self, readme_text: str):
        assert "UTTS" in readme_text

    def test_readme_references_n_std_utts_01(self, readme_text: str):
        assert "N-STD-UTTS-01" in readme_text

    def test_readme_references_mtl_tiers(self, readme_text: str):
        assert "MTL₁" in readme_text or "MTL1" in readme_text
        assert "MTL₂" in readme_text or "MTL2" in readme_text
        assert "MTL₃" in readme_text or "MTL3" in readme_text

    def test_readme_references_ata96(self, readme_text: str):
        assert "ATA 96" in readme_text


# =============================================================================
# N-NEURAL_NETWORKS Documentation UTTS Reference Tests
# =============================================================================


class TestNNeuralNetworksUTTSReferences:
    """Tests that N-NEURAL_NETWORKS documentation references UTTS."""

    @pytest.fixture
    def index_text(self) -> str:
        return (N_NEURAL / "00_INDEX.md").read_text(encoding="utf-8")

    @pytest.fixture
    def readme_text(self) -> str:
        return (N_NEURAL / "README.md").read_text(encoding="utf-8")

    def test_index_references_utts(self, index_text: str):
        assert "UTTS" in index_text

    def test_index_references_n_std_utts_01(self, index_text: str):
        assert "N-STD-UTTS-01" in index_text

    def test_readme_references_utts(self, readme_text: str):
        assert "UTTS" in readme_text or "Unified Teknia Token System" in readme_text

    def test_readme_references_utts_standard(self, readme_text: str):
        assert "N-STD-UTTS-01" in readme_text

    def test_readme_related_docs_has_utts(self, readme_text: str):
        assert "UTTS Standard" in readme_text or "N-STD-UTTS-01" in readme_text
