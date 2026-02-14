"""
Tests for OKNOT-002 cryo-fatigue KNU decomposition plan.

Validates the KNU_PLAN_OKNOT002.csv file and corresponding trace entries
for the C2-28-OKNOT-002 (Circular Cell Structural Fatigue Under Cryo Cycling)
graduation into 8 Knowledge Node Units spanning LC02–LC08 and PUB.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SUBJECT = (
    REPO_ROOT
    / "OPT-IN_FRAMEWORK"
    / "T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS"
    / "C2-CIRCULAR_CRYOGENIC_CELLS"
    / "ATA_28-FUEL"
    / "28-10-storage"
    / "28-10-00-fuel-storage-general"
)
PLM = SUBJECT / "KDB" / "LM" / "SSOT" / "PLM"
GENESIS = SUBJECT.parent / "GENESIS"


def _read_csv(path: Path) -> list[dict]:
    """Read a CSV file and return a list of row dicts."""
    assert path.exists(), f"CSV must exist: {path}"
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


# =========================================================================
# KNU Plan File Existence
# =========================================================================


class TestKNUPlanFile:
    """KNU_PLAN_OKNOT002.csv must exist and be well-formed."""

    KNU_PLAN = PLM / "LC01_PROBLEM_STATEMENT" / "KNU_PLAN_OKNOT002.csv"

    def test_file_exists(self):
        assert self.KNU_PLAN.exists()

    def test_is_valid_csv(self):
        rows = _read_csv(self.KNU_PLAN)
        assert len(rows) > 0

    def test_has_expected_columns(self):
        rows = _read_csv(self.KNU_PLAN)
        expected = {
            "KNU_ID", "KNOT_ID", "KNU_Type", "Artifact_Class",
            "Expected_Location", "Acceptance_Criteria", "Verification_Method",
            "Owner_AoR", "Due_Date", "Status", "Effort_Predicted", "Description",
        }
        assert expected == set(rows[0].keys())


# =========================================================================
# KNU Record Completeness
# =========================================================================


class TestKNURecords:
    """All 8 KNU items must be present with correct attributes."""

    @pytest.fixture
    def rows(self) -> list[dict]:
        return _read_csv(PLM / "LC01_PROBLEM_STATEMENT" / "KNU_PLAN_OKNOT002.csv")

    def test_total_count(self, rows):
        assert len(rows) == 8

    def test_all_reference_oknot002(self, rows):
        for r in rows:
            assert r["KNOT_ID"] == "C2-28-OKNOT-002"

    def test_all_status_planned(self, rows):
        for r in rows:
            assert r["Status"] == "PLANNED"

    @pytest.mark.parametrize(
        "knu_id",
        [
            "KNU-28-10-00-REQ-002",
            "KNU-28-10-00-ANA-002",
            "KNU-28-10-00-ANA-003",
            "KNU-28-10-00-SAF-002",
            "KNU-28-10-00-TEST-001",
            "KNU-28-10-00-TEST-002",
            "KNU-28-10-00-CM-001",
            "KNU-28-10-00-PUB-DM-002",
        ],
    )
    def test_knu_id_present(self, rows, knu_id):
        ids = [r["KNU_ID"] for r in rows]
        assert knu_id in ids

    @pytest.mark.parametrize(
        "knu_type,count",
        [("REQ", 1), ("ANA", 2), ("SAF", 1), ("TEST", 2), ("CM", 1), ("PUB", 1)],
    )
    def test_knu_type_distribution(self, rows, knu_type, count):
        actual = sum(1 for r in rows if r["KNU_Type"] == knu_type)
        assert actual == count

    def test_total_effort(self, rows):
        total = sum(int(r["Effort_Predicted"]) for r in rows)
        assert total == 68

    def test_artifact_classes(self, rows):
        classes = {r["Artifact_Class"] for r in rows}
        assert classes == {"SSOT", "CSDB"}

    def test_req_002_owner(self, rows):
        req = next(r for r in rows if r["KNU_ID"] == "KNU-28-10-00-REQ-002")
        assert req["Owner_AoR"] == "STK_ENG"

    def test_saf_002_owner(self, rows):
        saf = next(r for r in rows if r["KNU_ID"] == "KNU-28-10-00-SAF-002")
        assert saf["Owner_AoR"] == "STK_SAF"

    def test_test_001_owner(self, rows):
        test = next(r for r in rows if r["KNU_ID"] == "KNU-28-10-00-TEST-001")
        assert test["Owner_AoR"] == "STK_TEST"

    def test_cm_001_owner(self, rows):
        cm = next(r for r in rows if r["KNU_ID"] == "KNU-28-10-00-CM-001")
        assert cm["Owner_AoR"] == "STK_CM"

    def test_pub_dm_002_verification_method(self, rows):
        pub = next(r for r in rows if r["KNU_ID"] == "KNU-28-10-00-PUB-DM-002")
        assert pub["Verification_Method"] == "BREX+CI"

    def test_req_002_cs25_traceability(self, rows):
        req = next(r for r in rows if r["KNU_ID"] == "KNU-28-10-00-REQ-002")
        assert "CS-25.571" in req["Acceptance_Criteria"]


# =========================================================================
# Trace Files
# =========================================================================


class TestTraceLC01:
    """TRACE_LC01 must link OKNOT-002 to all 8 KNUs."""

    @pytest.fixture
    def rows(self) -> list[dict]:
        return _read_csv(PLM / "LC01_PROBLEM_STATEMENT" / "TRACE_LC01.csv")

    def test_oknot002_entries_count(self, rows):
        oknot002 = [r for r in rows if r["source_id"] == "C2-28-OKNOT-002"]
        assert len(oknot002) == 8

    def test_oknot002_relationship(self, rows):
        oknot002 = [r for r in rows if r["source_id"] == "C2-28-OKNOT-002"]
        for r in oknot002:
            assert r["relationship"] == "resolved_by"
            assert r["status"] == "active"


class TestTraceLC02:
    """LC02 trace must reference KNU-28-10-00-REQ-002."""

    @pytest.fixture
    def rows(self) -> list[dict]:
        return _read_csv(PLM / "LC02_SYSTEM_REQUIREMENTS" / "TRACE_LC02.csv")

    def test_req_002_in_trace(self, rows):
        ids = [r["source_id"] for r in rows]
        assert "KNU-28-10-00-REQ-002" in ids


class TestTraceLC03:
    """LC03 trace must reference KNU-28-10-00-SAF-002."""

    @pytest.fixture
    def rows(self) -> list[dict]:
        return _read_csv(PLM / "LC03_SAFETY_RELIABILITY" / "TRACE_LC03.csv")

    def test_saf_002_in_trace(self, rows):
        ids = [r["source_id"] for r in rows]
        assert "KNU-28-10-00-SAF-002" in ids


class TestTraceLC05:
    """LC05 trace must reference both ANA KNUs."""

    @pytest.fixture
    def rows(self) -> list[dict]:
        return _read_csv(PLM / "LC05_ANALYSIS_MODELS_CAE" / "TRACE_LC05.csv")

    def test_ana_002_in_trace(self, rows):
        ids = [r["source_id"] for r in rows]
        assert "KNU-28-10-00-ANA-002" in ids

    def test_ana_003_in_trace(self, rows):
        ids = [r["source_id"] for r in rows]
        assert "KNU-28-10-00-ANA-003" in ids


class TestTraceLC06:
    """LC06 trace must reference both TEST KNUs."""

    @pytest.fixture
    def rows(self) -> list[dict]:
        return _read_csv(PLM / "LC06_INTEGRATION_TEST_PMU" / "TRACE_LC06.csv")

    def test_test_001_in_trace(self, rows):
        ids = [r["source_id"] for r in rows]
        assert "KNU-28-10-00-TEST-001" in ids

    def test_test_002_in_trace(self, rows):
        ids = [r["source_id"] for r in rows]
        assert "KNU-28-10-00-TEST-002" in ids


class TestTraceLC08:
    """LC08 trace must reference KNU-28-10-00-CM-001."""

    @pytest.fixture
    def rows(self) -> list[dict]:
        return _read_csv(
            PLM / "LC08_FLIGHT_TEST_CERTIFICATION" / "TRACE_LC08.csv"
        )

    def test_cm_001_in_trace(self, rows):
        ids = [r["source_id"] for r in rows]
        assert "KNU-28-10-00-CM-001" in ids


# =========================================================================
# GENESIS Discovery Log
# =========================================================================


class TestDiscoveryLog:
    """DISCOVERY_LOG.md must record the OKNOT-002 graduation."""

    @pytest.fixture
    def text(self) -> str:
        path = GENESIS / "DISCOVERY_LOG.md"
        assert path.exists()
        return path.read_text(encoding="utf-8")

    def test_oknot002_graduation_section(self, text):
        assert "OKNOT-002 Graduated" in text

    def test_knu_count_mentioned(self, text):
        assert "KNU items created (8)" in text

    def test_total_effort_mentioned(self, text):
        assert "68 person-days" in text

    def test_plan_file_referenced(self, text):
        assert "KNU_PLAN_OKNOT002.csv" in text


# =========================================================================
# Subject Manifest Update
# =========================================================================


class TestSubjectManifest:
    """SUBJECT_MANIFEST.yaml must reflect new planned items."""

    @pytest.fixture
    def manifest(self) -> dict:
        path = SUBJECT / "SUBJECT_MANIFEST.yaml"
        assert path.exists()
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f)

    def test_requirements_count_updated(self, manifest):
        assert manifest["status_counts"]["requirements"] >= 16

    def test_tests_count_updated(self, manifest):
        assert manifest["status_counts"]["tests"] >= 2

    def test_publications_count_updated(self, manifest):
        assert manifest["status_counts"]["publications"] >= 1
