# Digital Twin Integrated Documentation Pipeline Demo

## Overview

This demonstration package showcases the **Digital Twin Integrated Documentation Pipeline** — a comprehensive framework for generating aerospace technical documentation that integrates with digital twin infrastructure.

The demo illustrates three key pipeline modes:
1. **Condition-Based Documentation** — Documentation triggered by system health conditions
2. **Event-Driven Documentation** — Documentation generated in response to operational events
3. **Certification Documentation** — Evidence packages for regulatory compliance

## What This Demo Demonstrates

- ✓ Multi-mode pipeline execution (condition, event, certification)
- ✓ Digital twin data integration patterns
- ✓ Dynamic documentation generation based on system state
- ✓ Certification evidence traceability
- ✓ S1000D-compliant output structure
- ✓ Complete governance under ASIT authority

## Directory Structure

```
digital_twin_demo/
├── README.md                       # This file
├── run_demo.py                     # Interactive demo runner
├── program_config.yaml             # Program configuration
│
├── ASIT/                           # Governance layer
│   ├── GOVERNANCE/
│   │   └── BASELINE_REGISTER.csv   # Baseline definitions
│   ├── STRUCTURE/
│   │   └── DIGITAL_TWIN_MAPPING.yaml
│   ├── CONTRACTS/
│   │   └── active/
│   │       ├── DT-CTR-CONDITION-001.yaml   # Condition-based contract
│   │       ├── DT-CTR-EVENT-001.yaml       # Event-driven contract
│   │       └── DT-CTR-CERT-001.yaml        # Certification contract
│   └── INDEX/
│       └── TRACE_MASTER.csv
│
├── ASIGT/                          # Generation layer
│   ├── brex/
│   │   └── DT_brex.yaml            # Digital Twin BREX rules
│   └── pipelines/
│       ├── condition_based_pipeline.yaml
│       ├── event_driven_pipeline.yaml
│       └── certification_pipeline.yaml
│
├── KDB/                            # Source data (Knowledge Database)
│   ├── requirements/
│   │   └── digital_twin_requirements.yaml
│   ├── tasks/
│   │   └── maintenance_tasks.yaml
│   ├── system_data/
│   │   └── component_health.yaml   # Simulated digital twin data
│   └── events/
│       └── operational_events.yaml # Simulated event log
│
├── IDB/                            # Output (Information Database)
│   └── csdb/
│       └── dms/                    # Generated data modules
│
└── output/                         # Rendered publications
```

## Pipeline Modes

### 1. Condition-Based Documentation

Generates documentation when digital twin sensors detect conditions requiring maintenance attention.

**Trigger Examples:**
- Component wear exceeding threshold
- Scheduled maintenance interval reached
- Performance degradation detected

**Output:**
- Maintenance task cards
- Inspection procedures
- Part replacement guides

```bash
# Run condition-based pipeline
python run_demo.py --mode condition
```

### 2. Event-Driven Documentation

Generates documentation in response to specific operational events captured by the digital twin.

**Trigger Examples:**
- Fault code activation
- Configuration change
- Operational limit exceedance

**Output:**
- Troubleshooting procedures
- Fault isolation guides
- Service bulletins

```bash
# Run event-driven pipeline
python run_demo.py --mode event
```

### 3. Certification Documentation

Generates evidence packages for regulatory certification and continued airworthiness.

**Trigger Examples:**
- Type certification submission
- Airworthiness directive compliance
- Design change approval

**Output:**
- Compliance matrices
- Test evidence packages
- Traceability reports

```bash
# Run certification pipeline
python run_demo.py --mode certification
```

## Quick Start

### 1. Navigate to Demo Directory

```bash
cd examples/digital_twin_demo
```

### 2. Run the Interactive Demo

```bash
# Run all three modes sequentially
python run_demo.py --mode all

# Or run individual modes
python run_demo.py --mode condition
python run_demo.py --mode event
python run_demo.py --mode certification
```

### 3. Examine Generated Output

After running the demo:

- **Data Modules**: `IDB/csdb/dms/` — Generated S1000D content
- **Trace Matrix**: `output/TRACE_MATRIX.csv` — Source-to-output traceability
- **Reports**: `output/reports/` — Validation and metrics reports

## Example Scenarios

### Scenario 1: Wear-Based Maintenance

The digital twin detects that the hydraulic pump (ATA 29) has exceeded 80% of its wear limit.

```yaml
# Condition trigger (from digital twin)
condition:
  component_id: "HYD-PUMP-001"
  ata_chapter: "29"
  parameter: "wear_percentage"
  value: 82.5
  threshold: 80.0
  status: "exceeded"
```

The condition-based pipeline generates:
- Inspection procedure DM for hydraulic pump
- Replacement task card
- Parts list reference

### Scenario 2: Fault Event Response

The digital twin logs a fault event: "ENG-VIBRATION-HIGH" on engine #1.

```yaml
# Event trigger (from digital twin)
event:
  event_id: "EVT-2026-001234"
  type: "fault"
  code: "ENG-VIBRATION-HIGH"
  ata_chapter: "72"
  component: "Engine #1"
  timestamp: "2026-01-22T14:30:00Z"
```

The event-driven pipeline generates:
- Fault isolation procedure
- Troubleshooting flowchart DM
- Corrective action procedures

### Scenario 3: Certification Evidence

Regulatory authority requests evidence of compliance with AD 2026-01-15.

```yaml
# Certification request
certification:
  directive: "AD-2026-01-15"
  subject: "Fuel system inspection requirements"
  ata_chapters: ["28"]
  evidence_required:
    - design_compliance
    - test_reports
    - maintenance_instructions
```

The certification pipeline generates:
- Compliance matrix document
- Linked test evidence package
- Maintenance manual excerpts with traceability

## Integration Points

### Digital Twin Data Interface

The demo simulates digital twin data in `KDB/system_data/`. In production, this would connect to:

- IoT sensor platforms
- Fleet health monitoring systems
- MRO information systems
- Configuration management databases

### Data Flow

```
Digital Twin Platform
        │
        ▼
┌───────────────────┐
│   ASIT Gateway    │  ← Validates authority & scope
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  Pipeline Engine  │  ← Selects appropriate pipeline
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│      ASIGT        │  ← Generates S1000D content
└─────────┬─────────┘
          │
          ▼
    Output (IDB/CSDB)
```

## Key Concepts

### Governed Generation

All documentation generation is controlled by ASIT contracts. No content is generated without:
- Valid baseline reference
- Authorized contract
- Defined scope and effectivity

### Traceability

Every generated artifact traces back to:
- Source requirements
- Digital twin data points
- Triggering conditions/events
- Authorizing contracts

### Certification Readiness

Output packages include:
- Provenance metadata
- Hash-based integrity verification
- Complete audit trail
- Regulatory reference mapping

## Customization Guide

### Adding New Condition Types

1. Define condition schema in `KDB/system_data/`
2. Create mapping in `ASIT/STRUCTURE/DIGITAL_TWIN_MAPPING.yaml`
3. Add contract for new condition type
4. Update pipeline to handle new triggers

### Extending Event Handling

1. Add event definitions to `KDB/events/`
2. Create event-to-procedure mapping
3. Define BREX rules for new content
4. Test with sample events

### Certification Package Customization

1. Review regulatory requirements
2. Define evidence matrix
3. Configure traceability links
4. Validate output against compliance checklist

## Technical Requirements

- Python 3.9+
- AEROSPACEMODEL package (optional for full execution)
- YAML/JSON processing tools for inspection

## Support

- See main [Examples README](../README.md) for general guidance
- Report issues at [GitHub Issues](https://github.com/AEROSPACEMODEL/ASIT-ASIGT/issues)
- Framework documentation at [docs.aerospacemodel.io](https://docs.aerospacemodel.io)

## Related Resources

- [AMM Pipeline](../../pipelines/amm_pipeline.yaml) — Aircraft Maintenance Manual pipeline
- [CMM Pipeline](../../pipelines/cmm_pipeline.yaml) — Component Maintenance Manual pipeline
- [ASIT Core](../../ASIT/ASIT_CORE.md) — ASIT governance documentation
- [ASIGT Core](../../ASIGT/ASIGT_CORE.md) — ASIGT generation documentation
