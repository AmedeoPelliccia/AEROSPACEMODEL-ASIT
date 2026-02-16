# CSDB_REF / NU — Atomic Reference Units

This directory stores **atomic consumable reference units (NU)** derived from SSOT executions.

## Role in GenKISS

- **GENESIS**: knowledge determination (uncertain)
- **SSOT**: authoritative lifecycle information (validated)
- **CSDB_REF/NU**: distilled reference units for downstream consumption

NU content is derivative and must never replace SSOT authority.

## Rules

1. Every `NU-<ID>/` must contain `_source.yaml`.
2. `_source.yaml` must point to an SSOT execution artifact path.
3. No orphan NU directories (must appear in `index.csv`).
4. NU is ATDP-agnostic: can feed AMM, IPC, SRM, TSM, WDM, FIM, MMEL, MPD.

## Minimal Unit Structure

```text
NU-<ID>/
├── content.*            # atomic reference content
├── _source.yaml         # provenance from SSOT execution
└── metadata.yaml        # optional classification/tags/effectivity
```

## Example index.csv

```csv
NU_ID,Title,Source_KNU_ID,Source_SSOT_Path,Status,Created_UTC,Owner_AoR,Notes
NU-28-10-001,Tank Geometry Reference,KNU-28-10-001,SSOT/LC05/.../artifact.yaml,ACTIVE,2026-01-15T10:00:00Z,ENG_STRUCT,
```

## Example _source.yaml Schema

```yaml
nu_id: NU-28-10-001
source_knu_id: KNU-28-10-001
source_ssot_execution_path: SSOT/LC05_ANALYSIS_MODELS/KNU-28-10-001/_executions/2026-01-15T10-00-00Z/artifact.yaml
derived_utc: 2026-01-15T10:30:00Z
transformation_contract: CNT-SSOT-TO-NU-001
```

---

**GenKISS**: General Knowledge and Information Standard Systems
