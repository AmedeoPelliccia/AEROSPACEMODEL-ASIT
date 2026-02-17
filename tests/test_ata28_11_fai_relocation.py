"""
Tests for FAI relocation from flat LC07_INDUSTRIALIZATION path
to canonical 28-11-lh2-primary-tank structure.

Validates that WP-28-03-05 FAI (First Article Inspection) artifacts
have been relocated to the canonical LC07_QUALITY/PACKAGES/ACCEPTANCE
path under the 28-11 section hierarchy.
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

# Old flat path (should no longer exist)
OLD_FAI = ATA28 / "LC07_INDUSTRIALIZATION" / "ATA_28-11-00" / "WP-28-03-05" / "fai"

# New canonical path
SECTION = ATA28 / "28-11-lh2-primary-tank"
SUBJECT = SECTION / "28-11-00-lh2-primary-tank-general"
KDB_PLM = SUBJECT / "KDB" / "LM" / "SSOT" / "PLM"
LC07 = KDB_PLM / "LC07_QUALITY"
ACCEPTANCE = LC07 / "PACKAGES" / "ACCEPTANCE"
NEW_FAI = ACCEPTANCE / "WP-28-03-05" / "fai"

NEW_REL = (
    "28-11-lh2-primary-tank/28-11-00-lh2-primary-tank-general"
    "/KDB/LM/SSOT/PLM/LC07_QUALITY/PACKAGES/ACCEPTANCE/WP-28-03-05/fai"
)


# =========================================================================
# Old Flat Path Removal
# =========================================================================


class TestOldPathRemoved:
    """The flat LC07_INDUSTRIALIZATION FAI path must no longer exist."""

    def test_old_fai_directory_absent(self):
        assert not OLD_FAI.exists(), (
            f"Old flat path {OLD_FAI.relative_to(REPO_ROOT)} must be removed"
        )

    def test_old_meta_yaml_absent(self):
        old_meta = OLD_FAI / "FAI-28-11-00-plan.meta.yaml"
        assert not old_meta.exists(), "Old meta.yaml must be removed"


# =========================================================================
# New Canonical Path Existence
# =========================================================================


class TestCanonicalPathExists:
    """FAI directory and meta file exist under canonical path."""

    def test_lc07_quality_directory(self):
        assert LC07.is_dir(), "LC07_QUALITY must exist"

    def test_acceptance_package(self):
        assert ACCEPTANCE.is_dir(), "ACCEPTANCE package must exist"

    def test_fai_directory(self):
        assert NEW_FAI.is_dir(), "WP-28-03-05/fai must exist under ACCEPTANCE"

    def test_meta_yaml_exists(self):
        meta = NEW_FAI / "FAI-28-11-00-plan.meta.yaml"
        assert meta.is_file(), "FAI meta.yaml must exist at canonical location"


# =========================================================================
# Meta YAML Content
# =========================================================================


class TestMetaYamlContent:
    """FAI meta.yaml must have correct content with updated paths."""

    @pytest.fixture()
    def meta(self):
        meta_path = NEW_FAI / "FAI-28-11-00-plan.meta.yaml"
        return yaml.safe_load(meta_path.read_text())

    def test_output_id(self, meta):
        assert meta["output_id"] == "fai_plan"

    def test_work_package(self, meta):
        assert meta["work_package"] == "WP-28-03-05"

    def test_lc_phase(self, meta):
        assert meta["lc_phase"] == "LC07_QUALITY"

    def test_ata(self, meta):
        assert meta["ata"] == "28-11-00"

    def test_domain(self, meta):
        assert meta["domain"] == "C2-CIRCULAR_CRYOGENIC_CELLS"

    def test_file_paths_use_canonical_prefix(self, meta):
        for entry in meta["files"]:
            assert entry["file"].startswith(NEW_REL), (
                f"File path must use canonical prefix: {entry['file']}"
            )

    def test_file_count(self, meta):
        assert len(meta["files"]) == 3

    @pytest.mark.parametrize(
        "file_id",
        ["FAI-28-11-00-plan", "FAI-28-11-00-checklist", "FAI-28-11-00-fair-template"],
    )
    def test_file_ids_present(self, meta, file_id):
        ids = [f["id"] for f in meta["files"]]
        assert file_id in ids

    def test_no_old_path_references(self, meta):
        raw = (NEW_FAI / "FAI-28-11-00-plan.meta.yaml").read_text()
        assert "LC07_INDUSTRIALIZATION" not in raw


# =========================================================================
# WBS References
# =========================================================================


class TestWBSReferences:
    """WBS_LEVEL_2.yaml must point to canonical FAI path."""

    @pytest.fixture()
    def wbs(self):
        wbs_path = ATA28 / "WBS" / "WBS_LEVEL_2.yaml"
        return yaml.safe_load(wbs_path.read_text())

    def _find_fai_output(self, wbs):
        for wp in wbs.get("work_packages", []):
            if wp.get("id") == "WP-28-03-05":
                for out in wp.get("outputs", []):
                    if out.get("id") == "fai_plan":
                        return out
        return None

    def test_fai_plan_output_exists(self, wbs):
        fai = self._find_fai_output(wbs)
        assert fai is not None, "fai_plan output must exist in WP-28-03-05"

    def test_fai_files_use_canonical_path(self, wbs):
        fai = self._find_fai_output(wbs)
        for f in fai["files"]:
            assert f.startswith("28-11-lh2-primary-tank/"), (
                f"WBS file path must use canonical prefix: {f}"
            )

    def test_fai_meta_file_uses_canonical_path(self, wbs):
        fai = self._find_fai_output(wbs)
        assert fai["meta_file"].startswith("28-11-lh2-primary-tank/"), (
            "WBS meta_file must use canonical prefix"
        )

    def test_no_old_wbs_references(self, wbs):
        raw = (ATA28 / "WBS" / "WBS_LEVEL_2.yaml").read_text()
        assert "LC07_INDUSTRIALIZATION" not in raw


# =========================================================================
# Script Compatibility
# =========================================================================


class TestExtractLcPhase:
    """generate_wbs_meta_files.py must extract LC phase from canonical paths."""

    def test_canonical_path_extraction(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "generate_wbs_meta_files",
            REPO_ROOT / "scripts" / "generate_wbs_meta_files.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        canonical = (
            "28-11-lh2-primary-tank/28-11-00-lh2-primary-tank-general"
            "/KDB/LM/SSOT/PLM/LC07_QUALITY/PACKAGES/ACCEPTANCE"
            "/WP-28-03-05/fai/FAI-28-11-00-plan.meta.yaml"
        )
        assert mod.extract_lc_phase_from_path(canonical) == "LC07_QUALITY"

    def test_flat_path_extraction_still_works(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "generate_wbs_meta_files",
            REPO_ROOT / "scripts" / "generate_wbs_meta_files.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        flat = "LC04_DESIGN_DEFINITION/ATA_28-11-00/WP-28-03-01/geometry/GEOM.meta.yaml"
        assert mod.extract_lc_phase_from_path(flat) == "LC04_DESIGN_DEFINITION"
