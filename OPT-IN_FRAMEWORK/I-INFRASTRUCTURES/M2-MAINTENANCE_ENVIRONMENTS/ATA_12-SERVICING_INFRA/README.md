# ATA 12 — Servicing Infrastructure

**Subdomain:** M2 / Maintenance Environments — ATA 12  
**Domain:** I-INFRASTRUCTURES  
**Lifecycle Phases:** LC11, LC12

---

## Scope

The **ATA_12-SERVICING_INFRA** directory documents the maintenance environment infrastructure for routine
servicing operations at AMPEL360 Q100 line stations and maintenance facilities, including fluid
replenishment, oil servicing, and ground support.

---

## Applicable Standards and Regulations

- **EASA Part-M / FAR 43** — Continuing airworthiness maintenance requirements for servicing tasks
- **EASA Part 145 / FAR 145** — Maintenance organisation approval requirements (facility standards)
- **IATA Dangerous Goods Regulations (DGR)** — Handling and storage of aviation fluids
- **NFPA 2 / NFPA 55** — Hydrogen safety during H₂-related servicing operations (interface with ATA 28)
- **Manufacturer's AMM ATA 12** — Servicing procedures specific to AMPEL360 Q100

---

## Infrastructure Requirements

### Fluid Servicing
- Hydraulic fluid servicing carts (Skydrol or equivalent, per AMM specification)
- Engine oil servicing equipment with correct oil grade dispensers
- Potable water and wastewater servicing connections
- Nitrogen / dry air servicing equipment for strut servicing

### H₂ and Fuel Cell Servicing Interface
- H₂ leak detection monitors at all LH₂ servicing points (see ATA 28 H₂ Cryogenic docs)
- Bonding and grounding cables for LH₂ refuelling operations
- Emergency isolation valves accessible from outside the aircraft

### Ground Power
- External power unit (GPU) or fixed ground power supply rated for AMPEL360 Q100 electrical loads
- Pre-conditioned air (PCA) units for cabin conditioning during ground operations

### Safety Equipment
- Spill kits and absorbents rated for aviation fluids and cryogenic liquids
- Emergency eye-wash and safety shower stations within 10 m of fluid servicing areas
- Fire extinguishers rated for aviation fluid and hydrogen fires

---

## Interface Notes

### Lifecycle Phases
- **LC11 (Customer Integration):** Customer facility servicing equipment qualification and handover
- **LC12 (Continued Airworthiness & MRO):** Routine line servicing, tool calibration, and fluid replenishment records

### Related M2 Directories
- [`../ATA_08-LEVELING_AND_WEIGHING_INFRA/README.md`](../ATA_08-LEVELING_AND_WEIGHING_INFRA/README.md) — Leveling and weighing infrastructure
- [`../ATA_10-PARKING_MOORING_STORAGE_RTS_INFRA/README.md`](../ATA_10-PARKING_MOORING_STORAGE_RTS_INFRA/README.md) — Parking and mooring infrastructure

### Related ATA Domains
- [ATA 28 H₂ Cryogenic Instructions](../../../../.github/instructions/ata28_h2_cryogenic.instructions.md) — Hydrogen safety interface

---

*End of ATA_12-SERVICING_INFRA README*
