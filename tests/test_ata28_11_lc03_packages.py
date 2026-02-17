"""
Tests for LC03 Safety & Reliability Packages (ATA 28-11).

Validates directory structure, YAML schema integrity, traceability,
and governance controls for the LC03 SSOT packages at:
  .../KDB/LM/SSOT/PLM/LC03_SAFETY_RELIABILITY/PACKAGES/
    - SAFETY
    - HAZARD_MGMT
    - RELIABILITY
"""

from __future__ import annotations

import csv
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
LC03_DIR = (
    REPO_ROOT
    / "OPT-IN_FRAMEWORK"
    / "T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS"
    / "C2-CIRCULAR_CRYOGENIC_CELLS"
    / "ATA_28-FUEL"
    / "28-11-lh2-primary-tank"
    / "28-11-00-lh2-primary-tank-general"
    / "KDB"
    / "LM"
    / "SSOT"
    / "PLM"
    / "LC03_SAFETY_RELIABILITY"
)

PACKAGES_DIR = LC03_DIR / "PACKAGES"
SAFETY_DIR = PACKAGES_DIR / "SAFETY"
HAZARD_DIR = PACKAGES_DIR / "HAZARD_MGMT"
RELIABILITY_DIR = PACKAGES_DIR / "RELIABILITY"

# ── Required files per package ────────────────────────────────────────────

SAFETY_FILES = [
    "SAFETY_PACKAGE.yaml",
    "SAFETY_ASSESSMENT_PLAN.md",
]

HAZARD_FILES = [
    "HAZARD_REGISTER.yaml",
]

RELIABILITY_FILES = [
    "RELIABILITY_PACKAGE.yaml",
]

ROOT_FILES = [
    "README.md",
    "TRACE_LC03.csv",
]


# ── Directory structure tests ─────────────────────────────────────────────

def test_lc03_root_directory_exists():
    """Verify LC03 root directory exists."""
    assert LC03_DIR.exists(), f"LC03 root directory not found: {LC03_DIR}"
    assert LC03_DIR.is_dir(), f"LC03 root path is not a directory: {LC03_DIR}"


def test_packages_directory_exists():
    """Verify PACKAGES directory exists."""
    assert PACKAGES_DIR.exists(), f"PACKAGES directory not found: {PACKAGES_DIR}"
    assert PACKAGES_DIR.is_dir(), f"PACKAGES path is not a directory: {PACKAGES_DIR}"


def test_safety_directory_exists():
    """Verify SAFETY package directory exists and is populated."""
    assert SAFETY_DIR.exists(), f"SAFETY directory not found: {SAFETY_DIR}"
    assert SAFETY_DIR.is_dir(), f"SAFETY path is not a directory: {SAFETY_DIR}"
    # Ensure no .gitkeep files remain
    assert not (SAFETY_DIR / ".gitkeep").exists(), "SAFETY directory still contains .gitkeep"


def test_hazard_mgmt_directory_exists():
    """Verify HAZARD_MGMT package directory exists and is populated."""
    assert HAZARD_DIR.exists(), f"HAZARD_MGMT directory not found: {HAZARD_DIR}"
    assert HAZARD_DIR.is_dir(), f"HAZARD_MGMT path is not a directory: {HAZARD_DIR}"
    # Ensure no .gitkeep files remain
    assert not (HAZARD_DIR / ".gitkeep").exists(), "HAZARD_MGMT directory still contains .gitkeep"


def test_reliability_directory_exists():
    """Verify RELIABILITY package directory exists and is populated."""
    assert RELIABILITY_DIR.exists(), f"RELIABILITY directory not found: {RELIABILITY_DIR}"
    assert RELIABILITY_DIR.is_dir(), f"RELIABILITY path is not a directory: {RELIABILITY_DIR}"
    # Ensure no .gitkeep files remain
    assert not (RELIABILITY_DIR / ".gitkeep").exists(), "RELIABILITY directory still contains .gitkeep"


# ── File existence tests ──────────────────────────────────────────────────

@pytest.mark.parametrize("filename", SAFETY_FILES)
def test_safety_file_exists(filename):
    """Verify all required SAFETY package files exist."""
    file_path = SAFETY_DIR / filename
    assert file_path.exists(), f"SAFETY file not found: {file_path}"
    assert file_path.is_file(), f"SAFETY path is not a file: {file_path}"


@pytest.mark.parametrize("filename", HAZARD_FILES)
def test_hazard_file_exists(filename):
    """Verify all required HAZARD_MGMT package files exist."""
    file_path = HAZARD_DIR / filename
    assert file_path.exists(), f"HAZARD_MGMT file not found: {file_path}"
    assert file_path.is_file(), f"HAZARD_MGMT path is not a file: {file_path}"


@pytest.mark.parametrize("filename", RELIABILITY_FILES)
def test_reliability_file_exists(filename):
    """Verify all required RELIABILITY package files exist."""
    file_path = RELIABILITY_DIR / filename
    assert file_path.exists(), f"RELIABILITY file not found: {file_path}"
    assert file_path.is_file(), f"RELIABILITY path is not a file: {file_path}"


@pytest.mark.parametrize("filename", ROOT_FILES)
def test_root_file_exists(filename):
    """Verify all required root-level files exist."""
    file_path = LC03_DIR / filename
    assert file_path.exists(), f"Root file not found: {file_path}"
    assert file_path.is_file(), f"Root path is not a file: {file_path}"


# ── YAML parsing tests ────────────────────────────────────────────────────

def test_safety_package_yaml_valid():
    """Verify SAFETY_PACKAGE.yaml is valid YAML."""
    file_path = SAFETY_DIR / "SAFETY_PACKAGE.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert data is not None, "SAFETY_PACKAGE.yaml is empty or invalid"
    assert "safety_package" in data, "SAFETY_PACKAGE.yaml missing 'safety_package' key"


def test_hazard_register_yaml_valid():
    """Verify HAZARD_REGISTER.yaml is valid YAML."""
    file_path = HAZARD_DIR / "HAZARD_REGISTER.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert data is not None, "HAZARD_REGISTER.yaml is empty or invalid"
    assert "hazard_register" in data, "HAZARD_REGISTER.yaml missing 'hazard_register' key"


def test_reliability_package_yaml_valid():
    """Verify RELIABILITY_PACKAGE.yaml is valid YAML."""
    file_path = RELIABILITY_DIR / "RELIABILITY_PACKAGE.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert data is not None, "RELIABILITY_PACKAGE.yaml is empty or invalid"
    assert "reliability_package" in data, "RELIABILITY_PACKAGE.yaml missing 'reliability_package' key"


# ── Safety Package schema tests ───────────────────────────────────────────

def test_safety_package_required_fields():
    """Verify SAFETY_PACKAGE.yaml has all required fields."""
    file_path = SAFETY_DIR / "SAFETY_PACKAGE.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    pkg = data["safety_package"]
    required_fields = [
        "package_id", "package_title", "program", "domain", "lifecycle_phase",
        "ata_scope", "status", "baseline_state", "version", "owner_role",
        "governance_authority", "created_on", "last_updated_on"
    ]
    
    for field in required_fields:
        assert field in pkg, f"SAFETY_PACKAGE.yaml missing required field: {field}"


def test_safety_package_status_is_dev():
    """Verify SAFETY_PACKAGE.yaml status is 'DEV'."""
    file_path = SAFETY_DIR / "SAFETY_PACKAGE.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    assert data["safety_package"]["status"] == "DEV", "SAFETY_PACKAGE.yaml status must be 'DEV'"


def test_safety_package_has_methodology():
    """Verify SAFETY_PACKAGE.yaml includes ARP4761 methodology."""
    file_path = SAFETY_DIR / "SAFETY_PACKAGE.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    assert "methodology" in data["safety_package"], "SAFETY_PACKAGE.yaml missing 'methodology'"
    methodology = data["safety_package"]["methodology"]
    assert methodology["standard"] == "ARP4761", "SAFETY_PACKAGE.yaml methodology must be 'ARP4761'"
    assert "phases" in methodology, "SAFETY_PACKAGE.yaml missing methodology phases"
    
    phase_ids = [phase["id"] for phase in methodology["phases"]]
    assert "FHA" in phase_ids, "SAFETY_PACKAGE.yaml missing FHA phase"
    assert "PSSA" in phase_ids, "SAFETY_PACKAGE.yaml missing PSSA phase"
    assert "SSA" in phase_ids, "SAFETY_PACKAGE.yaml missing SSA phase"


def test_safety_package_has_regulatory_basis():
    """Verify SAFETY_PACKAGE.yaml includes regulatory basis."""
    file_path = SAFETY_DIR / "SAFETY_PACKAGE.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    assert "regulatory_basis" in data["safety_package"], "SAFETY_PACKAGE.yaml missing 'regulatory_basis'"
    reg = data["safety_package"]["regulatory_basis"]
    assert reg["primary"] == "EASA CS-25", "SAFETY_PACKAGE.yaml primary regulation must be 'EASA CS-25'"
    assert "special_conditions" in reg, "SAFETY_PACKAGE.yaml missing special_conditions"


def test_safety_package_has_special_conditions():
    """Verify SAFETY_PACKAGE.yaml includes all 5 LH2 special conditions."""
    file_path = SAFETY_DIR / "SAFETY_PACKAGE.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    scs = data["safety_package"]["regulatory_basis"]["special_conditions"]
    expected_scs = ["SC-LH2-01", "SC-LH2-02", "SC-LH2-03", "SC-LH2-04", "SC-LH2-05"]
    
    for sc in expected_scs:
        found = any(sc in condition for condition in scs)
        assert found, f"SAFETY_PACKAGE.yaml missing special condition: {sc}"


def test_safety_package_inherits_governance():
    """Verify SAFETY_PACKAGE.yaml inherits safety precedence from LC01."""
    file_path = SAFETY_DIR / "SAFETY_PACKAGE.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    assert "safety_precedence" in data["safety_package"], "SAFETY_PACKAGE.yaml missing 'safety_precedence'"
    precedence = data["safety_package"]["safety_precedence"]
    assert "inherits" in precedence, "SAFETY_PACKAGE.yaml missing inheritance reference"
    assert "GOV-LC01-ATA28-11" in precedence["inherits"], "SAFETY_PACKAGE.yaml must inherit from GOV-LC01-ATA28-11"


def test_safety_package_has_escalation_policy():
    """Verify SAFETY_PACKAGE.yaml includes SAFETY-H2-001 escalation policy."""
    file_path = SAFETY_DIR / "SAFETY_PACKAGE.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    assert "escalation_policy" in data["safety_package"], "SAFETY_PACKAGE.yaml missing 'escalation_policy'"
    esc = data["safety_package"]["escalation_policy"]
    assert esc["safety_content_generation"] == "SAFETY-H2-001", "SAFETY_PACKAGE.yaml must reference SAFETY-H2-001"
    assert esc["human_authorizer_required"] is True, "SAFETY_PACKAGE.yaml must require human authorizer"


# ── Hazard Register schema tests ──────────────────────────────────────────

def test_hazard_register_required_fields():
    """Verify HAZARD_REGISTER.yaml has all required fields."""
    file_path = HAZARD_DIR / "HAZARD_REGISTER.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    reg = data["hazard_register"]
    required_fields = [
        "register_id", "ata_scope", "program", "version", "status", "date", "owner"
    ]
    
    for field in required_fields:
        assert field in reg, f"HAZARD_REGISTER.yaml missing required field: {field}"


def test_hazard_register_status_is_dev():
    """Verify HAZARD_REGISTER.yaml status is 'DEV'."""
    file_path = HAZARD_DIR / "HAZARD_REGISTER.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    assert data["hazard_register"]["status"] == "DEV", "HAZARD_REGISTER.yaml status must be 'DEV'"


def test_hazard_register_has_hazards():
    """Verify HAZARD_REGISTER.yaml includes hazards list."""
    file_path = HAZARD_DIR / "HAZARD_REGISTER.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    assert "hazards" in data["hazard_register"], "HAZARD_REGISTER.yaml missing 'hazards'"
    hazards = data["hazard_register"]["hazards"]
    assert len(hazards) == 6, f"HAZARD_REGISTER.yaml must have 6 hazards, found {len(hazards)}"


def test_hazard_register_hazard_ids():
    """Verify HAZARD_REGISTER.yaml has correct hazard IDs (HAZ-28-11-001 through 006)."""
    file_path = HAZARD_DIR / "HAZARD_REGISTER.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    expected_ids = [f"HAZ-28-11-{i:03d}" for i in range(1, 7)]
    actual_ids = [hazard["id"] for hazard in data["hazard_register"]["hazards"]]
    
    for expected_id in expected_ids:
        assert expected_id in actual_ids, f"HAZARD_REGISTER.yaml missing hazard: {expected_id}"


@pytest.mark.parametrize("hazard_id", [f"HAZ-28-11-{i:03d}" for i in range(1, 7)])
def test_hazard_has_required_fields(hazard_id):
    """Verify each hazard has all required fields."""
    file_path = HAZARD_DIR / "HAZARD_REGISTER.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    hazards = {h["id"]: h for h in data["hazard_register"]["hazards"]}
    assert hazard_id in hazards, f"Hazard not found: {hazard_id}"
    
    hazard = hazards[hazard_id]
    required_fields = ["id", "function", "failure_condition", "classification", "rate_target", "mitigation", "trace_to"]
    
    for field in required_fields:
        assert field in hazard, f"Hazard {hazard_id} missing required field: {field}"


def test_hazard_classifications():
    """Verify hazard classifications match the Safety Assessment Plan."""
    file_path = HAZARD_DIR / "HAZARD_REGISTER.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    expected_classifications = {
        "HAZ-28-11-001": "Catastrophic",
        "HAZ-28-11-002": "Catastrophic",
        "HAZ-28-11-003": "Hazardous",
        "HAZ-28-11-004": "Major",
        "HAZ-28-11-005": "Catastrophic",
        "HAZ-28-11-006": "Hazardous",
    }
    
    hazards = {h["id"]: h for h in data["hazard_register"]["hazards"]}
    
    for hazard_id, expected_class in expected_classifications.items():
        assert hazards[hazard_id]["classification"] == expected_class, \
            f"Hazard {hazard_id} has incorrect classification"


def test_hazard_register_has_methodology():
    """Verify HAZARD_REGISTER.yaml includes methodology section."""
    file_path = HAZARD_DIR / "HAZARD_REGISTER.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    assert "methodology" in data["hazard_register"], "HAZARD_REGISTER.yaml missing 'methodology'"
    methodology = data["hazard_register"]["methodology"]
    assert methodology["standard"] == "ARP4761", "HAZARD_REGISTER.yaml methodology must be 'ARP4761'"
    assert "severity_scale" in methodology, "HAZARD_REGISTER.yaml missing severity_scale"
    assert "rate_basis" in methodology, "HAZARD_REGISTER.yaml missing rate_basis"


def test_hazard_register_has_approval_gate():
    """Verify HAZARD_REGISTER.yaml includes approval gate section."""
    file_path = HAZARD_DIR / "HAZARD_REGISTER.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    assert "approval_gate" in data["hazard_register"], "HAZARD_REGISTER.yaml missing 'approval_gate'"
    gate = data["hazard_register"]["approval_gate"]
    assert gate["reviewer"] == "STK_SAF", "HAZARD_REGISTER.yaml reviewer must be 'STK_SAF'"
    assert gate["authority"] == "CCB", "HAZARD_REGISTER.yaml authority must be 'CCB'"
    assert gate["status"] == "Pending", "HAZARD_REGISTER.yaml approval status must be 'Pending'"


@pytest.mark.parametrize("hazard_id", [f"HAZ-28-11-{i:03d}" for i in range(1, 7)])
def test_hazard_has_enhanced_fields(hazard_id):
    """Verify each hazard has enhanced schema fields (title, causes, effects, etc.)."""
    file_path = HAZARD_DIR / "HAZARD_REGISTER.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    hazards = {h["id"]: h for h in data["hazard_register"]["hazards"]}
    assert hazard_id in hazards, f"Hazard not found: {hazard_id}"
    
    hazard = hazards[hazard_id]
    enhanced_fields = ["title", "phase_applicability", "causes", "effects", "detection_controls", "verification", "residual_risk"]
    
    for field in enhanced_fields:
        assert field in hazard, f"Hazard {hazard_id} missing enhanced field: {field}"


def test_hazard_004_has_saf_003_trace():
    """Verify HAZ-28-11-004 includes SAF-28-11-003 in safety traces."""
    file_path = HAZARD_DIR / "HAZARD_REGISTER.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    hazards = {h["id"]: h for h in data["hazard_register"]["hazards"]}
    haz_004 = hazards["HAZ-28-11-004"]
    
    assert "safety" in haz_004["trace_to"], "HAZ-28-11-004 missing safety traces"
    safety_traces = haz_004["trace_to"]["safety"]
    assert "SAF-28-11-003" in safety_traces, "HAZ-28-11-004 must include SAF-28-11-003 in safety traces"
    assert "SAF-28-11-005" in safety_traces, "HAZ-28-11-004 must include SAF-28-11-005 in safety traces"


# ── Reliability Package schema tests ──────────────────────────────────────

def test_reliability_package_required_fields():
    """Verify RELIABILITY_PACKAGE.yaml has all required fields."""
    file_path = RELIABILITY_DIR / "RELIABILITY_PACKAGE.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    pkg = data["reliability_package"]
    required_fields = [
        "package_id", "package_title", "program", "ata_scope", "status", "version", "date", "owner"
    ]
    
    for field in required_fields:
        assert field in pkg, f"RELIABILITY_PACKAGE.yaml missing required field: {field}"


def test_reliability_package_status_is_dev():
    """Verify RELIABILITY_PACKAGE.yaml status is 'DEV'."""
    file_path = RELIABILITY_DIR / "RELIABILITY_PACKAGE.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    assert data["reliability_package"]["status"] == "DEV", "RELIABILITY_PACKAGE.yaml status must be 'DEV'"


def test_reliability_package_has_critical_items():
    """Verify RELIABILITY_PACKAGE.yaml includes critical items list."""
    file_path = RELIABILITY_DIR / "RELIABILITY_PACKAGE.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    assert "critical_items" in data["reliability_package"], "RELIABILITY_PACKAGE.yaml missing 'critical_items'"
    items = data["reliability_package"]["critical_items"]
    assert len(items) == 6, f"RELIABILITY_PACKAGE.yaml must have 6 critical items, found {len(items)}"


def test_reliability_critical_items_have_required_fields():
    """Verify each critical item has required fields."""
    file_path = RELIABILITY_DIR / "RELIABILITY_PACKAGE.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    items = data["reliability_package"]["critical_items"]
    required_fields = ["item", "key_parameters", "source"]
    
    for item in items:
        for field in required_fields:
            assert field in item, f"Critical item '{item.get('item', 'unknown')}' missing field: {field}"


# ── Traceability CSV tests ────────────────────────────────────────────────

def test_trace_csv_exists_and_readable():
    """Verify TRACE_LC03.csv exists and is readable."""
    file_path = LC03_DIR / "TRACE_LC03.csv"
    assert file_path.exists(), f"TRACE_LC03.csv not found: {file_path}"
    
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    assert len(rows) > 0, "TRACE_LC03.csv is empty"


def test_trace_csv_has_required_columns():
    """Verify TRACE_LC03.csv has required columns."""
    file_path = LC03_DIR / "TRACE_LC03.csv"
    
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames
    
    required_columns = ["source_id", "target_id", "relationship", "direction", "status"]
    for col in required_columns:
        assert col in columns, f"TRACE_LC03.csv missing required column: {col}"


def test_trace_csv_has_31_rows():
    """Verify TRACE_LC03.csv has exactly 31 traceability rows."""
    file_path = LC03_DIR / "TRACE_LC03.csv"
    
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    assert len(rows) == 31, f"TRACE_LC03.csv must have 31 rows, found {len(rows)}"


def test_trace_csv_all_hazards_traced():
    """Verify all 6 hazards (HAZ-28-11-001 through 006) are traced."""
    file_path = LC03_DIR / "TRACE_LC03.csv"
    
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    source_ids = {row["source_id"] for row in rows}
    expected_hazards = [f"HAZ-28-11-{i:03d}" for i in range(1, 7)]
    
    for hazard_id in expected_hazards:
        assert hazard_id in source_ids, f"TRACE_LC03.csv missing traceability for: {hazard_id}"


def test_trace_csv_all_safety_hazards_traced():
    """Verify all 8 safety hazards (SAF-28-11-001 through 008) are traced."""
    file_path = LC03_DIR / "TRACE_LC03.csv"
    
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    source_ids = {row["source_id"] for row in rows}
    expected_safety = [f"SAF-28-11-{i:03d}" for i in range(1, 9)]
    
    for safety_id in expected_safety:
        assert safety_id in source_ids, f"TRACE_LC03.csv missing traceability for: {safety_id}"


def test_trace_csv_all_risks_traced():
    """Verify all open risks (RISK-01, RISK-02, RISK-03, RISK-05) are traced."""
    file_path = LC03_DIR / "TRACE_LC03.csv"
    
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    source_ids = {row["source_id"] for row in rows}
    expected_risks = ["RISK-01", "RISK-02", "RISK-03", "RISK-05"]
    
    for risk_id in expected_risks:
        assert risk_id in source_ids, f"TRACE_LC03.csv missing traceability for: {risk_id}"


def test_trace_csv_relationships():
    """Verify TRACE_LC03.csv uses correct relationship types."""
    file_path = LC03_DIR / "TRACE_LC03.csv"
    
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    relationships = {row["relationship"] for row in rows}
    expected_relationships = {"mitigated_by", "informed_by", "addresses", "informs"}
    
    for rel in relationships:
        assert rel in expected_relationships, f"TRACE_LC03.csv has unexpected relationship type: {rel}"


def test_trace_csv_all_active():
    """Verify all traceability rows are marked as active."""
    file_path = LC03_DIR / "TRACE_LC03.csv"
    
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    for row in rows:
        assert row["status"] == "active", f"TRACE_LC03.csv row not active: {row['source_id']} -> {row['target_id']}"


# ── README tests ──────────────────────────────────────────────────────────

def test_readme_is_markdown():
    """Verify README.md exists and is readable."""
    file_path = LC03_DIR / "README.md"
    assert file_path.exists(), f"README.md not found: {file_path}"
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    assert len(content) > 100, "README.md is too short"


def test_readme_references_packages():
    """Verify README.md documents all three packages."""
    file_path = LC03_DIR / "README.md"
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    assert "PACKAGES/SAFETY/" in content, "README.md missing SAFETY package reference"
    assert "PACKAGES/HAZARD_MGMT/" in content, "README.md missing HAZARD_MGMT package reference"
    assert "PACKAGES/RELIABILITY/" in content, "README.md missing RELIABILITY package reference"


def test_readme_references_trade_studies():
    """Verify README.md references all three trade studies."""
    file_path = LC03_DIR / "README.md"
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    assert "TS-28-11-TS01" in content, "README.md missing TS01 reference"
    assert "TS-28-11-TS02" in content, "README.md missing TS02 reference"
    assert "TS-28-11-TS03" in content, "README.md missing TS03 reference"


def test_readme_references_governance():
    """Verify README.md references LC01 governance."""
    file_path = LC03_DIR / "README.md"
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    assert "GOV-LC01-ATA28-11" in content, "README.md missing governance reference"
    assert "SAFETY-H2-001" in content, "README.md missing SAFETY-H2-001 escalation reference"


# ── Cross-package consistency tests ───────────────────────────────────────

def test_package_ids_unique():
    """Verify all package IDs are unique."""
    safety_path = SAFETY_DIR / "SAFETY_PACKAGE.yaml"
    reliability_path = RELIABILITY_DIR / "RELIABILITY_PACKAGE.yaml"
    hazard_path = HAZARD_DIR / "HAZARD_REGISTER.yaml"
    
    with open(safety_path, "r", encoding="utf-8") as f:
        safety_id = yaml.safe_load(f)["safety_package"]["package_id"]
    
    with open(reliability_path, "r", encoding="utf-8") as f:
        reliability_id = yaml.safe_load(f)["reliability_package"]["package_id"]
    
    with open(hazard_path, "r", encoding="utf-8") as f:
        hazard_id = yaml.safe_load(f)["hazard_register"]["register_id"]
    
    ids = [safety_id, reliability_id, hazard_id]
    assert len(ids) == len(set(ids)), "Package IDs are not unique"


def test_all_packages_same_ata_scope():
    """Verify all packages reference the same ATA scope (28-11-00)."""
    safety_path = SAFETY_DIR / "SAFETY_PACKAGE.yaml"
    reliability_path = RELIABILITY_DIR / "RELIABILITY_PACKAGE.yaml"
    hazard_path = HAZARD_DIR / "HAZARD_REGISTER.yaml"
    
    with open(safety_path, "r", encoding="utf-8") as f:
        safety_scope = yaml.safe_load(f)["safety_package"]["ata_scope"]
    
    with open(reliability_path, "r", encoding="utf-8") as f:
        reliability_scope = yaml.safe_load(f)["reliability_package"]["ata_scope"]
    
    with open(hazard_path, "r", encoding="utf-8") as f:
        hazard_scope = yaml.safe_load(f)["hazard_register"]["ata_scope"]
    
    expected_scope = ["28-11-00"]
    assert safety_scope == expected_scope, f"SAFETY package has wrong ATA scope: {safety_scope}"
    assert reliability_scope == expected_scope, f"RELIABILITY package has wrong ATA scope: {reliability_scope}"
    assert hazard_scope == "28-11-00", f"HAZARD_MGMT package has wrong ATA scope: {hazard_scope}"


def test_all_packages_same_program():
    """Verify all packages reference the same program (AMPEL360 Q100)."""
    safety_path = SAFETY_DIR / "SAFETY_PACKAGE.yaml"
    reliability_path = RELIABILITY_DIR / "RELIABILITY_PACKAGE.yaml"
    hazard_path = HAZARD_DIR / "HAZARD_REGISTER.yaml"
    
    with open(safety_path, "r", encoding="utf-8") as f:
        safety_program = yaml.safe_load(f)["safety_package"]["program"]
    
    with open(reliability_path, "r", encoding="utf-8") as f:
        reliability_program = yaml.safe_load(f)["reliability_package"]["program"]
    
    with open(hazard_path, "r", encoding="utf-8") as f:
        hazard_program = yaml.safe_load(f)["hazard_register"]["program"]
    
    expected_program = "AMPEL360 Q100"
    assert safety_program == expected_program, f"SAFETY package has wrong program: {safety_program}"
    assert reliability_program == expected_program, f"RELIABILITY package has wrong program: {reliability_program}"
    assert hazard_program == expected_program, f"HAZARD_MGMT package has wrong program: {hazard_program}"


def test_all_packages_dev_status():
    """Verify all packages have DEV status."""
    safety_path = SAFETY_DIR / "SAFETY_PACKAGE.yaml"
    reliability_path = RELIABILITY_DIR / "RELIABILITY_PACKAGE.yaml"
    hazard_path = HAZARD_DIR / "HAZARD_REGISTER.yaml"
    
    with open(safety_path, "r", encoding="utf-8") as f:
        safety_status = yaml.safe_load(f)["safety_package"]["status"]
    
    with open(reliability_path, "r", encoding="utf-8") as f:
        reliability_status = yaml.safe_load(f)["reliability_package"]["status"]
    
    with open(hazard_path, "r", encoding="utf-8") as f:
        hazard_status = yaml.safe_load(f)["hazard_register"]["status"]
    
    assert safety_status == "DEV", f"SAFETY package has wrong status: {safety_status}"
    assert reliability_status == "DEV", f"RELIABILITY package has wrong status: {reliability_status}"
    assert hazard_status == "DEV", f"HAZARD_MGMT package has wrong status: {hazard_status}"
