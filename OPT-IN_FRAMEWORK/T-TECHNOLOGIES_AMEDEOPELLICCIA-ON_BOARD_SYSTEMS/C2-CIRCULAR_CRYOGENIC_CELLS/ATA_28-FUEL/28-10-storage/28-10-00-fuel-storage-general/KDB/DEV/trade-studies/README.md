# Trade Studies — ATA 28-10-00

**Circular Cryogenic Cells (LH₂) — General Storage Architecture**

| Key | Value |
|-----|-------|
| Lifecycle Context | LC04 (Design Definition) → feeds LC03 (Safety) + LC05 (Verification) |
| ATA Mapping | 28-10 Fuel Storage |
| Configuration Domain | BWB LH₂ distributed / centerbody integrated |
| Status | DEV (non-baselined) |

## Contents

| File | Trade Study | Selected Baseline |
|------|-------------|-------------------|
| `TS-28-10-TS01_geometry.yaml` | Circular vs Non-Circular Cryogenic Tanks | Circular Cryogenic Cell (CCC) |
| `TS-28-10-TS02_distributed_architecture.yaml` | Distributed Small Cells vs Single Large Tank | Distributed Circular Cryogenic Cells |
| `TS-28-10-TS03_insulation.yaml` | Insulation Concept | Vacuum + MLI |
| `evaluation_criteria.yaml` | Weighted evaluation matrix & open risks | Multi-Cell Circular Vacuum-MLI |
| `CS25_compliance_matrix.yaml` | EASA CS-25 compliance matrix (YAML, machine-readable) | 23 reqs + 6 Special Conditions |
| `CS25_compliance_matrix.md` | EASA CS-25 compliance matrix (Markdown, human-readable) | — |

## Governance

These trade studies reside in `KDB/DEV/trade-studies/` and are **not
baselined**.  Promotion to `KDB/LM/SSOT/` requires:

- BREX validation
- Trace coverage verification
- STK_ENG / STK_SAF approval
- ECR submission via `GOVERNANCE/CHANGE_CONTROL/`
