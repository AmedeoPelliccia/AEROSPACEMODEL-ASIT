# COMMON_CSDB / DM — Shared Data Module Layer

This directory contains reusable, product-agnostic Data Module (DM) assets
for ATDP products (AMM, IPC, SRM, TSM, WDM, FIM, MMEL, MPD).

## Purpose
- Provide common DM templates and fragments
- Enforce uniform metadata and traceability
- Reduce duplication across product-specific publication trees

## Rules
1. Every DM asset must be registered in `dm_index.csv`.
2. Every DM metadata file must include SSOT/CSDB_REF provenance.
3. No product-exclusive payload in COMMON DM.
4. Naming must be deterministic and stable.

## Minimal naming convention
- Content: `DM-<DOMAIN>-<CODE>.md`
- Metadata: `DM-<DOMAIN>-<CODE>.meta.yaml`

Example:
- `DM-TEMPLATE-COMMON-0001.md`
- `DM-TEMPLATE-COMMON-0001.meta.yaml`

---

**GenKISS**: General Knowledge and Information Standard Systems
