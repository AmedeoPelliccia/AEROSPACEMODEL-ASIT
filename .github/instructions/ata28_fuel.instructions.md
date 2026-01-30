---
# =============================================================================
# BREX-DRIVEN COPILOT INSTRUCTION FILE
# ATA 28 – Fuel System Domain
# =============================================================================
#
# This instruction file demonstrates the BREX-driven instruction system
# for the AEROSPACEMODEL Agent. All reasoning is constrained, guided,
# and explainable through BREX rules.
#
audience: engineering
ata_domain: "ATA 28 – Fuel"
authority: ASIT
baseline_required: true
contract_required: true
brex_profile: "AEROSPACEMODEL-PRJ-01"
determinism: strict
version: "1.0.0"
---

# AEROSPACEMODEL Agent Instructions: ATA 28 – Fuel System

> **Authority:** ASIT (Aircraft Systems Information Transponder)  
> **Determinism Level:** STRICT  
> **Compliance:** S1000D Issue 5.0, DO-178C, ARP4761

---

## 1. Purpose

This instruction file governs AEROSPACEMODEL Agent behavior for ATA 28 (Fuel) domain operations. All agent reasoning is constrained by BREX decision rules. No free-form autonomy exists.

---

## 2. BREX Decision Integration

The following BREX rules MUST be evaluated before any operation:

```yaml
brex_rules:
  # Structure Rules
  - id: STRUCT-001
    condition: "ata_domain MUST exist"
    enforcement: block
    message: "Fuel system content requires ATA 28 domain classification"

  # Authority Rules
  - id: AUTHOR-002
    condition: "content generation requires ASIT-approved contract"
    enforcement: require_contract
    message: "Generation requires contract: KITDM-CTR-LM-CSDB_ATA28"

  # Safety Rules
  - id: SAFETY-002
    condition: "if safety-related, require human approval"
    enforcement: escalate
    escalation_target: STK_SAF
    message: "Fuel system safety content requires human approval"

  - id: SAFETY-FUEL-001
    condition: "fuel handling procedures require safety review"
    enforcement: escalate
    escalation_target: STK_SAF
    message: "Fuel handling safety assessment required"

  - id: SAFETY-FUEL-002
    condition: "hydrogen system procedures require special warnings"
    enforcement: require_warning
    message: "H2 procedures require mandatory safety warnings"

  # Pipeline Rules
  - id: PIPELINE-004
    condition: "transformation must be contract-approved"
    enforcement: require_approval
    message: "Content transformation requires contract approval"
```

---

## 3. Domain Knowledge Requirements

ATA 28 – Fuel domain requires specific knowledge:

### 3.1 Fuel System Components

```yaml
fuel_systems:
  storage:
    - name: "Center Tank"
      ata_section: "28-11"
      description: "Main fuselage fuel storage"
      capacity: "Variable by aircraft type"
      
    - name: "Wing Tank (LH/RH)"
      ata_section: "28-12"
      description: "Integral wing fuel storage"
      capacity: "Variable by aircraft type"
      
    - name: "Auxiliary Tank"
      ata_section: "28-13"
      description: "Extended range fuel storage"
      optional: true

  distribution:
    - name: "Fuel Pump"
      ata_section: "28-21"
      description: "Boost and transfer pumps"
      
    - name: "Fuel Lines"
      ata_section: "28-22"
      description: "Fuel distribution piping"
      
    - name: "Crossfeed System"
      ata_section: "28-23"
      description: "Tank interconnection system"

  indication:
    - name: "Fuel Quantity Indication"
      ata_section: "28-41"
      description: "Tank level measurement and display"
      
    - name: "Fuel Temperature"
      ata_section: "28-42"
      description: "Fuel temperature monitoring"
```

### 3.2 Alternative Fuels

```yaml
alternative_fuels:
  - type: "Sustainable Aviation Fuel (SAF)"
    ata_reference: "28-00"
    description: "Drop-in replacement fuels"
    compatibility: "Requires fuel system validation"
    
  - type: "Hydrogen (H2)"
    ata_reference: "28-00, 73-00"
    description: "Cryogenic or compressed hydrogen"
    special_requirements:
      - "Cryogenic handling procedures"
      - "Leak detection systems"
      - "Special material requirements"
      - "Explosion prevention measures"
```

### 3.3 Failure Modes (ARP4761)

```yaml
failure_modes:
  - mode: "Fuel starvation"
    severity: "Catastrophic"
    probability: "< 1E-9 per flight hour"
    mitigation: "Redundant feed, low level warning"
    
  - mode: "Fuel leak (major)"
    severity: "Hazardous"
    probability: "< 1E-7 per flight hour"
    mitigation: "Leak detection, isolation valves"
    
  - mode: "Fuel imbalance"
    severity: "Major"
    probability: "< 1E-5 per flight hour"
    mitigation: "CG monitoring, crossfeed capability"
    
  - mode: "Contaminated fuel"
    severity: "Major"
    probability: "< 1E-5 per flight hour"
    mitigation: "Fuel filter, water drain, sampling"
```

---

## 4. Allowed Operations

Operations permitted under BREX governance:

```yaml
allowed_operations:
  - operation: "generate_dm_if"
    brex_rules: ["AUTHOR-002", "STRUCT-001"]
    description: "Generate Data Module for ATA 28"
    contract: "KITDM-CTR-LM-CSDB_ATA28"
    
  - operation: "produce_publication_if"
    brex_rules: ["STRUCT-001", "BREX-001"]
    description: "Produce AMM/SRM content for fuel system"
    output_target: "IDB/PUB/AMM/CSDB/ATA28"
    
  - operation: "transform_content_if"
    brex_rules: ["PIPELINE-004", "TRACE-001"]
    description: "Transform engineering data to S1000D"
    pipeline: "pipelines/ata28_pipeline.yaml"
    
  - operation: "validate_safety_content_if"
    brex_rules: ["SAFETY-002", "SAFETY-FUEL-001"]
    description: "Validate safety-critical fuel content"
    escalation_required: true
```

---

## 5. Prohibited Operations

Operations NOT permitted under any circumstance:

```yaml
prohibited_operations:
  - operation: "generate_content_without_contract"
    violation: "CRITICAL"
    message: "Cannot generate ATA 28 content without KITDM-CTR-LM-CSDB_ATA28"
    
  - operation: "create_structure_without_ata_domain"
    violation: "ERROR"
    message: "Cannot create content without ATA 28 domain classification"
    
  - operation: "bypass_lifecycle_states"
    violation: "ERROR"
    message: "Cannot bypass LC04 design review for fuel systems"
    
  - operation: "auto_invent_safety_content"
    violation: "CRITICAL"
    message: "Cannot auto-generate fuel safety warnings without STK_SAF approval"
    
  - operation: "omit_hydrogen_warnings"
    violation: "CRITICAL"
    message: "Cannot omit H2 safety warnings in hydrogen-related procedures"
```

---

## 6. S1000D DMC Constraints

Data Module Code constraints for ATA 28:

```yaml
dmc_constraints:
  model_ident_code: "${MODEL_IDENT_CODE}"  # Project-specific
  system_diff_code: "A"
  system_code: "28"
  
  sub_systems:
    - sub_system: "00"
      description: "Fuel - General"
    - sub_system: "10"
      description: "Storage"
    - sub_system: "20"
      description: "Distribution"
    - sub_system: "30"
      description: "Dump"
    - sub_system: "40"
      description: "Indicating"
      
  info_codes:
    descriptive: ["000", "001", "040", "041", "042"]
    procedural: ["100", "200", "300", "400", "500", "510", "520", "600", "700"]
    parts: ["941", "942"]
```

---

## 7. Special Handling: Hydrogen Systems

For hydrogen-based fuel systems (SAF-H2, LH2):

```yaml
hydrogen_requirements:
  mandatory_warnings:
    - type: "EXPLOSION HAZARD"
      placement: "Before any H2 procedure"
      content: "Hydrogen is extremely flammable. Ensure adequate ventilation."
      
    - type: "CRYOGENIC HAZARD"
      placement: "Before LH2 handling"
      content: "Liquid hydrogen at -253°C. Use appropriate PPE."
      
    - type: "LEAK DETECTION"
      placement: "During H2 system work"
      content: "Use H2-rated leak detection equipment."

  special_procedures:
    - "Bonding and grounding required"
    - "No open flames within 15m"
    - "H2-rated tools only"
    - "Continuous H2 monitoring"
    
  escalation_required:
    trigger: "Any H2-related content generation"
    escalation_target: "STK_SAF"
    approval_timeout: "72 hours"
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
    - "H2 warning inclusion (if applicable)"
    
  retention: "7 years minimum (certification)"
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
| ATA 28 Contract | ASIT/CONTRACTS/active/KITDM-CTR-LM-CSDB_ATA28.yaml |
| Project BREX | ASIGT/brex/project_brex.yaml |

---

*End of ATA 28 BREX-Driven Instructions*
