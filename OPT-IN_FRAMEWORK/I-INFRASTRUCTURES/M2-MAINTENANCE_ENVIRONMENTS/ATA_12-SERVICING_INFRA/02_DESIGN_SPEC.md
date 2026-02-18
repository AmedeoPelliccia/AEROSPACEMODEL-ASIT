# ATA 12I — Servicing Infrastructure: Design Specifications

**Domain:** I-INFRASTRUCTURES / M2-MAINTENANCE_ENVIRONMENTS / ATA_12  
**Document Type:** Design Specification  
**Revision:** 0.1.0

---

## 1. Purpose

This document specifies the design requirements for servicing infrastructure facilities and equipment for AMPEL360 Q100 aircraft, including novel hydrogen fueling systems.

---

## 2. Ground Power Infrastructure

### 2.1 400 Hz Ground Power Unit (GPU)

| Parameter | Specification |
|-----------|---------------|
| Output | 115/200V AC, 3-phase, 400 Hz |
| Capacity | ≥ 90 kVA (AMPEL360 Q100 peak demand) |
| Regulation | Voltage ±2%, frequency ±1 Hz |
| Cable | ≥ 25 m, aircraft-type connector (NATO/ARINC) |
| Control | Over-current, over-voltage, phase-loss protection |
| Rating | Fixed pit or mobile unit |

### 2.2 Fixed Ground Power (Pit Systems)

Preferred design for line stations: underground conduit to pit-mounted outlets:

| Parameter | Value |
|-----------|-------|
| Pit location | ≤ 15 m from aircraft nose stop bar |
| Conduit rating | ATEX Group IIC (⭐ if in H₂ zone) |
| Access | Hinged lid, flush with apron |

---

## 3. Fluid Servicing Infrastructure

### 3.1 Hydraulic Service Cart

| Parameter | Specification |
|-----------|---------------|
| Fluid types | Per aircraft AMM ATA 29 (dedicated per fluid type) |
| Pressure rating | 0–350 bar operating |
| Flow rate | 5–15 L/min |
| Filter | 3 micron absolute |
| Tank | Stainless steel or compatible aluminum |

### 3.2 Oil Service Equipment

| Parameter | Specification |
|-----------|---------------|
| Dispensing | Sealed, metered pump unit |
| Labels | Oil type, grade, specification clearly labeled |
| Cross-contamination prevention | Color-coded fittings per aircraft type |

---

## 4. ⭐ Special Condition: LH₂ Fueling Infrastructure Design

### 4.1 LH₂ Fueling Station Layout

```
                          ┌─────────────────────────┐
                          │    AIRCRAFT              │
                          │    H₂ FUELING PANEL      │
                          └──────────┬──────────────┘
                                     │ Cryogenic hose
                                     │
                          ┌──────────┴──────────────┐
                          │  LH₂ DISPENSER UNIT     │
                          │  (Mobile or Fixed)       │
                          │                         │
                          │  Flow meter             │
                          │  Pressure control       │
                          │  Emergency shutdown      │
                          └──────────┬──────────────┘
                                     │ Vacuum-insulated
                                     │ transfer line
                          ┌──────────┴──────────────┐
                          │  LH₂ STORAGE TANK       │
                          │  (Ground-side, vacuum    │
                          │   jacketed, ≥ 1000 L)   │
                          └─────────────────────────┘

  Zone: ATEX IIC, T3 (≥ 15 m clearance from buildings/other aircraft)
  Bonding: Aircraft → Dispenser → Tank (mandatory before transfer)
```

### 4.2 LH₂ Fueling System Components

| Component | Specification |
|-----------|---------------|
| Transfer hose | Vacuum-jacketed, flexible, -270°C rated |
| Coupling | Aircraft-specific cryogenic quick-disconnect |
| Flow meter | Coriolis or turbine, cryogenic-rated |
| Pressure regulator | 0–10 bar, cryogenic-compatible |
| Emergency shutdown valve | Fail-closed, manual + automatic |
| Ground-side storage tank | Vacuum-insulated, ≥ 1,000 L |
| Bonding cables | Cryogenic-rated, ≥ 10 m |
| Fill panel | Stainless steel, weather-protected |

### 4.3 H₂ Detection at Fueling Station

| Sensor | Location | Type | Setpoint |
|--------|----------|------|----------|
| Primary | 1.5 m height at fueling area | Electrochemical | 10% LEL (alarm), 25% LEL (shutdown) |
| Secondary | Roof/overhang above fueling area | Thermal conductivity | 10% LEL (alarm) |
| Portable | Operator-worn | Electrochemical | 10% LEL (personal alarm) |

### 4.4 Fueling Area Safety Infrastructure

| Element | Specification |
|---------|---------------|
| Bonding post | Minimum 2 posts (one at aircraft, one at dispenser) |
| Emergency stop buttons | At aircraft panel, at dispenser, at control point |
| Fire extinguisher | CO₂ (not water) × 2, within 10 m |
| Safety shower/eyewash | Within 15 m of fueling area |
| Wind sock / anemometer | For wind direction awareness |
| Barricades | Physical zone demarcation (15 m radius) |
| Signage | H₂ hazard, no ignition, ATEX zone signs |

---

## 5. Conventional Servicing Layout

### 5.1 Servicing Bay Design

| Parameter | Value |
|-----------|-------|
| Clear height | ≥ 4 m (for servicing vehicles access) |
| Floor surface | Concrete, oil-resistant coating |
| Drainage | Oil separator on all floor drains |
| Compressed air | ≥ 10 bar, filtered (10 micron), dry |
| Nitrogen supply | High-pressure ≥ 200 bar cylinders on safe stands |

---

## 6. Traceability

| Design Element | Requirements Reference | Standard |
|----------------|----------------------|----------|
| 400 Hz GPU | REQ-12I-001 to 004 | SAE ARP 1375 |
| LH₂ fueling system | REQ-12I-060 to 068 | NFPA 2, ISO 14687-2, SC-28-H2-001 |
| H₂ detection | REQ-12I-067 | ATEX 2014/34/EU |

---

## 7. Related Documents

- [ATA 12I Requirements](01_REQUIREMENTS.md)
- [ATA 12I Services Catalog](03_SERVICES.md)
- [ATA 12I Safety Risks](05_SAFETY_RISKS.md)
- [ATA 28 H₂ Cryogenic Instructions](../../../../.github/instructions/ata28_h2_cryogenic.instructions.md)
- [O-OPERATIONS H₂ GSE](../../O-OPERATIONS_SERVICE_STRUCTURES/ATA_IN_H2_GSE_AND_SUPPLY_CHAIN/)
