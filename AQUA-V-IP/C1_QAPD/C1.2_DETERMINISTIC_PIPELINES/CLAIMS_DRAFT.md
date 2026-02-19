# Claims Draft — C1.2 Deterministic Reproducibility Pipelines

**Title:** Deterministic Reproducibility Pipeline for Quantum-Assisted Design Computations in Safety-Critical Systems  
**Docket:** AQUA-V-C1.2-2026-001  
**Parent:** AQUA-V-P0-2026-001  
**Date:** 2026-02-19  
**Priority:** ★ HIGHEST PRIORITY — EP filing target: 2026-03-05 at EPO (Munich, EU)  
**Style:** EPO / USPTO Dual-Format

> **Drafting note:** C1.2 contains the strongest novel claims in the portfolio. These claims should be drafted conservatively (narrow but clearly allowable) to ensure grant, with broader claims pursued via divisional.

---

## CLAIMS

### Independent Claim 1 — Method

**1.** A computer-implemented method for ensuring deterministic reproducibility of quantum-assisted design computations in a safety-critical system, the method comprising:

(a) generating a global seed value by computing a cryptographic hash function over a canonical serialisation of all input data to a quantum computation, and deriving the global seed from a fixed-length prefix of the hash value;

(b) computing a cryptographic hash of the input data and recording a solver version identifier that uniquely identifies the quantum software stack, backend hardware identifier, and compiler version used for the computation;

(c) executing the quantum computation using the global seed to initialise all pseudo-random number generators employed within the quantum algorithm, wherein the quantum computation produces a set of candidate solutions ranked by an objective function value;

(d) generating a cryptographic evidence record comprising: the global seed value; the cryptographic hash of the input data; the solver version identifier; a representation of a top-k ranked subset of the candidate solutions; a cryptographic hash of the top-k ranked subset; and a digital signature computed over all preceding fields using an asymmetric key pair, wherein the digital signature key is managed under a hardware security module (HSM); and

(e) storing the cryptographic evidence record in a persistent evidence store, wherein the stored record enables exact reconstruction of the top-k ranked subset by any party with access to the evidence record, without re-executing the quantum computation on quantum hardware.

---

### Independent Claim 2 — System

**2.** A system for ensuring deterministic reproducibility of quantum-assisted design computations in a safety-critical system, the system comprising:

one or more classical processors;

a hardware security module (HSM);

a non-transitory memory storing instructions that, when executed by the one or more classical processors, cause the system to perform operations comprising:

generating a global seed value from a cryptographic hash of canonical input data;

recording a solver version identifier for the quantum software stack and backend;

executing a quantum computation with the global seed applied to all pseudo-random number generators;

generating a cryptographic evidence record comprising the global seed, input hash, solver version identifier, top-k results, result hash, and an HSM-computed digital signature; and

storing the cryptographic evidence record in a persistent evidence store.

---

### Independent Claim 3 — Computer Program Product

**3.** A non-transitory computer-readable medium storing instructions that, when executed by one or more processors, cause the processors to perform a method for ensuring deterministic reproducibility of quantum-assisted design computations in a safety-critical system, the method comprising:

generating a global seed from a cryptographic hash of canonical input data;

recording a solver version identifier;

executing a quantum computation with the global seed;

generating a cryptographic evidence record comprising the global seed, input hash, solver version identifier, top-k ranked results, result hash, and a digital signature; and

storing the cryptographic evidence record in a persistent evidence store enabling reconstruction of the top-k results without re-executing on quantum hardware.

---

### Dependent Claims

**4.** The method of claim 1, wherein generating the global seed value comprises computing a SHA-256 hash over the canonical serialisation of the input data and deriving the global seed as the first 64 bits of the SHA-256 hash value, wherein the canonical serialisation is a deterministic byte representation of the input data obtained by applying a canonical JSON serialisation with lexicographically sorted keys and no whitespace.

**5.** The method of claim 1, wherein the solver version identifier comprises: a first field identifying the quantum algorithm name; a second field identifying the software library name and version number; a third field identifying the backend hardware or simulator identifier; and a fourth field identifying the circuit compiler version, wherein each field is a non-empty string and the combination of all four fields uniquely identifies the quantum software configuration.

**6.** The method of claim 1, wherein executing the quantum computation comprises: if a quantum processing unit (QPU) backend is available and selected, executing the quantum circuit on the QPU and recording the hardware-returned measurement results directly in the evidence record; and if a classical simulation backend is selected, executing the quantum circuit simulation with the global seed applied to the shot-sampling pseudo-random number generator such that re-simulation with the same seed and circuit produces an identical measurement result distribution.

**7.** The method of claim 1, wherein the digital signature in the cryptographic evidence record is computed using the Elliptic Curve Digital Signature Algorithm (ECDSA) with the P-384 curve over a canonical serialisation of all fields of the evidence record excluding the digital signature field, and wherein the HSM is compliant with FIPS 140-2 Level 3 or the EU eIDAS Regulation qualified electronic signature requirements.

**8.** The method of claim 1, wherein the cryptographic evidence record further comprises a lifecycle phase identifier selected from a set of defined lifecycle phase identifiers corresponding to stages of an aerospace system development lifecycle, and wherein the lifecycle phase identifier identifies the development stage at which the quantum computation was performed.

**9.** The method of claim 8, wherein the lifecycle phase identifier corresponds to one of: a system architecture phase; a detailed design phase; a verification phase; or a certification evidence phase; and wherein the evidence store enforces that a record with a certification evidence phase identifier is immutable after creation.

**10.** The method of claim 1, further comprising: transmitting the cryptographic evidence record to a regulatory compliance packaging system that generates a compliance artefact comprising: a machine-readable traceability record linking the evidence record to one or more requirements in a system requirements specification; a human-readable summary of the quantum computation configuration; and metadata formatted for submission to a certification authority.

**11.** The method of claim 1, wherein the safety-critical system is an aircraft and the method further comprises: associating the cryptographic evidence record with a Design Assurance Level (DAL) indicator derived from a functional hazard assessment of the aircraft function for which the quantum computation was performed; and requiring human approval before storing the evidence record in the evidence store if the DAL indicator corresponds to DAL A or DAL B.

**12.** The method of claim 1, further comprising verifying the integrity of a previously stored cryptographic evidence record by: recomputing the cryptographic hash of the top-k ranked subset from the stored representation; comparing the recomputed hash to the stored result hash field; and verifying the digital signature using the public key corresponding to the HSM key identified by the signing key identifier field; wherein a mismatch in either comparison causes the evidence record to be flagged as tampered.

**13.** The method of claim 1, wherein the quantum computation comprises execution of a Quantum Approximate Optimisation Algorithm (QAOA), and wherein the global seed is applied to the initialisation of the QAOA variational parameters and to the shot-sampling pseudo-random number generator, such that two independent executions with the same global seed, same circuit, and same simulator backend return an identical top-k ranked result set.

**14.** The system of claim 2, wherein the system further comprises an evidence store that is an append-only, cryptographically linked log such that each stored evidence record contains a hash of the previous record in the log, forming a tamper-evident chain of design computation records across a product development lifecycle.

**15.** The computer program product of claim 3, wherein the instructions further cause the processors to: generate a reconstruction verification report by retrieving a stored evidence record; computing the canonical serialisation of the top-k results; computing the SHA-256 hash of the canonical serialisation; and comparing the computed hash to the result hash stored in the evidence record; and reporting whether the evidence record integrity is verified or failed.

---

## EPO Prosecution Notes

**Art. 52 EPC Framing:**
The claimed method produces a concrete technical effect: a cryptographic evidence record that enables deterministic reconstruction of quantum computation results for use in aerospace certification. This is a technical process operating on technical data (quantum measurement results, cryptographic hashes) and producing a technical output (a digitally signed artefact that satisfies regulatory traceability requirements). It is not a mathematical method per se (T 0258/03).

**Novelty anchor (Art. 54 EPC):**
No prior art discloses: (a) global seed derivation from SHA-256 of input data + (b) solver version recording + (c) evidence record with digital signature + (d) reconstruction capability from stored record, in combination for safety-critical quantum computations.

**Inventive step (Art. 56 EPC):**
Starting from the closest prior art (quantum computation logging / DO-178C tool qualification), the non-obvious step is the specific combination of: input-derived seed (ensures same inputs → same seed, independent of wall-clock time), result storage (handles non-deterministic QPU hardware), digital signature (tamper evidence), and lifecycle phase binding (regulatory integration).

---

*★ Highest priority child claim — target EP filing at EPO (Munich, EU) by 2026-03-05.*  
*All claims to be reviewed and finalised by European Patent Attorney registered at EPO before filing.*
