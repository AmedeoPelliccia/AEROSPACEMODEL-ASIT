"""
Tests for ATA 28-11-00 Standard Token Procedures (STP) in KDB/DEV/mtl/.

Validates the STP YAML record that composes MTL subject tokens (MTK-*)
and process/scaling tokens (MTP-*) into single-token standard procedures.
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
STP_FILE = "STP-28-11-00_standard_procedures.yaml"


# =========================================================================
# Directory and Files
# =========================================================================


class TestSTPDirectory:
    """STP files must exist in the MTL directory."""

    def test_yaml_exists(self):
        assert (MTL_DIR / STP_FILE).exists()

    def test_markdown_companion_exists(self):
        md = STP_FILE.replace(".yaml", ".md")
        assert (MTL_DIR / md).exists()


# =========================================================================
# YAML Validity and Schema
# =========================================================================


class TestSTPSchema:
    """STP YAML must have required metadata and structure."""

    @pytest.fixture()
    def stp_data(self):
        with open(MTL_DIR / STP_FILE) as f:
            return yaml.safe_load(f)

    def test_yaml_parses(self, stp_data):
        assert stp_data is not None

    def test_has_stp_id(self, stp_data):
        assert stp_data.get("stp_id") == "STP-28-11-00"

    def test_has_ata_code(self, stp_data):
        assert stp_data.get("ata_code") == "28-11-00"

    def test_has_technology_domain(self, stp_data):
        assert stp_data.get("technology_domain") == "C2"

    def test_has_lifecycle_phase(self, stp_data):
        assert stp_data.get("lifecycle_phase") == "LC04"

    def test_has_token_pattern(self, stp_data):
        assert "STP-28-11" in stp_data.get("token_pattern", "")

    def test_has_procedures(self, stp_data):
        assert isinstance(stp_data.get("procedures"), list)
        assert len(stp_data["procedures"]) >= 1


# =========================================================================
# Procedure Structure
# =========================================================================


class TestSTPProcedures:
    """Each procedure must have required fields."""

    @pytest.fixture()
    def stp_data(self):
        with open(MTL_DIR / STP_FILE) as f:
            return yaml.safe_load(f)

    def test_all_have_token(self, stp_data):
        for proc in stp_data["procedures"]:
            assert proc["token"].startswith("STP-28-11-")

    def test_all_have_title(self, stp_data):
        for proc in stp_data["procedures"]:
            assert "title" in proc
            assert len(proc["title"]) > 0

    def test_all_have_procedure_class(self, stp_data):
        for proc in stp_data["procedures"]:
            assert "procedure_class" in proc

    def test_all_have_inputs(self, stp_data):
        for proc in stp_data["procedures"]:
            assert isinstance(proc.get("inputs"), list)
            assert len(proc["inputs"]) >= 1

    def test_all_have_steps(self, stp_data):
        for proc in stp_data["procedures"]:
            assert isinstance(proc.get("steps"), list)
            assert len(proc["steps"]) >= 1

    def test_all_have_outputs(self, stp_data):
        for proc in stp_data["procedures"]:
            assert isinstance(proc.get("outputs"), list)
            assert len(proc["outputs"]) >= 1

    def test_all_have_acceptance_gates(self, stp_data):
        for proc in stp_data["procedures"]:
            assert isinstance(proc.get("acceptance_gates"), list)
            assert len(proc["acceptance_gates"]) >= 1

    def test_all_have_tokens_consumed(self, stp_data):
        for proc in stp_data["procedures"]:
            assert isinstance(proc.get("tokens_consumed"), list)
            assert len(proc["tokens_consumed"]) >= 1

    def test_token_ids_unique(self, stp_data):
        ids = [p["token"] for p in stp_data["procedures"]]
        assert len(ids) == len(set(ids))


# =========================================================================
# Steps Structure
# =========================================================================


class TestSTPSteps:
    """Steps must have seq, token_ref (or action), and hand_off."""

    @pytest.fixture()
    def stp_data(self):
        with open(MTL_DIR / STP_FILE) as f:
            return yaml.safe_load(f)

    def test_steps_have_seq(self, stp_data):
        for proc in stp_data["procedures"]:
            for step in proc["steps"]:
                assert "seq" in step

    def test_steps_have_action(self, stp_data):
        for proc in stp_data["procedures"]:
            for step in proc["steps"]:
                assert "action" in step

    def test_steps_sequential(self, stp_data):
        for proc in stp_data["procedures"]:
            seqs = [s["seq"] for s in proc["steps"]]
            assert seqs == sorted(seqs)

    def test_token_refs_valid_prefix(self, stp_data):
        for proc in stp_data["procedures"]:
            for step in proc["steps"]:
                ref = step.get("token_ref")
                if ref is not None:
                    assert ref.startswith("MTP-28-11-") or ref.startswith("MTK-28-11-")


# =========================================================================
# Token Composition Integrity
# =========================================================================


class TestSTPComposition:
    """Tokens consumed must reference valid MTK/MTP tokens."""

    @pytest.fixture()
    def stp_data(self):
        with open(MTL_DIR / STP_FILE) as f:
            return yaml.safe_load(f)

    def test_consumed_tokens_all_valid_prefix(self, stp_data):
        for proc in stp_data["procedures"]:
            for tok in proc["tokens_consumed"]:
                assert tok.startswith("MTP-28-11-") or tok.startswith("MTK-28-11-")

    def test_step_token_refs_subset_of_consumed(self, stp_data):
        for proc in stp_data["procedures"]:
            consumed = set(proc["tokens_consumed"])
            for step in proc["steps"]:
                ref = step.get("token_ref")
                if ref is not None:
                    assert ref in consumed, f"{ref} in steps but not in tokens_consumed"


# =========================================================================
# Summary
# =========================================================================


class TestSTPSummary:
    """Summary section must match actual counts."""

    @pytest.fixture()
    def stp_data(self):
        with open(MTL_DIR / STP_FILE) as f:
            return yaml.safe_load(f)

    def test_has_summary(self, stp_data):
        assert "summary" in stp_data

    def test_total_procedures_matches(self, stp_data):
        assert stp_data["summary"]["total_procedures"] == len(stp_data["procedures"])

    def test_procedure_classes_match(self, stp_data):
        actual = {}
        for proc in stp_data["procedures"]:
            cls = proc["procedure_class"]
            actual[cls] = actual.get(cls, 0) + 1
        assert stp_data["summary"]["procedure_classes"] == actual


# =========================================================================
# Traceability
# =========================================================================


class TestSTPTraceability:
    """STP must trace to MTL source artifacts."""

    @pytest.fixture()
    def stp_data(self):
        with open(MTL_DIR / STP_FILE) as f:
            return yaml.safe_load(f)

    def test_has_traceability(self, stp_data):
        assert "traceability" in stp_data

    def test_derives_from_mtl(self, stp_data):
        derives = stp_data["traceability"]["derives_from"]
        assert "MTL-28-11-00" in derives
        assert "MTL-28-11-00-PROC" in derives

    def test_feeds_lifecycle(self, stp_data):
        feeds = stp_data["traceability"]["feeds"]
        assert isinstance(feeds, list)
        assert len(feeds) >= 1


# =========================================================================
# Artifact Catalog Registration
# =========================================================================


class TestArtifactCatalogSTP:
    """ARTIFACT_CATALOG.yaml must include standard_token_procedures."""

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

    def test_stp_registered(self, catalog_data):
        stp = catalog_data.get("artifact_types", {}).get("standard_token_procedures")
        assert stp is not None

    def test_stp_count(self, catalog_data):
        stp = catalog_data["artifact_types"]["standard_token_procedures"]
        assert stp["count"] == 1
