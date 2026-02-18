# ATA 08I — Leveling and Weighing Infrastructure: Design Specifications

**Domain:** I-INFRASTRUCTURES / M2-MAINTENANCE_ENVIRONMENTS / ATA_08  
**Document Type:** Design Specification  
**Revision:** 0.1.0

---

## 1. Purpose

This document specifies the design requirements for leveling and weighing infrastructure facilities and equipment supporting AMPEL360 Q100 weight and balance operations.

---

## 2. Facility Design

### 2.1 Weighing Bay Layout

```
┌─────────────────────────────────────────────────────────┐
│                    WEIGHING BAY                          │
│                                                         │
│    ┌──────────────────────────────────────────────┐    │
│    │           AIRCRAFT FOOTPRINT                  │    │
│    │                                              │    │
│    │  [NOSE SCALE]          [L MAIN]  [R MAIN]   │    │
│    │       ⊕                   ⊕          ⊕       │    │
│    └──────────────────────────────────────────────┘    │
│                                                         │
│  [CONTROL CONSOLE]      [DISPLAY UNIT]                  │
│                                                         │
│  Floor: Reinforced concrete, level to ±0.05°           │
│  Clear height: Aircraft tail + 1.5 m minimum           │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Structural Design Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Floor load capacity | ≥ 2.5 × MTOW / contact area | Distributed load |
| Floor levelness | ±0.05° over aircraft footprint | ISO 1101 compliant |
| Clear floor area | Wingspan + 5 m × fuselage + 10 m | Minimum working envelope |
| Ceiling clearance | Tail height + 1.5 m | For jacking clearance |
| Vibration isolation | < 0.01 g RMS (0.1–10 Hz) | During measurement |

---

## 3. Weighing System Design

### 3.1 Load Cell Platforms

| Specification | Value |
|---------------|-------|
| Type | Electronic load cell platform (3-point system) |
| Capacity per scale | ≥ Maximum landing gear load + 20% |
| Accuracy | ±0.05% of reading (per REQ-08I-013) |
| Resolution | 1 kg or 0.1% of capacity (whichever is less) |
| Interface | Digital (RS-485 or Ethernet), with analogue backup |
| Display | Remote digital readout with totalizer |
| Environmental rating | IP54 minimum |

### 3.2 Data Acquisition and Computation

| Component | Specification |
|-----------|---------------|
| Weight and balance computer | Dedicated system with aircraft-type database |
| Input channels | 3× load cell inputs + fuel quantity + tank temp (H₂) |
| Output | Weight, CG (% MAC), moment |
| Record format | Digital log with timestamp, operator ID, calibration ref |
| Backup | Manual calculation worksheet as secondary method |

---

## 4. Jacking Infrastructure

### 4.1 Jack Pad Design

| Parameter | Value |
|-----------|-------|
| Jack pad material | Steel, per aircraft AMM specifications |
| Load rating | As specified in AMM ATA 07 |
| Jack type | Tripod hydraulic, variable-height |
| Synchronization | Manual (with level indicators) or automated |

### 4.2 Jack Positioning Guides

Floor markings or embedded guides shall indicate:
- Nose gear jack point
- Left and right main gear jack points
- Safety support positions

---

## 5. Leveling System Design

### 5.1 Aircraft Leveling Methods

| Method | Equipment | Accuracy |
|--------|-----------|----------|
| Spirit level | Precision spirit level (0.02°/div) | ±0.05° |
| Electronic inclinometer | Digital inclinometer (MEMS-based) | ±0.02° |
| Laser reference | Rotating laser level | ±0.01° over 20 m |
| Plumb bob | Traditional, as backup | ±0.1° |

---

## 6. ⭐ Special Condition: H₂ Integration Design

For AMPEL360 Q100 cryogenic hydrogen systems:

### 6.1 LH₂ Fuel Quantity Interface

| Component | Specification |
|-----------|---------------|
| Tank temperature input | Cryogenic PT100 or NTC sensors, -270°C to +20°C range |
| Tank pressure input | 0–10 bar absolute, ±0.1% accuracy |
| Fuel quantity interface | CAN bus / ARINC 429 from aircraft fuel system |
| Density computation | LH₂ density table (NIST Webbook reference) vs. T and P |
| Mass correction | Automatic in weight and balance computer |

### 6.2 H₂ Safety in Weighing Bay

The weighing bay for H₂ aircraft requires ATEX/IECEx zone classification:

| Zone | Location | Equipment Requirement |
|------|----------|----------------------|
| Zone 2 | Within 1 m of any H₂ vent or pressure relief | Ex-rated electrical equipment |
| Zone 1 | Fueling connections during operation | Not permitted for weighing (fuel isolated) |
| Non-hazardous | Control console location | Standard electrical equipment |

> ⭐ **Special Condition SC-28-H2-001:** Refer to ATA 28 H₂ cryogenic special conditions for zone classification and equipment approval.

---

## 7. Traceability

| Specification | Requirements Reference | Standard |
|---------------|----------------------|----------|
| Load cell accuracy | REQ-08I-013 | OIML R 76, EASA Part-145 |
| Floor levelness | REQ-08I-020 | ISO 1101 |
| H₂ density computation | REQ-08I-040 to 043 | NIST Webbook, SC-28-H2-001 |

---

## 8. Related Documents

- [ATA 08I Requirements](01_REQUIREMENTS.md)
- [ATA 08I Equipment Catalog](03_EQUIPMENT.md)
- [ATA 08I Procedures](04_PROCEDURES.md)
- [ATA 28 H₂ Cryogenic Instructions](../../../../.github/instructions/ata28_h2_cryogenic.instructions.md)
