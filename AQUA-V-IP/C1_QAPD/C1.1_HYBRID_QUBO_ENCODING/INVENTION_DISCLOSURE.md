# Invention Disclosure — C1.1 Hybrid QUBO Encoding

**Title:** Hybrid Discrete-Continuous QUBO Encoding with Domain-Specific Aerospace Constraint Penalty Terms for Certified Systems Design  
**Docket:** AQUA-V-C1.1-2026-001  
**Parent Docket:** AQUA-V-P0-2026-001  
**Date:** 2026-02-19

---

## 1. Inventors

| Name | Role | Contribution |
|---|---|---|
| **Amedeo Pelliccia** | Primary Inventor | QUBO formulation framework; aerospace constraint schema; hybrid encoding methodology |

---

## 2. Technical Problem

Standard QUBO formulations treat all design variables as binary and encode constraints as generic quadratic penalty terms. This is inadequate for aerospace systems design because:

1. Many aerospace design variables are continuous (e.g., panel thickness, fuel fraction, structural member cross-section) — naïve discretisation either loses precision or requires exponentially many qubits
2. Aerospace constraints are domain-specific and physically motivated: cryogenic temperature bounds, material compatibility (e.g., H₂-compatible alloys), DAL-classified failure probability bounds, aerodynamic packaging constraints
3. Standard QUBO libraries (Ocean, Qiskit Optimisation) provide no aerospace constraint primitives
4. The penalty coefficients for aerospace constraints have physical meaning (e.g., a penalty for violating cryogenic bounds must scale with the severity of the thermal stress) — generic formulations set penalty coefficients arbitrarily

---

## 3. Description of the Invention

### 3.1 Hybrid Discrete-Continuous Encoding

The invention introduces a two-tier variable encoding:

**Tier 1 — Binary categorical variables:** Represent discrete design choices
- Material selection from a compatibility matrix (each material is one binary variable)
- Structural topology (each candidate topology is one binary variable)
- Component configuration options

**Tier 2 — Continuous variables in binary registers:** Represent continuous parameters with configurable precision
- A continuous variable x ∈ [x_min, x_max] is encoded as an n-bit binary register: x ≈ x_min + (x_max - x_min) × (Σ_{i=0}^{n-1} b_i × 2^i) / (2^n - 1)
- The precision n is selected based on the sensitivity of the objective function to the variable

### 3.2 Aerospace Constraint Schema

A structured schema maps physical aerospace constraints to QUBO penalty terms:

```python
@dataclass
class AerospaceConstraintPenalty:
    constraint_type: str      # e.g., "cryogenic_thermal", "dal_probability", "material_compatibility"
    penalty_coefficient: float  # Physically motivated scaling
    binary_variables: list    # Indices into QUBO variable vector
    violation_function: callable  # Quadratic form expressing constraint violation
    ata_reference: str        # e.g., "ATA 28-11" for LH₂ tank
    dal_level: str            # "DAL-A", "DAL-B", etc.
    regulatory_ref: str       # e.g., "CS-25.981", "ARP4761 Section 4.3"
```

### 3.3 Penalty Term Construction

For each constraint type:

**Cryogenic thermal constraint:** Penalises material choices that do not maintain structural integrity below −253°C
- Penalty = λ_cryo × Σ_{m ∉ cryo_compatible} b_m × (allocation variable)

**Material compatibility constraint:** Penalises H₂-incompatible materials in fuel system components
- Penalty = λ_mat × Σ_{m ∉ h2_compatible} b_m × (fuel_system_allocation)

**DAL probability bound constraint:** Penalises topologies whose worst-case failure probability exceeds the DAL requirement
- Penalty = λ_dal × max(0, P_failure(topology) − P_DAL_requirement)²

**Geometric packaging constraint:** Penalises configurations that violate CG envelope or volume bounds
- Penalty = λ_geom × max(0, CG_deviation(x) − CG_tolerance)²

---

## 4. Advantages Over Prior Art

| Prior Art | AQUA-V C1.1 Advantage |
|---|---|
| Generic QUBO libraries (Ocean, Qiskit Opt.) | Domain-specific constraint schema with ATA/DAL references; physically motivated penalty scaling |
| QUBO for aircraft loads (Springer 2024) | Extends to continuous variables; adds cryogenic, material, regulatory penalty types |
| Classical topology optimisation (SIMP, etc.) | Quantum-explorable discrete-continuous design space; certification-aware constraint encoding |

---

## 5. Embodiments

### Primary: BWB-H₂ Structural Topology
QUBO encoding of BWB internal bay topology with LH₂ tank placement, incorporating thermal, material, and load path constraints.

### Secondary: Wing Rib Spacing Optimisation
Continuous rib spacing variables discretised to 8-bit registers; constraints from fatigue life and aeroelastic divergence.

---

*Confidential — not for publication before provisional filing.*
