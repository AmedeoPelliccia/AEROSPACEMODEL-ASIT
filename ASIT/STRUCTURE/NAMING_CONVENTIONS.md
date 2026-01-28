# Naming Conventions

## Overview

This document defines the **ID grammar** for all artifacts within the ASIT-ASIGT framework. Consistent naming ensures traceability, searchability, and interoperability across the entire information ecosystem.

> **Every artifact has a unique, meaningful, and traceable identifier.**

---

## General Principles

| Principle | Description |
|-----------|-------------|
| **Uniqueness** | Each ID is globally unique within the program |
| **Meaningfulness** | IDs encode relevant metadata |
| **Traceability** | IDs support upstream/downstream linking |
| **Parsability** | IDs follow strict grammar for automated processing |
| **Stability** | Once assigned, IDs do not change |

---

## Character Set

| Allowed | Characters |
|---------|------------|
| Alphanumeric | A-Z, 0-9 |
| Separators | - (hyphen), _ (underscore) |
| Case | UPPERCASE preferred for codes |

> **Prohibited**: Spaces, special characters (&, *, #, etc.), non-ASCII

---

## ID Types

### 1. Baseline IDs

**Format**: `<TYPE>-<YEAR>-<QUARTER>-<SEQUENCE>`

| Component | Description | Example |
|-----------|-------------|---------|
| TYPE | Baseline type (FBL, ABL, PBL, OBL) | FBL |
| YEAR | 4-digit year | 2026 |
| QUARTER | Quarter (Q1-Q4) | Q1 |
| SEQUENCE | 3-digit sequence | 001 |

**Examples**:
```
FBL-2026-Q1-001     # Functional Baseline
ABL-2026-Q2-003     # Allocated Baseline
PBL-2026-Q3-001     # Product Baseline
OBL-2026-Q4-002     # Operational Baseline
```

---

### 2. Change Control IDs

#### ECR (Engineering Change Request)

**Format**: `ECR-<YEAR>-<SEQUENCE>`

| Component | Description | Example |
|-----------|-------------|---------|
| ECR | Fixed prefix | ECR |
| YEAR | 4-digit year | 2026 |
| SEQUENCE | 4-digit sequence | 0001 |

**Example**: `ECR-2026-0042`

#### ECO (Engineering Change Order)

**Format**: `ECO-<YEAR>-<SEQUENCE>`

**Example**: `ECO-2026-0035`

#### CCB (Configuration Control Board)

**Format**: `CCB-<YEAR>-<SEQUENCE>`

**Example**: `CCB-2026-0012`

---

### 3. Contract IDs

**Format**: `<PREFIX>-CTR-<CATEGORY>-<TARGET>[-<SCOPE>][-<VERSION>]`

| Component | Description | Example |
|-----------|-------------|---------|
| PREFIX | Program/project prefix | KITDM |
| CTR | Fixed "contract" marker | CTR |
| CATEGORY | Contract category | LM, OPS |
| TARGET | Target publication/output | CSDB, EXPORT |
| SCOPE | Optional scope qualifier | ATA28 |
| VERSION | Version (vX.Y.Z) | v1.2.0 |

**Examples**:
```
KITDM-CTR-LM-CSDB               # CSDB generation contract
KITDM-CTR-LM-CSDB_ATA28-v1.2.0  # ATA28-specific version
KITDM-CTR-OPS-SB                # Service Bulletin contract
KITDM-CTR-LM-EXPORT             # Export contract
```

#### Contract Categories

| Code | Meaning |
|------|---------|
| LM | Lifecycle Management |
| OPS | Operations |
| MRO | Maintenance/Repair/Overhaul |
| TRN | Training |
| CERT | Certification |

---

### 4. S1000D Data Module Codes (DMC)

**Format**: Per S1000D Issue 5.0 specification

```
<MODEL>-<DIFF>-<SYSTEM>-<SUBSYS>-<SUBSUBSYS>-<ASSY>-<DISASSY>-<VARIANT>-<INFO>-<VARIANT>-<LOCATION>
```

| Component | Length | Description |
|-----------|--------|-------------|
| MODEL | 2-14 | Model identification code |
| DIFF | 1-4 | System difference code |
| SYSTEM | 2-3 | System code (ATA chapter) |
| SUBSYS | 1-2 | Subsystem code |
| SUBSUBSYS | 1-2 | Sub-subsystem code |
| ASSY | 2 | Assembly code |
| DISASSY | 2 | Disassembly code |
| VARIANT | 1-3 | Disassembly code variant |
| INFO | 3 | Information code |
| VARIANT | 1 | Information code variant |
| LOCATION | 1 | Item location code |

**Example**:
```
HJ1-A-28-10-00-00A-040A-A      # Fuel storage description
│   │ │  │  │  │   │    └── Item location
│   │ │  │  │  │   └─────── Info code + variant (040A = Description)
│   │ │  │  │  └─────────── Disassy code variant
│   │ │  │  └────────────── Assembly/Disassembly codes
│   │ │  └───────────────── Sub-subsystem
│   │ └──────────────────── Subsystem (Storage)
│   └────────────────────── System code (Fuel)
└────────────────────────── Model + System diff code
```

#### Common Information Codes

| Code | Type | Description |
|------|------|-------------|
| 000 | Functional | Function description |
| 040 | Description | Descriptive information |
| 100 | Operation | Operating procedures |
| 200 | Servicing | Servicing procedures |
| 300 | Inspection | Inspection procedures |
| 400 | Removal | Removal procedures |
| 500 | Installation | Installation procedures |
| 600 | Repair | Repair procedures |
| 700 | Setting/Test | Adjustment and test |
| 800 | Storage | Storage procedures |
| 900 | Parts | Illustrated parts data |
| 941 | Parts | IPD - parts breakdown |

---

### 5. Publication Module Codes (PMC)

**Format**: `<MODEL>-<PMIC>-<ISSUE>-<LANGUAGE>`

| Component | Description | Example |
|-----------|-------------|---------|
| MODEL | Model identification | HJ1 |
| PMIC | PM identification code | 00001 |
| ISSUE | Issue number | 001 |
| LANGUAGE | Language code | EN |

**Example**: `HJ1-00001-001-EN`

---

### 6. Information Control Numbers (ICN)

**Format**: `ICN-<MODEL>-<TYPE>-<SEQUENCE>-<VARIANT>-<ISSUE>`

| Component | Description | Example |
|-----------|-------------|---------|
| ICN | Fixed prefix | ICN |
| MODEL | Model code | HJ1 |
| TYPE | Graphic type | SH (sheet), IL (illustration) |
| SEQUENCE | 5-digit sequence | 00001 |
| VARIANT | Variant code | A |
| ISSUE | Issue (3-digit) | 001 |

**Example**: `ICN-HJ1-SH-00001-A-001`

#### Graphic Types

| Code | Type |
|------|------|
| SH | Sheet (drawing) |
| IL | Illustration |
| PH | Photograph |
| SC | Schematic |
| WD | Wiring diagram |
| MM | Multimedia |

---

### 7. Run/Execution IDs

**Format**: `<YYYYMMDD>-<HHMM>__<CONTRACT-ID>`

**Example**: `20260122-1430__KITDM-CTR-LM-CSDB_ATA28`

---

### 8. Artifact IDs

#### KDB Artifacts

**Format**: `KDB-<CATEGORY>-<TYPE>-<SEQUENCE>`

| Component | Description |
|-----------|-------------|
| KDB | Fixed prefix |
| CATEGORY | REQ, DSN, ANA, TST, CERT |
| TYPE | Artifact type code |
| SEQUENCE | Unique sequence |

**Examples**:
```
KDB-REQ-SYS-0001        # System requirement
KDB-DSN-SCH-0042        # Schematic design
KDB-ANA-STR-0015        # Stress analysis
KDB-TST-QUA-0008        # Qualification test
```

#### IDB Artifacts

**Format**: S1000D DMC (see above)

---

### 9. Stakeholder Codes

**Format**: `STK_<ROLE>`

| Code | Role |
|------|------|
| STK_ENG | Engineering |
| STK_CERT | Certification |
| STK_CM | Configuration Management |
| STK_QA | Quality Assurance |
| STK_MFG | Manufacturing |
| STK_OPS | Operations |
| STK_MRO | Maintenance/Repair/Overhaul |
| STK_BUS | Business/Program |

---

### 10. Version Numbers

**Format**: `v<MAJOR>.<MINOR>.<PATCH>`

Following Semantic Versioning:

| Component | Increment When |
|-----------|----------------|
| MAJOR | Breaking changes |
| MINOR | Backward-compatible additions |
| PATCH | Backward-compatible fixes |

**Examples**:
```
v1.0.0      # Initial release
v1.1.0      # Added features
v1.1.1      # Bug fix
v2.0.0      # Breaking change
```

---

## ID Registry

All assigned IDs must be registered in [../INDEX/ID_REGISTRY.csv](../INDEX/ID_REGISTRY.csv).

### Registry Fields

| Field | Description |
|-------|-------------|
| id | The assigned ID |
| type | ID type (baseline, contract, dmc, etc.) |
| description | Brief description |
| created_date | ISO 8601 date |
| created_by | Creator stakeholder |
| status | ACTIVE, SUPERSEDED, WITHDRAWN |
| superseded_by | Replacement ID (if applicable) |

---

## Validation Rules

### Automated Validation

All IDs must pass validation:

```yaml
validation_rules:
  baseline_id:
    pattern: "^(FBL|ABL|PBL|OBL)-\\d{4}-Q[1-4]-\\d{3}$"
    
  ecr_id:
    pattern: "^ECR-\\d{4}-\\d{4}$"
    
  eco_id:
    pattern: "^ECO-\\d{4}-\\d{4}$"
    
  contract_id:
    pattern: "^[A-Z0-9]+-CTR-[A-Z]+-[A-Z0-9]+(-[A-Za-z0-9_]+)?(-v\\d+\\.\\d+\\.\\d+)?$"
    
  dmc:
    pattern: "^[A-Z0-9]{2,14}-[A-Z0-9]{1,4}-\\d{2,3}-\\d{1,2}-\\d{1,2}-\\d{2}[A-Z]?-\\d{3}[A-Z]-[A-Z]$"
    
  version:
    pattern: "^v\\d+\\.\\d+\\.\\d+$"
```

---

## Related Documents

- [ATA_MAPPING.yaml](ATA_MAPPING.yaml) — ATA chapter codes
- [LIFECYCLE_PHASES.yaml](LIFECYCLE_PHASES.yaml) — Lifecycle phase codes
- [../INDEX/ID_REGISTRY.csv](../INDEX/ID_REGISTRY.csv) — ID registry
- [../CONTRACTS/CONTRACT_SCHEMA.yaml](../CONTRACTS/CONTRACT_SCHEMA.yaml) — Contract ID structure
