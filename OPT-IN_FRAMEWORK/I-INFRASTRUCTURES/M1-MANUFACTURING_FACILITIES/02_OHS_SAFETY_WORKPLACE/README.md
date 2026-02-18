# 02 — OHS Safety Workplace

**Subdomain:** M1 / Occupational Health & Safety / Workplace  
**Lifecycle Phases:** LC07, LC10

---

## Scope

The **OHS Safety Workplace** subdomain establishes occupational health and safety requirements for personnel working in AMPEL360 Q100 production facilities, including hydrogen-handling environments, cryogenic operations, and high-voltage electrical systems.

---

## Applicable Regulations

### ES RD 486/1997 — Workplace Minimum Conditions (Spain)
- **Scope:** Minimum health and safety requirements for workplaces in Spain
- **Why it applies to M1:** Legal requirement for Spanish production facilities
- **Evidence expected:** Workplace Safety Assessment, Emergency Evacuation Plans

### OSHA 29 CFR 1910 — General Industry (United States)
- **Scope:** General industry safety and health standards including hazardous materials, machine guarding, PPE, and lockout/tagout
- **Why it applies to M1:** Legal requirement for US production facilities
- **Evidence expected:** OSHA Compliance Records, Safety Data Sheets (SDS)

---

## Applicable Standards

### ISO 45001:2018 — Occupational Health and Safety Management System
- **Scope:** Requirements for OHS management systems to prevent work-related injury and ill health
- **Why it applies to M1:** International framework for systematic OHS management
- **Evidence expected:** OHS Policy, Risk Assessment Records, Incident Investigation Reports

### ISO 6385:2016 — Ergonomics — Work System Design
- **Scope:** Ergonomic principles for designing work systems to promote health, safety, and well-being
- **Why it applies to M1:** Assembly operations require ergonomic workstation design to prevent musculoskeletal disorders
- **Evidence expected:** Ergonomics Assessment Reports, Workstation Design Documents

### ISO 45003:2021 — Psychosocial Risk Management
- **Scope:** Managing psychosocial risks in the workplace
- **Why it applies to M1:** Addresses stress, workload, and mental health in production environments
- **Evidence expected:** Psychosocial Risk Assessment, Employee Well-being Programs

---

## Controls & Checklists

Located in `controls/`:

- **PPE Matrix** — Required personal protective equipment by work area and task
  - Cryogenic gloves and face shields (LH₂ handling)
  - Arc flash PPE (electrical work)
  - Respiratory protection (composite layup, paint booth)
  - Safety glasses, steel-toed boots (general production)

- **LOTO (Lockout/Tagout) Procedure** — Energy isolation procedures for equipment maintenance
  - Electrical LOTO
  - Pneumatic/Hydraulic LOTO
  - Cryogenic system LOTO

- **Ergonomics Risk Assessment** — Workstation and task ergonomics evaluation checklist

---

## Interface Notes

### Lifecycle Phases
- **LC07 (QA & Process Compliance):** OHS compliance audits, safety procedure validation
- **LC10 (Industrial & Supply Chain):** Production line safety design, PPE procurement

### OPT-IN Domains
- **T/C2-CIRCULAR_CRYOGENIC_CELLS:** Cryogenic handling safety (NFPA 2/55 interface)
- **T/P-PROPULSION:** Fuel cell electrical safety, thermal hazards
- **M1/03_ENVIRONMENT_HAZMAT:** Hazardous material safety coordination

---

## Audit Questions

1. Is the facility certified to ISO 45001 or equivalent OHS management system?
2. Are all personnel trained on hydrogen safety procedures (cryogenic burns, asphyxiation, explosion hazards)?
3. Is PPE provided, maintained, and used in accordance with the PPE Matrix?
4. Are LOTO procedures documented, posted, and enforced for all energy sources?
5. Are ergonomics assessments conducted for all repetitive or high-risk tasks?
6. Are incident investigations conducted with root cause analysis and corrective actions?

---

*End of 02_OHS_SAFETY_WORKPLACE README*
