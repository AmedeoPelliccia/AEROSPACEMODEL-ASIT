# Method Token Library (MTL) — ATA 28-11-00

**LH₂ Primary Tank — Circular Cryogenic Cells**

| Key | Value |
|-----|-------|
| Lifecycle Context | LC04 (Design Definition) → feeds LC05 (Parametric Models) |
| ATA Mapping | 28-11 LH₂ Primary Tank |
| Architecture | 5-dimensional token model |
| System Domain Token | `SDR-28` |
| Section Token Pattern | `SCR-28-{SECTION_CODE}` |
| Procedure Token Pattern | `STP-28-11-{SEQ}` |
| Process Token Pattern | `MTP-28-11-{DOMAIN}-{SEQ}` |
| Subject Token Pattern | `MTK-28-11-{DOMAIN}-{SEQ}` |
| Total Tokens | 58 |
| Status | DEV (non-baselined) |

## Contents

| File | Layer | Description |
|------|:-----:|-------------|
| `SDR-28_system_domain.yaml` | D5 | System domain entry point (ATA 28 Fuel) |
| `SDR-28_system_domain.md` | D5 | Human-readable companion |
| `SCR-28_section_resolver.yaml` | D4 | Section/component resolver (12 sections) |
| `SCR-28_section_resolver.md` | D4 | Human-readable companion |
| `STP-28-11-00_standard_procedures.yaml` | D3 | Standard Token Procedures — 5 composed procedures (40 token refs) |
| `STP-28-11-00_standard_procedures.md` | D3 | Human-readable companion |
| `MTL-28-11-00_process_methods.yaml` | D2 | Process and scaling method tokens (21 tokens across 5 domains) |
| `MTL-28-11-00_process_methods.md` | D2 | Human-readable companion |
| `MTL-28-11-00_method_token_library.yaml` | D1 | Subject-level token library (19 tokens across 4 domains) |
| `MTL-28-11-00_method_token_library.md` | D1 | Human-readable companion |

## Five-Dimensional Token Architecture

```
┌─────────────────────────────────────────────────────────┐
│  D5  SYSTEM DOMAIN          SDR-28                      │
│       └─ ATA 28 Fuel System (C2 Circular Cryogenic)     │
├─────────────────────────────────────────────────────────┤
│  D4  SECTION / COMPONENT    SCR-28-{SS}                 │
│       └─ 12 sections: 00, 10, 11, 13, 21–23, 30–31,    │
│          41–43                                          │
├─────────────────────────────────────────────────────────┤
│  D3  STANDARD PROCEDURE     STP-28-{SS}-{SEQ}           │
│       └─ 5 composed procedures (sizing, structural,     │
│          evaluation, compliance)                         │
├─────────────────────────────────────────────────────────┤
│  D2  PROCESS / SCALING      MTP-28-{SS}-{DOM}-{SEQ}     │
│       └─ 21 analytical methods and empirical             │
│          correlations (GEOM, THRM, MATL, CERT, EVAL)     │
├─────────────────────────────────────────────────────────┤
│  D1  SUBJECT                MTK-28-{SS}-{DOM}-{SEQ}     │
│       └─ 19 subject tokens (TS, CM, SC, EC)              │
└─────────────────────────────────────────────────────────┘
```

The five layers, from top to bottom:

1. **D5 — System Domain** (`SDR-*`): top-level entry point.  Resolves
   which ATA system domain a model request targets and provides the
   full system context (mission, scope, regulatory baseline, special
   conditions).

2. **D4 — Section / Component** (`SCR-*`): resolves which sub-system
   section within the ATA chapter.  Each SCR token enumerates the
   Standard Token Procedures available at that section.

3. **D3 — Standard Procedure** (`STP-*`): compose subject and process
   tokens into end-to-end standard procedures.  A model consuming one
   STP token receives the full procedure — inputs, sequenced steps,
   intermediate hand-offs, terminal outputs, and acceptance gates —
   enabling a complete standard procedure in a single token call.

4. **D2 — Process / Scaling** (`MTP-*`): extract the actual industry
   processes (closed-form analytical methods) and scaling relationships
   (empirical correlations where no inference boundary exists) embedded
   in every YAML file.

5. **D1 — Subject** (`MTK-*`): tokenise every subject title from trade
   studies, compliance matrices, evaluation criteria, and special conditions
   into a flat namespace of deterministic method identifiers.

Each token defines `method_class`, `inputs`, and `outputs` for model
programming and can be referenced by parametric models, scoring
pipelines, and test matrices.

## Governance

This MTL resides in `KDB/DEV/mtl/` and is **not baselined**.
Promotion to `KDB/LM/SSOT/` requires:

- BREX validation
- Trace coverage verification
- STK_ENG approval
- ECR submission via `GOVERNANCE/CHANGE_CONTROL/`
