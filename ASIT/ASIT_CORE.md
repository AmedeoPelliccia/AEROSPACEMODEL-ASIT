# ASIT_CORE

## Aircraft Systems Information Transponder — Specification

> **Version:** 2.0.0  
> **Status:** Normative  
> **Classification:** Framework Specification

---

## 1. Purpose

**ASIT (Aircraft Systems Information Transponder)** is the **authoritative governance layer** that defines the structure, lifecycle, contracts, and approval authority for aerospace information transformation.

ASIT does not generate content. ASIT defines:

- **WHAT** can be transformed
- **FROM WHERE** (which baseline)
- **UNDER WHAT AUTHORITY** (governance)
- **TO WHAT STATE** (lifecycle)
- **WITH WHAT EVIDENCE** (traceability)

---

## 2. Fundamental Constraint

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   ASIT IS THE SINGLE AUTHORITY FOR INFORMATION STRUCTURE AND GOVERNANCE    │
│                                                                             │
│   No transformation occurs without:                                         │
│     1. An approved ASIT contract                                            │
│     2. A defined ASIT baseline                                              │
│     3. A valid ASIT lifecycle state                                         │
│     4. An ASIT-authorized execution context                                 │
│                                                                             │
│   ASIGT cannot execute without ASIT authorization.                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Architecture

### 3.1 ASIT Domains

```
ASIT
├── GOVERNANCE        # Authority, approvals, change control
├── STRUCTURE         # System hierarchy, KDB/IDB partitioning
├── LIFECYCLE         # Phases, states, effectivity
├── CONTRACTS         # Transformation rules, scope
├── INDEX             # Navigation, traceability, registry
└── CONFIG            # Program configuration
```

### 3.2 Domain Responsibilities

| Domain | Primary Responsibility |
|--------|------------------------|
| **GOVERNANCE** | Who controls what, change authorization |
| **STRUCTURE** | What exists, how it's organized |
| **LIFECYCLE** | When things transition, from which state |
| **CONTRACTS** | What transforms to what, under what rules |
| **INDEX** | Where to find things, how they relate |
| **CONFIG** | Program-specific parameters |

---

## 4. GOVERNANCE Domain

### 4.1 Purpose

GOVERNANCE controls **authority** for all information operations.

### 4.2 Components

#### 4.2.1 Baseline Management

| Baseline Type | Code | Purpose |
|---------------|------|---------|
| Functional Baseline | FBL | Requirements freeze |
| Design Baseline | DBL | Design definition freeze |
| Product Baseline | PBL | Production configuration |
| Operational Baseline | OBL | In-service configuration |

**Baseline Schema:**

```yaml
baseline:
  id: "FBL-2026-Q1-003"
  type: "FBL"
  status: "ESTABLISHED"           # PROPOSED | ESTABLISHED | SUPERSEDED
  
  scope:
    ata_chapters: ["21", "24", "28"]
    lifecycle_phases: ["LC02", "LC04"]
    
  contents:
    - artifact_id: "REQ-ATA28-001"
      path: "KDB/LM/SSOT/PLM/LC02_.../REQ-ATA28-001.yaml"
      hash: "sha256:a1b2c3d4..."
      version: "1.2.0"
      
  effectivity:
    established_date: "2026-01-15"
    superseded_date: null
    msn_range: ["001", "050"]
    
  authority:
    ccb_reference: "CCB-2026-0003"
    approved_by: "STK_CM"
    approval_date: "2026-01-15"
```

#### 4.2.2 Change Control

**Engineering Change Request (ECR):**

```yaml
ecr:
  id: "ECR-2026-042"
  title: "Update fuel system maintenance intervals"
  status: "OPEN"                  # OPEN | UNDER_REVIEW | APPROVED | REJECTED
  
  classification:
    type: "MAJOR"                 # MAJOR | MINOR | ADMINISTRATIVE
    impact: ["MAINTENANCE", "CERTIFICATION"]
    
  affected_items:
    - artifact: "DM-ATA28-001"
      change_type: "MODIFY"       # ADD | MODIFY | DELETE
      
  analysis:
    safety_impact: "No safety impact"
    certification_impact: "MMEL update required"
    
  disposition: null               # Populated by CCB
```

**Engineering Change Order (ECO):**

```yaml
eco:
  id: "ECO-2026-027"
  ecr_reference: "ECR-2026-042"
  status: "IN_PROGRESS"           # PENDING | IN_PROGRESS | COMPLETE
  
  implementation:
    affected_baselines: ["FBL-2026-Q1-003"]
    target_baseline: "FBL-2026-Q2-001"
    
  verification:
    criteria: ["BREX validation", "Trace coverage 100%"]
    evidence: []                  # Populated on completion
```

#### 4.2.3 Approval Matrix

```csv
artifact_type,lifecycle_phase,approver_role,required,backup_role
REQ,LC02,STK_SE,true,STK_PM
DM,LC04,STK_CM,true,STK_SE
SAFETY,LC03,STK_SAF,true,
TEST,LC06,STK_TEST,true,STK_SE
```

---

## 5. STRUCTURE Domain

### 5.1 Purpose

STRUCTURE defines **what exists and how it's organized**.

### 5.2 ATA iSpec 2200 Mapping

```yaml
ata_mapping:
  version: "iSpec 2200"
  
  chapters:
    - chapter: "21"
      title: "Air Conditioning and Pressurization"
      sections:
        - section: "00"
          title: "General"
        - section: "10"
          title: "Compression"
        - section: "20"
          title: "Distribution"
        # ... etc.
        
    - chapter: "28"
      title: "Fuel"
      sections:
        - section: "00"
          title: "General"
        - section: "10"
          title: "Storage"
        - section: "20"
          title: "Distribution"
        # ... etc.
```

### 5.3 KDB/IDB Partitioning

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        KNOWLEDGE vs INFORMATION                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   KDB (Knowledge Data Base)              IDB (Information Data Base)        │
│   ═══════════════════════════            ═══════════════════════════        │
│   Engineering truth                      Operational projection             │
│   SSOT for requirements,                 Publications, IETP,                │
│   design, safety, analysis               service bulletins                  │
│                                                                             │
│   KDB/                                   IDB/                               │
│   ├── DEV/          (Working)            ├── OPS/          (Operations)     │
│   │   └── ...                            │   └── LM/                        │
│   └── LM/           (Lifecycle-Managed)  │       ├── LC11_...               │
│       └── SSOT/                          │       ├── LC12_...               │
│           └── PLM/                       │       ├── LC13_...               │
│               ├── LC01_...               │       └── LC14_...               │
│               ├── LC02_...               │                                  │
│               ├── ...                    └── PUB/          (Publications)   │
│               └── LC10_...                   ├── AMM/                       │
│                                              ├── SRM/                       │
│   Engineering creates KDB                    ├── CMM/                       │
│   ASIT governs KDB→IDB                       └── IPC/                       │
│   ASIGT materializes IDB                                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.4 Lifecycle Phases

| Phase | Code | Description |
|-------|------|-------------|
| Problem Statement | LC01 | Uncertainty orchestration, KNOT/KNU |
| System Requirements | LC02 | Requirements definition |
| Safety/Reliability | LC03 | Safety analysis, FMEA |
| Design Definition | LC04 | Design specs, ICDs |
| Analysis/Models | LC05 | FEA, CFD, simulations |
| Verification | LC06 | Test procedures, evidence |
| Validation | LC07 | Integration testing |
| Configuration | LC08 | Baselines, effectivity |
| Production | LC09 | Manufacturing |
| Operations | LC10 | Operational documentation |
| Maintenance | LC11 | MRO procedures |
| Customer Care | LC12 | Support, AOG, bulletins |
| MRO Sustainment | LC13 | Maintenance sources |
| Retirement/Circularity | LC14 | End-of-life, DPP |

---

## 6. CONTRACTS Domain

### 6.1 Purpose

A contract defines a **governed transformation** from sources to outputs.

### 6.2 Contract Naming Convention

```
KITDM-CTR-<DOMAIN>-<TYPE>_<SCOPE>

Where:
  KITDM  = Knowledge Information Transformation Data Module
  CTR    = Contract
  DOMAIN = LM (Lifecycle-Managed) | OPS (Operational)
  TYPE   = CSDB | EXPORT | IETP | SB | REPAIR | COC
  SCOPE  = ATA chapter or custom identifier
```

**Examples:**
- `KITDM-CTR-LM-CSDB_ATA28` — KDB→CSDB for ATA 28
- `KITDM-CTR-LM-EXPORT_ATA28` — CSDB→PDF/HTML for ATA 28
- `KITDM-CTR-OPS-SB_ATA28` — Service Bulletin generation for ATA 28

### 6.3 Contract Schema

```yaml
contract:
  # ═══════════════════════════════════════════════════════════════════
  # IDENTIFICATION
  # ═══════════════════════════════════════════════════════════════════
  
  id: "KITDM-CTR-LM-CSDB_ATA28"
  version: "1.2.0"
  status: "APPROVED"              # DRAFT | REVIEW | APPROVED | SUPERSEDED
  
  metadata:
    title: "ATA 28 Fuel System CSDB Generation"
    description: "Transform fuel system engineering data to AMM"
    author: "Configuration Management"
    created: "2026-01-10"
    approved: "2026-01-15"
    
  # ═══════════════════════════════════════════════════════════════════
  # SCOPE
  # ═══════════════════════════════════════════════════════════════════
  
  scope:
    ata_chapters: ["28"]
    ata_sections: ["00", "10", "20", "30", "40"]
    lifecycle_sources: ["LC02", "LC04", "LC13"]
    publication_target: "AMM"
    
  # ═══════════════════════════════════════════════════════════════════
  # INPUTS — What to consume
  # ═══════════════════════════════════════════════════════════════════
  
  inputs:
    baseline: "FBL-2026-Q1-003"     # Or "LATEST"
    
    required:
      - id: "requirements"
        source: "KDB/LM/SSOT/PLM/LC02_.../PACKAGES/REQ/**/*.yaml"
        type: "requirement"
        min_count: 1
        
      - id: "maintenance_tasks"
        source: "IDB/OPS/LM/LC13_.../Maintenance_Source/AMM_TASKS/**/*.yaml"
        type: "maintenance_task"
        min_count: 1
        
    optional:
      - id: "safety_data"
        source: "KDB/LM/SSOT/PLM/LC03_.../PACKAGES/SAFETY/**/*.yaml"
        type: "safety_analysis"
        
      - id: "graphics"
        source: "assets/graphics/ata28/**/*.svg"
        type: "icn"
        
  # ═══════════════════════════════════════════════════════════════════
  # OUTPUTS — What to produce
  # ═══════════════════════════════════════════════════════════════════
  
  outputs:
    - id: "data_modules"
      target: "IDB/PUB/AMM/CSDB/DM"
      type: "S1000D_DM"
      naming: "S1000D"
      expected_count: ">=10"
      
    - id: "data_module_list"
      target: "IDB/PUB/AMM/CSDB/DML"
      type: "S1000D_DML"
      expected_count: 1
      
    - id: "publication_module"
      target: "IDB/PUB/AMM/CSDB/PM"
      type: "S1000D_PM"
      expected_count: 1
      
  # ═══════════════════════════════════════════════════════════════════
  # TRANSFORMATION — How to map (delegates to ASIGT)
  # ═══════════════════════════════════════════════════════════════════
  
  transformation:
    pipeline: "pipelines/amm_pipeline.yaml"
    
    mappings:
      - source: "requirements"
        target: "data_modules"
        rules: "ASIGT/mapping/requirement_to_dm.yaml"
        template: "ASIGT/s1000d_templates/dm_descriptive.xml"
        
      - source: "maintenance_tasks"
        target: "data_modules"
        rules: "ASIGT/mapping/task_to_dm.yaml"
        template: "ASIGT/s1000d_templates/dm_procedural.xml"
        
  # ═══════════════════════════════════════════════════════════════════
  # VALIDATION — What to verify
  # ═══════════════════════════════════════════════════════════════════
  
  validation:
    brex:
      required: true
      rules: "ASIGT/brex/project_brex.yaml"
      fail_on_warning: false
      
    schema:
      required: true
      version: "S1000D_5.0"
      
    trace:
      required: true
      min_coverage_percent: 100
      
  # ═══════════════════════════════════════════════════════════════════
  # ACCEPTANCE — What makes it complete
  # ═══════════════════════════════════════════════════════════════════
  
  acceptance:
    all_inputs_processed: true
    no_validation_errors: true
    trace_complete: true
    
  # ═══════════════════════════════════════════════════════════════════
  # AUTHORITY — Who approved
  # ═══════════════════════════════════════════════════════════════════
  
  approvals:
    - role: "STK_CM"
      required: true
      name: "Jane Smith"
      signature: "CM-2026-0042"
      date: "2026-01-15"
      
    - role: "STK_SE"
      required: true
      name: "John Doe"
      signature: "SE-2026-0108"
      date: "2026-01-15"
```

### 6.4 Contract Lifecycle

```
┌─────────┐     ┌─────────┐     ┌──────────┐     ┌────────────┐
│  DRAFT  │────▶│ REVIEW  │────▶│ APPROVED │────▶│ SUPERSEDED │
└─────────┘     └─────────┘     └──────────┘     └────────────┘
     │                               │
     │   ASIGT cannot execute        │   ASIGT can execute
     └───────────────────────────────┘
```

---

## 7. ASIT–ASIGT Interface

### 7.1 Execution Context

When ASIT invokes ASIGT, it provides an **execution context**:

```yaml
execution_context:
  # Contract identification
  contract_id: "KITDM-CTR-LM-CSDB_ATA28"
  contract_version: "1.2.0"
  
  # Source baseline
  baseline_id: "FBL-2026-Q1-003"
  baseline_effective: "2026-01-15"
  
  # Authority
  invoker: "pipeline-runner@aerospacemodel.io"
  invocation_time: "2026-01-21T14:30:00Z"
  authority_reference: "CCB-2026-0042"
  
  # Paths
  input_manifest: "runs/20260121-1430/INPUT_MANIFEST.json"
  output_target: "IDB/PUB/AMM/CSDB"
  run_archive: "ASIGT/runs/20260121-1430__KITDM-CTR-LM-CSDB_ATA28"
  
  # Validation requirements
  brex_rules: "ASIGT/brex/project_brex.yaml"
  schema_version: "S1000D_5.0"
  trace_coverage_required: 100
```

### 7.2 ASIGT Response

ASIGT returns a **run result** to ASIT:

```yaml
run_result:
  run_id: "20260121-1430__KITDM-CTR-LM-CSDB_ATA28"
  status: "SUCCESS"               # SUCCESS | PARTIAL | FAILED
  
  execution:
    start_time: "2026-01-21T14:30:00Z"
    end_time: "2026-01-21T14:35:42Z"
    duration_seconds: 342
    
  metrics:
    inputs_loaded: 47
    inputs_processed: 47
    outputs_generated: 52
    transformations_applied: 156
    
  validation:
    brex_status: "PASS"
    brex_errors: 0
    brex_warnings: 3
    schema_status: "PASS"
    trace_coverage: 100.0
    
  artifacts:
    input_manifest: "runs/.../INPUT_MANIFEST.json"
    output_manifest: "runs/.../OUTPUT_MANIFEST.json"
    trace_matrix: "runs/.../TRACE_MATRIX.csv"
    validation_report: "runs/.../VALIDATION_REPORT.json"
    metrics: "runs/.../METRICS.json"
    log: "runs/.../LOG.txt"
```

---

## 8. Traceability Requirements

### 8.1 Minimum Coverage

| Contract Type | Required Trace Coverage |
|---------------|------------------------|
| CSDB Publication | 100% |
| Export (PDF/HTML) | Inherited from source |
| Service Bulletin | 100% |
| Repair Data | 100% |

### 8.2 Trace Link Types

| Type | Meaning | Example |
|------|---------|---------|
| `derives` | Target derived from source | Requirement → Design |
| `satisfies` | Target satisfies source | Design → Requirement |
| `implements` | Target implements source | Code → Design |
| `verifies` | Target verifies source | Test → Requirement |
| `transforms` | Target transformed from source | Task → DM |
| `supersedes` | Target replaces source | DM v2 → DM v1 |

### 8.3 Trace Matrix Format

```csv
source_id,source_path,source_hash,source_type,target_id,target_path,target_hash,target_type,link_type,contract_id,timestamp
REQ-ATA28-001,KDB/.../REQ-ATA28-001.yaml,sha256:a1b2...,requirement,DMC-...-001-A,IDB/.../DMC-...-001-A.xml,sha256:e5f6...,data_module,transforms,KITDM-CTR-LM-CSDB_ATA28,2026-01-21T14:32:15Z
```

---

## 9. Compliance Mapping

| Requirement | ASIT Component |
|-------------|----------------|
| ARP4754A Development Assurance | LIFECYCLE, GOVERNANCE |
| ARP4761 Safety Assessment | TRACEABILITY, BASELINES |
| DO-178C Software Traceability | TRACE_MATRIX, CONTRACTS |
| AS9100 Quality Management | CHANGE_CONTROL, APPROVALS |
| S1000D Technical Publications | CONTRACT → ASIGT |
| ATA iSpec 2200 | STRUCTURE/ATA_MAPPING |

---

## 10. Glossary

| Term | Definition |
|------|------------|
| **ASIT** | Aircraft Systems Information Transponder — governance layer |
| **ASIGT** | Aircraft Systems Information Generative Transponder — generation layer |
| **Baseline** | Frozen, identified configuration snapshot |
| **Contract** | Governed transformation specification |
| **KDB** | Knowledge Data Base (engineering SSOT) |
| **IDB** | Information Data Base (operational projection) |
| **SSOT** | Single Source of Truth |
| **KITDM** | Knowledge Information Transformation Data Module |

---

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | ASIT-CORE-v2.0.0 |
| **Status** | Normative |
| **Next Review** | 2027-01-01 |

---

*End of ASIT_CORE Specification*
