# Prior Art Matrix — C2.3 Cryptographic Certification Evidence Ledger

**Docket:** AQUA-V-C2.3-2026-001  
**Date:** 2026-02-19

---

| Reference | Date | What It Covers | What It Does NOT Cover (AQUA-V Gap) | Risk Level |
|---|---|---|---|---|
| **Bitcoin / blockchain** ([Nakamoto 2008](https://bitcoin.org/bitcoin.pdf)) | 2008 | Cryptographically linked append-only ledger; distributed consensus; tamper evidence | Aerospace certification use; ATA chapter indexing; eIDAS-qualified signatures; GAIA-X data sovereignty; regulatory query interface; lifecycle phase binding | Low |
| **Certificate Transparency (RFC 9162)** ([IETF](https://datatracker.ietf.org/doc/rfc9162/)) | 2021 | Append-only cryptographic log for TLS certificates; Merkle tree structure; audit proofs | Quantum computation evidence; aerospace lifecycle phases; DAL-indexed queries; EASA regulatory interface | Low |
| **DO-178C tool qualification records** | 2011 | Documentation of software tools used in certification; output records | Cryptographic chaining; append-only enforcement; quantum evidence; automated query interface; eIDAS signatures | Low |
| **EASA Part 21 documentation requirements** ([EASA](https://www.easa.europa.eu)) | 2020 | Design Organisation documentation; 7-year retention; evidence submissions | Cryptographic evidence records; quantum computation evidence; automated ledger; machine-readable query interface | Low |
| **GAIA-X data sovereignty** ([GAIA-X 2022](https://gaia-x.eu)) | 2022 | Federated EU data infrastructure; data residency; access control contracts | Not prior art; provides the technical framework for Claim 4 (EU hosting requirement) | Low |
| **eIDAS Regulation** ([EU 910/2014](https://eur-lex.europa.eu)) | 2014 | Qualified electronic signatures; trust service providers | Not prior art; provides the legal basis for Claim 5 (eIDAS signature requirement) | Low |
| **Git / Merkle DAG** ([Torvalds 2005](https://git-scm.com)) | 2005 | Content-addressed storage; Merkle tree for commit history; tamper-evident history | Aerospace certification use; eIDAS signatures; regulatory query interface; lifecycle phase binding | Low |
| **Digital twins in aerospace** ([Nature 2024](https://www.nature.com/articles/s43588-024-00613-8)) | 2024 | DT data provenance; audit trail | Cryptographic chaining; append-only ledger; quantum evidence records; GAIA-X hosting | Low |

## Gap Analysis

No prior art reference combines: (1) append-only cryptographic chaining, (2) aerospace lifecycle phase indexing, (3) eIDAS-qualified signatures, (4) GAIA-X EU-sovereign hosting, and (5) regulatory authority query interface. The combination is specifically motivated by the EU framework mandate and aerospace certification requirements.
