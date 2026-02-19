# Claims Draft — C1.3 Automated Certification Evidence Generation

**Title:** Automated Generation of Aerospace Certification Evidence from Quantum-Assisted Design Computations  
**Docket:** AQUA-V-C1.3-2026-001  
**Parent:** AQUA-V-P0-2026-001  
**Date:** 2026-02-19  
**Style:** EPO format (EU-first)

---

## CLAIMS

### Independent Claim 1 — Method

**1.** A computer-implemented method for automated generation of aerospace certification evidence from quantum-assisted design computations, the method comprising:

(a) retrieving one or more cryptographic evidence records, each evidence record corresponding to a quantum-assisted design computation performed during a development lifecycle phase of an aerospace system, each evidence record comprising at least a cryptographic hash of computation inputs, a solver version identifier, a top-k result set, and a digital signature;

(b) verifying the integrity of each retrieved evidence record by recomputing the hash of the stored top-k result set and verifying the digital signature;

(c) generating a traceability mapping that links each verified evidence record to: one or more requirements in a system requirements specification applicable to the aerospace system; one or more design decisions recorded in a Single Source of Truth (SSOT) repository; and one or more objectives from an applicable aerospace certification standard;

(d) generating a certification evidence package comprising: the verified evidence records; the traceability mapping; regulatory metadata identifying the applicable certification standard, regulatory authority, and aircraft certification basis; and a package integrity record comprising a cryptographic hash of all included content and a qualified electronic signature compliant with an applicable electronic signature regulation; and

(e) transmitting the certification evidence package to a compliance management system for review by a certification authority.

---

### Independent Claim 2 — System

**2.** A system for automated generation of aerospace certification evidence from quantum-assisted design computations, the system comprising one or more processors and instructions that when executed perform the operations of claim 1.

---

### Independent Claim 3 — Computer Program Product

**3.** A non-transitory computer-readable medium storing instructions that when executed perform the method of claim 1.

---

### Dependent Claims

**4.** The method of claim 1, wherein the applicable aerospace certification standard comprises at least one of: EASA CS-25 (Certification Specifications for Large Aeroplanes); FAA 14 CFR Part 25; RTCA DO-178C (Software Considerations in Airborne Systems and Equipment); SAE ARP4754A (Guidelines for Development of Civil Aircraft and Systems); or SAE ARP4761 (Guidelines and Methods for Conducting Safety Assessment).

**5.** The method of claim 1, wherein the qualified electronic signature is compliant with EU Regulation No 910/2014 (eIDAS Regulation) and is created using a qualified electronic signature creation device (QSCD) registered with an EU trust service provider listed in a national trusted list under eIDAS Article 22.

**6.** The method of claim 1, wherein generating the traceability mapping comprises: parsing the lifecycle phase identifier in each evidence record to identify the applicable certification standard objectives for that phase; querying the SSOT repository for design decisions that reference the evidence record identifier; and generating a machine-readable traceability matrix in a format specified by a data exchange standard for certification data management.

**7.** The method of claim 1, wherein the certification evidence package further comprises a natural language summary of each quantum computation, generated from the fields of the evidence record, describing the computation purpose, inputs, solver configuration, and results in terms understandable to a certification engineer without quantum computing expertise.

---

*Preliminary draft — review by European Patent Attorney before EP filing at EPO.*
