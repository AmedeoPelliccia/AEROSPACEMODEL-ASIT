"""
Tests for the Meta Transformation Layers (MTL) Core Standard.

Validates the MTL_META_STANDARD_v1.0.0.yaml, MTL_META_BREX.yaml,
and README.md artifacts in ASIT/STANDARDS/MTL_META/.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
META_DIR = REPO_ROOT / "ASIT" / "STANDARDS" / "MTL_META"
STANDARD_FILE = "MTL_META_STANDARD_v1.0.0.yaml"
BREX_FILE = "MTL_META_BREX.yaml"


# =========================================================================
# Directory and Files
# =========================================================================


class TestMetaDirectory:
    """MTL_META directory must contain the expected files."""

    def test_directory_exists(self):
        assert META_DIR.is_dir()

    def test_readme_exists(self):
        assert (META_DIR / "README.md").exists()

    def test_standard_yaml_exists(self):
        assert (META_DIR / STANDARD_FILE).exists()

    def test_brex_yaml_exists(self):
        assert (META_DIR / BREX_FILE).exists()


# =========================================================================
# Standard YAML — Metadata
# =========================================================================


class TestStandardMetadata:
    """Standard YAML must have required metadata."""

    @pytest.fixture()
    def data(self):
        with open(META_DIR / STANDARD_FILE) as f:
            return yaml.safe_load(f)

    def test_yaml_parses(self, data):
        assert data is not None

    def test_standard_id(self, data):
        assert data["metadata"]["standard_id"] == "MTL-META-CORE"

    def test_version(self, data):
        assert data["metadata"]["version"] == "1.0.0"

    def test_status(self, data):
        assert data["metadata"]["status"] in ("DRAFT", "REVIEW", "APPROVED", "ACTIVE")

    def test_determinism_strict(self, data):
        assert data["metadata"]["determinism_level"] == "strict"

    def test_compliance_list(self, data):
        c = data["metadata"]["compliance"]
        assert isinstance(c, list) and len(c) >= 1


# =========================================================================
# Standard YAML — Layers
# =========================================================================


EXPECTED_LAYERS = ["L5", "L4", "L3", "L2", "L1"]


class TestStandardLayers:
    """Standard must define exactly five layers with patterns."""

    @pytest.fixture()
    def data(self):
        with open(META_DIR / STANDARD_FILE) as f:
            return yaml.safe_load(f)

    def test_five_layers(self, data):
        assert len(data["layers"]) == 5

    def test_layer_ids(self, data):
        ids = [l["id"] for l in data["layers"]]
        assert ids == EXPECTED_LAYERS

    def test_each_layer_has_pattern(self, data):
        for layer in data["layers"]:
            assert "token_pattern" in layer, f"{layer['id']} missing token_pattern"

    def test_each_layer_has_name(self, data):
        for layer in data["layers"]:
            assert "name" in layer, f"{layer['id']} missing name"

    def test_each_layer_has_purpose(self, data):
        for layer in data["layers"]:
            assert "purpose" in layer, f"{layer['id']} missing purpose"

    def test_each_layer_has_examples(self, data):
        for layer in data["layers"]:
            assert len(layer.get("examples", [])) >= 1, f"{layer['id']} missing examples"


# =========================================================================
# Standard YAML — Token Contract
# =========================================================================


class TestTokenContract:
    """Token contract must define core, governance, trace, and layer-specific fields."""

    @pytest.fixture()
    def data(self):
        with open(META_DIR / STANDARD_FILE) as f:
            return yaml.safe_load(f)

    def test_has_token_contract(self, data):
        assert "token_contract" in data

    def test_core_required_fields(self, data):
        fields = data["token_contract"]["core_required_fields"]
        for name in ("token_id", "layer", "name", "intent", "acceptance_gates", "governance"):
            assert name in fields, f"Core field '{name}' missing"

    def test_governance_required_fields(self, data):
        fields = data["token_contract"]["governance_required_fields"]
        for name in ("owner_role", "status", "version"):
            assert name in fields, f"Governance field '{name}' missing"

    def test_trace_required_fields(self, data):
        fields = data["token_contract"]["trace_required_fields"]
        for name in ("derives_from", "feeds"):
            assert name in fields, f"Trace field '{name}' missing"

    def test_layer_specific_fields_all_layers(self, data):
        lsf = data["token_contract"]["layer_specific_fields"]
        for layer in EXPECTED_LAYERS:
            assert layer in lsf, f"Layer-specific fields missing for {layer}"
            assert isinstance(lsf[layer], list) and len(lsf[layer]) >= 1

    def test_l2_requires_method_class(self, data):
        lsf = data["token_contract"]["layer_specific_fields"]
        assert "method_class" in lsf["L2"]

    def test_l3_requires_procedure_steps(self, data):
        lsf = data["token_contract"]["layer_specific_fields"]
        assert "procedure_steps" in lsf["L3"]


# =========================================================================
# Standard YAML — Method Classes
# =========================================================================


EXPECTED_CLASSES = [
    "GEOM", "KIN", "DYN", "THRM", "MATL", "CTRL",
    "QUAL", "SAFE", "CERT", "EVAL", "OPS", "MRO",
]


class TestMethodClasses:
    """L2 method-class taxonomy must contain the 12 canonical classes."""

    @pytest.fixture()
    def data(self):
        with open(META_DIR / STANDARD_FILE) as f:
            return yaml.safe_load(f)

    def test_twelve_classes(self, data):
        assert len(data["method_classes"]["classes"]) == 12

    def test_class_ids(self, data):
        ids = [c["id"] for c in data["method_classes"]["classes"]]
        assert ids == EXPECTED_CLASSES


# =========================================================================
# Standard YAML — Invariants
# =========================================================================


class TestInvariants:
    """Standard must define the four global invariants."""

    @pytest.fixture()
    def data(self):
        with open(META_DIR / STANDARD_FILE) as f:
            return yaml.safe_load(f)

    def test_four_invariants(self, data):
        assert len(data["invariants"]["rules"]) == 4

    def test_invariant_ids(self, data):
        ids = [r["id"] for r in data["invariants"]["rules"]]
        for inv in ("INV-001", "INV-002", "INV-003", "INV-004"):
            assert inv in ids


# =========================================================================
# Standard YAML — Governance Policies
# =========================================================================


class TestGovernancePolicies:
    """Standard must define the four governance policies."""

    @pytest.fixture()
    def data(self):
        with open(META_DIR / STANDARD_FILE) as f:
            return yaml.safe_load(f)

    def test_four_policies(self, data):
        assert len(data["governance"]["policies"]) == 4

    def test_policy_ids(self, data):
        ids = [p["id"] for p in data["governance"]["policies"]]
        for gov in ("GOV-001", "GOV-002", "GOV-003", "GOV-004"):
            assert gov in ids


# =========================================================================
# Standard YAML — Domain Profiles
# =========================================================================


class TestDomainProfiles:
    """Standard must define at least 5 domain profiles."""

    @pytest.fixture()
    def data(self):
        with open(META_DIR / STANDARD_FILE) as f:
            return yaml.safe_load(f)

    def test_profile_count(self, data):
        profiles = data["domain_profiles"]["profiles"]
        assert len(profiles) >= 5

    def test_aero_profile(self, data):
        ids = [p["profile_id"] for p in data["domain_profiles"]["profiles"]]
        assert "AERO" in ids

    def test_rob_profile_alias(self, data):
        rob = [p for p in data["domain_profiles"]["profiles"] if p["profile_id"] == "ROB"]
        assert len(rob) == 1
        assert rob[0].get("alias") == "Motion Transmission Lever"


# =========================================================================
# Standard YAML — ATA 28-11 Backward Compatibility
# =========================================================================


class TestBackwardCompatibility:
    """Standard must map layers to existing ATA 28-11 5D equivalents."""

    @pytest.fixture()
    def data(self):
        with open(META_DIR / STANDARD_FILE) as f:
            return yaml.safe_load(f)

    def test_has_compatibility_section(self, data):
        assert "compatibility" in data

    def test_all_layers_mapped(self, data):
        lm = data["compatibility"]["ata_28_mapping"]["layer_map"]
        for layer in EXPECTED_LAYERS:
            assert layer in lm, f"Layer {layer} not mapped"


# =========================================================================
# Standard YAML — Decision States
# =========================================================================


EXPECTED_STATES = ["ALLOW", "HOLD", "REJECT", "ESCALATE"]


class TestDecisionStates:
    """Standard must define a deterministic decision state machine."""

    @pytest.fixture()
    def data(self):
        with open(META_DIR / STANDARD_FILE) as f:
            return yaml.safe_load(f)

    def test_has_decision_states(self, data):
        assert "decision_states" in data

    def test_four_states(self, data):
        assert data["decision_states"]["allowed_states"] == EXPECTED_STATES

    def test_has_transition_rules(self, data):
        rules = data["decision_states"]["transition_rules"]
        assert isinstance(rules, list) and len(rules) >= 4

    def test_each_transition_has_when_then(self, data):
        for rule in data["decision_states"]["transition_rules"]:
            assert "when" in rule, "Transition rule missing 'when'"
            assert "then" in rule, "Transition rule missing 'then'"

    def test_all_then_values_are_valid_states(self, data):
        for rule in data["decision_states"]["transition_rules"]:
            assert rule["then"] in EXPECTED_STATES, f"Invalid state: {rule['then']}"


# =========================================================================
# Standard YAML — Backward Mapping Rules
# =========================================================================


class TestBackwardMappingRules:
    """Standard must provide regex-based backward mapping for ATA 28-11 IDs."""

    @pytest.fixture()
    def data(self):
        with open(META_DIR / STANDARD_FILE) as f:
            return yaml.safe_load(f)

    def test_has_backward_mapping_rules(self, data):
        assert "backward_mapping_rules" in data["compatibility"]

    def test_five_mapping_rules(self, data):
        rules = data["compatibility"]["backward_mapping_rules"]["rules"]
        assert len(rules) == 5

    def test_each_rule_has_regex_and_pattern(self, data):
        for rule in data["compatibility"]["backward_mapping_rules"]["rules"]:
            assert "from_regex" in rule, "Mapping rule missing from_regex"
            assert "to_pattern" in rule, "Mapping rule missing to_pattern"

    def test_sdr_regex_compiles(self, data):
        rules = data["compatibility"]["backward_mapping_rules"]["rules"]
        sdr = [r for r in rules if r["to_pattern"].startswith("CTX-")]
        assert len(sdr) == 1
        compiled = re.compile(sdr[0]["from_regex"])
        assert compiled.groups >= 1, "Regex must have at least one capture group"

    def test_sdr_regex_matches_legacy(self, data):
        rules = data["compatibility"]["backward_mapping_rules"]["rules"]
        sdr = [r for r in rules if r["to_pattern"].startswith("CTX-")][0]
        assert re.match(sdr["from_regex"], "SDR-28")

    def test_scr_regex_matches_legacy(self, data):
        rules = data["compatibility"]["backward_mapping_rules"]["rules"]
        scr = [r for r in rules if r["to_pattern"].startswith("STR-")][0]
        assert re.match(scr["from_regex"], "SCR-28-11")

    def test_stp_regex_matches_legacy(self, data):
        rules = data["compatibility"]["backward_mapping_rules"]["rules"]
        stp = [r for r in rules if r["to_pattern"].startswith("PRC-")][0]
        assert re.match(stp["from_regex"], "STP-28-11-001")

    def test_mtp_regex_matches_legacy(self, data):
        rules = data["compatibility"]["backward_mapping_rules"]["rules"]
        mtp = [r for r in rules if r["to_pattern"].startswith("XFM-")][0]
        assert re.match(mtp["from_regex"], "MTP-28-11-GEOM-001")

    def test_mtk_regex_matches_legacy(self, data):
        rules = data["compatibility"]["backward_mapping_rules"]["rules"]
        mtk = [r for r in rules if r["to_pattern"].startswith("SBJ-")][0]
        assert re.match(mtk["from_regex"], "MTK-28-11-TS-001")


# =========================================================================
# Standard YAML — Summary
# =========================================================================


class TestStandardSummary:
    """Summary counts must match actual data."""

    @pytest.fixture()
    def data(self):
        with open(META_DIR / STANDARD_FILE) as f:
            return yaml.safe_load(f)

    def test_total_layers(self, data):
        assert data["summary"]["total_layers"] == len(data["layers"])

    def test_total_method_classes(self, data):
        assert data["summary"]["total_method_classes"] == len(data["method_classes"]["classes"])

    def test_total_invariants(self, data):
        assert data["summary"]["total_invariants"] == len(data["invariants"]["rules"])

    def test_total_governance_policies(self, data):
        assert data["summary"]["total_governance_policies"] == len(data["governance"]["policies"])

    def test_total_domain_profiles(self, data):
        assert data["summary"]["total_domain_profiles"] == len(
            data["domain_profiles"]["profiles"]
        )

    def test_total_decision_states(self, data):
        assert data["summary"]["total_decision_states"] == len(
            data["decision_states"]["allowed_states"]
        )

    def test_total_backward_mapping_rules(self, data):
        assert data["summary"]["total_backward_mapping_rules"] == len(
            data["compatibility"]["backward_mapping_rules"]["rules"]
        )


# =========================================================================
# Standard YAML — Learning Rule
# =========================================================================


class TestLearningRule:
    """Standard must define the canonical learning rule."""

    @pytest.fixture()
    def data(self):
        with open(META_DIR / STANDARD_FILE) as f:
            return yaml.safe_load(f)

    def test_has_learning_rule(self, data):
        assert "learning_rule" in data

    def test_has_statement(self, data):
        assert "statement" in data["learning_rule"]

    def test_has_benefits(self, data):
        assert len(data["learning_rule"]["benefits"]) >= 4


# =========================================================================
# BREX YAML — Metadata
# =========================================================================


class TestBREXMetadata:
    """BREX YAML must have required metadata."""

    @pytest.fixture()
    def data(self):
        with open(META_DIR / BREX_FILE) as f:
            return yaml.safe_load(f)

    def test_yaml_parses(self, data):
        assert data is not None

    def test_brex_id(self, data):
        assert data["metadata"]["brex_id"] == "MTL-META-BREX-001"

    def test_references_standard(self, data):
        assert "MTL-META-CORE" in data["metadata"]["standard_reference"]

    def test_references_parent_authority(self, data):
        assert data["metadata"]["parent_authority"] == "ASIT-BREX-MASTER-001"


# =========================================================================
# BREX YAML — Rule Categories
# =========================================================================


class TestBREXRuleCategories:
    """BREX must define rules in all required categories."""

    @pytest.fixture()
    def data(self):
        with open(META_DIR / BREX_FILE) as f:
            return yaml.safe_load(f)

    def test_has_structure_rules(self, data):
        assert len(data["structure_rules"]) >= 3

    def test_has_contract_rules(self, data):
        assert len(data["contract_rules"]) >= 9

    def test_has_traceability_rules(self, data):
        assert len(data["traceability_rules"]) >= 3

    def test_has_governance_rules(self, data):
        assert len(data["governance_rules"]) >= 4

    def test_has_safety_rules(self, data):
        assert len(data["safety_rules"]) >= 3

    def test_has_lifecycle_rules(self, data):
        assert len(data["lifecycle_rules"]) >= 3

    def test_has_learning_rules(self, data):
        assert len(data["learning_rules"]) >= 3


# =========================================================================
# BREX YAML — Token Pattern Regex
# =========================================================================


class TestBREXPatterns:
    """BREX structure rules must provide valid regex for each layer."""

    @pytest.fixture()
    def data(self):
        with open(META_DIR / BREX_FILE) as f:
            return yaml.safe_load(f)

    def _patterns(self, data):
        rule = [r for r in data["structure_rules"] if r["id"] == "MTL-STRUCT-002"]
        assert len(rule) == 1
        return rule[0]["patterns"]

    def test_l5_pattern_matches_example(self, data):
        pat = self._patterns(data)["L5"]
        assert re.match(pat, "CTX-AERO-28")

    def test_l4_pattern_matches_example(self, data):
        pat = self._patterns(data)["L4"]
        assert re.match(pat, "STR-ROB-LINE-ST04")

    def test_l3_pattern_matches_example(self, data):
        pat = self._patterns(data)["L3"]
        assert re.match(pat, "PRC-AERO-28-001")

    def test_l2_pattern_matches_example(self, data):
        pat = self._patterns(data)["L2"]
        assert re.match(pat, "XFM-ROB-LINE-KIN-003")

    def test_l1_pattern_matches_example(self, data):
        pat = self._patterns(data)["L1"]
        assert re.match(pat, "SBJ-MRO-ENG-SAFE-003")


# =========================================================================
# BREX YAML — Method Class Constraint
# =========================================================================


class TestBREXMethodClassConstraint:
    """BREX must list allowed method classes matching the standard."""

    @pytest.fixture()
    def data(self):
        with open(META_DIR / BREX_FILE) as f:
            return yaml.safe_load(f)

    @pytest.fixture()
    def standard_data(self):
        with open(META_DIR / STANDARD_FILE) as f:
            return yaml.safe_load(f)

    def test_brex_classes_match_standard(self, data, standard_data):
        brex_rule = [r for r in data["structure_rules"] if r["id"] == "MTL-STRUCT-003"]
        brex_classes = set(brex_rule[0]["allowed_classes"])
        std_classes = {c["id"] for c in standard_data["method_classes"]["classes"]}
        assert brex_classes == std_classes


# =========================================================================
# BREX YAML — Summary
# =========================================================================


class TestBREXSummary:
    """BREX summary counts must match actual rules."""

    @pytest.fixture()
    def data(self):
        with open(META_DIR / BREX_FILE) as f:
            return yaml.safe_load(f)

    def test_structure_count(self, data):
        assert data["summary"]["total_structure_rules"] == len(data["structure_rules"])

    def test_contract_count(self, data):
        assert data["summary"]["total_contract_rules"] == len(data["contract_rules"])

    def test_traceability_count(self, data):
        assert data["summary"]["total_traceability_rules"] == len(data["traceability_rules"])

    def test_governance_count(self, data):
        assert data["summary"]["total_governance_rules"] == len(data["governance_rules"])

    def test_safety_count(self, data):
        assert data["summary"]["total_safety_rules"] == len(data["safety_rules"])

    def test_lifecycle_count(self, data):
        assert data["summary"]["total_lifecycle_rules"] == len(data["lifecycle_rules"])

    def test_learning_count(self, data):
        assert data["summary"]["total_learning_rules"] == len(data["learning_rules"])
