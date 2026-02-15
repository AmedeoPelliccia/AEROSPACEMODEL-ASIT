"""
Tests for Cryogenic Tank Cutaway Prototype in KDB/DEV/prototypes.

Validates:
- File and directory existence
- HTML structure and required content markers
- All eight tank layers referenced in the visualisation
- ATA 28-10-00 domain references
- README documentation
"""

from __future__ import annotations

from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
PROTO_DIR = (
    REPO_ROOT
    / "OPT-IN_FRAMEWORK"
    / "T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS"
    / "C2-CIRCULAR_CRYOGENIC_CELLS"
    / "ATA_28-FUEL"
    / "28-10-storage"
    / "28-10-00-fuel-storage-general"
    / "KDB"
    / "DEV"
    / "prototypes"
)


# =============================================================================
# Directory Structure Tests
# =============================================================================


class TestPrototypeStructure:
    """Tests that the prototypes directory has the required files."""

    def test_prototypes_directory_exists(self):
        assert PROTO_DIR.is_dir(), "KDB/DEV/prototypes/ must exist"

    def test_cryo_tank_html_exists(self):
        path = PROTO_DIR / "CRYO_TANK_CUTAWAY.html"
        assert path.exists(), "CRYO_TANK_CUTAWAY.html must exist"

    def test_readme_exists(self):
        path = PROTO_DIR / "README.md"
        assert path.exists(), "README.md must exist in prototypes/"


# =============================================================================
# HTML Structure Tests
# =============================================================================


class TestCryoTankHTML:
    """Tests for CRYO_TANK_CUTAWAY.html structure and content."""

    @pytest.fixture
    def html(self) -> str:
        path = PROTO_DIR / "CRYO_TANK_CUTAWAY.html"
        assert path.exists()
        return path.read_text(encoding="utf-8")

    def test_is_valid_html(self, html):
        assert "<!DOCTYPE html>" in html
        assert "<html" in html
        assert "</html>" in html

    def test_has_title(self, html):
        assert "<title>" in html
        assert "Cryogenic Tank" in html or "LH" in html

    def test_references_ata_28(self, html):
        assert "ATA 28" in html or "28-10" in html

    def test_references_three_js(self, html):
        assert "three" in html.lower()

    def test_references_react(self, html):
        assert "react" in html.lower()


# =============================================================================
# Tank Layer Content Tests
# =============================================================================


class TestTankLayers:
    """Each of the eight layers must be referenced in the visualisation."""

    @pytest.fixture
    def html(self) -> str:
        path = PROTO_DIR / "CRYO_TANK_CUTAWAY.html"
        return path.read_text(encoding="utf-8")

    LAYER_IDS = [
        "vessel",
        "lh2",
        "mli",
        "vacuum",
        "jacket",
        "cradle",
        "strut",
        "feedthrough",
    ]

    @pytest.mark.parametrize("layer_id", LAYER_IDS)
    def test_layer_registered(self, html, layer_id):
        assert f'"{layer_id}"' in html, (
            f"Layer '{layer_id}' must be registered in the mesh index"
        )

    def test_inner_pressure_vessel_label(self, html):
        assert "Inner Pressure Vessel" in html

    def test_lh2_label(self, html):
        assert "Liquid Hydrogen" in html

    def test_mli_label(self, html):
        assert "MLI Blanket" in html

    def test_vacuum_annulus_label(self, html):
        assert "Vacuum Annulus" in html

    def test_outer_jacket_label(self, html):
        assert "Outer Vacuum Jacket" in html

    def test_ring_cradle_label(self, html):
        assert "Ring Cradle" in html

    def test_bipod_struts_label(self, html):
        assert "Bipod Composite Struts" in html

    def test_feedthrough_label(self, html):
        assert "Feed-through" in html


# =============================================================================
# Technical Content Tests
# =============================================================================


class TestTechnicalContent:
    """Validate key engineering parameters are present."""

    @pytest.fixture
    def html(self) -> str:
        path = PROTO_DIR / "CRYO_TANK_CUTAWAY.html"
        return path.read_text(encoding="utf-8")

    def test_temperature_reference(self, html):
        assert "20 K" in html or "20.28 K" in html

    def test_pressure_reference(self, html):
        assert "3.5 bar" in html

    def test_mli_layer_count(self, html):
        assert "60 layers" in html

    def test_mli_total_constant(self, html):
        """The totalMLI constant must match the documented 60 layers."""
        assert "totalMLI = 60" in html

    def test_wall_thickness(self, html):
        assert "3 mm" in html

    def test_al_li_material(self, html):
        assert "Al-Li" in html

    def test_cfrp_material(self, html):
        assert "CFRP" in html

    def test_g10_cr_material(self, html):
        assert "G10-CR" in html

    def test_ptfe_material(self, html):
        assert "PTFE" in html


# =============================================================================
# README Tests
# =============================================================================


class TestPrototypeReadme:
    """Tests for prototypes README.md content."""

    @pytest.fixture
    def readme(self) -> str:
        path = PROTO_DIR / "README.md"
        return path.read_text(encoding="utf-8")

    def test_references_cryo_tank_file(self, readme):
        assert "CRYO_TANK_CUTAWAY.html" in readme

    def test_references_ata_28(self, readme):
        assert "28-10" in readme

    def test_references_c2_technology(self, readme):
        assert "C2" in readme

    def test_not_baselined_disclaimer(self, readme):
        assert "not baselined" in readme.lower()

    def test_lists_all_layers(self, readme):
        assert "Inner Pressure Vessel" in readme
        assert "Liquid Hydrogen" in readme
        assert "MLI" in readme
        assert "Vacuum Annulus" in readme
        assert "Outer Vacuum Jacket" in readme
        assert "Ring Cradle" in readme
        assert "Bipod Composite Struts" in readme
        assert "Feed-through" in readme
