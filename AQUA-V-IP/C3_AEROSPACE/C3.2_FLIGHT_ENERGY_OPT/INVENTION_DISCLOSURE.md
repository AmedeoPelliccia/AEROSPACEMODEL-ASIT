# Invention Disclosure — C3.2 Flight Energy Optimisation

**Title:** Hybrid Quantum-Classical Flight Energy Optimisation for Hydrogen-Powered Blended Wing Body Aircraft  
**Docket:** AQUA-V-C3.2-2026-001  
**Parent Docket:** AQUA-V-P0-2026-001  
**Date:** 2026-02-19

---

## 1. Inventors

| Name | Role | Contribution |
|---|---|---|
| **Amedeo Pelliccia** | Primary Inventor | Flight energy QUBO formulation; BWB-H₂ operational constraint encoding; QAOS QW2 integration; energy optimisation objective |

---

## 2. Technical Problem

BWB-H₂ aircraft energy management is significantly more complex than conventional jet-fuel aircraft:
1. LH₂ boil-off is a continuous fuel loss mechanism — optimal routing must account for boil-off rate as a function of flight time and altitude
2. Fuel cell power output varies non-linearly with temperature, pressure, and load — optimal thrust allocation is a mixed-integer problem
3. H₂ purity requirements constrain acceptable fuel usage rates (ISO 14687-2)
4. The combined route optimisation + fuel allocation + boil-off management problem is NP-hard and not tractable for classical exact solvers at commercial scale

This problem is a natural QAOA/QUBO target — but the aerospace-specific constraints (boil-off, fuel cell characteristics, H₂ purity) are not present in any existing quantum optimisation formulation.

---

## 3. Description of the Invention

### 3.1 Problem Encoding

The flight energy problem is encoded as a multi-objective QUBO:

**Objective:** Minimise total energy consumption per flight (H₂ mass consumed + boil-off loss)

**Constraints:**
- Route feasibility (waypoint sequence, airspace restrictions)
- Fuel cell operating envelope (temperature, pressure, load bounds)
- LH₂ tank pressure management (boil-off venting vs. recovery)
- H₂ purity threshold enforcement

**QAOS integration:** The energy optimisation workload is classified as QW2 (mission-critical, ≤100 ms) for pre-departure planning and QW3 (operational) for in-flight re-optimisation.

### 3.2 Deterministic Evidence

Each QAOS QW2 execution for pre-departure energy planning generates a DER, creating a complete audit trail from flight plan approval to quantum computation evidence.

---

## 4. Embodiment

**Primary:** AMPEL360 BWB-H₂ long-range flight profile optimisation — route + altitude + speed profile + fuel allocation joint optimisation.

**Secondary:** Short-range BWB shuttle with frequent departure cycles — in-flight re-optimisation via QAOS QW3.

---

*Confidential — EP divisional at EPO (Munich, EU) after first simulation validation.*
