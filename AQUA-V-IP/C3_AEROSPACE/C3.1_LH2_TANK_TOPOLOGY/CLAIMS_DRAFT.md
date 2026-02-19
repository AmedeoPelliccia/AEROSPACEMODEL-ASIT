# Claims Draft — C3.1 LH₂ Tank Topology Optimisation

**Docket:** AQUA-V-C3.1-2026-001  
**Date:** 2026-02-19  
**Style:** EPO format (EU-first)

---

## CLAIMS

### Independent Claim 1 — Method

**1.** A computer-implemented method for optimising the structural topology of a liquid hydrogen (LH₂) fuel tank for integration into an aircraft fuselage, the method comprising:

(a) defining a structural topology design space comprising a plurality of discrete structural element configurations, each configuration specifying at least a material selection from a materials catalogue and a structural connectivity pattern;

(b) encoding the structural topology design space as a Quadratic Unconstrained Binary Optimisation (QUBO) instance, wherein the QUBO cost matrix incorporates:
  (i) a cryogenic thermal penalty term that penalises material selections that exhibit structural integrity degradation at operating temperatures at or below −253°C, with a penalty coefficient derived from a thermal stress severity function evaluated at cryogenic operating conditions;
  (ii) a hydrogen material compatibility penalty term that penalises structural configurations that create galvanic coupling between materials that are incompatible with liquid hydrogen contact, based on a hydrogen material compatibility matrix;
  (iii) a multi-load structural integrity penalty term that penalises configurations for which a structural analysis model predicts failure under at least one of: ground handling loads, flight manoeuvre loads, cryogenic thermal loads, or internal pressure loads; and
  (iv) a fuel system routing compatibility penalty term that penalises structural configurations that obstruct or conflict with a predefined liquid hydrogen distribution system routing plan;

(c) executing the QUBO instance on a quantum processing unit or hybrid quantum-classical solver with a global deterministic seed;

(d) generating a cryptographic evidence record as described in claim 1 of application AQUA-V-C1.2-2026-001 for the QUBO execution;

(e) selecting a structural topology from the top-k ranked solutions of the QUBO execution; and

(f) promoting the selected structural topology to a Single Source of Truth (SSOT) repository together with the cryptographic evidence record, subject to structural certification substantiation review.

---

### Dependent Claims

**2.** The method of claim 1, wherein the hydrogen material compatibility matrix classifies each material in the materials catalogue as compatible or incompatible with liquid hydrogen exposure, and wherein the penalty term penalises any structural configuration that assigns an incompatible material to a structural element in direct contact with liquid hydrogen or hydrogen vapour.

**3.** The method of claim 1, wherein the aircraft fuselage is a blended wing body (BWB) fuselage, and wherein the QUBO cost matrix further incorporates a centre-of-gravity envelope penalty term that penalises structural topologies for which the combined LH₂ tank and fuel mass produces a centre-of-gravity position outside the certified flight envelope of the BWB aircraft.

**4.** The method of claim 1, wherein the cryptographic evidence record is formatted for submission to a regulatory authority under EASA CS-25 Subpart D (Design and Construction) and includes a reference to the applicable special condition for hydrogen fuel systems.

---

*EP divisional — target filing at EPO (Munich, EU) upon BWB-H₂ TRL ≥ 4.*
