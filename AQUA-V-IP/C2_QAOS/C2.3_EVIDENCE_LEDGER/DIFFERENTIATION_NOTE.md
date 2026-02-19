# Differentiation Note — C2.3 Cryptographic Certification Evidence Ledger

**Docket:** AQUA-V-C2.3-2026-001  
**Date:** 2026-02-19

---

## 1. Technical Problem Solved

C2.3 solves the **archival and discoverability** problem for quantum certification evidence: DERs (C1.2) and DT transition records (C2.2) are individually verifiable, but without an indexed, queryable, tamper-evident aggregation store, a certification authority cannot efficiently retrieve all evidence pertaining to a specific ATA chapter and DAL level. C2.3 is the evidence store.

## 2. Why the Solution Is Non-Obvious

1. **Aerospace-specific indexing** (ATA chapter + lifecycle phase + DAL level) applied to a cryptographic ledger is non-obvious: blockchain/ledger systems typically use financial or identity-oriented keys, not aerospace certification taxonomy keys
2. **eIDAS-qualified signatures on ledger entries** is non-obvious: certificate transparency logs use server-side signing, not legally-qualified EU electronic signatures
3. **7-year EASA retention enforcement** as a system property (not just a policy) is non-obvious: most ledger systems do not enforce retention periods as architectural constraints

## 3. Inventive Step Beyond Closest Prior Art

No single prior art reference is close. The combination of Certificate Transparency (cryptographic log structure) + aerospace metadata indexing (ATA/DAL/LC-phase) + eIDAS signatures + GAIA-X hosting + EASA retention enforcement is non-obvious because it requires simultaneous expertise in: cryptographic protocols, aerospace certification taxonomy, EU electronic signature law, EU data sovereignty, and aerospace regulatory practice.

## 4. Connection to AQUA-V Architecture and EU Framework

C2.3 is the **EU-hosted certification nerve centre** of the AQUA-V architecture. It stores all evidence produced by C1.2 (DERs), referenced by C2.2 (DT transitions), and consumed by C1.3 (certification packages). Its GAIA-X hosting requirement and eIDAS signatures make it the most explicitly EU-aligned claim in the portfolio — a direct technical implementation of the AEROSPACEMODEL repository's GAIA-X data sovereignty and EASA certification principles.
