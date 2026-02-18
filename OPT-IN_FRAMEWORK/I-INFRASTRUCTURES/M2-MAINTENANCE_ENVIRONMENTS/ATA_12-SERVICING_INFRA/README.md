# ATA 12 — Servicing Infrastructure

**Domain:** I-INFRASTRUCTURES / M2-MAINTENANCE_ENVIRONMENTS  
**ATA Code:** 12I (Infrastructure variant of ATA 12)  
**Lifecycle Profile:** Standard  
**Novel Technology:** ⭐ Special Condition for LH₂ cryogenic fueling, H₂ ground support equipment

---

## Scope

This directory covers all ground-based infrastructure required to perform **routine servicing** of the AMPEL360 Q100 aircraft. Servicing infrastructure includes all equipment, facilities, and fluid-handling systems needed to service the aircraft's consumable systems, including fuels, fluids, gases, and electrical power.

For the AMPEL360 Q100 with LH₂ cryogenic propulsion and hydrogen fuel cell systems, this includes **⭐ Special Condition** hydrogen refueling infrastructure not present in conventional aircraft servicing facilities.

### Coverage

- Ground electrical power infrastructure (400 Hz, DC, HVDC)
- Pneumatic/air start infrastructure
- Hydraulic servicing carts and systems
- Oxygen and nitrogen service points
- Potable water and waste servicing
- Tire inflation and landing gear servicing
- Engine oil and lubrication servicing
- **⭐ Cryogenic LH₂ fueling infrastructure**
- **⭐ Compressed hydrogen (GH₂) servicing (if applicable)**
- **⭐ Hydrogen safety systems for servicing environments**

---

## ATA Cross-References

| ATA Chapter | System | Relationship |
|-------------|--------|--------------|
| ATA 12 (P-PROGRAMS/S) | Servicing Procedures | Aircraft procedures; this file covers facilities |
| ATA 28 | H₂ Cryogenic Fuel System | LH₂ fueling interface and specifications |
| ATA 24 | Electrical Power | Ground power supply specifications |
| ATA 29 | Hydraulic Power | Ground hydraulic service equipment |
| ATA 32 | Landing Gear | Tire and strut servicing |
| ATA 71 | Fuel Cell Power Plant | H₂ fuel cell system interface |
| O-OPERATIONS ATA IN H₂ GSE | H₂ Supply Chain | H₂ logistics and supply interface |

---

## Regulatory References

| Standard | Title |
|----------|-------|
| EASA Part-145 | MRO Maintenance Organisation |
| EASA Part-M | Continuing Airworthiness |
| IATA AHM 900 | Aircraft Ground Handling Manual |
| SAE ARP 1375 | 400 Hz Ground Power |
| ISO 14687-2 | Hydrogen Fuel Quality |
| ATEX 2014/34/EU | Equipment in Explosive Atmospheres |
| NFPA 2 | Hydrogen Technologies Code |

---

## File Structure

| File | Purpose |
|------|---------|
| `README.md` | This file — scope, ATA reference, cross-references |
| `01_REQUIREMENTS.md` | Normative requirements |
| `02_DESIGN_SPEC.md` | Facility and equipment design specifications |
| `03_SERVICES.md` | Service catalog: fluids, gases, power, H₂ |
| `04_PROCEDURES.md` | Servicing operational procedures |
| `05_SAFETY_RISKS.md` | Safety risks and mitigations |
| `06_CASE_STUDIES.md` | Case studies and lessons learned |

---

## Related Documents

- [M2-MAINTENANCE_ENVIRONMENTS README](../README.md)
- [M2-MAINTENANCE_ENVIRONMENTS Index](../00_INDEX.md)
- [I-INFRASTRUCTURES README](../../README.md)
- [O-OPERATIONS H₂ GSE](../../O-OPERATIONS_SERVICE_STRUCTURES/ATA_IN_H2_GSE_AND_SUPPLY_CHAIN/)
- [ATA 28 H₂ Cryogenic Instructions](../../../../.github/instructions/ata28_h2_cryogenic.instructions.md)
- [ATA 71 Fuel Cell Instructions](../../../../.github/instructions/ata71_fuel_cell.instructions.md)
- [P-PROGRAMS ATA 12 Service Instruction](../../../P-PROGRAMS/S-SERVICE_INSTRUCTION/ATA_12-SERVICING/)
