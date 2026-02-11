# Formal Response to EASA NPA 2025-07

> **Document ID:** AEROSPACEMODEL-GOV-NPA-2025-07  
> **Type:** Notice of Proposed Amendment (NPA) Response  
> **NPA Reference:** NPA 2025-07 — Artificial Intelligence in Aviation  
> **Respondent:** AEROSPACEMODEL Project  
> **Status:** DRAFT  
> **Date:** 2025-07-01

---

## 1. Introduction

This document constitutes the AEROSPACEMODEL project's formal response
to EASA NPA 2025-07 on the use of artificial intelligence in aviation
systems. The response is structured per EASA Comment-Response Document
(CRD) conventions and addresses each proposed amendment area.

The AEROSPACEMODEL project implements a governance framework that
preempts many of the requirements proposed in NPA 2025-07, as
documented in the [AI Governance Standard](EASA_ESA_AI_GOVERNANCE_STANDARD_v1.0.md)
and the [Digital Constitution](../Model_Digital_Constitution.md).

---

## 2. Executive Summary

AEROSPACEMODEL supports the objectives of NPA 2025-07 and provides
the following position:

| NPA Area | Position | Rationale |
|----------|----------|-----------|
| AI Trustworthiness Framework | **Support** | Aligned with Constitution-bounded governance |
| Human Oversight Requirements | **Support** | Already enforced via Art. 3 and BREX rules |
| Learning Assurance | **Support with comment** | Recommend frozen baselines for certified systems |
| AI Explainability | **Support** | BREX audit trail provides full traceability |
| Risk-Based Classification | **Support** | Mapped to DAL levels and ARP4761 severity |
| Continuing Airworthiness | **Support with comment** | Recommend S1000D integration for AI maintenance data |

---

## 3. Detailed Comments

### 3.1 AI Trustworthiness Framework

**NPA Proposal:** Establish a trustworthiness framework for AI systems
used in aviation, covering reliability, robustness, and security.

**AEROSPACEMODEL Response:**

We **support** this proposal. The AEROSPACEMODEL project implements
trustworthiness through:

- **BREX-constrained generation**: All AI outputs are governed by
  deterministic BREX rules, preventing unconstrained behavior.
- **Contract-based transformations**: Every content transformation
  requires an ASIT-approved contract (BREX-AUTHOR-002).
- **Constitutional limits**: The Digital Constitution (Art. 10)
  provides immutable boundary protection via SHA-256 hash validation.

**Recommendation:** The framework should recognize deterministic,
rule-bounded AI systems as a distinct trustworthiness category with
proportionate assurance requirements.

### 3.2 Human Oversight Requirements

**NPA Proposal:** Mandate human oversight for high-risk AI systems
in aviation operations and maintenance.

**AEROSPACEMODEL Response:**

We **support** this proposal. The AEROSPACEMODEL foundational axiom
explicitly requires:

> *Technology → serves*

Enforcement mechanisms include:

- **Commit-as-contract** (Art. 4): Every AI artifact requires human
  authorship commitment before acceptance.
- **Safety escalation** (Art. 6): Bayesian confidence < 0.92 triggers
  auto-escalation to STK_SAF with a 48-hour SLA.
- **BREX-SAFETY-002**: All safety-related content requires human
  approval before publication.

**Recommendation:** Distinguish between advisory AI (human decides)
and autonomous AI (system decides). AEROSPACEMODEL operates exclusively
in advisory mode.

### 3.3 Learning Assurance

**NPA Proposal:** Define assurance requirements for machine learning
models used in certified aviation systems.

**AEROSPACEMODEL Response:**

We **support with comment**. The AEROSPACEMODEL project uses:

- **Frozen model baselines**: No in-service learning without
  Configuration Control Board (CCB) approval.
- **Deterministic pipelines**: Content generation uses rule-based
  transformations, not learned models.
- **Bayesian twin monitoring**: Statistical models are bounded by
  ARP4761 severity classifications.

**Recommendation:** The NPA should explicitly address:

1. **Rule-based AI systems** that do not use machine learning but
   apply deterministic AI governance.
2. **Baseline management** requirements for ML models in certified
   environments, including version control and rollback procedures.
3. **Data provenance** requirements aligned with S1000D traceability.

### 3.4 AI Explainability

**NPA Proposal:** Require explainability for AI decisions affecting
aviation safety.

**AEROSPACEMODEL Response:**

We **support** this proposal. Every AEROSPACEMODEL AI output is
traceable to:

- The governing BREX rule ID
- The authorizing transformation contract
- The input data source and provenance
- The audit log entry with timestamp

**Recommendation:** Accept BREX audit trails and transformation
contract logs as valid evidence of AI explainability for deterministic
systems.

### 3.5 Risk-Based Classification

**NPA Proposal:** Classify AI systems based on their risk level to
aviation safety.

**AEROSPACEMODEL Response:**

We **support** this proposal. The project maps AI risk to existing
aviation safety classifications:

| AI Risk Level | Aviation Mapping | AEROSPACEMODEL Control |
|--------------|-----------------|----------------------|
| High | DAL A/B, Catastrophic/Hazardous | ARP4761 + STK_SAF + CCB |
| Medium | DAL C, Major | BREX governance + contract |
| Low | DAL D/E, Minor/No Effect | Standard review process |

**Recommendation:** Align AI risk classification with existing
DO-178C Development Assurance Levels to minimize regulatory
fragmentation.

### 3.6 Continuing Airworthiness for AI Systems

**NPA Proposal:** Address AI-specific considerations in continuing
airworthiness requirements.

**AEROSPACEMODEL Response:**

We **support with comment**. The project maintains AI-generated
maintenance content through:

- **S1000D compliance**: All maintenance documentation follows
  S1000D Issue 5.0 structure.
- **Configuration management**: Part 21.A.3A traceability for
  all AI-generated data modules.
- **Digital continuity**: Unbroken data chain from design through
  sustainment.

**Recommendation:** The NPA should:

1. Reference S1000D as an acceptable means of compliance for
   AI-generated maintenance documentation.
2. Define requirements for AI model updates in the context of
   Part-M continuing airworthiness.
3. Address the interaction between AI system updates and existing
   type certificate data.

---

## 4. Cross-Cutting Comments

### 4.1 Regulatory Harmonization

We recommend coordination between:

- **EASA** and **FAA** on AI certification requirements
- **EASA** and **ESA** for dual-use aviation/space AI systems
- **EU AI Act** and aviation-specific AI regulation to avoid
  conflicting requirements

### 4.2 Standards Integration

The NPA should reference and align with:

| Standard | Relevance |
|----------|-----------|
| DO-178C / ED-12C | Software assurance levels for AI |
| DO-333 / ED-216 | Formal methods for AI verification |
| ARP4754A / ED-79A | System development process for AI integration |
| ARP4761 / ED-135 | Safety assessment for AI failure modes |
| S1000D Issue 5.0 | AI-generated technical documentation |

### 4.3 EAARF Forum

We support the establishment of the European Aviation AI Requirements
Framework (EAARF) forum as a venue for ongoing industry–regulator
dialogue. See the [EAARF Charter Draft](EAARF_CHARTER_DRAFT.md).

---

## 5. Conclusion

The AEROSPACEMODEL project's governance framework—grounded in the
Digital Constitution and enforced through BREX rules—demonstrates
that many of the NPA 2025-07 objectives can be achieved through
deterministic, human-overseen AI governance. We welcome further
dialogue with EASA on the proposed amendments.

---

## 6. Related Documents

| Document | Reference |
|----------|-----------|
| AI Governance Standard | [`EASA_ESA_AI_GOVERNANCE_STANDARD_v1.0.md`](EASA_ESA_AI_GOVERNANCE_STANDARD_v1.0.md) |
| Digital Constitution | [`Model_Digital_Constitution.md`](../Model_Digital_Constitution.md) |
| Operational Governance | [`GOVERNANCE.md`](../GOVERNANCE.md) |
| EASA/FAA Vocabulary Mapping | [`docs/EASA_FAA_VOCABULARY_MAPPING.md`](../docs/EASA_FAA_VOCABULARY_MAPPING.md) |
| EAARF Charter | [`EAARF_CHARTER_DRAFT.md`](EAARF_CHARTER_DRAFT.md) |

---

*Governed by the AEROSPACEMODEL Digital Constitution.*
