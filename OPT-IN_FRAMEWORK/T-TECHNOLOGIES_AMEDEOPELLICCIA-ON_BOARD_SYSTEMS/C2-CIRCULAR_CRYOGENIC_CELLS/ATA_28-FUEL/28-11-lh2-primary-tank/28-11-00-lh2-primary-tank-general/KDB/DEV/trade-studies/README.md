# Trade Studies — ATA 28-11-00

**LH₂ Primary Tank — Circular Cryogenic Cells**

| Key | Value |
|-----|-------|
| Lifecycle Context | LC04 (Design Definition) → feeds LC03 (Safety) + LC05 (Verification) |
| ATA Mapping | 28-11 LH₂ Primary Tank |
| Configuration Domain | Non-integral cryogenic tank within modular circular cell |
| Status | DEV (non-baselined) |

## Contents

| File | Trade Study | Selected Baseline |
|------|-------------|-------------------|
| `TS-28-11-TS01_tank_architecture.yaml` | Spherical vs Cylindrical vs Conformal | Cylindrical Hemispherical Non-Integral Tank |
| `TS-28-11-TS02_materials.yaml` | Al-Li vs Stainless vs Composite | Al-Li 2195 Metallic Inner Vessel |
| `TS-28-11-TS03_insulation_thermal.yaml` | Vacuum+MLI vs Foam vs Active Cooling | Vacuum Jacket + MLI with Engineered Thermal Bridges |
| `evaluation_criteria.yaml` | Weighted evaluation matrix & open risks | Cylindrical Al-Li Vacuum-MLI |
| `CS25_compliance_matrix.yaml` | EASA CS-25 compliance matrix (YAML, machine-readable) | 10 reqs + 5 Special Conditions |

## Promotion to SSOT

The Functional Baseline (in `KDB/LM/SSOT/`) defines the acceptance
criteria for promoting these trade study outputs.  All promotion gates
must be satisfied before content moves from DEV to SSOT.

## Governance

These trade studies reside in `KDB/DEV/trade-studies/` and are **not
baselined**.  Promotion to `KDB/LM/SSOT/` requires:

- BREX validation
- Trace coverage verification
- STK_ENG / STK_SAF approval
- ECR submission via `GOVERNANCE/CHANGE_CONTROL/`
