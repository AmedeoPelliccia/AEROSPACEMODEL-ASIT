# Differentiation Note — C1.2 Deterministic Reproducibility Pipelines

**Docket:** AQUA-V-C1.2-2026-001  
**Date:** 2026-02-19  
**Priority:** ★ HIGHEST PRIORITY

---

## 1. Technical Problem Solved

C1.2 solves a problem that is **unique to quantum computing in certified systems**: quantum computations are non-deterministic by nature, but certification authorities require that design decisions be reproducible, traceable, and independently verifiable. The specific technical problem is:

> How to generate a compact, tamper-evident evidence record that enables any authorised party to verify (and where possible reconstruct) the outcome of a quantum computation, using only the evidence record, without access to the original quantum hardware, at any point in the future.

This problem does not arise in classical computing (deterministic by default) and has not been addressed in any existing quantum computing service or academic publication.

## 2. Why the Solution Is Non-Obvious

### 2.1 The Input-Derived Seed Is Non-Obvious

A person skilled in quantum computing would know about seeded simulation. However, the **key non-obvious step** is deriving the seed from the SHA-256 hash of the input data — not from a random source or timestamp. This creates a **deterministic, input-bound seed** that:
- Is independently reproducible by any party with access to the input data
- Changes whenever the input data changes (seed tracks input changes)
- Is compact (64 bits) regardless of input data size

This is qualitatively different from simply seeding a PRNG with a random number.

### 2.2 The Evidence Record Structure Is Non-Obvious

The specific combination of fields in the DER is non-obvious:
- Input hash alone does not prove which solver was used
- Solver version alone does not prove which inputs were used
- Top-k results alone do not prove they were not cherry-picked
- The **combination** with digital signature creates a tamper-evident, complete provenance record

### 2.3 HSM Integration for Regulatory Compliance Is Non-Obvious

Using an HSM (FIPS 140-2 / EU eIDAS qualified) to sign the evidence record is non-obvious for a quantum computing application. The motivation comes from aerospace certification practice (DO-178C tool qualification records must be tamper-evident), not from quantum computing practice.

## 3. Inventive Step Beyond Closest Prior Art

**Closest prior art:** Autodesk Certification-Ready Design Digital Twin

| Feature | Autodesk | C1.2 | Delta |
|---|---|---|---|
| Computation type | Classical simulation | Quantum / hybrid | Quantum non-determinism addressed |
| Reproducibility mechanism | Deterministic by default | Seed derivation from input hash | Non-obvious for probabilistic quantum |
| Evidence record | Simulation logs | Compact DER with digital signature | Cryptographic binding + HSM |
| Regulatory packaging | Manual traceability | Machine-generated compliance artefact | Automated certification integration |
| Reconstruction capability | Re-run simulation | Reconstruct from DER without re-execution | Key differentiator |

**Second closest:** Qiskit Aer `seed_simulator` parameter

| Feature | Qiskit Aer | C1.2 | Delta |
|---|---|---|---|
| Seed source | Arbitrary integer | SHA-256 of input data | Input-binding property |
| Evidence record | None | Full DER with signature | Complete provenance |
| QPU support | Simulator only | Both QPU (result storage) and simulator | Hardware non-determinism handled |
| Certification | None | LC-phase binding, regulatory packaging | Certification integration |

## 4. Connection to AQUA-V Architecture

C1.2 is the **integrity backbone** of the entire AQUA-V architecture. Without deterministic evidence records:
- The SSOT promotion gate (P0 Claim 1(e)) has no trustworthy evidence to reference
- The digital twin synchronisation (P0 Claim 1(f)) cannot prove that a DT update was triggered by a verified quantum computation
- The certification evidence ledger (C2.3) has nothing to store

C1.2 claims are designed to be **independently assertable** — they can be infringed by a competitor implementing a quantum computation reproducibility pipeline even without the rest of the AQUA-V architecture. This is why C1.2 is the highest-priority child application.

## 5. Commercial Importance

Any quantum computing service provider that wants to sell to aerospace, defence, or other regulated industries (medical devices, nuclear, rail safety) will need a mechanism equivalent to C1.2. The claim scope deliberately covers the general mechanism, not only the AQUA-V-specific implementation, making this the most commercially valuable child application in the portfolio.

---

*This note is confidential and protected under attorney-client privilege.*
