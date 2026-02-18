# 07 — Airworthiness Production

**Subdomain:** M1 / Airworthiness Production Organisation Approvals  
**Lifecycle Phases:** LC07, LC10

---

## Scope

The **Airworthiness Production** subdomain establishes requirements for obtaining and maintaining Production Organisation Approval (POA) from EASA (Europe) and Production Certificate (PC) from FAA (United States) for AMPEL360 Q100 aircraft manufacturing.

These approvals authorize the organization to manufacture aircraft or aircraft parts under a Type Certificate (TC) or Supplemental Type Certificate (STC), with regulatory authority approval substituting for individual part conformity inspections.

---

## Applicable Regulations

### EASA Part 21 Subpart G — Production Organisation Approval (POA)
- **Regulation:** EASA Part 21 Subpart G (21.A.131 – 21.A.165)
- **Scope:** Requirements for production organization approval to manufacture aircraft, engines, propellers, or parts under EASA oversight
- **Why it applies to M1:** AMPEL360 Q100 production in EU requires EASA POA for type-certificated aircraft
- **Evidence expected:**
  - Production Organisation Exposition (POE) — describes organization, processes, and procedures
  - Quality System Manual compliant with AS9100 or equivalent
  - Process Control Procedures — manufacturing, inspection, testing
  - Supplier Management System — approved supplier list, audits
  - Configuration Management System — engineering change control (ECR/ECO)
  - Inspection Procedures — acceptance criteria, inspection records
  - Traceability System — serialization, material certifications
  - Personnel Qualification Records — operator training, certifications
  - EASA POA Certificate (Form 52)
  - Continuous Airworthiness Surveillance Records — EASA audits

**Key Requirements:**
- 21.A.139: Quality system requirements (equivalent to AS9100)
- 21.A.145: Inspection system
- 21.A.147: Changes to production organization
- 21.A.150: Privileges of the holder of a POA

**Interface with EASA:**
- Initial POA application and assessment (document review, facility audit)
- Continuous surveillance (periodic audits, production monitoring)
- Change notifications (facility, process, quality system changes)

### FAA 14 CFR Part 21 — Production Certificate (PC)
- **Regulation:** FAA 14 CFR Part 21 Subpart G (21.131 – 21.150)
- **Scope:** Requirements for production certificate to manufacture aircraft or aircraft parts under FAA oversight
- **Why it applies to M1:** AMPEL360 Q100 production for US market requires FAA PC
- **Evidence expected:**
  - Production Approval System Document (PASD) or Quality Manual
  - Production Inspection System (PIS) — inspection procedures, criteria, records
  - Test Procedures for acceptance testing
  - Material and Process Specifications
  - Supplier Control System
  - Configuration Management Procedures
  - FAA Production Certificate (Form 8120-11)
  - FAA Manufacturing Inspection District Office (MIDO) surveillance records

**Key Requirements:**
- 21.137: Quality system (FAA Order 8100.15, Production Certification)
- 21.138: Quality manual
- 21.140: Inspections and tests
- 21.143: Changes to type design (production changes)

**Interface with FAA:**
- Initial PC application and assessment (document review, facility inspection)
- Continuous surveillance (periodic inspections by MIDO)
- Change notifications (facility, process, quality system changes)

---

## Controls & Checklists

Located in `EASA_FAA/`:

- **POE (Production Organisation Exposition)** — EASA template and checklist
- **PASD (Production Approval System Document)** — FAA template and checklist
- **Supplier Audit Checklist** — Assessment of approved suppliers
- **Change Notification Template** — ECR/ECO notification to EASA/FAA
- **Internal Audit Schedule** — Production system audits per POA/PC requirements

---

## Interface Notes

### Lifecycle Phases
- **LC07 (QA & Process Compliance):** Primary activation — POA/PC preparation, quality system validation, conformity inspections
- **LC10 (Industrial & Supply Chain):** Production system setup, supplier qualification, continuous surveillance

### OPT-IN Domains
- **O-ORGANIZATIONS/A-AUTHORITATIVE:** Airworthiness requirements and limitations
- **M1/01_QUALITY:** QMS integration (AS9100 supports POA/PC quality system requirements)
- **T/C2-CIRCULAR_CRYOGENIC_CELLS:** Novel technology may require Special Conditions (SC-28-H2-001)
- **T/P-PROPULSION:** Novel technology may require Special Conditions (SC-71-FUELCELL-001)

---

## Audit Questions

1. Is the organization approved under EASA Part 21 Subpart G (POA) and/or FAA Part 21 Subpart G (PC)?
2. Is the Production Organisation Exposition (POE) or Production Approval System Document (PASD) current and approved by the authority?
3. Is the quality system compliant with AS9100 or equivalent aerospace quality standard?
4. Are all production processes controlled and documented with process specifications?
5. Is an approved supplier list maintained with periodic audits?
6. Is configuration management implemented with ECR/ECO control?
7. Are inspection procedures defined with clear acceptance criteria?
8. Are production changes notified to EASA/FAA per regulatory requirements?
9. Are continuous surveillance audits conducted by EASA/FAA MIDO?
10. Are personnel qualified and trained for their production roles?

---

## Special Considerations for Novel Technology

AMPEL360 Q100 incorporates novel technologies (hydrogen cryogenic fuel systems, fuel cell propulsion) that may require:

- **Special Conditions (SC):** Certification requirements not covered by existing regulations
  - SC-28-H2-001: Hydrogen Storage and Distribution
  - SC-71-FUELCELL-001: Fuel Cell Power Plant Certification
- **Type Inspection Authorization (TIA):** FAA may require TIA for novel design features
- **Means of Compliance (MOC):** Agreement with authority on how to demonstrate compliance with special conditions
- **Certification Plan:** Detailed plan for demonstrating airworthiness of novel technologies

**Production Impact:**
- Production processes for novel technologies require additional scrutiny and documentation
- Special inspections or witness points may be required by authority
- Traceability requirements may be enhanced (e.g., all LH₂ welds witnessed)

---

*End of 07_AIRWORTHINESS_PRODUCTION README*
