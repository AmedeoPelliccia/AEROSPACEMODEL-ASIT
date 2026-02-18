# 03 — Environment HAZMAT

**Subdomain:** M1 / Environment & Hazardous Materials  
**Lifecycle Phases:** LC09 (ESG), LC10

---

## Scope

The **Environment HAZMAT** subdomain establishes environmental management and hazardous materials handling requirements for AMPEL360 Q100 production facilities, with special emphasis on hydrogen safety, cryogenic fluids, and sustainable manufacturing practices.

---

## Applicable Standards

### ISO 14001:2015 — Environmental Management System
- **Scope:** Requirements for environmental management systems to enhance environmental performance
- **Why it applies to M1:** Framework for managing environmental impacts (energy, water, waste, emissions)
- **Evidence expected:** Environmental Policy, Environmental Aspects Register, Environmental Monitoring Data

### REACH/CLP — EU Chemical Regulation
- **Scope:** Registration, Evaluation, Authorisation and Restriction of Chemicals (REACH) and Classification, Labelling and Packaging (CLP)
- **Why it applies to M1:** Legal requirement for chemical management in EU production facilities
- **Evidence expected:** Chemical Inventory, Safety Data Sheets (SDS), REACH Registration Numbers

### NFPA 2 — Hydrogen Technologies Code
- **Scope:** Requirements for hydrogen generation, storage, piping, and use systems
- **Why it applies to M1:** Mandatory for facilities handling hydrogen fuel (LH₂ or GH₂) including production line refueling, leak testing, and storage
- **Evidence expected:** Hydrogen Safety Plan, Leak Detection System Documentation, Emergency Response Procedures

### NFPA 55 — Compressed Gases and Cryogenic Fluids
- **Scope:** Requirements for storage, use, and handling of compressed and cryogenic fluids
- **Why it applies to M1:** Applies to LH₂ storage tanks, cryogenic transfer systems, and inert gas systems (N₂, Ar)
- **Evidence expected:** Cryogenic Safety Procedures, Pressure Relief System Design, Operator Training Records

---

## Controls & Checklists

Located in `controls/`:

- **HAZMAT Storage Matrix** — Classification and segregation requirements for hazardous materials
  - Flammable liquids (solvents, adhesives)
  - Oxidizers (oxygen, hydrogen peroxide)
  - Cryogenic fluids (LH₂, LN₂)
  - Corrosives (acids, bases)
  - Toxic materials

- **Waste Streams Register** — Waste classification, handling, and disposal tracking
  - Hazardous waste (solvents, contaminated rags)
  - Recyclable materials (metals, plastics)
  - Non-hazardous industrial waste

- **Spill Response Plan** — Emergency response procedures for chemical and cryogenic spills
  - LH₂ leak/spill response (evacuation, ventilation, ignition source elimination)
  - Chemical spill containment and cleanup
  - Emergency contacts and equipment locations

---

## Interface Notes

### Lifecycle Phases
- **LC09 (ESG Sustainability Assessment):** Environmental impact assessment, carbon footprint, circular economy
- **LC10 (Industrial & Supply Chain):** HAZMAT procurement, storage design, waste management

### OPT-IN Domains
- **T/C2-CIRCULAR_CRYOGENIC_CELLS:** LH₂ handling safety (NFPA 2/55 primary interface)
- **T/P-PROPULSION:** Fuel cell production chemicals and coolants
- **M1/02_OHS_SAFETY_WORKPLACE:** Personnel safety coordination

---

## Audit Questions

1. Is the facility certified to ISO 14001 or equivalent environmental management system?
2. Are all chemicals registered and compliant with REACH/CLP regulations?
3. Is the facility designed and operated in compliance with NFPA 2 (Hydrogen Technologies Code)?
4. Are cryogenic handling procedures compliant with NFPA 55?
5. Is a HAZMAT Storage Matrix implemented and followed for all hazardous materials?
6. Are waste streams properly classified, segregated, and disposed of in accordance with regulations?
7. Are hydrogen leak detection systems installed and tested at all potential leak points?
8. Are emergency spill response procedures documented and personnel trained?

---

*End of 03_ENVIRONMENT_HAZMAT README*
