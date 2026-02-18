# 01 — Quality

**Subdomain:** M1 / Quality Management System  
**Lifecycle Phases:** LC07, LC08

---

## Scope

The **Quality** subdomain establishes the Quality Management System (QMS) for AMPEL360 Q100 aircraft production, ensuring compliance with aerospace quality standards and special process requirements.

---

## Applicable Standards

### ISO 9001:2015 — Quality Management Systems
- **Scope:** General QMS framework for all manufacturing operations
- **Why it applies to M1:** Foundation for process control, document management, and continuous improvement
- **Evidence expected:** QMS Manual, Procedure Documents, Internal Audit Records

### AS9100 Rev D — Aerospace Quality Management
- **Scope:** Aerospace-specific quality requirements including configuration management, risk management, and first article inspection
- **Why it applies to M1:** Mandatory for aerospace production organizations
- **Evidence expected:** AS9100 Certification, Process FMEA, Configuration Management Plan

### AS9120 — Aerospace and Defense Distributors Quality Management
- **Scope:** Quality management for distributors and suppliers of aerospace parts
- **Why it applies to M1:** Supply chain and vendor qualification requirements
- **Evidence expected:** Approved Supplier List, Supplier Audit Reports

### NADCAP — Special Process Accreditation
- **Scope:** Special process qualification (welding, heat treatment, non-destructive testing, surface treatment, composites)
- **Why it applies to M1:** Required for critical manufacturing processes on hydrogen storage tanks, fuel cell stacks, and structural components
- **Evidence expected:** NADCAP Accreditation Certificates, Process Qualification Records

### AS9102 — First Article Inspection (FAI)
- **Scope:** Requirements for first article inspection of new parts or processes
- **Why it applies to M1:** Ensures new parts meet all design and specification requirements before production
- **Evidence expected:** FAI Reports per AS9102 Form 1/2/3, Dimensional Inspection Results

### ISO 10007 — Configuration Management
- **Scope:** Configuration management guidelines for technical products
- **Why it applies to M1:** Essential for controlling engineering changes and maintaining product traceability
- **Evidence expected:** Configuration Management Plan, Engineering Change Records (ECR/ECO)

---

## Controls & Checklists

Located in `templates/`:

- **QMS Audit Checklist** — Internal audit checklist covering all AS9100 clauses
- **FAI Record Template** — AS9102 Form 1/2/3 templates for first article inspection
- **Supplier Qualification Checklist** — Vendor assessment and approval form
- **Non-Conformance Report (NCR) Template** — Template for documenting quality issues

---

## Interface Notes

### Lifecycle Phases
- **LC07 (QA & Process Compliance):** Primary activation — FAI execution, QMS audits, non-conformance tracking
- **LC08 (Certification):** Quality records support type certification and production organization approval

### OPT-IN Domains
- **T/C2-CIRCULAR_CRYOGENIC_CELLS:** LH₂ tank manufacturing quality requirements
- **T/P-PROPULSION:** Fuel cell stack assembly quality requirements
- **I/M2-MAINTENANCE_ENVIRONMENTS:** MRO quality system coordination

---

## Audit Questions

1. Is the QMS certified to AS9100 Rev D or later?
2. Are all special processes (welding, NDT, heat treatment) NADCAP accredited?
3. Are First Article Inspections (FAI) performed per AS9102 for all new parts?
4. Is the configuration management system compliant with ISO 10007?
5. Are internal audits conducted at planned intervals?
6. Are corrective actions tracked to closure?

---

*End of 01_QUALITY README*
