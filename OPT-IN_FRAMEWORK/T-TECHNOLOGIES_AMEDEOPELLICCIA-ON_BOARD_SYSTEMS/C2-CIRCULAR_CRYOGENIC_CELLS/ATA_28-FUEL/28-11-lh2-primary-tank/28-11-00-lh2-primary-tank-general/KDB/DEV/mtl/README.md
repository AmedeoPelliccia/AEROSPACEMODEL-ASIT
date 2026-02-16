# Method Token Library (MTL) — ATA 28-11-00

**LH₂ Primary Tank — Circular Cryogenic Cells**

| Key | Value |
|-----|-------|
| Lifecycle Context | LC04 (Design Definition) → feeds LC05 (Parametric Models) |
| ATA Mapping | 28-11 LH₂ Primary Tank |
| Token Pattern | `MTK-28-11-{DOMAIN}-{SEQ}` |
| Status | DEV (non-baselined) |

## Contents

| File | Description |
|------|-------------|
| `MTL-28-11-00_method_token_library.yaml` | Machine-readable token library (19 tokens across 4 domains) |
| `MTL-28-11-00_method_token_library.md` | Human-readable companion |

## What Is an MTL?

A Method Token Library tokenises every subject title from trade studies,
compliance matrices, evaluation criteria, and special conditions into a
flat namespace of deterministic method identifiers.  Each token:

- Maps 1-to-1 to a source subject (trade study, compliance section, etc.)
- Defines `method_class`, `inputs`, and `outputs` for model programming
- Can be referenced by parametric models, scoring pipelines, and test matrices

## Governance

This MTL resides in `KDB/DEV/mtl/` and is **not baselined**.
Promotion to `KDB/LM/SSOT/` requires:

- BREX validation
- Trace coverage verification
- STK_ENG approval
- ECR submission via `GOVERNANCE/CHANGE_CONTROL/`
