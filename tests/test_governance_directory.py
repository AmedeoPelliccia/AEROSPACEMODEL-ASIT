"""
Tests for Governance Directory Documents

Validates that Governance/ directory documents (AI Governance Standard,
NPA Response, EAARF Charter) exist and contain required structural elements.
"""

from pathlib import Path

import pytest


# Resolve repository root (tests/ is one level below root)
REPO_ROOT = Path(__file__).resolve().parent.parent
GOVERNANCE_DIR = REPO_ROOT / "Governance"


class TestGovernanceDirectoryStructure:
    """Tests that the Governance/ directory exists with required files."""

    def test_governance_directory_exists(self):
        """Governance/ directory must exist."""
        assert GOVERNANCE_DIR.is_dir(), "Governance/ directory must exist"

    def test_ai_governance_standard_exists(self):
        """AI Governance Standard document must exist."""
        path = GOVERNANCE_DIR / "EASA_ESA_AI_GOVERNANCE_STANDARD_v1.0.md"
        assert path.exists(), "EASA_ESA_AI_GOVERNANCE_STANDARD_v1.0.md must exist"

    def test_npa_response_exists(self):
        """NPA 2025-07 Response document must exist."""
        path = GOVERNANCE_DIR / "NPA_2025-07_RESPONSE.md"
        assert path.exists(), "NPA_2025-07_RESPONSE.md must exist"

    def test_eaarf_charter_exists(self):
        """EAARF Charter Draft document must exist."""
        path = GOVERNANCE_DIR / "EAARF_CHARTER_DRAFT.md"
        assert path.exists(), "EAARF_CHARTER_DRAFT.md must exist"


class TestAIGovernanceStandard:
    """Tests for EASA_ESA_AI_GOVERNANCE_STANDARD_v1.0.md structural integrity."""

    @pytest.fixture
    def standard_text(self) -> str:
        path = GOVERNANCE_DIR / "EASA_ESA_AI_GOVERNANCE_STANDARD_v1.0.md"
        assert path.exists(), "AI Governance Standard must exist"
        return path.read_text(encoding="utf-8")

    def test_references_digital_constitution(self, standard_text: str):
        """Standard must reference the Digital Constitution."""
        assert "Model_Digital_Constitution.md" in standard_text

    def test_references_easa(self, standard_text: str):
        """Standard must reference EASA."""
        assert "EASA" in standard_text

    def test_references_esa(self, standard_text: str):
        """Standard must reference ESA."""
        assert "ESA" in standard_text

    def test_human_oversight_section(self, standard_text: str):
        """Standard must address human oversight."""
        assert "Human Oversight" in standard_text

    def test_risk_classification(self, standard_text: str):
        """Standard must include risk classification."""
        assert "Risk" in standard_text

    def test_enforcement_section(self, standard_text: str):
        """Standard must include enforcement mechanisms."""
        assert "Enforcement" in standard_text

    def test_architectural_prevention_of_autonomy(self, standard_text: str):
        """Standard must architecturally prevent autonomous AI decisions."""
        assert "prevents" in standard_text
        assert "human-authorization gate" in standard_text

    def test_change_history(self, standard_text: str):
        """Standard must include a change history table."""
        assert "Change History" in standard_text

    def test_compliance_traceability_matrix(self, standard_text: str):
        """Standard must include a Compliance Traceability Matrix."""
        assert "Compliance Traceability Matrix" in standard_text
        assert "GOV-001" in standard_text

    def test_operational_monitoring(self, standard_text: str):
        """Standard must include operational monitoring section."""
        assert "Operational Monitoring" in standard_text
        assert "Performance Degradation" in standard_text

    def test_frozen_baseline_definition(self, standard_text: str):
        """Standard must define frozen model baseline components."""
        assert "Frozen Model Baseline Definition" in standard_text
        assert "Cryptographic seal" in standard_text

    def test_consistent_brex_references(self, standard_text: str):
        """Standard must use consistent BREX-{CATEGORY}-{NNN} format."""
        assert "BREX-SAFETY-002" in standard_text
        assert "BREX-AUDIT-001" in standard_text

    def test_enhanced_audit_log_format(self, standard_text: str):
        """Audit log must include actor, ai_model_version, input_hash."""
        assert "{actor}" in standard_text
        assert "{ai_model_version}" in standard_text
        assert "{input_hash}" in standard_text

    def test_sequential_cicd_gates(self, standard_text: str):
        """CI/CD must describe sequential gates."""
        assert "Gate 1" in standard_text or "sequential gates" in standard_text


class TestNPAResponse:
    """Tests for NPA_2025-07_RESPONSE.md structural integrity."""

    @pytest.fixture
    def npa_text(self) -> str:
        path = GOVERNANCE_DIR / "NPA_2025-07_RESPONSE.md"
        assert path.exists(), "NPA Response must exist"
        return path.read_text(encoding="utf-8")

    def test_references_npa_2025_07(self, npa_text: str):
        """Response must reference NPA 2025-07."""
        assert "NPA 2025-07" in npa_text

    def test_references_easa(self, npa_text: str):
        """Response must reference EASA."""
        assert "EASA" in npa_text

    def test_has_executive_summary(self, npa_text: str):
        """Response must include an executive summary."""
        assert "Executive Summary" in npa_text

    def test_has_detailed_comments(self, npa_text: str):
        """Response must include detailed comments."""
        assert "Detailed Comments" in npa_text

    def test_references_digital_constitution(self, npa_text: str):
        """Response must reference the Digital Constitution."""
        assert "Digital Constitution" in npa_text

    def test_references_eaarf(self, npa_text: str):
        """Response must reference the EAARF forum."""
        assert "EAARF" in npa_text


class TestEAARFCharter:
    """Tests for EAARF_CHARTER_DRAFT.md structural integrity."""

    @pytest.fixture
    def charter_text(self) -> str:
        path = GOVERNANCE_DIR / "EAARF_CHARTER_DRAFT.md"
        assert path.exists(), "EAARF Charter must exist"
        return path.read_text(encoding="utf-8")

    def test_defines_eaarf_name(self, charter_text: str):
        """Charter must define EAARF full name."""
        assert "European Aviation AI Requirements Framework" in charter_text

    def test_has_mission(self, charter_text: str):
        """Charter must include a mission statement."""
        assert "Mission" in charter_text

    def test_has_scope(self, charter_text: str):
        """Charter must define scope."""
        assert "Scope" in charter_text

    def test_has_governance_structure(self, charter_text: str):
        """Charter must define governance structure."""
        assert "Governance Structure" in charter_text

    def test_has_membership(self, charter_text: str):
        """Charter must define membership."""
        assert "Membership" in charter_text

    def test_has_working_groups(self, charter_text: str):
        """Charter must define working groups."""
        assert "Working Group" in charter_text

    def test_references_digital_constitution(self, charter_text: str):
        """Charter must reference the Digital Constitution."""
        assert "Digital Constitution" in charter_text
