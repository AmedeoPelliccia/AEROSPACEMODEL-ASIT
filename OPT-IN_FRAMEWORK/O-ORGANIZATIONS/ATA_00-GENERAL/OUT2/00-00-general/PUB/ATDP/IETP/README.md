# ATDP / IETP — Interactive Electronic Technical Publication

IETP assembly and runtime packaging surface for ATDP products.

## Purpose
This directory defines the deterministic packaging contract for interactive delivery
of ATDP product content (AMM, IPC, SRM, CMM, etc.) while preserving lineage to
SSOT and CSDB_REF.

## Inputs
- `../COMMON_CSDB/*` shared publication primitives
- `../PRODUCTS/*/CSDB/*` product-specific publication assets
- `../PRODUCTS/*/TRACE/*` product traceability evidence

## Outputs
- Package-ready IETP bundles in `packages/`
- Navigation and applicability configuration
- Search index configuration
- Compliance mapping and lineage records
