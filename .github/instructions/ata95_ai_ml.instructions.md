---
# =============================================================================
# BREX-DRIVEN COPILOT INSTRUCTION FILE
# ATA 95 – AI/ML Models Domain
# =============================================================================
#
# This instruction file demonstrates the BREX-driven instruction system
# for the AEROSPACEMODEL Agent. All reasoning is constrained, guided,
# and explainable through BREX rules.
#
audience: engineering
ata_domain: "ATA 95 – AI/ML Models"
authority: ASIT
baseline_required: true
contract_required: true
brex_profile: "AEROSPACEMODEL-PRJ-01"
determinism: strict
version: "1.0.0"
---

# AEROSPACEMODEL Agent Instructions: ATA 95 – AI/ML Models

> **Authority:** ASIT (Aircraft Systems Information Transponder)  
> **Determinism Level:** STRICT  
> **Compliance:** S1000D Issue 5.0, DO-178C, ARP4754A, ARP4761, EU AI Act

---

## 1. Purpose

This instruction file governs AEROSPACEMODEL Agent behavior for ATA 95 (AI/ML Models) domain operations. All agent reasoning is constrained by BREX decision rules. No free-form autonomy exists.

---

## 2. BREX Decision Integration

The following BREX rules MUST be evaluated before any operation:

```yaml
brex_rules:
  # Structure Rules
  - id: STRUCT-001
    condition: "ata_domain MUST exist"
    enforcement: block
    message: "AI/ML content requires ATA 95 domain classification"

  # Authority Rules
  - id: AUTHOR-002
    condition: "content generation requires ASIT-approved contract"
    enforcement: require_contract
    message: "Generation requires contract: KITDM-CTR-LM-CSDB_ATA95"

  # Safety Rules
  - id: SAFETY-002
    condition: "if safety-related, require human approval"
    enforcement: escalate
    escalation_target: STK_SAF
    message: "AI/ML safety content requires human approval"

  - id: SAFETY-AI-001
    condition: "AI model assurance requires human approval"
    enforcement: escalate
    escalation_target: STK_SAF
    message: "AI model safety assessment requires human review"

  - id: SAFETY-AI-002
    condition: "training data governance required"
    enforcement: block
    message: "AI training data must meet governance requirements"

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

ATA 95 – AI/ML Models domain requires specific knowledge:

### 3.1 AI/ML Model Types

```yaml
model_types:
  inference_models:
    - name: "Predictive Maintenance"
      description: "Predict component failures and maintenance needs"
      dal_classification: "DAL B or C"
      input_data: "Sensor data, maintenance history, flight parameters"
      output: "Failure predictions, remaining useful life estimates"
      
    - name: "Flight Data Analysis"
      description: "Analyze flight data for optimization and anomaly detection"
      dal_classification: "DAL C or D"
      input_data: "Flight data recorder, quick access recorder"
      output: "Performance metrics, anomalies, recommendations"
      
    - name: "System Monitoring"
      description: "Real-time monitoring of aircraft systems"
      dal_classification: "DAL B"
      input_data: "System sensors, operational parameters"
      output: "Health status, alerts, diagnostics"
  
  training_models:
    - name: "Model Training Pipeline"
      description: "Training and validation infrastructure"
      components: ["Data preprocessing", "Model training", "Validation", "Deployment"]
      
    - name: "Continuous Learning"
      description: "Model retraining and updates"
      components: ["Data collection", "Drift detection", "Retraining", "A/B testing"]

  explainability:
    - name: "Explainable AI (XAI)"
      description: "Model interpretability and transparency"
      techniques: ["SHAP", "LIME", "Attention mechanisms", "Feature importance"]
      requirement: "Mandatory for DAL A/B systems"
```

### 3.2 EU AI Act Risk Categories

```yaml
eu_ai_act_categories:
  high_risk:
    description: "AI systems with significant safety or rights implications"
    examples:
      - "Safety-critical flight control assistance"
      - "Pilot decision support systems"
      - "Critical system monitoring"
    requirements:
      - "Risk management system"
      - "Data governance and quality"
      - "Technical documentation"
      - "Transparency and user information"
      - "Human oversight"
      - "Robustness and cybersecurity"
      - "Conformity assessment"
    
  limited_risk:
    description: "AI systems with transparency obligations"
    examples:
      - "Non-critical maintenance recommendations"
      - "Flight data analytics dashboards"
    requirements:
      - "Transparency obligations"
      - "User awareness of AI interaction"
    
  minimal_risk:
    description: "AI systems with no specific obligations"
    examples:
      - "Back-office data processing"
      - "Non-operational analytics"
    requirements: []
```

### 3.3 Data Governance Requirements

```yaml
data_governance:
  training_data:
    requirements:
      - "Data provenance and traceability"
      - "Data quality validation"
      - "Bias detection and mitigation"
      - "Data versioning and lineage"
      - "Privacy compliance (GDPR, etc.)"
    
    validation:
      - "Statistical representativeness"
      - "Adversarial robustness testing"
      - "Edge case coverage"
      - "Synthetic data validation (ATA 97)"
  
  operational_data:
    requirements:
      - "Data collection consent"
      - "Data anonymization"
      - "Secure storage and transmission"
      - "Retention and deletion policies"
```

### 3.4 Failure Modes (ARP4761)

```yaml
failure_modes:
  - mode: "Model prediction error (false negative)"
    severity: "Hazardous or Catastrophic (depends on application)"
    probability: "Must meet DAL requirements"
    mitigation: "Human oversight, redundant monitoring, confidence thresholds"
    
  - mode: "Model prediction error (false positive)"
    severity: "Major"
    probability: "< 1E-5 per flight hour"
    mitigation: "Alert filtering, human confirmation, multi-model consensus"
    
  - mode: "Model drift (performance degradation)"
    severity: "Major"
    probability: "< 1E-5 per flight hour"
    mitigation: "Continuous monitoring, periodic retraining, performance thresholds"
    
  - mode: "Data poisoning (adversarial attack)"
    severity: "Hazardous"
    probability: "< 1E-7 per flight hour"
    mitigation: "Input validation, anomaly detection, secure data pipeline"
    
  - mode: "Model unavailability"
    severity: "Major or Minor (depends on application)"
    probability: "< 1E-5 per flight hour"
    mitigation: "Fallback to traditional algorithms, graceful degradation"
```

---

## 4. Allowed Operations

Operations permitted under BREX governance:

```yaml
allowed_operations:
  - operation: "generate_dm_if"
    brex_rules: ["AUTHOR-002", "STRUCT-001"]
    description: "Generate Data Module for ATA 95"
    contract: "KITDM-CTR-LM-CSDB_ATA95"
    
  - operation: "produce_publication_if"
    brex_rules: ["STRUCT-001", "BREX-001"]
    description: "Produce AMM/SRM content for AI/ML systems"
    output_target: "IDB/PUB/AMM/CSDB/ATA95"
    
  - operation: "transform_content_if"
    brex_rules: ["PIPELINE-004", "TRACE-001"]
    description: "Transform AI/ML documentation to S1000D"
    pipeline: "pipelines/ata95_pipeline.yaml"
    
  - operation: "validate_ai_safety_content_if"
    brex_rules: ["SAFETY-002", "SAFETY-AI-001", "SAFETY-AI-002"]
    description: "Validate AI model safety and data governance"
    escalation_required: true
```

---

## 5. Prohibited Operations

Operations NOT permitted under any circumstance:

```yaml
prohibited_operations:
  - operation: "generate_content_without_contract"
    violation: "CRITICAL"
    message: "Cannot generate ATA 95 content without KITDM-CTR-LM-CSDB_ATA95"
    
  - operation: "create_structure_without_ata_domain"
    violation: "ERROR"
    message: "Cannot create content without ATA 95 domain classification"
    
  - operation: "bypass_lifecycle_states"
    violation: "ERROR"
    message: "Cannot bypass LC04 design review for AI/ML systems"
    
  - operation: "auto_invent_ai_safety_content"
    violation: "CRITICAL"
    message: "Cannot auto-generate AI safety warnings without STK_SAF approval"
    
  - operation: "omit_data_governance"
    violation: "CRITICAL"
    message: "Cannot omit training data governance documentation"
    
  - operation: "skip_explainability"
    violation: "ERROR"
    message: "Cannot skip explainability for DAL A/B AI systems"
```

---

## 6. S1000D DMC Constraints

Data Module Code constraints for ATA 95:

```yaml
dmc_constraints:
  model_ident_code: "${MODEL_IDENT_CODE}"  # Project-specific
  system_diff_code: "A"
  system_code: "95"
  
  sub_systems:
    - sub_system: "00"
      description: "AI/ML Models - General"
    - sub_system: "10"
      description: "Predictive Maintenance Models"
    - sub_system: "20"
      description: "Flight Data Analysis Models"
    - sub_system: "30"
      description: "System Monitoring Models"
    - sub_system: "40"
      description: "Model Training Infrastructure"
    - sub_system: "50"
      description: "Model Deployment and Management"
    - sub_system: "60"
      description: "Explainability and Transparency"
      
  info_codes:
    descriptive: ["000", "001", "040", "041", "042"]
    procedural: ["100", "200", "300", "400", "500", "510", "520", "600", "700"]
    parts: ["941", "942"]
```

---

## 7. Special Handling: AI Model Assurance

For AI/ML systems requiring certification:

```yaml
ai_assurance_requirements:
  mandatory_documentation:
    - type: "MODEL ARCHITECTURE"
      placement: "Before model deployment"
      content: "Complete model architecture, hyperparameters, and training configuration"
      
    - type: "TRAINING DATA GOVERNANCE"
      placement: "Before model training"
      content: "Data sources, quality metrics, bias detection results, provenance"
      
    - type: "EXPLAINABILITY ANALYSIS"
      placement: "Before operational use"
      content: "XAI analysis, feature importance, decision boundaries, interpretability"
      
    - type: "ADVERSARIAL TESTING"
      placement: "During verification (LC06)"
      content: "Adversarial robustness testing, edge case validation, failure mode analysis"
  
  special_procedures:
    - "Model versioning and lineage tracking"
    - "Continuous monitoring and drift detection"
    - "Periodic retraining and revalidation"
    - "Human oversight and override capability"
    - "Fallback to traditional algorithms"
    
  escalation_required:
    trigger: "Any DAL A or DAL B AI system"
    escalation_target: "STK_SAF"
    approval_timeout: "72 hours"
    
  eu_ai_act_compliance:
    trigger: "Any high-risk AI system per EU AI Act"
    requirements:
      - "Conformity assessment"
      - "CE marking"
      - "Registration in EU database"
      - "Post-market monitoring"
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
    - "Data governance validation"
    - "Explainability assessment (if applicable)"
    - "EU AI Act compliance check (if applicable)"
    
  retention: "7 years minimum (certification)"
```

---

## 9. Escalation Procedures

When human approval is required:

```yaml
escalation_procedures:
  ai_safety_content:
    trigger: "SAFETY-AI-001 or SAFETY-AI-002"
    escalation_target: "STK_SAF"
    required_review:
      - "AI model safety assessment"
      - "Training data governance"
      - "Explainability analysis"
      - "Failure mode and effects analysis"
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
| ATA 95 Contract | ASIT/CONTRACTS/active/KITDM-CTR-LM-CSDB_ATA95.yaml |
| Project BREX | ASIGT/brex/project_brex.yaml |
| T-Subdomain LC Activation | lifecycle/T_SUBDOMAIN_LC_ACTIVATION.yaml |

---

*End of ATA 95 BREX-Driven Instructions*
