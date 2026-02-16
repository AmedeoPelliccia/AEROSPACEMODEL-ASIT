# COMMON_CSDB / PM — Shared Publication Module Layer

This directory contains reusable, product-agnostic Publication Module (PM)
assets for ATDP products (AMM, IPC, SRM, TSM, WDM, FIM, MMEL, MPD).

## Purpose
- Provide common PM assembly templates
- Standardize module composition order
- Preserve traceability to SSOT/CSDB_REF sources

## Rules
1. Every PM asset must be registered in `pm_index.csv`.
2. Every PM metadata file must include provenance and derived UTC.
3. COMMON PM must not include product-exclusive payload.
4. PMs can reference COMMON_CSDB/DM modules only through declared refs.

## Minimal naming convention
- Content: `PM-<DOMAIN>-<CODE>.md`
- Metadata: `PM-<DOMAIN>-<CODE>.meta.yaml`

Example:
- `PM-TEMPLATE-COMMON-0001.md`
- `PM-TEMPLATE-COMMON-0001.meta.yaml`

---

**GenKISS**: General Knowledge and Information Standard Systems
