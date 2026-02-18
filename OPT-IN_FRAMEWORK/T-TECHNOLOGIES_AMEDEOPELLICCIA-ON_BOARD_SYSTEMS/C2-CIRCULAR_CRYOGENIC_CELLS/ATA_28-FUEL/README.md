# ATA 28 – Fuel System (Circular Cryogenic Cells – LH₂)

> **Aircraft:** AMPEL360 Q100 Hydrogen-Electric  
> **Technology Domain:** C2-CIRCULAR_CRYOGENIC_CELLS  
> **ATA Chapter:** 28 – Fuel  
> **Authority:** ASIT / BREX Profile AEROSPACEMODEL-PRJ-01  
> **Compliance:** S1000D Issue 5.0, DO-160, CS-25, ARP4754A, ARP4761

---

## 1. Mission

Provide a safe, certifiable cryogenic hydrogen fuel system for the AMPEL360 Q100
hydrogen-electric aircraft. The system stores, distributes, and manages liquid
hydrogen (LH₂) at –253 °C using circular cryogenic cell architecture.

## 2. Scope

| Area | Coverage |
|------|----------|
| LH₂ Storage | Primary and auxiliary cryogenic tanks (28-11, 28-13) |
| Distribution | Cryogenic transfer pumps, insulated lines, pressure control (28-21 – 28-23) |
| Boil-Off Management | BOG capture, venting, thermal management (28-30, 28-31) |
| Safety Systems | H₂ leak detection, pressure relief, fire protection (28-41 – 28-43) |
| Ground Handling | Refueling, defueling, purge, and warm-up procedures |
| Indication | Fuel quantity, temperature, and pressure monitoring (28-41, 28-42) |

## 3. Navigation

| Folder | Contents |
|--------|----------|
| [WBS/](WBS/) | Work Breakdown Structure and task packages |
| [GOVERNANCE/](GOVERNANCE/) | Baseline policy, change authority, approval gates |
| [INDEX/](INDEX/) | Master index of KNOTs, KNUs, requirements, and data modules |
| [28-00-general/](28-00-general/) | H₂ Cryogenic Fuel — General |
| [28-10-storage/](28-10-storage/) | LH₂ tank design, insulation, and structural data |
| [28-11-lh2-primary-tank/](28-11-lh2-primary-tank/) | LH₂ primary storage tank design and certification |
| [28-13-lh2-auxiliary-tank/](28-13-lh2-auxiliary-tank/) | LH₂ auxiliary/extended-range storage tank |
| [28-21-cryogenic-transfer/](28-21-cryogenic-transfer/) | Cryogenic transfer pumps and systems |
| [28-22-insulated-transfer-lines/](28-22-insulated-transfer-lines/) | Vacuum-insulated hydrogen distribution piping |
| [28-23-pressure-control/](28-23-pressure-control/) | Tank pressurization and pressure regulation |
| [28-30-boil-off-management/](28-30-boil-off-management/) | Boil-off gas capture, venting, and management |
| [28-31-thermal-management/](28-31-thermal-management/) | Active/passive cooling and thermal control |
| [28-41-h2-leak-detection/](28-41-h2-leak-detection/) | Multi-sensor hydrogen leak detection |
| [28-42-pressure-relief-venting/](28-42-pressure-relief-venting/) | Over-pressure protection and emergency venting |
| [28-43-fire-detection-suppression/](28-43-fire-detection-suppression/) | H₂ fire detection and suppression |

## 4. Key Contacts

| Role | Stakeholder Code | Responsibility |
|------|-------------------|----------------|
| Program Manager | STK_PM | Schedule, budget, deliverables |
| Systems Engineer | STK_SE | System design and integration |
| Safety Engineer | STK_SAF | Safety assessment, H₂ hazard review |
| Configuration Manager | STK_CM | Baseline control, change management |

## 5. Special Conditions

| ID | Title | Description |
|----|-------|-------------|
| SC-28-H2-001 | Hydrogen Storage and Distribution | Special conditions for H₂ fuel storage and distribution |
| SC-28-CRYO-002 | Cryogenic Temperature Handling | Special conditions for systems at cryogenic temperatures |
| SC-28-ATEX-003 | ATEX Zone Classification | ATEX/IECEx zone classification for all H₂ explosive atmosphere areas (see ATX-28-41-00) |
| SC-28-ESD-004 | ESD Bonding and Grounding | Electrostatic discharge control for H₂ system components (see ESD-28-00-00) |

These special conditions apply in addition to CS-25 standard requirements.

## 6. Technology Domain

- **Domain:** C2-CIRCULAR_CRYOGENIC_CELLS
- **Classification:** Novel Technology
- **Lifecycle Activation:** Full LC01 – LC14
- **BREX Contract:** KITDM-CTR-LM-CSDB_ATA28_H2
- **Determinism Level:** STRICT

All content generation, transformation, and publication for this ATA chapter is
governed by BREX decision rules. No free-form autonomy is permitted.

## 7. Applicable Standards

| Standard | Application |
|----------|-------------|
| S1000D Issue 5.0 | Technical data structure and exchange |
| DO-160 | Environmental qualification |
| ARP4754A | System development assurance |
| ARP4761 | Safety assessment (FHA, FMEA, FTA) |
| ISO 14687-2 | Hydrogen fuel quality |
| CS-25 + Special Conditions | Airworthiness certification |
| ATEX 2014/34/EU | Equipment in explosive atmospheres (EU) |
| IEC 60079 series | Explosive-atmosphere equipment and installation |
| SAE ARP 1489 | Aircraft fuel system ESD bonding and grounding |
| NFPA 2 | Hydrogen technologies code — aircraft operations |

## 8. Quick Reference

```
System Code:    28
Sub-systems:    00, 11, 13, 21, 22, 23, 30, 31, 41, 42, 43
DMC prefix:     DMC-Q100-A-28-
SSOT prefix:    SSOT-Q100-C2-
KNOT prefix:    KNOT-ATA28-
```

---

*Governed by ASIT. All changes require CCB approval per GOVERNANCE_POLICY.md.*
