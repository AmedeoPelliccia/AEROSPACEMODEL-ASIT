# AEROSPACEMODEL Examples

## Working Examples

This directory contains complete, runnable examples demonstrating different use cases of the AEROSPACEMODEL framework.

## Available Examples

| Example | Description | Complexity |
|---------|-------------|------------|
| [minimal/](minimal/) | Bare minimum setup for learning | ⭐ |
| [digital_twin_demo/](digital_twin_demo/) | Digital Twin documentation pipeline | ⭐⭐ |
| [regional_jet/](regional_jet/) | Regional aircraft program | ⭐⭐⭐ |
| [evtol/](evtol/) | Electric vertical takeoff (eVTOL/UAM) | ⭐⭐ |
| [hydrogen_aircraft/](hydrogen_aircraft/) | Hydrogen-powered aircraft | ⭐⭐⭐ |
| [component_supplier/](component_supplier/) | Tier-1 supplier (CMM/IPC only) | ⭐⭐ |

## Quick Start

### Run an Example

```bash
# Navigate to an example
cd examples/minimal

# Run the example transformation
aerospacemodel run --contract DEMO-CTR-AMM-001 --baseline DBL-DEMO-001

# Or use the provided script
python run_example.py
```

### Explore the Structure

Each example contains:

```
<example>/
├── README.md           # Example documentation
├── run_example.py      # Executable script
├── program_config.yaml # Program configuration
│
├── ASIT/               # Governance layer (example data)
│   ├── GOVERNANCE/
│   ├── STRUCTURE/
│   ├── CONTRACTS/
│   └── INDEX/
│
├── ASIGT/              # Generation layer (example config)
│   └── brex/
│
├── KDB/                # Sample source data
│   └── ...
│
├── IDB/                # Generated output (after running)
│   └── ...
│
└── output/             # Rendered publications (after running)
    └── ...
```

## Example Progression

### 1. Start with `minimal/`

Learn the core concepts:
- ASIT governance structure
- ASIGT generation
- Contract-based transformation
- Basic traceability

### 2. Move to `evtol/` or `component_supplier/`

Learn intermediate patterns:
- Multiple ATA chapters
- Publication-specific contracts
- BREX customization

### 3. Explore `regional_jet/` or `hydrogen_aircraft/`

Learn advanced patterns:
- Full publication suites
- Complex applicability
- Multi-baseline management
- Certification evidence

## What Each Example Demonstrates

### minimal/
- Single ATA chapter (ATA 28 - Fuel)
- One Data Module generation
- Basic contract structure
- Minimal governance setup

### regional_jet/
- Full AMM, IPC, and SRM
- Multiple ATA chapters
- Complete baseline management
- Gate review process

### evtol/
- Electric propulsion systems
- Novel ATA chapter mapping
- Startup-friendly governance
- Rapid iteration support

### hydrogen_aircraft/
- Hydrogen fuel systems (ATA 28 extension)
- Safety-critical content handling
- Certification traceability
- Full evidence package

### component_supplier/
- CMM and IPC focus
- OEM interface contracts
- Supplier-specific BREX
- Part number management

### digital_twin_demo/
- Digital Twin integration patterns
- Three pipeline modes (Condition, Event, Certification)
- Health monitoring triggers
- Fault isolation documentation
- Certification evidence packages

## Customizing Examples

### Use as Starting Point

```bash
# Copy an example to start your program
cp -r examples/minimal my-program

# Customize program_config.yaml
# Update ASIT governance
# Add your source data to KDB/
# Run transformation
```

### Modify for Learning

Each example is designed to be modified:
1. Change ATA chapter scope
2. Add/remove publication types
3. Adjust BREX rules
4. Extend transformation contracts

## Requirements

- Python 3.9+
- AEROSPACEMODEL package installed
- (Optional) S1000D schema files for full validation

## Support

- See individual example READMEs for specific instructions
- Report issues at [GitHub Issues](https://github.com/AEROSPACEMODEL/ASIT-ASIGT/issues)
- Framework documentation at [docs.aerospacemodel.io](https://docs.aerospacemodel.io)
