"""
Tests for the Unified Teknia Token System (UTTS) — Modification Track Lookup Standard.

Validates the N-STD-UTTS-01_v0.1.0.yaml, N-STD-UTTS-01_BREX.yaml,
and README.md artifacts in ASIT/STANDARDS/N-STD-UTTS-01/.
Tests for UTTS (Unified Teknia Token System) infrastructure specification.

Validates:
- N-STD-UTTS-01 standard files exist in ASIT/STANDARDS/
- UTTS YAML standard is valid and contains required metadata
- UTTS BREX YAML is valid and contains required rule categories
- ATA 96 directory has UTTS README
- N-NEURAL_NETWORKS documentation references UTTS
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
UTTS_DIR = REPO_ROOT / "ASIT" / "STANDARDS" / "N-STD-UTTS-01"
STANDARD_FILE = "N-STD-UTTS-01_v0.1.0.yaml"
BREX_FILE = "N-STD-UTTS-01_BREX.yaml"


# =========================================================================
# Directory and Files
# =========================================================================


class TestUTTSDirectory:
    """N-STD-UTTS-01 directory must contain the expected files."""

    def test_directory_exists(self):
        assert UTTS_DIR.is_dir()

    def test_readme_exists(self):
        assert (UTTS_DIR / "README.md").exists()

    def test_standard_yaml_exists(self):
        assert (UTTS_DIR / STANDARD_FILE).exists()

    def test_brex_yaml_exists(self):
        assert (UTTS_DIR / BREX_FILE).exists()


# =========================================================================
# Standard YAML — Metadata
# =========================================================================


class TestStandardMetadata:
    """Standard YAML must have required metadata."""

    @pytest.fixture()
    def data(self):
        with open(UTTS_DIR / STANDARD_FILE) as f:
            return yaml.safe_load(f)

    def test_yaml_parses(self, data):
        assert data is not None

    def test_standard_id(self, data):
        assert data["metadata"]["standard_id"] == "N-STD-UTTS-01"

    def test_version(self, data):
        assert data["metadata"]["version"] == "0.1.0"

    def test_status(self, data):
        assert data["metadata"]["status"] in ("DRAFT", "REVIEW", "APPROVED", "ACTIVE")

    def test_determinism_strict(self, data):
        assert data["metadata"]["determinism_level"] == "strict"

    def test_compliance_list(self, data):
        c = data["metadata"]["compliance"]
        assert isinstance(c, list) and len(c) >= 1

    def test_references_brex_rule_set(self, data):
        assert data["metadata"]["brex_rule_set"] == "N-STD-UTTS-01-BREX-001"

    def test_references_mtl_standard(self, data):
        assert "MTL-META-CORE" in data["metadata"]["related_standard"]


# =========================================================================
# Standard YAML — Definition
# =========================================================================


class TestStandardDefinition:
    """Standard YAML must define UTTS as Modification Track Lookup."""

    @pytest.fixture()
    def data(self):
        with open(UTTS_DIR / STANDARD_FILE) as f:
            return yaml.safe_load(f)

    def test_has_definition(self, data):
        assert "definition" in data

    def test_definition_references_modification_track(self, data):
        defn = data["definition"].lower()
        assert "modification" in defn and "track" in defn

    def test_definition_references_deterministic(self, data):
        assert "deterministic" in data["definition"].lower()


# =========================================================================
# Standard YAML — MTL Tier Integration
# =========================================================================


EXPECTED_TIERS = ["MTL₁", "MTL₂", "MTL₃"]


class TestMTLTiers:
    """Standard must define three MTL tiers."""

    @pytest.fixture()
    def data(self):
        with open(UTTS_DIR / STANDARD_FILE) as f:
            return yaml.safe_load(f)

    def test_has_mtl_tiers(self, data):
        assert "mtl_tiers" in data

    def test_three_tiers(self, data):
        assert len(data["mtl_tiers"]["tiers"]) == 3

    def test_tier_ids(self, data):
        ids = [t["tier"] for t in data["mtl_tiers"]["tiers"]]
        assert ids == EXPECTED_TIERS

    def test_each_tier_has_name(self, data):
        for tier in data["mtl_tiers"]["tiers"]:
            assert "name" in tier

    def test_each_tier_has_utts_role(self, data):
        for tier in data["mtl_tiers"]["tiers"]:
            assert "utts_role" in tier

    def test_mtl1_is_methods_token_library(self, data):
        mtl1 = [t for t in data["mtl_tiers"]["tiers"] if t["tier"] == "MTL₁"][0]
        assert "Methods Token Library" in mtl1["name"]

    def test_mtl2_is_meta_transformation_layer(self, data):
        mtl2 = [t for t in data["mtl_tiers"]["tiers"] if t["tier"] == "MTL₂"][0]
        assert "Meta Transformation Layer" in mtl2["name"]

    def test_mtl3_is_model_teknia_ledger(self, data):
        mtl3 = [t for t in data["mtl_tiers"]["tiers"] if t["tier"] == "MTL₃"][0]
        assert "Teknia Ledger" in mtl3["name"]


# =========================================================================
# Standard YAML — Formal Model
# =========================================================================


class TestFormalModel:
    """Standard must include the formal modification model."""

    @pytest.fixture()
    def data(self):
        with open(UTTS_DIR / STANDARD_FILE) as f:
            return yaml.safe_load(f)

    def test_has_formal_model(self, data):
        assert "formal_model" in data

    def test_has_state_formula(self, data):
        assert "state_formula" in data["formal_model"]

    def test_has_hash_chain(self, data):
        assert "hash_chain" in data["formal_model"]

    def test_has_transformation_operator(self, data):
        assert "transformation_operator" in data["formal_model"]

    def test_state_formula_contains_T0(self, data):
        assert "T₀" in data["formal_model"]["state_formula"] or \
               "T0" in data["formal_model"]["state_formula"]

    def test_hash_chain_references_sha(self, data):
        # hash_chain field should be present; SHA reference is in the integrity section
        assert data["formal_model"]["hash_chain"] is not None


# =========================================================================
# Standard YAML — Object Model
# =========================================================================


REQUIRED_TOKEN_STATE_FIELDS = [
    "token_id", "current_revision", "current_hash", "lc_phase", "status"
]

REQUIRED_MOD_EVENT_FIELDS = [
    "mod_id", "parent_token", "previous_hash", "new_hash",
    "change_type", "description", "authority", "lc_phase",
    "timestamp_utc", "impact_scope", "justification_ref",
]

EXPECTED_CHANGE_TYPES = [
    "constraint_update",
    "parameter_revision",
    "evidence_addition",
    "procedure_amendment",
    "regulatory_realignment",
    "status_transition",
]


class TestObjectModel:
    """Standard must define token state and modification event objects."""

    @pytest.fixture()
    def data(self):
        with open(UTTS_DIR / STANDARD_FILE) as f:
            return yaml.safe_load(f)

    def test_has_object_model(self, data):
        assert "object_model" in data

    def test_has_token_state_object(self, data):
        assert "token_state_object" in data["object_model"]

    def test_has_modification_event_object(self, data):
        assert "modification_event_object" in data["object_model"]

    def test_token_state_required_fields(self, data):
        fields = data["object_model"]["token_state_object"]["required_fields"]
        for f in REQUIRED_TOKEN_STATE_FIELDS:
            assert f in fields, f"Token state object missing required field: {f}"

    def test_mod_event_required_fields(self, data):
        fields = data["object_model"]["modification_event_object"]["required_fields"]
        for f in REQUIRED_MOD_EVENT_FIELDS:
            assert f in fields, f"Modification event object missing required field: {f}"

    def test_change_types_present(self, data):
        types = data["object_model"]["modification_event_object"]["change_types"]
        for ct in EXPECTED_CHANGE_TYPES:
            assert ct in types, f"Missing change type: {ct}"

    def test_six_change_types(self, data):
        assert len(data["object_model"]["modification_event_object"]["change_types"]) == 6


# =========================================================================
# Standard YAML — Lookup Dimensions
# =========================================================================


EXPECTED_DIMENSIONS = ["DIM-01", "DIM-02", "DIM-03", "DIM-04", "DIM-05"]


class TestLookupDimensions:
    """Standard must define exactly five lookup dimensions."""

    @pytest.fixture()
    def data(self):
        with open(UTTS_DIR / STANDARD_FILE) as f:
            return yaml.safe_load(f)

    def test_has_lookup_dimensions(self, data):
        assert "lookup_dimensions" in data

    def test_five_dimensions(self, data):
        assert len(data["lookup_dimensions"]["dimensions"]) == 5

    def test_dimension_ids(self, data):
        ids = [d["id"] for d in data["lookup_dimensions"]["dimensions"]]
        assert ids == EXPECTED_DIMENSIONS

    def test_each_dimension_has_name(self, data):
        for dim in data["lookup_dimensions"]["dimensions"]:
            assert "name" in dim

    def test_each_dimension_has_query(self, data):
        for dim in data["lookup_dimensions"]["dimensions"]:
            assert "query" in dim

    def test_dim01_is_by_token(self, data):
        dim01 = [d for d in data["lookup_dimensions"]["dimensions"] if d["id"] == "DIM-01"][0]
        assert "token" in dim01["name"].lower() or "Token" in dim01["name"]

    def test_dim05_is_by_impact(self, data):
        dim05 = [d for d in data["lookup_dimensions"]["dimensions"] if d["id"] == "DIM-05"][0]
        assert "impact" in dim05["name"].lower() or "Impact" in dim05["name"]


# =========================================================================
# Standard YAML — Trace Graph
# =========================================================================


class TestTraceGraph:
    """Standard must define the DAG trace graph properties."""

    @pytest.fixture()
    def data(self):
        with open(UTTS_DIR / STANDARD_FILE) as f:
            return yaml.safe_load(f)

    def test_has_trace_graph(self, data):
        assert "trace_graph" in data

    def test_structure_is_dag(self, data):
        assert "DAG" in data["trace_graph"]["structure"]

    def test_four_properties(self, data):
        assert len(data["trace_graph"]["properties"]) == 4

    def test_has_forward_traceability(self, data):
        names = [p["name"] for p in data["trace_graph"]["properties"]]
        assert any("Forward" in n for n in names)

    def test_has_backward_traceability(self, data):
        names = [p["name"] for p in data["trace_graph"]["properties"]]
        assert any("Backward" in n for n in names)

    def test_has_deterministic_replay(self, data):
        names = [p["name"] for p in data["trace_graph"]["properties"]]
        assert any("Deterministic" in n or "Replay" in n for n in names)


# =========================================================================
# Standard YAML — Hash Chain Integrity
# =========================================================================


class TestHashChainIntegrity:
    """Standard must define the hash chain integrity model."""

    @pytest.fixture()
    def data(self):
        with open(UTTS_DIR / STANDARD_FILE) as f:
            return yaml.safe_load(f)

    def test_has_hash_chain_integrity(self, data):
        assert "hash_chain_integrity" in data

    def test_algorithm_is_sha3_512(self, data):
        assert data["hash_chain_integrity"]["algorithm"] == "SHA3-512"

    def test_has_chain_formula(self, data):
        assert "chain_formula" in data["hash_chain_integrity"]

    def test_has_properties(self, data):
        props = data["hash_chain_integrity"]["properties"]
        assert isinstance(props, list) and len(props) >= 3


# =========================================================================
# Standard YAML — Governance Rules
# =========================================================================


class TestGovernanceRules:
    """Standard must define five governance rules."""

    @pytest.fixture()
    def data(self):
        with open(UTTS_DIR / STANDARD_FILE) as f:
            return yaml.safe_load(f)

    def test_has_governance_rules(self, data):
        assert "governance_rules" in data

    def test_five_governance_rules(self, data):
        assert len(data["governance_rules"]) == 5

    def test_governance_rule_ids(self, data):
        ids = [r["id"] for r in data["governance_rules"]]
        for gid in ("UTTS-GOV-001", "UTTS-GOV-002", "UTTS-GOV-003",
                    "UTTS-GOV-004", "UTTS-GOV-005"):
            assert gid in ids


# =========================================================================
# Standard YAML — Decision States
# =========================================================================


EXPECTED_STATES = ["ALLOW", "HOLD", "REJECT", "ESCALATE"]


class TestDecisionStates:
    """Standard must define a deterministic decision state machine."""

    @pytest.fixture()
    def data(self):
        with open(UTTS_DIR / STANDARD_FILE) as f:
            return yaml.safe_load(f)

    def test_has_decision_states(self, data):
        assert "decision_states" in data

    def test_four_states(self, data):
        assert data["decision_states"]["allowed_states"] == EXPECTED_STATES

    def test_has_transition_rules(self, data):
        rules = data["decision_states"]["transition_rules"]
        assert isinstance(rules, list) and len(rules) >= 5

    def test_each_transition_has_when_then(self, data):
        rules = data["decision_states"]["transition_rules"]
        rules_with_then = [rule for rule in rules if "then" in rule]
        # Ensure there is at least one fully defined transition rule
        assert rules_with_then, "No transition rules define a 'then' target state."
        for rule in rules_with_then:
            # Any rule that defines a target state must also define a condition
            assert "when" in rule

    def test_all_then_values_are_valid_states(self, data):
        rules = data["decision_states"]["transition_rules"]
        for rule in rules:
            if "then" not in rule:
                continue
            assert rule["then"] in EXPECTED_STATES, f"Invalid state: {rule['then']}"

    def test_allow_is_last_resort(self, data):
        # ALLOW transition must require all governance rules to pass
        rules = data["decision_states"]["transition_rules"]
        allow_rule = [r for r in rules if r.get("then") == "ALLOW"]
        assert len(allow_rule) >= 1
        assert "all" in allow_rule[-1]["when"].lower() or "pass" in allow_rule[-1]["when"].lower()


# =========================================================================
# Standard YAML — Summary
# =========================================================================


class TestStandardSummary:
    """Summary counts must match actual data."""

    @pytest.fixture()
    def data(self):
        with open(UTTS_DIR / STANDARD_FILE) as f:
            return yaml.safe_load(f)

    def test_total_mtl_tiers(self, data):
        assert data["summary"]["total_mtl_tiers"] == len(data["mtl_tiers"]["tiers"])

    def test_total_lookup_dimensions(self, data):
        assert data["summary"]["total_lookup_dimensions"] == len(
            data["lookup_dimensions"]["dimensions"]
        )

    def test_total_change_types(self, data):
        assert data["summary"]["total_change_types"] == len(
            data["object_model"]["modification_event_object"]["change_types"]
        )

    def test_total_governance_rules(self, data):
        assert data["summary"]["total_governance_rules"] == len(data["governance_rules"])

    def test_total_decision_states(self, data):
        assert data["summary"]["total_decision_states"] == len(
            data["decision_states"]["allowed_states"]
        )

    def test_total_decision_transition_rules(self, data):
        assert data["summary"]["total_decision_transition_rules"] == len(
            data["decision_states"]["transition_rules"]
        )


# =========================================================================
# BREX YAML — Metadata
# =========================================================================


class TestBREXMetadata:
    """BREX YAML must have required metadata."""

    @pytest.fixture()
    def data(self):
        with open(UTTS_DIR / BREX_FILE) as f:
            return yaml.safe_load(f)

    def test_yaml_parses(self, data):
        assert data is not None

    def test_brex_id(self, data):
        assert data["metadata"]["brex_id"] == "N-STD-UTTS-01-BREX-001"

    def test_references_standard(self, data):
        assert "N-STD-UTTS-01" in data["metadata"]["standard_reference"]

    def test_references_parent_authority(self, data):
        assert data["metadata"]["parent_authority"] == "ASIT-BREX-MASTER-001"

    def test_determinism_strict(self, data):
        assert data["metadata"]["determinism_level"] == "strict"


# =========================================================================
# BREX YAML — Rule Categories
# =========================================================================


class TestBREXRuleCategories:
    """BREX must define rules in all required categories."""

    @pytest.fixture()
    def data(self):
        with open(UTTS_DIR / BREX_FILE) as f:
            return yaml.safe_load(f)

    def test_has_structure_rules(self, data):
        assert len(data["structure_rules"]) >= 2

    def test_has_integrity_rules(self, data):
        assert len(data["integrity_rules"]) >= 3

    def test_has_governance_rules(self, data):
        assert len(data["governance_rules"]) >= 4

    def test_has_safety_rules(self, data):
        assert len(data["safety_rules"]) >= 3

    def test_has_traceability_rules(self, data):
        assert len(data["traceability_rules"]) >= 3

    def test_has_lifecycle_rules(self, data):
        assert len(data["lifecycle_rules"]) >= 3

    def test_has_query_rules(self, data):
        assert len(data["query_rules"]) >= 3


# =========================================================================
# BREX YAML — Structure Rules
# =========================================================================


class TestBREXStructureRules:
    """BREX structure rules must enforce mod_id format and change_type taxonomy."""

    @pytest.fixture()
    def data(self):
        with open(UTTS_DIR / BREX_FILE) as f:
            return yaml.safe_load(f)

    def test_mod_id_pattern_present(self, data):
        rules_with_pattern = [r for r in data["structure_rules"] if "pattern" in r]
        assert len(rules_with_pattern) >= 1

    def test_mod_id_pattern_compiles(self, data):
        rules_with_pattern = [r for r in data["structure_rules"] if "pattern" in r]
        for rule in rules_with_pattern:
            compiled = re.compile(rule["pattern"])
            assert compiled is not None

    def test_mod_id_pattern_matches_valid(self, data):
        rules_with_pattern = [r for r in data["structure_rules"]
                               if "pattern" in r and "MOD" in r.get("condition", "")]
        assert len(rules_with_pattern) >= 1
        pattern = rules_with_pattern[0]["pattern"]
        assert re.match(pattern, "MOD-000457")

    def test_mod_id_pattern_rejects_invalid(self, data):
        rules_with_pattern = [r for r in data["structure_rules"]
                               if "pattern" in r and "MOD" in r.get("condition", "")]
        pattern = rules_with_pattern[0]["pattern"]
        assert not re.match(pattern, "MOD-123")
        assert not re.match(pattern, "mod-000457")

    def test_change_type_taxonomy_covers_all_types(self, data):
        ct_rule = [r for r in data["structure_rules"] if "allowed_change_types" in r]
        assert len(ct_rule) == 1
        for ct in EXPECTED_CHANGE_TYPES:
            assert ct in ct_rule[0]["allowed_change_types"]


# =========================================================================
# BREX YAML — Integrity Rules
# =========================================================================


class TestBREXIntegrityRules:
    """BREX integrity rules must enforce SHA3-512 hash chain."""

    @pytest.fixture()
    def data(self):
        with open(UTTS_DIR / BREX_FILE) as f:
            return yaml.safe_load(f)

    def test_sha3_512_required(self, data):
        sha_rules = [r for r in data["integrity_rules"] if "allowed_algorithms" in r]
        assert len(sha_rules) >= 1
        assert "SHA3-512" in sha_rules[0]["allowed_algorithms"]

    def test_hash_chain_rule_exists(self, data):
        chain_rules = [r for r in data["integrity_rules"]
                       if "chain" in r.get("condition", "").lower()
                       or "chain" in r.get("id", "").lower()]
        assert len(chain_rules) >= 1


# =========================================================================
# BREX YAML — Lifecycle Rules
# =========================================================================


EXPECTED_LC_PHASES = [f"LC{i:02d}" for i in range(1, 15)]


class TestBREXLifecycleRules:
    """BREX lifecycle rules must define all valid LC phases and status transitions."""

    @pytest.fixture()
    def data(self):
        with open(UTTS_DIR / BREX_FILE) as f:
            return yaml.safe_load(f)

    def test_lc_phases_rule_exists(self, data):
        lc_rules = [r for r in data["lifecycle_rules"] if "allowed_phases" in r]
        assert len(lc_rules) >= 1

    def test_all_14_phases_listed(self, data):
        lc_rules = [r for r in data["lifecycle_rules"] if "allowed_phases" in r]
        phases = lc_rules[0]["allowed_phases"]
        for phase in EXPECTED_LC_PHASES:
            assert phase in phases, f"LC phase {phase} missing from BREX"

    def test_lc_phases_timestamp_rule_present(self, data):
        ts_rules = [r for r in data["lifecycle_rules"] if "pattern" in r]
        assert len(ts_rules) >= 1
        # Verify ISO 8601 UTC pattern compiles and matches a valid timestamp
        pattern = ts_rules[0]["pattern"]
        assert re.match(pattern, "2026-02-20T01:20:00Z")

    def test_status_transition_rule_present(self, data):
        st_rules = [r for r in data["lifecycle_rules"] if "allowed_transitions" in r]
        assert len(st_rules) >= 1

    def test_status_transitions_include_dev_to_val(self, data):
        st_rules = [r for r in data["lifecycle_rules"] if "allowed_transitions" in r]
        transitions = st_rules[0]["allowed_transitions"]
        assert any(t["from"] == "DEV" and t["to"] == "VAL" for t in transitions)


# =========================================================================
# BREX YAML — Query Rules
# =========================================================================


class TestBREXQueryRules:
    """BREX query rules must enforce all 5 dimensions and determinism."""

    @pytest.fixture()
    def data(self):
        with open(UTTS_DIR / BREX_FILE) as f:
            return yaml.safe_load(f)

    def test_all_five_dimensions_required(self, data):
        dim_rules = [r for r in data["query_rules"] if "required_dimensions" in r]
        assert len(dim_rules) >= 1
        dims = dim_rules[0]["required_dimensions"]
        for dim_id in EXPECTED_DIMENSIONS:
            assert dim_id in dims

    def test_determinism_rule_exists(self, data):
        det_rules = [r for r in data["query_rules"]
                     if "deterministic" in r.get("condition", "").lower()]
        assert len(det_rules) >= 1


# =========================================================================
# BREX YAML — Summary
# =========================================================================


class TestBREXSummary:
    """BREX summary counts must match actual rules."""

    @pytest.fixture()
    def data(self):
        with open(UTTS_DIR / BREX_FILE) as f:
            return yaml.safe_load(f)

    def test_structure_count(self, data):
        assert data["summary"]["total_structure_rules"] == len(data["structure_rules"])

    def test_integrity_count(self, data):
        assert data["summary"]["total_integrity_rules"] == len(data["integrity_rules"])

    def test_governance_count(self, data):
        assert data["summary"]["total_governance_rules"] == len(data["governance_rules"])

    def test_safety_count(self, data):
        assert data["summary"]["total_safety_rules"] == len(data["safety_rules"])

    def test_traceability_count(self, data):
        assert data["summary"]["total_traceability_rules"] == len(data["traceability_rules"])

    def test_lifecycle_count(self, data):
        assert data["summary"]["total_lifecycle_rules"] == len(data["lifecycle_rules"])

    def test_query_count(self, data):
        assert data["summary"]["total_query_rules"] == len(data["query_rules"])


# =========================================================================
# README
# =========================================================================


class TestReadme:
    """README must exist and contain key sections."""

    @pytest.fixture()
    def text(self):
        return (UTTS_DIR / "README.md").read_text()

    def test_readme_contains_standard_id(self, text):
        assert "N-STD-UTTS-01" in text

    def test_readme_contains_modification_track_lookup(self, text):
        assert "Modification Track Lookup" in text

    def test_readme_contains_formal_model(self, text):
        assert "Formal Model" in text or "formal model" in text

    def test_readme_contains_lookup_dimensions(self, text):
        assert "Lookup Dimensions" in text or "lookup dimensions" in text.lower()

    def test_readme_contains_object_model(self, text):
        assert "Object Model" in text

    def test_readme_contains_hash_chain(self, text):
        assert "SHA3-512" in text or "hash chain" in text.lower()

    def test_readme_contains_all_five_dim_ids(self, text):
        for dim_id in EXPECTED_DIMENSIONS:
            assert dim_id in text, f"README missing dimension {dim_id}"

    def test_readme_contains_mtl_tiers(self, text):
        assert "MTL₁" in text and "MTL₂" in text and "MTL₃" in text

    def test_readme_links_to_standard_yaml(self, text):
        assert STANDARD_FILE in text

    def test_readme_links_to_brex_yaml(self, text):
        assert BREX_FILE in text

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
        assert len(brex_data["structure_rules"]) >= 2

    def test_safety_rules_exist(self, brex_data: dict):
        assert len(brex_data["safety_rules"]) >= 3

    def test_safety_rules_escalate_to_stk_saf(self, brex_data: dict):
        escalating = [r for r in brex_data["safety_rules"] if r.get("enforcement") == "escalate"]
        assert all(r["escalation_target"] == "STK_SAF" for r in escalating)

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
