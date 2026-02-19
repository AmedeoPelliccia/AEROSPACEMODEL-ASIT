# Prior Art Matrix — C1.1 Hybrid QUBO Encoding

**Title:** Hybrid Discrete-Continuous QUBO Encoding for Certified Aerospace Systems  
**Docket:** AQUA-V-C1.1-2026-001  
**Date:** 2026-02-19

---

| Reference | Date | What It Covers | What It Does NOT Cover (AQUA-V Gap) | Risk Level |
|---|---|---|---|---|
| **QUBO formulation for aircraft load optimisation** ([Springer 2024](https://link.springer.com/article/10.1007/s11128-024-04569-6)) | 2024 | QUBO encoding of structural load distribution; binary variable representation | Continuous variable encoding in binary registers; cryogenic material constraints; DAL failure probability bounds; material compatibility matrices; penalty coefficient physical motivation | Medium |
| **Optimised QUBO formulation methods** ([arXiv:2406.07681](https://arxiv.org/abs/2406.07681)) | 2024 | Penalty coefficient optimisation; constraint satisfaction in QUBO; slack variable techniques | Aerospace-specific constraint types; physically motivated coefficients; ATA/DAL/regulatory schema | Medium |
| **Qubit-efficient QUBO** ([arXiv:2509.08080](https://arxiv.org/abs/2509.08080)) | 2025 | Encoding efficiency; qubit count reduction; variable mapping compression | Domain-specific aerospace constraints; hybrid discrete-continuous encoding for certification | Low |
| **D-Wave Ocean SDK documentation** ([D-Wave Systems](https://docs.dwavesys.com)) | 2022–2025 | Generic QUBO construction API; binary variable encoding; constraint penalty methods | Aerospace-specific constraint schema; cryogenic constraints; DAL constraints; ATA-referenced penalty terms | Low |
| **Qiskit Optimisation module** ([IBM Quantum](https://qiskit-community.github.io/qiskit-optimization/)) | 2023–2025 | QuadraticProgram API; constraint-to-QUBO conversion; penalty parameter setting | Aerospace constraint types; physically motivated penalty scaling; hybrid binary-register encoding | Low |
| **Classical topology optimisation — SIMP method** ([Sigmund, Struct Multidisc Optim 2001](https://link.springer.com/article/10.1007/s001580050176)) | 2001 | Density-based structural topology optimisation; continuous density variables; penalisation | Binary/quantum-explorable design space; cryogenic constraints; certification evidence; QUBO formulation | Low |
| **Airbus Digital Twins** ([Airbus 2025](https://www.airbus.com/en/newsroom/stories/2025-04-digital-twins-accelerating-aerospace-innovation-from-design-to-operations)) | 2025 | DT for aerospace structural design; simulation-based design exploration | Quantum computation; QUBO encoding; domain-specific aerospace constraint schema for quantum solvers | Low |

---

## Gap Analysis

The closest prior art is the Springer 2024 QUBO-for-aircraft-loads paper. Key gaps:
1. That paper uses only **discrete binary variables**; C1.1 introduces the hybrid discrete-continuous (binary register) encoding
2. That paper does not encode **cryogenic temperature constraints** (relevant for LH₂ systems)
3. That paper does not include **DAL failure probability bounds** as QUBO penalty terms
4. No paper reviewed maps penalty coefficients to **physical severity metrics** from regulatory documents

*Full patent search to be completed by counsel.*
