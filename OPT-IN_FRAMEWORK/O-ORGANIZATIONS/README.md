# O-ORGANIZATIONS Domain

**ATA Chapters 00–05: Organizational and Governance Documentation**

---

## Scope

The O-ORGANIZATIONS domain contains organizational, governance, and policy-level documentation that establishes the framework for aircraft maintenance, operations, and airworthiness management.

---

## Subdomain Structure

The O-ORGANIZATIONS domain is organized into two subdomains that separate regulatory authority from business enforcement:

### A — Authoritative
**Agency, regulatory, and legal-derived** — Chapters rooted in certification authority requirements, airworthiness directives, and regulatory mandates. These define the legal framework within which the aircraft must operate.

### B — Business Enforcement
**Operator business policies and enforcement** — Chapters driven by the operator's business decisions for maintenance programs, organizational structure, and support logistics. These translate regulatory requirements into actionable business processes.

---

## ATA Chapters

### A — Authoritative

#### ATA 00 – General
General information, abbreviations, and introductory material applicable to all aircraft systems.

#### ATA 04 – Airworthiness Limitations
Mandatory airworthiness limitations, life-limited parts, and certification maintenance requirements.

#### ATA 05 – Time Limits / Maintenance Checks
Time limits, maintenance check intervals, and inspection program definitions.

### B — Business Enforcement

#### ATA 01 – Maintenance Policy
Maintenance program policies, scheduled maintenance requirements, and maintenance planning documents.

#### ATA 02 – Operations Organization
Operational procedures, flight operations manual content, and operational policies.

#### ATA 03 – Support Information
Support equipment, tooling, and support infrastructure information.

---

## Lifecycle Applicability

Standard lifecycle profile applies to this domain:
- **Mandatory Phases:** LC01, LC02, LC04, LC06, LC08, LC10, LC12, LC13
- **Optional Phases:** LC03, LC05, LC07, LC09, LC11, LC14

---

## Cross-Domain Integration

### O-ORGANIZATIONS → P-PROGRAMS
Organizational maintenance policies (ATA 01) and airworthiness limitations (ATA 04/05) establish the governance baseline that P-PROGRAMS service instructions must comply with. Time limits and inspection intervals (ATA 05) directly constrain servicing procedures (ATA 12) and storage requirements (ATA 10).

### O-ORGANIZATIONS → T-TECHNOLOGIES
Airworthiness limitations (ATA 04) and time limits (ATA 05) apply across all T-TECHNOLOGIES on-board systems. All technology subdomain content must trace to organizational airworthiness mandates defined here, particularly Novel Technology subdomains (C2, I2, P-PROPULSION) which carry additional Special Conditions.

### O-ORGANIZATIONS → I-INFRASTRUCTURES
Maintenance program policies (ATA 01) drive the infrastructure requirements for M2-MAINTENANCE_ENVIRONMENTS (hangars, shops). Support information (ATA 03) defines the ground support equipment and tooling catalogued in I-INFRASTRUCTURES/O-OPERATIONS_SERVICE_STRUCTURES.

### O-ORGANIZATIONS → N-NEURAL_NETWORKS
General documentation conventions (ATA 00) define abbreviation and data governance standards referenced by the Digital Thread & Traceability subdomain (ATA 96). AI Governance & Assurance policies align with the organizational compliance framework (ATA 02 — Operations Organization).

---

## Related Documents

- [OPT-IN_FRAMEWORK Main README](../README.md)
- [P-PROGRAMS Domain](../P-PROGRAMS/README.md)
- [T-TECHNOLOGIES Domain](../T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS/README.md)
- [I-INFRASTRUCTURES Domain](../I-INFRASTRUCTURES/README.md)
- [N-NEURAL_NETWORKS Domain](../N-NEURAL_NETWORKS/README.md)
- [Lifecycle Phase Registry](../../lifecycle/LC_PHASE_REGISTRY.yaml)
- [T-Subdomain LC Activation Rules](../../lifecycle/T_SUBDOMAIN_LC_ACTIVATION.yaml)

---
