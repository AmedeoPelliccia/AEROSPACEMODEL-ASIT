"""
Tests for ATA 28-10-00 Parametric Models in KDB/DEV/models/.

Validates the LC05 parametric model YAML records created for the C2
Circular Cryogenic Cells fuel storage system: tank geometry
optimisation, MLI thermal stack-up, and mounting / load path analysis.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
MODELS = (
    REPO_ROOT
    / "OPT-IN_FRAMEWORK"
    / "T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS"
    / "C2-CIRCULAR_CRYOGENIC_CELLS"
    / "ATA_28-FUEL"
    / "28-10-storage"
    / "28-10-00-fuel-storage-general"
    / "KDB"
    / "DEV"
    / "models"
)


# =========================================================================
# Directory and README
# =========================================================================


class TestModelsDirectory:
    """Models directory must contain the expected files."""

    def test_directory_exists(self):
        assert MODELS.is_dir()

    def test_readme_exists(self):
        assert (MODELS / "README.md").exists()

    @pytest.mark.parametrize(
        "filename",
        [
            "PM-28-10-PM01_tank_geometry.yaml",
            "PM-28-10-PM02_mli_stackup.yaml",
            "PM-28-10-PM03_mounting_loads.yaml",
        ],
    )
    def test_model_yaml_exists(self, filename):
        assert (MODELS / filename).exists()

    @pytest.mark.parametrize(
        "filename",
        [
            "PM-28-10-PM01_tank_geometry.md",
            "PM-28-10-PM02_mli_stackup.md",
            "PM-28-10-PM03_mounting_loads.md",
        ],
    )
    def test_model_md_exists(self, filename):
        assert (MODELS / filename).exists()


# =========================================================================
# YAML Validity
# =========================================================================


_PM_FILES = [
    "PM-28-10-PM01_tank_geometry.yaml",
    "PM-28-10-PM02_mli_stackup.yaml",
    "PM-28-10-PM03_mounting_loads.yaml",
]


class TestModelYAMLValidity:
    """Every parametric model YAML must parse without errors."""

    @pytest.mark.parametrize("filename", _PM_FILES)
    def test_yaml_parses(self, filename):
        path = MODELS / filename
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data is not None


# =========================================================================
# Common Schema Checks
# =========================================================================


class TestModelSchema:
    """Each parametric model record must have the required metadata."""

    @pytest.fixture(params=_PM_FILES)
    def pm_data(self, request):
        path = MODELS / request.param
        with open(path) as f:
            return yaml.safe_load(f)

    def test_has_model_id(self, pm_data):
        assert "model_id" in pm_data

    def test_has_title(self, pm_data):
        assert "title" in pm_data

    def test_has_ata_code(self, pm_data):
        assert pm_data.get("ata_code") == "28-10-00"

    def test_has_technology_domain(self, pm_data):
        assert pm_data.get("technology_domain") == "C2"

    def test_has_lifecycle_phase(self, pm_data):
        assert pm_data.get("lifecycle_phase") == "LC05"

    def test_has_objective(self, pm_data):
        assert "objective" in pm_data

    def test_has_traceability(self, pm_data):
        trace = pm_data.get("traceability")
        assert trace is not None
        assert "derives_from" in trace

    def test_has_feeds(self, pm_data):
        feeds = pm_data.get("feeds")
        assert isinstance(feeds, list)
        assert len(feeds) >= 1

    def test_has_outputs(self, pm_data):
        outputs = pm_data.get("outputs")
        assert isinstance(outputs, list)
        assert len(outputs) >= 2


# =========================================================================
# PM01 — Tank Geometry Specific
# =========================================================================


class TestPM01TankGeometry:
    """Tank geometry model must have parameters and governing equations."""

    @pytest.fixture()
    def pm01(self):
        path = MODELS / "PM-28-10-PM01_tank_geometry.yaml"
        with open(path) as f:
            return yaml.safe_load(f)

    def test_has_parameters(self, pm01):
        params = pm01.get("parameters")
        assert isinstance(params, list)
        assert len(params) >= 4

    def test_has_governing_equations(self, pm01):
        eqs = pm01.get("governing_equations")
        assert isinstance(eqs, list)
        assert len(eqs) >= 3

    def test_has_optimisation(self, pm01):
        opt = pm01.get("optimisation")
        assert opt is not None
        assert "objective_function" in opt
        assert "constraints" in opt
        assert "design_variables" in opt

    def test_has_material_candidates(self, pm01):
        mats = pm01.get("material_candidates")
        assert isinstance(mats, list)
        assert len(mats) >= 2

    def test_derives_from_ts01(self, pm01):
        derives = pm01["traceability"]["derives_from"]
        assert "TS-28-10-TS01" in derives

    def test_satisfies_fbl_req_001(self, pm01):
        satisfies = pm01["traceability"]["satisfies"]
        assert "FBL-REQ-001" in satisfies


# =========================================================================
# PM02 — MLI Thermal Stack-Up Specific
# =========================================================================


class TestPM02MLIStackup:
    """MLI model must have thermal parameters and reference cases."""

    @pytest.fixture()
    def pm02(self):
        path = MODELS / "PM-28-10-PM02_mli_stackup.yaml"
        with open(path) as f:
            return yaml.safe_load(f)

    def test_has_parameters(self, pm02):
        params = pm02.get("parameters")
        assert isinstance(params, list)
        assert len(params) >= 5

    def test_has_governing_equations(self, pm02):
        eqs = pm02.get("governing_equations")
        assert isinstance(eqs, list)
        assert len(eqs) >= 4

    def test_has_reference_cases(self, pm02):
        cases = pm02.get("reference_cases")
        assert isinstance(cases, list)
        assert len(cases) >= 2

    def test_has_optimisation(self, pm02):
        opt = pm02.get("optimisation")
        assert opt is not None
        assert "constraints" in opt

    def test_derives_from_ts03(self, pm02):
        derives = pm02["traceability"]["derives_from"]
        assert "TS-28-10-TS03" in derives

    def test_satisfies_fbl_req_003(self, pm02):
        satisfies = pm02["traceability"]["satisfies"]
        assert "FBL-REQ-003" in satisfies


# =========================================================================
# PM03 — Mounting / Load Path Specific
# =========================================================================


class TestPM03MountingLoads:
    """Mounting model must define load cases and acceptance criteria."""

    @pytest.fixture()
    def pm03(self):
        path = MODELS / "PM-28-10-PM03_mounting_loads.yaml"
        with open(path) as f:
            return yaml.safe_load(f)

    def test_has_load_cases(self, pm03):
        lcs = pm03.get("load_cases")
        assert isinstance(lcs, list)
        assert len(lcs) >= 5

    def test_has_vibration_cases(self, pm03):
        lcs = pm03["load_cases"]
        vib = [lc for lc in lcs if lc.get("type") == "vibration"]
        assert len(vib) >= 1

    def test_has_crash_cases(self, pm03):
        lcs = pm03["load_cases"]
        crash = [lc for lc in lcs if lc.get("type") == "crash"]
        assert len(crash) >= 3

    def test_has_thermal_cycling_cases(self, pm03):
        lcs = pm03["load_cases"]
        therm = [lc for lc in lcs if lc.get("type") == "thermal_cycling"]
        assert len(therm) >= 1

    def test_has_mount_concepts(self, pm03):
        mounts = pm03.get("mount_concepts")
        assert isinstance(mounts, list)
        assert len(mounts) >= 2

    def test_has_analysis_methods(self, pm03):
        methods = pm03.get("analysis_methods")
        assert isinstance(methods, list)
        assert len(methods) >= 3

    def test_has_acceptance_criteria(self, pm03):
        criteria = pm03.get("acceptance_criteria")
        assert isinstance(criteria, list)
        assert len(criteria) >= 3

    def test_derives_from_fbl(self, pm03):
        derives = pm03["traceability"]["derives_from"]
        assert "FBL-Q100-ATA28-001" in derives

    def test_satisfies_fbl_req_010(self, pm03):
        satisfies = pm03["traceability"]["satisfies"]
        assert "FBL-REQ-010" in satisfies


# =========================================================================
# Artifact Catalog Registration
# =========================================================================


class TestArtifactCatalogModels:
    """ARTIFACT_CATALOG.yaml must include parametric_models entry."""

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

    def test_parametric_models_registered(self, catalog_data):
        pm = catalog_data.get("artifact_types", {}).get("parametric_models")
        assert pm is not None

    def test_parametric_models_count(self, catalog_data):
        pm = catalog_data["artifact_types"]["parametric_models"]
        assert pm["count"] == 3


# =========================================================================
# FBL Evidence Package
# =========================================================================


class TestFBLEvidencePackageModels:
    """FBL evidence package must reference the parametric models."""

    @pytest.fixture()
    def fbl_data(self):
        path = (
            REPO_ROOT
            / "OPT-IN_FRAMEWORK"
            / "T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS"
            / "C2-CIRCULAR_CRYOGENIC_CELLS"
            / "ATA_28-FUEL"
            / "28-10-storage"
            / "28-10-00-fuel-storage-general"
            / "KDB"
            / "LM"
            / "SSOT"
            / "FBL-Q100-ATA28-001.yaml"
        )
        with open(path) as f:
            return yaml.safe_load(f)

    @pytest.mark.parametrize(
        "artifact",
        [
            "PM-28-10-PM01_tank_geometry.yaml",
            "PM-28-10-PM02_mli_stackup.yaml",
            "PM-28-10-PM03_mounting_loads.yaml",
        ],
    )
    def test_model_in_evidence_package(self, fbl_data, artifact):
        assert artifact in fbl_data.get("evidence_package", [])


# =========================================================================
# KNU Plan & Traceability
# =========================================================================


class TestKNUPlanModels:
    """KNU plan must contain entries for the three parametric models."""

    @pytest.fixture()
    def knu_lines(self):
        path = (
            REPO_ROOT
            / "OPT-IN_FRAMEWORK"
            / "T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS"
            / "C2-CIRCULAR_CRYOGENIC_CELLS"
            / "ATA_28-FUEL"
            / "28-10-storage"
            / "28-10-00-fuel-storage-general"
            / "KDB"
            / "LM"
            / "SSOT"
            / "PLM"
            / "LC01_PROBLEM_STATEMENT"
            / "KNU_PLAN.csv"
        )
        return path.read_text().strip().splitlines()

    @pytest.mark.parametrize(
        "knu_id",
        ["KNU-C2-004", "KNU-C2-005", "KNU-C2-006"],
    )
    def test_knu_entry_exists(self, knu_lines, knu_id):
        assert any(knu_id in line for line in knu_lines)


class TestTraceLCModels:
    """TRACE_LC01.csv must map new KNOTs to KNUs."""

    @pytest.fixture()
    def trace_lines(self):
        path = (
            REPO_ROOT
            / "OPT-IN_FRAMEWORK"
            / "T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS"
            / "C2-CIRCULAR_CRYOGENIC_CELLS"
            / "ATA_28-FUEL"
            / "28-10-storage"
            / "28-10-00-fuel-storage-general"
            / "KDB"
            / "LM"
            / "SSOT"
            / "PLM"
            / "LC01_PROBLEM_STATEMENT"
            / "TRACE_LC01.csv"
        )
        return path.read_text().strip().splitlines()

    @pytest.mark.parametrize(
        "knot_id",
        ["KNOT-C2-004", "KNOT-C2-005", "KNOT-C2-006"],
    )
    def test_trace_entry_exists(self, trace_lines, knot_id):
        assert any(knot_id in line for line in trace_lines)
