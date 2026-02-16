# ATDP / PRODUCTS / AMM — Aircraft Maintenance Manual Domain

AMM product domain under `PUB/ATDP/PRODUCTS`.

## Scope
This folder hosts AMM-specific publication assets and configuration.
Shared reusable primitives must be consumed from:

- `../../COMMON_CSDB/DM`
- `../../COMMON_CSDB/PM`
- `../../COMMON_CSDB/BREX`
- `../../COMMON_CSDB/APPLICABILITY`
- `../../COMMON_CSDB/COMMON`
- `../../COMMON_CSDB/ICN`

## Governance
- AMM content is publication-layer output and must trace to SSOT/CSDB_REF lineage.
- No authority inversion: SSOT remains authoritative lifecycle source.
- Product deltas must be explicit and versioned.

## Minimal Deliverables
- AMM DM/PM seeds
- DML seed
- Applicability seed
- Traceability lineage map
- Export target configuration

---

**GenKISS**: General Knowledge and Information Standard Systems
