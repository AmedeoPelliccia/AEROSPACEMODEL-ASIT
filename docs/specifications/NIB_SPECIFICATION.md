# Non-Inference Boundary (NIB) Technical Specification

**Document ID:** AEROSPACEMODEL-ASIT-NIB-SPEC-001  
**Version:** 1.0 DRAFT  
**Status:** DRAFT  
**Classification:** Programme Controlled  
**Date:** 2026-02-13  
**Author:** Amedeo Pelliccia  
**Organisation:** IDEALEeu Enterprise / AMPEL360 Programme  

---

## Document Control

### Revision History

| Version | Date | Author | Change Summary |
|---------|------|--------|----------------|
| 1.0 | 2026-02-13 | A. Pelliccia | Initial release. Establishes NIB taxonomy, detection logic, escalation protocols, evidence requirements, and integration with CNOT-gate architecture and EU AI Act Articles 14–15. |

### Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Chief Systems Engineer | | | |
| Safety & Certification Lead | | | |
| AI Governance Authority | | | |
| Configuration Manager | | | |

---

## Table of Contents

1. [Scope and Purpose](#1-scope-and-purpose)
2. [Definitions, Abbreviations, and Conventions](#2-definitions-abbreviations-and-conventions)
3. [Concept of Operations](#3-concept-of-operations)
4. [NIB Classification Taxonomy](#4-nib-classification-taxonomy)
5. [Detection and Escalation Protocol](#5-detection-and-escalation-protocol)
6. [Implementation Guidelines](#6-implementation-guidelines)
7. [Regulatory Compliance](#7-regulatory-compliance)
8. [Conclusion](#8-conclusion)
9. [Appendices](#9-appendices)

---

## 1. Scope and Purpose

This specification defines the concept, classification, detection logic, escalation protocol, and evidence requirements for **Non-Inference Boundaries (NIBs)** within the AEROSPACEMODEL framework.

### Definition

A **Non-Inference Boundary** is the precise point in a governed automation chain where the system's deterministic reasoning capability is exhausted and human cognitive authority must be engaged to resolve irreducible ambiguity.

### Key Principle

The NIB concept is the technical mechanism by which AEROSPACEMODEL satisfies the Human-in-the-Loop (HITL) requirements of:
- **EU AI Act** (Articles 14–15)
- **EASA AI Roadmap 2.0** principles
- The programme's own **Model Digital Constitution**

Unlike conventional HITL checkpoints—which are placed at arbitrary process milestones—**NIBs are structurally derived properties of transformation contracts**. They emerge where the BREX decision cascade cannot deterministically resolve an operation, making human oversight a consequence of epistemic limits rather than procedural ceremony.

### Normative References

This document is normatively referenced by:
- ASIT Governance layer
- BREX Decision Engine
- CNOT-Gate Lifecycle Architecture
- EASA/ESA AI Governance Standard v1.0 draft

### Applicability

This specification applies to:
- All ASIGT-mediated content transformations within the AEROSPACEMODEL ecosystem
- AMPEL360 Q100 programme and related programmes
- Every point where automated processes terminate deterministic execution and require human resolution
- PLM lifecycle phases (LC01–LC10, rooted in KDB)
- Operational phases (LC11–LC14, rooted in IDB)

---

## 2. Definitions, Abbreviations, and Conventions

### 2.1 Key Definitions

| Term | Definition |
|------|------------|
| **Non-Inference Boundary (NIB)** | A formally identified point in the BREX decision cascade where the automation's deterministic reasoning is exhausted and human cognitive authority is required to resolve the ambiguity. The NIB is a property of the transformation contract, not an arbitrary checkpoint. |
| **Deterministic Envelope** | The set of all operations that can be resolved by the BREX decision cascade without human intervention, given a valid contract, baseline, and authority context. |
| **State Collapse** | The authorised resolution of a lifecycle ambiguity into a concrete, versioned artifact. In NIB terms, the human decision at a boundary that collapses the superposition of possible states into a single governed outcome. |
| **Escalation Authority** | The designated human role or board empowered to resolve a specific NIB class. Determined by the NIB classification and the safety impact assessment. |
| **BREX Undefined Condition** | A state in the BREX decision cascade where no rule matches the current operation context. This always triggers a NIB—the system halts rather than proceeding with undefined behaviour. |
| **Provenance Vector** | Machine-readable traceability chain: output → source → contract → context → human decision. NIB resolutions are recorded as provenance vector nodes. |
| **Transformation Contract** | Machine-actionable specification governing a cross-domain information transformation, including its permitted inputs, outputs, BREX rules, and NIB conditions. |

### 2.2 Abbreviations

| Abbreviation | Expansion |
|--------------|-----------|
| NIB | Non-Inference Boundary |
| ASIT | Aircraft Systems Information Transponder |
| ASIGT | Aircraft Systems Information Generative Transponder |
| BREX | Business Rules Exchange |
| TLI | Top-Level Instruction |
| HITL | Human-in-the-Loop |
| CNOT | Controlled-NOT (gate) |
| KDB | Knowledge Database |
| IDB | Information Database |
| CCB | Configuration Control Board |
| DER | Designated Engineering Representative |
| FHA | Functional Hazard Assessment |
| DAL | Design Assurance Level (A–E) |

---

## 3. Concept of Operations

### 3.1 The Problem: Unbounded Automation

Conventional AI-assisted content generation in aerospace operates on a spectrum from fully manual authoring to fully autonomous generation. Neither extreme is acceptable for certification-grade information products:

- **Manual processes** are slow, expensive, and prone to transcription error
- **Autonomous generation** introduces risks:
  - Hallucination
  - Uncontrolled semantic drift
  - Loss of traceability to engineering intent (SSOT)

The fundamental challenge is **not whether to automate, but where automation must stop**.

Most frameworks answer this with **process-based checkpoints**: a human reviews output at predetermined milestones. This approach is structurally flawed because:
- Checkpoints bear no necessary relationship to the actual epistemic limits of automation
- A review gate after a fully deterministic transformation adds cost without safety value
- A review gate absent where automation is genuinely uncertain creates a latent hazard

### 3.2 The Solution: Structurally Derived Boundaries

AEROSPACEMODEL resolves this by **deriving the location and type of human intervention directly from the structure of the transformation itself**.

When the BREX decision cascade encounters a condition it cannot resolve:
- Rules are incomplete
- Input is ambiguous
- Safety impact exceeds automation's authority
- Contract explicitly prohibits autonomous resolution

→ **The system halts and declares a Non-Inference Boundary**

This means every NIB is a **falsifiable claim**: the system asserts that it cannot, given its current rule set and context, produce a deterministic output.

The human at the boundary:
- Does not merely approve
- Resolves the ambiguity by providing cognitive input the system lacks
- Their decision is recorded as a provenance vector node
- Becomes part of the traceable evidence chain

### 3.3 Relationship to Governance Stack

| Layer | Document | NIB Relationship |
|-------|----------|------------------|
| Foundational | Model Digital Constitution | Establishes principle: "Automation proposes; humans authorise" |
| Charter | HCDS Charter v1.0 | Mandates HITL at every non-inference boundary |
| Standard | EASA/ESA AI Gov. Std v1.0 | Defines NIBs as the mechanism for Art. 14–15 compliance |
| Framework | TLI v2.1 | Specifies TLI-level boundary declarations |
| Implementation | This Specification (NIB-SPEC-001) | Defines taxonomy, detection, escalation, evidence |
| Execution | BREX Decision Engine | Implements NIB detection at runtime |

---

## 4. NIB Classification Taxonomy

Non-Inference Boundaries are classified along **two orthogonal axes**:
1. **Source** of the boundary (why the automation halts)
2. **Safety Impact** of the decision (what is at stake)

The intersection determines the **escalation authority** and **evidence requirements**.

### 4.1 Axis 1 — Boundary Source

| Code | Source Type | Description |
|------|-------------|-------------|
| **NIB-R** | Rule Exhaustion | The BREX cascade terminates without a matching rule. The rule set is incomplete for the given context. This is the "BREX Undefined Condition". |
| **NIB-A** | Ambiguity | Multiple BREX rules match with conflicting outcomes. The system cannot deterministically select one. The ambiguity is in the rule set itself or in the input data. |
| **NIB-S** | Safety Threshold | The BREX cascade resolves, but the operation's safety impact exceeds the automation's delegated authority level. The system can produce an answer but is not authorised to act on it. |
| **NIB-C** | Contractual Prohibition | The transformation contract explicitly requires human resolution for this operation class, regardless of whether the automation could resolve it. This is a governance choice, not an epistemic limit. |
| **NIB-T** | Trust Boundary | The operation crosses a trust domain boundary (e.g., KDB → IDB transition, cross-organisation data exchange, security classification change). Even if the transformation is deterministic, the boundary requires human attestation. |
| **NIB-E** | Epistemic Limit | The input data is genuinely insufficient to produce a deterministic output. Missing data, unresolved KNOTs, or incomplete baselines. This is an intrinsic property of the knowledge state, not a rule-set deficiency. |

### 4.2 Axis 2 — Safety Impact Level

Derived from the **Functional Hazard Assessment (FHA)** classification, aligned with ARP4761 and CS-25.1309:

| Level | FHA Classification | DAL Equivalent | NIB Implication |
|-------|-------------------|----------------|-----------------|
| **SIL-CAT** | Catastrophic | DAL A | Maximum evidence, dual-authority escalation, mandatory DER involvement |
| **SIL-HAZ** | Hazardous | DAL B | Formal escalation, safety board review, documented rationale |
| **SIL-MAJ** | Major | DAL C | Standard escalation, domain expert resolution |
| **SIL-MIN** | Minor | DAL D | Logged resolution, post-facto review acceptable |
| **SIL-NSE** | No Safety Effect | DAL E | Recorded, minimal formality |

### 4.3 Combined Classification Matrix

Each NIB instance is classified as a **tuple** (Source, Impact), e.g., `NIB-S/SIL-HAZ`.

This tuple determines:
- Escalation authority
- Maximum permitted resolution time
- Evidence depth

#### Escalation Authority Matrix

| Source ↓ Impact → | CAT | HAZ | MAJ | MIN | NSE |
|-------------------|-----|-----|-----|-----|-----|
| **NIB-R** | DER + CCB | CCB | STK_SE | STK_SE | Auto-log |
| **NIB-A** | DER + CCB | CCB | STK_SE | STK_SE | Auto-log |
| **NIB-S** | DER + SAF Board | STK_SAF + DER | STK_SAF | STK_SE | Auto-log |
| **NIB-C** | Per Contract | Per Contract | Per Contract | Per Contract | Per Contract |
| **NIB-T** | CCB + both domains | CCB | STK_CM | STK_CM | Auto-log |
| **NIB-E** | DER + CCB | CCB | STK_SE | STK_SE | Auto-log |

**Legend:**
- **DER**: Designated Engineering Representative
- **CCB**: Configuration Control Board
- **STK_SAF**: Safety Stakeholder
- **STK_SE**: Systems Engineering Stakeholder
- **STK_CM**: Configuration Management Stakeholder

---

## 5. Detection and Escalation Protocol

### 5.1 Detection Mechanism

NIB detection is implemented in the **BREX Decision Engine runtime**.

When a NIB is triggered:
1. The BREX cascade evaluates rules in order
2. **Trigger conditions:**
   - No rule matches
   - Multiple conflicting rules match
   - A matching rule's action is `ESCALATE`
3. A NIB is declared

The detection mechanism logs:
- Rule set version
- Input parameters
- Matching attempts
- Reason for halting

### 5.2 Escalation Workflow

Upon NIB detection, the system creates an **escalation ticket** containing:

| Field | Content |
|-------|---------|
| NIB Classification | e.g., NIB-S/SIL-HAZ |
| Context Snapshot | All input data, contract ID, baseline reference |
| Proposed Resolution Options | If available |
| Escalation Authority | Derived from classification matrix |
| Maximum Resolution Time | SLA based on safety impact |

### 5.3 Resolution Recording

The human decision at a NIB is recorded with **full provenance**:

| Field | Content |
|-------|---------|
| **Decision ID** | Unique identifier for this NIB resolution |
| **NIB Classification** | Source and Impact tuple |
| **Resolver Identity** | Authenticated user or board that made the decision |
| **Resolution Rationale** | Textual explanation of the decision |
| **Timestamp** | ISO 8601 UTC timestamp |
| **Input Context Hash** | SHA-256 hash of the input state |
| **Output State** | The resolved artifact or decision outcome |

---

## 6. Implementation Guidelines

### 6.1 BREX Rule Annotation

BREX rules that may trigger NIBs must be annotated with NIB metadata:

```yaml
- id: SAFETY-H2-001
  condition: "hydrogen handling requires safety review"
  enforcement: escalate
  escalation_target: STK_SAF
  nib_metadata:
    source_type: NIB-S
    safety_impact: SIL-HAZ
    evidence_required:
      - FHA reference
      - H2 safety procedure review
      - DER sign-off
```

### 6.2 Audit Trail Requirements

All NIB events and resolutions must be logged to an **immutable audit trail**.

The audit log must support:
- ✅ Chronological ordering with nanosecond precision
- ✅ Cryptographic integrity verification
- ✅ Role-based access control
- ✅ Export to regulatory-compliant formats

### 6.3 Integration with CNOT Architecture

NIBs integrate with the **CNOT-gate lifecycle architecture** as control gates.

Each lifecycle phase (LC01–LC14) may define phase-specific NIB conditions. The CNOT gate prevents state progression until all NIBs in the current phase are resolved.

---

## 7. Regulatory Compliance

### 7.1 EU AI Act Articles 14–15

The NIB framework directly implements the **human oversight requirements** of EU AI Act Articles 14 and 15:

| Article | Requirement | NIB Implementation |
|---------|-------------|-------------------|
| **Art. 14(1) – Design** | Human oversight designed into system | NIBs are structurally derived from transformation contracts, ensuring human oversight is designed in, not added as afterthought |
| **Art. 14(2) – Understand Output** | Humans must understand AI output | NIB resolution requires the human to review context, understand the ambiguity, and document rationale |
| **Art. 14(3) – Interpretation** | Provide means for human interpretation | The system provides full context and proposed options at NIBs, enabling informed human interpretation |
| **Art. 14(4) – Override** | Ability to override AI decisions | NIBs halt execution; the human decision is the authoritative resolution, not a mere approval |
| **Art. 15 – Accuracy** | Ensure appropriate accuracy | NIBs are triggered when deterministic accuracy cannot be guaranteed, ensuring appropriate human oversight |

### 7.2 EASA AI Roadmap 2.0

EASA AI Roadmap 2.0 emphasises:
- **Explainability**: Every NIB records why the automation halted
- **Traceability**: Full provenance vector from input to human decision
- **Human Oversight**: Structurally enforced at epistemic limits

---

## 8. Conclusion

The Non-Inference Boundary specification provides a **rigorous, deterministic framework** for human-in-the-loop governance in AI-assisted aerospace content generation.

### Key Achievements

By deriving human oversight requirements directly from the epistemic limits of automation, AEROSPACEMODEL ensures that:

✅ Human oversight is applied **where it is needed**  
✅ Human oversight is applied **only where it is needed**  
✅ Maximises both **safety** and **efficiency**

### Living Document

This specification is a **living document**. As the AEROSPACEMODEL ecosystem evolves, this document will be updated to reflect:
- New NIB types
- Escalation authorities
- Integration patterns

All changes will be subject to the ASIT governance process and recorded in the revision history.

---

## 9. Appendices

### Appendix A: Example NIB Scenarios

#### A.1 Scenario: Undefined ATA Chapter

**Situation:**  
An ASIGT transformation attempts to generate content for ATA Chapter 97 (Novel Technologies), but no BREX rule exists for this chapter.

**NIB Trigger:**  
The BREX cascade terminates → **NIB-R** (Rule Exhaustion)

**Classification:**  
NIB-R/SIL-MAJ

**Escalation:**  
STK_SE (Systems Engineering Stakeholder)

**Resolution:**  
1. Systems engineer reviews ATA 97 requirements
2. Creates appropriate BREX rule
3. Updates `master_brex_authority.yaml`
4. Resubmits transformation

---

#### A.2 Scenario: Safety-Critical Content

**Situation:**  
An automated transformation generates a WARNING for a fuel system procedure. The BREX rule matches, but flags the operation as safety-critical (DAL A).

**NIB Trigger:**  
Safety threshold exceeded → **NIB-S** (Safety Threshold)

**Classification:**  
NIB-S/SIL-CAT

**Escalation:**  
DER + Safety Board

**Resolution:**  
1. DER reviews warning text
2. Verifies against FHA
3. Approves or modifies
4. Signs off
5. Decision recorded in audit log

---

#### A.3 Scenario: Baseline Transition

**Situation:**  
A content package is ready to transition from Knowledge Database (KDB) to Information Database (IDB), crossing from design phase to production.

**NIB Trigger:**  
Trust boundary crossed → **NIB-T** (Trust Boundary)

**Classification:**  
NIB-T/SIL-MAJ

**Escalation:**  
Configuration Control Board (CCB)

**Resolution:**  
1. CCB reviews baseline
2. Verifies all design artifacts are complete and approved
3. Authorises transition
4. Updates baseline register

---

### Appendix B: BREX Rule Template for NIB Annotation

Example YAML template for annotating BREX rules with NIB metadata:

```yaml
# Example: Hydrogen Safety Rule with NIB Metadata
- id: SAFETY-H2-001
  condition: "hydrogen handling requires safety review"
  enforcement: escalate
  escalation_target: STK_SAF
  message: "Hydrogen handling safety assessment required"
  
  # NIB Metadata
  nib_metadata:
    source_type: NIB-S              # Safety Threshold
    safety_impact: SIL-HAZ          # Hazardous
    evidence_required:
      - FHA reference
      - H2 safety procedure review
      - DER sign-off
    resolution_sla: 72h             # Maximum 72 hours
    audit_level: DETAILED           # Full audit trail
```

---

## References

| Reference | Document |
|-----------|----------|
| **MDC** | Model Digital Constitution (AEROSPACEMODEL root) |
| **TLI v2.1** | Top-Level Instruction Specification, version 2.1 |
| **BREX-DE** | BREX Decision Engine (`ASIGT/brex/brex_decision_engine.py`) |
| **CNOT-ARCH** | CNOT Agent Lifecycle Architecture (`docs/CNOT_AGENT_LIFECYCLE_ARCHITECTURE.md`) |
| **EU AI Act** | Regulation (EU) 2024/1689 — Articles 6, 9, 12–15 |
| **EASA AI RM 2.0** | EASA Artificial Intelligence Roadmap 2.0 (2024) |
| **HCDS Charter v1.0** | Human-Centric Digital Systems Charter |
| **ARP4754A** | SAE ARP4754A — Development of Civil Aircraft and Systems |
| **ARP4761** | SAE ARP4761 — Safety Assessment Process |
| **DO-178C** | RTCA DO-178C — Software Considerations in Airborne Systems |

---

**Document End**

AEROSPACEMODEL-ASIT-NIB-SPEC-001 v1.0 DRAFT  
© 2026 Amedeo Pelliccia / IDEALEeu Enterprise  
Released under CC0-1.0 (Public Domain Dedication)
