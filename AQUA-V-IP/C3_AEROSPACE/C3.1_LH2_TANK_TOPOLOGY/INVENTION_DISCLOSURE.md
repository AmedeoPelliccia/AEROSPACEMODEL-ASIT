# Invention Disclosure — C3.1 LH₂ Tank Topology Optimisation

**Title:** Liquid Hydrogen Tank Structural Topology Optimisation via Hybrid QUBO with Cryogenic and Certification Constraints  
**Docket:** AQUA-V-C3.1-2026-001  
**Parent Docket:** AQUA-V-P0-2026-001  
**Date:** 2026-02-19

---

## 1. Inventors

| Name | Role | Contribution |
|---|---|---|
| **Amedeo Pelliccia** | Primary Inventor | LH₂ tank QUBO formulation; cryogenic constraint encoding; BWB integration topology; certification DAL mapping |

---

## 2. Technical Problem

Blended Wing Body aircraft with liquid hydrogen propulsion (BWB-H₂) requires LH₂ tanks to be structurally integrated into the fuselage. The structural topology optimisation problem for LH₂ tank bays is uniquely challenging:

1. **Cryogenic constraints**: Tank structure must maintain integrity at −253°C (LH₂ boiling point) while the outer fuselage operates near −50°C at cruise altitude — thermal gradient creates differential thermal stress
2. **Hydrogen material compatibility**: Tank internal surfaces must use H₂-compatible alloys (no standard steel); structural members must not create galvanic coupling with H₂-compatible liners
3. **Multi-load case**: Structural topology must satisfy: ground handling loads + flight manoeuvre loads + cryogenic thermal loads + pressure loads simultaneously
4. **Coupled with ATA 28**: Tank topology directly interfaces with the H₂ distribution system (ATA 28 LH₂ transfer lines and valves) — topology changes affect plumbing routing
5. **Certification burden**: Any structural topology requires EASA CS-25 substantiation — the topology decision must be traceable to a DER

This problem cannot be solved by classical topology optimisation (continuous density variables) because the material compatibility constraints are **discrete** (material A or material B at each node, not an interpolation).

---

## 3. Description of the Invention

### 3.1 QUBO Formulation

The LH₂ tank topology problem is encoded as a QUBO instance using C1.1 hybrid discrete-continuous encoding with the following domain-specific penalty terms:

**Cryogenic thermal penalty:**
```
P_cryo = lambda_cryo * SUM_{i: material_i NOT IN cryo_compatible} x_i * thermal_stress_factor_i
```
(Unicode equivalent: P_cryo = λ_cryo × Σ_{i: material_i ∉ cryo_compatible} x_i × thermal_stress_factor_i)

**H₂ material compatibility penalty:**
```
P_h2 = lambda_h2 * SUM_{edge(i,j): galvanic_risk(material_i, material_j) > threshold} x_i * x_j
```
(Unicode equivalent: P_h2 = λ_h2 × Σ_{edge(i,j): galvanic_risk > threshold} x_i × x_j)

**Multi-load structural integrity penalty:**
```
P_struct = lambda_struct * SUM_{load_case k} max(0, sigma_max(x,k) - sigma_allowable(material,cryo=True))^2
```
(Unicode equivalent: P_struct = λ_struct × Σ_{load_case k} max(0, σ_max(x,k) − σ_allowable)²)

**ATA 28 routing compatibility penalty:**
```
P_routing = lambda_route * SUM_{plumbing_node n} conflict(topology_x, h2_line_n)
```
(Unicode equivalent: P_routing = λ_route × Σ_{plumbing_node n} conflict(topology_x, h2_line_n))

### 3.2 Deterministic Evidence

Each QUBO execution generates a DER (C1.2) with `ata_reference = "ATA 28-11"` and `lc_phase = "LC04"`, binding the topology decision to an auditable record.

### 3.3 SSOT Promotion

Winning topology is promoted to SSOT after human approval (CS-25 structural substantiation review). The SSOT record references the DER, making the topology decision traceable to the quantum computation.

---

## 4. Embodiment

**Primary:** AMPEL360 BWB-H₂ aft fuselage LH₂ tank bay topology, with three candidate structural concepts encoded as QUBO binary variables and cryogenic + material + routing constraints.

**Secondary:** Modular sub-tank assembly topology for shorter-range BWB variants.

---

*Confidential — EP divisional to be filed at EPO (Munich, EU) upon BWB-H₂ design maturity (target: 2028).*
