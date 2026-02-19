# Differentiation Note — C2.1 Criticality-Aware Quantum Resource Orchestrator

**Docket:** AQUA-V-C2.1-2026-001  
**Date:** 2026-02-19

---

## 1. Technical Problem Solved

C2.1 solves the problem of **safely deploying quantum computing in operational safety-critical systems**. The specific problem: a quantum backend that is fast enough for one workload type (e.g., route optimisation at 200 ms) may be too slow for another (real-time structural health monitoring at 5 ms). Without criticality-aware orchestration, either: (a) safety-critical workloads share a queue with background workloads and miss deadlines, or (b) separate dedicated backends are provisioned (prohibitively expensive).

## 2. Why the Solution Is Non-Obvious

1. **QW1–QW4 classification with specific millisecond deadlines** is non-obvious for quantum computing. Real-time scheduling theory (ARINC 653, Liu & Layland) is well-known, but applying it to quantum circuits requires understanding that quantum circuits have non-deterministic execution times dependent on noise and queue depth — making deadline enforcement non-trivial.

2. **Pre-validated classical fallback designation** is non-obvious: it requires that the orchestrator, at submission time, identify and reserve a classical backend that is already validated for the specific workload type. This forward-looking reservation mechanism does not exist in any quantum scheduler.

3. **Noise × circuit_depth as a noise proxy** in the composite score is non-obvious: it combines two parameters from different domains (quantum hardware characterisation and circuit design) into a single quality proxy that predicts result fidelity.

## 3. Inventive Step Beyond Closest Prior Art

**Closest: IBM Qiskit Runtime**

| Feature | Qiskit Runtime | C2.1 | Delta |
|---|---|---|---|
| Priority | Session priority tiers | QW1–QW4 safety criticality | Safety-specific classification |
| Deadline | Configurable timeout | 5 ms hard QW1 deadline | Hard safety bound |
| Fallback | Retry on failure | Pre-validated classical fallback | Forward-looking reservation |
| Evidence | Job result storage | Cryptographic evidence log | Regulatory compliance |
| Noise-aware selection | Backend calibration data available | Noise × circuit_depth composite score | Active noise-latency scoring |

## 4. Connection to AQUA-V Architecture

C2.1 is the **operational scheduler** of QAOS. It bridges the QAOS backend resource pool and the requesting operational systems. Its evidence log is the source material for C2.3 (Evidence Ledger). Its fallback mechanism ensures that C1.2 DERs can always be generated (classical fallback also generates DERs). Human oversight hooks satisfy EU AI Act Article 14 for high-risk AI systems.

## 5. EU AI Act Alignment

Under EU AI Act Annex III, AI systems used in safety-critical operations (transport, critical infrastructure) are high-risk. C2.1's human oversight hook for QW1 results directly implements the human oversight requirement of EU AI Act Article 14 — making C2.1 a claim with direct EU regulatory significance beyond patent law.
