# eVTOL Example

## AEROSPACEMODEL — Electric Vertical Take-Off and Landing Aircraft

This example demonstrates AEROSPACEMODEL configuration for an **electric VTOL** urban air mobility (UAM) aircraft program with novel certification considerations.

## What This Example Demonstrates

- ✓ Novel aircraft category (Powered-Lift / Special Class)
- ✓ Electric propulsion systems (ATA 24/45/70)
- ✓ Distributed Electric Propulsion (DEP)
- ✓ High-voltage battery systems
- ✓ Fly-by-wire flight controls
- ✓ Autonomous flight capability hooks
- ✓ Special Conditions certification path
- ✓ Software-intensive system documentation (DO-178C)

## Program Details

| Attribute | Value |
|-----------|-------|
| **Program** | SkyLift-200 |
| **Model Code** | SL2 |
| **Category** | Powered-Lift (14 CFR Part 23 / SC-VTOL) |
| **Passengers** | 4 + 1 pilot |
| **Propulsion** | Distributed Electric (8 rotors) |
| **Range** | 60 nm (with reserves) |
| **Battery** | 800V High-Voltage Li-ion |
| **Organization** | Urban Mobility Systems Inc. |

## Structure

```
evtol/
├── README.md                   # This file
├── run_example.py              # Execution script
├── program_config.yaml         # Program configuration
│
├── ASIT/
│   ├── GOVERNANCE/
│   │   ├── BASELINES.md
│   │   ├── BASELINE_REGISTER.csv
│   │   ├── APPROVALS/
│   │   │   └── APPROVAL_MATRIX.csv
│   │   └── CERTIFICATION/
│   │       └── SPECIAL_CONDITIONS.md
│   ├── STRUCTURE/
│   │   ├── ATA_MAPPING.yaml
│   │   └── EVTOL_SYSTEMS.yaml
│   ├── CONTRACTS/
│   │   └── active/
│   │       ├── SL2-CTR-AMM-001.yaml
│   │       └── SL2-CTR-CMM-001.yaml
│   └── INDEX/
│       └── TRACE_MASTER.csv
│
├── ASIGT/
│   ├── brex/
│   │   └── SL2_brex.yaml
│   └── applicability/
│       └── ACT.yaml
│
├── KDB/
│   ├── requirements/
│   │   ├── ata24_electrical.yaml
│   │   ├── ata27_flight_controls.yaml
│   │   ├── ata45_central_maintenance.yaml
│   │   ├── ata70_propulsion.yaml
│   │   └── battery_system.yaml
│   └── software/
│       └── flight_control_software.yaml
│
├── IDB/
│   └── csdb/
│
└── output/
```

## eVTOL-Specific Systems

### Novel ATA Adaptations

| ATA | Traditional | eVTOL Adaptation |
|-----|-------------|------------------|
| **24** | Electrical Power | High-Voltage Battery System |
| **45** | Central Maintenance | Health Monitoring / Prognostics |
| **70** | Standard Practices - Engines | Distributed Electric Propulsion |
| **71** | Power Plant | Electric Motor Units |
| **72** | Engine | Motor/Controller Units |

### Special Systems

| System | Description |
|--------|-------------|
| **Battery Management System (BMS)** | Cell monitoring, thermal management |
| **Power Distribution Unit (PDU)** | 800V DC distribution |
| **Motor Controller Units (MCU)** | 8x rotor control |
| **Flight Control Computer (FCC)** | Quadruple redundant |
| **Vehicle Management System (VMS)** | Autonomous capable |

## Certification Considerations

### Certification Basis

```
14 CFR Part 23 (Amendment 64)
+ Special Conditions for Powered-Lift
+ EASA SC-VTOL
+ Means of Compliance (MoC)
```

### Special Conditions Addressed

- SC-01: High-Voltage Electrical Systems
- SC-02: Distributed Propulsion
- SC-03: Battery Fire Protection
- SC-04: Continued Safe Flight and Landing (DEP)
- SC-05: Autonomous Flight Functions
- SC-06: Cyber Security

### Software Levels (DO-178C)

| Component | DAL | Rationale |
|-----------|-----|-----------|
| Flight Control Computer | A | Catastrophic failure |
| Battery Management System | B | Hazardous failure |
| Vehicle Management System | B | Hazardous failure |
| Health Monitoring | C | Major failure |

## Quick Start

### 1. Navigate to Example

```bash
cd examples/evtol
```

### 2. Run AMM Generation

```bash
aerospacemodel run --contract SL2-CTR-AMM-001 --baseline FBL-SL2-2026-Q1

# Or use the helper script
python run_example.py --contract SL2-CTR-AMM-001
```

### 3. Generate CMM for Battery

```bash
aerospacemodel run --contract SL2-CTR-CMM-001 --baseline FBL-SL2-2026-Q1
```

## Publications

| Publication | Contract | Scope |
|-------------|----------|-------|
| **AMM** | SL2-CTR-AMM-001 | Aircraft-level maintenance |
| **CMM** | SL2-CTR-CMM-001 | Battery pack maintenance |

## Learning Exercises

### Exercise 1: Add Motor Controller CMM

1. Create `KDB/requirements/motor_controller.yaml`
2. Create new CMM contract for MCU
3. Add to BREX for MCU-specific rules

### Exercise 2: Implement Software Traceability

1. Review `KDB/software/flight_control_software.yaml`
2. Trace software requirements to DMs
3. Generate DO-178C evidence artifacts

### Exercise 3: Battery Safety Documentation

1. Examine battery system requirements
2. Add thermal runaway procedures
3. Create emergency response DMs

## Comparison to Other Examples

| Feature | Minimal | Regional Jet | eVTOL |
|---------|---------|--------------|-------|
| Propulsion | N/A | Turbofan | Electric DEP |
| Certification | N/A | Part 25 | Part 23 + SC |
| Battery System | No | No | Yes (800V) |
| Software DAL | N/A | N/A | DAL A/B |
| Novel Systems | No | No | Yes |

## Industry Context

This example represents the documentation approach for:
- Joby Aviation
- Archer Aviation
- Lilium
- Wisk Aero
- Beta Technologies
- Other UAM/AAM developers

## Next Steps

After mastering this example:
1. Add autonomy system documentation
2. Implement cybersecurity compliance DMs
3. Create vertiport operations manuals
4. Develop pilot training documentation
