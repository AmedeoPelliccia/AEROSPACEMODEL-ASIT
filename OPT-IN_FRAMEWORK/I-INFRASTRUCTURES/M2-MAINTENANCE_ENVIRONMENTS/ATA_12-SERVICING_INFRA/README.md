# ATA 12 — Servicing Infrastructure

**Domain:** I-INFRASTRUCTURES / M2  
**ATA Chapter:** 12 — Servicing  
**Directory:** `ATA_12-SERVICING_INFRA/`  
**Program:** AMPEL360 Q100  
**Authority:** ASIT

---

## Scope

The **ATA_12-SERVICING_INFRA** directory covers all ground infrastructure required to perform scheduled and unscheduled servicing of the AMPEL360 Q100 aircraft fluids, gases, and consumables.

Key service capabilities:
- Hydraulic fluid servicing (filling, sampling, flushing)
- Engine oil and lubrication servicing
- Oxygen system servicing (crew and passenger)
- Nitrogen and pneumatic system servicing
- Potable water and waste servicing
- **⭐ Liquid hydrogen (LH₂) fuel servicing** — novel technology

---

## ATA Chapter Decomposition

| Sub-Section | Description |
|---|---|
| 12-10 | Replenishing — fluids and gases filling |
| 12-20 | Scheduled servicing — periodic lubrication and fluid checks |
| 12-30 | Unscheduled servicing — fault-driven fluid or gas servicing |
| 12-40 | Waste and water — potable water, waste system servicing |
| 12-50 | LH₂ fuel servicing ⭐ — cryogenic hydrogen refuelling |

---

## Novel Technology Aspects ⭐

The AMPEL360 Q100 LH₂ propulsion system introduces a qualitatively different servicing tier:

- **⭐ LH₂ refuelling:** Requires cryogenic fuel servicing carts, vacuum-jacketed hoses, and bayonet cryogenic couplings rated to −253 °C.
- **⭐ Boil-off recovery during fuelling:** Boil-off gas from displacement of LH₂ into the tank must be captured and managed; venting to atmosphere is permitted only as secondary emergency measure.
- **⭐ H₂ purity check:** LH₂ purity must meet ISO 14687-2 (> 99.97% H₂, CO < 0.2 ppm, CO₂ < 2 ppm) before each fuel upload.
- **⭐ Post-fuelling purge verification:** After LH₂ coupling disconnect, the fuelling port must be purged with GN₂ before any personnel approach within 1 m.

---

## Cross-References

| Domain | Interface |
|---|---|
| T/C2-CIRCULAR_CRYOGENIC_CELLS (ATA 28) | LH₂ system interface: pressures, purities, coupling specs |
| T/P-PROPULSION (ATA 71) | Fuel cell fluid servicing (coolant, air filter) |
| [`I-INFRASTRUCTURES/O-OPERATIONS_SERVICE_STRUCTURES/ATA_IN_H2_GSE_AND_SUPPLY_CHAIN`](../../O-OPERATIONS_SERVICE_STRUCTURES/ATA_IN_H2_GSE_AND_SUPPLY_CHAIN/) | LH₂ delivery from airport supply to servicing cart |
| P/S-SERVICE_INSTRUCTION/ATA_12 | Aircraft-side servicing procedures |

---

## Document Index

| File | Section | Description |
|---|---|---|
| `README.md` ← *this file* | 1 — Overview & Scope | Scope, ATA decomposition, cross-refs |
| `01_REQUIREMENTS.md` | 2 — Normative Requirements | Regulations and standards |
| `02_DESIGN_SPEC.md` | 3 — Design Specification | Cart and facility design specifications |
| `03_SERVICES.md` | 4 — Services | Service portfolio and capability matrix |
| `04_PROCEDURES.md` | 5 — Procedures | Step-by-step servicing procedures |
| `05_SAFETY_RISKS.md` | 6 — Safety & Risk Assessment | Hazards, mitigations, failure modes |
| `06_CASE_STUDIES.md` | 7 — Case Studies | Reference implementations and lessons learned |

See [`../CROSSWALK.md`](../CROSSWALK.md) for the full 7-section summary crosswalk.

---

*End of ATA 12 — Servicing Infrastructure README*
