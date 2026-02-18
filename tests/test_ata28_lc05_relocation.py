"""
Tests for LC05 Verification & Validation relocation from flat
LC05_VERIFICATION_VALIDATION/ into canonical subsystem PACKAGES/VALIDATION/.

Validates that 7 meta.yaml files were relocated from the flat
ATA_28-FUEL/LC05_VERIFICATION_VALIDATION/ATA_28-XX-00/ structure into
28-XX-*/28-XX-00-*/KDB/LM/SSOT/PLM/LC05_ANALYSIS_MODELS_CAE/PACKAGES/VALIDATION/.
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

# Canonical subsystem paths
VALIDATION_28_10 = (
    ATA28
    / "28-10-storage"
    / "28-10-00-fuel-storage-general"
    / "KDB" / "LM" / "SSOT" / "PLM"
    / "LC05_ANALYSIS_MODELS_CAE" / "PACKAGES" / "VALIDATION"
)
VALIDATION_28_11 = (
    ATA28
    / "28-11-lh2-primary-tank"
    / "28-11-00-lh2-primary-tank-general"
    / "KDB" / "LM" / "SSOT" / "PLM"
    / "LC05_ANALYSIS_MODELS_CAE" / "PACKAGES" / "VALIDATION"
)
VALIDATION_28_23 = (
    ATA28
    / "28-23-pressure-control"
    / "28-23-00-pressure-control-general"
    / "KDB" / "LM" / "SSOT" / "PLM"
    / "LC05_ANALYSIS_MODELS_CAE" / "PACKAGES" / "VALIDATION"
)
VALIDATION_28_41 = (
    ATA28
    / "28-41-h2-leak-detection"
    / "28-41-00-h2-leak-detection-general"
    / "KDB" / "LM" / "SSOT" / "PLM"
    / "LC05_ANALYSIS_MODELS_CAE" / "PACKAGES" / "VALIDATION"
)


# =========================================================================
# Flat directory removed
# =========================================================================


class TestFlatLC05Removed:
    """The old flat LC05_VERIFICATION_VALIDATION directory must not exist."""

    def test_flat_lc05_removed(self):
        flat = ATA28 / "LC05_VERIFICATION_VALIDATION"
        assert not flat.exists(), (
            f"Flat LC05_VERIFICATION_VALIDATION still exists at {flat}"
        )


# =========================================================================
# Relocated meta.yaml files exist
# =========================================================================


class TestRelocatedFilesExist:
    """All 7 meta.yaml files must exist at their canonical locations."""

    @pytest.mark.parametrize(
        "path",
        [
            VALIDATION_28_10 / "WP-28-03-02" / "thermal" / "THM-28-10-00-model.meta.yaml",
            VALIDATION_28_10 / "WP-28-03-02" / "tests" / "ITP-28-10-00-insulation-test-plan.meta.yaml",
            VALIDATION_28_11 / "WP-28-03-04" / "materials" / "MAT-28-11-00-test-plan.meta.yaml",
            VALIDATION_28_11 / "WP-28-03-04" / "materials" / "MAT-28-11-00-allowables.meta.yaml",
            VALIDATION_28_23 / "WP-28-03-03" / "safety" / "FMEA-28-23-00-pressure.meta.yaml",            VALIDATION_28_41 / "WP-28-06-02" / "reliability" / "LDS-28-41-00-redundancy.meta.yaml",
            VALIDATION_28_41 / "WP-28-06-03" / "calibration" / "CAL-28-41-00-procedure.meta.yaml",
        ],
        ids=[
            "THM-28-10-00-model",
            "ITP-28-10-00-insulation-test-plan",
            "MAT-28-11-00-test-plan",
            "MAT-28-11-00-allowables",
            "FMEA-28-23-00-pressure",
            "LDS-28-41-00-redundancy",
            "CAL-28-41-00-procedure",
        ],
    )
    def test_file_exists(self, path):
        assert path.is_file(), f"Relocated file not found: {path}"


# =========================================================================
# Meta YAML content validation
# =========================================================================


class TestMetaYAMLContent:
    """Relocated meta files must have updated lc_phase and valid YAML."""

    @pytest.fixture(params=[
        VALIDATION_28_10 / "WP-28-03-02" / "thermal" / "THM-28-10-00-model.meta.yaml",
        VALIDATION_28_10 / "WP-28-03-02" / "tests" / "ITP-28-10-00-insulation-test-plan.meta.yaml",
        VALIDATION_28_11 / "WP-28-03-04" / "materials" / "MAT-28-11-00-test-plan.meta.yaml",
        VALIDATION_28_11 / "WP-28-03-04" / "materials" / "MAT-28-11-00-allowables.meta.yaml",
        VALIDATION_28_23 / "WP-28-03-03" / "safety" / "FMEA-28-23-00-pressure.meta.yaml",
        VALIDATION_28_41 / "WP-28-06-02" / "reliability" / "LDS-28-41-00-redundancy.meta.yaml",
        VALIDATION_28_41 / "WP-28-06-03" / "calibration" / "CAL-28-41-00-procedure.meta.yaml",
    ])
    def meta(self, request):
        path = request.param
        with open(path) as f:
            return yaml.safe_load(f)

    def test_lc_phase_updated(self, meta):
        assert meta["lc_phase"] == "LC05_ANALYSIS_MODELS_CAE", (
            f"lc_phase not updated: {meta['lc_phase']}"
        )

    def test_no_old_path_references(self, meta):
        for entry in meta.get("files", []):
            assert "LC05_VERIFICATION_VALIDATION" not in entry.get("file", ""), (
                f"Old path reference found in files: {entry['file']}"
            )

    def test_has_required_fields(self, meta):
        for field in ("output_id", "work_package", "lc_phase", "ata", "integrity"):
            assert field in meta, f"Missing required field: {field}"


# =========================================================================
# WBS path references
# =========================================================================


class TestWBSReferences:
    """WBS_LEVEL_2.yaml must not contain old LC05_VERIFICATION_VALIDATION paths."""

    @pytest.fixture(scope="class")
    def wbs_text(self):
        wbs_path = ATA28 / "WBS" / "WBS_LEVEL_2.yaml"
        return wbs_path.read_text()

    @pytest.fixture(scope="class")
    def wbs_data(self, wbs_text):
        return yaml.safe_load(wbs_text)

    def test_no_old_lc05_refs_in_wbs(self, wbs_text):
        assert "LC05_VERIFICATION_VALIDATION" not in wbs_text, (
            "WBS still references LC05_VERIFICATION_VALIDATION"
        )

    def test_wbs_valid_yaml(self, wbs_data):
        assert "work_packages" in wbs_data

    def test_wbs_has_canonical_paths(self, wbs_text):
        assert "LC05_ANALYSIS_MODELS_CAE/PACKAGES/VALIDATION" in wbs_text


# =========================================================================
# Canonical VALIDATION directories exist
# =========================================================================


class TestCanonicalDirectories:
    """VALIDATION directories must exist under each subsystem's LC05."""

    @pytest.mark.parametrize(
        "validation_dir",
        [VALIDATION_28_10, VALIDATION_28_11, VALIDATION_28_23, VALIDATION_28_41],
        ids=["28-10-storage", "28-11-lh2-primary-tank", "28-23-pressure-control", "28-41-h2-leak-detection"],
    )
    def test_validation_dir_exists(self, validation_dir):
        assert validation_dir.is_dir(), f"VALIDATION dir missing: {validation_dir}"
