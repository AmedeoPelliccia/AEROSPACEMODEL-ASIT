# ASIGT_CORE

## Aircraft Systems Information Generative Transponder — Specification

> **Version:** 2.0.0  
> **Status:** Normative  
> **Classification:** Framework Specification

---

## 1. Purpose

**ASIGT (Aircraft Systems Information Generative Transponder)** is the **content materialization layer** that transforms governed engineering knowledge into operational information products.

ASIGT performs:

- **GENERATION** of S1000D artifacts (DM, PM, DML)
- **VALIDATION** against BREX and schema
- **FILTERING** by applicability (ACT/PCT/CCT)
- **PACKAGING** for delivery (IETP, PDF, HTML)
- **TRACING** of all transformations

---

## 2. Fundamental Constraint

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   ASIGT CANNOT OPERATE STANDALONE                                           │
│                                                                             │
│   ASIGT executes ONLY when:                                                 │
│     1. An ASIT contract is provided                                         │
│     2. The contract status is APPROVED                                      │
│     3. A valid baseline reference exists                                    │
│     4. An authorized execution context is established                       │
│                                                                             │
│   ASIGT does NOT:                                                           │
│     • Define what to transform (ASIT does)                                  │
│     • Determine scope or configuration (ASIT does)                          │
│     • Approve or authorize outputs (ASIT does)                              │
│                                                                             │
│   This is a certification-safe architectural constraint.                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Architecture

### 3.1 ASIGT Components

```
ASIGT
├── GENERATORS        # Content creation (DM, PM, DML)
├── VALIDATORS        # Compliance checking (BREX, Schema, Trace)
├── RENDERERS         # Output production (PDF, HTML, IETP)
├── TEMPLATES         # S1000D XML templates
├── MAPPING           # Source→target transformation rules
├── BREX              # Business rules
└── RUNS              # Execution history (immutable archive)
```

### 3.2 Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| **GENERATORS** | Create S1000D artifacts from source data |
| **VALIDATORS** | Verify BREX compliance, schema conformance, trace coverage |
| **RENDERERS** | Produce deliverable formats (PDF, HTML, IETP) |
| **TEMPLATES** | Provide S1000D XML structure |
| **MAPPING** | Define source-to-target field mappings |
| **BREX** | Encode business rules for validation |
| **RUNS** | Store immutable execution evidence |

---

## 4. Execution Model

### 4.1 Invocation Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ASIGT EXECUTION FLOW                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   1. RECEIVE EXECUTION CONTEXT (from ASIT)                                  │
│      ├── Contract ID + version                                              │
│      ├── Baseline reference                                                 │
│      ├── Authority credentials                                              │
│      └── Validation requirements                                            │
│                                                                             │
│   2. VALIDATE CONTRACT                                                      │
│      ├── Status must be APPROVED                                            │
│      ├── Baseline must exist                                                │
│      └── Authority must be valid                                            │
│                                                                             │
│   3. LOAD SOURCES                                                           │
│      ├── Resolve paths from contract                                        │
│      ├── Load artifacts from baseline                                       │
│      ├── Compute input hashes                                               │
│      └── Build INPUT_MANIFEST                                               │
│                                                                             │
│   4. TRANSFORM                                                              │
│      ├── Apply mapping rules                                                │
│      ├── Use S1000D templates                                               │
│      ├── Generate DM/PM/DML                                                 │
│      └── Link ICN references                                                │
│                                                                             │
│   5. VALIDATE                                                               │
│      ├── BREX validation                                                    │
│      ├── Schema validation                                                  │
│      ├── Trace coverage check                                               │
│      └── Build VALIDATION_REPORT                                            │
│                                                                             │
│   6. PACKAGE                                                                │
│      ├── Write outputs to target paths                                      │
│      ├── Build OUTPUT_MANIFEST                                              │
│      ├── Build TRACE_MATRIX                                                 │
│      └── Archive run artifacts                                              │
│                                                                             │
│   7. RETURN RESULT (to ASIT)                                                │
│      ├── Status (SUCCESS | PARTIAL | FAILED)                                │
│      ├── Metrics                                                            │
│      ├── Validation summary                                                 │
│      └── Artifact paths                                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Pre-Execution Validation

Before any transformation, ASIGT MUST verify:

```python
def validate_execution_context(context: ExecutionContext) -> bool:
    """
    ASIGT must validate before executing.
    Returns True only if all checks pass.
    """
    # 1. Contract must be provided
    if not context.contract_id:
        raise ASIGTError("No contract provided")
    
    # 2. Contract must be APPROVED
    contract = load_contract(context.contract_id)
    if contract.status != "APPROVED":
        raise ASIGTError(f"Contract not approved: {contract.status}")
    
    # 3. Baseline must exist
    baseline = load_baseline(context.baseline_id)
    if not baseline:
        raise ASIGTError(f"Baseline not found: {context.baseline_id}")
    
    # 4. Authority must be valid
    if not verify_authority(context.authority_reference):
        raise ASIGTError("Invalid authority")
    
    return True
```

---

## 5. Generators

### 5.1 Data Module Generator

Generates S1000D Data Modules from source artifacts.

**Supported DM Types:**

| Type | Code | Template |
|------|------|----------|
| Descriptive | descript | `dm_descriptive.xml` |
| Procedural | proced | `dm_procedural.xml` |
| Fault Isolation | fault | `dm_fault_isolation.xml` |
| Illustrated Parts Data | ipd | `dm_ipd.xml` |
| Crew/Operator | crew | `dm_crew.xml` |
| Maintenance Planning | schedul | `dm_maintenance.xml` |

**DM Generation Process:**

```yaml
dm_generation:
  input:
    source_artifact: "TASK-ATA28-001.yaml"
    mapping_rules: "task_to_dm.yaml"
    template: "dm_procedural.xml"
    
  steps:
    - name: "Parse source"
      action: "load_yaml"
      
    - name: "Apply mapping"
      action: "transform_fields"
      rules:
        - source: "task.title"
          target: "dmTitle/techName"
        - source: "task.description"
          target: "dmContent/description/para"
        - source: "task.steps[]"
          target: "dmContent/procedure/mainProcedure/proceduralStep"
          
    - name: "Generate DMC"
      action: "build_dmc"
      pattern:
        modelIdentCode: "${program.model_code}"
        systemDiffCode: "A"
        systemCode: "${ata.chapter}"
        subSystemCode: "${ata.section}"
        subSubSystemCode: "${ata.subject}"
        assyCode: "00"
        disassyCode: "00"
        disassyCodeVariant: "A"
        infoCode: "040"
        infoCodeVariant: "A"
        itemLocationCode: "A"
        
    - name: "Render XML"
      action: "apply_template"
      
  output:
    path: "IDB/PUB/AMM/CSDB/DM/DMC-${dmc}.xml"
    hash: "sha256:..."
```

### 5.2 Publication Module Generator

Generates S1000D Publication Modules that organize DMs.

```yaml
pm_generation:
  structure:
    - pmEntry:
        title: "Chapter 28 - Fuel"
        children:
          - pmEntry:
              title: "28-00 General"
              dmRefs:
                - "DMC-...-28-00-00-00A-018A-A"
                - "DMC-...-28-00-00-00A-040A-A"
          - pmEntry:
              title: "28-10 Storage"
              dmRefs:
                - "DMC-...-28-10-00-00A-040A-A"
```

### 5.3 Data Module List Generator

Generates DMLs for configuration control.

```yaml
dml_generation:
  grouping: "by_ata_chapter"
  
  content:
    - dmRef:
        dmCode: "DMC-...-28-00-00-00A-018A-A"
        issueInfo:
          issueNumber: "001"
          inWork: "00"
        dmTitle:
          techName: "Fuel System"
          infoName: "Description and operation"
```

---

## 6. Validators

### 6.1 BREX Validator

Validates Data Modules against Business Rules Exchange.

**BREX Rule Structure:**

```yaml
brex_rule:
  id: "BREX-S-001"
  category: "structure"
  severity: "error"              # error | warning
  
  rule:
    xpath: "//dmContent/procedure"
    condition: "count(preliminaryRqmts) >= 1"
    
  message: "Procedural DMs must have preliminary requirements"
  
  remediation: |
    Add <preliminaryRqmts> element before <mainProcedure>.
    Include required persons, spares, and support equipment.
```

**BREX Categories:**

| Category | Description |
|----------|-------------|
| `structure` | XML structure requirements |
| `content` | Content completeness |
| `naming` | Identifier formats |
| `reference` | Cross-references |
| `custom` | Project-specific rules |

### 6.2 Schema Validator

Validates against S1000D XML schemas.

```yaml
schema_validation:
  schema_version: "S1000D_5.0"
  schema_path: "schemas/s1000d/5.0/"
  
  checks:
    - well_formed_xml: true
    - valid_against_schema: true
    - namespace_correct: true
```

### 6.3 Trace Validator

Validates traceability completeness.

```yaml
trace_validation:
  requirements:
    min_coverage: 100            # Percentage
    all_inputs_traced: true
    no_orphan_outputs: true
    
  checks:
    - every input has ≥1 output
    - every output has ≥1 input
    - no circular references
```

---

## 7. Templates

### 7.1 S1000D Template Structure

Templates provide the XML skeleton for generated artifacts.

**Procedural DM Template:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!--
  S1000D Procedural Data Module Template
  ASIGT v2.0.0
-->
<dmodule xmlns="http://www.s1000d.org/S1000D_5-0">
  <identAndStatusSection>
    <dmAddress>
      <dmIdent>
        <dmCode 
          modelIdentCode="${dmc.modelIdentCode}"
          systemDiffCode="${dmc.systemDiffCode}"
          systemCode="${dmc.systemCode}"
          subSystemCode="${dmc.subSystemCode}"
          subSubSystemCode="${dmc.subSubSystemCode}"
          assyCode="${dmc.assyCode}"
          disassyCode="${dmc.disassyCode}"
          disassyCodeVariant="${dmc.disassyCodeVariant}"
          infoCode="${dmc.infoCode}"
          infoCodeVariant="${dmc.infoCodeVariant}"
          itemLocationCode="${dmc.itemLocationCode}"/>
        <language languageIsoCode="${language.code}" countryIsoCode="${language.country}"/>
        <issueInfo issueNumber="${issue.number}" inWork="${issue.inWork}"/>
      </dmIdent>
      <dmAddressItems>
        <issueDate year="${date.year}" month="${date.month}" day="${date.day}"/>
        <dmTitle>
          <techName>${title.techName}</techName>
          <infoName>${title.infoName}</infoName>
        </dmTitle>
      </dmAddressItems>
    </dmAddress>
    <dmStatus>
      <security securityClassification="${security.classification}"/>
      <responsiblePartnerCompany>
        <enterpriseName>${organization.name}</enterpriseName>
      </responsiblePartnerCompany>
      <originator>
        <enterpriseName>${organization.name}</enterpriseName>
      </originator>
      <applic>
        <displayText>
          <simplePara>${applicability.text}</simplePara>
        </displayText>
      </applic>
      <brexDmRef>
        <dmRef>
          <dmRefIdent>
            <dmCode ${brex.dmCode}/>
          </dmRefIdent>
        </dmRef>
      </brexDmRef>
      <qualityAssurance>
        <unverified/>
      </qualityAssurance>
    </dmStatus>
  </identAndStatusSection>
  
  <content>
    <procedure>
      <preliminaryRqmts>
        <!-- ${foreach:prelim.items} -->
        <reqCondGroup>
          <reqCond>
            <reqCondNoRef>
              <reqCond>${item.condition}</reqCond>
            </reqCondNoRef>
          </reqCond>
        </reqCondGroup>
        <!-- ${endforeach} -->
        
        <reqSupportEquips>
          <!-- ${foreach:support.equipment} -->
          <supportEquipDescrGroup>
            <supportEquipDescr>
              <name>${equip.name}</name>
              <shortName>${equip.shortName}</shortName>
            </supportEquipDescr>
          </supportEquipDescrGroup>
          <!-- ${endforeach} -->
        </reqSupportEquips>
        
        <reqSupplies>
          <!-- ${foreach:supplies} -->
          <supplyDescrGroup>
            <supplyDescr>
              <name>${supply.name}</name>
            </supplyDescr>
          </supplyDescrGroup>
          <!-- ${endforeach} -->
        </reqSupplies>
        
        <reqSpares>
          <!-- ${foreach:spares} -->
          <spareDescrGroup>
            <spareDescr>
              <name>${spare.name}</name>
              <shortName>${spare.partNumber}</shortName>
            </spareDescr>
          </spareDescrGroup>
          <!-- ${endforeach} -->
        </reqSpares>
        
        <reqSafety>
          <!-- ${foreach:warnings} -->
          <safetyRqmts>
            <warning>
              <warningAndCautionPara>${warning.text}</warningAndCautionPara>
            </warning>
          </safetyRqmts>
          <!-- ${endforeach} -->
        </reqSafety>
      </preliminaryRqmts>
      
      <mainProcedure>
        <!-- ${foreach:steps} -->
        <proceduralStep>
          <para>${step.text}</para>
          <!-- ${if:step.hasSubsteps} -->
          <!-- ${foreach:step.substeps} -->
          <proceduralStep>
            <para>${substep.text}</para>
          </proceduralStep>
          <!-- ${endforeach} -->
          <!-- ${endif} -->
        </proceduralStep>
        <!-- ${endforeach} -->
      </mainProcedure>
      
      <closeRqmts>
        <reqCondGroup>
          <!-- ${foreach:closeout.conditions} -->
          <reqCond>
            <reqCondNoRef>
              <reqCond>${condition.text}</reqCond>
            </reqCondNoRef>
          </reqCond>
          <!-- ${endforeach} -->
        </reqCondGroup>
      </closeRqmts>
    </procedure>
  </content>
</dmodule>
```

---

## 8. Mapping Rules

### 8.1 Mapping Structure

Mapping rules define how source fields transform to target fields.

```yaml
# mapping/task_to_dm.yaml

mapping:
  name: "Maintenance Task to Procedural DM"
  version: "1.0.0"
  
  source:
    type: "maintenance_task"
    schema: "schemas/maintenance_task.yaml"
    
  target:
    type: "S1000D_DM"
    template: "dm_procedural.xml"
    
  field_mappings:
    # Direct mappings
    - source: "task.id"
      target: "_meta.source_id"
      transform: "direct"
      
    - source: "task.title"
      target: "dmTitle.techName"
      transform: "direct"
      
    - source: "task.taskType"
      target: "dmCode.infoCode"
      transform: "lookup"
      lookup_table:
        "inspection": "040"
        "removal": "520"
        "installation": "720"
        "test": "300"
        "servicing": "200"
        
    # Computed mappings
    - source: "task.ata.chapter"
      target: "dmCode.systemCode"
      transform: "format"
      format: "%02d"
      
    # Array mappings
    - source: "task.steps[]"
      target: "mainProcedure.proceduralStep[]"
      transform: "iterate"
      item_mapping:
        - source: "step.instruction"
          target: "para"
        - source: "step.substeps[]"
          target: "proceduralStep[]"
          
    # Conditional mappings
    - source: "task.warnings[]"
      target: "reqSafety.warning[]"
      condition: "length(source) > 0"
      transform: "iterate"
      item_mapping:
        - source: "warning.text"
          target: "warningAndCautionPara"
```

---

## 9. Run Artifacts

### 9.1 Archive Structure

Every ASIGT execution creates an immutable archive:

```
ASIGT/runs/
└── 20260121-1430__KITDM-CTR-LM-CSDB_ATA28/
    ├── INPUT_MANIFEST.json      # What was consumed
    ├── CONTEXT.json             # Execution context from ASIT
    ├── OUTPUT_MANIFEST.json     # What was produced
    ├── TRACE_MATRIX.csv         # Input→output relationships
    ├── VALIDATION_REPORT.json   # BREX/schema/trace results
    ├── METRICS.json             # Performance data
    └── LOG.txt                  # Detailed execution log
```

### 9.2 Artifact Schemas

**INPUT_MANIFEST.json:**

```json
{
  "manifest_version": "1.0.0",
  "run_id": "20260121-1430__KITDM-CTR-LM-CSDB_ATA28",
  "contract_id": "KITDM-CTR-LM-CSDB_ATA28",
  "baseline_id": "FBL-2026-Q1-003",
  "timestamp": "2026-01-21T14:30:00Z",
  "inputs": [
    {
      "id": "requirements:REQ-ATA28-001",
      "path": "KDB/LM/SSOT/PLM/LC02_.../REQ-ATA28-001.yaml",
      "type": "requirement",
      "hash_sha256": "a1b2c3d4e5f6...",
      "size_bytes": 2048,
      "modified": "2026-01-15T10:00:00Z"
    }
  ],
  "summary": {
    "total_inputs": 47,
    "total_size_bytes": 156789,
    "input_types": {
      "requirement": 15,
      "maintenance_task": 25,
      "safety_analysis": 5,
      "icn": 2
    }
  }
}
```

**TRACE_MATRIX.csv:**

```csv
source_id,source_path,source_hash,source_type,target_id,target_path,target_hash,target_type,link_type,transform_rule,timestamp
REQ-ATA28-001,KDB/.../REQ-ATA28-001.yaml,sha256:a1b2...,requirement,DMC-HJ1-A-28-00-00-00A-018A-A,IDB/.../DMC-HJ1-A-28-00-00-00A-018A-A.xml,sha256:e5f6...,data_module,transforms,requirement_to_dm:v1.0.0,2026-01-21T14:32:15Z
TASK-ATA28-001,IDB/.../TASK-ATA28-001.yaml,sha256:c3d4...,maintenance_task,DMC-HJ1-A-28-10-00-00A-040A-A,IDB/.../DMC-HJ1-A-28-10-00-00A-040A-A.xml,sha256:g7h8...,data_module,transforms,task_to_dm:v1.0.0,2026-01-21T14:32:18Z
```

**VALIDATION_REPORT.json:**

```json
{
  "report_version": "1.0.0",
  "run_id": "20260121-1430__KITDM-CTR-LM-CSDB_ATA28",
  "timestamp": "2026-01-21T14:35:00Z",
  "overall_status": "PASS",
  
  "brex": {
    "status": "PASS",
    "rules_applied": 847,
    "errors": 0,
    "warnings": 3,
    "details": [
      {
        "rule_id": "BREX-C-001",
        "severity": "warning",
        "artifact": "DMC-HJ1-A-28-10-00-00A-040A-A.xml",
        "message": "Recommended element 'reasonForUpdate' not present",
        "line": 45
      }
    ]
  },
  
  "schema": {
    "status": "PASS",
    "schema_version": "S1000D_5.0",
    "documents_checked": 52,
    "valid": 52,
    "invalid": 0
  },
  
  "trace": {
    "status": "PASS",
    "coverage_percent": 100.0,
    "inputs_traced": 47,
    "outputs_traced": 52,
    "orphan_inputs": 0,
    "orphan_outputs": 0
  }
}
```

---

## 10. Renderers

### 10.1 PDF Renderer

Converts CSDB content to PDF publications.

```yaml
pdf_rendering:
  input: "IDB/PUB/AMM/CSDB"
  output: "IDB/PUB/AMM/EXPORT/PDF"
  
  settings:
    page_size: "A4"
    orientation: "portrait"
    margins:
      top: "25mm"
      bottom: "25mm"
      left: "20mm"
      right: "20mm"
      
  styling:
    stylesheet: "renderers/styles/amm_pdf.xsl"
    fonts:
      body: "Arial"
      headings: "Arial Bold"
      code: "Courier"
      
  options:
    toc: true
    bookmarks: true
    hyperlinks: true
    page_numbers: true
```

### 10.2 HTML Renderer

Converts CSDB content to HTML.

```yaml
html_rendering:
  input: "IDB/PUB/AMM/CSDB"
  output: "IDB/PUB/AMM/EXPORT/HTML"
  
  settings:
    responsive: true
    single_page: false
    
  styling:
    stylesheet: "renderers/styles/amm_html.css"
    
  options:
    navigation: true
    search: true
    print_friendly: true
```

### 10.3 IETP Packager

Creates Interactive Electronic Technical Publication packages.

```yaml
ietp_packaging:
  input: "IDB/PUB/AMM/CSDB"
  output: "IDB/PUB/AMM/IETP"
  
  structure:
    app/
      viewer.html
      scripts/
      styles/
    data/
      dm/
      pm/
      icn/
    operators/
      config.yaml
      applicability.yaml
      
  viewer:
    type: "web"
    features:
      - navigation
      - search
      - bookmarks
      - applicability_filtering
      - print
```

---

## 11. Compliance Mapping

| Requirement | ASIGT Component |
|-------------|-----------------|
| S1000D Data Modules | GENERATORS, TEMPLATES |
| S1000D BREX | VALIDATORS/brex |
| S1000D Schemas | VALIDATORS/schema |
| DO-178C Traceability | TRACE_MATRIX, RUN_ARTIFACTS |
| Reproducibility | IMMUTABLE_RUNS |

---

## 12. Error Handling

### 12.1 Error Categories

| Category | Severity | Action |
|----------|----------|--------|
| Contract Invalid | FATAL | Abort, no outputs |
| Baseline Missing | FATAL | Abort, no outputs |
| Input Parse Error | ERROR | Skip artifact, continue |
| BREX Violation | ERROR/WARN | Log, flag in report |
| Schema Violation | ERROR | Log, flag in report |
| Trace Gap | ERROR | Log, flag in report |

### 12.2 Error Response

```yaml
error_response:
  on_fatal:
    - abort_execution
    - create_error_log
    - return_failed_status
    
  on_error:
    - log_error
    - continue_if_possible
    - include_in_validation_report
    
  on_warning:
    - log_warning
    - continue
    - include_in_validation_report
```

---

## 13. Glossary

| Term | Definition |
|------|------------|
| **DM** | Data Module — atomic S1000D content unit |
| **PM** | Publication Module — organizes DMs into publications |
| **DML** | Data Module List — configuration control list |
| **ICN** | Information Control Number — graphics identifier |
| **BREX** | Business Rules Exchange — validation rules |
| **ACT/PCT/CCT** | Applicability Cross-reference Tables |

---

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | ASIGT-CORE-v2.0.0 |
| **Status** | Normative |
| **Next Review** | 2027-01-01 |

---

*End of ASIGT_CORE Specification*
