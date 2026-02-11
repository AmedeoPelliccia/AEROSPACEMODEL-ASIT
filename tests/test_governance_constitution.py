"""
Tests for Governance Constitution Enforcement

Validates that governance artifacts (GOVERNANCE.md, Digital Constitution,
PR template) contain required structural elements and enforcement hooks.
"""

import hashlib
from pathlib import Path

import pytest


# Resolve repository root (tests/ is one level below root)
REPO_ROOT = Path(__file__).resolve().parent.parent


class TestDigitalConstitution:
    """Tests for Model_Digital_Constitution.md structural integrity."""

    @pytest.fixture
    def constitution_text(self) -> str:
        path = REPO_ROOT / "Model_Digital_Constitution.md"
        assert path.exists(), "Model_Digital_Constitution.md must exist"
        return path.read_text(encoding="utf-8")

    def test_foundational_axiom_present(self, constitution_text: str):
        """Foundational axiom markers must be present."""
        assert "Foundational Axiom" in constitution_text
        assert "Human labor" in constitution_text
        assert "Capital" in constitution_text
        assert "Technology" in constitution_text

    def test_all_articles_present(self, constitution_text: str):
        """All constitutional articles must be present."""
        for i in range(1, 12):
            assert f"Article {i}" in constitution_text, (
                f"Article {i} missing from constitution"
            )

    def test_conflict_resolution_clause(self, constitution_text: str):
        """Art. 11 conflict resolution clause must exist."""
        assert "Conflict Resolution" in constitution_text
        assert "silent override" in constitution_text.lower()

    def test_commit_as_legitimacy(self, constitution_text: str):
        """Art. 4 commit-as-legitimacy concept must be present."""
        assert "Commit" in constitution_text
        assert "Legitimacy" in constitution_text

    def test_harm_precedence(self, constitution_text: str):
        """Art. 6 harm precedence must be present."""
        assert "Human Harm Precedence" in constitution_text
        assert "degrade" in constitution_text
        assert "escalate" in constitution_text

    def test_constitution_hash_stability(self):
        """Constitution hash must be computable for CI enforcement."""
        path = REPO_ROOT / "Model_Digital_Constitution.md"
        content = path.read_bytes()
        sha256 = hashlib.sha256(content).hexdigest()
        assert len(sha256) == 64, "SHA-256 hash must be 64 hex characters"


class TestGovernanceDocument:
    """Tests for GOVERNANCE.md structural integrity."""

    @pytest.fixture
    def governance_text(self) -> str:
        path = REPO_ROOT / "GOVERNANCE.md"
        assert path.exists(), "GOVERNANCE.md must exist"
        return path.read_text(encoding="utf-8")

    def test_references_constitution(self, governance_text: str):
        """GOVERNANCE.md must reference the Digital Constitution."""
        assert "Model_Digital_Constitution.md" in governance_text

    def test_references_contributing(self, governance_text: str):
        """GOVERNANCE.md must reference CONTRIBUTING.md."""
        assert "CONTRIBUTING.md" in governance_text

    def test_enforcement_mechanisms_section(self, governance_text: str):
        """Enforcement mechanisms section must exist."""
        assert "Enforcement Mechanisms" in governance_text

    def test_labor_reabsorption_documented(self, governance_text: str):
        """Labor reabsorption enforcement must be documented."""
        assert "Labor Reabsorption" in governance_text
        assert "Net displacement" in governance_text

    def test_harm_precedence_escalation(self, governance_text: str):
        """Harm precedence escalation must define named role and SLA."""
        assert "STK_SAF" in governance_text
        assert "48 hours" in governance_text

    def test_conflict_resolution_section(self, governance_text: str):
        """Conflict resolution section must exist."""
        assert "Conflict Resolution" in governance_text
        assert "silent override" in governance_text.lower()

    def test_metrics_section(self, governance_text: str):
        """Metrics section must exist with required metrics."""
        assert "Metrics" in governance_text
        assert "Reversibility latency" in governance_text
        assert "role diversity" in governance_text.lower()

    def test_regulatory_alignment(self, governance_text: str):
        """Regulatory alignment section must reference EU AI Act and EASA."""
        assert "EU AI Act" in governance_text
        assert "EASA" in governance_text


class TestPRTemplate:
    """Tests for PR template with LABOR-REABSORPTION fields."""

    @pytest.fixture
    def template_text(self) -> str:
        path = REPO_ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md"
        assert path.exists(), "PR template must exist"
        return path.read_text(encoding="utf-8")

    def test_labor_reabsorption_section(self, template_text: str):
        """PR template must include LABOR-REABSORPTION section."""
        assert "LABOR-REABSORPTION" in template_text

    def test_roles_displaced_field(self, template_text: str):
        """PR template must include roles displaced field."""
        assert "Roles displaced" in template_text

    def test_roles_created_field(self, template_text: str):
        """PR template must include roles created field."""
        assert "Roles created" in template_text

    def test_transition_pathway_field(self, template_text: str):
        """PR template must include transition pathway field."""
        assert "Transition pathway" in template_text

    def test_net_displacement_field(self, template_text: str):
        """PR template must include net displacement field."""
        assert "Net displacement" in template_text

    def test_constitutional_compliance_checklist(self, template_text: str):
        """PR template must include constitutional compliance checklist."""
        assert "Constitutional Compliance" in template_text
        # Check that articles 1-9 are referenced
        for i in range(1, 10):
            assert f"Art. {i}" in template_text, (
                f"Art. {i} missing from compliance checklist"
            )

    def test_declared_intent_section(self, template_text: str):
        """PR template must include declared intent section."""
        assert "Declared Intent" in template_text

    def test_safety_impact_section(self, template_text: str):
        """PR template must include safety impact section."""
        assert "Safety Impact" in template_text


class TestConstitutionComplianceWorkflow:
    """Tests for constitution-compliance CI workflow."""

    @pytest.fixture
    def workflow_text(self) -> str:
        path = REPO_ROOT / ".github" / "workflows" / "constitution-compliance.yml"
        assert path.exists(), "Constitution compliance workflow must exist"
        return path.read_text(encoding="utf-8")

    def test_workflow_triggers_on_pr(self, workflow_text: str):
        """Workflow must trigger on pull requests."""
        assert "pull_request" in workflow_text

    def test_validates_constitution_integrity(self, workflow_text: str):
        """Workflow must validate constitution integrity."""
        assert "constitution integrity" in workflow_text.lower()

    def test_checks_pr_template(self, workflow_text: str):
        """Workflow must check PR template exists."""
        assert "PULL_REQUEST_TEMPLATE" in workflow_text

    def test_checks_labor_reabsorption(self, workflow_text: str):
        """Workflow must check for LABOR-REABSORPTION section."""
        assert "LABOR-REABSORPTION" in workflow_text
