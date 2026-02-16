"""
Tests for LC01 Problem Statement Governance Package (ATA 28-11).

Validates directory structure, YAML schema integrity, governance
controls, RACI matrix, admission policy, and cross-file consistency
for the SSOT governance package at:
  .../KDB/LM/SSOT/PLM/LC01_PROBLEM_STATEMENT/PACKAGES/GOVERNANCE/
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
GOV_DIR = (
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
    / "LC01_PROBLEM_STATEMENT"
    / "PACKAGES"
    / "GOVERNANCE"
)

# Required governance YAML files
REQUIRED_YAML_FILES = [
    "GOVERNANCE_PACKAGE.yaml",
    "FOUNDATIONAL_AXIOM.yaml",
    "PROBLEM_BOUNDARY.yaml",
    "DECISION_RIGHTS_AND_RACI.yaml",
    "CONSTITUTION_BINDING.yaml",
    "SAFETY_AND_HUMAN_HARM_PRECEDENCE.yaml",
    "LABOR_CONTINUITY_POLICY.yaml",
    "ADMISSION_POLICY_LC01.yaml",
    "ESCALATION_AND_CONFLICT_RESOLUTION.yaml",
    "TRACEABILITY_OBLIGATIONS.yaml",
    "CHANGE_CONTROL.yaml",
]

EVIDENCE_FILES = [
    "evidence/EVIDENCE_INDEX.yaml",
    "evidence/signatures/SIGNATURE_MANIFEST.yaml",
    "evidence/signatures/checksums.sha256",
]


# =========================================================================
# 1. All required governance files present
# =========================================================================


class TestGovernanceDirectoryStructure:
    """All required governance files must exist."""

    def test_governance_dir_exists(self):
        assert GOV_DIR.is_dir()

    def test_readme_exists(self):
        assert (GOV_DIR / "README.md").exists()

    @pytest.mark.parametrize("filename", REQUIRED_YAML_FILES)
    def test_required_yaml_present(self, filename):
        assert (GOV_DIR / filename).exists(), f"Missing: {filename}"

    @pytest.mark.parametrize("filename", EVIDENCE_FILES)
    def test_evidence_files_present(self, filename):
        assert (GOV_DIR / filename).exists(), f"Missing: {filename}"

    def test_evidence_dir_exists(self):
        assert (GOV_DIR / "evidence").is_dir()

    def test_signatures_dir_exists(self):
        assert (GOV_DIR / "evidence" / "signatures").is_dir()


# =========================================================================
# Helpers
# =========================================================================


def _load(name: str) -> dict:
    with open(GOV_DIR / name) as f:
        return yaml.safe_load(f)


# =========================================================================
# 2. No placeholder values (TBD, TBC, empty required fields)
# =========================================================================


class TestNoPlaceholders:
    """No TBD/TBC/empty required fields in governance YAML files."""

    @pytest.mark.parametrize("filename", REQUIRED_YAML_FILES)
    def test_no_tbd_tbc(self, filename):
        text = (GOV_DIR / filename).read_text(encoding="utf-8")
        for placeholder in ("TBD", "TBC", "TODO", "FIXME"):
            assert placeholder not in text, (
                f"{filename} contains placeholder '{placeholder}'"
            )

    @pytest.mark.parametrize("filename", REQUIRED_YAML_FILES)
    def test_yaml_loads(self, filename):
        data = _load(filename)
        assert data is not None, f"{filename} parsed as empty"


# =========================================================================
# 3. GOVERNANCE_PACKAGE.yaml
# =========================================================================


class TestGovernancePackage:
    """Governance package identity and metadata."""

    @pytest.fixture()
    def data(self):
        return _load("GOVERNANCE_PACKAGE.yaml")

    def test_has_package_id(self, data):
        assert data["governance_package"]["package_id"] == "GOV-LC01-ATA28-11"

    def test_lifecycle_phase(self, data):
        assert data["governance_package"]["lifecycle_phase"] == "LC01"

    def test_status_ssot(self, data):
        assert data["governance_package"]["status"] == "SSOT"

    def test_baseline_state(self, data):
        assert data["governance_package"]["baseline_state"] == "baselined"

    def test_ata_scope(self, data):
        assert "28-11-00" in data["governance_package"]["ata_scope"]

    def test_owner_role(self, data):
        assert data["governance_package"]["owner_role"] == "REPOSITORY_STEWARD"

    def test_governance_authority(self, data):
        assert data["governance_package"]["governance_authority"] == "CCB"

    def test_version(self, data):
        assert data["governance_package"]["version"] == "1.0.0"


# =========================================================================
# 4. FOUNDATIONAL_AXIOM.yaml
# =========================================================================


class TestFoundationalAxiom:
    """Foundational axiom must be non-negotiable."""

    @pytest.fixture()
    def data(self):
        return _load("FOUNDATIONAL_AXIOM.yaml")

    def test_axiom_statement_present(self, data):
        stmt = data["foundational_axiom"]["statement"]
        assert "Human labor founds" in stmt

    def test_interpretation_rules_not_empty(self, data):
        rules = data["foundational_axiom"]["interpretation_rules"]
        assert len(rules) >= 3

    def test_binding_scope_covers_lc01_through_lc14(self, data):
        scopes = data["foundational_axiom"]["binding_scope"]
        assert any("LC01" in s and "LC14" in s for s in scopes)

    def test_violation_action(self, data):
        assert data["foundational_axiom"]["violation_action"] == "HOLD_AND_CCB_ESCALATION"


# =========================================================================
# 5. CONSTITUTION_BINDING.yaml — deny conditions mapped to actions
# =========================================================================


class TestConstitutionBinding:
    """Constitution binding must enforce deny-by-default."""

    @pytest.fixture()
    def data(self):
        return _load("CONSTITUTION_BINDING.yaml")

    def test_enforcement_mode(self, data):
        assert data["constitution_binding"]["enforcement_mode"] == "deny_by_default"

    def test_has_controls(self, data):
        controls = data["constitution_binding"]["controls"]
        assert len(controls) >= 5

    def test_deny_conditions_present(self, data):
        conds = data["constitution_binding"]["deny_conditions"]
        assert len(conds) >= 5

    def test_article_a4_commit_legitimacy(self, data):
        ids = [c["control_id"] for c in data["constitution_binding"]["controls"]]
        assert "MDC-CTL-A4" in ids

    def test_article_a5_traceability(self, data):
        ids = [c["control_id"] for c in data["constitution_binding"]["controls"]]
        assert "MDC-CTL-A5" in ids

    def test_article_a6_harm_precedence(self, data):
        ids = [c["control_id"] for c in data["constitution_binding"]["controls"]]
        assert "MDC-CTL-A6" in ids

    def test_article_a8_human_exclusion(self, data):
        ids = [c["control_id"] for c in data["constitution_binding"]["controls"]]
        assert "MDC-CTL-A8" in ids

    def test_article_a11_conflict_resolution(self, data):
        ids = [c["control_id"] for c in data["constitution_binding"]["controls"]]
        assert "MDC-CTL-A11" in ids

    def test_applicable_articles(self, data):
        arts = data["constitution_binding"]["applicable_articles"]
        for a in ["A1", "A4", "A5", "A6", "A8", "A10", "A11"]:
            assert a in arts, f"Missing article {a}"


# =========================================================================
# 6. DECISION_RIGHTS_AND_RACI.yaml — exactly one A per decision
# =========================================================================


class TestDecisionRightsAndRACI:
    """RACI matrix must have exactly one Accountable per decision."""

    @pytest.fixture()
    def data(self):
        return _load("DECISION_RIGHTS_AND_RACI.yaml")

    def test_roles_defined(self, data):
        roles = data["decision_rights_and_raci"]["roles"]
        assert len(roles) >= 5

    def test_raci_matrix_present(self, data):
        matrix = data["decision_rights_and_raci"]["raci_matrix"]
        assert len(matrix) >= 2

    def test_exactly_one_accountable_per_decision(self, data):
        for item in data["decision_rights_and_raci"]["raci_matrix"]:
            a = item.get("A", [])
            assert len(a) == 1, (
                f"Decision '{item['decision']}' has {len(a)} Accountable(s), expected 1"
            )

    def test_required_roles_present(self, data):
        role_names = {r["role"] for r in data["decision_rights_and_raci"]["roles"]}
        for required in ["REPOSITORY_STEWARD", "CCB", "STK_ENG", "STK_SAF", "STK_CM"]:
            assert required in role_names, f"Missing role: {required}"


# =========================================================================
# 7. SAFETY_AND_HUMAN_HARM_PRECEDENCE.yaml
# =========================================================================


class TestSafetyPrecedence:
    """Safety precedence order must prioritize human harm avoidance."""

    @pytest.fixture()
    def data(self):
        return _load("SAFETY_AND_HUMAN_HARM_PRECEDENCE.yaml")

    def test_human_harm_first(self, data):
        order = data["safety_and_human_harm_precedence"]["precedence_order"]
        assert 1 in order, "precedence_order must have key 1"
        assert "harm" in order[1].lower() or "human" in order[1].lower()

    def test_has_required_actions(self, data):
        actions = data["safety_and_human_harm_precedence"]["uncertainty_policy"]["required_actions"]
        for action in ["DEGRADE", "PAUSE", "ESCALATE"]:
            assert action in actions, f"Required action '{action}' not found in uncertainty_policy"

    def test_autonomous_harm_forbidden(self, data):
        policy = data["safety_and_human_harm_precedence"]["uncertainty_policy"]
        assert policy["autonomous_harm_tradeoff_decisions"] == "forbidden"

    def test_human_authorizer_required(self, data):
        policy = data["safety_and_human_harm_precedence"]["uncertainty_policy"]
        assert policy["human_authorizer_required_for_resume"] is True


# =========================================================================
# 8. LABOR_CONTINUITY_POLICY.yaml
# =========================================================================


class TestLaborContinuityPolicy:
    """Labor continuity policy must protect against displacement."""

    @pytest.fixture()
    def data(self):
        return _load("LABOR_CONTINUITY_POLICY.yaml")

    def test_principle_present(self, data):
        assert "augment" in data["labor_continuity_policy"]["principle"].lower()

    def test_hard_rules_not_empty(self, data):
        assert len(data["labor_continuity_policy"]["hard_rules"]) >= 3

    def test_required_evidence_defined(self, data):
        evidence = data["labor_continuity_policy"]["required_evidence"]
        assert "reabsorption_plan" in evidence
        assert "role_impact_assessment" in evidence

    def test_enforcement_action(self, data):
        assert data["labor_continuity_policy"]["enforcement_action_on_missing_evidence"] == "HOLD_RELEASE"


# =========================================================================
# 9. ADMISSION_POLICY_LC01.yaml — references all mandatory controls
# =========================================================================


class TestAdmissionPolicy:
    """Admission policy must reference all mandatory governance controls."""

    @pytest.fixture()
    def data(self):
        return _load("ADMISSION_POLICY_LC01.yaml")

    def test_required_for_admission_complete(self, data):
        required = data["admission_policy_lc01"]["required_for_admission"]
        for item in [
            "constitution_binding_complete",
            "decision_rights_defined",
            "safety_precedence_defined",
            "labor_continuity_policy_defined",
            "traceability_obligations_defined",
            "signed_governance_commit_present",
        ]:
            assert item in required, f"Missing admission requirement: {item}"

    def test_prohibited_items(self, data):
        prohibited = data["admission_policy_lc01"]["prohibited"]
        assert len(prohibited) >= 3

    def test_on_fail_action(self, data):
        assert data["admission_policy_lc01"]["on_fail"] == "REJECT_AND_OPEN_ECR"


# =========================================================================
# 10. ESCALATION_AND_CONFLICT_RESOLUTION.yaml
# =========================================================================


class TestEscalation:
    """Escalation must cover key conflict types."""

    @pytest.fixture()
    def data(self):
        return _load("ESCALATION_AND_CONFLICT_RESOLUTION.yaml")

    def test_conflict_types_defined(self, data):
        types = data["escalation_and_conflict_resolution"]["conflict_types"]
        assert len(types) >= 3

    def test_silent_override_denied(self, data):
        for ct in data["escalation_and_conflict_resolution"]["conflict_types"]:
            if "silent_override_allowed" in ct:
                assert ct["silent_override_allowed"] is False

    def test_escalation_sla_present(self, data):
        sla = data["escalation_and_conflict_resolution"]["escalation_sla"]
        assert "acknowledge_hours" in sla
        assert "decision_days" in sla


# =========================================================================
# 11. TRACEABILITY_OBLIGATIONS.yaml — closure check
# =========================================================================


class TestTraceability:
    """Traceability must enforce closure."""

    @pytest.fixture()
    def data(self):
        return _load("TRACEABILITY_OBLIGATIONS.yaml")

    def test_mandatory_links_not_empty(self, data):
        links = data["traceability_obligations"]["mandatory_links"]
        assert len(links) >= 4

    def test_closure_required(self, data):
        assert data["traceability_obligations"]["closure_required"] is True

    def test_orphan_policy(self, data):
        assert data["traceability_obligations"]["orphan_policy"] == "reject_publish"


# =========================================================================
# 12. CHANGE_CONTROL.yaml
# =========================================================================


class TestChangeControl:
    """Change control must enforce CCB authority and no silent override."""

    @pytest.fixture()
    def data(self):
        return _load("CHANGE_CONTROL.yaml")

    def test_authority_is_ccb(self, data):
        assert data["change_control"]["authority"] == "CCB"

    def test_update_requires_ecr(self, data):
        required = data["change_control"]["update_requires"]
        assert "ECR_ID" in required

    def test_semantic_versioning(self, data):
        sv = data["change_control"]["semantic_versioning"]
        assert "major" in sv
        assert "minor" in sv
        assert "patch" in sv

    def test_no_silent_override(self, data):
        assert data["change_control"]["silent_override_allowed"] is False


# =========================================================================
# 13. PROBLEM_BOUNDARY.yaml
# =========================================================================


class TestProblemBoundary:
    """Problem boundary must define scope and exclusions."""

    @pytest.fixture()
    def data(self):
        return _load("PROBLEM_BOUNDARY.yaml")

    def test_in_scope_not_empty(self, data):
        assert len(data["problem_boundary"]["in_scope"]) >= 3

    def test_out_of_scope_not_empty(self, data):
        assert len(data["problem_boundary"]["out_of_scope"]) >= 3

    def test_success_criteria_defined(self, data):
        assert len(data["problem_boundary"]["success_criteria"]) >= 2


# =========================================================================
# 14. README.md content
# =========================================================================


class TestReadme:
    """README must document non-negotiables."""

    @pytest.fixture()
    def text(self):
        return (GOV_DIR / "README.md").read_text(encoding="utf-8")

    def test_title(self, text):
        assert "GOVERNANCE" in text

    def test_mentions_deny_by_default(self, text):
        assert "Deny-by-default" in text

    def test_mentions_signed_commit(self, text):
        assert "signed" in text.lower()

    def test_mentions_harm_precedence(self, text):
        assert "DEGRADE/PAUSE/ESCALATE" in text

    def test_mentions_human_exclusion(self, text):
        assert "human exclusion" in text.lower()

    def test_mentions_silent_override(self, text):
        assert "silent override" in text.lower()
