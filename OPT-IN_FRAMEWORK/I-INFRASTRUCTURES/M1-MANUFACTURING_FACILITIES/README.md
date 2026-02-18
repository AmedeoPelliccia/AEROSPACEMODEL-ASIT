# M1 — Manufacturing Facilities

**Domain:** I-INFRASTRUCTURES / M1  
**ATA Designation:** 85-00-00 (Manufacturing Facilities)  
**Program:** AMPEL360 Q100  
**Authority:** ASIT (Aircraft Systems Information Transponder)

---

## Purpose

The **M1-MANUFACTURING_FACILITIES** subdomain organizes manufacturing facility standards, regulations, and operational controls that govern the production, assembly, testing, and quality assurance of the AMPEL360 Q100 aircraft and its hydrogen-powered propulsion systems.

M1 establishes the industrial baseline for:
- Quality management systems (QMS) aligned with aerospace standards
- Occupational health & safety (OHS) compliance
- Environmental management and hazardous materials (HAZMAT) handling
- Machinery and process safety operations
- Warehouse, inventory, and logistics traceability
- Additive manufacturing (AM) quality gates
- Airworthiness production organization approvals (EASA Part 21 Subpart G, FAA 14 CFR Part 21)

---

## Subdomain Structure

| Subdomain | Code | Description | Key Standards/Regulations |
|-----------|------|-------------|---------------------------|
| **Quality** | 01 | Quality Management System | ISO 9001, AS9100 Rev D, AS9120, NADCAP, AS9102, ISO 10007 |
| **OHS Safety Workplace** | 02 | Occupational Health & Safety / Workplace | ISO 45001, ISO 6385, ISO 45003, ES RD 486/1997, OSHA 29 CFR 1910 |
| **Environment HAZMAT** | 03 | Environment & Hazardous Materials | ISO 14001, REACH/CLP, NFPA 2, NFPA 55 |
| **Machinery Process Safety** | 04 | Machinery & Process Safety Operations | ISO 12100, ISO 13849, ISO 9241 |
| **Warehouse Inventory** | 05 | Warehouse, Inventory & Logistics | RFID/QR Traceability, ISO 17025 (Calibration & Metrology) |
| **Additive Manufacturing** | 06 | Additive Manufacturing / On-Demand 3D Print | AM Quality Gate Criteria, Material Batch Traceability, NADCAP |
| **Airworthiness Production** | 07 | Airworthiness Production Organisation Approvals | EASA Part 21 Subpart G, FAA 14 CFR Part 21 |
| **Templates Meta** | 90 | Template `.meta.yaml` sidecars and schemas | — |
| **References** | 99 | External standards, regulations, and reference links | — |

---

## Directory Conventions

Each subdomain directory (01–07) contains:

- **`README.md`** — Subdomain scope, applicable standards/regulations, controls/checklists, and interface notes
- **`standards/`** — Standard record files (`.yaml`, `.md`) describing how each standard applies to M1
- **`regulation/`** — Regulatory compliance records (where applicable)
- **`controls/`** — Operational checklists, audit templates, and control procedures
- **`templates/`** — QMS, FAI, or other template files (where applicable)

Subdomain 90 contains:
- **`meta_sidecars/`** — Template `.meta.yaml` files for M1 records
- **`schemas/`** — JSON Schema definitions for validating M1 `.meta.yaml` files

Subdomain 99 contains:
- External reference links and documentation pointers

---

## Standard Record Format

Each standard or regulation record in M1 follows this structure:

```yaml
id: M1-STD-<CODE>
type: STANDARD_RECORD
title: <Full Standard/Regulation Title>
owner: ASIT
revision: 0.1.0
status: draft
lc_phase: LC07_QA_PROCESS
work_package: M1-<WP-CODE>
ata: 85-00-00
domain: I-INFRASTRUCTURES/M1
created_on: to be set during baseline finalization
last_updated_on: to be set during baseline finalization
integrity:
  checksum: to be generated upon baseline finalization
  algorithm: sha256
standard:
  id: <STANDARD_ID>
  full_title: <Full Standard/Regulation Title>
  issuing_body: <ISO, EASA, FAA, OSHA, etc.>
  norm_type: system_management | regulation | technical_process | control
  edition: <Edition/Version>
  scope: <Brief description>
  why_it_applies_to_M1: <Justification for M1 domain>
  evidence_expected:
    - <Evidence type 1>
    - <Evidence type 2>
    - ...
  audit_questions:
    - <Audit question 1>
    - <Audit question 2>
    - ...
  interfaces:
    lc_phases:
      - LC07_QA_PROCESS
      - LC10_INDUSTRIAL_SUPPLY_CHAIN
      - LC12_MRO_CONTINUED_AIRWORTHINESS
    ata_chapters:
      - 85-00-00
    opt_in_domains:
      - I-INFRASTRUCTURES/M1
      - T/C2-CIRCULAR_CRYOGENIC_CELLS
      - T/P-PROPULSION
links:
  reqs: []
  safety: []
  verification: []
tags:
  - M1
  - manufacturing
  - standard
```

**Note:** This is the complete structure. See `90_TEMPLATES_META/meta_sidecars/M1_standard_record.meta.yaml` for the full template.

This format ensures:
- **Traceability** to lifecycle phases, ATA chapters, and OPT-IN domains
- **Auditability** via explicit audit questions and evidence expectations
- **Reproducibility** through deterministic record structure

---

## Lifecycle Integration

M1 primarily activates during the following lifecycle phases:

### LC07 — QA & Process Compliance
- First Article Inspection (FAI) per AS9102
- QMS audit trail generation
- Process validation and capability studies
- Non-conformance tracking and corrective action

### LC10 — Industrial & Supply Chain
- Production line setup and validation
- Supplier qualification and audits
- Material traceability (RFID/QR tagging)
- Manufacturing process instructions (MPIs)
- Tooling and test rig qualification

### LC12 — Continued Airworthiness & MRO
- Production organization approval maintenance (EASA Part 21 Subpart G)
- Spare parts manufacturing traceability
- Repair station integration
- Obsolescence management and supply chain continuity

---

## Governance

- **Owner:** ASIT (Aircraft Systems Information Transponder)
- **Responsible Stakeholder:** STK_CM (Configuration Manager), STK_QA (Quality Assurance)
- **Change Control:** ECR/ECO via Configuration Control Board (CCB)
- **Baseline Authority:** Master BREX Authority (`ASIT/GOVERNANCE/master_brex_authority.yaml`)
- **Lifecycle Activation Rules:** Defined in `lifecycle/T_SUBDOMAIN_LC_ACTIVATION.yaml`

All changes to M1 structure, standards, or controls require:
1. Engineering Change Request (ECR) submission
2. Impact assessment on downstream lifecycle phases
3. CCB approval
4. Formal baseline update

---

## Related Documents

| Document | Path | Purpose |
|----------|------|---------|
| OPT-IN_FRAMEWORK README | `../README.md` | Canonical architecture overview |
| I-INFRASTRUCTURES Index | `../00_INDEX.md` | I-INFRASTRUCTURES subdomain index |
| M1 Index | `00_INDEX.md` | M1 subdomain navigation |
| LC Phase Registry | `../../../lifecycle/LC_PHASE_REGISTRY.yaml` | Lifecycle phase definitions |
| T-Subdomain LC Activation | `../../../lifecycle/T_SUBDOMAIN_LC_ACTIVATION.yaml` | Lifecycle activation rules |
| Master BREX Authority | `../../../ASIT/GOVERNANCE/master_brex_authority.yaml` | BREX decision rules |
| ATA 28 H2 Cryogenic Instructions | `../../../.github/instructions/ata28_h2_cryogenic.instructions.md` | Hydrogen safety procedures |
| ATA 71 Fuel Cell Instructions | `../../../.github/instructions/ata71_fuel_cell.instructions.md` | Fuel cell production safety |

---

## Version History

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0.0 | 2026-02-18 | ASIT | Initial M1 subdomain structure for AMPEL360 Q100 production |

---

*End of M1 — Manufacturing Facilities README*
