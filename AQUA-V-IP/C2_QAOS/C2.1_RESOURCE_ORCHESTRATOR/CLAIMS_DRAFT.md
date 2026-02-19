# Claims Draft — C2.1 Criticality-Aware Quantum Resource Orchestrator

**Title:** Criticality-Aware Quantum Resource Orchestrator with Latency-Bounded Backend Selection  
**Docket:** AQUA-V-C2.1-2026-001  
**Parent:** AQUA-V-P0-2026-001  
**Date:** 2026-02-19  
**Priority:** ★ HIGH PRIORITY — EP filing target: 2026-03-05 at EPO (Munich, EU)  
**Style:** EPO format (EU-first)

---

## CLAIMS

### Independent Claim 1 — Method

**1.** A computer-implemented method for orchestrating quantum computing workloads in a safety-critical operational system, the method comprising:

(a) receiving a quantum computing workload request comprising a quantum circuit to be executed and a workload descriptor, wherein the workload descriptor includes a safety criticality indicator selected from at least a first class corresponding to safety-critical workloads with a response deadline of 5 milliseconds or less and a second class corresponding to non-safety-critical workloads with a longer response deadline;

(b) measuring, for each available quantum or classical computing backend in a resource pool, at least: a current execution latency metric; a gate error rate or equivalent noise metric; and a current queue depth;

(c) computing a composite backend score for each available backend using a scoring function that combines the latency metric, noise metric, and queue depth metric, wherein the scoring function returns an infeasible score for any backend whose measured latency metric exceeds the response deadline associated with the safety criticality indicator;

(d) selecting the backend with the most favourable composite score as a primary backend and designating a pre-validated classical computing backend as a fallback backend;

(e) submitting the quantum circuit to the primary backend for execution and monitoring execution progress against the response deadline;

(f) if the primary backend has not returned a result within the response deadline: routing the workload to the fallback backend; and recording a fallback event in an evidence log associated with the workload; and

(g) returning the result obtained from either the primary or fallback backend, together with the evidence log entry, to the requesting system.

---

### Independent Claim 2 — System

**2.** A system for orchestrating quantum computing workloads in a safety-critical operational system, the system comprising one or more processors and a non-transitory memory storing instructions that, when executed, cause the system to perform the operations of claim 1.

---

### Independent Claim 3 — Computer Program Product

**3.** A non-transitory computer-readable medium storing instructions that, when executed by one or more processors, perform the method of claim 1.

---

### Dependent Claims

**4.** The method of claim 1, wherein the safety criticality indicator is selected from a set of four workload classes comprising: a first class (QW1) for safety-critical workloads with a response deadline of 5 milliseconds or less; a second class (QW2) for mission-critical workloads with a response deadline of 100 milliseconds or less; a third class (QW3) for operational workloads with a response deadline of 1,000 milliseconds or less; and a fourth class (QW4) for background workloads without a hard deadline; and wherein the composite backend scoring function weights the latency metric inversely proportionally to the response deadline of the submitted workload class.

**5.** The method of claim 4, wherein a QW1 workload for which no available quantum or classical backend can meet the 5 millisecond deadline causes the orchestrator to: reject the workload with a deadline-miss notification; invoke a safety hold procedure in the requesting system; and log the deadline-miss event with a timestamp and the list of available backends and their measured latencies.

**6.** The method of claim 1, wherein the fallback backend is a classical computing backend that has been pre-validated for the specific workload type by executing the classical algorithm on a reference dataset and verifying that the output meets a specified quality threshold, and wherein the pre-validation result is stored in the evidence log as a pre-validation record.

**7.** The method of claim 1, wherein the composite backend score is computed as a weighted sum: S = w₁ × (latency / deadline) + w₂ × (noise × circuit_depth) + w₃ × (queue_depth × avg_job_time / deadline), where w₁, w₂, w₃ are configurable weight parameters, and wherein any backend for which latency / deadline > 1.0 receives an infeasible score that prevents its selection.

**8.** The method of claim 1, further comprising: after receiving a result from the primary or fallback backend, generating a cryptographic evidence record binding: the workload identifier, the safety criticality class, the selected backend identifier, the execution latency, an indicator of whether the primary or fallback backend was used, and a hash of the computation result; and storing the evidence record in an append-only evidence ledger.

**9.** The method of claim 8, wherein the evidence record is formatted as a data structure compatible with a lifecycle evidence packaging specification, and wherein a QW1 evidence record that references a fallback execution is automatically escalated to a human oversight review queue before the result is applied to a safety-critical operational state.

**10.** The method of claim 1, wherein measuring the backend latency metric comprises: maintaining a rolling window of recent execution latencies for each backend; computing the 50th percentile (p50) and 95th percentile (p95) latency from the rolling window; and using the p95 latency for QW1 workloads and the p50 latency for QW2, QW3, and QW4 workloads in the composite backend score computation.

**11.** The method of claim 1, wherein the resource pool comprises at least one gate-based quantum processing unit, at least one quantum annealing device, and at least one classical computing backend, and wherein the orchestrator selects among these heterogeneous backends based on: compatibility of the quantum circuit type with the backend architecture; measured backend latency and noise; and the response deadline of the submitted workload class.

**12.** The method of claim 1, wherein the safety-critical operational system is an aircraft and the workload descriptor further comprises an aircraft state vector at the time of workload submission, and wherein the orchestrator adjusts the response deadline for QW1 workloads to a stricter value during safety-critical flight phases identified from the aircraft state vector.

---

## EPO Prosecution Notes

**Technical effect:** The claimed method achieves a concrete technical effect — guaranteed response within a hard deadline for safety-critical quantum workloads via pre-designated classical fallback with recorded evidence — that cannot be achieved by existing quantum job schedulers.

**Novelty:** No quantum cloud scheduler discloses safety criticality classes with hard deadline enforcement and pre-validated classical fallback designation. The QW1–QW4 classification scheme with the 5 ms deadline bound for QW1 is novel.

**Inventive step:** The non-obvious combination is: safety criticality classification (from real-time systems domain) + multi-objective backend scoring (from cloud computing domain) + pre-validated classical fallback (from safety-critical systems domain) + cryptographic evidence log (from C1.2). A person skilled in quantum computing would not combine these without the insight that aerospace safety requirements impose hard deadline constraints incompatible with typical quantum cloud SLAs.

---

*★ High priority — target EP filing at EPO (Munich, EU) by 2026-03-05.*
