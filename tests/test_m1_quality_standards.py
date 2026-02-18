"""
Tests for M1 Manufacturing Facilities — 01_QUALITY/standards meta.yaml records.

Validates that all 6 standard records exist, are valid YAML, and comply with
the M1_standard_record.schema.json constraints for required fields.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
STANDARDS_DIR = (
    REPO_ROOT
    / "OPT-IN_FRAMEWORK"
    / "I-INFRASTRUCTURES"
    / "M1-MANUFACTURING_FACILITIES"
    / "01_QUALITY"
    / "standards"
)
SCHEMA_FILE = (
    REPO_ROOT
    / "OPT-IN_FRAMEWORK"
    / "I-INFRASTRUCTURES"
    / "M1-MANUFACTURING_FACILITIES"
    / "90_TEMPLATES_META"
    / "schemas"
    / "M1_standard_record.schema.json"
)

EXPECTED_STANDARDS = [
    "ISO_9001.meta.yaml",
    "AS9100.meta.yaml",
    "AS9120.meta.yaml",
    "NADCAP.meta.yaml",
    "AS9102.meta.yaml",
    "ISO_10007.meta.yaml",
]

EXPECTED_IDS = {
    "ISO_9001.meta.yaml": "M1-STD-ISO9001",
    "AS9100.meta.yaml": "M1-STD-AS9100",
    "AS9120.meta.yaml": "M1-STD-AS9120",
    "NADCAP.meta.yaml": "M1-STD-NADCAP",
    "AS9102.meta.yaml": "M1-STD-AS9102",
    "ISO_10007.meta.yaml": "M1-STD-ISO10007",
}


# =============================================================================
# Existence Tests
# =============================================================================


class TestStandardFilesExist:
    """All 6 standard record files must be present."""

    @pytest.mark.parametrize("filename", EXPECTED_STANDARDS)
    def test_standard_file_exists(self, filename: str):
        path = STANDARDS_DIR / filename
        assert path.exists(), f"Standard record file missing: {filename}"

    def test_no_extra_gitkeep_blocking(self):
        """standards/ directory must be accessible."""
        assert STANDARDS_DIR.is_dir(), "01_QUALITY/standards/ directory must exist"


# =============================================================================
# YAML Parse Tests
# =============================================================================


class TestStandardYAMLParseable:
    """All standard record files must be valid YAML."""

    @pytest.mark.parametrize("filename", EXPECTED_STANDARDS)
    def test_yaml_parseable(self, filename: str):
        path = STANDARDS_DIR / filename
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert isinstance(data, dict), f"{filename} must parse to a YAML mapping"


# =============================================================================
# Required Top-Level Fields
# =============================================================================


class TestStandardTopLevelFields:
    """Each file must have all required top-level fields per schema."""

    REQUIRED_FIELDS = ["id", "type", "title", "owner", "revision", "status", "lc_phase", "ata", "domain", "integrity"]

    @pytest.fixture(params=EXPECTED_STANDARDS)
    def record(self, request):
        path = STANDARDS_DIR / request.param
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    @pytest.mark.parametrize("field", REQUIRED_FIELDS)
    def test_required_field_present(self, record, field):
        assert field in record, f"Required field '{field}' missing from {record.get('id', '?')}"

    def test_id_starts_with_M1(self, record):
        assert record["id"].startswith("M1-"), f"id must start with 'M1-', got: {record['id']}"

    def test_type_is_standard_record(self, record):
        assert record["type"] == "STANDARD_RECORD"

    def test_ata_is_85_00_00(self, record):
        assert record["ata"] == "85-00-00"

    def test_domain_is_m1(self, record):
        assert record["domain"] == "I-INFRASTRUCTURES/M1"

    def test_status_valid(self, record):
        valid_statuses = {"draft", "review", "approved", "active", "obsolete"}
        assert record["status"] in valid_statuses

    def test_revision_semver(self, record):
        import re
        assert re.match(r"^\d+\.\d+\.\d+$", record["revision"]), (
            f"revision must be semver, got: {record['revision']}"
        )

    def test_lc_phase_pattern(self, record):
        import re
        assert re.match(r"^LC\d{2}", record["lc_phase"]), (
            f"lc_phase must match ^LC\\d{{2}}, got: {record['lc_phase']}"
        )

    def test_integrity_block(self, record):
        assert "integrity" in record
        assert "checksum" in record["integrity"]
        assert "algorithm" in record["integrity"]
        assert record["integrity"]["algorithm"] in {"sha256", "sha512", "md5"}


# =============================================================================
# Standard Sub-Object Fields
# =============================================================================


class TestStandardSubObject:
    """Each STANDARD_RECORD must have a populated 'standard' sub-object."""

    REQUIRED_STANDARD_FIELDS = [
        "id",
        "full_title",
        "issuing_body",
        "norm_type",
        "scope",
        "why_it_applies_to_M1",
        "evidence_expected",
        "audit_questions",
    ]

    @pytest.fixture(params=EXPECTED_STANDARDS)
    def standard(self, request):
        path = STANDARDS_DIR / request.param
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert "standard" in data, f"'standard' block missing from {request.param}"
        return data["standard"]

    @pytest.mark.parametrize("field", REQUIRED_STANDARD_FIELDS)
    def test_standard_field_present(self, standard, field):
        assert field in standard, f"standard.{field} missing"

    def test_norm_type_valid(self, standard):
        valid = {"system_management", "regulation", "technical_process", "control"}
        assert standard["norm_type"] in valid

    def test_evidence_expected_non_empty(self, standard):
        assert isinstance(standard["evidence_expected"], list)
        assert len(standard["evidence_expected"]) > 0

    def test_audit_questions_non_empty(self, standard):
        assert isinstance(standard["audit_questions"], list)
        assert len(standard["audit_questions"]) > 0


# =============================================================================
# Specific Standard IDs
# =============================================================================


class TestSpecificStandardIDs:
    """Each file must have the expected M1 identifier."""

    @pytest.mark.parametrize("filename,expected_id", EXPECTED_IDS.items())
    def test_standard_has_correct_id(self, filename: str, expected_id: str):
        path = STANDARDS_DIR / filename
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert data["id"] == expected_id, f"{filename}: expected id={expected_id}, got {data['id']}"


# =============================================================================
# Interface Fields
# =============================================================================


class TestStandardInterfaces:
    """Each standard must reference LC07 and 85-00-00."""

    @pytest.fixture(params=EXPECTED_STANDARDS)
    def standard(self, request):
        path = STANDARDS_DIR / request.param
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return data["standard"]

    def test_lc_phases_present(self, standard):
        assert "interfaces" in standard
        assert "lc_phases" in standard["interfaces"]
        assert len(standard["interfaces"]["lc_phases"]) > 0

    def test_lc07_referenced(self, standard):
        lc_phases = standard["interfaces"]["lc_phases"]
        assert any(lc.startswith("LC07") for lc in lc_phases), (
            "LC07_QA_PROCESS must be in lc_phases"
        )

    def test_ata_chapters_present(self, standard):
        assert "ata_chapters" in standard["interfaces"]
        assert "85-00-00" in standard["interfaces"]["ata_chapters"]

    def test_m1_domain_in_opt_in(self, standard):
        assert "opt_in_domains" in standard["interfaces"]
        assert "I-INFRASTRUCTURES/M1" in standard["interfaces"]["opt_in_domains"]
