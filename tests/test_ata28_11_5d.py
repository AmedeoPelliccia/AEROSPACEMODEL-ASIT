"""
Tests for ATA 28 5-dimensional token architecture layers D4 (SCR) and D5 (SDR).

Validates the two new upper layers that extend the 3-layer MTL
(MTK → MTP → STP) to a full 5D model:
  D5 — System Domain Resolution (SDR-28)
  D4 — Section / Component Resolution (SCR-28-*)
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
MTL_DIR = (
    REPO_ROOT
    / "OPT-IN_FRAMEWORK"
    / "T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS"
    / "C2-CIRCULAR_CRYOGENIC_CELLS"
    / "ATA_28-FUEL"
    / "28-11-lh2-primary-tank"
    / "28-11-00-lh2-primary-tank-general"
    / "KDB"
    / "DEV"
    / "mtl"
)
SCR_FILE = "SCR-28_section_resolver.yaml"
SDR_FILE = "SDR-28_system_domain.yaml"

ATA28_SECTIONS = [
    "28-00", "28-10", "28-11", "28-13",
    "28-21", "28-22", "28-23",
    "28-30", "28-31",
    "28-41", "28-42", "28-43",
]


# =========================================================================
# Directory and Files
# =========================================================================


class TestD4D5Directory:
    """SCR and SDR files must exist with markdown companions."""

    def test_scr_yaml_exists(self):
        assert (MTL_DIR / SCR_FILE).exists()

    def test_scr_markdown_exists(self):
        md = SCR_FILE.replace(".yaml", ".md")
        assert (MTL_DIR / md).exists()

    def test_sdr_yaml_exists(self):
        assert (MTL_DIR / SDR_FILE).exists()

    def test_sdr_markdown_exists(self):
        md = SDR_FILE.replace(".yaml", ".md")
        assert (MTL_DIR / md).exists()


# =========================================================================
# SCR Schema (Layer D4)
# =========================================================================


class TestSCRSchema:
    """SCR YAML must have required metadata and section list."""

    @pytest.fixture()
    def scr_data(self):
        with open(MTL_DIR / SCR_FILE) as f:
            return yaml.safe_load(f)

    def test_yaml_parses(self, scr_data):
        assert scr_data is not None

    def test_has_scr_id(self, scr_data):
        assert scr_data.get("scr_id") == "SCR-28"

    def test_has_ata_code(self, scr_data):
        assert scr_data.get("ata_code") == "28"

    def test_has_technology_domain(self, scr_data):
        assert scr_data.get("technology_domain") == "C2"

    def test_has_token_pattern(self, scr_data):
        assert "SCR-28" in scr_data.get("token_pattern", "")

    def test_has_sections(self, scr_data):
        assert isinstance(scr_data.get("sections"), list)
        assert len(scr_data["sections"]) >= 1


# =========================================================================
# SCR Sections
# =========================================================================


class TestSCRSections:
    """Each section token must have required fields."""

    @pytest.fixture()
    def scr_data(self):
        with open(MTL_DIR / SCR_FILE) as f:
            return yaml.safe_load(f)

    def test_all_have_token(self, scr_data):
        for s in scr_data["sections"]:
            assert s["token"].startswith("SCR-28-")

    def test_all_have_section_code(self, scr_data):
        for s in scr_data["sections"]:
            assert "section_code" in s

    def test_all_have_title(self, scr_data):
        for s in scr_data["sections"]:
            assert len(s.get("title", "")) > 0

    def test_all_have_available_stps(self, scr_data):
        for s in scr_data["sections"]:
            assert isinstance(s.get("available_stps"), list)

    def test_all_have_maturity(self, scr_data):
        for s in scr_data["sections"]:
            assert "maturity" in s

    def test_token_ids_unique(self, scr_data):
        ids = [s["token"] for s in scr_data["sections"]]
        assert len(ids) == len(set(ids))

    def test_covers_all_ata28_sections(self, scr_data):
        codes = {s["section_code"] for s in scr_data["sections"]}
        for expected in ATA28_SECTIONS:
            assert expected in codes, f"{expected} missing from SCR"

    def test_section_28_11_has_stps(self, scr_data):
        s11 = [s for s in scr_data["sections"] if s["section_code"] == "28-11"]
        assert len(s11) == 1
        assert len(s11[0]["available_stps"]) == 5

    def test_stps_reference_valid_prefix(self, scr_data):
        for s in scr_data["sections"]:
            for stp in s["available_stps"]:
                assert stp.startswith("STP-28-")


# =========================================================================
# SDR Schema (Layer D5)
# =========================================================================


class TestSDRSchema:
    """SDR YAML must have required metadata and system context."""

    @pytest.fixture()
    def sdr_data(self):
        with open(MTL_DIR / SDR_FILE) as f:
            return yaml.safe_load(f)

    def test_yaml_parses(self, sdr_data):
        assert sdr_data is not None

    def test_has_sdr_id(self, sdr_data):
        assert sdr_data.get("sdr_id") == "SDR-28"

    def test_has_ata_chapter(self, sdr_data):
        assert sdr_data.get("ata_chapter") == "28"

    def test_has_ata_title(self, sdr_data):
        assert sdr_data.get("ata_title") == "Fuel"

    def test_has_technology_domain(self, sdr_data):
        assert sdr_data.get("technology_domain") == "C2"

    def test_has_token_pattern(self, sdr_data):
        assert "SDR-" in sdr_data.get("token_pattern", "")

    def test_has_system_context(self, sdr_data):
        ctx = sdr_data.get("system_context")
        assert ctx is not None
        assert "mission" in ctx
        assert "scope" in ctx
        assert "regulatory_basis" in ctx
        assert "special_conditions" in ctx

    def test_has_available_sections(self, sdr_data):
        secs = sdr_data.get("available_sections")
        assert isinstance(secs, list)
        assert len(secs) == 12


# =========================================================================
# SDR 5D Architecture Map
# =========================================================================


class TestSDR5DArchitecture:
    """SDR must document the full 5D architecture."""

    @pytest.fixture()
    def sdr_data(self):
        with open(MTL_DIR / SDR_FILE) as f:
            return yaml.safe_load(f)

    def test_has_five_d_architecture(self, sdr_data):
        arch = sdr_data.get("five_d_architecture")
        assert arch is not None

    def test_all_five_dimensions_present(self, sdr_data):
        arch = sdr_data["five_d_architecture"]
        expected = [
            "D5_system_domain",
            "D4_section_component",
            "D3_standard_procedure",
            "D2_process_scaling",
            "D1_subject",
        ]
        for dim in expected:
            assert dim in arch, f"{dim} missing from 5D architecture"

    def test_each_dimension_has_prefix(self, sdr_data):
        arch = sdr_data["five_d_architecture"]
        expected_prefixes = {
            "D5_system_domain": "SDR-",
            "D4_section_component": "SCR-",
            "D3_standard_procedure": "STP-",
            "D2_process_scaling": "MTP-",
            "D1_subject": "MTK-",
        }
        for dim, prefix in expected_prefixes.items():
            assert arch[dim]["token_prefix"] == prefix


# =========================================================================
# SDR Available Sections match SCR tokens
# =========================================================================


class TestSDRSCRConsistency:
    """SDR available_sections must match SCR token list."""

    @pytest.fixture()
    def sdr_data(self):
        with open(MTL_DIR / SDR_FILE) as f:
            return yaml.safe_load(f)

    @pytest.fixture()
    def scr_data(self):
        with open(MTL_DIR / SCR_FILE) as f:
            return yaml.safe_load(f)

    def test_sdr_sections_match_scr_tokens(self, sdr_data, scr_data):
        sdr_sections = set(sdr_data["available_sections"])
        scr_tokens = {s["token"] for s in scr_data["sections"]}
        assert sdr_sections == scr_tokens

    def test_total_tokens_consistent(self, sdr_data):
        summary = sdr_data.get("summary", {})
        expected = (
            1   # SDR
            + summary.get("total_sections", 0)
            + summary.get("total_stps_reachable", 0)
            + summary.get("total_mtp_tokens_reachable", 0)
            + summary.get("total_mtk_tokens_reachable", 0)
        )
        assert summary.get("total_tokens_in_model") == expected


# =========================================================================
# SCR and SDR Summary
# =========================================================================


class TestSCRSummary:
    """SCR summary must match actual counts."""

    @pytest.fixture()
    def scr_data(self):
        with open(MTL_DIR / SCR_FILE) as f:
            return yaml.safe_load(f)

    def test_has_summary(self, scr_data):
        assert "summary" in scr_data

    def test_total_sections_matches(self, scr_data):
        assert scr_data["summary"]["total_sections"] == len(scr_data["sections"])

    def test_sections_with_stps_matches(self, scr_data):
        actual = sum(1 for s in scr_data["sections"] if s["available_stps"])
        assert scr_data["summary"]["sections_with_stps"] == actual


# =========================================================================
# Traceability
# =========================================================================


class TestD4D5Traceability:
    """Both layers must have traceability sections."""

    @pytest.fixture()
    def scr_data(self):
        with open(MTL_DIR / SCR_FILE) as f:
            return yaml.safe_load(f)

    @pytest.fixture()
    def sdr_data(self):
        with open(MTL_DIR / SDR_FILE) as f:
            return yaml.safe_load(f)

    def test_scr_has_traceability(self, scr_data):
        assert "traceability" in scr_data

    def test_scr_derives_from_sdr(self, scr_data):
        derives = scr_data["traceability"]["derives_from"]
        assert "SDR-28" in derives

    def test_sdr_has_traceability(self, sdr_data):
        assert "traceability" in sdr_data

    def test_sdr_feeds_d4(self, sdr_data):
        feeds = sdr_data["traceability"]["feeds"]
        layers = [f["layer"] for f in feeds]
        assert "D4" in layers


# =========================================================================
# Artifact Catalog Registration
# =========================================================================


class TestArtifactCatalog5D:
    """ARTIFACT_CATALOG.yaml must include SCR and SDR entries."""

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

    def test_scr_registered(self, catalog_data):
        scr = catalog_data.get("artifact_types", {}).get("section_component_resolvers")
        assert scr is not None

    def test_scr_count(self, catalog_data):
        scr = catalog_data["artifact_types"]["section_component_resolvers"]
        assert scr["count"] == 1

    def test_sdr_registered(self, catalog_data):
        sdr = catalog_data.get("artifact_types", {}).get("system_domain_resolvers")
        assert sdr is not None

    def test_sdr_count(self, catalog_data):
        sdr = catalog_data["artifact_types"]["system_domain_resolvers"]
        assert sdr["count"] == 1
