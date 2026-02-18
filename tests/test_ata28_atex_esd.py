"""
Tests for ATEX, ESD, and Future-Proofing sections for H₂/fuel cell infrastructure.

Validates that the following new safety artifacts exist at canonical paths:

  ATA 28-41 (H₂ Leak Detection):
    LC03_SAFETY_RELIABILITY/PACKAGES/HAZARD_MGMT/
        ATX-28-41-00-atex-esd-zone-classification.md
        ATX-28-41-00-atex-esd-zone-classification.meta.yaml

  ATA 28-00 (Fuel — General):
    LC03_SAFETY_RELIABILITY/PACKAGES/HAZARD_MGMT/
        ESD-28-00-00-bonding-grounding.md
        ESD-28-00-00-bonding-grounding.meta.yaml
    LC03_SAFETY_RELIABILITY/PACKAGES/SAFETY/
        FUT-28-00-00-future-standards.md
        FUT-28-00-00-future-standards.meta.yaml

  ATA 71 (Power Plant / Fuel Cell):
    P-PROPULSION/ATA_71-POWER_PLANT/README.md

Also validates:
  - WBS_LEVEL_2.yaml includes WP-28-07-01/02/03 entries
  - SECTION_INDEX.yaml for 28-41 reflects updated metrics
  - README.md for ATA 28-FUEL includes ATEX/ESD special conditions
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest
import yaml

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent

ATA28 = (
    REPO_ROOT
    / "OPT-IN_FRAMEWORK"
    / "T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS"
    / "C2-CIRCULAR_CRYOGENIC_CELLS"
    / "ATA_28-FUEL"
)

ATA28_41_HAZARD = (
    ATA28
    / "28-41-h2-leak-detection"
    / "28-41-00-h2-leak-detection-general"
    / "KDB" / "LM" / "SSOT" / "PLM"
    / "LC03_SAFETY_RELIABILITY"
    / "PACKAGES" / "HAZARD_MGMT"
)

ATA28_00_HAZARD = (
    ATA28
    / "28-00-general"
    / "28-00-00-general-general"
    / "KDB" / "LM" / "SSOT" / "PLM"
    / "LC03_SAFETY_RELIABILITY"
    / "PACKAGES" / "HAZARD_MGMT"
)

ATA28_00_SAFETY = (
    ATA28
    / "28-00-general"
    / "28-00-00-general-general"
    / "KDB" / "LM" / "SSOT" / "PLM"
    / "LC03_SAFETY_RELIABILITY"
    / "PACKAGES" / "SAFETY"
)

ATA71 = (
    REPO_ROOT
    / "OPT-IN_FRAMEWORK"
    / "T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS"
    / "P-PROPULSION"
    / "ATA_71-POWER_PLANT"
)


# ===========================================================================
# ATEX / ESD zone classification artifacts (28-41)
# ===========================================================================
class TestAtexZoneClassificationExists:
    """ATEX/ESD zone classification document must exist under 28-41 HAZARD_MGMT."""

    def test_atex_md_exists(self):
        path = ATA28_41_HAZARD / "ATX-28-41-00-atex-esd-zone-classification.md"
        assert path.exists(), f"Missing: {path.relative_to(REPO_ROOT)}"

    def test_atex_meta_yaml_exists(self):
        path = ATA28_41_HAZARD / "ATX-28-41-00-atex-esd-zone-classification.meta.yaml"
        assert path.exists(), f"Missing: {path.relative_to(REPO_ROOT)}"

    def test_atex_md_not_empty(self):
        path = ATA28_41_HAZARD / "ATX-28-41-00-atex-esd-zone-classification.md"
        assert path.stat().st_size > 0

    def test_atex_meta_is_valid_yaml(self):
        path = ATA28_41_HAZARD / "ATX-28-41-00-atex-esd-zone-classification.meta.yaml"
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data is not None


class TestAtexZoneClassificationContent:
    """ATEX zone classification document must cover required safety topics."""

    @pytest.fixture
    def atex_md(self):
        path = ATA28_41_HAZARD / "ATX-28-41-00-atex-esd-zone-classification.md"
        return path.read_text(encoding="utf-8")

    @pytest.fixture
    def atex_meta(self):
        path = ATA28_41_HAZARD / "ATX-28-41-00-atex-esd-zone-classification.meta.yaml"
        with open(path) as f:
            return yaml.safe_load(f)

    def test_atex_md_has_zone_classification_header(self, atex_md):
        assert "Zone Classification" in atex_md or "zone classification" in atex_md.lower()

    def test_atex_md_references_iec_60079(self, atex_md):
        assert "IEC 60079" in atex_md

    def test_atex_md_covers_zone0(self, atex_md):
        assert "Zone 0" in atex_md

    def test_atex_md_covers_zone1(self, atex_md):
        assert "Zone 1" in atex_md

    def test_atex_md_covers_zone2(self, atex_md):
        assert "Zone 2" in atex_md

    def test_atex_md_references_esd(self, atex_md):
        assert "ESD" in atex_md or "electrostatic" in atex_md.lower()

    def test_atex_md_references_iic_gas_group(self, atex_md):
        assert "IIC" in atex_md

    def test_atex_md_has_future_proofing_section(self, atex_md):
        assert "Future" in atex_md or "future" in atex_md.lower()

    def test_atex_md_references_atex_directive(self, atex_md):
        assert "ATEX" in atex_md

    def test_atex_meta_work_package(self, atex_meta):
        assert atex_meta["work_package"] == "WP-28-07-01"

    def test_atex_meta_lc_phase(self, atex_meta):
        assert atex_meta["lc_phase"] == "LC03_SAFETY_RELIABILITY"

    def test_atex_meta_ata(self, atex_meta):
        assert atex_meta["ata"] == "28-41-00"

    def test_atex_meta_domain(self, atex_meta):
        assert atex_meta["domain"] == "C2-CIRCULAR_CRYOGENIC_CELLS"

    def test_atex_meta_has_atex_tag(self, atex_meta):
        assert "atex" in atex_meta.get("tags", [])

    def test_atex_meta_files_reference_canonical_path(self, atex_meta):
        for entry in atex_meta.get("files", []):
            assert "28-41-h2-leak-detection" in entry["file"]


# ===========================================================================
# ESD bonding & grounding document (28-00)
# ===========================================================================
class TestEsdBondingGroundingExists:
    """ESD bonding and grounding document must exist under 28-00 HAZARD_MGMT."""

    def test_esd_md_exists(self):
        path = ATA28_00_HAZARD / "ESD-28-00-00-bonding-grounding.md"
        assert path.exists(), f"Missing: {path.relative_to(REPO_ROOT)}"

    def test_esd_meta_yaml_exists(self):
        path = ATA28_00_HAZARD / "ESD-28-00-00-bonding-grounding.meta.yaml"
        assert path.exists(), f"Missing: {path.relative_to(REPO_ROOT)}"

    def test_esd_md_not_empty(self):
        path = ATA28_00_HAZARD / "ESD-28-00-00-bonding-grounding.md"
        assert path.stat().st_size > 0

    def test_esd_meta_is_valid_yaml(self):
        path = ATA28_00_HAZARD / "ESD-28-00-00-bonding-grounding.meta.yaml"
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data is not None


class TestEsdBondingGroundingContent:
    """ESD bonding document must cover all required safety topics."""

    @pytest.fixture
    def esd_md(self):
        path = ATA28_00_HAZARD / "ESD-28-00-00-bonding-grounding.md"
        return path.read_text(encoding="utf-8")

    @pytest.fixture
    def esd_meta(self):
        path = ATA28_00_HAZARD / "ESD-28-00-00-bonding-grounding.meta.yaml"
        with open(path) as f:
            return yaml.safe_load(f)

    def test_esd_md_has_bonding_header(self, esd_md):
        assert "Bonding" in esd_md or "bonding" in esd_md.lower()

    def test_esd_md_references_arp1489(self, esd_md):
        assert "ARP 1489" in esd_md or "ARP1489" in esd_md

    def test_esd_md_references_mie(self, esd_md):
        assert "MIE" in esd_md or "minimum ignition energy" in esd_md.lower()

    def test_esd_md_has_composite_airframe_section(self, esd_md):
        assert "composite" in esd_md.lower() or "CFRP" in esd_md

    def test_esd_md_has_bonding_resistance_values(self, esd_md):
        assert "1 Ω" in esd_md or "1 Ohm" in esd_md or "≤ 1" in esd_md

    def test_esd_md_covers_ground_handling(self, esd_md):
        assert "Ground" in esd_md or "ground handling" in esd_md.lower()

    def test_esd_meta_work_package(self, esd_meta):
        assert esd_meta["work_package"] == "WP-28-07-02"

    def test_esd_meta_lc_phase(self, esd_meta):
        assert esd_meta["lc_phase"] == "LC03_SAFETY_RELIABILITY"

    def test_esd_meta_ata(self, esd_meta):
        assert esd_meta["ata"] == "28-00-00"

    def test_esd_meta_domain(self, esd_meta):
        assert esd_meta["domain"] == "C2-CIRCULAR_CRYOGENIC_CELLS"

    def test_esd_meta_has_esd_tag(self, esd_meta):
        assert "esd" in esd_meta.get("tags", [])

    def test_esd_meta_files_reference_canonical_path(self, esd_meta):
        for entry in esd_meta.get("files", []):
            assert "28-00-general" in entry["file"]


# ===========================================================================
# Future standards watch document (28-00)
# ===========================================================================
class TestFutureStandardsWatchExists:
    """Future standards watch document must exist under 28-00 SAFETY."""

    def test_fut_md_exists(self):
        path = ATA28_00_SAFETY / "FUT-28-00-00-future-standards.md"
        assert path.exists(), f"Missing: {path.relative_to(REPO_ROOT)}"

    def test_fut_meta_yaml_exists(self):
        path = ATA28_00_SAFETY / "FUT-28-00-00-future-standards.meta.yaml"
        assert path.exists(), f"Missing: {path.relative_to(REPO_ROOT)}"

    def test_fut_md_not_empty(self):
        path = ATA28_00_SAFETY / "FUT-28-00-00-future-standards.md"
        assert path.stat().st_size > 0

    def test_fut_meta_is_valid_yaml(self):
        path = ATA28_00_SAFETY / "FUT-28-00-00-future-standards.meta.yaml"
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data is not None


class TestFutureStandardsWatchContent:
    """Future standards watch must cover ATEX, ESD, and fuel cell standards."""

    @pytest.fixture
    def fut_md(self):
        path = ATA28_00_SAFETY / "FUT-28-00-00-future-standards.md"
        return path.read_text(encoding="utf-8")

    @pytest.fixture
    def fut_meta(self):
        path = ATA28_00_SAFETY / "FUT-28-00-00-future-standards.meta.yaml"
        with open(path) as f:
            return yaml.safe_load(f)

    def test_fut_md_covers_atex_standards(self, fut_md):
        assert "IEC 60079" in fut_md or "ATEX" in fut_md

    def test_fut_md_covers_esd_standards(self, fut_md):
        assert "ARP 1489" in fut_md or "ARP1489" in fut_md or "ESD" in fut_md

    def test_fut_md_covers_fuel_cell_standards(self, fut_md):
        assert "IEC 62282" in fut_md or "fuel cell" in fut_md.lower()

    def test_fut_md_has_action_register(self, fut_md):
        assert "Action" in fut_md or "FUT-001" in fut_md

    def test_fut_md_covers_h2_iso_standards(self, fut_md):
        assert "ISO" in fut_md

    def test_fut_meta_work_package(self, fut_meta):
        assert fut_meta["work_package"] == "WP-28-07-03"

    def test_fut_meta_lc_phase(self, fut_meta):
        assert fut_meta["lc_phase"] == "LC03_SAFETY_RELIABILITY"

    def test_fut_meta_ata(self, fut_meta):
        assert fut_meta["ata"] == "28-00-00"

    def test_fut_meta_has_future_proofing_tag(self, fut_meta):
        assert "future_proofing" in fut_meta.get("tags", [])


# ===========================================================================
# ATA 71 Fuel Cell Power Plant README
# ===========================================================================
class TestAta71FuelCellReadmeExists:
    """ATA 71 README must exist with ATEX/ESD content."""

    def test_ata71_readme_exists(self):
        path = ATA71 / "README.md"
        assert path.exists(), f"Missing: {path.relative_to(REPO_ROOT)}"

    def test_ata71_readme_not_empty(self):
        path = ATA71 / "README.md"
        assert path.stat().st_size > 0


class TestAta71FuelCellReadmeContent:
    """ATA 71 README must reference ATEX/ESD requirements."""

    @pytest.fixture
    def ata71_readme(self):
        path = ATA71 / "README.md"
        return path.read_text(encoding="utf-8")

    def test_ata71_readme_has_atex_section(self, ata71_readme):
        assert "ATEX" in ata71_readme

    def test_ata71_readme_has_esd_section(self, ata71_readme):
        assert "ESD" in ata71_readme

    def test_ata71_readme_references_fuel_cell(self, ata71_readme):
        assert "fuel cell" in ata71_readme.lower() or "Fuel Cell" in ata71_readme

    def test_ata71_readme_has_iic_t1_requirement(self, ata71_readme):
        assert "IIC T1" in ata71_readme

    def test_ata71_readme_has_future_proofing_section(self, ata71_readme):
        assert "Future" in ata71_readme or "future" in ata71_readme.lower()

    def test_ata71_readme_cross_references_atx_28_41(self, ata71_readme):
        assert "ATX-28-41" in ata71_readme

    def test_ata71_readme_cross_references_esd_28_00(self, ata71_readme):
        assert "ESD-28-00" in ata71_readme


# ===========================================================================
# WBS validation
# ===========================================================================
class TestWbsAtexEsdEntries:
    """WBS_LEVEL_2.yaml must include WP-28-07-01, WP-28-07-02, WP-28-07-03."""

    @pytest.fixture
    def wbs(self):
        path = ATA28 / "WBS" / "WBS_LEVEL_2.yaml"
        with open(path) as f:
            return yaml.safe_load(f)

    @pytest.fixture
    def wbs_text(self):
        path = ATA28 / "WBS" / "WBS_LEVEL_2.yaml"
        return path.read_text(encoding="utf-8")

    def _find_wp(self, wbs, wp_id):
        for item in wbs.get("work_packages", []):
            if item.get("id") == wp_id:
                return item
        return None

    @pytest.mark.parametrize("wp_id", ["WP-28-07-01", "WP-28-07-02", "WP-28-07-03"])
    def test_wp_exists(self, wbs, wp_id):
        wp = self._find_wp(wbs, wp_id)
        assert wp is not None, f"Work package {wp_id} not found in WBS"

    def test_wp_28_07_01_output_file_canonical(self, wbs):
        wp = self._find_wp(wbs, "WP-28-07-01")
        assert wp is not None
        output = next(o for o in wp["outputs"] if o["id"] == "atex_esd_zone_classification")
        for f in output["files"]:
            assert "28-41-h2-leak-detection" in f

    def test_wp_28_07_02_output_file_canonical(self, wbs):
        wp = self._find_wp(wbs, "WP-28-07-02")
        assert wp is not None
        output = next(o for o in wp["outputs"] if o["id"] == "esd_bonding_grounding")
        for f in output["files"]:
            assert "28-00-general" in f

    def test_wp_28_07_03_output_file_canonical(self, wbs):
        wp = self._find_wp(wbs, "WP-28-07-03")
        assert wp is not None
        output = next(o for o in wp["outputs"] if o["id"] == "future_standards_watch")
        for f in output["files"]:
            assert "28-00-general" in f

    @pytest.mark.parametrize("wp_id", ["WP-28-07-01", "WP-28-07-02", "WP-28-07-03"])
    def test_wp_has_atex_or_esd_tag(self, wbs, wp_id):
        wp = self._find_wp(wbs, wp_id)
        assert wp is not None
        tags = wp.get("tags", [])
        has_relevant_tag = any(
            t in tags for t in ["atex", "esd", "future_proofing", "hydrogen_safety"]
        )
        assert has_relevant_tag, f"{wp_id} must have an ATEX/ESD/future-proofing tag"

    def test_wbs_is_valid_yaml(self, wbs_text):
        data = yaml.safe_load(wbs_text)
        assert data is not None


# ===========================================================================
# SECTION_INDEX update
# ===========================================================================
class TestSectionIndexUpdatedForAtex:
    """SECTION_INDEX.yaml for 28-41 must reflect the two new HAZARD_MGMT artifacts."""

    @pytest.fixture
    def section_index(self):
        path = ATA28 / "28-41-h2-leak-detection" / "SECTION_INDEX.yaml"
        with open(path) as f:
            return yaml.safe_load(f)

    def test_safety_count_is_at_least_5(self, section_index):
        assert section_index["metrics"]["safety_count"] >= 5, (
            "safety_count must be ≥ 5 after adding ATEX/ESD artifacts"
        )

    def test_total_artifacts_is_at_least_5(self, section_index):
        assert section_index["metrics"]["total_artifacts"] >= 5, (
            "total_artifacts must be ≥ 5 after adding ATEX/ESD artifacts"
        )


# ===========================================================================
# ATA 28 README special conditions
# ===========================================================================
class TestAta28ReadmeAtexEsdConditions:
    """ATA 28 README must reference ATEX and ESD special conditions."""

    @pytest.fixture
    def ata28_readme(self):
        path = ATA28 / "README.md"
        return path.read_text(encoding="utf-8")

    def test_readme_has_atex_special_condition(self, ata28_readme):
        assert "ATEX" in ata28_readme

    def test_readme_has_esd_special_condition(self, ata28_readme):
        assert "ESD" in ata28_readme

    def test_readme_references_atx_document(self, ata28_readme):
        assert "ATX-28-41-00" in ata28_readme

    def test_readme_references_esd_document(self, ata28_readme):
        assert "ESD-28-00-00" in ata28_readme

    def test_readme_has_atex_in_standards(self, ata28_readme):
        assert "ATEX 2014/34/EU" in ata28_readme or "ATEX" in ata28_readme

    def test_readme_has_arp1489_in_standards(self, ata28_readme):
        assert "ARP 1489" in ata28_readme or "ARP1489" in ata28_readme
