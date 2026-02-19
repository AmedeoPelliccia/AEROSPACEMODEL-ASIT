# Invention Disclosure — C4.1 Quantum-Assisted Supply Chain Optimisation

**Title:** Quantum-Assisted Multi-Tier Aerospace Supply Chain Optimisation with Regulatory Compliance Constraints  
**Docket:** AQUA-V-C4.1-2026-001  
**Parent Docket:** AQUA-V-P0-2026-001  
**Date:** 2026-02-19

---

## 1. Inventors

| Name | Role | Contribution |
|---|---|---|
| **Amedeo Pelliccia** | Primary Inventor | Supply chain QUBO formulation; regulatory compliance constraint encoding; QAOS QW3 integration |

---

## 2. Technical Problem

Multi-tier aerospace supply chain scheduling must simultaneously satisfy:
1. **Production capacity constraints**: Tier-1, Tier-2, Tier-3 supplier capacities
2. **Lead time constraints**: Part delivery windows for aircraft final assembly
3. **Regulatory constraints**: REACH (chemical substance restrictions), conflict minerals (EU Regulation 2017/821), export control (ITAR, EAR for non-EU suppliers)
4. **Disruption recovery**: Geopolitical disruptions, supplier failures — rapid re-scheduling required

The combined problem is a multi-dimensional vehicle routing + scheduling + constraint satisfaction problem that is NP-hard and not tractable for classical exact solvers at commercial scale (>100 suppliers, >1000 part types).

---

## 3. Description of the Invention

### 3.1 QUBO Formulation

The supply chain scheduling problem is encoded as a QUBO with:
- **Supplier selection variables**: Binary selection of alternative suppliers for each part
- **Delivery window penalty**: Penalises schedules that violate assembly line sequencing windows
- **REACH compliance penalty**: Penalises supplier selections that include substances on the REACH SVHC list
- **Conflict minerals penalty**: Penalises suppliers sourcing from conflict-affected areas per EU Regulation 2017/821
- **Export control penalty**: Penalises non-EU supplier combinations that trigger ITAR/EAR licensing requirements

### 3.2 QAOS Integration

Supply chain re-scheduling is a QW3 workload (≤1 s deadline). QAOS routes it to an appropriate backend based on urgency. DERs are generated for all re-scheduling decisions.

### 3.3 EU Regulatory Alignment

The REACH and conflict minerals penalty terms directly implement EU regulatory requirements. The QUBO formulation embeds EU law into the optimisation objective — a novel application of quantum computing to regulatory compliance.

---

## 4. Embodiment

**Primary:** AMPEL360 BWB-H₂ supply chain with 200+ suppliers, optimising for delivery windows, REACH compliance, and EU conflict minerals regulation, with QAOS QW3 re-scheduling during disruptions.

---

*EP independent application at EPO (Munich, EU) — target: 2029.*
