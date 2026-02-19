# Differentiation Note — C2.2 Digital Twin Synchronisation Layer

**Docket:** AQUA-V-C2.2-2026-001  
**Date:** 2026-02-19

---

## 1. Technical Problem Solved

C2.2 solves the problem of maintaining **cryptographic provenance continuity** across DT state transitions when some transitions are sourced from quantum computations. Without this mechanism, the DT is a "black box" that cannot be audited for certification purposes.

## 2. Why the Solution Is Non-Obvious

1. **Provenance-linked state transitions** are known in blockchain and append-only log systems — but applying this concept to operational DT updates requires re-engineering the DT update path to carry provenance metadata, which DT platforms do not natively support
2. **Governance-gated DT updates** are a new concept: existing DT platforms apply all authorised updates immediately; gating an update on human approval is a non-obvious safety engineering constraint
3. **GAIA-X hosting requirement** (Claim 4) is non-obvious for a DT platform claim — it combines data sovereignty law with technical system design

## 3. Inventive Step Beyond Closest Prior Art

Closest: Autodesk Certification-Ready DT. Delta: C2.2 adds quantum provenance reference, governance gating, human approval for safety-critical updates, and EU data sovereignty constraint. Each individually might be considered obvious; the combination as a governed DT synchronisation mechanism is not.

## 4. Connection to AQUA-V Architecture

C2.2 is the **operational state management layer** of QAOS. It consumes DERs (C1.2) as provenance references, enforces SSOT authority (P0 Claim 1(e)), and provides the audit trail that makes the operational DT certifiable. The GAIA-X data sovereignty constraint (Claim 4) directly implements the EU framework mandate for the operational layer.
