# Claims Draft — P0 Parent Architecture

**Title:** Artificial Quantum Unified Architectures for Hybrid Product Development and Operational Optimization  
**Docket:** AQUA-V-P0-2026-001  
**Date:** 2026-02-19  
**Style:** EPO / USPTO Dual-Format

> **Drafting note:** These are preliminary claims for discussion. Final claims will be refined by qualified patent counsel prior to filing.

---

## CLAIMS

### Independent Claim 1 — Method

**1.** A computer-implemented method for hybrid quantum-classical product development and operational optimisation in a safety-critical system, the method comprising:

(a) receiving, by one or more processors, a set of design parameters and a set of domain-specific constraints associated with a product to be developed, wherein the domain-specific constraints comprise at least one of: material compatibility constraints, thermal operating bounds, regulatory compliance bounds, or failure mode probability bounds derived from a safety assessment;

(b) encoding the design parameters and domain-specific constraints as a Quadratic Unconstrained Binary Optimisation (QUBO) instance using a hybrid discrete-continuous mapping that maps continuous design parameters to binary registers and incorporates the domain-specific constraints as penalty terms in a QUBO cost matrix;

(c) generating a global deterministic seed value derived from a cryptographic hash of the QUBO instance inputs, recording a solver version identifier corresponding to a quantum processing unit (QPU) backend or hybrid quantum-classical solver to be used, and executing the QUBO instance on the QPU backend or hybrid solver with the global deterministic seed applied to any pseudo-random number generator used in the execution;

(d) generating a cryptographic evidence record that binds together: the global deterministic seed, the cryptographic hash of the QUBO instance inputs, the solver version identifier, a representation of a top-k ranked solution set returned by the execution, and a digital signature over the foregoing fields, wherein the cryptographic evidence record enables exact reconstruction of the top-k ranked solution set from the record without re-executing the QUBO instance on quantum hardware;

(e) promoting, upon satisfaction of a validation criterion, a validated design derived from the top-k ranked solution set to a Single Source of Truth (SSOT) repository together with a reference to the cryptographic evidence record, wherein the SSOT repository is a governed data store accessible to both design-time and operational systems; and

(f) synchronising an operational digital twin of the product with the validated design and the cryptographic evidence record, wherein each state transition of the operational digital twin is associated with the cryptographic evidence record that caused it.

---

### Independent Claim 2 — System

**2.** A system for hybrid quantum-classical product development and operational optimisation in a safety-critical system, the system comprising:

one or more classical processors;

at least one quantum processing unit (QPU) or access to a hybrid quantum-classical solver service;

a non-transitory memory storing instructions that, when executed by the one or more classical processors, cause the system to perform operations comprising:

(a) receiving a set of design parameters and domain-specific constraints;

(b) encoding the design parameters and domain-specific constraints as a QUBO instance using a hybrid discrete-continuous mapping;

(c) generating a global deterministic seed, recording a solver version identifier, and executing the QUBO instance with deterministic seeding;

(d) generating a cryptographic evidence record binding the deterministic seed, input hash, solver version, top-k results, and a digital signature;

(e) promoting a validated design to a Single Source of Truth (SSOT) repository with a reference to the cryptographic evidence record; and

(f) synchronising an operational digital twin with the validated design and the cryptographic evidence record.

---

### Independent Claim 3 — Computer Program Product

**3.** A non-transitory computer-readable medium storing instructions that, when executed by one or more processors, cause the processors to perform a method for hybrid quantum-classical product development and operational optimisation in a safety-critical system, the method comprising:

receiving a set of design parameters and domain-specific constraints associated with a product;

encoding the design parameters and domain-specific constraints as a QUBO instance using a hybrid discrete-continuous mapping incorporating the domain-specific constraints as penalty terms;

generating a global deterministic seed derived from a cryptographic hash of the QUBO instance inputs and executing the QUBO instance with the deterministic seed;

generating a cryptographic evidence record binding the deterministic seed, input hash, solver version identifier, top-k ranked results, and a digital signature;

promoting a validated design to a Single Source of Truth (SSOT) repository with a reference to the cryptographic evidence record; and

synchronising an operational digital twin with the validated design, wherein each digital twin state transition is associated with the cryptographic evidence record that caused it.

---

### Dependent Claims

**4.** The method of claim 1, wherein the safety-critical system is an aircraft and the domain-specific constraints comprise at least one of: cryogenic temperature bounds for a liquid hydrogen fuel system operating at or below −253°C; structural load path constraints derived from a finite element model; aerodynamic performance bounds; or Design Assurance Level (DAL) failure probability bounds from an ARP4761 safety assessment.

**5.** The method of claim 1, wherein encoding the design parameters as a QUBO instance comprises encoding structural topology selection as a set of binary variables, encoding material selection from a compatibility matrix as a set of binary variables, and constructing a penalty term for each domain-specific constraint as a quadratic function of the binary variables.

**6.** The method of claim 1, wherein executing the QUBO instance comprises executing a Quantum Approximate Optimisation Algorithm (QAOA) with a circuit depth parameter p on the QPU backend, and wherein, if the QPU backend is unavailable or fails to return a result within a configurable timeout, automatically falling back to a classical simulated annealing solver using the same global deterministic seed.

**7.** The method of claim 1, wherein the cryptographic evidence record is formatted as a data structure compliant with a lifecycle evidence packaging specification tied to a lifecycle phase identifier selected from LC03, LC04, LC05, LC06, LC07, or LC08.

**8.** The method of claim 1, further comprising classifying operational quantum workloads into a plurality of criticality classes comprising: a first class (QW1) for safety-critical workloads having a response deadline of 5 milliseconds or less; a second class (QW2) for mission-critical workloads having a response deadline of 100 milliseconds or less; a third class (QW3) for operational workloads having a response deadline of 1 second or less; and a fourth class (QW4) for background workloads without a hard deadline; and selecting a quantum or classical backend for each workload based on the criticality class and measured backend latency and noise metrics.

**9.** The method of claim 8, wherein a QW1 workload that cannot be served by any available quantum backend within the 5 millisecond deadline is automatically routed to a pre-validated classical fallback backend, and wherein this fallback event is recorded in the cryptographic evidence record.

**10.** The method of claim 1, wherein promoting the validated design to the SSOT repository is conditioned on a human approval step for designs that affect a safety-critical function classified at Design Assurance Level A or B.

**11.** The method of claim 1, wherein generating the global deterministic seed comprises computing a SHA-256 hash of a canonical serialisation of the QUBO input dataset, and deriving the global seed as the first 64 bits of the SHA-256 hash value.

**12.** The method of claim 1, wherein the digital signature in the cryptographic evidence record is computed using an asymmetric signature scheme over a canonical serialisation of all other fields of the evidence record, and wherein the signing key is managed under a hardware security module (HSM) compliant with FIPS 140-2 Level 3 or equivalent.

**13.** The method of claim 1, wherein the operational digital twin is synchronised at a first level of fidelity using the validated design, and subsequently at a second, higher level of fidelity using operational sensor data, wherein each fidelity-level update references the cryptographic evidence record associated with the design basis of the twin.

**14.** The system of claim 2, wherein the system further comprises a governance rule engine configured to enforce contract-gated operations, wherein each operation that modifies the SSOT repository requires a valid contract identifier matching a pre-registered contract stored in a contract registry.

**15.** The computer program product of claim 3, wherein the instructions further cause the processors to generate compliance packaging artefacts for the cryptographic evidence record formatted for submission to a regulatory authority, the compliance packaging artefacts comprising: a machine-readable traceability record linking the evidence record to requirements in a system requirements specification; a human-readable summary of the quantum computation configuration; and a verification status field indicating the lifecycle phase at which the evidence record was generated.

---

## EPO-Format Claim Summary

*Per EPO Guidelines for Examination, Part F, Chapter IV:*

- **Independent claims:** 1 (method), 2 (system), 3 (CRM) — three categories
- **Dependent claims:** 4–15 (method dependent on claim 1, except 14 dependent on claim 2 and 15 on claim 3)
- **Total claims:** 15
- **Independent claim count:** 3 (within EPO's typical single-category preferred practice; however, three categories are permissible as "problem-solution" set)

---

## USPTO-Format Notes

*Per MPEP § 608.01(n):*

- Claims 1, 2, 3 are independent
- Claims 4–13, 15 are dependent on method claim 1 or CRM claim 3
- Claim 14 is dependent on system claim 2
- Alice/§ 101 framing: claims are directed to a specific computer-implemented process with concrete technical effect (deterministic reproducibility enabling aerospace certification audit trails)

---

*Preliminary draft only. All claims to be reviewed and finalised by registered patent counsel.*
