# M2 — Maintenance Environments

**Domain:** I-INFRASTRUCTURES / M2  
**ATA Designation:** 08I, 10I, 12I (Maintenance Infrastructure)  
**Program:** AMPEL360 Q100  
**Authority:** ASIT (Aircraft Systems Information Transponder)

---

## Purpose

The **M2-MAINTENANCE_ENVIRONMENTS** subdomain organizes the ground-based infrastructure, facilities, and equipment required to perform in-service maintenance of the AMPEL360 Q100 aircraft. It covers the full maintenance ecosystem from line stations and heavy-maintenance hangars through to component and shop-level workstations.

M2 establishes the maintenance infrastructure baseline for:
- Aircraft leveling and weighing facilities
- Parking, mooring, storage, and return-to-service (RTS) infrastructure
- Servicing equipment and fluid-handling systems

---

## Subdomain Structure

| Category | Directory | ATA Reference | Description |
|----------|-----------|---------------|-------------|
| **Leveling & Weighing** | [`ATA_08-LEVELING_AND_WEIGHING_INFRA/`](ATA_08-LEVELING_AND_WEIGHING_INFRA/) | ATA 08I | Jacking, leveling, and weighing facilities and GSE |
| **Parking, Mooring & Storage** | [`ATA_10-PARKING_MOORING_STORAGE_RTS_INFRA/`](ATA_10-PARKING_MOORING_STORAGE_RTS_INFRA/) | ATA 10I | Parking stands, mooring fixtures, storage bays, and return-to-service rigs |
| **Servicing** | [`ATA_12-SERVICING_INFRA/`](ATA_12-SERVICING_INFRA/) | ATA 12I | Servicing carts, fluid-handling equipment, and replenishment systems |

---

## Directory Conventions

Each ATA category directory contains (when populated):

- **`README.md`** — Category scope, applicable standards/regulations, and interface notes
- **`standards/`** — Standard record files describing how each standard applies to M2
- **`regulation/`** — Regulatory compliance records (where applicable)
- **`controls/`** — Operational checklists, inspection templates, and control procedures
- **`templates/`** — Maintenance task, acceptance, or tooling template files (where applicable)

---

## Lifecycle Integration

M2 primarily activates during the following lifecycle phases:

### LC06 — Integration Test & PMU
- Maintenance facility acceptance testing
- Ground support equipment (GSE) commissioning
- Servicing rig qualification and functional checks

### LC10 — Industrial & Supply Chain
- Maintenance facility setup and tooling provisioning
- Spare-parts logistics and traceability infrastructure
- Fluid-handling system procurement and qualification

### LC12 — Continued Airworthiness & MRO
- Routine maintenance environment surveillance
- Maintenance organisation approval upkeep (EASA Part 145, FAA Part 145)
- Return-to-service documentation and tooling calibration records
- Servicing infrastructure upgrade and obsolescence management

---

## Governance

- **Owner:** ASIT (Aircraft Systems Information Transponder)
- **Responsible Stakeholder:** STK_CM (Configuration Manager), STK_MRO (MRO Manager)
- **Change Control:** ECR/ECO via Configuration Control Board (CCB)
- **Baseline Authority:** Master BREX Authority (`ASIT/GOVERNANCE/master_brex_authority.yaml`)
- **Lifecycle Activation Rules:** Defined in `lifecycle/T_SUBDOMAIN_LC_ACTIVATION.yaml`

All changes to M2 structure, standards, or controls require:
1. Engineering Change Request (ECR) submission
2. Impact assessment on downstream lifecycle phases
3. CCB approval
4. Formal baseline update

---

## Related Documents

| Document | Path | Purpose |
|----------|------|---------|
| OPT-IN_FRAMEWORK README | `../../README.md` | Canonical architecture overview |
| I-INFRASTRUCTURES Index | `../00_INDEX.md` | I-INFRASTRUCTURES subdomain index |
| M1 README | `../M1-MANUFACTURING_FACILITIES/README.md` | Manufacturing Facilities subdomain |
| O subdomain directory | `../O-OPERATIONS_SERVICE_STRUCTURES/` | Operations & Service Structures subdomain |
| LC Phase Registry | `../../../lifecycle/LC_PHASE_REGISTRY.yaml` | Lifecycle phase definitions |
| T-Subdomain LC Activation | `../../../lifecycle/T_SUBDOMAIN_LC_ACTIVATION.yaml` | Lifecycle activation rules |
| Master BREX Authority | `../../../ASIT/GOVERNANCE/master_brex_authority.yaml` | BREX decision rules |
| ATA 28 H2 Cryogenic Instructions | `../../../.github/instructions/ata28_h2_cryogenic.instructions.md` | Hydrogen safety procedures |

---

## Version History

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0.0 | 2026-02-18 | ASIT | Initial M2 subdomain README for AMPEL360 Q100 maintenance environments |

---

*End of M2 — Maintenance Environments README*
