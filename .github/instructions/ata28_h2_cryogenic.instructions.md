---
# =============================================================================
# BREX-DRIVEN COPILOT INSTRUCTION FILE
# ATA 28 – Hydrogen Cryogenic Fuel Systems Domain
# =============================================================================
#
# This instruction file demonstrates the BREX-driven instruction system
# for the AEROSPACEMODEL Agent. All reasoning is constrained, guided,
# and explainable through BREX rules.
#
audience: engineering
ata_domain: "ATA 28 – Hydrogen Cryogenic Fuel Systems"
authority: ASIT
baseline_required: true
contract_required: true
brex_profile: "AEROSPACEMODEL-PRJ-01"
determinism: strict
version: "1.0.0"
---

# AEROSPACEMODEL Agent Instructions: ATA 28 – Hydrogen Cryogenic Fuel Systems

> **Authority:** ASIT (Aircraft Systems Information Transponder)  
> **Determinism Level:** STRICT  
> **Compliance:** S1000D Issue 5.0, DO-160, CS-25 Special Conditions, ARP4754A, ARP4761

---

## 1. Purpose

This instruction file governs AEROSPACEMODEL Agent behavior for ATA 28 Hydrogen Cryogenic Fuel Systems domain operations. All agent reasoning is constrained by BREX decision rules. No free-form autonomy exists.

---

## 2. BREX Decision Integration

The following BREX rules MUST be evaluated before any operation:

```yaml
brex_rules:
  # Structure Rules
  - id: STRUCT-001
    condition: "ata_domain MUST exist"
    enforcement: block
    message: "H2 cryogenic fuel content requires ATA 28 domain classification"

  # Authority Rules
  - id: AUTHOR-002
    condition: "content generation requires ASIT-approved contract"
    enforcement: require_contract
    message: "Generation requires contract: KITDM-CTR-LM-CSDB_ATA28_H2"

  # Safety Rules
  - id: SAFETY-002
    condition: "if safety-related, require human approval"
    enforcement: escalate
    escalation_target: STK_SAF
    message: "H2 cryogenic safety content requires human approval"

  - id: SAFETY-H2-001
    condition: "hydrogen handling requires safety review"
    enforcement: escalate
    escalation_target: STK_SAF
    message: "Hydrogen handling procedures require safety assessment"

  - id: SAFETY-H2-002
    condition: "cryogenic temperature procedures require special warnings"
    enforcement: require_warning
    message: "Cryogenic procedures require mandatory safety warnings"

  - id: SAFETY-H2-003
    condition: "leak detection systems mandatory"
    enforcement: block
    message: "H2 leak detection systems must be documented"

  # Lifecycle Rules
  - id: LC-001
    condition: "content must be in valid lifecycle state"
    enforcement: block
    message: "Lifecycle state validation required"

  # Pipeline Rules
  - id: PIPELINE-004
    condition: "transformation must be contract-approved"
    enforcement: require_approval
    message: "Content transformation requires contract approval"
```

---

## 3. Domain Knowledge Requirements

ATA 28 – Hydrogen Cryogenic Fuel Systems domain requires specific knowledge:

### 3.1 LH₂ Fuel System Components

```yaml
lh2_systems:
  storage:
    - name: "LH₂ Primary Tank"
      ata_section: "28-11"
      description: "Main liquid hydrogen storage tank (cryogenic)"
      temperature: "-253°C (-423°F)"
      pressure: "Typically 1-6 bar"
      insulation: "Vacuum-jacketed multi-layer insulation (MLI)"
      capacity: "Variable by aircraft type"
      safety_criticality: "DAL A"
      
    - name: "LH₂ Auxiliary Tank"
      ata_section: "28-13"
      description: "Extended range cryogenic hydrogen storage"
      temperature: "-253°C (-423°F)"
      optional: true
      safety_criticality: "DAL A"
  
  distribution:
    - name: "Cryogenic Transfer Pump"
      ata_section: "28-21"
      description: "LH₂ boost and transfer pumps"
      materials: "Cryogenic-compatible alloys"
      
    - name: "Insulated Transfer Lines"
      ata_section: "28-22"
      description: "Vacuum-insulated hydrogen distribution piping"
      materials: "Stainless steel, aluminum alloys"
      
    - name: "Pressure Control System"
      ata_section: "28-23"
      description: "Tank pressurization and pressure relief"
  
  boil_off_management:
    - name: "Boil-Off Gas (BOG) Management"
      ata_section: "28-30"
      description: "Capture and management of hydrogen boil-off"
      options: ["Vent to atmosphere", "Recovery and reliquefaction", "Use in fuel cell APU"]
      
    - name: "Thermal Management"
      ata_section: "28-31"
      description: "Active and passive cooling systems"
      techniques: ["MLI insulation", "Cryocoolers", "Shield cooling"]
  
  safety_systems:
    - name: "H₂ Leak Detection"
      ata_section: "28-41"
      description: "Multi-sensor hydrogen leak detection system"
      sensor_types: ["Electrochemical", "Thermal conductivity", "Optical"]
      coverage: "All potential leak points, enclosed spaces"
      safety_criticality: "DAL A"
      
    - name: "Pressure Relief and Venting"
      ata_section: "28-42"
      description: "Over-pressure protection and emergency venting"
      safety_criticality: "DAL A"
      
    - name: "Fire Detection and Suppression"
      ata_section: "28-43"
      description: "H₂ fire detection and suppression (if required)"
      integration: "ATA 26 - Fire Protection"
```

### 3.2 Cryogenic Handling Procedures

```yaml
cryogenic_procedures:
  refueling:
    description: "LH₂ ground refueling procedures"
    safety_requirements:
      - "Personnel training on cryogenic hazards"
      - "Appropriate PPE (face shield, cryogenic gloves, apron)"
      - "Bonding and grounding"
      - "Continuous H₂ monitoring"
      - "Emergency procedures and equipment"
    
    steps:
      - "Pre-flight inspection of tank and transfer system"
      - "Connect bonding cable"
      - "Connect refueling line with cryogenic coupling"
      - "Purge system with inert gas"
      - "Initiate LH₂ transfer with flow control"
      - "Monitor tank level, pressure, and temperature"
      - "Complete transfer and disconnect"
      - "Post-refueling inspection"
  
  defueling:
    description: "LH₂ removal for maintenance"
    safety_requirements:
      - "Controlled boil-off or transfer to ground storage"
      - "Tank venting and purging"
      - "Warm-up procedures"
      - "Continuous monitoring"
  
  maintenance:
    description: "Cryogenic system maintenance"
    special_requirements:
      - "Tank warm-up before entry (if required)"
      - "Inert gas purging"
      - "Leak testing after maintenance"
      - "Vacuum insulation integrity checks"
      - "Special tools for cryogenic components"
```

### 3.3 Material Compatibility

```yaml
materials:
  cryogenic_compatible:
    - material: "Stainless Steel (304, 316)"
      application: "Tanks, piping, fittings"
      temperature_range: "-253°C to ambient"
      
    - material: "Aluminum Alloys (5083, 6061)"
      application: "Structural components, piping"
      temperature_range: "-253°C to ambient"
      notes: "Good thermal conductivity, lightweight"
      
    - material: "Inconel (718, 625)"
      application: "High-stress components, valves"
      temperature_range: "-253°C to high temperature"
      
    - material: "PTFE (Teflon)"
      application: "Seals, gaskets"
      temperature_range: "-253°C to 260°C"
  
  avoid:
    - material: "Carbon Steel"
      reason: "Brittle at cryogenic temperatures"
      
    - material: "Standard Elastomers"
      reason: "Lose elasticity at cryogenic temperatures"
```

### 3.4 Failure Modes (ARP4761)

```yaml
failure_modes:
  - mode: "LH₂ tank leak (major)"
    severity: "Catastrophic"
    probability: "< 1E-9 per flight hour"
    mitigation: "Multiple barrier design, leak detection, isolation valves, emergency venting"
    
  - mode: "Boil-off excessive (loss of fuel)"
    severity: "Hazardous"
    probability: "< 1E-7 per flight hour"
    mitigation: "Thermal management, boil-off capture, redundant insulation"
    
  - mode: "Pressure relief valve failure"
    severity: "Hazardous"
    probability: "< 1E-7 per flight hour"
    mitigation: "Redundant pressure relief, burst discs, continuous monitoring"
    
  - mode: "H₂ leak (minor, detectable)"
    severity: "Major"
    probability: "< 1E-5 per flight hour"
    mitigation: "Leak detection, ventilation, isolation, crew alerting"
    
  - mode: "Cryogenic burn (ground personnel)"
    severity: "Major (ground safety)"
    probability: "< 1E-5 per operation"
    mitigation: "PPE requirements, training, emergency showers, safety procedures"
    
  - mode: "H₂ ignition (fire/explosion)"
    severity: "Catastrophic"
    probability: "< 1E-9 per flight hour"
    mitigation: "Leak prevention, ventilation, ignition source elimination, bonding/grounding"
```

---

## 4. Allowed Operations

Operations permitted under BREX governance:

```yaml
allowed_operations:
  - operation: "generate_dm_if"
    brex_rules: ["AUTHOR-002", "STRUCT-001"]
    description: "Generate Data Module for ATA 28 H2 Cryogenic"
    contract: "KITDM-CTR-LM-CSDB_ATA28_H2"
    
  - operation: "produce_publication_if"
    brex_rules: ["STRUCT-001", "BREX-001"]
    description: "Produce AMM/SRM content for H2 cryogenic fuel systems"
    output_target: "IDB/PUB/AMM/CSDB/ATA28_H2"
    
  - operation: "transform_content_if"
    brex_rules: ["PIPELINE-004", "TRACE-001"]
    description: "Transform H2 cryogenic data to S1000D"
    pipeline: "pipelines/ata28_h2_pipeline.yaml"
    
  - operation: "validate_h2_safety_content_if"
    brex_rules: ["SAFETY-002", "SAFETY-H2-001", "SAFETY-H2-002", "SAFETY-H2-003"]
    description: "Validate H2 cryogenic safety content"
    escalation_required: true
```

---

## 5. Prohibited Operations

Operations NOT permitted under any circumstance:

```yaml
prohibited_operations:
  - operation: "generate_content_without_contract"
    violation: "CRITICAL"
    message: "Cannot generate ATA 28 H2 content without KITDM-CTR-LM-CSDB_ATA28_H2"
    
  - operation: "create_structure_without_ata_domain"
    violation: "ERROR"
    message: "Cannot create content without ATA 28 H2 domain classification"
    
  - operation: "bypass_lifecycle_states"
    violation: "ERROR"
    message: "Cannot bypass LC04 design review for H2 cryogenic systems"
    
  - operation: "auto_invent_h2_safety_content"
    violation: "CRITICAL"
    message: "Cannot auto-generate H2 safety warnings without STK_SAF approval"
    
  - operation: "omit_cryogenic_warnings"
    violation: "CRITICAL"
    message: "Cannot omit cryogenic temperature warnings in procedures"
    
  - operation: "skip_leak_detection_docs"
    violation: "CRITICAL"
    message: "Cannot omit leak detection system documentation"
```

---

## 6. S1000D DMC Constraints

Data Module Code constraints for ATA 28 H2 Cryogenic:

```yaml
dmc_constraints:
  model_ident_code: "${MODEL_IDENT_CODE}"  # Project-specific
  system_diff_code: "A"
  system_code: "28"
  
  sub_systems:
    - sub_system: "00"
      description: "H2 Cryogenic Fuel - General"
    - sub_system: "11"
      description: "LH₂ Storage Tanks"
    - sub_system: "21"
      description: "Cryogenic Transfer System"
    - sub_system: "30"
      description: "Boil-Off Management"
    - sub_system: "31"
      description: "Thermal Management"
    - sub_system: "41"
      description: "H₂ Leak Detection"
    - sub_system: "42"
      description: "Pressure Relief and Venting"
      
  info_codes:
    descriptive: ["000", "001", "040", "041", "042"]
    procedural: ["100", "200", "300", "400", "500", "510", "520", "600", "700"]
    parts: ["941", "942"]
```

---

## 7. Special Handling: Hydrogen Cryogenic Systems

For hydrogen cryogenic fuel systems:

```yaml
h2_cryogenic_requirements:
  mandatory_warnings:
    - type: "EXPLOSION HAZARD"
      placement: "Before any H2 procedure"
      content: "DANGER: Hydrogen is extremely flammable. Concentrations of 4-75% in air are explosive. Ensure adequate ventilation. No open flames or ignition sources within 15 meters."
      
    - type: "CRYOGENIC HAZARD"
      placement: "Before LH₂ handling"
      content: "DANGER: Liquid hydrogen at -253°C (-423°F). Contact causes severe cryogenic burns and frostbite. Wear face shield, cryogenic gloves, and protective apron. Emergency shower and eyewash must be accessible."
      
    - type: "LEAK DETECTION"
      placement: "During H2 system work"
      content: "WARNING: Use H2-rated leak detection equipment. Hydrogen leaks are invisible and odorless. Continuous monitoring required."
      
    - type: "ASPHYXIATION HAZARD"
      placement: "Before entering enclosed spaces"
      content: "DANGER: Hydrogen displaces oxygen. Enclosed space entry requires oxygen monitoring and ventilation. Follow confined space procedures."
  
  special_procedures:
    - "Bonding and grounding required for all H2 operations"
    - "No open flames or ignition sources within 15m"
    - "H2-rated tools only (non-sparking)"
    - "Continuous H2 monitoring during all operations"
    - "Emergency procedures posted and personnel trained"
    - "Fire extinguishers rated for hydrogen fires"
    
  escalation_required:
    trigger: "Any H2 cryogenic content generation"
    escalation_target: "STK_SAF"
    approval_timeout: "72 hours"
    
  special_conditions:
    - condition: "SC-28-H2-001"
      title: "Hydrogen Storage and Distribution"
      description: "Special conditions for hydrogen fuel storage and distribution systems"
      
    - condition: "SC-28-CRYO-002"
      title: "Cryogenic Temperature Handling"
      description: "Special conditions for systems operating at cryogenic temperatures"
```

---

## 8. Audit Log Requirements

All operations MUST be logged:

```yaml
audit_requirements:
  format: |
    {timestamp} | RULE {rule_id} | {rule_name} | {status} | {context}
    
  required_entries:
    - "Contract validation"
    - "ATA domain verification"
    - "Safety impact assessment"
    - "BREX compliance check"
    - "Trace coverage validation"
    - "H2 warning inclusion"
    - "Cryogenic warning inclusion"
    - "Leak detection documentation check"
    
  retention: "7 years minimum (certification)"
```

---

## 9. Escalation Procedures

When human approval is required:

```yaml
escalation_procedures:
  h2_safety_content:
    trigger: "SAFETY-H2-001, SAFETY-H2-002, or SAFETY-H2-003"
    escalation_target: "STK_SAF"
    required_review:
      - "Hydrogen handling procedures"
      - "Cryogenic temperature warnings"
      - "Leak detection system documentation"
      - "Emergency procedures"
    timeout: "72 hours"
    
  baseline_modification:
    trigger: "BL-002"
    escalation_target: "CCB"
    required_approval:
      - "ECR submission"
      - "Impact assessment"
      - "CCB decision"
    timeout: "5 business days"
    
  undefined_condition:
    trigger: "No matching BREX rule"
    escalation_target: "STK_CM"
    action: "HALT and wait for rule definition"
```

---

## 10. Determinism Guarantee

This instruction file ensures:

- ✅ **No unconstrained LLM freedom**
- ✅ **No hallucination**
- ✅ **Full reproducibility**
- ✅ **All outputs explainable and validated**
- ✅ **Only contract-approved transformations**

If the agent reaches an unruled situation:
→ **It halts**  
→ **Raises a BREX Undefined Condition Violation**

---

## 11. Related Documents

| Document | Reference |
|----------|-----------|
| ASIT Core Specification | ASIT/ASIT_CORE.md |
| Master BREX Authority | ASIT/GOVERNANCE/master_brex_authority.yaml |
| S1000D 5.0 Default BREX | ASIGT/brex/S1000D_5.0_DEFAULT.yaml |
| ATA 28 H2 Contract | ASIT/CONTRACTS/active/KITDM-CTR-LM-CSDB_ATA28_H2.yaml |
| Project BREX | ASIGT/brex/project_brex.yaml |
| T-Subdomain LC Activation | lifecycle/T_SUBDOMAIN_LC_ACTIVATION.yaml |
| ATA 28 Standard Fuel Instructions | .github/instructions/ata28_fuel.instructions.md |

---

*End of ATA 28 H2 Cryogenic BREX-Driven Instructions*
