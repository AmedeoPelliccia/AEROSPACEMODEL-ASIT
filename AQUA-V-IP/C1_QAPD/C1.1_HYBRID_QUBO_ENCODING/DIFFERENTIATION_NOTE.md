# Differentiation Note — C1.1 Hybrid QUBO Encoding

**Title:** Hybrid Discrete-Continuous QUBO Encoding for Certified Aerospace Systems  
**Docket:** AQUA-V-C1.1-2026-001  
**Date:** 2026-02-19

---

## 1. Technical Problem Solved

Existing QUBO formulations for aerospace optimisation use only binary (discrete) variables and generic penalty terms. C1.1 solves the problem of encoding **continuous aerospace design parameters** (panel thickness, fuel fraction, structural cross-sections) alongside **discrete topology choices** in a single QUBO instance, while incorporating **domain-specific physical constraints** (cryogenic bounds, material compatibility, DAL failure probabilities) as rigorously scaled quadratic penalty terms with regulatory traceability.

## 2. Why the Solution Is Non-Obvious

A person skilled in quantum optimisation would know how to discretise continuous variables into binary registers. A person skilled in aerospace design would know the relevant constraint types. However, the **non-obvious inventive step** is:

1. **Physically motivated penalty coefficient scaling** — the penalty coefficient for a cryogenic constraint is derived from the thermomechanical severity function, not set arbitrarily as in standard QUBO practice
2. **Regulatory traceability schema** — each penalty term carries a reference to the ATA chapter, DAL level, and regulatory document (CS-25, ARP4761) that motivates it, enabling certification audit
3. **Hybrid encoding for certified systems** — the precision of the binary register is chosen based on design sensitivity analysis, not heuristically, and is itself a documented design decision in the evidence record

## 3. Inventive Step Beyond Closest Prior Art

Closest prior art: Springer 2024 QUBO for aircraft loads.

| Feature | Springer 2024 | C1.1 | Delta |
|---|---|---|---|
| Variable types | Binary only | Binary + continuous register | Hybrid encoding |
| Constraint types | Structural load only | Cryogenic, material compat., DAL, geometric | Domain-specific aerospace schema |
| Penalty coefficient | Heuristic | Physically motivated | Scaled by severity function |
| Regulatory traceability | None | ATA/DAL/CS-25/ARP4761 references | Full certification linkage |

## 4. Connection to AQUA-V Architecture

C1.1 is the **encoding foundation** of QAPD. The hybrid QUBO it generates is the input to C1.2 (Deterministic Pipelines) and C1.3 (Certification Evidence). Without domain-specific encoding, the deterministic evidence record of C1.2 would contain only a hash of a generic QUBO — not a hash of an aerospace-constraint-aware formulation. The domain-specificity of C1.1 is what makes the evidence chain legally defensible for EASA certification.
