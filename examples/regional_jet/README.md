# Regional Jet Example

## AEROSPACEMODEL — Full Regional Aircraft Program

This example demonstrates a comprehensive AEROSPACEMODEL setup for a **70-seat regional jet** program with full publication suite and governance.

## What This Example Demonstrates

- ✓ Full ASIT governance with CCB and gate reviews
- ✓ Multiple baselines (DBL, FBL, PBL)
- ✓ Multiple publication types (AMM, IPC, SRM)
- ✓ Multiple ATA chapters (21, 24, 27, 28, 29, 32, 52, 53, 57, 72)
- ✓ Complete change control workflow
- ✓ Applicability management (variants)
- ✓ Production-ready BREX rules
- ✓ Full traceability chain

## Program Details

| Attribute | Value |
|-----------|-------|
| **Program** | RegionalJet-700 |
| **Model Code** | RJ7 |
| **Capacity** | 70 passengers |
| **Variants** | RJ7-STD (Standard), RJ7-ER (Extended Range) |
| **Engines** | Twin turbofan |
| **Organization** | Regional Aircraft Corporation |

## Structure

```
regional_jet/
├── README.md                   # This file
├── run_example.py              # Execution script
├── program_config.yaml         # Program configuration
│
├── ASIT/                       # Full governance layer
│   ├── GOVERNANCE/
│   │   ├── BASELINES.md
│   │   ├── BASELINE_REGISTER.csv
│   │   ├── CHANGE_CONTROL/
│   │   │   ├── ECR_TEMPLATE.md
│   │   │   ├── ECO_TEMPLATE.md
│   │   │   └── CCB_MINUTES/
│   │   ├── APPROVALS/
│   │   │   ├── APPROVAL_MATRIX.csv
│   │   │   └── GATE_REVIEWS/
│   │   └── RELEASES/
│   │       └── RELEASE_REGISTER.csv
│   ├── STRUCTURE/
│   │   ├── ATA_MAPPING.yaml
│   │   └── LIFECYCLE_PHASES.yaml
│   ├── CONTRACTS/
│   │   └── active/
│   │       ├── RJ7-CTR-AMM-001.yaml
│   │       ├── RJ7-CTR-IPC-001.yaml
│   │       └── RJ7-CTR-SRM-001.yaml
│   └── INDEX/
│       ├── SSOT_INDEX.yaml
│       └── TRACE_MASTER.csv
│
├── ASIGT/                      # Generation layer
│   ├── brex/
│   │   └── RJ7_brex.yaml
│   └── applicability/
│       ├── ACT.yaml            # Applicability Cross-ref
│       └── PCT.yaml            # Product Cross-ref
│
├── KDB/                        # Source data (multi-chapter)
│   ├── requirements/
│   │   ├── ata21_aircon.yaml
│   │   ├── ata24_electrical.yaml
│   │   ├── ata27_flight_controls.yaml
│   │   ├── ata28_fuel.yaml
│   │   ├── ata32_landing_gear.yaml
│   │   └── ata72_engine.yaml
│   ├── tasks/
│   │   └── scheduled_maintenance.yaml
│   ├── parts/
│   │   └── parts_catalog.yaml
│   └── repairs/
│       └── structural_repairs.yaml
│
├── IDB/                        # Generated output
│   └── csdb/
│
└── output/                     # Rendered publications
```

## Publications Generated

| Publication | Contract | Scope |
|-------------|----------|-------|
| **AMM** | RJ7-CTR-AMM-001 | ATA 21, 24, 27, 28, 29, 32, 72 |
| **IPC** | RJ7-CTR-IPC-001 | All chapters |
| **SRM** | RJ7-CTR-SRM-001 | ATA 52, 53, 57 |

## Quick Start

### 1. Navigate to Example

```bash
cd examples/regional_jet
```

### 2. Run All Publications

```bash
# Generate AMM
aerospacemodel run --contract RJ7-CTR-AMM-001 --baseline FBL-RJ7-2026-Q1

# Generate IPC
aerospacemodel run --contract RJ7-CTR-IPC-001 --baseline PBL-RJ7-2026-Q1

# Generate SRM
aerospacemodel run --contract RJ7-CTR-SRM-001 --baseline FBL-RJ7-2026-Q1

# Or run all at once
python run_example.py --all
```

### 3. Examine Outputs

```
IDB/csdb/dms/          # Generated Data Modules
output/amm/            # AMM publication
output/ipc/            # IPC publication
output/srm/            # SRM publication
```

## Governance Features

### Baselines

| ID | Type | Status | Scope |
|----|------|--------|-------|
| DBL-RJ7-2025-Q4 | Design | Frozen | Initial design |
| FBL-RJ7-2026-Q1 | Functional | Active | Development |
| PBL-RJ7-2026-Q2 | Product | Draft | Production prep |

### Gate Reviews

- **PDR** — Preliminary Design Review (Passed)
- **CDR** — Critical Design Review (Passed)
- **TRR** — Test Readiness Review (Scheduled)
- **PRR** — Production Readiness Review (Planned)

### Change Control

Sample ECRs and ECOs demonstrate the change management workflow.

## Applicability

### Aircraft Variants

| Code | Variant | Description |
|------|---------|-------------|
| `RJ7-STD` | Standard | Base configuration |
| `RJ7-ER` | Extended Range | Additional fuel tanks |

### Effectivity

Content is filtered by:
- Aircraft variant
- Modification status
- Serial number range

## Learning Exercises

### Exercise 1: Add New ATA Chapter

1. Create `KDB/requirements/ata30_ice_protection.yaml`
2. Update `ATA_MAPPING.yaml`
3. Modify AMM contract scope
4. Run and verify

### Exercise 2: Create New Baseline

1. Create ECR for content changes
2. Get CCB approval
3. Create new FBL entry
4. Run contract against new baseline

### Exercise 3: Add Aircraft Variant

1. Update `ASIGT/applicability/PCT.yaml`
2. Add variant-specific content to KDB
3. Run with applicability filtering
4. Verify variant-specific output

## Comparison to Minimal Example

| Feature | Minimal | Regional Jet |
|---------|---------|--------------|
| ATA Chapters | 1 | 10+ |
| Publications | AMM only | AMM, IPC, SRM |
| Baselines | 1 (demo) | 3 (real workflow) |
| Governance | Disabled | Full CCB |
| Applicability | None | Variants |
| Change Control | None | ECR/ECO |

## Next Steps

After mastering this example:
1. Try adding TSM (Troubleshooting Manual)
2. Implement Service Bulletin workflow
3. Configure IETP packaging
4. Create your own program using `aerospacemodel init`
