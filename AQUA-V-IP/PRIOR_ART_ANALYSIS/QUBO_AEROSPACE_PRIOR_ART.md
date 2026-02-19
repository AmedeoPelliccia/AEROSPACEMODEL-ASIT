# QUBO Aerospace Prior Art Analysis

**Portfolio:** AQUA-V  
**Date:** 2026-02-19  
**Scope:** QUBO formulations applied to aerospace optimisation problems  
**Registry:** EPO patent register (Espacenet) + academic literature

---

## Overview

This document consolidates prior art analysis for QUBO-based aerospace optimisation across the C1.1, C3.1, and C3.2 child applications. It focuses on references that teach or suggest QUBO encoding of aerospace design or operational problems.

---

## Reference Table

| # | Reference | Date | URL | What It Covers | AQUA-V Gap | Risk |
|---|---|---|---|---|---|---|
| 1 | **QUBO formulation for aircraft load optimisation** (Springer Quantum Information Processing) | 2024 | [link.springer.com/article/10.1007/s11128-024-04569-6](https://link.springer.com/article/10.1007/s11128-024-04569-6) | QUBO encoding of structural load distribution in aircraft fuselage; binary variable representation of load path selection; penalty terms for load balance constraints | Does not address: continuous variable encoding; cryogenic constraints; H₂ material compatibility; multi-load case with thermal loads; ATA 28 routing; deterministic evidence records; certification traceability | Medium |
| 2 | **Optimised QUBO formulation methods** (arXiv) | 2024 | [arxiv.org/abs/2406.07681](https://arxiv.org/abs/2406.07681) | Systematic methods for reducing QUBO matrix size; constraint satisfaction in QUBO; slack variable introduction; penalty coefficient selection | Generic methods applicable to any domain; no aerospace-specific constraints; no physical motivation for penalty coefficients; no certification integration | Medium |
| 3 | **Qubit-efficient QUBO encoding** (arXiv) | 2025 | [arxiv.org/abs/2509.08080](https://arxiv.org/abs/2509.08080) | Variable encoding efficiency for large QUBO instances; qubit count reduction; domain wall encoding | Pure qubit compression; no aerospace constraint types; no cryogenic/material/DAL penalty terms; no deterministic seeding or evidence chain | Low |
| 4 | **QAOA for combinatorial optimisation** Farhi et al. | 2014 | [arxiv.org/abs/1411.4028](https://arxiv.org/abs/1411.4028) | Quantum Approximate Optimisation Algorithm; MaxCut and combinatorial problems; circuit depth parameter p | Foundation algorithm only; no aerospace application; no deterministic seeding; no evidence records | Low |
| 5 | **Quantum annealing for aircraft scheduling** (D-Wave, multiple) | 2019–2025 | [dwavesys.com](https://www.dwavesys.com/solutions-and-products/aerospace/) | Flight scheduling; gate assignment; crew rostering; baggage routing using QUBO on annealing hardware | Scheduling only (not design topology); no cryogenic/material/DAL constraints; no deterministic evidence; no certification | Medium |
| 6 | **QUBO for vehicle routing** (multiple arXiv) | 2020–2025 | [arxiv.org/search/?query=QUBO+vehicle+routing](https://arxiv.org/search/?query=QUBO+vehicle+routing) | Capacitated vehicle routing; TSP; delivery scheduling via QUBO | Generic routing; no hydrogen boil-off; no fuel cell envelope; no flight trajectory constraints | Low |

---

## Consolidated Gap Analysis

### What the QUBO aerospace literature collectively covers:
- Binary structural load path selection (discrete topology)
- Flight scheduling and gate assignment (combinatorial scheduling)
- Generic constraint satisfaction and penalty methods
- QAOA algorithm theory and extensions

### What no QUBO aerospace reference covers (AQUA-V novelty space):
1. **Cryogenic thermal penalty terms** scaled by thermomechanical severity at −253°C
2. **Hydrogen material compatibility penalty terms** based on galvanic coupling and H₂-compatibility catalogues
3. **DAL-classified failure probability bounds** as QUBO penalty coefficients derived from ARP4761 assessments
4. **ATA chapter-referenced constraint schema** mapping QUBO penalty terms to regulatory documents
5. **Deterministic evidence records** (seed + hash + version + results + signature) for certification
6. **Continuous variable binary register encoding** with precision derived from design sensitivity analysis
7. **SSOT promotion gate** conditioning design decisions on DER validity
8. **Liquid hydrogen boil-off penalty** parameterised by flight duration and thermal model
9. **Fuel cell operating envelope penalty** translating fuel cell characteristic curves to QUBO

---

## Prosecution Implications

For EPO examination, the combination of any two adjacent rows in the gap analysis above is non-obvious because it requires simultaneous expertise in quantum computing and aerospace engineering discipline (structures, thermodynamics, certification, regulatory). This "two-expert problem" is the core inventive step argument across C1.1, C3.1, and C3.2.

*Full Espacenet search to be performed by European Patent Attorney (EPA) registered at EPO. Search queries: IPC G06N10/60, B64F5/00, G06F30/15; CPC G06N10/40, G06N10/60.*
