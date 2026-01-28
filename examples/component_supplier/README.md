# Component Supplier Example

## AEROSPACEMODEL — Tier-1 Aerospace Supplier

This example demonstrates AEROSPACEMODEL configuration for a **Tier-1 aerospace component supplier** producing CMM and IPC deliverables for multiple OEM customers.

## What This Example Demonstrates

- ✓ Supplier-centric documentation workflow
- ✓ Multi-customer baseline management
- ✓ Component Maintenance Manual (CMM) generation
- ✓ Illustrated Parts Catalog (IPC) generation
- ✓ OEM interface requirements
- ✓ Part number and effectivity management
- ✓ Repair/Overhaul documentation
- ✓ AS9100 quality traceability

## Supplier Profile

| Attribute | Value |
|-----------|-------|
| **Company** | AeroParts International |
| **CAGE Code** | API01 |
| **Product Line** | Landing Gear Actuators |
| **Part Number** | LGA-5000 Series |
| **Customers** | Multiple aircraft OEMs |
| **Certifications** | AS9100D, FAA-PMA, EASA Part 21G |

## Structure

```
component_supplier/
├── README.md                   # This file
├── run_example.py              # Execution script
├── program_config.yaml         # Supplier configuration
│
├── ASIT/
│   ├── GOVERNANCE/
│   │   ├── BASELINES.md
│   │   ├── BASELINE_REGISTER.csv
│   │   ├── APPROVALS/
│   │   │   └── APPROVAL_MATRIX.csv
│   │   └── CUSTOMER_INTERFACES/
│   │       └── OEM_REQUIREMENTS.md
│   ├── STRUCTURE/
│   │   ├── PRODUCT_BREAKDOWN.yaml
│   │   └── EFFECTIVITY_MATRIX.yaml
│   ├── CONTRACTS/
│   │   └── active/
│   │       ├── API-CTR-CMM-001.yaml
│   │       └── API-CTR-IPC-001.yaml
│   └── INDEX/
│       └── TRACE_MASTER.csv
│
├── ASIGT/
│   ├── brex/
│   │   └── API_brex.yaml
│   └── applicability/
│       └── ACT.yaml
│
├── KDB/
│   ├── components/
│   │   ├── lga5000_assembly.yaml
│   │   └── lga5000_parts.yaml
│   ├── maintenance/
│   │   ├── overhaul_requirements.yaml
│   │   └── repair_procedures.yaml
│   └── quality/
│       └── inspection_requirements.yaml
│
├── IDB/
│   └── csdb/
│
└── output/
```

## Supplier Scenario

### Product: Landing Gear Actuator (LGA-5000)

The LGA-5000 series landing gear actuator is installed on multiple aircraft types from different OEMs.

| P/N | Description | OEM Application |
|-----|-------------|-----------------|
| LGA-5000-100 | Main Gear Actuator | OEM-A: Aircraft Type X |
| LGA-5000-200 | Nose Gear Actuator | OEM-A: Aircraft Type X |
| LGA-5000-150 | Main Gear Actuator | OEM-B: Aircraft Type Y |
| LGA-5000-250 | Nose Gear Actuator | OEM-B: Aircraft Type Y |

### Documentation Deliverables

| Document | Description | Recipient |
|----------|-------------|-----------|
| **CMM** | Component Maintenance Manual | MRO shops, OEMs |
| **IPC** | Illustrated Parts Catalog | MRO shops, spares |
| **OHM** | Overhaul Manual | Authorized repair facilities |

## Key Supplier Challenges Addressed

### 1. Multi-Customer Effectivity

Different OEMs have different aircraft types, requiring careful effectivity management:

```yaml
# Single part, multiple applications
LGA-5000-100:
  - OEM-A / Aircraft-X / MSN 001-500
  - OEM-C / Aircraft-Z / MSN 001-200
```

### 2. Baseline Synchronization

Supplier must track changes against both:
- Internal product baselines
- OEM aircraft baselines (provided by customer)

### 3. OEM Compliance

Each OEM may have specific requirements:
- Document format preferences
- BREX customizations
- Delivery schedules
- Change notification processes

## Quick Start

### 1. Navigate to Example

```bash
cd examples/component_supplier
```

### 2. Generate CMM

```bash
aerospacemodel run --contract API-CTR-CMM-001 --baseline CBL-LGA5000-2026-Q1

# Or use helper script
python run_example.py --contract API-CTR-CMM-001
```

### 3. Generate IPC

```bash
aerospacemodel run --contract API-CTR-IPC-001 --baseline CBL-LGA5000-2026-Q1
```

## Publications

| Publication | Contract | Scope |
|-------------|----------|-------|
| **CMM** | API-CTR-CMM-001 | LGA-5000 maintenance/overhaul |
| **IPC** | API-CTR-IPC-001 | LGA-5000 parts breakdown |

## Supplier-Specific Features

### Part Number Management

```yaml
parts:
  - supplier_pn: "LGA-5000-100"
    oem_pn: "OEM-A-32-4001"
    cage: "API01"
    nsn: "1680-01-123-4567"
```

### Effectivity by Customer

```yaml
effectivity:
  - customer: "OEM-A"
    aircraft: "Type-X"
    msn_range: "001-500"
  - customer: "OEM-B"
    aircraft: "Type-Y"
    msn_range: "001-300"
```

### Quality Traceability (AS9100)

- Part serialization tracking
- Test record references
- First Article Inspection (FAI) links
- Non-conformance trace

## Learning Exercises

### Exercise 1: Add New Customer

1. Add OEM-C to effectivity matrix
2. Create customer-specific BREX rules
3. Generate CMM for OEM-C application

### Exercise 2: Service Bulletin

1. Create a Service Bulletin for field modification
2. Update affected CMM sections
3. Regenerate with new effectivity

### Exercise 3: PMA Part Addition

1. Add PMA (Parts Manufacturer Approval) part
2. Document as alternative to OEM part
3. Update IPC with PMA effectivity

## Comparison to OEM Examples

| Feature | OEM (Aircraft) | Supplier (Component) |
|---------|----------------|----------------------|
| Scope | Full aircraft | Single component |
| Customers | End operators | OEMs, MROs |
| ATA Chapters | All applicable | Focused (e.g., 32) |
| Effectivity | By MSN | By P/N and customer |
| Baselines | Aircraft-level | Component-level |

## Industry Context

This example represents the documentation approach for:
- Tier-1 suppliers (landing gear, engines, avionics)
- Component MRO organizations
- PMA manufacturers
- Repair stations

## Regulatory References

| Standard | Application |
|----------|-------------|
| AS9100D | Quality management |
| FAA-PMA | Parts manufacturing |
| EASA Part 21G | Production approval |
| AC 43.13 | Acceptable methods |

## Next Steps

After mastering this example:
1. Implement multi-OEM delivery automation
2. Add repair development documentation
3. Create PMA substantiation workflow
4. Develop supplier change notification process
