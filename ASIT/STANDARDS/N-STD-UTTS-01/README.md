# Unified Teknia Token System (UTTS) — N-STD-UTTS-01 v0.1.0

| Field              | Value                                                           |
|--------------------|-----------------------------------------------------------------|
| Standard ID        | `N-STD-UTTS-01`                                                 |
| Version            | `0.1.0`                                                         |
| Status             | DRAFT                                                           |
| Authority          | ASIT (Aircraft Systems Information Transponder)                  |
| Parent Standard    | `MTL-META-CORE v1.0.0`                                         |
| Parent BREX        | `ASIT-BREX-MASTER-001`                                         |
| BREX Rule Set      | `N-STD-UTTS-01-BREX-001`                                       |
| ATA Domain         | 96 / 98 (N-NEURAL_NETWORKS)                                    |

---

## 1. Purpose

The **Unified Teknia Token System (UTTS)** is a three-tier deterministic
token transformation and immutable ledger recording infrastructure
co-located with the N-NEURAL_NETWORKS ATA 9x domain.

It extends the existing ATA 96 DPP/traceability infrastructure with:

- **MTL₁** — Methods Token Library (procedural tokenization)
- **MTL₂** — Meta Transformation Layer (cross-domain semantic abstraction via Φ)
- **MTL₃** — Model Teknia Ledger (immutable, hash-linked recording and lineage)

---

## 2. Problem Addressed

The N-NEURAL_NETWORKS domain (ATA 9x) hosts DPP and digital thread
traceability infrastructure but lacks a unified, deterministic,
compliance-grade token transformation and immutable ledger recording
system that spans all three MTL tiers.

UTTS enables traceable, immutable recording of knowledge evolution,
lifecycle phase mapping, and regulatory provenance — directly supporting
EU AI Act, EASA certification, and GAIA-X data sovereignty requirements.

---

## 3. Three-Tier Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  MTL₃  Model Teknia Ledger                                     │
│         Immutable, hash-linked recording and lineage            │
│         Append-only · SHA-256 chain · Authority signatures      │
├─────────────────────────────────────────────────────────────────┤
│  MTL₂  Meta Transformation Layer                                │
│         Cross-domain semantic abstraction via operator Φ        │
│         Deterministic · Contract-approved · Traceable           │
├─────────────────────────────────────────────────────────────────┤
│  MTL₁  Methods Token Library                                    │
│         Procedural tokenization (L1–L5 per MTL-META-CORE)       │
│         Domain tokens · Evidence tokens · Procedure tokens      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. MTL₁ — Methods Token Library

Procedural tokenization layer following [MTL-META-CORE](../MTL_META/README.md).

| Layer | Pattern                              | Purpose                          |
|-------|--------------------------------------|----------------------------------|
| L5    | `CTX-{DOMAIN}-{SYS}`                | Domain context                   |
| L4    | `STR-{DOMAIN}-{SYS}-{COMP}`         | Structure resolution             |
| L3    | `PRC-{DOMAIN}-{SYS}-{SEQ}`          | Procedure composition            |
| L2    | `XFM-{DOMAIN}-{SYS}-{CLASS}-{SEQ}`  | Transformation methods           |
| L1    | `SBJ-{DOMAIN}-{SYS}-{CLASS}-{SEQ}`  | Subject / evidence tokens        |

---

## 5. MTL₂ — Meta Transformation Layer (Φ Operator)

The Φ transformation operator converts tokens between domain profiles,
lifecycle phases, and semantic layers.

| Class          | Name                  | Description                                      |
|----------------|-----------------------|--------------------------------------------------|
| `DOMAIN_XFER`  | Domain Transfer       | Transfer between domain profiles (e.g., AERO → CERT) |
| `LC_PROMOTE`   | Lifecycle Promotion   | Promote across lifecycle phases (e.g., LC04 → LC08) |
| `LAYER_COMPOSE` | Layer Composition    | Compose lower-layer tokens into procedures       |
| `SEMANTIC_MAP` | Semantic Mapping      | Map to equivalent external system representations |

**Φ Contract:**
- Deterministic: same inputs always produce same outputs
- Contract-approved: requires ASIT transformation contract
- Traceable: full lineage from source to target preserved

---

## 6. MTL₃ — Model Teknia Ledger

Append-only, cryptographically linked ledger for immutable recording.

### Ledger Entry Schema

```yaml
entry_id: "UTTS-LEDGER-20260220-001"
timestamp: "2026-02-20T00:00:00Z"
event_type: "TOKEN_CREATE"
token_id: "CTX-AERO-96"
token_version: "0.1.0"
actor: "ASIT-CM"
payload_hash: "<SHA-256 of entry content>"
previous_hash: "<SHA-256 of previous entry>"
authority_signature: "<eIDAS-qualified or ASIT-ROOT signature>"
```

### Event Types

| Event              | Description                                 |
|--------------------|---------------------------------------------|
| `TOKEN_CREATE`     | New token created                           |
| `TOKEN_UPDATE`     | Token content modified                      |
| `TOKEN_PROMOTE`    | Token promoted (DEV → VAL → PROMOTED)       |
| `TOKEN_DEPRECATE`  | Token marked deprecated                     |
| `TOKEN_RETIRE`     | Token permanently retired                   |
| `TRANSFORM_PHI`    | Φ transformation applied                    |
| `GATE_PASS`        | Acceptance gate passed                      |
| `GATE_FAIL`        | Acceptance gate failed                      |
| `BASELINE_FREEZE`  | Baseline frozen (FBL/DBL/PBL)               |
| `AUTHORITY_SIGN`   | Authority signature applied                 |

---

## 7. Lifecycle Phase Coverage

| Phase | Name                          | UTTS Operations                                     |
|-------|-------------------------------|-----------------------------------------------------|
| LC04  | Design Definition             | Token creation, Φ domain transfer, ledger recording  |
| LC07  | QA & Process Compliance       | Φ validation, hash-chain audit                      |
| LC08  | Certification                 | Evidence chain assembly, authority signature          |
| LC09  | ESG & Sustainability          | ESG data tokenization, DPP integration               |
| LC10  | Industrial & Supply Chain     | Production baseline freeze                           |
| LC11  | Operations Customization      | Operational token instantiation                      |
| LC12  | Continued Airworthiness & MRO | MRO event recording, airworthiness evidence          |
| LC14  | End of Life                   | Final ledger snapshot, DPP closure                   |

---

## 8. Regulatory Alignment

| Regulation            | UTTS Alignment                                             |
|-----------------------|------------------------------------------------------------|
| EASA Part 21          | MTL₃ immutable certification evidence chain                |
| EU AI Act             | Full model lineage traceability via transformation reports  |
| GAIA-X                | Permissioned ledger with ASIT authority signatures          |
| EU Digital Product Passport | DPP data integrity backed by MTL₃ hash-chain        |

---

## 9. Invariants

| ID             | Property                        | Statement                                            |
|----------------|---------------------------------|------------------------------------------------------|
| `UTTS-INV-001` | Append-Only Ledger             | MTL₃ entries are append-only; no deletion            |
| `UTTS-INV-002` | Hash-Chain Integrity           | Every entry contains SHA-256 hash of previous entry  |
| `UTTS-INV-003` | Deterministic Transformation   | Φ produces identical output for identical input      |
| `UTTS-INV-004` | Authority Signature Required   | Baselines and cert entries require ASIT signature    |
| `UTTS-INV-005` | Full Lineage Traceability      | Every token traces lineage through all transforms    |

---

## 10. Governance Policies

| ID             | Policy                           | Enforcement |
|----------------|----------------------------------|-------------|
| `UTTS-GOV-001` | Permissioned ledger access       | Block       |
| `UTTS-GOV-002` | Transformation contract required | Block       |
| `UTTS-GOV-003` | Hash-chain continuity            | Block       |
| `UTTS-GOV-004` | Certification evidence immutability | Block    |

---

## 11. Evidence Expected

| Evidence Type                        | Description                                         |
|--------------------------------------|-----------------------------------------------------|
| Certification document               | EASA Part 21 evidence chain                         |
| Audit record                         | Hash-chain integrity verification report            |
| Process procedure                    | Φ transformation operator validation                |
| Transformation lineage report        | MTL₁ → MTL₂ → MTL₃ chain                           |
| Ledger export                        | Append-only, cryptographically linked entries        |
| Authority signature artifact         | ASIT-ROOT / eIDAS-qualified                         |
| DPP integration evidence             | ATA 96 compatibility proof                          |

---

## 12. Safety Impact

The UTTS ledger records certification evidence chains (LC03–LC08) that
are safety-relevant under EASA Part 21 and DO-178C.  A tampered or
corrupted ledger could compromise certification traceability.

**Escalation plan:**
1. STK_SAF review of hash-chain integrity verification logic
2. STK_SAF approval of authority signature validation rules
3. 72-hour review window for ledger append/verify module changes
4. Gate Group D token lineage checks require STK_SAF sign-off

---

## 13. Files in This Directory

| File                              | Description                                  |
|-----------------------------------|----------------------------------------------|
| `N-STD-UTTS-01_v0.1.0.yaml`     | Machine-readable standard definition (SSOT)  |
| `N-STD-UTTS-01_BREX.yaml`       | BREX governance rule set                     |
| `README.md`                       | This document (human-readable overview)      |

---

## 14. Related Documents

| Document                    | Reference                                                    |
|-----------------------------|--------------------------------------------------------------|
| ASIT Core Specification     | `ASIT/ASIT_CORE.md`                                         |
| Master BREX Authority       | `ASIT/GOVERNANCE/master_brex_authority.yaml`                 |
| MTL Meta Standard           | `ASIT/STANDARDS/MTL_META/README.md`                          |
| ATA 96 Traceability         | `OPT-IN_FRAMEWORK/N-NEURAL_NETWORKS/D-DIGITAL_THREAD_TRACEABILITY/ATA_96-TRACEABILITY_DPP_LEDGER/` |
| Contract Schema             | `ASIT/CONTRACTS/CONTRACT_SCHEMA.yaml`                        |
| LC Phase Registry           | `lifecycle/LC_PHASE_REGISTRY.yaml`                           |
| TLI Gate Rulebook           | `lifecycle/TLI_GATE_RULEBOOK.yaml`                           |
| Evidence Ledger Disclosure  | `AQUA-V-IP/C2_QAOS/C2.3_EVIDENCE_LEDGER/INVENTION_DISCLOSURE.md` |

---

*End of N-STD-UTTS-01 v0.1.0 README*
