# Invention Disclosure — C4.3 ESG Portfolio Optimisation

**Title:** Quantum-Assisted ESG Portfolio Optimisation Under EU Taxonomy and Sustainability Regulatory Constraints  
**Docket:** AQUA-V-C4.3-2026-001  
**Parent Docket:** AQUA-V-P0-2026-001  
**Date:** 2026-02-19

---

## 1. Inventors

| Name | Role | Contribution |
|---|---|---|
| **Amedeo Pelliccia** | Primary Inventor | ESG QUBO formulation; EU Taxonomy constraint encoding; QAOS QW4 integration |

---

## 2. Technical Problem

Aerospace companies subject to EU Corporate Sustainability Reporting Directive (CSRD) and EU Taxonomy Regulation must optimise their technology investment portfolios to:
1. Maximise alignment with EU Taxonomy "Do No Significant Harm" (DNSH) criteria
2. Meet Scope 1/2/3 emission reduction targets under net-zero trajectories
3. Satisfy EU Taxonomy minimum social safeguards (aligned with OECD Guidelines and UN Guiding Principles)
4. Balance R&D investment across technology readiness levels to maintain technology pipeline

This is a multi-objective combinatorial optimisation problem with regulatory constraints from EU Taxonomy (EU Regulation 2020/852) and CSRD (Directive 2022/2464/EU).

---

## 3. Description of the Invention

### 3.1 ESG QUBO Formulation

Technology investments are encoded as binary variables. The QUBO cost matrix incorporates:
- **EU Taxonomy alignment penalty**: Penalises investment combinations that do not meet the minimum threshold of EU Taxonomy-aligned economic activities (>50% of CapEx in Taxonomy-aligned activities)
- **DNSH compliance penalty**: Penalises investment combinations that cause significant harm to any of the six EU Taxonomy environmental objectives
- **Emission reduction trajectory penalty**: Penalises investment portfolios that produce a Scope 1/2/3 trajectory incompatible with a 1.5°C-aligned net-zero pathway
- **TRL balance penalty**: Penalises portfolio compositions that concentrate too heavily in high-TRL (near-commercial) or low-TRL (basic research) investments

### 3.2 QAOS Integration

ESG portfolio optimisation is classified as QW4 (background, best-effort). QAOS routes it to idle quantum backends. The DER ensures that portfolio decisions are auditable for CSRD disclosure purposes.

### 3.3 EU Regulatory Novelty

Embedding **EU Taxonomy DNSH criteria** as QUBO penalty terms is a novel application of quantum computing to EU regulatory compliance. The penalty terms directly encode EU law (Article 17 of EU Regulation 2020/852) into the optimisation objective.

---

## 4. Embodiment

**Primary:** AQUA-V technology investment portfolio optimisation for AEROSPACEMODEL — quarterly ESG portfolio re-balancing using QAOS QW4.

**Secondary:** EU-regulated infrastructure operator (energy, transport) portfolio optimisation under CSRD reporting requirements.

---

*EP independent application at EPO (Munich, EU) — target: 2029–2031.*
