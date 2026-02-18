# M1 — Manufacturing Facilities Index

**Domain:** I-INFRASTRUCTURES / M1  
**Program:** AMPEL360 Q100

---

## Subdomain Navigation

### 01 — Quality

**Quality Management System**  
[`01_QUALITY/README.md`](01_QUALITY/README.md)

**Standards:**
- ISO 9001 — Quality Management Systems
- AS9100 Rev D — Aerospace Quality Management
- AS9120 — Aerospace and Defense Distributors Quality Management
- NADCAP — Special Process Accreditation (Welding, Heat Treatment, Non-Destructive Testing)
- AS9102 — First Article Inspection (FAI)
- ISO 10007 — Configuration Management

**Templates:**
- QMS Audit Checklist
- FAI Record Template

---

### 02 — OHS Safety Workplace

**Occupational Health & Safety / Workplace**  
[`02_OHS_SAFETY_WORKPLACE/README.md`](02_OHS_SAFETY_WORKPLACE/README.md)

**Regulations:**
- ES RD 486/1997 — Workplace Minimum Conditions (Spain)
- OSHA 29 CFR 1910 — General Industry (United States)

**Standards:**
- ISO 45001 — Occupational Health and Safety Management System
- ISO 6385 — Ergonomics — Work System Design
- ISO 45003 — Psychosocial Risk Management

**Controls:**
- PPE Matrix
- LOTO (Lockout/Tagout) Procedure
- Ergonomics Risk Assessment

---

### 03 — Environment HAZMAT

**Environment & Hazardous Materials**  
[`03_ENVIRONMENT_HAZMAT/README.md`](03_ENVIRONMENT_HAZMAT/README.md)

**Standards:**
- ISO 14001 — Environmental Management System
- REACH/CLP — EU Chemical Regulation
- NFPA 2 — Hydrogen Technologies Code
- NFPA 55 — Compressed Gases and Cryogenic Fluids

**Controls:**
- HAZMAT Storage Matrix
- Waste Streams Register
- Spill Response Plan

**Interfaces:**
- T/C2-CIRCULAR_CRYOGENIC_CELLS (Hydrogen Cryogenic Fuel Systems)

---

### 04 — Machinery Process Safety

**Machinery & Process Safety Operations**  
[`04_MACHINERY_PROCESS_SAFETY/README.md`](04_MACHINERY_PROCESS_SAFETY/README.md)

**Standards:**
- ISO 12100 — Safety of Machinery — Risk Assessment
- ISO 13849 — Safety-Related Parts of Control Systems — Functional Safety
- ISO 9241 — Ergonomics of Human-System Interaction — HMI

**Controls:**
- Machine Guarding Checklist
- Permit to Work Template
- Emergency Stop Validation Procedure

---

### 05 — Warehouse Inventory

**Warehouse, Inventory & Logistics**  
[`05_WAREHOUSE_INVENTORY/README.md`](05_WAREHOUSE_INVENTORY/README.md)

**Standards:**
- Traceability (RFID/QR Tagging)
- Calibration & Metrology (ISO 17025 where applicable)

**Controls:**
- Receiving Inspection Procedure
- FIFO/FEFO Rules
- Stock Accuracy KPI Dashboard

---

### 06 — Additive Manufacturing

**Additive Manufacturing / On-Demand 3D Print**  
[`06_ADDITIVE_MANUFACTURING/README.md`](06_ADDITIVE_MANUFACTURING/README.md)

**Standards:**
- AM Quality Gate Criteria
- Material Batch Traceability
- NADCAP Special Process Qualification (where applicable)

**Controls:**
- Build Record Template
- Powder Handling Safety Procedure

---

### 07 — Airworthiness Production

**Airworthiness Production Organisation Approvals**  
[`07_AIRWORTHINESS_PRODUCTION/README.md`](07_AIRWORTHINESS_PRODUCTION/README.md)

**Regulations:**
- EASA Part 21 Subpart G — Production Organisation Approval
- FAA 14 CFR Part 21 — Production Certificate

**Interfaces:**
- LC07 (QA & Process Compliance)
- LC10 (Industrial & Supply Chain)
- O-ORGANIZATIONS/A-AUTHORITATIVE (Airworthiness Requirements)

---

### 90 — Templates Meta

**Template `.meta.yaml` Sidecars and Schemas**  
[`90_TEMPLATES_META/`](90_TEMPLATES_META/)

**Contents:**
- `meta_sidecars/M1_standard_record.meta.yaml` — Standard record template
- `meta_sidecars/M1_audit_pack.meta.yaml` — Audit pack template
- `schemas/M1_standard_record.schema.json` — JSON Schema for validation

---

### 99 — References

**External Standards, Regulations, and Reference Links**  
[`99_REFERENCES/links.md`](99_REFERENCES/links.md)

**Contents:**
- Quality standards (ISO 9001, AS9100, NADCAP)
- Safety standards (ISO 45001, ISO 12100)
- Environmental standards (ISO 14001, REACH)
- Hydrogen safety (NFPA 2, NFPA 55)
- Airworthiness (EASA Part 21, FAA Part 21)
- Additive manufacturing references

---

## Cross-References

| Reference | Path | Description |
|-----------|------|-------------|
| **LC07** | `../../../lifecycle/LC_PHASE_REGISTRY.yaml` | QA & Process Compliance |
| **LC10** | `../../../lifecycle/LC_PHASE_REGISTRY.yaml` | Industrial & Supply Chain |
| **LC12** | `../../../lifecycle/LC_PHASE_REGISTRY.yaml` | Continued Airworthiness & MRO |
| **T/C2** | `../../T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS/C2-CIRCULAR_CRYOGENIC_CELLS/` | Hydrogen Cryogenic Fuel Systems (NFPA 2/55 interface) |
| **Master BREX Authority** | `../../../ASIT/GOVERNANCE/master_brex_authority.yaml` | BREX decision rules |

---

## Summary

**9 subdomains** covering:
- 6 quality, safety, and operational standards (01–06)
- 1 airworthiness production approval (07)
- 1 templates/schemas directory (90)
- 1 external references directory (99)

**Primary Lifecycle Phases:** LC07, LC10, LC12  
**Authority:** ASIT

---

*End of M1 Index*
