# PUB / ATDP — Aircraft Technical Data Product Umbrella

ATDP is the canonical publication umbrella for aircraft technical data products in the GenKISS scaffold.  
Within ATDP, **CSDB is shared infrastructure** (COMMON_CSDB), and each product domain (AMM, IPC, SRM, CMM, etc.) provides product-specific deltas under `PRODUCTS/`.

---

## 1) Mission

Provide a governed publication surface that:

- Reuses shared CSDB primitives across products
- Preserves product-specific specialization without duplicating common assets
- Maintains strict lineage to SSOT and CSDB_REF
- Supports deterministic export and IETP packaging flows

---

## 2) Canonical Structure

```text
PUB/ATDP/
├── README.md
├── COMMON_CSDB/
│   ├── README.md
│   ├── DM/
│   ├── PM/
│   ├── DML/
│   ├── BREX/
│   ├── ICN/
│   ├── COMMON/
│   └── APPLICABILITY/
├── PRODUCTS/
│   ├── AMM/
│   ├── IPC/
│   ├── SRM/
│   ├── CMM/
│   └── ...
├── EXPORT/
│   ├── .gitkeep
│   ├── PDF/
│   ├── HTML/
│   └── IETP_PACKAGE/
└── IETP/
    └── .gitkeep
```

---

## 3) Governance Boundaries

### 3.1 Authority Model
- SSOT remains the authoritative lifecycle source.
- CSDB_REF provides atomic reference units derived from SSOT.
- PUB/ATDP is delivery-oriented and must never become an upstream authority.

### 3.2 Non-Inversion Rule

No product folder in `PUB/ATDP/PRODUCTS/*` may redefine lifecycle truth or bypass SSOT provenance.

### 3.3 Delta Rule

Product directories contain only:
- product-specific content,
- product-specific applicability/configuration,
- product-specific trace mappings.

Shared templates and primitives belong in COMMON_CSDB.

---

## 4) Product Domains

A product domain (e.g., PRODUCTS/AMM) should include:
- `CONFIG/` (effectivity, publication profile, export targets)
- `CSDB/` (DM, PM, DML, BREX, APPLICABILITY, etc.)
- `TRACE/` (lineage + compliance mapping)
- `EXPORT/` (product-local export outputs if enabled)

Each product must carry explicit lineage to:
- `../../SSOT`
- `../../CSDB_REF/NU`
- `../../COMMON_CSDB`

---

## 5) Reuse Philosophy

COMMON_CSDB hosts:
- Generic warnings, cautions, notes
- Standard procedures and checklists
- Reusable illustrations and graphics
- Business rules (BREX) for validation
- Applicability logic templates

Products consume and specialize, but do not duplicate.

---

**GenKISS**: General Knowledge and Information Standard Systems
