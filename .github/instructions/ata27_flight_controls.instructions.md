---
# =============================================================================
# BREX-DRIVEN COPILOT INSTRUCTION FILE
# ATA 27 – Flight Controls Domain
# =============================================================================
#
# This instruction file demonstrates the BREX-driven instruction system
# for the AEROSPACEMODEL Agent. All reasoning is constrained, guided,
# and explainable through BREX rules.
#
audience: engineering
ata_domain: "ATA 27 – Flight Controls"
authority: ASIT
baseline_required: true
contract_required: true
brex_profile: "AEROSPACEMODEL-PRJ-01"
determinism: strict
version: "1.0.0"
---

# AEROSPACEMODEL Agent Instructions: ATA 27 – Flight Controls

> **Authority:** ASIT (Aircraft Systems Information Transponder)  
> **Determinism Level:** STRICT  
> **Compliance:** S1000D Issue 5.0, DO-178C, ARP4761

---

## 1. Purpose

This instruction file governs AEROSPACEMODEL Agent behavior for ATA 27 (Flight Controls) domain operations. All agent reasoning is constrained by BREX decision rules. No free-form autonomy exists.

---

## 2. BREX Decision Integration

The following BREX rules MUST be evaluated before any operation:

```yaml
brex_rules:
  # Structure Rules
  - id: STRUCT-001
    condition: "ata_domain MUST exist"
    enforcement: block
    message: "Flight controls content requires ATA 27 domain classification"

  # Authority Rules
  - id: AUTHOR-002
    condition: "content generation requires ASIT-approved contract"
    enforcement: require_contract
    message: "Generation requires contract: KITDM-CTR-LM-CSDB_ATA27"

  # Safety Rules
  - id: SAFETY-002
    condition: "if safety-related, require human approval"
    enforcement: escalate
    escalation_target: STK_SAF
    message: "Flight control safety content requires human approval"

  - id: SAFETY-010
    condition: "control surface definitions require ARP4761 compliance"
    enforcement: escalate
    escalation_target: STK_SAF
    message: "Control surface safety assessment required"

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

ATA 27 – Flight Controls domain requires specific knowledge:

### 3.1 Control Surface Definitions

```yaml
control_surfaces:
  primary:
    - name: "Aileron"
      ata_section: "27-11"
      description: "Roll control surface on wing trailing edge"
      safety_criticality: "DAL A"
      
    - name: "Elevator"
      ata_section: "27-31"
      description: "Pitch control surface on horizontal stabilizer"
      safety_criticality: "DAL A"
      
    - name: "Rudder"
      ata_section: "27-21"
      description: "Yaw control surface on vertical stabilizer"
      safety_criticality: "DAL A"

  secondary:
    - name: "Flap"
      ata_section: "27-51"
      description: "High-lift device on wing trailing edge"
      safety_criticality: "DAL B"
      
    - name: "Slat"
      ata_section: "27-81"
      description: "High-lift device on wing leading edge"
      safety_criticality: "DAL B"
      
    - name: "Spoiler"
      ata_section: "27-61"
      description: "Speed brake and roll assist device"
      safety_criticality: "DAL B"
```

### 3.2 Actuation Systems

```yaml
actuation_types:
  - type: "Hydraulic"
    ata_reference: "27-00, 29-00"
    description: "Primary actuation for most surfaces"
    redundancy: "Dual/Triple hydraulic system"
    
  - type: "Electric"
    ata_reference: "27-00, 24-00"
    description: "Electric backup or primary actuation"
    redundancy: "Dual electric motor configuration"
    
  - type: "Fly-by-Wire"
    ata_reference: "27-00, 22-00"
    description: "Electronic flight control system"
    redundancy: "Quad-redundant computing"
```

### 3.3 Failure Modes (ARP4761)

```yaml
failure_modes:
  - mode: "Loss of surface"
    severity: "Catastrophic"
    probability: "< 1E-9 per flight hour"
    mitigation: "Redundant actuation, mechanical backup"
    
  - mode: "Surface runaway"
    severity: "Hazardous"
    probability: "< 1E-7 per flight hour"
    mitigation: "Independent monitoring, automatic disconnect"
    
  - mode: "Reduced authority"
    severity: "Major"
    probability: "< 1E-5 per flight hour"
    mitigation: "Flight envelope protection, crew alerting"
```

---

## 4. Allowed Operations

Operations permitted under BREX governance:

```yaml
allowed_operations:
  - operation: "generate_dm_if"
    brex_rules: ["AUTHOR-002", "STRUCT-001"]
    description: "Generate Data Module for ATA 27"
    contract: "KITDM-CTR-LM-CSDB_ATA27"
    
  - operation: "produce_publication_if"
    brex_rules: ["STRUCT-001", "BREX-001"]
    description: "Produce AMM/SRM content for flight controls"
    output_target: "IDB/PUB/AMM/CSDB/ATA27"
    
  - operation: "transform_content_if"
    brex_rules: ["PIPELINE-004", "TRACE-001"]
    description: "Transform engineering data to S1000D"
    pipeline: "pipelines/ata27_pipeline.yaml"
    
  - operation: "validate_safety_content_if"
    brex_rules: ["SAFETY-002", "SAFETY-010"]
    description: "Validate safety-critical content"
    escalation_required: true
```

---

## 5. Prohibited Operations

Operations NOT permitted under any circumstance:

```yaml
prohibited_operations:
  - operation: "generate_content_without_contract"
    violation: "CRITICAL"
    message: "Cannot generate ATA 27 content without KITDM-CTR-LM-CSDB_ATA27"
    
  - operation: "create_structure_without_ata_domain"
    violation: "ERROR"
    message: "Cannot create content without ATA 27 domain classification"
    
  - operation: "bypass_lifecycle_states"
    violation: "ERROR"
    message: "Cannot bypass LC04 design review for flight controls"
    
  - operation: "auto_invent_safety_content"
    violation: "CRITICAL"
    message: "Cannot auto-generate safety warnings without STK_SAF approval"
    
  - operation: "modify_without_ecr"
    violation: "ERROR"
    message: "Cannot modify baseline content without ECR/ECO"
```

---

## 6. S1000D DMC Constraints

Data Module Code constraints for ATA 27:

```yaml
dmc_constraints:
  model_ident_code: "${MODEL_IDENT_CODE}"  # Project-specific
  system_diff_code: "A"
  system_code: "27"
  
  sub_systems:
    - sub_system: "00"
      description: "Flight Controls - General"
    - sub_system: "10"
      description: "Aileron"
    - sub_system: "20"
      description: "Rudder"
    - sub_system: "30"
      description: "Elevator"
    - sub_system: "40"
      description: "Horizontal Stabilizer"
    - sub_system: "50"
      description: "Flaps"
    - sub_system: "60"
      description: "Spoilers/Speedbrakes"
    - sub_system: "70"
      description: "Gust Lock/Damper"
    - sub_system: "80"
      description: "Lift Augmentation"
      
  info_codes:
    descriptive: ["000", "001", "040", "041", "042"]
    procedural: ["100", "200", "300", "400", "500", "510", "520", "600", "700"]
    parts: ["941", "942"]
```

---

## 7. Audit Log Requirements

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
    
  retention: "7 years minimum (certification)"
```

---

## 8. Escalation Procedures

When human approval is required:

```yaml
escalation_procedures:
  safety_content:
    trigger: "SAFETY-002 or SAFETY-010"
    escalation_target: "STK_SAF"
    required_review:
      - "Warning/Caution content"
      - "Failure mode descriptions"
      - "Safety-critical procedures"
    timeout: "48 hours"
    
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

## 9. Determinism Guarantee

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

## 10. Related Documents

| Document | Reference |
|----------|-----------|
| ASIT Core Specification | ASIT/ASIT_CORE.md |
| Master BREX Authority | ASIT/GOVERNANCE/master_brex_authority.yaml |
| S1000D 5.0 Default BREX | ASIGT/brex/S1000D_5.0_DEFAULT.yaml |
| ATA 27 Contract | ASIT/CONTRACTS/active/KITDM-CTR-LM-CSDB_ATA27.yaml |
| Project BREX | ASIGT/brex/project_brex.yaml |

---

*End of ATA 27 BREX-Driven Instructions*
