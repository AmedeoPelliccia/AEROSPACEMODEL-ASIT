# CS-25 Compliance Matrix — ATA 28-10-00 Fuel Storage General (LH₂ Cryogenic Cells)

| Key | Value |
|-----|-------|
| Matrix ID | CM-28-10-CS25 |
| Regulation | EASA CS-25 |
| ATA Code | 28-10-00 |
| Technology Domain | C2 — Circular Cryogenic Cells |
| Aircraft Programme | AMPEL360 Q100 |
| Lifecycle Phase | LC04 (Design Definition) |
| Status | Preliminary (DEV — not baselined) |

> **Note:** CS-25 is written for conventional fuels.  For LH₂ cryogenic
> storage an additional package of **Special Conditions (SC)**, Issue
> Papers and Means of Compliance agreed with EASA is required.  Items
> flagged **SC-LH2-XX** identify those gaps explicitly.

---

## A) Architecture, Integrity and Fuel System Operation

| Req ID | CS-25 Ref | Topic | Applicability | Strategy (MoC) | Evidence / Artefacts | V&V |
|--------|-----------|-------|---------------|----------------|----------------------|-----|
| CM-A-001 | CS 25.951 | General — fuel system installation | High | Architecture analysis + design review | Sys Arch Doc, P&ID LH₂, ICDs, Hazard Zones 600–699 | Review + Analysis |
| CM-A-002 | CS 25.961 | Hot weather / operation | Medium | Thermal simulation + boil-off performance tests | Thermal model, mission profile, boil-off budget, venting logic | Analysis + Test |
| CM-A-003 | CS 25.963 | Fuel tanks general (integrity, drainage, ventilation, expansion) | Very High | Structural analysis + margin definition + leak tests | Tank spec, stress report, leak test plan, vent path analysis | Analysis + Test |
| CM-A-004 | CS 25.965 | Fuel tank tests | Very High | Cryogenic test campaign (pressure, cycles, thermal shock) | Qualification Test Plan/Report, acceptance criteria, instrumentation | Test |
| CM-A-005 | CS 25.967 | Fuel tank installation (supports, loads, vibration) | Very High | FEM + vibration tests + limit/ultimate load analysis | FEM, loads report, installation drawings, fastener substantiation | Analysis + Test |
| CM-A-006 | CS 25.969 | Fuel tank expansion space | High | Ullage definition + transient analysis + pressure/vent control | Vent/relief sizing, pressure control spec, transient simulation | Analysis |
| CM-A-007 | CS 25.971 | Fuel tank sump / drainage | Low–Medium | LH₂ interpretation (phases, purge) + SC | Purge strategy, contamination control, servicing procedure | Analysis + Inspection |
| CM-A-008 | CS 25.973 | Fuel tank filler connection — refuelling | High | Coupling tests + cross-connection prevention + containment | Refuel interface spec, spill containment, human factors | Test + Inspection |
| CM-A-009 | CS 25.975 | Fuel tank vents and relief | Very High | Vent/relief sizing + plume analysis | Relief valve sizing, vent routing, plume/ingestion analysis | Analysis + Test |
| CM-A-010 | CS 25.977 | Fuel tank outlet | Medium | Anti-vortex, anti-cavitation, phase control | Outlet design report, flow test, NPSH-like checks | Analysis + Test |
| CM-A-011 | CS 25.991 | Fuel pumps | Medium | Cryogenic pump qualification + redundancy | Pump qualification plan, reliability data, thermal compatibility | Test + Analysis |
| CM-A-012 | CS 25.993 | Fuel system lines and fittings | Very High | Cryogenic material selection + leak/compatibility tests | Materials & processes spec, line proof/leak tests, insulation details | Test + Inspection |

**Delta LH₂ (SC/MoC):** boil-off phenomenology, relief/vent sizing,
material embrittlement and compatibility, liquid/gas phase management.

---

## B) Fire and Explosion Prevention / Control (Fuel Tank Safety)

| Req ID | CS-25 Ref | Topic | Applicability | Strategy (MoC) | Evidence / Artefacts | V&V |
|--------|-----------|-------|---------------|----------------|----------------------|-----|
| CM-B-001 | CS 25.981 | Fuel tank ignition prevention | Critical | FHA/SSA + zonal safety + ignition source control + bonding/earthing | FHA/SSA (ATA28), Zonal Hazard Analysis, EWIS segregation, ignition source control | Analysis + Inspection |
| CM-B-002 | CS 25.863 / CS 25.867 | Fire protection — compartments | High | Compartment/zone definition + detection + suppression/vent | Fire zone definition, detection/suppression concept, vent strategy | Analysis + Test |
| CM-B-003 | CS 25.869 | Fire protection — systems | High | Integration with ATA 26 / ATA 36 / ATA 24 | System safety integration report, interface control | Analysis |
| CM-B-004 | CS 25.1309 | System safety — catastrophic/hazardous | Critical | ARP4761: FHA → PSSA → SSA + DAL/IDAL allocation | FHA/PSSA/SSA pack, fault trees, FMEA, requirements trace | Analysis |
| CM-B-005 | CS 25.1431 | Electronic equipment — environment | Medium | DO-160G + temperature/pressure + hydrogen environment | DO-160 env qualification, enclosure ratings, ignition control | Test |

**Delta LH₂:** H₂ ignition energy and diffusivity change detection,
ventilation, and ignition-source elimination design.  EASA typically
requires a dedicated safety argument (Issue Paper).

---

## C) Structure, Pressurisation, Discharges and Containment

| Req ID | CS-25 Ref | Topic | Applicability | Strategy (MoC) | Evidence / Artefacts | V&V |
|--------|-----------|-------|---------------|----------------|----------------------|-----|
| CM-C-001 | CS 25.571 | Damage tolerance / fatigue | Very High | Cryogenic fatigue tests/analysis + DT substantiation | Fatigue & DT report, crack growth assumptions, test coupons | Analysis + Test |
| CM-C-002 | CS 25.365 / CS 25.841 | Pressurisation / compartments interaction | Medium | Vent interaction with cabin/structure | Pressure relief integration, structural margins | Analysis |
| CM-C-003 | CS 25.901 et seq. | Engine/APU installation interfaces | Medium | Plume/ingestion/clearance analysis | Plume analysis, separation distances, hazard assessment | Analysis |

---

## D) Materials, Processes, Inspection and Maintenance

| Req ID | CS-25 Ref | Topic | Applicability | Strategy (MoC) | Evidence / Artefacts | V&V |
|--------|-----------|-------|---------------|----------------|----------------------|-----|
| CM-D-001 | CS 25.603 / CS 25.605 | Materials / fabrication | Very High | Cryogenic-compatible material selection (embrittlement, permeation) | Material allowables, M&P spec, welding/brazing qualification | Analysis + Test |
| CM-D-002 | CS 25.1529 | Instructions for Continued Airworthiness | High | LH₂-specific ICA: purges, inspections, leak checks, sensors | ICA draft, maintenance tasks, intervals, troubleshooting | Inspection + Review |
| CM-D-003 | CS 25.1301 | Function and installation | High | Verifiable functional requirements + installation conformity | Compliance checklist, installation conformity | Inspection |

---

## Special Conditions — LH₂ Gaps Beyond CS-25

These items fall outside the literal CS-25 text (or are only indirectly
covered) and require explicit Special Conditions agreed with EASA:

| SC ID | Topic | Description | MoC |
|-------|-------|-------------|-----|
| SC-LH2-01 | Boil-off management | Pressure, vent, normal/abnormal modes, dispatch criteria | Analysis + Test |
| SC-LH2-02 | Hydrogen detection | Sensor locations, thresholds, alert logic, SIL/DAL allocation | Analysis + Test + Inspection |
| SC-LH2-03 | Vent plume hazard | Ingestion, external ignition, cavity accumulation | Analysis + Test |
| SC-LH2-04 | Cryogenic thermal shock | Structure + insulation + interface survivability | Analysis + Test |
| SC-LH2-05 | Permeation / leak-before-burst | Quantitative criteria for hydrogen permeation and LBB argument | Analysis + Test |
| SC-LH2-06 | Ground operations | Refuelling, purging, degassing, emergency procedures | Inspection + Test |

---

## Minimum Evidence Package (Certification-Ready)

| # | Artefact |
|---|----------|
| 1 | ATA28_LH2_FuelStorage_SystemArchitecture.md |
| 2 | CS25_ComplianceMatrix_ATA28_LH2.yaml |
| 3 | FHA_PSSA_SSA_ATA28_LH2.pdf |
| 4 | Tank_Qualification_TestPlan_Report.pdf |
| 5 | VentingAndReliefSizing_Report.pdf |
| 6 | PlumeAndAccumulation_Analysis_Report.pdf |
| 7 | MaterialsAndProcesses_Cryogenic_Qualification.pdf |
| 8 | ICA_ATA28_LH2_FuelStorage_Draft.pdf |

---

## Governance

This compliance matrix resides in `KDB/DEV/trade-studies/` and is **not
baselined**.  Promotion to `KDB/LM/SSOT/` requires:

- BREX validation
- Trace coverage verification
- STK_ENG / STK_SAF approval
- ECR submission via `GOVERNANCE/CHANGE_CONTROL/`
