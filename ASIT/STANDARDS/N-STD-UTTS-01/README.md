# UTTS — Unified Teknia Token System v0.1.0
## Modification Track Lookup

| Field              | Value                                                          |
|--------------------|----------------------------------------------------------------|
| Standard ID        | `N-STD-UTTS-01`                                               |
| Version            | `0.1.0`                                                        |
| Status             | DRAFT                                                          |
| Authority          | ASIT (Aircraft Systems Information Transponder)                |
| Parent BREX        | `ASIT-BREX-MASTER-001`                                        |
| BREX Rule Set      | `N-STD-UTTS-01-BREX-001`                                      |
| Related Standard   | `MTL-META-CORE v1.0.0`                                        |

---

## 1. Purpose

**UTTS (Unified Teknia Token System)** — reinterpreted as **Modification Track Lookup** — is a deterministic, queryable lineage engine for all tokenized modifications in the AEROSPACEMODEL knowledge graph.

> UTTS is not a storage ledger. It is a **regulatory-grade deterministic reconstruction engine** for aerospace knowledge evolution.

It answers five governance queries for every token mutation:

| # | Question |
|---|----------|
| 1 | What changed? |
| 2 | Why did it change? |
| 3 | Under whose authority? |
| 4 | Under which lifecycle phase? |
| 5 | What downstream artifacts were impacted? |

---

## 2. Definition

> UTTS (Modification Track Lookup) is:
> *A cryptographically anchored, lifecycle-indexed, bidirectional trace system
> that enables deterministic reconstruction of any modification path.*

---

## 3. MTL Tier Integration

UTTS spans all three tiers of the MTL deterministic stack:

| Tier | Name | UTTS Role |
|------|------|-----------|
| **MTL₁** | Methods Token Library | Source of modification events at the procedural level |
| **MTL₂** | Meta Transformation Layer | Records transformation lineage: `T_m = Φ(T_p, context, constraints)` |
| **MTL₃** | Model Teknia Ledger | Stores the ordered track: `Hash_current = H(TT + Hash_prev)` |

---

## 4. Formal Model

Let:

```
T₀  = original token
Δᵢ  = modification event (ordered, governed)
Tₙ  = resulting token state
⊕   = governed transformation operator
ΣΔᵢ = ordered modification sequence
```

Then:

```
Tₙ = T₀ ⊕ ΣΔᵢ
```

UTTS stores the ordered set:

```
Track(Tₙ) = {Δ₁, Δ₂, Δ₃, …, Δₙ}
```

System state:

```
S = (Tokens, Modifications, Authorities, Lifecycle)
```

UTTS is the function:

```
UTTS : S → Ordered_Trace_Graph
```

Where the trace graph is:
- **Queryable** across 5 dimensions
- **Cryptographically anchored** (SHA3-512 hash chain)
- **Deterministically replayable**

---

## 5. Object Model

### A. Token State Object

```yaml
token_id: MTL-28-11-CRYO-0001
current_revision: 3.2.1
current_hash: SHA3-512(...)
lc_phase: LC04
status: BASELINED
```

### B. Modification Event Object

```yaml
mod_id: MOD-000457
parent_token: MTL-28-11-CRYO-0001
previous_hash: SHA3-512(...)
new_hash: SHA3-512(...)
change_type: constraint_update
description: Updated pressure upper bound per CS-25 load envelope analysis
authority: ASIT-STK_ENG
lc_phase: LC04
timestamp_utc: 2026-02-20T01:20:00Z
impact_scope:
  - FEM_report_28_11_A
  - CM-28-11-CS25
justification_ref:
  - CS-25.963
  - SC-LH2-02
```

---

## 6. Approved Change Types

| Change Type | Description |
|---|---|
| `constraint_update` | Updated parameter bounds or limits |
| `parameter_revision` | Revised numerical or categorical parameters |
| `evidence_addition` | New evidence artifact linked to token |
| `procedure_amendment` | Modified procedural step sequence |
| `regulatory_realignment` | Regulatory reference updated |
| `status_transition` | Token lifecycle status change |

---

## 7. Lookup Dimensions

UTTS supports deterministic queries across five orthogonal dimensions:

| Dimension | Name | Example Query |
|-----------|------|---------------|
| **DIM-01** | By Token | `Track(MTL-28-11-CRYO-0001)` → full modification history |
| **DIM-02** | By LC Phase | All modifications in `LC04` |
| **DIM-03** | By Authority | All modifications signed by `STK_ENG` |
| **DIM-04** | By Regulation | All modifications linked to `CS-25.981` |
| **DIM-05** | By Impact | All tokens affected by `MOD-000457` |

---

## 8. Trace Graph Architecture

The UTTS trace graph is a **Directed Acyclic Graph (DAG)** of token state transitions.

```
T₀ ──Δ₁──▶ T₁ ──Δ₂──▶ T₂ ──Δ₃──▶ T₃
                   │
                   └──Δ₂ᵦ──▶ T₂_alt  (design branch)
```

| Property | Description |
|----------|-------------|
| **Forward Traceability** | Evaluate blast radius: which downstream artifacts T_{n+k} require re-validation after Δᵢ? |
| **Backward Traceability** | Reconstruct provenance: who changed it, why, and in which LC phase? |
| **Branch Management** | Multiple modification paths from a common ancestor; CCB selects canonical branch |
| **Deterministic Replay** | Given T₀ and Track(Tₙ), the system reconstructs Tₙ deterministically |

---

## 9. Hash Chain Integrity

```
Hash(Tᵢ) = H(Tᵢ_data + Hash(Tᵢ₋₁))
```

**Algorithm:** SHA3-512

**Properties:**
- Tamper detection: any alteration in Δᵢ invalidates the entire chain to Tₙ
- No modification exists without record
- No token exists without lineage
- No authority exists without cryptographic signature

---

## 10. Decision State Machine

All BREX rule evaluations resolve to one deterministic state:

| State | Meaning |
|-------|---------|
| `ALLOW` | All governance rules pass |
| `HOLD` | Gate boundary uncertain — needs more data or review |
| `REJECT` | Blocking rule condition failed (hash break, missing anchor, etc.) |
| `ESCALATE` | Safety-critical or baseline modification requires human approval |

Transition rules (summary):

| Condition | State |
|-----------|-------|
| Hash continuity check fails | `REJECT` |
| Regulatory anchor missing | `REJECT` |
| Authority unrecognized | `REJECT` |
| LC regression without ECR | `ESCALATE` |
| Safety impact detected | `ESCALATE` |
| Gate boundary uncertain | `HOLD` |
| All governance rules pass | `ALLOW` |

---

## 11. Mathematical Synthesis

```
Knowledge_state_{n+1} = UTTS( Φ(Knowledge_state_n) )
```

**System invariants:**
1. No transformation exists without record
2. No token exists without lineage
3. No authority exists without signature
4. Every modification is deterministically replayable

---

## 12. BREX Rule Summary

| Category | Count | Key Enforcement |
|----------|-------|-----------------|
| Structure rules | 3 | mod_id format, change_type taxonomy |
| Integrity rules | 4 | Hash chain continuity, SHA3-512 |
| Governance rules | 5 | Authority, LC regression, regulatory anchoring |
| Safety rules | 3 | DAL A/B escalation, EU AI Act, gate integrity |
| Traceability rules | 4 | parent_token, justification_ref, impact_scope |
| Lifecycle rules | 3 | timestamp format, LC phase range, status machine |
| Query rules | 3 | All 5 dimensions, deterministic output |

---

## 13. Files in This Directory

| File | Description |
|------|-------------|
| `N-STD-UTTS-01_v0.1.0.yaml` | Machine-readable standard definition (SSOT) |
| `N-STD-UTTS-01_BREX.yaml` | BREX governance rule set |
| `README.md` | This document (human-readable overview) |

---

## 14. Related Documents

| Document | Reference |
|----------|-----------|
| ASIT Core Specification | `ASIT/ASIT_CORE.md` |
| Master BREX Authority | `ASIT/GOVERNANCE/master_brex_authority.yaml` |
| MTL Meta Standard | `ASIT/STANDARDS/MTL_META/` |
| ATA 28-11 MTL (5D) | `KDB/DEV/mtl/` in ATA 28-11-00 |
| Contract Schema | `ASIT/CONTRACTS/CONTRACT_SCHEMA.yaml` |

---

*End of UTTS Modification Track Lookup Standard v0.1.0 README*
