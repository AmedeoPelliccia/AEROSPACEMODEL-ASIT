"""
Tests for LC02 System Requirements Packages (ATA 28-11).

Validates directory structure, YAML schema integrity, cross-file consistency,
and governance controls for the three LC02 SSOT packages at:
  .../KDB/LM/SSOT/PLM/LC02_SYSTEM_REQUIREMENTS/PACKAGES/
    - COMPLIANCE_INTENT
    - DATA
    - ICD
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGES_DIR = (
    REPO_ROOT
    / "OPT-IN_FRAMEWORK"
    / "T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS"
    / "C2-CIRCULAR_CRYOGENIC_CELLS"
    / "ATA_28-FUEL"
    / "28-11-lh2-primary-tank"
    / "28-11-00-lh2-primary-tank-general"
    / "KDB"
    / "LM"
    / "SSOT"
    / "PLM"
    / "LC02_SYSTEM_REQUIREMENTS"
    / "PACKAGES"
)

CINT_DIR = PACKAGES_DIR / "COMPLIANCE_INTENT"
DATA_DIR = PACKAGES_DIR / "DATA"
ICD_DIR = PACKAGES_DIR / "ICD"

# ── Required files per package ────────────────────────────────────────────

CINT_YAML_FILES = [
    "COMPLIANCE_INTENT_PACKAGE.yaml",
    "REGULATORY_BASIS.yaml",
    "SPECIAL_CONDITIONS_REGISTER.yaml",
    "REQUIREMENT_TO_REGULATION_MAP.yaml",
    "COMPLIANCE_INTENT_MATRIX.yaml",
    "MEANS_OF_COMPLIANCE_PLAN.yaml",
    "ACCEPTANCE_LOGIC.yaml",
    "EVIDENCE_INTENT_SCHEMA.yaml",
    "OPEN_ISSUES_AND_ASSUMPTIONS.yaml",
    "TRACEABILITY.yaml",
    "CHANGE_CONTROL.yaml",
]

CINT_EVIDENCE_FILES = [
    "evidence/REVIEW_RECORDS.yaml",
    "evidence/signatures/SIGNATURE_MANIFEST.yaml",
    "evidence/signatures/checksums.sha256",
]

DATA_YAML_FILES = [
    "DATA_PACKAGE.yaml",
    "DATA_MODEL.yaml",
    "REQUIREMENT_PARAMETER_DICTIONARY.yaml",
    "REQUIREMENT_DATASETS.yaml",
    "UNITS_AND_CONVERSIONS.yaml",
    "DATA_QUALITY_RULES.yaml",
    "VALIDATION_RULES.yaml",
    "MISSINGNESS_AND_DEFAULT_POLICY.yaml",
    "DATA_LINEAGE_AND_PROVENANCE.yaml",
    "DATA_ACCESS_AND_INTERFACE_POLICY.yaml",
    "DATA_FREEZE_AND_BASELINE_POLICY.yaml",
    "TRACEABILITY.yaml",
    "CHANGE_CONTROL.yaml",
]

DATA_EVIDENCE_FILES = [
    "evidence/DATA_VALIDATION_REPORT.yaml",
    "evidence/DATA_COVERAGE_REPORT.yaml",
    "evidence/signatures/SIGNATURE_MANIFEST.yaml",
    "evidence/signatures/checksums.sha256",
]

ICD_YAML_FILES = [
    "ICD_PACKAGE.yaml",
    "INTERFACE_SCOPE_AND_BOUNDARY.yaml",
    "INTERFACE_CATALOG.yaml",
    "INTERFACE_REQUIREMENTS.yaml",
    "FUNCTIONAL_INTERFACE_CONTRACTS.yaml",
    "DATA_INTERFACE_CONTRACTS.yaml",
    "PHYSICAL_INTERFACE_CONTRACTS.yaml",
    "SAFETY_INTERFACE_CONTRACTS.yaml",
    "TIMING_SYNCHRONIZATION_POLICY.yaml",
    "FAILURE_MODES_AND_FALLBACKS.yaml",
    "ACCEPTANCE_GATES.yaml",
    "VERIFICATION_INTENT.yaml",
    "TRACEABILITY.yaml",
    "CHANGE_CONTROL.yaml",
]

ICD_EVIDENCE_FILES = [
    "evidence/ICD_REVIEW_LOG.yaml",
    "evidence/signatures/SIGNATURE_MANIFEST.yaml",
    "evidence/signatures/checksums.sha256",
]


# =========================================================================
# Helpers
# =========================================================================


def _load(pkg_dir: Path, name: str) -> dict:
    with open(pkg_dir / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


# =========================================================================
# 1. COMPLIANCE_INTENT — Directory structure
# =========================================================================


class TestComplianceIntentStructure:
    """All required COMPLIANCE_INTENT files must exist."""

    def test_dir_exists(self):
        assert CINT_DIR.is_dir()

    def test_readme_exists(self):
        assert (CINT_DIR / "README.md").exists()

    @pytest.mark.parametrize("filename", CINT_YAML_FILES)
    def test_required_yaml_present(self, filename):
        assert (CINT_DIR / filename).exists(), f"Missing: {filename}"

    @pytest.mark.parametrize("filename", CINT_EVIDENCE_FILES)
    def test_evidence_files_present(self, filename):
        assert (CINT_DIR / filename).exists(), f"Missing: {filename}"

    def test_evidence_dir_exists(self):
        assert (CINT_DIR / "evidence").is_dir()

    def test_signatures_dir_exists(self):
        assert (CINT_DIR / "evidence" / "signatures").is_dir()


# =========================================================================
# 2. COMPLIANCE_INTENT — No placeholders
# =========================================================================


class TestComplianceIntentNoPlaceholders:
    """No TBD/TBC/empty required fields in COMPLIANCE_INTENT YAML files."""

    @pytest.mark.parametrize("filename", CINT_YAML_FILES)
    def test_no_tbd_tbc(self, filename):
        text = (CINT_DIR / filename).read_text(encoding="utf-8")
        for placeholder in ("TBD", "TBC", "TODO", "FIXME"):
            assert placeholder not in text, (
                f"{filename} contains placeholder '{placeholder}'"
            )

    @pytest.mark.parametrize("filename", CINT_YAML_FILES)
    def test_yaml_loads(self, filename):
        data = _load(CINT_DIR, filename)
        assert data is not None, f"{filename} parsed as empty"


# =========================================================================
# 3. COMPLIANCE_INTENT_PACKAGE.yaml
# =========================================================================


class TestComplianceIntentPackage:
    """Compliance intent package identity and metadata."""

    @pytest.fixture()
    def data(self):
        return _load(CINT_DIR, "COMPLIANCE_INTENT_PACKAGE.yaml")

    def test_has_package_id(self, data):
        assert data["compliance_intent_package"]["package_id"] == "CINT-LC02-ATA28-11"

    def test_lifecycle_phase(self, data):
        assert data["compliance_intent_package"]["lifecycle_phase"] == "LC02"

    def test_status_ssot(self, data):
        assert data["compliance_intent_package"]["status"] == "SSOT"

    def test_baseline_state(self, data):
        assert data["compliance_intent_package"]["baseline_state"] == "baselined"

    def test_ata_scope(self, data):
        assert "28-11-00" in data["compliance_intent_package"]["ata_scope"]

    def test_owner_role(self, data):
        assert data["compliance_intent_package"]["owner_role"] == "STK_CERT"

    def test_accountable_authority(self, data):
        assert data["compliance_intent_package"]["accountable_authority"] == "CCB"

    def test_version(self, data):
        assert data["compliance_intent_package"]["version"] == "1.0.0"


# =========================================================================
# 4. REGULATORY_BASIS.yaml
# =========================================================================


class TestRegulatoryBasis:
    """Regulatory basis must define primary and supporting standards."""

    @pytest.fixture()
    def data(self):
        return _load(CINT_DIR, "REGULATORY_BASIS.yaml")

    def test_primary_includes_cs25(self, data):
        assert "EASA CS-25" in data["regulatory_basis"]["primary"]

    def test_supporting_not_empty(self, data):
        assert len(data["regulatory_basis"]["supporting"]) >= 3

    def test_authority_engagement_required(self, data):
        assert data["regulatory_basis"]["authority_engagement_required"] is True


# =========================================================================
# 5. REQUIREMENT_TO_REGULATION_MAP.yaml
# =========================================================================


class TestRequirementToRegulationMap:
    """Every requirement must map to at least one regulation."""

    @pytest.fixture()
    def data(self):
        return _load(CINT_DIR, "REQUIREMENT_TO_REGULATION_MAP.yaml")

    def test_entries_not_empty(self, data):
        entries = data["requirement_to_regulation_map"]["entries"]
        assert len(entries) >= 4

    def test_every_entry_has_regulation(self, data):
        for entry in data["requirement_to_regulation_map"]["entries"]:
            assert len(entry["regulations"]) >= 1, (
                f"{entry['req_id']} has no regulation mapping"
            )

    def test_every_entry_has_req_id(self, data):
        for entry in data["requirement_to_regulation_map"]["entries"]:
            assert entry["req_id"].startswith("REQ-28-11-")


# =========================================================================
# 6. COMPLIANCE_INTENT_MATRIX.yaml
# =========================================================================


class TestComplianceIntentMatrix:
    """Every CINT row must have planned MoC and lifecycle targets."""

    @pytest.fixture()
    def data(self):
        return _load(CINT_DIR, "COMPLIANCE_INTENT_MATRIX.yaml")

    def test_policy_is_intent_only(self, data):
        assert data["compliance_intent_matrix"]["policy"] == "intent_level_only"

    def test_rows_not_empty(self, data):
        assert len(data["compliance_intent_matrix"]["rows"]) >= 4

    def test_every_row_has_planned_moc(self, data):
        for row in data["compliance_intent_matrix"]["rows"]:
            assert len(row["planned_moc"]) >= 1, (
                f"{row['cint_id']} has no planned MoC"
            )

    def test_every_row_has_lifecycle_realization(self, data):
        for row in data["compliance_intent_matrix"]["rows"]:
            assert len(row["lifecycle_realization"]) >= 1, (
                f"{row['cint_id']} has no lifecycle realization targets"
            )

    def test_every_row_has_req_id(self, data):
        for row in data["compliance_intent_matrix"]["rows"]:
            assert row["req_id"].startswith("REQ-28-11-")

    def test_every_row_has_cint_id(self, data):
        for row in data["compliance_intent_matrix"]["rows"]:
            assert row["cint_id"].startswith("CINT-")


# =========================================================================
# 7. ACCEPTANCE_LOGIC.yaml
# =========================================================================


class TestAcceptanceLogic:
    """Acceptance logic must define states and release rule."""

    @pytest.fixture()
    def data(self):
        return _load(CINT_DIR, "ACCEPTANCE_LOGIC.yaml")

    def test_states_defined(self, data):
        states = data["acceptance_logic"]["states"]
        for s in ["PASS", "OPEN", "FAIL", "HOLD"]:
            assert s in states

    def test_rules_not_empty(self, data):
        assert len(data["acceptance_logic"]["rules"]) >= 4

    def test_release_rule_present(self, data):
        assert "statement" in data["acceptance_logic"]["release_rule"]

    def test_escalation_path_present(self, data):
        ep = data["acceptance_logic"]["escalation_path"]
        assert "on_HOLD" in ep
        assert "on_FAIL" in ep

    def test_escalation_hold_requires_steward(self, data):
        ep = data["acceptance_logic"]["escalation_path"]
        assert "steward" in ep["on_HOLD"].lower()

    def test_escalation_fail_blocks_merge(self, data):
        ep = data["acceptance_logic"]["escalation_path"]
        assert "block" in ep["on_FAIL"].lower()


# =========================================================================
# 8. MEANS_OF_COMPLIANCE_PLAN.yaml
# =========================================================================


class TestMeansOfCompliancePlan:
    """MoC plan must define taxonomy and cluster assignments."""

    @pytest.fixture()
    def data(self):
        return _load(CINT_DIR, "MEANS_OF_COMPLIANCE_PLAN.yaml")

    def test_taxonomy_not_empty(self, data):
        assert len(data["means_of_compliance_plan"]["moc_taxonomy"]) >= 3

    def test_cluster_plan_not_empty(self, data):
        assert len(data["means_of_compliance_plan"]["cluster_plan"]) >= 4

    def test_every_cluster_has_reqs(self, data):
        for name, cluster in data["means_of_compliance_plan"]["cluster_plan"].items():
            assert len(cluster["reqs"]) >= 1, f"Cluster {name} has no reqs"
            assert len(cluster["moc_mix"]) >= 1, f"Cluster {name} has no moc_mix"


# =========================================================================
# 9. SPECIAL_CONDITIONS_REGISTER.yaml
# =========================================================================


class TestSpecialConditionsRegister:
    """Special conditions must have IDs, titles, and status."""

    @pytest.fixture()
    def data(self):
        return _load(CINT_DIR, "SPECIAL_CONDITIONS_REGISTER.yaml")

    def test_conditions_not_empty(self, data):
        assert len(data["special_conditions_register"]["conditions"]) >= 2

    def test_closure_gate_defined(self, data):
        assert "closure_gate" in data["special_conditions_register"]

    def test_every_sc_has_id(self, data):
        for sc in data["special_conditions_register"]["conditions"]:
            assert sc["sc_id"].startswith("SC-28-")


# =========================================================================
# 10. OPEN_ISSUES_AND_ASSUMPTIONS.yaml
# =========================================================================


class TestOpenIssuesAndAssumptions:
    """Open issues must have owner and target phase."""

    @pytest.fixture()
    def data(self):
        return _load(CINT_DIR, "OPEN_ISSUES_AND_ASSUMPTIONS.yaml")

    def test_open_issues_not_empty(self, data):
        assert len(data["open_issues_and_assumptions"]["open_issues"]) >= 1

    def test_every_issue_has_owner(self, data):
        for oi in data["open_issues_and_assumptions"]["open_issues"]:
            assert "owner" in oi and oi["owner"]

    def test_every_issue_has_target_phase(self, data):
        for oi in data["open_issues_and_assumptions"]["open_issues"]:
            assert "target_phase" in oi and oi["target_phase"]

    def test_assumptions_not_empty(self, data):
        assert len(data["open_issues_and_assumptions"]["assumptions"]) >= 1


# =========================================================================
# 11. COMPLIANCE_INTENT — TRACEABILITY.yaml
# =========================================================================


class TestComplianceIntentTraceability:
    """Traceability must enforce closure."""

    @pytest.fixture()
    def data(self):
        return _load(CINT_DIR, "TRACEABILITY.yaml")

    def test_derives_from_not_empty(self, data):
        assert len(data["traceability"]["derives_from"]) >= 1

    def test_feeds_not_empty(self, data):
        assert len(data["traceability"]["feeds"]) >= 2

    def test_closure_required(self, data):
        assert data["traceability"]["closure_required"] is True

    def test_orphan_policy(self, data):
        assert data["traceability"]["orphan_policy"] == "reject_publish"


# =========================================================================
# 12. COMPLIANCE_INTENT — CHANGE_CONTROL.yaml
# =========================================================================


class TestComplianceIntentChangeControl:
    """Change control must enforce CCB authority and no silent override."""

    @pytest.fixture()
    def data(self):
        return _load(CINT_DIR, "CHANGE_CONTROL.yaml")

    def test_authority_is_ccb(self, data):
        assert data["change_control"]["authority"] == "CCB"

    def test_update_requires_ecr(self, data):
        assert "ECR_ID" in data["change_control"]["update_requires"]

    def test_semantic_versioning(self, data):
        sv = data["change_control"]["semantic_versioning"]
        for key in ("major", "minor", "patch"):
            assert key in sv

    def test_no_silent_override(self, data):
        assert data["change_control"]["silent_override_allowed"] is False


# =========================================================================
# 13. COMPLIANCE_INTENT — README.md
# =========================================================================


class TestComplianceIntentReadme:
    """README must document scope and non-negotiables."""

    @pytest.fixture()
    def text(self):
        return (CINT_DIR / "README.md").read_text(encoding="utf-8")

    def test_title(self, text):
        assert "COMPLIANCE_INTENT" in text

    def test_mentions_moc(self, text):
        assert "MoC" in text

    def test_mentions_silent_overrides(self, text):
        assert "silent override" in text.lower()

    def test_mentions_hold(self, text):
        assert "HOLD" in text


# =========================================================================
# 14. DATA — Directory structure
# =========================================================================


class TestDataStructure:
    """All required DATA files must exist."""

    def test_dir_exists(self):
        assert DATA_DIR.is_dir()

    def test_readme_exists(self):
        assert (DATA_DIR / "README.md").exists()

    @pytest.mark.parametrize("filename", DATA_YAML_FILES)
    def test_required_yaml_present(self, filename):
        assert (DATA_DIR / filename).exists(), f"Missing: {filename}"

    @pytest.mark.parametrize("filename", DATA_EVIDENCE_FILES)
    def test_evidence_files_present(self, filename):
        assert (DATA_DIR / filename).exists(), f"Missing: {filename}"

    def test_evidence_dir_exists(self):
        assert (DATA_DIR / "evidence").is_dir()

    def test_signatures_dir_exists(self):
        assert (DATA_DIR / "evidence" / "signatures").is_dir()


# =========================================================================
# 15. DATA — No placeholders
# =========================================================================


class TestDataNoPlaceholders:
    """No TBD/TBC/empty required fields in DATA YAML files."""

    @pytest.mark.parametrize("filename", DATA_YAML_FILES)
    def test_no_tbd_tbc(self, filename):
        text = (DATA_DIR / filename).read_text(encoding="utf-8")
        for placeholder in ("TBD", "TBC", "TODO", "FIXME"):
            assert placeholder not in text, (
                f"{filename} contains placeholder '{placeholder}'"
            )

    @pytest.mark.parametrize("filename", DATA_YAML_FILES)
    def test_yaml_loads(self, filename):
        data = _load(DATA_DIR, filename)
        assert data is not None, f"{filename} parsed as empty"


# =========================================================================
# 16. DATA_PACKAGE.yaml
# =========================================================================


class TestDataPackage:
    """Data package identity and metadata."""

    @pytest.fixture()
    def data(self):
        return _load(DATA_DIR, "DATA_PACKAGE.yaml")

    def test_has_package_id(self, data):
        assert data["data_package"]["package_id"] == "DATA-LC02-ATA28-11"

    def test_lifecycle_phase(self, data):
        assert data["data_package"]["lifecycle_phase"] == "LC02"

    def test_status_ssot(self, data):
        assert data["data_package"]["status"] == "SSOT"

    def test_baseline_state(self, data):
        assert data["data_package"]["baseline_state"] == "baselined"

    def test_ata_scope(self, data):
        assert "28-11-00" in data["data_package"]["ata_scope"]

    def test_owner_role(self, data):
        assert data["data_package"]["owner_role"] == "STK_ENG"

    def test_data_authority(self, data):
        assert data["data_package"]["data_authority"] == "STK_CM"

    def test_version(self, data):
        assert data["data_package"]["version"] == "1.0.0"

    def test_constitutional_constraints_present(self, data):
        cc = data["data_package"]["constitutional_constraints"]
        assert cc["human_authorization_required_for_override"] is True

    def test_harm_precedence_threshold(self, data):
        cc = data["data_package"]["constitutional_constraints"]
        assert cc["harm_precedence_threshold"] >= 0.9

    def test_constitution_version(self, data):
        cc = data["data_package"]["constitutional_constraints"]
        assert cc["constitution_version"] == "v1.0"


# =========================================================================
# 17. DATA_MODEL.yaml
# =========================================================================


class TestDataModel:
    """Data model must define entities and relations."""

    @pytest.fixture()
    def data(self):
        return _load(DATA_DIR, "DATA_MODEL.yaml")

    def test_model_id(self, data):
        assert data["data_model"]["model_id"] == "DM-LC02-ATA28-11"

    def test_entities_not_empty(self, data):
        assert len(data["data_model"]["entities"]) >= 3

    def test_relations_not_empty(self, data):
        assert len(data["data_model"]["relations"]) >= 2

    def test_every_entity_has_primary_key(self, data):
        for entity in data["data_model"]["entities"]:
            assert "primary_key" in entity
            assert "required_fields" in entity


# =========================================================================
# 18. REQUIREMENT_PARAMETER_DICTIONARY.yaml
# =========================================================================


class TestParameterDictionary:
    """Parameter dictionary must have well-formed entries."""

    @pytest.fixture()
    def data(self):
        return _load(DATA_DIR, "REQUIREMENT_PARAMETER_DICTIONARY.yaml")

    def test_parameters_not_empty(self, data):
        params = data["requirement_parameter_dictionary"]["parameters"]
        assert len(params) >= 5

    def test_every_param_has_required_fields(self, data):
        for p in data["requirement_parameter_dictionary"]["parameters"]:
            for field in ("param_id", "name", "unit", "data_type", "valid_range", "precision"):
                assert field in p, f"Parameter {p.get('param_id', '?')} missing {field}"

    def test_param_ids_well_formed(self, data):
        import re
        for p in data["requirement_parameter_dictionary"]["parameters"]:
            assert re.match(r"^P-28-11-\d{3}$", p["param_id"]), (
                f"Malformed param_id: {p['param_id']}"
            )

    def test_param_ids_unique(self, data):
        ids = [p["param_id"] for p in data["requirement_parameter_dictionary"]["parameters"]]
        assert len(ids) == len(set(ids))


# =========================================================================
# 19. DATA_QUALITY_RULES.yaml
# =========================================================================


class TestDataQualityRules:
    """Quality rules must enforce 100% thresholds."""

    @pytest.fixture()
    def data(self):
        return _load(DATA_DIR, "DATA_QUALITY_RULES.yaml")

    def test_dimensions_not_empty(self, data):
        assert len(data["data_quality_rules"]["dimensions"]) >= 5

    def test_thresholds_all_100(self, data):
        thresholds = data["data_quality_rules"]["thresholds"]
        for key, val in thresholds.items():
            assert val == 1.00, f"Threshold {key} is {val}, expected 1.00"

    def test_on_fail_action(self, data):
        assert data["data_quality_rules"]["on_fail"] == "REJECT_DATASET_AND_OPEN_ECR"


# =========================================================================
# 20. UNITS_AND_CONVERSIONS.yaml
# =========================================================================


class TestUnitsAndConversions:
    """Units policy must enforce SI canonical system."""

    @pytest.fixture()
    def data(self):
        return _load(DATA_DIR, "UNITS_AND_CONVERSIONS.yaml")

    def test_canonical_is_si(self, data):
        assert data["units_and_conversions"]["canonical_unit_system"] == "SI"

    def test_rules_not_empty(self, data):
        assert len(data["units_and_conversions"]["rules"]) >= 2

    def test_conversions_defined(self, data):
        assert len(data["units_and_conversions"]["conversions"]) >= 2


# =========================================================================
# 21. DATA — TRACEABILITY.yaml
# =========================================================================


class TestDataTraceability:
    """Traceability must enforce closure."""

    @pytest.fixture()
    def data(self):
        return _load(DATA_DIR, "TRACEABILITY.yaml")

    def test_derives_from_not_empty(self, data):
        assert len(data["traceability"]["derives_from"]) >= 1

    def test_feeds_not_empty(self, data):
        assert len(data["traceability"]["feeds"]) >= 2

    def test_mandatory_links_not_empty(self, data):
        assert len(data["traceability"]["mandatory_links"]) >= 4

    def test_closure_required(self, data):
        assert data["traceability"]["closure_required"] is True

    def test_orphan_policy(self, data):
        assert data["traceability"]["orphan_policy"] == "reject_publish"


# =========================================================================
# 22. DATA — CHANGE_CONTROL.yaml
# =========================================================================


class TestDataChangeControl:
    """Change control must enforce CCB authority and no silent override."""

    @pytest.fixture()
    def data(self):
        return _load(DATA_DIR, "CHANGE_CONTROL.yaml")

    def test_authority_is_ccb(self, data):
        assert data["change_control"]["authority"] == "CCB"

    def test_update_requires_ecr(self, data):
        assert "ECR_ID" in data["change_control"]["update_requires"]

    def test_no_silent_override(self, data):
        assert data["change_control"]["silent_override_allowed"] is False


# =========================================================================
# 23. DATA — README.md
# =========================================================================


class TestDataReadme:
    """README must document scope and non-negotiables."""

    @pytest.fixture()
    def text(self):
        return (DATA_DIR / "README.md").read_text(encoding="utf-8")

    def test_title(self, text):
        assert "DATA" in text

    def test_mentions_si(self, text):
        assert "SI" in text

    def test_mentions_provenance(self, text):
        assert "provenance" in text.lower()

    def test_mentions_no_silent_defaults(self, text):
        assert "silent default" in text.lower()


# =========================================================================
# 24. ICD — Directory structure
# =========================================================================


class TestIcdStructure:
    """All required ICD files must exist."""

    def test_dir_exists(self):
        assert ICD_DIR.is_dir()

    def test_readme_exists(self):
        assert (ICD_DIR / "README.md").exists()

    @pytest.mark.parametrize("filename", ICD_YAML_FILES)
    def test_required_yaml_present(self, filename):
        assert (ICD_DIR / filename).exists(), f"Missing: {filename}"

    @pytest.mark.parametrize("filename", ICD_EVIDENCE_FILES)
    def test_evidence_files_present(self, filename):
        assert (ICD_DIR / filename).exists(), f"Missing: {filename}"

    def test_evidence_dir_exists(self):
        assert (ICD_DIR / "evidence").is_dir()

    def test_signatures_dir_exists(self):
        assert (ICD_DIR / "evidence" / "signatures").is_dir()


# =========================================================================
# 25. ICD — No placeholders
# =========================================================================


class TestIcdNoPlaceholders:
    """No TBD/TBC/empty required fields in ICD YAML files."""

    @pytest.mark.parametrize("filename", ICD_YAML_FILES)
    def test_no_tbd_tbc(self, filename):
        text = (ICD_DIR / filename).read_text(encoding="utf-8")
        for placeholder in ("TBD", "TBC", "TODO", "FIXME"):
            assert placeholder not in text, (
                f"{filename} contains placeholder '{placeholder}'"
            )

    @pytest.mark.parametrize("filename", ICD_YAML_FILES)
    def test_yaml_loads(self, filename):
        data = _load(ICD_DIR, filename)
        assert data is not None, f"{filename} parsed as empty"


# =========================================================================
# 26. ICD_PACKAGE.yaml
# =========================================================================


class TestIcdPackage:
    """ICD package identity and metadata."""

    @pytest.fixture()
    def data(self):
        return _load(ICD_DIR, "ICD_PACKAGE.yaml")

    def test_has_package_id(self, data):
        assert data["icd_package"]["package_id"] == "ICD-LC02-ATA28-11"

    def test_lifecycle_phase(self, data):
        assert data["icd_package"]["lifecycle_phase"] == "LC02"

    def test_status_ssot(self, data):
        assert data["icd_package"]["status"] == "SSOT"

    def test_baseline_state(self, data):
        assert data["icd_package"]["baseline_state"] == "baselined"

    def test_ata_scope(self, data):
        assert "28-11-00" in data["icd_package"]["ata_scope"]

    def test_owner_role(self, data):
        assert data["icd_package"]["owner_role"] == "STK_SYS"

    def test_interface_authority(self, data):
        assert data["icd_package"]["interface_authority"] == "STK_CM"

    def test_version(self, data):
        assert data["icd_package"]["version"] == "1.0.0"


# =========================================================================
# 27. INTERFACE_CATALOG.yaml
# =========================================================================


class TestInterfaceCatalog:
    """Interface catalog must have well-formed entries."""

    @pytest.fixture()
    def data(self):
        return _load(ICD_DIR, "INTERFACE_CATALOG.yaml")

    def test_interfaces_not_empty(self, data):
        assert len(data["interface_catalog"]["interfaces"]) >= 5

    def test_every_interface_has_required_fields(self, data):
        for iface in data["interface_catalog"]["interfaces"]:
            for field in ("if_id", "name", "type", "endpoints", "criticality"):
                assert field in iface, f"Interface {iface.get('if_id', '?')} missing {field}"

    def test_if_ids_well_formed(self, data):
        import re
        for iface in data["interface_catalog"]["interfaces"]:
            assert re.match(r"^IF-28-11-\d{2}-\d{3}$", iface["if_id"]), (
                f"Malformed if_id: {iface['if_id']}"
            )

    def test_if_ids_unique(self, data):
        ids = [i["if_id"] for i in data["interface_catalog"]["interfaces"]]
        assert len(ids) == len(set(ids))


# =========================================================================
# 28. INTERFACE_REQUIREMENTS.yaml
# =========================================================================


class TestInterfaceRequirements:
    """Interface requirements must link to catalog entries."""

    @pytest.fixture()
    def data(self):
        return _load(ICD_DIR, "INTERFACE_REQUIREMENTS.yaml")

    def test_requirements_not_empty(self, data):
        assert len(data["interface_requirements"]["requirements"]) >= 4

    def test_every_req_has_if_id(self, data):
        for req in data["interface_requirements"]["requirements"]:
            assert req["if_id"].startswith("IF-28-11-")

    def test_every_req_has_acceptance_ref(self, data):
        for req in data["interface_requirements"]["requirements"]:
            assert "acceptance_ref" in req


# =========================================================================
# 29. DATA_INTERFACE_CONTRACTS.yaml — signals
# =========================================================================


class TestDataInterfaceContracts:
    """Data interface signals must have units and quality flags."""

    @pytest.fixture()
    def data(self):
        return _load(ICD_DIR, "DATA_INTERFACE_CONTRACTS.yaml")

    def test_signals_not_empty(self, data):
        assert len(data["data_interface_contracts"]["signals"]) >= 3

    def test_every_signal_has_required_fields(self, data):
        for sig in data["data_interface_contracts"]["signals"]:
            for field in ("signal_id", "if_id", "unit", "data_type", "valid_range", "quality_flags"):
                assert field in sig, f"Signal {sig.get('signal_id', '?')} missing {field}"


# =========================================================================
# 30. SAFETY_INTERFACE_CONTRACTS.yaml
# =========================================================================


class TestSafetyInterfaceContracts:
    """Safety contracts must have DAL classification."""

    @pytest.fixture()
    def data(self):
        return _load(ICD_DIR, "SAFETY_INTERFACE_CONTRACTS.yaml")

    def test_contracts_not_empty(self, data):
        assert len(data["safety_interface_contracts"]["contracts"]) >= 2

    def test_every_contract_has_dal(self, data):
        for c in data["safety_interface_contracts"]["contracts"]:
            assert "dal" in c, f"Contract {c.get('contract_id', '?')} missing DAL"

    def test_dal_a_contracts_have_human_in_the_loop(self, data):
        for c in data["safety_interface_contracts"]["contracts"]:
            if c["dal"] == "A":
                assert "human_in_the_loop" in c, (
                    f"DAL-A contract {c['contract_id']} missing human_in_the_loop"
                )

    def test_human_in_the_loop_has_required_fields(self, data):
        for c in data["safety_interface_contracts"]["contracts"]:
            if "human_in_the_loop" in c:
                hitl = c["human_in_the_loop"]
                assert "autonomous_action_limit" in hitl
                assert "human_authorization_required_for" in hitl
                assert "escalation_timeout_seconds" in hitl

    def test_autonomous_action_limit_is_alert_only(self, data):
        for c in data["safety_interface_contracts"]["contracts"]:
            if "human_in_the_loop" in c:
                assert c["human_in_the_loop"]["autonomous_action_limit"] == "alert_only"


# =========================================================================
# 31. FAILURE_MODES_AND_FALLBACKS.yaml
# =========================================================================


class TestFailureModesAndFallbacks:
    """Failure modes must have severity and fallback."""

    @pytest.fixture()
    def data(self):
        return _load(ICD_DIR, "FAILURE_MODES_AND_FALLBACKS.yaml")

    def test_failures_not_empty(self, data):
        assert len(data["failure_modes_and_fallbacks"]["interface_failures"]) >= 4

    def test_every_failure_has_severity(self, data):
        for f in data["failure_modes_and_fallbacks"]["interface_failures"]:
            assert "severity" in f

    def test_every_failure_has_fallback(self, data):
        for f in data["failure_modes_and_fallbacks"]["interface_failures"]:
            assert "fallback" in f


# =========================================================================
# 32. ICD — TRACEABILITY.yaml
# =========================================================================


class TestIcdTraceability:
    """Traceability must enforce closure."""

    @pytest.fixture()
    def data(self):
        return _load(ICD_DIR, "TRACEABILITY.yaml")

    def test_derives_from_not_empty(self, data):
        assert len(data["traceability"]["derives_from"]) >= 1

    def test_feeds_not_empty(self, data):
        assert len(data["traceability"]["feeds"]) >= 2

    def test_mandatory_links_not_empty(self, data):
        assert len(data["traceability"]["mandatory_links"]) >= 3

    def test_closure_required(self, data):
        assert data["traceability"]["closure_required"] is True

    def test_orphan_policy(self, data):
        assert data["traceability"]["orphan_policy"] == "reject_publish"


# =========================================================================
# 33. ICD — CHANGE_CONTROL.yaml
# =========================================================================


class TestIcdChangeControl:
    """Change control must enforce CCB authority and no silent override."""

    @pytest.fixture()
    def data(self):
        return _load(ICD_DIR, "CHANGE_CONTROL.yaml")

    def test_authority_is_ccb(self, data):
        assert data["change_control"]["authority"] == "CCB"

    def test_update_requires_ecr(self, data):
        assert "ECR_ID" in data["change_control"]["update_requires"]

    def test_no_silent_override(self, data):
        assert data["change_control"]["silent_override_allowed"] is False


# =========================================================================
# 34. ICD — README.md
# =========================================================================


class TestIcdReadme:
    """README must document scope and non-negotiables."""

    @pytest.fixture()
    def text(self):
        return (ICD_DIR / "README.md").read_text(encoding="utf-8")

    def test_title(self, text):
        assert "ICD" in text

    def test_mentions_interface(self, text):
        assert "interface" in text.lower()

    def test_mentions_no_silent_overrides(self, text):
        assert "silent override" in text.lower()

    def test_mentions_safety(self, text):
        assert "safety" in text.lower()


# =========================================================================
# 35. Cross-package consistency
# =========================================================================


class TestCrossPackageConsistency:
    """Cross-package linkage and consistency checks."""

    def test_cint_req_ids_match_regulation_map(self):
        """Every req_id in COMPLIANCE_INTENT_MATRIX maps to REQUIREMENT_TO_REGULATION_MAP."""
        matrix = _load(CINT_DIR, "COMPLIANCE_INTENT_MATRIX.yaml")
        reg_map = _load(CINT_DIR, "REQUIREMENT_TO_REGULATION_MAP.yaml")

        map_req_ids = {e["req_id"] for e in reg_map["requirement_to_regulation_map"]["entries"]}
        for row in matrix["compliance_intent_matrix"]["rows"]:
            assert row["req_id"] in map_req_ids, (
                f"CINT row {row['cint_id']} references {row['req_id']} not in regulation map"
            )

    def test_moc_cluster_reqs_match_regulation_map(self):
        """Every req in MoC cluster plan exists in the regulation map."""
        moc = _load(CINT_DIR, "MEANS_OF_COMPLIANCE_PLAN.yaml")
        reg_map = _load(CINT_DIR, "REQUIREMENT_TO_REGULATION_MAP.yaml")

        map_req_ids = {e["req_id"] for e in reg_map["requirement_to_regulation_map"]["entries"]}
        for name, cluster in moc["means_of_compliance_plan"]["cluster_plan"].items():
            for req_id in cluster["reqs"]:
                assert req_id in map_req_ids, (
                    f"Cluster {name} references {req_id} not in regulation map"
                )

    def test_icd_acceptance_refs_match_gates(self):
        """Every acceptance_ref in ICD requirements maps to ACCEPTANCE_GATES."""
        reqs = _load(ICD_DIR, "INTERFACE_REQUIREMENTS.yaml")
        gates = _load(ICD_DIR, "ACCEPTANCE_GATES.yaml")

        gate_ids = {g["gate_id"] for g in gates["acceptance_gates"]["gates"]}
        for req in reqs["interface_requirements"]["requirements"]:
            assert req["acceptance_ref"] in gate_ids, (
                f"IFR {req['if_req_id']} references gate {req['acceptance_ref']} not found"
            )

    def test_icd_signals_link_to_catalog(self):
        """Every signal if_id references an interface in the catalog."""
        signals = _load(ICD_DIR, "DATA_INTERFACE_CONTRACTS.yaml")
        catalog = _load(ICD_DIR, "INTERFACE_CATALOG.yaml")

        catalog_ids = {i["if_id"] for i in catalog["interface_catalog"]["interfaces"]}
        for sig in signals["data_interface_contracts"]["signals"]:
            assert sig["if_id"] in catalog_ids, (
                f"Signal {sig['signal_id']} references {sig['if_id']} not in catalog"
            )

    def test_all_three_packages_are_lc02(self):
        """All three packages declare LC02 lifecycle phase."""
        cint = _load(CINT_DIR, "COMPLIANCE_INTENT_PACKAGE.yaml")
        data_pkg = _load(DATA_DIR, "DATA_PACKAGE.yaml")
        icd = _load(ICD_DIR, "ICD_PACKAGE.yaml")

        assert cint["compliance_intent_package"]["lifecycle_phase"] == "LC02"
        assert data_pkg["data_package"]["lifecycle_phase"] == "LC02"
        assert icd["icd_package"]["lifecycle_phase"] == "LC02"

    def test_all_three_packages_are_ssot(self):
        """All three packages declare SSOT status."""
        cint = _load(CINT_DIR, "COMPLIANCE_INTENT_PACKAGE.yaml")
        data_pkg = _load(DATA_DIR, "DATA_PACKAGE.yaml")
        icd = _load(ICD_DIR, "ICD_PACKAGE.yaml")

        assert cint["compliance_intent_package"]["status"] == "SSOT"
        assert data_pkg["data_package"]["status"] == "SSOT"
        assert icd["icd_package"]["status"] == "SSOT"
