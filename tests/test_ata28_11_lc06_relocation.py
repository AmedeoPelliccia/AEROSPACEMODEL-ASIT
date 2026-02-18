"""
Tests for ATA 28-11-00 LC06 Certification Evidence relocation.

Validates that LC06_CERTIFICATION_EVIDENCE artifacts for ATA 28-11-00
have been relocated from the flat path
  ATA_28-FUEL/LC06_CERTIFICATION_EVIDENCE/ATA_28-11-00/
to the canonical nested path
  ATA_28-FUEL/28-11-lh2-primary-tank/28-11-00-lh2-primary-tank-general/
    KDB/LM/SSOT/PLM/LC06_CERTIFICATION_EVIDENCE/
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
LC06_NEW = (
    ATA28
    / "28-11-lh2-primary-tank"
    / "28-11-00-lh2-primary-tank-general"
    / "KDB"
    / "LM"
    / "SSOT"
    / "PLM"
    / "LC06_CERTIFICATION_EVIDENCE"
)
LC06_OLD = ATA28 / "LC06_CERTIFICATION_EVIDENCE" / "ATA_28-11-00"


# =========================================================================
# Old flat-path removal
# =========================================================================


class TestOldPathRemoved:
    """The old flat-path ATA_28-11-00 directory must no longer exist."""

    def test_old_ata_28_11_00_directory_removed(self):
        assert not LC06_OLD.exists(), (
            "Old flat path LC06_CERTIFICATION_EVIDENCE/ATA_28-11-00 "
            "must be removed after relocation"
        )


# =========================================================================
# New canonical directory structure
# =========================================================================


class TestLC06DirectoryStructure:
    """LC06_CERTIFICATION_EVIDENCE directory at canonical 28-11 path."""

    def test_lc06_certification_evidence_directory_exists(self):
        assert LC06_NEW.is_dir(), "LC06_CERTIFICATION_EVIDENCE directory must exist"

    def test_readme_exists(self):
        assert (LC06_NEW / "README.md").exists(), "README.md must exist"

    @pytest.mark.parametrize(
        "subdir",
        [
            "WP-28-03-04/materials",
            "WP-28-03-05/manufacturing",
            "WP-28-03-05/tooling",
        ],
    )
    def test_work_package_subdirectory_exists(self, subdir):
        assert (LC06_NEW / subdir).is_dir(), f"{subdir} directory must exist"


# =========================================================================
# Meta-YAML files at new location
# =========================================================================

META_FILES = [
    "WP-28-03-04/materials/MAT-28-11-00-qualification-report.meta.yaml",
    "WP-28-03-05/manufacturing/MFG-28-11-00-process-flow.meta.yaml",
    "WP-28-03-05/tooling/TLG-28-11-00-package.meta.yaml",
]


class TestLC06MetaFiles:
    """Meta-YAML files must exist and be valid at the new canonical path."""

    @pytest.mark.parametrize("rel_path", META_FILES)
    def test_meta_file_exists(self, rel_path):
        assert (LC06_NEW / rel_path).exists(), f"{rel_path} must exist"

    @pytest.mark.parametrize("rel_path", META_FILES)
    def test_meta_file_is_valid_yaml(self, rel_path):
        with open(LC06_NEW / rel_path) as f:
            data = yaml.safe_load(f)
        assert data is not None, f"{rel_path} must be valid YAML"

    @pytest.mark.parametrize("rel_path", META_FILES)
    def test_meta_file_has_lc_phase(self, rel_path):
        with open(LC06_NEW / rel_path) as f:
            data = yaml.safe_load(f)
        assert data["lc_phase"] == "LC06_CERTIFICATION_EVIDENCE"

    @pytest.mark.parametrize("rel_path", META_FILES)
    def test_meta_file_has_ata_28_11_00(self, rel_path):
        with open(LC06_NEW / rel_path) as f:
            data = yaml.safe_load(f)
        assert data["ata"] == "28-11-00"

    @pytest.mark.parametrize("rel_path", META_FILES)
    def test_meta_file_paths_use_canonical_prefix(self, rel_path):
        """File references inside meta.yaml must use the canonical path."""
        canonical_prefix = (
            "28-11-lh2-primary-tank/28-11-00-lh2-primary-tank-general/"
            "KDB/LM/SSOT/PLM/LC06_CERTIFICATION_EVIDENCE"
        )
        with open(LC06_NEW / rel_path) as f:
            data = yaml.safe_load(f)
        for entry in data["files"]:
            assert entry["file"].startswith(canonical_prefix), (
                f"File path '{entry['file']}' must start with canonical prefix"
            )

    @pytest.mark.parametrize("rel_path", META_FILES)
    def test_meta_file_no_old_flat_path(self, rel_path):
        """No references to the old flat path should remain."""
        with open(LC06_NEW / rel_path) as f:
            content = f.read()
        assert "LC06_CERTIFICATION_EVIDENCE/ATA_28-11-00" not in content


# =========================================================================
# WBS_LEVEL_2.yaml references
# =========================================================================


class TestWBSReferences:
    """WBS_LEVEL_2.yaml must reference the new canonical paths."""

    WBS = ATA28 / "WBS" / "WBS_LEVEL_2.yaml"

    def test_wbs_is_valid_yaml(self):
        with open(self.WBS) as f:
            data = yaml.safe_load(f)
        assert data is not None

    def test_wbs_no_old_lc06_ata_28_11_references(self):
        with open(self.WBS) as f:
            content = f.read()
        assert "LC06_CERTIFICATION_EVIDENCE/ATA_28-11-00" not in content, (
            "WBS must not reference old flat LC06 path for ATA 28-11-00"
        )

    def test_wbs_has_canonical_lc06_references(self):
        canonical_prefix = (
            "28-11-lh2-primary-tank/28-11-00-lh2-primary-tank-general/"
            "KDB/LM/SSOT/PLM/LC06_CERTIFICATION_EVIDENCE"
        )
        with open(self.WBS) as f:
            content = f.read()
        assert canonical_prefix in content, (
            "WBS must reference canonical LC06 path for ATA 28-11-00"
        )
