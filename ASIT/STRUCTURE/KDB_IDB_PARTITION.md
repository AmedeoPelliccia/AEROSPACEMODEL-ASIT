# Knowledge Database (KDB) vs Information Database (IDB) Partition

## Overview

The ASIT-ASIGT framework enforces a strict separation between **engineering knowledge** (KDB) and **operational information** (IDB). This separation ensures that the Single Source of Truth (SSOT) remains uncorrupted while enabling governed transformation into operational publications.

> **KDB is the truth. IDB is the projection.**

---

## Fundamental Principle

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   KDB (Knowledge Database)                                          │
│   ═══════════════════════                                           │
│   • Engineering truth (SSOT)                                        │
│   • Requirements, designs, analyses                                 │
│   • Owned by Engineering                                            │
│   • NEVER directly modified by downstream consumers                 │
│                                                                     │
│                          │                                          │
│                          │  ASIT-governed transformation            │
│                          │  (contract-bound, traced)                │
│                          ▼                                          │
│                                                                     │
│   IDB (Information Database)                                        │
│   ══════════════════════════                                        │
│   • Operational publications                                        │
│   • AMM, SRM, IPC, SB, etc.                                        │
│   • Owned by Publications                                           │
│   • Derived ONLY from KDB through ASIGT                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Database Definitions

### KDB — Knowledge Database

| Attribute | Description |
|-----------|-------------|
| **Purpose** | Store validated engineering knowledge |
| **Content** | Requirements, designs, analyses, test results, certifications |
| **Owner** | Engineering organization |
| **Authority** | STK_ENG, STK_CERT |
| **Mutability** | Controlled via ECR/ECO process |
| **Consumers** | ASIGT (read-only) |

#### KDB Content Categories

| Category | Examples |
|----------|----------|
| Requirements | System requirements, interface requirements, safety requirements |
| Design | CAD models, schematics, calculations |
| Analysis | Stress analysis, thermal analysis, FMEA |
| Test | Test procedures, test results, qualification reports |
| Certification | Compliance matrices, MOC documents, TC data |

### IDB — Information Database

| Attribute | Description |
|-----------|-------------|
| **Purpose** | Store operational technical publications |
| **Content** | S1000D Data Modules, Publication Modules |
| **Owner** | Publications organization |
| **Authority** | STK_CM, STK_OPS |
| **Mutability** | Regenerated from KDB via ASIGT |
| **Consumers** | MRO, operators, training |

#### IDB Content Categories

| Category | Publications |
|----------|--------------|
| Maintenance | AMM, SRM, CMM, WDM |
| Operations | FCOM, QRH, MEL |
| Parts | IPC, AIPC |
| Service | SB, SL, AD |
| Training | Training manuals, CBT |

---

## Partition Rules

### Rule 1: No Direct IDB Authoring

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   PROHIBITED: Direct authoring in IDB                               │
│   ─────────────────────────────────────                             │
│   • No manual creation of Data Modules                              │
│   • No direct editing of generated content                          │
│   • No copy-paste from external sources                             │
│                                                                     │
│   REQUIRED: All IDB content generated via ASIGT from KDB            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Rule 2: Traceability Mandatory

Every IDB artifact must trace to:
- Source KDB artifact(s)
- ASIT contract that authorized transformation
- Baseline version
- Generation timestamp

### Rule 3: KDB Primacy

When discrepancy exists:
- KDB is authoritative
- IDB must be regenerated
- Discrepancy logged as nonconformance

### Rule 4: Bidirectional Awareness

| Direction | Purpose |
|-----------|---------|
| KDB → IDB | Transformation (ASIGT generates) |
| IDB → KDB | Feedback (issues, gaps identified) |

> Feedback never modifies KDB directly. It triggers ECR/ECO process.

---

## Content Mapping

### KDB to IDB Transformation Types

| KDB Source | IDB Target | Transformation |
|------------|------------|----------------|
| System Requirement | Descriptive DM | Requirement to description |
| Maintenance Task | Procedural DM | Task to procedure |
| Structural Repair | SRM DM | Repair data to repair procedure |
| Part Definition | IPD DM | Part data to illustrated parts |
| Troubleshooting Logic | Fault DM | Fault tree to isolation procedure |
| Wiring Data | WDM DM | Wiring database to diagram |

### Mapping Configuration

```yaml
# Example mapping configuration
mappings:
  - source_type: "REQUIREMENT"
    source_location: "KDB/REQUIREMENTS/"
    target_type: "DM_DESCRIPTIVE"
    target_location: "IDB/CSDB/"
    mapping_rules: "mapping/requirement_to_dm.yaml"
    
  - source_type: "TASK"
    source_location: "KDB/TASKS/"
    target_type: "DM_PROCEDURAL"
    target_location: "IDB/CSDB/"
    mapping_rules: "mapping/task_to_dm.yaml"
```

---

## Directory Structure

### KDB Structure (Reference)

```
KDB/
├── REQUIREMENTS/
│   ├── system/
│   ├── interface/
│   └── safety/
├── DESIGN/
│   ├── models/
│   ├── schematics/
│   └── calculations/
├── ANALYSIS/
│   ├── stress/
│   ├── thermal/
│   └── fmea/
├── TEST/
│   ├── procedures/
│   ├── results/
│   └── qualification/
└── CERTIFICATION/
    ├── compliance/
    ├── moc/
    └── tc_data/
```

### IDB Structure (Reference)

```
IDB/
├── CSDB/                           # Common Source Database
│   ├── DMC/                        # Data Modules by code
│   ├── PMC/                        # Publication Modules
│   └── ICN/                        # Information Control Numbers
├── PUBLICATIONS/
│   ├── AMM/
│   ├── SRM/
│   ├── IPC/
│   └── SB/
└── EXPORTS/
    ├── PDF/
    ├── HTML/
    └── IETP/
```

---

## Governance

### KDB Governance

| Aspect | Rule |
|--------|------|
| Access | Read: Engineering, Publications; Write: Engineering |
| Changes | Via ECR/ECO only |
| Baselines | FBL, ABL, PBL |
| Retention | Life of program + regulatory requirements |

### IDB Governance

| Aspect | Rule |
|--------|------|
| Access | Read: All authorized; Write: ASIGT only |
| Changes | Regeneration from KDB only |
| Baselines | OBL (derived from KDB baselines) |
| Retention | Per publication requirements |

---

## Synchronization

### Triggers for IDB Regeneration

| Trigger | Action |
|---------|--------|
| KDB baseline release | Full or incremental IDB regeneration |
| ECO completion | Affected artifacts regenerated |
| Publication request | On-demand generation |
| Scheduled refresh | Periodic consistency check |

### Synchronization Process

```
1. Change detected in KDB (or scheduled sync)
2. ASIT identifies affected contracts
3. ASIGT executes transformations
4. Validation performed (BREX, schema)
5. Trace matrix updated
6. IDB baseline released
7. Distribution to consumers
```

---

## Audit and Compliance

### Traceability Artifacts

| Artifact | Purpose |
|----------|---------|
| TRACE_MATRIX.csv | Source → target mapping |
| INPUT_MANIFEST.json | KDB inputs for each run |
| OUTPUT_MANIFEST.json | IDB outputs for each run |
| VALIDATION_REPORT.json | Compliance verification |

### Compliance Checks

- [ ] All IDB content traces to KDB source
- [ ] No orphan IDB artifacts (missing KDB source)
- [ ] No stale IDB artifacts (KDB source updated)
- [ ] Baseline alignment verified
- [ ] Authority chain documented

---

## Related Documents

- [../GOVERNANCE/BASELINES.md](../GOVERNANCE/BASELINES.md) — Baseline policies
- [../../ASIGT/mapping/](../../ASIGT/mapping/) — Transformation mapping rules
- [../CONTRACTS/](../CONTRACTS/) — Transformation contracts
