# Minimal Example

## AEROSPACEMODEL — Bare Minimum Working Example

This is the simplest possible AEROSPACEMODEL setup, designed for learning the core concepts.

## What This Example Demonstrates

- ✓ Basic ASIT governance structure
- ✓ Single transformation contract
- ✓ One Data Module generation (ATA 28 - Fuel System Description)
- ✓ BREX validation
- ✓ Traceability from source to output

## Structure

```
minimal/
├── README.md               # This file
├── run_example.py          # Run the example
├── program_config.yaml     # Program configuration
│
├── ASIT/                   # Governance
│   ├── GOVERNANCE/
│   │   └── BASELINE_REGISTER.csv
│   ├── STRUCTURE/
│   │   └── ATA_MAPPING.yaml
│   ├── CONTRACTS/
│   │   └── active/
│   │       └── DEMO-CTR-AMM-001.yaml
│   └── INDEX/
│       └── TRACE_MASTER.csv
│
├── ASIGT/                  # Generation config
│   └── brex/
│       └── DEMO_brex.yaml
│
├── KDB/                    # Source data
│   └── requirements/
│       └── ata28_fuel_req.yaml
│
├── IDB/                    # Output (generated)
│   └── csdb/
│       └── dms/
│
└── output/                 # Rendered (generated)
```

## Quick Start

### 1. Navigate to Example

```bash
cd examples/minimal
```

### 2. Run the Example

```bash
# Using CLI
aerospacemodel run --contract DEMO-CTR-AMM-001 --baseline DBL-DEMO-001

# Or using the script
python run_example.py
```

### 3. Examine Output

After running:
- `IDB/csdb/dms/` — Generated S1000D Data Module
- `output/` — Rendered HTML/PDF
- `ASIGT/runs/` — Execution artifacts and trace matrix

## Files Explained

### program_config.yaml

Defines the program identity and settings:
```yaml
program:
  name: "Demo Aircraft"
  model_code: "DEMO"
  organization: "AEROSPACEMODEL Examples"
```

### ASIT/CONTRACTS/active/DEMO-CTR-AMM-001.yaml

The transformation contract that authorizes generation:
```yaml
contract:
  id: "DEMO-CTR-AMM-001"
  source:
    baseline: "DBL-DEMO-001"
    scope:
      ata_chapters: ["28"]
  target:
    publication: "AMM"
```

### KDB/requirements/ata28_fuel_req.yaml

Sample source data (engineering knowledge):
```yaml
requirements:
  - id: "REQ-FUEL-001"
    title: "Fuel System Description"
    content: "The fuel system shall..."
```

### ASIGT/brex/DEMO_brex.yaml

Business rules for validation:
```yaml
rules:
  - rule_id: "DEMO-BR-001"
    element: "modelIdentCode"
    pattern: "^DEMO$"
```

## Expected Output

### Generated Data Module

```
IDB/csdb/dms/DMC-DEMO-A-28-00-00-00A-040A-A_001-00.xml
```

Content type: Descriptive (info code 040)
Subject: Fuel System Description

### Trace Matrix

```
ASIGT/runs/<timestamp>__DEMO-CTR-AMM-001/TRACE_MATRIX.csv
```

Shows: `REQ-FUEL-001` → `DMC-DEMO-A-28-00-00-00A-040A-A`

## Learning Exercises

### Exercise 1: Add Another Requirement

1. Edit `KDB/requirements/ata28_fuel_req.yaml`
2. Add a new requirement (e.g., REQ-FUEL-002)
3. Run the transformation
4. Verify new DM is generated

### Exercise 2: Change ATA Chapter

1. Edit contract to include ATA 27 (Flight Controls)
2. Add source data for ATA 27
3. Update ATA_MAPPING.yaml
4. Run and verify

### Exercise 3: Customize BREX

1. Edit `ASIGT/brex/DEMO_brex.yaml`
2. Add a custom validation rule
3. Create content that violates the rule
4. Observe validation failure

## Next Steps

After understanding this example:
1. Try `examples/evtol/` for a more complete setup
2. Read the [Getting Started Guide](../../docs/getting-started.md)
3. Create your own program using `aerospacemodel init`

## Troubleshooting

### "Contract not found"
Ensure you're in the `examples/minimal/` directory.

### "Baseline not found"
Check `ASIT/GOVERNANCE/BASELINE_REGISTER.csv` exists.

### "Validation failed"
Review `ASIGT/runs/<latest>/VALIDATION_REPORT.json`.
