# P-PROGRAMS Domain

**ATA Chapters 06–12: Program-Level Procedures and Servicing**

---

## Scope

The P-PROGRAMS domain contains program-level procedures for aircraft handling, servicing, and ground operations. This includes physical characteristics, ground handling procedures, and routine servicing operations.

---

## Subdomain Structure

The P-PROGRAMS domain is organized into two subdomains that mirror the classic distinction in aerospace documentation:

### P — Product Definition
**What the product is** — Chapters that define the aircraft's physical characteristics, weight, and identification on the ground. This subdomain feeds into configuration management workflows.

### S — Service Instruction
**How you handle it** — Chapters that describe how ground crews interact with the aircraft. This subdomain feeds into ground operations manual workflows.

---

## ATA Chapters

### P — Product Definition

#### ATA 06 – Dimensions and Areas
Aircraft dimensions, areas, zonal arrangements, and access information.

#### ATA 08 – Leveling and Weighing
Aircraft leveling procedures and weighing operations.

#### ATA 11 – Placards and Markings
Required placards, markings, and identification plates.

### S — Service Instruction

#### ATA 07 – Lifting and Shoring
Jacking, lifting, and shoring procedures for maintenance and ground handling.

#### ATA 09 – Towing and Taxiing
Towing procedures, taxi operations, and ground movement.

#### ATA 10 – Parking, Mooring, Storage, and Return to Service
Parking procedures, storage requirements, and return-to-service checks.

#### ATA 12 – Servicing
Routine servicing procedures for fluids, gases, and consumables.

---

## Lifecycle Applicability

Standard lifecycle profile applies to this domain:
- **Mandatory Phases:** LC01, LC02, LC04, LC06, LC08, LC10, LC12, LC13
- **Optional Phases:** LC03, LC05, LC07, LC09, LC11, LC14

---

## Cross-Domain Integration

### P-PROGRAMS → O-ORGANIZATIONS
Program-level service procedures must comply with the organizational maintenance policy (ATA 01) and airworthiness limitations (ATA 04/05) defined in O-ORGANIZATIONS. Time limits (ATA 05) constrain servicing intervals in ATA 12; airworthiness limitations constrain product configuration in ATA 06/08/11.

### P-PROGRAMS → T-TECHNOLOGIES
Service instructions (ATA 07 Lifting, ATA 09 Towing, ATA 10 Parking, ATA 12 Servicing) depend on on-board systems and servicing interfaces documented in the T-TECHNOLOGIES domain. Detailed servicing procedures should be authored with reference to the relevant T-TECHNOLOGIES system- and technology-level documentation (for example, hydrogen storage and distribution systems, electrical power systems, and hydraulic systems).

### P-PROGRAMS → I-INFRASTRUCTURES
Servicing procedures (ATA 12) and storage operations (ATA 10) are performed using ground support equipment and infrastructure documented in I-INFRASTRUCTURES. Specifically:
- **M2-MAINTENANCE_ENVIRONMENTS**: Provides facilities for leveling (ATA 08), weighing, and routine servicing
- **O-OPERATIONS_SERVICE_STRUCTURES**: Provides airport infrastructure for parking, mooring, and H₂ servicing logistics

### P-PROGRAMS → N-NEURAL_NETWORKS
Product definition data (ATA 06, 08, 11) feeds into the Digital Product Passport (ATA 96, N-NEURAL_NETWORKS/D) for configuration traceability. Return-to-service data (ATA 10) and servicing records (ATA 12) are captured in the DPP as operational lifecycle entries.

---

## Related Documents

- [OPT-IN_FRAMEWORK Main README](../README.md)
- [O-ORGANIZATIONS Domain](../O-ORGANIZATIONS/README.md)
- [T-TECHNOLOGIES Domain](../T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS/README.md)
- [I-INFRASTRUCTURES Domain](../I-INFRASTRUCTURES/README.md)
- [N-NEURAL_NETWORKS Domain](../N-NEURAL_NETWORKS/README.md)
- [Lifecycle Phase Registry](../../lifecycle/LC_PHASE_REGISTRY.yaml)
- [T-Subdomain LC Activation Rules](../../lifecycle/T_SUBDOMAIN_LC_ACTIVATION.yaml)

---
