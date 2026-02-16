# ATDP / EXPORT — Publication Export Surface

Deterministic export surface for ATDP products (AMM, IPC, SRM, CMM).

## Purpose
Provide controlled rendering and packaging outputs from governed ATDP inputs:
- PDF
- HTML
- IETP_PACKAGE

## Governance
- Export artifacts are delivery outputs, not authority sources.
- Lineage must point to `PUB/ATDP` sources and upstream SSOT/CSDB_REF.
- Rebuilds with identical inputs must produce reproducible outputs.

## Operational Areas
- `jobs/` queue and retry control
- `logs/` export execution history
- `trace/` lineage and compliance mapping
