"""Tests for ATA 28-41 sensor files relocation into 28-41-h2-leak-detection structure.

Validates that the WP-28-06-01 sensor trade study artifacts have been properly
relocated from the flat LC03_SAFETY_RELIABILITY path into the existing
28-41-h2-leak-detection subsection structure.
"""

import csv
import os

import pytest
import yaml

# Repository root
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Base path for ATA 28 fuel system
ATA28_FUEL = os.path.join(
    REPO_ROOT,
    "OPT-IN_FRAMEWORK",
    "T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS",
    "C2-CIRCULAR_CRYOGENIC_CELLS",
    "ATA_28-FUEL",
)

# New target path within h2-leak-detection structure
TARGET_SENSORS = os.path.join(
    ATA28_FUEL,
    "28-41-h2-leak-detection",
    "28-41-00-h2-leak-detection-general",
    "KDB", "LM", "SSOT", "PLM",
    "LC03_SAFETY_RELIABILITY",
    "WP-28-06-01",
    "sensors",
)

# Old flat path (should no longer exist)
OLD_SENSORS = os.path.join(
    ATA28_FUEL,
    "LC03_SAFETY_RELIABILITY",
    "ATA_28-41-00",
    "WP-28-06-01",
    "sensors",
)


class TestSensorFilesExistInNewLocation:
    """Verify sensor files exist in the 28-41-h2-leak-detection structure."""

    def test_target_sensors_directory_exists(self):
        assert os.path.isdir(TARGET_SENSORS), \
            f"Target sensors directory missing: {TARGET_SENSORS}"

    def test_trade_study_md_exists(self):
        path = os.path.join(TARGET_SENSORS, "SEN-28-41-00-trade-study.md")
        assert os.path.isfile(path)

    def test_trade_study_meta_yaml_exists(self):
        path = os.path.join(TARGET_SENSORS, "SEN-28-41-00-trade-study.meta.yaml")
        assert os.path.isfile(path)

    def test_criteria_matrix_csv_exists(self):
        path = os.path.join(TARGET_SENSORS, "SEN-28-41-00-criteria-matrix.csv")
        assert os.path.isfile(path)

    def test_exactly_three_sensor_files(self):
        files = os.listdir(TARGET_SENSORS)
        assert len(files) == 3


class TestOldLocationRemoved:
    """Verify old flat LC paths for ATA 28-41-00 no longer exist."""

    def test_old_sensors_directory_removed(self):
        assert not os.path.exists(OLD_SENSORS), \
            f"Old sensors directory still exists: {OLD_SENSORS}"

    def test_old_lc03_flat_directory_removed(self):
        old_lc03 = os.path.join(ATA28_FUEL, "LC03_SAFETY_RELIABILITY")
        assert not os.path.exists(old_lc03), \
            f"Old flat LC03_SAFETY_RELIABILITY still exists: {old_lc03}"

    def test_old_lc04_ata28_41_removed(self):
        old = os.path.join(ATA28_FUEL, "LC04_DESIGN_DEFINITION", "ATA_28-41-00")
        assert not os.path.exists(old), \
            f"Old flat LC04 ATA_28-41-00 still exists: {old}"

    def test_old_lc05_ata28_41_removed(self):
        old = os.path.join(ATA28_FUEL, "LC05_VERIFICATION_VALIDATION", "ATA_28-41-00")
        assert not os.path.exists(old), \
            f"Old flat LC05 ATA_28-41-00 still exists: {old}"

    def test_old_lc06_ata28_41_removed(self):
        old = os.path.join(ATA28_FUEL, "LC06_CERTIFICATION_EVIDENCE", "ATA_28-41-00")
        assert not os.path.exists(old), \
            f"Old flat LC06 ATA_28-41-00 still exists: {old}"

    def test_no_flat_lc_paths_for_ata28_41(self):
        """No ATA_28-41-00 directories should exist under any flat LC path."""
        import glob
        pattern = os.path.join(ATA28_FUEL, "LC0*", "ATA_28-41-00")
        matches = glob.glob(pattern)
        assert len(matches) == 0, \
            f"Found ATA_28-41-00 in flat LC paths: {matches}"


class TestMetaYamlPaths:
    """Verify meta.yaml file references point to the new location."""

    @pytest.fixture
    def meta(self):
        path = os.path.join(TARGET_SENSORS, "SEN-28-41-00-trade-study.meta.yaml")
        with open(path) as f:
            return yaml.safe_load(f)

    def test_meta_work_package(self, meta):
        assert meta["work_package"] == "WP-28-06-01"

    def test_meta_lc_phase(self, meta):
        assert meta["lc_phase"] == "LC03_SAFETY_RELIABILITY"

    def test_meta_ata(self, meta):
        assert meta["ata"] == "28-41-00"

    def test_meta_files_reference_new_path(self, meta):
        for entry in meta["files"]:
            assert "28-41-h2-leak-detection" in entry["file"], \
                f"File path does not reference new location: {entry['file']}"
            assert "LC03_SAFETY_RELIABILITY/ATA_28-41-00" not in entry["file"], \
                f"File path still references old flat path: {entry['file']}"


class TestWbsReferences:
    """Verify WBS_LEVEL_2.yaml references updated to new location."""

    @pytest.fixture
    def wbs(self):
        path = os.path.join(ATA28_FUEL, "WBS", "WBS_LEVEL_2.yaml")
        with open(path) as f:
            return yaml.safe_load(f)

    def test_wp_28_06_01_files_reference_new_path(self, wbs):
        wp = None
        for item in wbs["work_packages"]:
            if item["id"] == "WP-28-06-01":
                wp = item
                break
        assert wp is not None, "WP-28-06-01 not found in WBS"

        trade_study_output = wp["outputs"][0]
        for file_path in trade_study_output["files"]:
            assert "28-41-h2-leak-detection" in file_path, \
                f"WBS file reference not updated: {file_path}"

    def test_wp_28_06_01_meta_reference_new_path(self, wbs):
        wp = None
        for item in wbs["work_packages"]:
            if item["id"] == "WP-28-06-01":
                wp = item
                break
        assert wp is not None

        trade_study_output = wp["outputs"][0]
        meta_file = trade_study_output["meta_file"]
        assert "28-41-h2-leak-detection" in meta_file, \
            f"WBS meta_file reference not updated: {meta_file}"


class TestSectionIndexUpdated:
    """Verify SECTION_INDEX.yaml metrics reflect the new artifacts."""

    @pytest.fixture
    def section_index(self):
        path = os.path.join(
            ATA28_FUEL, "28-41-h2-leak-detection", "SECTION_INDEX.yaml"
        )
        with open(path) as f:
            return yaml.safe_load(f)

    def test_safety_count_updated(self, section_index):
        assert section_index["metrics"]["safety_count"] == 5

    def test_total_artifacts_updated(self, section_index):
        assert section_index["metrics"]["total_artifacts"] == 5


class TestContentIntegrity:
    """Verify file content is intact after relocation."""

    def test_trade_study_md_has_expected_header(self):
        path = os.path.join(TARGET_SENSORS, "SEN-28-41-00-trade-study.md")
        with open(path) as f:
            content = f.read()
        assert "# Hydrogen Sensor Trade Study Report" in content
        assert "WP-28-06-01" in content

    def test_criteria_matrix_csv_has_expected_columns(self):
        path = os.path.join(TARGET_SENSORS, "SEN-28-41-00-criteria-matrix.csv")
        with open(path) as f:
            reader = csv.reader(f)
            header = next(reader)
        assert "Requirement" in header
        assert "MEMS TCD" in header

    def test_criteria_matrix_has_data_rows(self):
        path = os.path.join(TARGET_SENSORS, "SEN-28-41-00-criteria-matrix.csv")
        with open(path) as f:
            reader = csv.reader(f)
            rows = list(reader)
        assert len(rows) >= 10, "Criteria matrix should have at least 10 rows"
