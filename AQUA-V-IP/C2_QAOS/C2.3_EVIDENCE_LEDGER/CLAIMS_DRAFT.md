# Claims Draft — C2.3 Cryptographic Certification Evidence Ledger

**Docket:** AQUA-V-C2.3-2026-001  
**Date:** 2026-02-19  
**Style:** EPO format (EU-first)

---

## CLAIMS

### Independent Claim 1 — System

**1.** A system for maintaining an append-only cryptographic certification evidence ledger for a safety-critical system development lifecycle, the system comprising:

one or more processors;

a non-transitory storage medium hosted on an EU-resident infrastructure node compliant with data sovereignty requirements of a European data space framework; and

instructions that, when executed by the one or more processors, cause the system to perform operations comprising:

(a) receiving evidence entries comprising at least one of: a cryptographic evidence record of a quantum-assisted computation; a digital twin state transition record; a Single Source of Truth promotion record; or a human approval record;

(b) for each received entry, computing a cryptographic hash of the received entry and a cryptographic hash that chains the entry to the immediately preceding entry in the ledger by incorporating the hash of the preceding entry into the hash computation;

(c) storing each entry with its chain hash and a qualified electronic signature compliant with an applicable EU electronic signature regulation;

(d) exposing a query interface that accepts filter parameters comprising at least one of: an ATA chapter identifier; a lifecycle phase identifier; a Design Assurance Level indicator; an entry type; or a time range; and returns all matching entries together with a chain verification proof enabling an independent party to verify the integrity of each returned entry; and

(e) enforcing an append-only constraint on the ledger such that no stored entry may be modified or deleted after creation.

---

### Independent Claim 2 — Method

**2.** A computer-implemented method for maintaining the append-only cryptographic certification evidence ledger of claim 1.

---

### Independent Claim 3 — Computer Program Product

**3.** A non-transitory computer-readable medium storing instructions implementing the system of claim 1.

---

### Dependent Claims

**4.** The system of claim 1, wherein the EU-resident infrastructure node is a member of a GAIA-X federated data space, and wherein the data residency policy restricts storage of ledger entries to servers physically located within EU member states, and wherein any access request from outside the European Economic Area is logged and subject to an explicit data transfer agreement compliant with GDPR Chapter V.

**5.** The system of claim 1, wherein the qualified electronic signature is a qualified electronic signature under EU Regulation No 910/2014 (eIDAS) created by a qualified trust service provider listed in a national trusted list under eIDAS Article 22, ensuring legal equivalence to a handwritten signature for regulatory submissions to EU authorities including EASA.

**6.** The system of claim 1, wherein the chain verification proof comprises a Merkle proof enabling verification of any individual entry's integrity using only the entry's hash, its sibling hashes at each level of a Merkle tree, and the root hash of the Merkle tree, without requiring access to the full ledger.

**7.** The system of claim 1, further comprising a long-term archival subsystem that retains all ledger entries for a minimum retention period of seven years from the date of certification of the safety-critical system, in compliance with EASA Part 21 documentation retention requirements.

---

*Preliminary draft — EP filing at EPO (Munich, EU). Target: 2026-03-19.*
