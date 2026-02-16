"""
Tests for ATA 28-11-00 Method Token Library (MTL) in KDB/DEV/mtl/.

Validates the MTL YAML record created during LC04 design definition
for the C2 Circular Cryogenic Cells LH2 primary tank.
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
MTL_FILE = "MTL-28-11-00_method_token_library.yaml"


# =========================================================================
# Directory and Files
# =========================================================================


class TestMTLDirectory:
    """MTL directory must contain the expected files."""

    def test_directory_exists(self):
        assert MTL_DIR.is_dir()

    def test_readme_exists(self):
        assert (MTL_DIR / "README.md").exists()

    def test_yaml_exists(self):
        assert (MTL_DIR / MTL_FILE).exists()

    def test_markdown_companion_exists(self):
        md = MTL_FILE.replace(".yaml", ".md")
        assert (MTL_DIR / md).exists()


# =========================================================================
# YAML Validity and Schema
# =========================================================================


class TestMTLSchema:
    """MTL YAML must have required metadata and structure."""

    @pytest.fixture()
    def mtl_data(self):
        with open(MTL_DIR / MTL_FILE) as f:
            return yaml.safe_load(f)

    def test_yaml_parses(self, mtl_data):
        assert mtl_data is not None

    def test_has_mtl_id(self, mtl_data):
        assert mtl_data.get("mtl_id") == "MTL-28-11-00"

    def test_has_ata_code(self, mtl_data):
        assert mtl_data.get("ata_code") == "28-11-00"

    def test_has_technology_domain(self, mtl_data):
        assert mtl_data.get("technology_domain") == "C2"

    def test_has_lifecycle_phase(self, mtl_data):
        assert mtl_data.get("lifecycle_phase") == "LC04"

    def test_has_token_pattern(self, mtl_data):
        assert "MTK-28-11" in mtl_data.get("token_pattern", "")


# =========================================================================
# Domains and Tokens
# =========================================================================


class TestMTLDomains:
    """MTL must contain the expected domains with valid tokens."""

    @pytest.fixture()
    def mtl_data(self):
        with open(MTL_DIR / MTL_FILE) as f:
            return yaml.safe_load(f)

    def test_has_domains(self, mtl_data):
        domains = mtl_data.get("domains")
        assert isinstance(domains, list)
        assert len(domains) >= 2

    def test_domain_ids(self, mtl_data):
        ids = {d["domain_id"] for d in mtl_data["domains"]}
        assert {"TS", "CM", "SC", "EC"} <= ids

    def test_all_tokens_have_token_id(self, mtl_data):
        for domain in mtl_data["domains"]:
            for token in domain["tokens"]:
                assert "token" in token
                assert token["token"].startswith("MTK-28-11-")

    def test_all_tokens_have_subject(self, mtl_data):
        for domain in mtl_data["domains"]:
            for token in domain["tokens"]:
                assert "subject" in token

    def test_all_tokens_have_method_class(self, mtl_data):
        for domain in mtl_data["domains"]:
            for token in domain["tokens"]:
                assert "method_class" in token

    def test_token_ids_unique(self, mtl_data):
        all_ids = []
        for domain in mtl_data["domains"]:
            for token in domain["tokens"]:
                all_ids.append(token["token"])
        assert len(all_ids) == len(set(all_ids))


# =========================================================================
# Token Count and Summary
# =========================================================================


class TestMTLSummary:
    """Summary section must match actual token counts."""

    @pytest.fixture()
    def mtl_data(self):
        with open(MTL_DIR / MTL_FILE) as f:
            return yaml.safe_load(f)

    def test_has_summary(self, mtl_data):
        assert "summary" in mtl_data

    def test_total_tokens_matches(self, mtl_data):
        actual = sum(
            len(d["tokens"]) for d in mtl_data["domains"]
        )
        assert mtl_data["summary"]["total_tokens"] == actual

    def test_domain_counts_match(self, mtl_data):
        for domain in mtl_data["domains"]:
            did = domain["domain_id"]
            expected = mtl_data["summary"]["domain_counts"][did]
            assert len(domain["tokens"]) == expected


# =========================================================================
# Traceability
# =========================================================================


class TestMTLTraceability:
    """MTL must have traceability to source artifacts."""

    @pytest.fixture()
    def mtl_data(self):
        with open(MTL_DIR / MTL_FILE) as f:
            return yaml.safe_load(f)

    def test_has_traceability(self, mtl_data):
        assert "traceability" in mtl_data

    def test_derives_from_trade_studies(self, mtl_data):
        derives = mtl_data["traceability"]["derives_from"]
        assert "TS-28-11-TS01" in derives
        assert "CM-28-11-CS25" in derives

    def test_feeds_lifecycle(self, mtl_data):
        feeds = mtl_data["traceability"]["feeds"]
        assert isinstance(feeds, list)
        assert len(feeds) >= 1


# =========================================================================
# Artifact Catalog Registration
# =========================================================================


class TestArtifactCatalogMTL:
    """ARTIFACT_CATALOG.yaml must include method_token_libraries entry."""

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

    def test_mtl_registered(self, catalog_data):
        mtl = catalog_data.get("artifact_types", {}).get("method_token_libraries")
        assert mtl is not None

    def test_mtl_count(self, catalog_data):
        mtl = catalog_data["artifact_types"]["method_token_libraries"]
        assert mtl["count"] == 2


# =========================================================================
# Process/Scaling MTL — Directory and Schema
# =========================================================================

PROC_FILE = "MTL-28-11-00_process_methods.yaml"


class TestProcessMTLDirectory:
    """Process MTL files must exist."""

    def test_yaml_exists(self):
        assert (MTL_DIR / PROC_FILE).exists()

    def test_markdown_companion_exists(self):
        md = PROC_FILE.replace(".yaml", ".md")
        assert (MTL_DIR / md).exists()


class TestProcessMTLSchema:
    """Process MTL YAML must have required metadata and structure."""

    @pytest.fixture()
    def proc_data(self):
        with open(MTL_DIR / PROC_FILE) as f:
            return yaml.safe_load(f)

    def test_yaml_parses(self, proc_data):
        assert proc_data is not None

    def test_has_mtl_id(self, proc_data):
        assert proc_data.get("mtl_id") == "MTL-28-11-00-PROC"

    def test_has_ata_code(self, proc_data):
        assert proc_data.get("ata_code") == "28-11-00"

    def test_has_token_pattern(self, proc_data):
        assert "MTP-28-11" in proc_data.get("token_pattern", "")


class TestProcessMTLDomains:
    """Process MTL must contain the expected domains."""

    @pytest.fixture()
    def proc_data(self):
        with open(MTL_DIR / PROC_FILE) as f:
            return yaml.safe_load(f)

    def test_domain_ids(self, proc_data):
        ids = {d["domain_id"] for d in proc_data["domains"]}
        assert {"GEOM", "THRM", "MATL", "CERT", "EVAL"} <= ids

    def test_all_tokens_have_type(self, proc_data):
        for domain in proc_data["domains"]:
            for token in domain["tokens"]:
                assert token.get("type") in ("process", "scaling")

    def test_all_tokens_have_method(self, proc_data):
        for domain in proc_data["domains"]:
            for token in domain["tokens"]:
                assert "method" in token

    def test_all_tokens_have_inputs_outputs(self, proc_data):
        for domain in proc_data["domains"]:
            for token in domain["tokens"]:
                assert "inputs" in token
                assert "outputs" in token

    def test_token_ids_unique(self, proc_data):
        all_ids = [
            t["token"] for d in proc_data["domains"] for t in d["tokens"]
        ]
        assert len(all_ids) == len(set(all_ids))

    def test_token_ids_start_with_mtp(self, proc_data):
        for domain in proc_data["domains"]:
            for token in domain["tokens"]:
                assert token["token"].startswith("MTP-28-11-")


class TestProcessMTLSummary:
    """Summary section must match actual counts."""

    @pytest.fixture()
    def proc_data(self):
        with open(MTL_DIR / PROC_FILE) as f:
            return yaml.safe_load(f)

    def test_total_tokens_matches(self, proc_data):
        actual = sum(len(d["tokens"]) for d in proc_data["domains"])
        assert proc_data["summary"]["total_tokens"] == actual

    def test_domain_counts_match(self, proc_data):
        for domain in proc_data["domains"]:
            did = domain["domain_id"]
            expected = proc_data["summary"]["domain_counts"][did]
            assert len(domain["tokens"]) == expected

    def test_type_counts_match(self, proc_data):
        actual_process = sum(
            1
            for d in proc_data["domains"]
            for t in d["tokens"]
            if t["type"] == "process"
        )
        actual_scaling = sum(
            1
            for d in proc_data["domains"]
            for t in d["tokens"]
            if t["type"] == "scaling"
        )
        assert proc_data["summary"]["type_counts"]["process"] == actual_process
        assert proc_data["summary"]["type_counts"]["scaling"] == actual_scaling


class TestProcessMTLTraceability:
    """Process MTL must trace to source artifacts."""

    @pytest.fixture()
    def proc_data(self):
        with open(MTL_DIR / PROC_FILE) as f:
            return yaml.safe_load(f)

    def test_has_traceability(self, proc_data):
        assert "traceability" in proc_data

    def test_derives_from_includes_subject_mtl(self, proc_data):
        derives = proc_data["traceability"]["derives_from"]
        assert "MTL-28-11-00" in derives
