# M2 — Maintenance Environments: 7-Section Summary Crosswalk

**Domain:** I-INFRASTRUCTURES / M2  
**Authority:** ASIT  
**Purpose:** Maps each of the seven sections of the M2 executive summary to the canonical file(s) within each ATA subdirectory.

---

## Overview

The M2-MAINTENANCE_ENVIRONMENTS executive summary is decomposed into **seven canonical sections**. This crosswalk document provides the authoritative mapping from each summary section to the specific file(s) that hold its content across the three ATA subdirectories:

| ATA | Directory |
|---|---|
| **ATA 08** | `ATA_08-LEVELING_AND_WEIGHING_INFRA/` |
| **ATA 10** | `ATA_10-PARKING_MOORING_STORAGE_RTS_INFRA/` |
| **ATA 12** | `ATA_12-SERVICING_INFRA/` |

---

## 7-Section Summary → File Crosswalk

### Section 1 — Overview & Scope

> *What is this infrastructure? Which ATA chapter does it cover? What are the key cross-references to on-board systems and other domains?*

| ATA | Target File | Notes |
|---|---|---|
| ATA 08 | `ATA_08-LEVELING_AND_WEIGHING_INFRA/README.md` | ATA scope, facility description, cross-refs to ATA 28/C2 |
| ATA 10 | `ATA_10-PARKING_MOORING_STORAGE_RTS_INFRA/README.md` | ATA scope, ground handling overview, cross-refs |
| ATA 12 | `ATA_12-SERVICING_INFRA/README.md` | ATA scope, servicing portfolio, cross-refs |
| M2 root | `README.md` | Combined M2 domain overview and navigation |

---

### Section 2 — Normative Requirements

> *Which regulations, standards, and directives are mandatory for this infrastructure? What evidence is required for compliance?*

| ATA | Target File | Key Requirements |
|---|---|---|
| ATA 08 | `ATA_08-LEVELING_AND_WEIGHING_INFRA/01_REQUIREMENTS.md` | EASA Part-M Subpart E, FAA AC 43.13-1B Ch.10, CS-25 weighing requirement |
| ATA 10 | `ATA_10-PARKING_MOORING_STORAGE_RTS_INFRA/01_REQUIREMENTS.md` | EASA Part-M/145, FAA AC 43.13-1B, ICAO Annex 14 (aerodrome) |
| ATA 12 | `ATA_12-SERVICING_INFRA/01_REQUIREMENTS.md` | EASA Part-145, FAA 14 CFR Part 43, NFPA 2 (H₂), ISO 45001 |

---

### Section 3 — Design Specification

> *What are the performance, dimensional, and environmental design requirements for the infrastructure? What design standards govern facility layout?*

| ATA | Target File | Key Content |
|---|---|---|
| ATA 08 | `ATA_08-LEVELING_AND_WEIGHING_INFRA/02_DESIGN_SPEC.md` | Jack-point loads, platform capacity, calibration intervals, environmental limits |
| ATA 10 | `ATA_10-PARKING_MOORING_STORAGE_RTS_INFRA/02_DESIGN_SPEC.md` | Bay dimensions, tie-down anchor loads, GPU capacity, H₂ bay ventilation design |
| ATA 12 | `ATA_12-SERVICING_INFRA/02_DESIGN_SPEC.md` | Fluid system specs, cryogenic connector specs, LH₂-compatible hose standards |

---

### Section 4 — Equipment / Services

> *What physical equipment or service portfolio does this infrastructure provide? Includes tool lists, cart specifications, and special equipment.*

| ATA | Target File | Key Content |
|---|---|---|
| ATA 08 | `ATA_08-LEVELING_AND_WEIGHING_INFRA/03_EQUIPMENT.md` | Jack types, weighing platforms, calibration standards, tooling list |
| ATA 10 | `ATA_10-PARKING_MOORING_STORAGE_RTS_INFRA/03_EQUIPMENT.md` | Tow bars, chocks, tie-down sets, GPU/APU carts, RTS tool kits |
| ATA 12 | `ATA_12-SERVICING_INFRA/03_SERVICES.md` | Fluid servicing carts (hydraulic, oxygen, nitrogen, LH₂), special tools, boil-off lines |

> **Note:** ATA 12 uses `03_SERVICES.md` (service portfolio focus) while ATA 08 and ATA 10 use `03_EQUIPMENT.md` (hardware inventory focus).

---

### Section 5 — Procedures / Operations

> *How is the infrastructure operated? What are the step-by-step maintenance or operational procedures?*

| ATA | Target File | Key Content |
|---|---|---|
| ATA 08 | `ATA_08-LEVELING_AND_WEIGHING_INFRA/04_PROCEDURES.md` | Weighing sequence, leveling sequence, calibration procedure, recording requirements |
| ATA 10 | `ATA_10-PARKING_MOORING_STORAGE_RTS_INFRA/04_OPERATIONS.md` | Parking procedure, mooring procedure, RTS checklist, storage inspection intervals |
| ATA 12 | `ATA_12-SERVICING_INFRA/04_PROCEDURES.md` | Fluid servicing procedures, LH₂ servicing sequence, equipment connect/disconnect SOP |

> **Note:** ATA 10 uses `04_OPERATIONS.md` (operationally-oriented) while ATA 08 and ATA 12 use `04_PROCEDURES.md` (procedure-step oriented).

---

### Section 6 — Safety & Risk Assessment

> *What are the hazards associated with this infrastructure? What mitigations, PPE requirements, and emergency procedures apply?*

| ATA | Target File | Key Content |
|---|---|---|
| ATA 08 | `ATA_08-LEVELING_AND_WEIGHING_INFRA/05_SAFETY_RISKS.md` | Jack collapse risk, floor load limits, LH₂ spill risk during weighing, PPE |
| ATA 10 | `ATA_10-PARKING_MOORING_STORAGE_RTS_INFRA/05_SAFETY_RISKS.md` | Ground collision risk, H₂ leak risk in bay, tie-down failure modes, fire hazards |
| ATA 12 | `ATA_12-SERVICING_INFRA/05_SAFETY_RISKS.md` | Cryogenic burn hazard, H₂ explosion/asphyxiation, fluid spill, high-pressure line failures |

> **⭐ Special Condition:** All three ATA chapters include hydrogen-specific risk entries for AMPEL360 Q100 LH₂ propulsion.

---

### Section 7 — Case Studies & Best Practices

> *What reference implementations, lessons learned, and best practices exist? Includes historical examples, industry benchmarks, and novel-technology pilot programs.*

| ATA | Target File | Key Content |
|---|---|---|
| ATA 08 | `ATA_08-LEVELING_AND_WEIGHING_INFRA/06_CASE_STUDIES.md` | Weighing after modification examples, LH₂ mass correction case |
| ATA 10 | `ATA_10-PARKING_MOORING_STORAGE_RTS_INFRA/06_CASE_STUDIES.md` | H₂-bay parking pilot (cryogenic aircraft), airport RTS workflow optimisation |
| ATA 12 | `ATA_12-SERVICING_INFRA/06_CASE_STUDIES.md` | LH₂ servicing cart qualification trial, hydrogen boil-off recovery implementation |

---

## Summary Matrix

| Summary Section | Section Number | ATA 08 File | ATA 10 File | ATA 12 File |
|---|---|---|---|---|
| Overview & Scope | 1 | `README.md` | `README.md` | `README.md` |
| Normative Requirements | 2 | `01_REQUIREMENTS.md` | `01_REQUIREMENTS.md` | `01_REQUIREMENTS.md` |
| Design Specification | 3 | `02_DESIGN_SPEC.md` | `02_DESIGN_SPEC.md` | `02_DESIGN_SPEC.md` |
| Equipment / Services | 4 | `03_EQUIPMENT.md` | `03_EQUIPMENT.md` | `03_SERVICES.md` |
| Procedures / Operations | 5 | `04_PROCEDURES.md` | `04_OPERATIONS.md` | `04_PROCEDURES.md` |
| Safety & Risk Assessment | 6 | `05_SAFETY_RISKS.md` | `05_SAFETY_RISKS.md` | `05_SAFETY_RISKS.md` |
| Case Studies | 7 | `06_CASE_STUDIES.md` | `06_CASE_STUDIES.md` | `06_CASE_STUDIES.md` |

---

## File Naming Convention

Section files use a zero-padded two-digit numeric prefix (01–06) to enforce consistent ordering and navigation:

```
<ATA_DIR>/
├── README.md               ← Section 1: Overview & Scope
├── 01_REQUIREMENTS.md      ← Section 2: Normative Requirements
├── 02_DESIGN_SPEC.md       ← Section 3: Design Specification
├── 03_EQUIPMENT.md         ← Section 4: Equipment   (ATA 08, 10)
│   or 03_SERVICES.md       ← Section 4: Services    (ATA 12)
├── 04_PROCEDURES.md        ← Section 5: Procedures  (ATA 08, 12)
│   or 04_OPERATIONS.md     ← Section 5: Operations  (ATA 10)
├── 05_SAFETY_RISKS.md      ← Section 6: Safety & Risk Assessment
└── 06_CASE_STUDIES.md      ← Section 7: Case Studies
```

---

## Traceability Notes

- Every section file references its parent `README.md` and the framework `CROSSWALK.md`.
- Safety content (Section 6) requires **STK_SAF** review per BREX rule `SAFETY-002`.
- Novel-technology content is tagged **⭐ Special Condition** inline.
- Cross-references to T-TECHNOLOGIES (ATA 28, ATA 71) and O-OPERATIONS (ATA IN H₂ GSE) are maintained in `README.md` files.

---

*End of M2 Crosswalk*
