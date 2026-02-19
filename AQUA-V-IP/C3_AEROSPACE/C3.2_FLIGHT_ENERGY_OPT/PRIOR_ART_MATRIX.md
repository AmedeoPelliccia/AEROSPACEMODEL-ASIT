# Prior Art Matrix — C3.2 Flight Energy Optimisation

**Docket:** AQUA-V-C3.2-2026-001  
**Date:** 2026-02-19

---

| Reference | Date | What It Covers | What It Does NOT Cover (AQUA-V Gap) | Risk Level |
|---|---|---|---|---|
| **QUBO for aircraft loads** ([Springer 2024](https://link.springer.com/article/10.1007/s11128-024-04569-6)) | 2024 | QUBO for structural load distribution | Flight energy; boil-off; fuel cell operating envelope; route optimisation | Low |
| **Airbus ZEROe hydrogen programme** ([Airbus](https://www.airbus.com/en/innovation/low-carbon-aviation/hydrogen)) | 2022–2025 | LH₂ propulsion concepts; boil-off management; fuel cell integration | QUBO optimisation; quantum-assisted energy optimisation; deterministic evidence records | Medium |
| **Classical trajectory optimisation** (Betts 2010; GPOPS-II) | 2010–2025 | Direct collocation; pseudospectral methods; fuel-optimal trajectories | Hydrogen-specific constraints; boil-off; quantum computation; QUBO encoding | Low |
| **Quantum computing for vehicle routing** ([multiple arXiv papers]) | 2020–2025 | QUBO/QAOA for vehicle routing; combinatorial route optimisation | Hydrogen boil-off constraints; fuel cell envelope; H₂ purity; BWB CG management | Medium |
| **Digital twins in aerospace** ([Nature 2024](https://www.nature.com/articles/s43588-024-00613-8)) | 2024 | DT for operational optimisation | Quantum energy optimisation; QUBO formulation; H₂-specific constraints | Low |

## Gap Analysis

The closest prior art is the combination of (1) quantum vehicle routing QUBO papers + (2) Airbus hydrogen propulsion. Neither source combines QUBO formulation with hydrogen-specific penalty terms. The boil-off + fuel cell envelope + H₂ purity combination is unique to BWB-H₂ flight energy optimisation.
