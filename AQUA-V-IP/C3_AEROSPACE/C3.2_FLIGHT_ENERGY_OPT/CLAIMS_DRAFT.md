# Claims Draft — C3.2 Flight Energy Optimisation

**Docket:** AQUA-V-C3.2-2026-001  
**Date:** 2026-02-19  
**Style:** EPO format (EU-first)

---

## CLAIMS

### Independent Claim 1 — Method

**1.** A computer-implemented method for optimising flight energy consumption of a hydrogen-powered aircraft, the method comprising:

(a) receiving a flight mission specification comprising at least an origin, a destination, a departure time, an initial liquid hydrogen fuel quantity, and a set of airspace constraints;

(b) encoding a joint optimisation problem comprising route selection, altitude profile, speed profile, and fuel allocation decisions as a Quadratic Unconstrained Binary Optimisation (QUBO) instance, wherein the QUBO cost matrix incorporates:
  (i) a liquid hydrogen boil-off penalty term that penalises route and altitude decisions that increase boil-off losses as a function of flight duration and thermal environment;
  (ii) a fuel cell operating envelope penalty term that penalises thrust allocation decisions that cause fuel cell stack temperature, pressure, or load to exceed certified operating bounds;
  (iii) an H₂ purity constraint penalty term that penalises fuel usage rates inconsistent with H₂ purity threshold requirements; and
  (iv) an airspace feasibility penalty term that penalises route segments that violate applicable airspace restrictions;

(c) executing the QUBO instance via a criticality-aware quantum resource orchestrator, classifying the workload as a mission-critical class workload with a response deadline commensurate with flight planning requirements;

(d) generating a cryptographic evidence record for the QUBO execution; and

(e) returning the optimal flight plan from the top-k ranked solutions, together with the cryptographic evidence record.

---

### Dependent Claims

**2.** The method of claim 1, wherein the liquid hydrogen boil-off penalty term is parameterised by a boil-off rate model that estimates the rate of boil-off as a function of flight altitude, ambient temperature, and tank insulation characteristics, and wherein the penalty coefficient is proportional to the expected boil-off mass loss over the flight duration.

**3.** The method of claim 1, wherein the QUBO instance is re-executed during flight as a quantum resource orchestrator QW3 workload to update the flight plan based on updated weather data, airspace restrictions, or fuel system measurements, and wherein each in-flight re-optimisation generates an updated cryptographic evidence record linked to the previous evidence record.

**4.** The method of claim 1, wherein the aircraft is a blended wing body aircraft and the QUBO cost matrix further incorporates a centre-of-gravity management penalty term that penalises fuel allocation sequences that drive the centre-of-gravity outside the blended wing body flight envelope.

---

*EP divisional — target filing at EPO (Munich, EU) after first simulation validation.*
