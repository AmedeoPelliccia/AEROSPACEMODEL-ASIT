"""
Tests for ECR-ATA28-11-CS25-SSOT-001 and SSOT promotion.

Validates the Engineering Change Request document, promoted SSOT copy
of the CS-25 compliance matrix, ECR register entry, and baseline
register entry for ATA 28-11-00 LH₂ Primary Tank.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
BASE_28_11 = (
    REPO_ROOT
    / "OPT-IN_FRAMEWORK"
    / "T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS"
    / "C2-CIRCULAR_CRYOGENIC_CELLS"
    / "ATA_28-FUEL"
    / "28-11-lh2-primary-tank"
    / "28-11-00-lh2-primary-tank-general"
)
ECR_DIR = BASE_28_11 / "GOVERNANCE" / "CHANGE_CONTROL" / "ECR"
SSOT_DIR = BASE_28_11 / "KDB" / "LM" / "SSOT"
DEV_DIR = BASE_28_11 / "KDB" / "DEV" / "trade-studies"
ECR_REGISTER = (
    REPO_ROOT
    / "OPT-IN_FRAMEWORK"
    / "T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS"
    / "C2-CIRCULAR_CRYOGENIC_CELLS"
    / "ATA_28-FUEL"
    / "GOVERNANCE"
    / "CHANGE_CONTROL"
    / "ECR"
    / "ECR_REGISTER.csv"
)
BASELINE_REGISTER = BASE_28_11 / "GOVERNANCE" / "BASELINE_REGISTER.csv"


# =========================================================================
# ECR Document Existence and Content
# =========================================================================


class TestECRDocument:
    """ECR-ATA28-11-CS25-SSOT-001.md must exist with required sections."""

    ECR_PATH = ECR_DIR / "ECR-ATA28-11-CS25-SSOT-001.md"

    def test_ecr_exists(self):
        assert self.ECR_PATH.exists()

    @pytest.fixture()
    def ecr_text(self):
        return self.ECR_PATH.read_text(encoding="utf-8")

    def test_ecr_has_header_section(self, ecr_text):
        assert "## Header" in ecr_text

    def test_ecr_has_ecr_id(self, ecr_text):
        assert "ECR-ATA28-11-CS25-SSOT-001" in ecr_text

    def test_ecr_has_description(self, ecr_text):
        assert "## Description of Change" in ecr_text

    def test_ecr_has_rationale(self, ecr_text):
        assert "## Rationale" in ecr_text

    def test_ecr_has_safety_impact(self, ecr_text):
        assert "## Safety Impact" in ecr_text

    def test_ecr_safety_flagged_yes(self, ecr_text):
        assert "[x] Yes" in ecr_text

    def test_ecr_has_affected_baselines(self, ecr_text):
        assert "## Affected Baselines" in ecr_text

    def test_ecr_has_impact_assessment(self, ecr_text):
        assert "## Impact Assessment" in ecr_text

    def test_ecr_has_approval_status(self, ecr_text):
        assert "## Approval Status" in ecr_text

    def test_ecr_references_source_artifact(self, ecr_text):
        assert "CS25_compliance_matrix.yaml" in ecr_text

    def test_ecr_references_ssot(self, ecr_text):
        assert "KDB/LM/SSOT/" in ecr_text

    def test_ecr_references_trade_studies(self, ecr_text):
        for ts_id in ["TS-28-11-TS01", "TS-28-11-TS02", "TS-28-11-TS03"]:
            assert ts_id in ecr_text, f"Missing trade study reference: {ts_id}"

    def test_ecr_references_mtl_tokens(self, ecr_text):
        assert "MTK-28-11-CM-" in ecr_text or "MTP-" in ecr_text or "STP-" in ecr_text


# =========================================================================
# SSOT Promoted Copy
# =========================================================================


class TestSSOTPromotedCopy:
    """KDB/LM/SSOT/ must contain the promoted compliance matrix."""

    def test_ssot_yaml_exists(self):
        assert (SSOT_DIR / "CS25_compliance_matrix.yaml").exists()

    def test_ssot_md_exists(self):
        assert (SSOT_DIR / "CS25_compliance_matrix.md").exists()

    @pytest.fixture()
    def ssot_data(self):
        with open(SSOT_DIR / "CS25_compliance_matrix.yaml") as f:
            return yaml.safe_load(f)

    @pytest.fixture()
    def dev_data(self):
        with open(DEV_DIR / "CS25_compliance_matrix.yaml") as f:
            return yaml.safe_load(f)

    def test_ssot_status_is_promoted(self, ssot_data):
        assert ssot_data["status"] == "promoted"

    def test_ssot_matrix_id_matches_dev(self, ssot_data, dev_data):
        assert ssot_data["matrix_id"] == dev_data["matrix_id"]

    def test_ssot_sections_match_dev(self, ssot_data, dev_data):
        ssot_sections = {s["id"] for s in ssot_data["sections"]}
        dev_sections = {s["id"] for s in dev_data["sections"]}
        assert ssot_sections == dev_sections

    def test_ssot_special_conditions_match_dev(self, ssot_data, dev_data):
        ssot_scs = {sc["sc_id"] for sc in ssot_data["special_conditions"]}
        dev_scs = {sc["sc_id"] for sc in dev_data["special_conditions"]}
        assert ssot_scs == dev_scs

    def test_ssot_evidence_package_matches_dev(self, ssot_data, dev_data):
        assert set(ssot_data["evidence_package"]) == set(dev_data["evidence_package"])

    def test_ssot_yaml_has_ecr_comment(self):
        text = (SSOT_DIR / "CS25_compliance_matrix.yaml").read_text(encoding="utf-8")
        assert "ECR-ATA28-11-CS25-SSOT-001" in text

    def test_ssot_yaml_has_promoted_header(self):
        text = (SSOT_DIR / "CS25_compliance_matrix.yaml").read_text(encoding="utf-8")
        assert "SSOT PROMOTED COPY" in text


# =========================================================================
# ECR Register
# =========================================================================


class TestECRRegister:
    """ATA 28 ECR register must contain the new entry."""

    @pytest.fixture()
    def register_rows(self):
        with open(ECR_REGISTER, newline="") as f:
            return list(csv.DictReader(f))

    def test_register_has_entry(self, register_rows):
        ids = [r["ecr_id"] for r in register_rows]
        assert "ECR-ATA28-11-CS25-SSOT-001" in ids

    def test_register_entry_ata_section(self, register_rows):
        entry = next(r for r in register_rows if r["ecr_id"] == "ECR-ATA28-11-CS25-SSOT-001")
        assert entry["ata_section"] == "28-11-00"

    def test_register_entry_safety_impact(self, register_rows):
        entry = next(r for r in register_rows if r["ecr_id"] == "ECR-ATA28-11-CS25-SSOT-001")
        assert entry["safety_impact"] == "yes"

    def test_register_entry_status(self, register_rows):
        entry = next(r for r in register_rows if r["ecr_id"] == "ECR-ATA28-11-CS25-SSOT-001")
        assert entry["status"] == "open"


# =========================================================================
# Baseline Register
# =========================================================================


class TestBaselineRegister:
    """28-11-00 baseline register must reflect the new FBL entry."""

    @pytest.fixture()
    def baseline_rows(self):
        with open(BASELINE_REGISTER, newline="") as f:
            return list(csv.DictReader(f))

    def test_baseline_has_entry(self, baseline_rows):
        ids = [r["baseline_id"] for r in baseline_rows]
        assert "BL-28-11-CS25-001" in ids

    def test_baseline_type_is_fbl(self, baseline_rows):
        entry = next(r for r in baseline_rows if r["baseline_id"] == "BL-28-11-CS25-001")
        assert entry["type"] == "FBL"

    def test_baseline_status_pending(self, baseline_rows):
        entry = next(r for r in baseline_rows if r["baseline_id"] == "BL-28-11-CS25-001")
        assert entry["status"] == "pending"
