"""
Tests for ATA 28 Canonical Directory Structure in OPT-IN_FRAMEWORK.

Validates the complete ATA chapter directory tree for ATA_28-FUEL
(Circular Cryogenic Cells) per the canonical structure specification.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
ATA28 = (
    REPO_ROOT
    / "OPT-IN_FRAMEWORK"
    / "T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS"
    / "C2-CIRCULAR_CRYOGENIC_CELLS"
    / "ATA_28-FUEL"
)
SECTION = ATA28 / "28-10-storage"
SUBJECT = SECTION / "28-10-00-fuel-storage-general"


# =========================================================================
# Root-Level Files
# =========================================================================


class TestATA28RootFiles:
    """Root-level documentation files must exist."""

    @pytest.mark.parametrize(
        "filename",
        [
            "README.md",
            "NAMING_CONVENTIONS.md",
            "TRACEABILITY_CONVENTIONS.md",
            "GOVERNANCE_POLICY.md",
        ],
    )
    def test_root_file_exists(self, filename):
        assert (ATA28 / filename).exists(), f"{filename} must exist at ATA_28-FUEL root"


# =========================================================================
# WBS
# =========================================================================


class TestWBS:
    """Work Breakdown Structure directory and key files."""

    def test_wbs_directory_exists(self):
        assert (ATA28 / "WBS").is_dir()

    @pytest.mark.parametrize(
        "filename",
        [
            "SYSTEM_MISSION.md",
            "SYSTEM_VISION.md",
            "SYSTEM_OBJECTIVES.md",
            "WBS_LEVEL_1.yaml",
            "WBS_LEVEL_2.yaml",
            "WBS_TRACE_TO_PROJECT.csv",
            "WBS_BUDGET_TT.yaml",
        ],
    )
    def test_wbs_file_exists(self, filename):
        assert (ATA28 / "WBS" / filename).exists()

    def test_wbs_level_1_is_valid_yaml(self):
        path = ATA28 / "WBS" / "WBS_LEVEL_1.yaml"
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data is not None


# =========================================================================
# GOVERNANCE
# =========================================================================


class TestGovernance:
    """System-level governance structure."""

    GOV = ATA28 / "GOVERNANCE"

    def test_governance_directory_exists(self):
        assert self.GOV.is_dir()

    @pytest.mark.parametrize(
        "path",
        [
            "README.md",
            "BASELINES.md",
            "BASELINE_REGISTER.csv",
            "CHANGE_LOG.md",
            "CHANGE_CONTROL/README.md",
            "CHANGE_CONTROL/ECR_TEMPLATE.md",
            "CHANGE_CONTROL/ECO_TEMPLATE.md",
            "CHANGE_CONTROL/ECR/ECR_REGISTER.csv",
            "CHANGE_CONTROL/ECO/ECO_REGISTER.csv",
            "APPROVALS/APPROVAL_MATRIX.csv",
            "APPROVALS/GATE_REVIEWS/PDR_APPROVAL.md",
            "APPROVALS/GATE_REVIEWS/CDR_APPROVAL.md",
            "APPROVALS/GATE_REVIEWS/TRR_APPROVAL.md",
            "APPROVALS/GATE_REVIEWS/FRR_APPROVAL.md",
            "RELEASES/RELEASE_POLICY.md",
            "RELEASES/RELEASE_REGISTER.csv",
            "INCENTIVES/README.md",
            "INCENTIVES/TT_ALLOCATION.yaml",
            "INCENTIVES/TT_DISTRIBUTION.csv",
            "INCENTIVES/TT_POLICY.md",
        ],
    )
    def test_governance_file_exists(self, path):
        assert (self.GOV / path).exists(), f"GOVERNANCE/{path} must exist"


# =========================================================================
# INDEX
# =========================================================================


class TestIndex:
    """System-wide index files."""

    IDX = ATA28 / "INDEX"

    @pytest.mark.parametrize(
        "filename",
        [
            "README.md",
            "SSOT_INDEX.yaml",
            "TRACE_MASTER.csv",
            "ID_REGISTRY.csv",
            "ARTIFACT_CATALOG.yaml",
        ],
    )
    def test_index_file_exists(self, filename):
        assert (self.IDX / filename).exists()

    def test_ssot_index_is_valid_yaml(self):
        with open(self.IDX / "SSOT_INDEX.yaml") as f:
            data = yaml.safe_load(f)
        assert data is not None


# =========================================================================
# Section: 28-10-storage
# =========================================================================


class TestSection:
    """Section-level structure for 28-10-storage."""

    def test_section_directory_exists(self):
        assert SECTION.is_dir()

    def test_section_readme(self):
        assert (SECTION / "README.md").exists()

    def test_section_index(self):
        assert (SECTION / "SECTION_INDEX.yaml").exists()

    def test_genesis_directory(self):
        assert (SECTION / "GENESIS").is_dir()

    @pytest.mark.parametrize(
        "filename",
        [
            "README.md",
            "O-KNOTS.csv",
            "Y-KNOTS.csv",
            "DISCOVERY_LOG.md",
            "GRADUATION_CRITERIA.md",
        ],
    )
    def test_genesis_file_exists(self, filename):
        assert (SECTION / "GENESIS" / filename).exists()


# =========================================================================
# Subject: 28-10-00-fuel-storage-general
# =========================================================================


class TestSubjectRoot:
    """Subject-level root files."""

    def test_subject_directory_exists(self):
        assert SUBJECT.is_dir()

    def test_subject_readme(self):
        assert (SUBJECT / "README.md").exists()

    def test_subject_manifest(self):
        path = SUBJECT / "SUBJECT_MANIFEST.yaml"
        assert path.exists()
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data is not None


class TestSubjectKDB:
    """Subject KDB structure: DEV + LM/SSOT/PLM with LC01-LC10."""

    KDB = SUBJECT / "KDB"

    def test_kdb_readme(self):
        assert (self.KDB / "README.md").exists()

    def test_dev_workspace(self):
        for d in ("working", "trade-studies", "prototypes", "dev-evidence"):
            assert (self.KDB / "DEV" / d).is_dir()

    def test_ssot_policy(self):
        assert (self.KDB / "LM" / "SSOT" / "SSOT_POLICY.md").exists()

    @pytest.mark.parametrize(
        "lc_dir",
        [
            "LC01_PROBLEM_STATEMENT",
            "LC02_SYSTEM_REQUIREMENTS",
            "LC03_SAFETY_RELIABILITY",
            "LC04_DESIGN_DEFINITION_DMU",
            "LC05_ANALYSIS_MODELS_CAE",
            "LC06_INTEGRATION_TEST_PMU",
            "LC07_QUALITY",
            "LC08_FLIGHT_TEST_CERTIFICATION",
            "LC09_GREEN_AIRCRAFT_BASELINES",
            "LC10_INDUSTRIALIZATION_PRODUCTION_CAM",
        ],
    )
    def test_lifecycle_phase_directory(self, lc_dir):
        phase = self.KDB / "LM" / "SSOT" / "PLM" / lc_dir
        assert phase.is_dir(), f"{lc_dir} directory must exist"
        assert (phase / "README.md").exists(), f"{lc_dir}/README.md must exist"
        assert (phase / "PACKAGES").is_dir(), f"{lc_dir}/PACKAGES must exist"


class TestSubjectContracts:
    """Subject CONTRACTS structure."""

    CTR = SUBJECT / "CONTRACTS"

    def test_contracts_readme(self):
        assert (self.CTR / "README.md").exists()

    def test_csdb_contract(self):
        assert (self.CTR / "KITDM-CTR-LM-CSDB_ATA28-10-00.yaml").exists()

    def test_export_contract(self):
        assert (self.CTR / "KITDM-CTR-LM-EXPORT_ATA28-10-00.yaml").exists()

    def test_ietp_contract(self):
        assert (self.CTR / "KITDM-CTR-LM-IETP_ATA28-10-00.yaml").exists()

    def test_approval_log(self):
        assert (self.CTR / "CONTRACT_APPROVAL_LOG.csv").exists()

    def test_evidence_directory(self):
        assert (self.CTR / "EVIDENCE" / "ACCEPTANCE_CRITERIA.md").exists()


class TestSubjectASIT:
    """Subject ASIT structure."""

    def test_asit_readme(self):
        assert (SUBJECT / "ASIT" / "README.md").exists()

    def test_asit_config(self):
        path = SUBJECT / "ASIT" / "asit_config.yaml"
        assert path.exists()
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data is not None

    def test_asit_subdirectories(self):
        for d in ("pipelines", "rules", "runs"):
            assert (SUBJECT / "ASIT" / d).is_dir()


class TestSubjectIDB:
    """Subject IDB structure: OPS + PUB + INDEX."""

    IDB = SUBJECT / "IDB"

    def test_idb_readme(self):
        assert (self.IDB / "README.md").exists()

    def test_idb_governance(self):
        assert (self.IDB / "IDB_GOVERNANCE.md").exists()

    # OPS lifecycle phases
    @pytest.mark.parametrize(
        "lc_dir",
        [
            "LC11_OPERATIONS_CUSTOMIZATION",
            "LC12_SUPPORT_SERVICES",
            "LC13_MRO_SUSTAINMENT",
            "LC14_RETIREMENT_CIRCULARITY",
        ],
    )
    def test_ops_lifecycle_phase(self, lc_dir):
        phase = self.IDB / "OPS" / "LM" / lc_dir
        assert phase.is_dir(), f"{lc_dir} must exist"
        assert (phase / "README.md").exists(), f"{lc_dir}/README.md must exist"

    # LC13 MRO sources
    @pytest.mark.parametrize(
        "source",
        ["Maintenance_Source", "Repair_Source", "Overhaul_Source"],
    )
    def test_lc13_mro_sources(self, source):
        path = self.IDB / "OPS" / "LM" / "LC13_MRO_SUSTAINMENT" / "PACKAGES" / source
        assert path.is_dir(), f"LC13/{source} must exist"
        assert (path / "README.md").exists()

    # Publications
    @pytest.mark.parametrize("pub", ["AMM", "SRM", "CMM"])
    def test_publication_structure(self, pub):
        pub_path = self.IDB / "PUB" / pub
        assert pub_path.is_dir()
        assert (pub_path / "CSDB" / "DM").is_dir()
        assert (pub_path / "CSDB" / "PM").is_dir()
        assert (pub_path / "CSDB" / "BREX").is_dir()
        assert (pub_path / "EXPORT" / "PDF").is_dir()
        assert (pub_path / "EXPORT" / "HTML").is_dir()
        assert (pub_path / "IETP_RUNTIME").is_dir()

    def test_ipc_directory(self):
        assert (self.IDB / "PUB" / "IPC").is_dir()

    # IDB INDEX
    @pytest.mark.parametrize(
        "filename",
        [
            "IDB_RELEASE_NOTES.md",
            "IDB_TRACE_SUMMARY.md",
            "PUBLICATION_MANIFEST.yaml",
            "BASELINE_REFERENCE.yaml",
            "COMPLIANCE_CHECKLIST.md",
            "CHANGELOG.md",
        ],
    )
    def test_idb_index_file(self, filename):
        assert (self.IDB / "INDEX" / filename).exists()
