---
# =============================================================================
# BREX-DRIVEN COPILOT INSTRUCTION FILE
# ATA 71 – Fuel Cell Power Plant Domain
# =============================================================================
#
# This instruction file demonstrates the BREX-driven instruction system
# for the AEROSPACEMODEL Agent. All reasoning is constrained, guided,
# and explainable through BREX rules.
#
audience: engineering
ata_domain: "ATA 71 – Fuel Cell Power Plant"
authority: ASIT
baseline_required: true
contract_required: true
brex_profile: "AEROSPACEMODEL-PRJ-01"
determinism: strict
version: "1.0.0"
---

# AEROSPACEMODEL Agent Instructions: ATA 71 – Fuel Cell Power Plant

> **Authority:** ASIT (Aircraft Systems Information Transponder)  
> **Determinism Level:** STRICT  
> **Compliance:** S1000D Issue 5.0, DO-160, CS-25, ARP4754A, ARP4761

---

## 1. Purpose

This instruction file governs AEROSPACEMODEL Agent behavior for ATA 71 (Fuel Cell Power Plant) domain operations. All agent reasoning is constrained by BREX decision rules. No free-form autonomy exists.

---

## 2. BREX Decision Integration

The following BREX rules MUST be evaluated before any operation:

```yaml
brex_rules:
  # Structure Rules
  - id: STRUCT-001
    condition: "ata_domain MUST exist"
    enforcement: block
    message: "Fuel cell content requires ATA 71 domain classification"

  # Authority Rules
  - id: AUTHOR-002
    condition: "content generation requires ASIT-approved contract"
    enforcement: require_contract
    message: "Generation requires contract: KITDM-CTR-LM-CSDB_ATA71"

  # Safety Rules
  - id: SAFETY-002
    condition: "if safety-related, require human approval"
    enforcement: escalate
    escalation_target: STK_SAF
    message: "Fuel cell safety content requires human approval"

  - id: SAFETY-FC-001
    condition: "fuel cell stack safety requires human approval"
    enforcement: escalate
    escalation_target: STK_SAF
    message: "Fuel cell stack safety assessment required"

  - id: SAFETY-FC-002
    condition: "thermal management procedures critical"
    enforcement: escalate
    escalation_target: STK_SAF
    message: "Thermal management safety procedures require review"

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

ATA 71 – Fuel Cell Power Plant domain requires specific knowledge:

### 3.1 Fuel Cell System Components

```yaml
fuel_cell_systems:
  fuel_cell_stack:
    - name: "PEM Fuel Cell Stack"
      ata_section: "71-11"
      description: "Proton Exchange Membrane fuel cell stack"
      operating_temperature: "60-80°C"
      power_output: "Variable by design (e.g., 100 kW - 2 MW)"
      efficiency: "40-60% (electrical)"
      reactants: "Hydrogen (from ATA 28), Air/Oxygen"
      safety_criticality: "DAL A"
      
    - name: "Stack Cooling System"
      ata_section: "71-12"
      description: "Integrated stack cooling and temperature control"
      coolant: "Deionized water/glycol mixture"
      
    - name: "Stack Monitoring System"
      ata_section: "71-13"
      description: "Individual cell voltage and temperature monitoring"
  
  balance_of_plant:
    - name: "Air Supply System"
      ata_section: "71-21"
      description: "Air compressor, humidification, and distribution"
      components: ["Air compressor", "Humidifier", "Air filter"]
      
    - name: "Hydrogen Supply Interface"
      ata_section: "71-22"
      description: "H2 interface from ATA 28 fuel system"
      integration: "ATA 28 - Fuel (H2 supply)"
      pressure_regulation: "Fuel cell operating pressure"
      
    - name: "Water Management"
      ata_section: "71-23"
      description: "Product water removal and management"
      
    - name: "Thermal Management System"
      ata_section: "71-24"
      description: "Heat rejection and temperature control"
      components: ["Coolant pump", "Heat exchanger", "Radiator", "Temperature sensors"]
      safety_criticality: "DAL A"
  
  power_conditioning:
    - name: "DC Power Conditioning"
      ata_section: "71-31"
      description: "DC/DC converters and voltage regulation"
      integration: "ATA 24 - Electrical Power"
      
    - name: "Inverter (if AC required)"
      ata_section: "71-32"
      description: "DC to AC conversion"
      integration: "ATA 24 - Electrical Power"
  
  control_system:
    - name: "Fuel Cell Controller"
      ata_section: "71-41"
      description: "Stack power management and protection"
      functions: ["Load management", "Thermal control", "Fault detection", "Emergency shutdown"]
      safety_criticality: "DAL A"
      
    - name: "Health Monitoring"
      ata_section: "71-42"
      description: "Performance monitoring and diagnostics"
      parameters: ["Cell voltages", "Stack current", "Temperatures", "Pressures", "Humidity"]
```

### 3.2 Fuel Cell Operating Modes

```yaml
operating_modes:
  normal_operation:
    description: "Steady-state power generation"
    power_range: "10-100% of rated power"
    start_time: "< 1 minute (typical)"
    
  cold_start:
    description: "Start from sub-zero temperatures"
    requirements:
      - "Pre-heating if required"
      - "Purge cycles"
      - "Gradual load increase"
    time: "Extended start sequence"
    
  emergency_shutdown:
    description: "Rapid shutdown for safety"
    triggers:
      - "Thermal runaway detection"
      - "H2 leak detection"
      - "Electrical fault"
      - "Loss of cooling"
    actions:
      - "Isolate H2 supply"
      - "Disconnect electrical load"
      - "Activate emergency cooling (if available)"
      - "Purge with inert gas"
    
  standby:
    description: "Warm standby mode"
    power: "Minimal power to maintain temperature"
```

### 3.3 Hydrogen Interface (ATA 28)

```yaml
h2_interface:
  supply_requirements:
    purity: "> 99.97% (per ISO 14687-2)"
    contaminants:
      - "CO: < 0.2 ppm"
      - "CO₂: < 2 ppm"
      - "H₂O: < 5 ppm"
      - "Total hydrocarbons: < 2 ppm"
    
    pressure: "Regulated to fuel cell operating pressure"
    flow_rate: "Variable based on power demand"
  
  safety_integration:
    - "H2 isolation valves (fail-closed)"
    - "Leak detection (interface to ATA 28 system)"
    - "Pressure relief coordination"
    - "Emergency shutdown coordination"
```

### 3.4 Failure Modes (ARP4761)

```yaml
failure_modes:
  - mode: "Fuel cell stack thermal runaway"
    severity: "Catastrophic"
    probability: "< 1E-9 per flight hour"
    mitigation: "Thermal monitoring, emergency shutdown, redundant cooling, fire protection"
    
  - mode: "H2 supply failure"
    severity: "Hazardous"
    probability: "< 1E-7 per flight hour"
    mitigation: "Backup power source (battery, APU), graceful degradation, crew alerting"
    
  - mode: "Loss of cooling (thermal management failure)"
    severity: "Hazardous"
    probability: "< 1E-7 per flight hour"
    mitigation: "Redundant cooling pumps, emergency shutdown, thermal protection"
    
  - mode: "Stack performance degradation"
    severity: "Major"
    probability: "< 1E-5 per flight hour"
    mitigation: "Health monitoring, predictive maintenance, power derating"
    
  - mode: "Electrical fault (short circuit)"
    severity: "Major"
    probability: "< 1E-5 per flight hour"
    mitigation: "Current limiting, circuit breakers, isolation, fault detection"
    
  - mode: "H2 leak at fuel cell interface"
    severity: "Hazardous"
    probability: "< 1E-7 per flight hour"
    mitigation: "Leak detection, isolation valves, ventilation, H2 monitoring (ATA 28)"
```

---

## 4. Allowed Operations

Operations permitted under BREX governance:

```yaml
allowed_operations:
  - operation: "generate_dm_if"
    brex_rules: ["AUTHOR-002", "STRUCT-001"]
    description: "Generate Data Module for ATA 71"
    contract: "KITDM-CTR-LM-CSDB_ATA71"
    
  - operation: "produce_publication_if"
    brex_rules: ["STRUCT-001", "BREX-001"]
    description: "Produce AMM/SRM content for fuel cell power plant"
    output_target: "IDB/PUB/AMM/CSDB/ATA71"
    
  - operation: "transform_content_if"
    brex_rules: ["PIPELINE-004", "TRACE-001"]
    description: "Transform fuel cell data to S1000D"
    pipeline: "pipelines/ata71_pipeline.yaml"
    
  - operation: "validate_fc_safety_content_if"
    brex_rules: ["SAFETY-002", "SAFETY-FC-001", "SAFETY-FC-002"]
    description: "Validate fuel cell safety content"
    escalation_required: true
```

---

## 5. Prohibited Operations

Operations NOT permitted under any circumstance:

```yaml
prohibited_operations:
  - operation: "generate_content_without_contract"
    violation: "CRITICAL"
    message: "Cannot generate ATA 71 content without KITDM-CTR-LM-CSDB_ATA71"
    
  - operation: "create_structure_without_ata_domain"
    violation: "ERROR"
    message: "Cannot create content without ATA 71 domain classification"
    
  - operation: "bypass_lifecycle_states"
    violation: "ERROR"
    message: "Cannot bypass LC04 design review for fuel cell systems"
    
  - operation: "auto_invent_fc_safety_content"
    violation: "CRITICAL"
    message: "Cannot auto-generate fuel cell safety warnings without STK_SAF approval"
    
  - operation: "omit_thermal_safety"
    violation: "CRITICAL"
    message: "Cannot omit thermal management safety procedures"
    
  - operation: "skip_h2_interface_docs"
    violation: "ERROR"
    message: "Cannot omit hydrogen supply interface documentation"
```

---

## 6. S1000D DMC Constraints

Data Module Code constraints for ATA 71:

```yaml
dmc_constraints:
  model_ident_code: "${MODEL_IDENT_CODE}"  # Project-specific
  system_diff_code: "A"
  system_code: "71"
  
  sub_systems:
    - sub_system: "00"
      description: "Fuel Cell Power Plant - General"
    - sub_system: "11"
      description: "Fuel Cell Stack"
    - sub_system: "21"
      description: "Balance of Plant (Air, H2, Water)"
    - sub_system: "24"
      description: "Thermal Management"
    - sub_system: "31"
      description: "Power Conditioning"
    - sub_system: "41"
      description: "Control and Monitoring"
      
  info_codes:
    descriptive: ["000", "001", "040", "041", "042"]
    procedural: ["100", "200", "300", "400", "500", "510", "520", "600", "700"]
    parts: ["941", "942"]
```

---

## 7. Special Handling: Fuel Cell Systems

For fuel cell power plant systems:

```yaml
fuel_cell_requirements:
  mandatory_warnings:
    - type: "THERMAL HAZARD"
      placement: "Before fuel cell maintenance"
      content: "WARNING: Fuel cell stack may be hot during and after operation. Allow cooling before maintenance. Operating temperature 60-80°C."
      
    - type: "ELECTRICAL HAZARD"
      placement: "Before electrical work"
      content: "DANGER: High voltage and current. De-energize and lockout/tagout before maintenance. Verify zero energy state."
      
    - type: "H2 SUPPLY HAZARD"
      placement: "Before H2 interface work"
      content: "DANGER: Hydrogen supply at interface. Isolate H2 supply and purge system before work. Refer to ATA 28 procedures."
      
    - type: "COOLANT HAZARD"
      placement: "Before cooling system work"
      content: "WARNING: Cooling system under pressure. Release pressure before opening. Coolant may be hot."
  
  special_procedures:
    - "Verify H2 isolation before maintenance (ATA 28 coordination)"
    - "Electrical lockout/tagout procedures"
    - "Cooling system pressure relief"
    - "Purge with inert gas before opening stack"
    - "Stack health monitoring and diagnostics"
    
  escalation_required:
    trigger: "Any fuel cell safety content generation"
    escalation_target: "STK_SAF"
    approval_timeout: "72 hours"
    
  special_conditions:
    - condition: "SC-71-FUELCELL-001"
      title: "Fuel Cell Power Plant Certification"
      description: "Special conditions for fuel cell propulsion systems"
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
    - "Thermal safety warning inclusion"
    - "H2 interface documentation check"
    
  retention: "7 years minimum (certification)"
```

---

## 9. Escalation Procedures

When human approval is required:

```yaml
escalation_procedures:
  fc_safety_content:
    trigger: "SAFETY-FC-001 or SAFETY-FC-002"
    escalation_target: "STK_SAF"
    required_review:
      - "Fuel cell stack safety procedures"
      - "Thermal management safety"
      - "Emergency shutdown procedures"
      - "H2 interface safety coordination"
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
| ATA 71 Contract | ASIT/CONTRACTS/active/KITDM-CTR-LM-CSDB_ATA71.yaml |
| Project BREX | ASIGT/brex/project_brex.yaml |
| T-Subdomain LC Activation | lifecycle/T_SUBDOMAIN_LC_ACTIVATION.yaml |
| ATA 28 H2 Cryogenic Instructions | .github/instructions/ata28_h2_cryogenic.instructions.md |

---

*End of ATA 71 Fuel Cell BREX-Driven Instructions*
