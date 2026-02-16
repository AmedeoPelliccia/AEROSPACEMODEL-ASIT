"""
Tests for ATA 28-11-00 Trade Studies in KDB/DEV/trade-studies/.

Validates the trade study YAML records created during LC04 design
definition for the C2 Circular Cryogenic Cells LH2 primary tank
architecture.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
TRADE_STUDIES = (
    REPO_ROOT
    / "OPT-IN_FRAMEWORK"
    / "T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS"
    / "C2-CIRCULAR_CRYOGENIC_CELLS"
    / "ATA_28-FUEL"
    / "28-11-lh2-primary-tank"
    / "28-11-00-lh2-primary-tank-general"
    / "KDB"
    / "DEV"
    / "trade-studies"
)


# =========================================================================
# Directory and README
# =========================================================================


class TestTradeStudiesDirectory:
    """Trade-studies directory must contain the expected files."""

    def test_directory_exists(self):
        assert TRADE_STUDIES.is_dir()

    def test_readme_exists(self):
        assert (TRADE_STUDIES / "README.md").exists()

    @pytest.mark.parametrize(
        "filename",
        [
            "TS-28-11-TS01_tank_architecture.yaml",
            "TS-28-11-TS02_materials.yaml",
            "TS-28-11-TS03_insulation_thermal.yaml",
            "evaluation_criteria.yaml",
        ],
    )
    def test_trade_study_file_exists(self, filename):
        assert (TRADE_STUDIES / filename).exists()


# =========================================================================
# YAML Validity
# =========================================================================


class TestTradeStudyYAMLValidity:
    """Every trade study YAML must parse without errors."""

    @pytest.mark.parametrize(
        "filename",
        [
            "TS-28-11-TS01_tank_architecture.yaml",
            "TS-28-11-TS02_materials.yaml",
            "TS-28-11-TS03_insulation_thermal.yaml",
            "evaluation_criteria.yaml",
        ],
    )
    def test_yaml_parses(self, filename):
        path = TRADE_STUDIES / filename
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data is not None


# =========================================================================
# Common Schema for Individual Trade Studies
# =========================================================================


_TS_FILES = [
    "TS-28-11-TS01_tank_architecture.yaml",
    "TS-28-11-TS02_materials.yaml",
    "TS-28-11-TS03_insulation_thermal.yaml",
]


class TestTradeStudySchema:
    """Each trade study record must have the required metadata fields."""

    @pytest.fixture(params=_TS_FILES)
    def ts_data(self, request):
        path = TRADE_STUDIES / request.param
        with open(path) as f:
            return yaml.safe_load(f)

    def test_has_trade_study_id(self, ts_data):
        assert "trade_study_id" in ts_data

    def test_has_title(self, ts_data):
        assert "title" in ts_data

    def test_has_ata_code(self, ts_data):
        assert ts_data.get("ata_code") == "28-11-00"

    def test_has_technology_domain(self, ts_data):
        assert ts_data.get("technology_domain") == "C2"

    def test_has_lifecycle_phase(self, ts_data):
        assert ts_data.get("lifecycle_phase") == "LC04"

    def test_has_options(self, ts_data):
        options = ts_data.get("options")
        assert isinstance(options, list)
        assert len(options) >= 2

    def test_has_preliminary_selection(self, ts_data):
        sel = ts_data.get("preliminary_selection")
        assert sel is not None
        assert "selected_option" in sel
        assert "rationale" in sel

    def test_has_traceability(self, ts_data):
        trace = ts_data.get("traceability")
        assert trace is not None
        assert "derives_from" in trace


# =========================================================================
# Evaluation Criteria
# =========================================================================


class TestEvaluationCriteria:
    """Evaluation criteria YAML must have criteria summing to 100%."""

    @pytest.fixture()
    def eval_data(self):
        path = TRADE_STUDIES / "evaluation_criteria.yaml"
        with open(path) as f:
            return yaml.safe_load(f)

    def test_criteria_present(self, eval_data):
        assert isinstance(eval_data.get("criteria"), list)
        assert len(eval_data["criteria"]) >= 3

    def test_weights_sum_to_100(self, eval_data):
        total = sum(c["weight_pct"] for c in eval_data["criteria"])
        assert total == 100

    def test_open_risks_present(self, eval_data):
        risks = eval_data.get("open_risks")
        assert isinstance(risks, list)
        assert len(risks) >= 1

    def test_next_actions_present(self, eval_data):
        actions = eval_data.get("next_actions")
        assert isinstance(actions, list)
        assert len(actions) >= 1


# =========================================================================
# CS-25 Compliance Matrix
# =========================================================================


class TestCS25ComplianceMatrix:
    """CS-25 compliance matrix must have required structure."""

    @pytest.fixture()
    def matrix_data(self):
        path = TRADE_STUDIES / "CS25_compliance_matrix.yaml"
        with open(path) as f:
            return yaml.safe_load(f)

    def test_has_matrix_id(self, matrix_data):
        assert matrix_data.get("matrix_id") == "CM-28-11-CS25"

    def test_has_sections(self, matrix_data):
        sections = matrix_data.get("sections")
        assert isinstance(sections, list)
        assert len(sections) >= 2

    def test_has_special_conditions(self, matrix_data):
        sc = matrix_data.get("special_conditions")
        assert isinstance(sc, list)
        assert len(sc) >= 1

    def test_has_evidence_package(self, matrix_data):
        ep = matrix_data.get("evidence_package")
        assert isinstance(ep, list)
        assert len(ep) >= 1


# =========================================================================
# Artifact Catalog Registration
# =========================================================================


class TestArtifactCatalogTradeStudies:
    """ARTIFACT_CATALOG.yaml must include 28-11 trade_studies entry."""

    @pytest.fixture()
    def catalog_data(self):
        path = (
            REPO_ROOT
            / "OPT-IN_FRAMEWORK"
            / "T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS"
            / "C2-CIRCULAR_CRYOGENIC_CELLS"
            / "ATA_28-FUEL"
            / "INDEX"
            / "ARTIFACT_CATALOG.yaml"
        )
        with open(path) as f:
            return yaml.safe_load(f)

    def test_trade_studies_28_11_registered(self, catalog_data):
        ts = catalog_data.get("artifact_types", {}).get("trade_studies_28_11")
        assert ts is not None

    def test_trade_studies_28_11_count(self, catalog_data):
        ts = catalog_data["artifact_types"]["trade_studies_28_11"]
        assert ts["count"] == 3
