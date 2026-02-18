# ATA 71 — Fuel Cell Power Plant

> **Aircraft:** AMPEL360 Q100 Hydrogen-Electric  
> **Technology Domain:** P-PROPULSION  
> **ATA Chapter:** 71 — Power Plant (Fuel Cell)  
> **Authority:** ASIT / BREX Profile AEROSPACEMODEL-PRJ-01  
> **Compliance:** S1000D Issue 5.0, DO-160, CS-25, ARP4754A, ARP4761, IEC 62282

---

## 1. Mission

Provide a safe, certifiable hydrogen fuel cell power plant for the AMPEL360 Q100
hydrogen-electric aircraft. The system converts liquid hydrogen (from ATA 28) into
electrical power via proton exchange membrane (PEM) fuel cell stacks, with thermal
management, power conditioning, and control functions.

---

## 2. Scope

| Area | Coverage |
|------|----------|
| PEM Fuel Cell Stack | Primary power generation (71-11, 71-12, 71-13) |
| Balance of Plant | Air supply, H₂ interface, water management (71-21 – 71-23) |
| Thermal Management | Stack cooling and heat rejection (71-24) |
| Power Conditioning | DC/DC converters, inverters, voltage regulation (71-31, 71-32) |
| Control and Monitoring | Fuel cell controller, health monitoring (71-41, 71-42) |

---

## 3. ATEX and ESD Requirements Summary

The fuel cell power plant operates in an environment where hydrogen is present as
both a reactant and a potential leak hazard. ATEX zone classification and ESD
control are mandatory.

### 3.1 ATEX Zone Classification (Fuel Cell Bay)

| Zone | Location | Basis |
|------|----------|-------|
| Zone 1 | Fuel cell stack enclosure (71-11) | H₂ supply present during normal operation; potential release at fittings |
| Zone 1 | H₂ inlet manifold area (71-22 interface) | Continuous H₂ connection to ATA 28 supply |
| Zone 1 | Anode exhaust / recirculation loop | H₂-rich exhaust gas present continuously |
| Zone 2 | Fuel cell bay outer boundary (1.5 m) | Potential H₂ accumulation from minor leaks or purge events |
| Zone 2 | Power conditioning enclosure adjacent to stack | H₂ diffusion from stack to adjacent electronics bay |

All equipment within the fuel cell bay must carry **IIC T1** ATEX/IECEx marking at
a minimum. Zone 1 equipment must be **Category 2G** minimum (Ex db, Ex ia, or Ex eb).

**ATEX equipment requirements for ATA 71:**

- Fuel cell controller (71-41): Ex eb IIC T1 Gb (increased safety enclosure)
- Stack sensors (voltage, temperature, pressure): Ex ia IIC T1 Ga (intrinsically safe)
- Cooling system instruments: Ex ia or Ex eb IIC T1 Gb
- Electrical connectors within Zone 1: Ex e (increased safety) terminal boxes

> Detailed zone map and full equipment ATEX register to be developed in
> a TBD ATA 71 work package (ATEX Zone Classification — Fuel Cell Bay), cross-referencing
> ATX-28-41-00-atex-esd-zone-classification.md.

### 3.2 ESD Control (Fuel Cell Bay)

The fuel cell bay presents combined ESD risks:

1. **H₂ supply interface (ATA 28 → ATA 71):** H₂ supply line connection is a Zone 1
   area; all bonding requirements from ESD-28-00-00-bonding-grounding.md apply at
   the interface point.

2. **Fuel cell stack internal ESD:** The PEM stack generates high internal voltages
   (up to ~600 V DC). Electrostatic discharge from the stack casing must be managed
   to prevent both ignition of anode purge gas and damage to stack membrane.
   - Stack enclosure bonded to aircraft structure: ≤ 1 Ω
   - Stack HV isolation monitoring per IEC 60664-1

3. **Power conditioning ESD (71-31):** High-voltage DC bus creates capacitive charge
   accumulation. All DC bus components must include bleed resistors; maintenance lockout
   required before any work in Zone 1/2 adjacent to the HV bus.

4. **Maintenance personnel ESD:** Same requirements as ATA 28 Zone 1 (wrist strap,
   ESD footwear, non-sparking tools) apply for all work in the fuel cell bay when
   H₂ is present. Refer to ESD-28-00-00-bonding-grounding.md Section 5.

### 3.3 Future-Proofing Provisions (ATA 71)

The following emerging standards are tracked for ATA 71 fuel cell impact:

| Standard | Status | Expected Impact on ATA 71 |
|----------|--------|--------------------------|
| IEC 62282-3-100 (Stationary FC systems) | Under revision (aviation provisions) | Fuel cell safety requirements may become formally applicable |
| SAE J2616 (FC for transportation) | Under review | Aviation adaptation expected; PEM stack safety provisions |
| ISO 23273 (FC road vehicles safety) | 2013 ed. | Zone classification principles for FC enclosures applicable by analogy |
| CS-E / FAR 33 H₂ addendum | Planned | Formal engine certification basis for fuel cell propulsion |
| EASA SC-71-FC (planned) | Not yet issued | Special conditions for fuel cell power plants expected post-2027 |

Design provision: The fuel cell bay is dimensioned with 20 % additional clearance
around Zone 1 boundaries to accommodate potential zone expansion from revised
IEC 62282 requirements.

---

## 4. Key Contacts

| Role | Stakeholder Code | Responsibility |
|------|-------------------|----------------|
| Program Manager | STK_PM | Schedule, budget, deliverables |
| Systems Engineer | STK_SE | System design, ATA 28/71 integration |
| Safety Engineer | STK_SAF | ATEX, ESD, H₂ safety, FC safety assessment |
| Configuration Manager | STK_CM | Baseline control, change management |

---

## 5. Special Conditions

| ID | Title | Description |
|----|-------|-------------|
| SC-71-FUELCELL-001 | Fuel Cell Power Plant Certification | Special conditions for fuel cell propulsion systems |
| SC-28-H2-001 | Hydrogen Storage and Distribution | H₂ supply interface conditions (ATA 28) |

---

## 6. Applicable Standards

| Standard | Application |
|----------|-------------|
| S1000D Issue 5.0 | Technical data structure and exchange |
| DO-160G | Environmental qualification |
| ARP4754A | System development assurance |
| ARP4761 | Safety assessment (FHA, FMEA, FTA) |
| IEC 62282-3-100 | Fuel cell systems safety |
| ATEX 2014/34/EU + IEC 60079 series | Explosive atmosphere equipment |
| CS-25 + Special Conditions | Airworthiness certification |

---

## 7. Cross-References

| Document | Path |
|----------|------|
| ATEX Zone Classification (28-41) | ATA_28-FUEL/28-41-h2-leak-detection/…/ATX-28-41-00-atex-esd-zone-classification.md |
| ESD Bonding & Grounding (28-00) | ATA_28-FUEL/28-00-general/…/ESD-28-00-00-bonding-grounding.md |
| Future Standards Watch (28-00) | ATA_28-FUEL/28-00-general/…/FUT-28-00-00-future-standards.md |
| ATA 28 Fuel System README | ATA_28-FUEL/README.md |

---

*Governed by ASIT. All changes require CCB approval per GOVERNANCE_POLICY.md.*
*ATEX and ESD content requires STK_SAF review before baseline lock (SAFETY-FC-001).*
