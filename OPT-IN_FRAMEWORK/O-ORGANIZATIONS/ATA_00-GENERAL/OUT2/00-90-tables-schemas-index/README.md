# ATA 00-90 — Tables, Schemas, and Canonical Index

This directory is the governance control plane for the GenKISS scaffold.  
It centralizes machine-readable contracts used to validate structure, lifecycle conformance, and publication integrity across:

- `00-00-general/GENESIS` (Knowledge Determination Space)
- `00-00-general/SSOT` (Authoritative Information Source)
- `00-00-general/CSDB_REF` (Reference Dataset)
- `00-00-general/PUB/ATDP` (Publication umbrella)

---

## 1) Purpose

`00-90-tables-schemas-index` provides:

1. **Canonical lifecycle registry materialization**  
   LC01–LC14 definitions exported as tabular index for deterministic checks.

2. **Schema contracts**  
   Structural validation rules for YAML/CSV/metadata artifacts.

3. **Controlled vocabularies and enumerations**  
   AoR, statuses, phase types, product codes, and trace semantics.

4. **Cross-domain consistency layer**  
   Single validation reference for generator, validator, CI pipeline, and audits.

---

## 2) Canonical Contents

```text
00-90-tables-schemas-index/
├── README.md
├── tables/
│   ├── canonical_lifecycle_registry.csv
│   ├── atdp_products.csv
│   ├── aor_codes.csv
│   ├── status_enumerations.csv
│   └── epistemic_domains.csv
├── schemas/
│   ├── discovery.schema.yaml
│   ├── justification.schema.yaml
│   ├── framing.schema.yaml
│   ├── derivation.schema.yaml
│   ├── downstream.schema.yaml
│   └── tokenomics.schema.yaml
└── index/
    ├── artifact_catalog.csv
    └── validation_profile.yaml
```

If `index/` files are not yet generated, they are optional bootstrap targets and can be created by CI/bootstrap jobs.

---

## 3) Lifecycle Contract (LC01–LC14)

`tables/canonical_lifecycle_registry.csv` is the deterministic phase reference used by validators.

### Required invariants
- Exactly 14 lifecycle IDs (LC01..LC14)
- Canonical naming only (no synthetic aliases)
- Valid phase type per row: PLM or OPS
- Canonical SSOT directory mapping present for each LC

### Validation implications
- Generator must produce exactly these LC directories in SSOT
- Validator rejects extra or missing LC directories
- Trace tools use this registry to validate cross-phase references

---

## 4) Product Contract

`tables/atdp_products.csv` defines product codes and COMMON_CSDB usage.

### Columns
- `Product_Code`: AMM, IPC, SRM, CMM, etc.
- `Uses_Common_CSDB`: TRUE if product consumes shared primitives

### Validation implications
- Product directories under `PUB/ATDP/PRODUCTS` must match this list
- Products with `Uses_Common_CSDB=TRUE` must reference `../../COMMON_CSDB`

---

## 5) Schema Directory (Optional Extension)

Future extensions may include JSON Schema files for:
- GENESIS O-KNOT/Y-KNOT/KNOT structures
- CSDB_REF NU provenance records
- SSOT KNU artifact metadata
- PUB/ATDP traceability formats

Schema files enable automated validation in CI pipelines.

---

## 6) Usage in Validation

Validators should:
1. Load `canonical_lifecycle_registry.csv`
2. Assert SSOT has exactly those LC directories
3. Assert no extra/missing directories
4. Load `atdp_products.csv`
5. Assert `PUB/ATDP/PRODUCTS` matches product list
6. Validate product structure against schema (if present)

---

**GenKISS**: General Knowledge and Information Standard Systems
