# ATA 12I — Servicing Infrastructure: Requirements

**Domain:** I-INFRASTRUCTURES / M2-MAINTENANCE_ENVIRONMENTS / ATA_12  
**Document Type:** Normative Requirements  
**Revision:** 0.1.0

---

## 1. General Requirements

### 1.1 Purpose

This document defines normative requirements for servicing infrastructure used to service AMPEL360 Q100 aircraft at maintenance facilities, including novel hydrogen fueling systems.

### 1.2 Applicability

These requirements apply to:
- All maintenance facilities servicing AMPEL360 Q100
- Line maintenance stations performing transit services
- MRO facilities performing base maintenance with system servicing

---

## 2. Electrical Power Requirements

### 2.1 Ground Power

| Requirement | Source | Description |
|-------------|--------|-------------|
| REQ-12I-001 | SAE ARP 1375 | 400 Hz ground power unit shall meet aircraft specification (115/200V AC, 3-phase) |
| REQ-12I-002 | AMM ATA 24 | GPU cable type and connector shall match aircraft receptacle |
| REQ-12I-003 | — | GPU shall provide automatic shutdown on overcurrent or voltage fault |
| REQ-12I-004 | — | DC ground power shall be available for battery charging (28V DC) |

---

## 3. Fluid Servicing Requirements

### 3.1 Hydraulic

| Requirement | Description |
|-------------|-------------|
| REQ-12I-010 | Hydraulic service cart shall dispense approved fluid type only (per AMM ATA 29) |
| REQ-12I-011 | Hydraulic service equipment shall be dedicated to fluid type (no cross-contamination) |
| REQ-12I-012 | Fluid dispensing filter: 3 micron absolute minimum |

### 3.2 Engine Oil

| Requirement | Description |
|-------------|-------------|
| REQ-12I-020 | Oil service equipment shall be dedicated to each oil type |
| REQ-12I-021 | All oil dispensing shall be from sealed, labeled containers |

### 3.3 Potable Water

| Requirement | Description |
|-------------|-------------|
| REQ-12I-030 | Water supply shall meet WHO potable water standards |
| REQ-12I-031 | Hose and fittings shall be food-grade, aircraft-specific connector |

---

## 4. Gas Servicing Requirements

### 4.1 Oxygen

| Requirement | Description |
|-------------|-------------|
| REQ-12I-040 | Oxygen service equipment shall be oxygen-clean (degreased, no hydrocarbons) |
| REQ-12I-041 | Oxygen working area shall be designated oil-free and no-smoking zone |

### 4.2 Nitrogen and Inert Gas

| Requirement | Description |
|-------------|-------------|
| REQ-12I-050 | N₂ supply shall be aviation-grade (purity ≥ 99.95%) |
| REQ-12I-051 | Nitrogen cylinders shall be secured against falling |

---

## 5. Novel Technology Requirements

### 5.1 ⭐ Special Condition: LH₂ Fueling Infrastructure

For AMPEL360 Q100 cryogenic hydrogen fueling:

| Requirement | Source | Description |
|-------------|--------|-------------|
| REQ-12I-060 | ⭐ SC-28-H2-001 | LH₂ fueling station shall meet ATA 28 hydrogen fuel quality requirements (ISO 14687-2) |
| REQ-12I-061 | ⭐ NFPA 2 | LH₂ refueling area shall be classified per NFPA 2 hydrogen zone requirements |
| REQ-12I-062 | ⭐ ATEX 2014/34/EU | All electrical equipment in H₂ zone shall be ATEX Group IIC rated |
| REQ-12I-063 | ⭐ ATA 28 | LH₂ transfer hose shall be cryogenic-rated (-270°C) with aircraft-specific coupling |
| REQ-12I-064 | ⭐ ATA 28 | LH₂ fueling rate shall not exceed aircraft fuel system maximum transfer rate |
| REQ-12I-065 | ⭐ SC-28-H2-001 | Bonding and grounding shall be applied before any LH₂ transfer |
| REQ-12I-066 | ⭐ NFPA 2 | Minimum setback: LH₂ fueling from building ≥ 15 m; from aircraft engine ≥ 3 m |
| REQ-12I-067 | ⭐ ATA 28 | H₂ leak detection shall cover the entire fueling area |
| REQ-12I-068 | ⭐ — | Personnel performing LH₂ fueling shall hold H₂ fueling qualification |

### 5.2 ⭐ H₂ GSE Interface

| Requirement | Description |
|-------------|-------------|
| REQ-12I-070 | ⭐ LH₂ fueling vehicle shall interface with airport H₂ supply per O-OPERATIONS ATA IN H₂ GSE specifications |
| REQ-12I-071 | ⭐ H₂ supply chain quality (purity) shall be verified at point of use before each fueling |

---

## 6. Traceability

| Requirement | Cross-Reference | Lifecycle Phase |
|-------------|----------------|-----------------|
| REQ-12I-001 to 004 | SAE ARP 1375, AMM ATA 24 | LC04, LC06 |
| REQ-12I-010 to 012 | AMM ATA 29, EASA Part-145 | LC04, LC06 |
| REQ-12I-060 to 068 | SC-28-H2-001, NFPA 2, ATA 28 | LC04, LC08 |
| REQ-12I-070 to 071 | O-OPERATIONS H₂ GSE | LC04, LC10 |

---

## 7. Related Documents

- [ATA 12I README](README.md)
- [ATA 12I Design Specifications](02_DESIGN_SPEC.md)
- [ATA 12I Safety Risks](05_SAFETY_RISKS.md)
- [ATA 28 H₂ Cryogenic Instructions](../../../../.github/instructions/ata28_h2_cryogenic.instructions.md)
