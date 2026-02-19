# Differentiation Note — C3.2 Flight Energy Optimisation

**Docket:** AQUA-V-C3.2-2026-001  
**Date:** 2026-02-19

---

## 1. Technical Problem Solved

C3.2 solves the NP-hard joint optimisation problem of route + altitude + speed + fuel allocation for hydrogen-powered aircraft, where the hydrogen-specific constraints (boil-off, fuel cell envelope, H₂ purity) make the problem qualitatively different from classical jet fuel flight optimisation.

## 2. Why the Solution Is Non-Obvious

1. **Boil-off penalty term parameterisation** requires aerospace thermodynamics knowledge (tank insulation model, altitude-dependent ambient temperature) — not in any quantum optimisation paper
2. **Fuel cell operating envelope as QUBO penalty** requires translating a continuous fuel cell characteristic curve into a quadratic penalty over discrete operating point choices — a non-obvious discretisation problem
3. **In-flight re-optimisation via QW3 workload** (Claim 3) with evidence record chaining is non-obvious: it creates a temporal chain of evidence records across a single flight, each linked to the previous, enabling post-flight audit of all quantum-assisted decisions

## 3. Inventive Step

Closest prior art combination: quantum vehicle routing QUBO + Airbus hydrogen propulsion. C3.2 adds three non-obvious elements absent from this combination: boil-off penalty, fuel cell envelope penalty, and H₂ purity constraint penalty, each requiring domain-specific knowledge to formulate.

## 4. Connection to AQUA-V Architecture

C3.2 is the **operational mission planning** application of AQUA-V. It uses QAOS (C2.1) for QW2/QW3 scheduling, generates DERs (C1.2) for flight plan auditability, and updates the operational DT (C2.2) with each re-optimisation. It is the clearest demonstration of AQUA-V's DEV→SSOT→Ops cycle in a real-time operational context.
