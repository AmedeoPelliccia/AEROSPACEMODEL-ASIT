"""
Tests for ATA 28-41-00 LC04 Design Definition Relocation.

Validates that LC04 design definition artifacts for H₂ leak detection
(ATA 28-41-00) have been relocated from the flat path:

    LC04_DESIGN_DEFINITION/ATA_28-41-00/WP-28-06-XX/{category}/

to the canonical subject-scoped path:

    28-41-h2-leak-detection/28-41-00-h2-leak-detection-general/
        KDB/LM/SSOT/PLM/LC04_DESIGN_DEFINITION_DMU/PACKAGES/DESIGN/{category}/

Work packages affected:
  WP-28-06-01  Sensor Selection      → DESIGN/sensors/
  WP-28-06-02  System Architecture   → DESIGN/architecture/
  WP-28-06-02  Sensor Placement      → DESIGN/placement/
  WP-28-06-03  Threshold Calibration → DESIGN/calibration/
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

NEW_BASE = (
    ATA28
    / "28-41-h2-leak-detection"
    / "28-41-00-h2-leak-detection-general"
    / "KDB" / "LM" / "SSOT" / "PLM"
    / "LC04_DESIGN_DEFINITION_DMU"
    / "PACKAGES" / "DESIGN"
)

OLD_BASE = ATA28 / "LC04_DESIGN_DEFINITION" / "ATA_28-41-00"

# =========================================================================
# Meta files that must exist at new canonical locations
# =========================================================================
META_FILES = [
    ("sensors", "SEN-28-41-00-selection-record.meta.yaml"),
    ("architecture", "LDS-28-41-00-architecture.meta.yaml"),
    ("placement", "LDS-28-41-00-placement.meta.yaml"),
    ("calibration", "CAL-28-41-00-threshold-spec.meta.yaml"),
]


# =========================================================================
# Old flat path must be removed
# =========================================================================
class TestOldPathRemoved:
    """The old flat LC04_DESIGN_DEFINITION/ATA_28-41-00 directory must not exist."""

    def test_old_directory_absent(self):
        assert not OLD_BASE.exists(), (
            f"Old flat path {OLD_BASE.relative_to(REPO_ROOT)} must be removed"
        )


# =========================================================================
# New canonical directory structure
# =========================================================================
class TestCanonicalDirectories:
    """PACKAGES/DESIGN must contain the four relocated sub-directories."""

    @pytest.mark.parametrize("subdir", ["sensors", "architecture", "placement", "calibration"])
    def test_design_subdirectory_exists(self, subdir):
        assert (NEW_BASE / subdir).is_dir(), f"DESIGN/{subdir} must exist"


# =========================================================================
# Meta files at new locations
# =========================================================================
class TestMetaFilesPresent:
    """Each relocated meta.yaml must exist at the new canonical path."""

    @pytest.mark.parametrize("subdir,filename", META_FILES)
    def test_meta_file_exists(self, subdir, filename):
        path = NEW_BASE / subdir / filename
        assert path.exists(), f"{subdir}/{filename} must exist at new path"

    @pytest.mark.parametrize("subdir,filename", META_FILES)
    def test_meta_file_is_valid_yaml(self, subdir, filename):
        path = NEW_BASE / subdir / filename
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data is not None


# =========================================================================
# Meta file content validation
# =========================================================================
class TestMetaFileContent:
    """Relocated meta files must reference the new canonical paths."""

    @pytest.mark.parametrize("subdir,filename", META_FILES)
    def test_meta_files_reference_new_path(self, subdir, filename):
        path = NEW_BASE / subdir / filename
        with open(path) as f:
            data = yaml.safe_load(f)
        for entry in data.get("files", []):
            file_ref = entry.get("file", "")
            assert "LC04_DESIGN_DEFINITION/ATA_28-41-00" not in file_ref, (
                f"Meta file {filename} still references old flat path in files[].file"
            )
            assert "28-41-h2-leak-detection" in file_ref, (
                f"Meta file {filename} must reference canonical path"
            )

    @pytest.mark.parametrize("subdir,filename", META_FILES)
    def test_meta_lc_phase(self, subdir, filename):
        path = NEW_BASE / subdir / filename
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data.get("lc_phase") == "LC04_DESIGN_DEFINITION"

    @pytest.mark.parametrize("subdir,filename", META_FILES)
    def test_meta_ata(self, subdir, filename):
        path = NEW_BASE / subdir / filename
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data.get("ata") == "28-41-00"

    @pytest.mark.parametrize("subdir,filename", META_FILES)
    def test_meta_domain(self, subdir, filename):
        path = NEW_BASE / subdir / filename
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data.get("domain") == "C2-CIRCULAR_CRYOGENIC_CELLS"


# =========================================================================
# WBS Level 2 references updated
# =========================================================================
class TestWBSReferences:
    """WBS_LEVEL_2.yaml must reference canonical paths for LC04 28-41 outputs."""

    @pytest.fixture
    def wbs(self):
        path = ATA28 / "WBS" / "WBS_LEVEL_2.yaml"
        with open(path) as f:
            return yaml.safe_load(f)

    @pytest.fixture
    def wbs_text(self):
        path = ATA28 / "WBS" / "WBS_LEVEL_2.yaml"
        return path.read_text(encoding="utf-8")

    def test_no_old_lc04_references(self, wbs_text):
        assert "LC04_DESIGN_DEFINITION/ATA_28-41-00" not in wbs_text, (
            "WBS must not reference old flat LC04 path for ATA 28-41-00"
        )

    def _find_wp(self, wbs, wp_id):
        for item in wbs.get("work_packages", []):
            if item.get("id") == wp_id:
                return item
        return None

    @pytest.mark.parametrize(
        "wp_id,output_id,expected_subdir",
        [
            ("WP-28-06-01", "selected_sensor_baseline", "sensors"),
            ("WP-28-06-02", "leak_detection_architecture", "architecture"),
            ("WP-28-06-02", "sensor_placement_definition", "placement"),
            ("WP-28-06-03", "threshold_definition", "calibration"),
        ],
    )
    def test_wbs_output_files_use_canonical_path(self, wbs, wp_id, output_id, expected_subdir):
        wp = self._find_wp(wbs, wp_id)
        assert wp is not None, f"Work package {wp_id} not found in WBS"
        output = None
        for o in wp.get("outputs", []):
            if o.get("id") == output_id:
                output = o
                break
        assert output is not None, f"Output {output_id} not found in {wp_id}"
        canonical = f"PACKAGES/DESIGN/{expected_subdir}/"
        for f in output.get("files", []):
            assert canonical in f, (
                f"File '{f}' in {wp_id}/{output_id} must use canonical DESIGN/{expected_subdir}/ path"
            )

    @pytest.mark.parametrize(
        "wp_id,output_id,expected_subdir",
        [
            ("WP-28-06-01", "selected_sensor_baseline", "sensors"),
            ("WP-28-06-02", "leak_detection_architecture", "architecture"),
            ("WP-28-06-02", "sensor_placement_definition", "placement"),
            ("WP-28-06-03", "threshold_definition", "calibration"),
        ],
    )
    def test_wbs_meta_file_uses_canonical_path(self, wbs, wp_id, output_id, expected_subdir):
        wp = self._find_wp(wbs, wp_id)
        assert wp is not None
        output = None
        for o in wp.get("outputs", []):
            if o.get("id") == output_id:
                output = o
                break
        assert output is not None
        meta = output.get("meta_file", "")
        canonical = f"PACKAGES/DESIGN/{expected_subdir}/"
        assert canonical in meta, (
            f"Meta file ref '{meta}' must use canonical DESIGN/{expected_subdir}/ path"
        )
