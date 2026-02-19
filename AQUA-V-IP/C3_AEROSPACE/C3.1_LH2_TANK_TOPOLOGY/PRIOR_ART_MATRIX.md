# Prior Art Matrix — C3.1 LH₂ Tank Topology Optimisation

**Docket:** AQUA-V-C3.1-2026-001  
**Date:** 2026-02-19

---

| Reference | Date | What It Covers | What It Does NOT Cover (AQUA-V Gap) | Risk Level |
|---|---|---|---|---|
| **QUBO for aircraft load optimisation** ([Springer 2024](https://link.springer.com/article/10.1007/s11128-024-04569-6)) | 2024 | QUBO encoding of structural loads in aircraft; binary topology variables | Cryogenic constraints (−253°C); H₂ material compatibility; ATA 28 routing compatibility; deterministic evidence record; certification traceability | Medium |
| **Optimised QUBO formulation methods** ([arXiv:2406.07681](https://arxiv.org/abs/2406.07681)) | 2024 | QUBO constraint satisfaction; penalty methods | LH₂-specific constraints; cryogenic material selection; galvanic compatibility; EASA substantiation | Low |
| **Airbus hydrogen propulsion research** ([Airbus ZEROe programme](https://www.airbus.com/en/innovation/low-carbon-aviation/hydrogen)) | 2020–2025 | LH₂ tank concepts for A320 fuselage; structural integration; material selection | QUBO optimisation; deterministic evidence records; quantum-assisted topology; SSOT promotion | **High** |
| **ATA 28 H₂ Cryogenic domain** (AEROSPACEMODEL this repo, ATA 28 instructions) | 2026 | LH₂ tank requirements; cryogenic material constraints; ATA 28-11 | Part of the same IP family — used as specification basis, not prior art | N/A |
| **Digital twins in aerospace** ([Nature 2024](https://www.nature.com/articles/s43588-024-00613-8)) | 2024 | DT for structural design; simulation integration | Quantum topology optimisation; QUBO formulation; cryogenic penalty terms | Low |
| **Classical topology optimisation (SIMP)** ([Sigmund 2001](https://link.springer.com/article/10.1007/s001580050176)) | 2001 | Continuous density topology optimisation; SIMP penalisation | Discrete material selection; cryogenic constraints; H₂ compatibility; quantum computation | Low |

## Gap Analysis

The Airbus ZEROe research is the highest-risk reference for the *problem domain* (LH₂ tank structural integration). However, it uses classical design methods. C3.1 is differentiated by: QUBO encoding of the topology problem, cryogenic and material compatibility penalty terms, and quantum-assisted execution with DER. The specific combination is not found in any prior art.
