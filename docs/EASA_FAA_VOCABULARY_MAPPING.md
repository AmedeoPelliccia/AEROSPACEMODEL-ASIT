# EASA/FAA Vocabulary Mapping

## Purpose

This document provides a mapping between AEROSPACEMODEL terminology and equivalent or related concepts in EASA (European Union Aviation Safety Agency) and FAA (Federal Aviation Administration) regulatory frameworks.

## Regulatory Context

The terms defined in AEROSPACEMODEL align with the following regulatory frameworks:
- **EASA**: Part 21 (Certification), Part 145 (Maintenance Organizations), CS-25 (Large Aircraft)
- **FAA**: 14 CFR Part 21 (Certification), Part 25 (Airworthiness Standards), Part 43 (Maintenance)
- **Standards**: ATA iSpec 2200, S1000D, ATA 100, DO-178C (Software), DO-254 (Hardware)

---

## Term Mappings

### 1. Digital Continuity

**AEROSPACEMODEL Definition:**
> The ability to preserve identity, configuration, authority, semantics, and evidence of aircraft data across all lifecycle stages (design, certification, production, operation, sustainment).

**EASA Equivalent:**
- **Term:** Configuration Management (CM) + Continued Airworthiness
- **Regulatory Basis:** 
  - EASA Part 21 Subpart D (Design Organisation Approval - DOA)
  - EASA Part 21.A.3A (Type Certificate Data)
  - EASA Part M (Continuing Airworthiness)
- **Reference Documents:**
  - AMC 21.A.3A - Configuration Management
  - CS-25 Book 1 (Design Data Requirements)

**FAA Equivalent:**
- **Term:** Configuration Management + Type Design Definition
- **Regulatory Basis:**
  - 14 CFR §21.31 (Type Design)
  - 14 CFR §21.50 (Instructions for Continued Airworthiness - ICA)
  - AC 21-50 (Instructions for Continued Airworthiness)
- **Reference Documents:**
  - FAA Order 8110.4C (Type Certification)

---

### 2. Broken Bridge / Broken Link

**AEROSPACEMODEL Definition:**
> A structural discontinuity at a process or tool interface where identity, configuration, semantics, authority, or evidence is lost or degraded.

**EASA Equivalent:**
- **Term:** Data Integrity Failure / Traceability Gap
- **Regulatory Basis:**
  - EASA Part 21.A.90 (Investigations of design failures)
  - EASA Part 21.A.3B(c) (Change Management)
  - AMC 20-115C (Software Considerations for Airborne Systems)
- **Safety Implication:** May lead to non-compliance with design approval requirements

**FAA Equivalent:**
- **Term:** Data Integrity Breach / Chain of Custody Failure
- **Regulatory Basis:**
  - 14 CFR §21.3 (Reporting of Failures)
  - AC 20-115D (Airborne Software Assurance)
  - FAA Order 8110.49A (Software Approval Guidelines)
- **Safety Implication:** Compromises airworthiness compliance evidence

---

### 3. Transformation Contract

**AEROSPACEMODEL Definition:**
> A formal, explicit specification that governs how information is transformed from one lifecycle context to another.

**EASA Equivalent:**
- **Term:** Interface Control Document (ICD) + Change Control Process
- **Regulatory Basis:**
  - EASA Part 21.A.91 (Design Changes)
  - EASA Part 21.A.3B (Design Data Management)
  - AMC 21.A.3B (Data Management and Configuration Control)

**FAA Equivalent:**
- **Term:** Design Change Control / Configuration Control Process
- **Regulatory Basis:**
  - 14 CFR §21.93 (Classification of Changes)
  - 14 CFR §21.97 (Approval of Major Design Changes)
  - AC 21.101-1 (Establishing Type Design)

---

### 4. Top-Level Instruction (TLI)

**AEROSPACEMODEL Definition:**
> A high-level, domain-licensed instruction that defines what is allowed to be done with data, not just how.

**EASA Equivalent:**
- **Term:** Certification Specification (CS) / Certification Basis
- **Regulatory Basis:**
  - EASA Part 21.A.17 (Type Certification Basis)
  - EASA Part 21.A.15 (Application for Type Certificate)
  - CS-25 (Certification Specifications for Large Aeroplanes)

**FAA Equivalent:**
- **Term:** Type Certification Basis / Special Conditions
- **Regulatory Basis:**
  - 14 CFR §21.17 (Designation of Applicable Regulations)
  - 14 CFR §21.16 (Special Conditions)
  - 14 CFR Part 25 (Airworthiness Standards)

---

### 5. SPCA – Software Programming Chain Application

**AEROSPACEMODEL Definition:**
> The executable programming chain that enforces transformation contracts across heterogeneous software ecosystems.

**EASA Equivalent:**
- **Term:** Software Configuration Management (SCM) System
- **Regulatory Basis:**
  - DO-178C Section 7 (Software Configuration Management)
  - EASA AMC 20-115C (Software Development Assurance)
  - Part 21.A.239 (Software Management)

**FAA Equivalent:**
- **Term:** Software Configuration Index (SCI) / Build Process
- **Regulatory Basis:**
  - AC 20-115D (Airborne Software Assurance)
  - DO-178C Level A-E (Software Level Determination)
  - FAA Order 8110.49A (Software Review)

---

### 6. Non-Inference Boundary

**AEROSPACEMODEL Definition:**
> A formally defined point where automation must stop because ambiguity cannot be resolved deterministically.

**EASA Equivalent:**
- **Term:** Design Approval Boundary / Engineering Authority Hold Point
- **Regulatory Basis:**
  - EASA Part 21.A.263 (Continuing airworthiness documents)
  - AMC 25.1309 (System Safety Assessment - Hold Points)
  - CS-25.1309 (Equipment, Systems, and Installations)

**FAA Equivalent:**
- **Term:** Designated Engineering Representative (DER) Approval Point
- **Regulatory Basis:**
  - 14 CFR §21.47 (Holder's Responsibilities)
  - AC 25.1309-1A (System Safety Analysis)
  - FAA Order 8100.16 (DER Procedures)

---

### 7. Human-in-the-Loop (HITL)

**AEROSPACEMODEL Definition:**
> Explicit, auditable human intervention triggered only at predefined non-inference boundaries.

**EASA Equivalent:**
- **Term:** Engineering Authority Approval / Design Approval
- **Regulatory Basis:**
  - EASA Part 21.A.20 (Compliance Demonstration)
  - EASA Part-M App.I (Technical Records)
  - AMC 20-115C (Human Oversight Requirements)

**FAA Equivalent:**
- **Term:** Engineering Authorization / Designated Approval
- **Regulatory Basis:**
  - 14 CFR §21.35 (Authorized Signatories)
  - AC 20-174 (Development of Civil Aircraft and Systems)
  - FAA Order 8110.4C (Type Certification - Human Approval)

---

### 8. Multiagent Domino

**AEROSPACEMODEL Definition:**
> A cascading failure pattern where locally valid outputs from chained agents propagate upstream errors into systemic lifecycle corruption.

**EASA Equivalent:**
- **Term:** Common Cause Failure / Cascading Failure
- **Regulatory Basis:**
  - CS-25.1309 (System Safety - Common Mode Analysis)
  - AMC 25.1309 (Common Cause Analysis)
  - EASA Part 21.A.90A (Investigation of Failures)

**FAA Equivalent:**
- **Term:** Common Mode Failure / Cascading System Failure
- **Regulatory Basis:**
  - 14 CFR §25.1309 (Equipment, Systems, and Installations)
  - AC 25.1309-1A (System Design and Analysis)
  - ARP4761 (Safety Assessment Process)

---

### 9. ABDB – Aircraft Blended Digital Body

**AEROSPACEMODEL Definition:**
> A System of Systems that represents the twin process of the aircraft lifecycle, not just its geometry.

**EASA Equivalent:**
- **Term:** Type Design Definition + Continuing Airworthiness Data
- **Regulatory Basis:**
  - EASA Part 21.A.31 (Type Design)
  - EASA Part 21.A.120A (Digital Data Management)
  - Part-M (Continuing Airworthiness Management)

**FAA Equivalent:**
- **Term:** Type Design + Type Certificate Data Sheet (TCDS)
- **Regulatory Basis:**
  - 14 CFR §21.31 (Type Design Definition)
  - 14 CFR §21.50 (Instructions for Continued Airworthiness)
  - FAA Order 8110.4C (Type Certification Process)

---

### 10. Twin Process

**AEROSPACEMODEL Definition:**
> A digital construct that mirrors how the aircraft is designed, certified, operated, and evolved, rather than how it looks or behaves physically.

**EASA Equivalent:**
- **Term:** Lifecycle Management System / Product Lifecycle Model
- **Regulatory Basis:**
  - EASA Part 21.A.4 (Organisation Structure)
  - EASA Part-M (Continuing Airworthiness)
  - AMC 21.A.239 (Design Lifecycle)

**FAA Equivalent:**
- **Term:** Product Lifecycle Management (PLM) / Design Lifecycle
- **Regulatory Basis:**
  - 14 CFR Part 21 (Complete Lifecycle)
  - AC 21-50 (Lifecycle Documentation)
  - FAA Order 8110.54 (Design Lifecycle Management)

---

### 11. System of Systems (SoS)

**AEROSPACEMODEL Definition:**
> An architecture where independently managed systems are orchestrated to produce a coherent lifecycle capability without replacing them.

**EASA Equivalent:**
- **Term:** Integrated System Architecture / Aircraft System Architecture
- **Regulatory Basis:**
  - CS-25.1301 (Function and Installation - Systems)
  - CS-25.1309 (System Safety Assessment)
  - AMC 25.1309 (Integrated Systems Analysis)

**FAA Equivalent:**
- **Term:** Integrated Aircraft Systems / System Architecture
- **Regulatory Basis:**
  - 14 CFR §25.1301 (Function and Installation)
  - 14 CFR §25.1309 (Equipment, Systems, Installations)
  - AC 25.1309-1A (Integrated Systems Safety Assessment)

---

### 12. ATA-Level Structuring

**AEROSPACEMODEL Definition:**
> Decomposition of transformation logic according to ATA chapters.

**EASA Equivalent:**
- **Term:** ATA iSpec 2200 Chapter Structure
- **Regulatory Basis:**
  - EASA Part-M Appendix I (Technical Records - ATA Structure)
  - EASA Part-145 (Maintenance Organization - ATA References)
  - AMC 20-8 (ATA Chapter Applicability)

**FAA Equivalent:**
- **Term:** ATA 100 / iSpec 2200 System Breakdown
- **Regulatory Basis:**
  - 14 CFR §43.13 (Maintenance Standards - ATA Reference)
  - 14 CFR §145.109 (Recordkeeping - ATA Chapters)
  - AC 43-9 (Maintenance Records - ATA Structure)

---

### 13. ASIT – Aircraft/System Information Transformer

**AEROSPACEMODEL Definition:**
> A deterministic transformation component that applies rule-based conversions where no inference is required.

**EASA Equivalent:**
- **Term:** Data Processing System (Deterministic) / Configuration Data Management
- **Regulatory Basis:**
  - EASA Part 21.A.3B (Design Data Management)
  - DO-178C (Deterministic Software)
  - AMC 21.A.239 (Software Tools)

**FAA Equivalent:**
- **Term:** Configuration Control System / Data Management System
- **Regulatory Basis:**
  - 14 CFR §21.3 (Data Integrity)
  - AC 20-115D (Software Tool Qualification)
  - DO-178C (Deterministic Transformation)

---

### 14. ASIGT – Aircraft/System Information Generative Transformer

**AEROSPACEMODEL Definition:**
> A generative transformer/transponder that produces lifecycle artifacts within strict contractual and ATA-scoped boundaries.

**EASA Equivalent:**
- **Term:** Computer-Aided Design (CAD) System / Generative Design Tool (with Constraints)
- **Regulatory Basis:**
  - EASA Part 21.A.239 (Software Qualification)
  - AMC 20-115C (Tool Qualification Requirements)
  - CS-AI (Emerging AI Regulation - In Development)

**FAA Equivalent:**
- **Term:** Design Tool / Configuration-Constrained Generation System
- **Regulatory Basis:**
  - 14 CFR §21.3(a) (Computer-Based Tools)
  - AC 20-115D (Tool Qualification)
  - DO-178C (Tool Qualification for Generative Systems)

---

### 15. Generative (Regulator-Safe Meaning)

**AEROSPACEMODEL Definition:**
> Generation that is derivative, constrained, and contract-bound, not open-ended or creative.

**EASA Equivalent:**
- **Term:** Deterministic Derivation / Constrained Generation
- **Regulatory Basis:**
  - AMC 20-115C (Derived Data Requirements)
  - EASA Part 21.A.33 (Derived Design Data)
  - DO-178C Table A-5 (Derived Requirements)

**FAA Equivalent:**
- **Term:** Derived Design Data / Constrained Automation
- **Regulatory Basis:**
  - AC 20-115D (Derived Data Definition)
  - 14 CFR §21.35(b) (Derived Design)
  - DO-178C Section 5.4 (Derived Requirements)

---

### 16. Quantum-Circuit–Inspired Logic

**AEROSPACEMODEL Definition:**
> A control-theoretic execution model where transformations behave like explicit gates rather than implicit data flows.

**EASA Equivalent:**
- **Term:** State Machine Logic / Formal Methods
- **Regulatory Basis:**
  - DO-178C (Formal Methods - Supplement DO-333)
  - AMC 20-115C (Formal Verification)
  - CS-25.1309 (System Logic Requirements)

**FAA Equivalent:**
- **Term:** Formal Methods / State-Based Verification
- **Regulatory Basis:**
  - AC 20-115D (Formal Methods)
  - DO-333 (Formal Methods Supplement to DO-178C)
  - 14 CFR §25.1309 (Logic Analysis)

---

### 17. CNOT – Control Neural Origin Transaction

**AEROSPACEMODEL Definition:**
> A transformation gate that executes only if the authoritative control state is valid.

**EASA Equivalent:**
- **Term:** Conditional Approval / Gated Release Process
- **Regulatory Basis:**
  - EASA Part 21.A.91 (Design Change Approval Gate)
  - Part 21.A.3B (Conditional Data Release)
  - AMC 21.A.3B (Gate Review Process)

**FAA Equivalent:**
- **Term:** Stage Gate Approval / Conditional Release
- **Regulatory Basis:**
  - 14 CFR §21.93 (Change Classification Gate)
  - 14 CFR §21.97 (Approval Gate)
  - AC 21.101-1 (Stage Gate Review)

---

### 18. State Collapse

**AEROSPACEMODEL Definition:**
> The moment when lifecycle ambiguity (variants, effectivity, context) is resolved into a concrete, usable artifact.

**EASA Equivalent:**
- **Term:** Effectivity Resolution / Configuration Freeze
- **Regulatory Basis:**
  - EASA Part 21.A.3A (Configuration Control)
  - Part-M App.I (Effectivity Statement)
  - AMC 21.A.3A (Baseline Establishment)

**FAA Equivalent:**
- **Term:** Effectivity Determination / Configuration Definition
- **Regulatory Basis:**
  - 14 CFR §21.31 (Type Design Freeze)
  - 14 CFR §21.50 (Effectivity Statement)
  - AC 21-50 (Configuration Baseline)

---

### 19. Provenance Vector

**AEROSPACEMODEL Definition:**
> A machine-readable record that links every output to source artifacts, transformation contracts, execution context, and human decisions.

**EASA Equivalent:**
- **Term:** Design Traceability Matrix / Compliance Evidence
- **Regulatory Basis:**
  - EASA Part 21.A.20B (Traceability Requirements)
  - Part-M App.I (Technical Records)
  - AMC 20-115C (Traceability Data)

**FAA Equivalent:**
- **Term:** Compliance Documentation / Traceability Matrix
- **Regulatory Basis:**
  - 14 CFR §21.33 (Inspection and Tests)
  - 14 CFR §21.50 (Evidence Records)
  - AC 20-174 (Development Assurance - Traceability)

---

### 20. Revolution Without Disruption

**AEROSPACEMODEL Definition:**
> A transformation strategy that improves lifecycle automation and assurance without replacing certified tools, invalidating approvals, or destabilizing programs.

**EASA Equivalent:**
- **Term:** Incremental Approval / Progressive Certification
- **Regulatory Basis:**
  - EASA Part 21.A.15B (Phased Type Certification)
  - Part 21.A.21 (Incremental Compliance Demonstration)
  - AMC 21.A.15 (Staged Certification)

**FAA Equivalent:**
- **Term:** Phased Certification / Incremental Compliance
- **Regulatory Basis:**
  - 14 CFR §21.17(b) (Staged Compliance)
  - AC 21-40 (Guide for Obtaining a Type Certificate)
  - FAA Order 8110.4C (Phased Approval Process)

---

## Cross-Reference Matrix

| AEROSPACEMODEL Term | Primary EASA Reference | Primary FAA Reference | Related Standard |
|---------------------|------------------------|----------------------|------------------|
| Digital Continuity | Part 21.A.3A | 14 CFR §21.31 | S1000D Issue 5.0 |
| Broken Bridge | AMC 20-115C | AC 20-115D | DO-178C |
| Transformation Contract | Part 21.A.3B | 14 CFR §21.93 | ATA iSpec 2200 |
| Top-Level Instruction | CS-25 | 14 CFR Part 25 | ARP4754A |
| SPCA | DO-178C Sec. 7 | AC 20-115D | DO-178C |
| Non-Inference Boundary | AMC 25.1309 | AC 25.1309-1A | ARP4761 |
| Human-in-the-Loop | Part 21.A.20 | 14 CFR §21.35 | DO-178C |
| Multiagent Domino | CS-25.1309 | 14 CFR §25.1309 | ARP4761 |
| ABDB | Part 21.A.31 | 14 CFR §21.31 | S1000D, ATA100 |
| Twin Process | Part-M | 14 CFR Part 21 | ISO 10303-242 |
| System of Systems | CS-25.1309 | 14 CFR §25.1309 | ARP4754A |
| ATA-Level Structuring | Part-M App.I | 14 CFR §43.13 | ATA iSpec 2200 |
| ASIT | Part 21.A.3B | AC 20-115D | DO-178C |
| ASIGT | AMC 20-115C | AC 20-115D | DO-178C + DO-333 |
| Generative (Safe) | DO-178C Table A-5 | AC 20-115D | DO-178C |
| Quantum Logic | DO-333 | DO-333 | DO-333 |
| CNOT | Part 21.A.91 | 14 CFR §21.93 | ISO 9001 |
| State Collapse | Part 21.A.3A | 14 CFR §21.31 | S1000D |
| Provenance Vector | Part 21.A.20B | 14 CFR §21.33 | LOTAR/MIL-STD-31000 |
| Revolution w/o Disruption | Part 21.A.15B | AC 21-40 | ARP4754A |

---

## Regulatory Alignment Summary

### EASA Key Documents
1. **Part 21** - Certification of Aircraft and Related Products, Parts and Appliances
2. **CS-25** - Certification Specifications for Large Aeroplanes
3. **AMC 20-115C** - Airborne Software Assurance
4. **Part-M** - Continuing Airworthiness Requirements
5. **Part-145** - Maintenance Organization Approvals

### FAA Key Documents
1. **14 CFR Part 21** - Certification Procedures for Products and Articles
2. **14 CFR Part 25** - Airworthiness Standards: Transport Category Airplanes
3. **AC 20-115D** - Airborne Software Assurance
4. **AC 21-50** - Instructions for Continued Airworthiness and Manufacturer's Maintenance Manuals
5. **FAA Order 8110.4C** - Type Certification

### Industry Standards
1. **S1000D Issue 5.0** - International specification for technical publications
2. **ATA iSpec 2200** - Information Standards for Aviation Maintenance
3. **DO-178C** - Software Considerations in Airborne Systems and Equipment Certification
4. **DO-333** - Formal Methods Supplement to DO-178C
5. **ARP4754A** - Guidelines for Development of Civil Aircraft and Systems
6. **ARP4761** - Guidelines and Methods for Conducting the Safety Assessment Process

---

## Compliance Notes

### Certification Context
All AEROSPACEMODEL terms align with established regulatory concepts but provide a **modernized digital framework** that:
- Maintains full regulatory compliance
- Enables automation within governed boundaries
- Preserves human authority and oversight
- Ensures complete traceability and auditability

### AI/ML Considerations
As regulators develop AI-specific guidance (EASA AI Roadmap 2.0, FAA AI Assurance), AEROSPACEMODEL's approach provides:
- **Bounded Generation** - Aligns with deterministic certification requirements
- **Human Oversight** - Maintains required engineering authority
- **Traceability** - Provides complete evidence chains
- **Safety Assurance** - Operates within established safety assessment frameworks

---

## Document Control

| Item | Value |
|------|-------|
| **Version** | 1.0 |
| **Date** | 2026-02-02 |
| **Status** | Active |
| **Owner** | AEROSPACEMODEL Documentation Team |
| **Review Date** | 2026-08-02 |

---

## References

### EASA Documents
- EASA Part 21 - https://www.easa.europa.eu/en/document-library/regulations/easa-part-21-regulation
- CS-25 - https://www.easa.europa.eu/en/document-library/certification-specifications/cs-25-large-aeroplanes
- AMC 20-115C - https://www.easa.europa.eu/en/document-library/acceptable-means-of-compliance-and-guidance-materials

### FAA Documents
- 14 CFR Parts 21, 25, 43, 145 - https://www.ecfr.gov/
- Advisory Circulars - https://www.faa.gov/regulations_policies/advisory_circulars/
- FAA Orders - https://www.faa.gov/regulations_policies/orders_notices/

### Industry Standards
- S1000D - http://www.s1000d.org/
- ATA iSpec 2200 - https://www.ataebiz.org/
- SAE ARP Standards - https://www.sae.org/standards/

---

*This mapping is maintained as a living document and updated as regulatory guidance evolves.*
