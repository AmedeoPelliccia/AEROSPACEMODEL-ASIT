# CS-25 Compliance Matrix — ATA 28-11-00 LH₂ Primary Tank (Cryogenic Cells)

| Key | Value |
|-----|-------|
| Matrix ID | CM-28-11-CS25 |
| Regulation | EASA CS-25 |
| ATA Code | 28-11-00 |
| Technology Domain | C2 — Circular Cryogenic Cells |
| Aircraft Programme | AMPEL360 Q100 |
| Lifecycle Phase | LC04 (Design Definition) |
| Status | Preliminary (DEV — not baselined) |

> **Note:** CS-25 is written for conventional fuels.  For LH₂ primary
> tank storage an additional package of **Special Conditions (SC)**, Issue
> Papers and Means of Compliance agreed with EASA is required.  Items
> flagged **SC-LH2-XX** identify those gaps explicitly.  14 CFR 25.981
> explosion prevention and 25.963 fuel tank structural loads remain
> applicable via performance-based safety arguments.

---

## A) Tank Structural Integrity and Loads

| Req ID | CS-25 Ref | Topic | Applicability | Strategy (MoC) | Evidence / Artefacts | V&V |
|--------|-----------|-------|---------------|----------------|----------------------|-----|
| CM-A-001 | CS 25.963 | Fuel tanks general — integrity, drainage, ventilation, expansion | Very High | Structural analysis + cryogenic margin definition + leak tests | Tank structural specification, stress report (limit/ultimate with cryogenic loads), leak test plan, thermal contraction analysis | Analysis + Test |
| CM-A-002 | CS 25.965 | Fuel tank tests | Very High | Cryogenic test campaign (pressure, cycles, thermal shock) | Qualification Test Plan/Report, acceptance criteria, instrumentation specification | Test |
| CM-A-003 | CS 25.967 | Fuel tank installation — supports, loads, vibration | Very High | FEM + vibration tests + limit/ultimate load analysis | FEM (including thermal contraction mismatch), loads report, installation drawings, support thermal bridge analysis | Analysis + Test |
| CM-A-004 | CS 25.571 | Damage tolerance / fatigue | Very High | Cryogenic fatigue tests/analysis + DT substantiation | Fatigue and DT report, crack growth assumptions (Al-Li at 20 K), test coupons (parent and weld material) | Analysis + Test |

**Delta LH₂ (SC/MoC):** cryogenic contraction mismatch (inner tank at
20 K vs jacket at ambient), hydrogen embrittlement, pressure cycling,
and crashworthiness for non-integral tanks.

---

## B) Pressure, Venting and Boil-Off Management

| Req ID | CS-25 Ref | Topic | Applicability | Strategy (MoC) | Evidence / Artefacts | V&V |
|--------|-----------|-------|---------------|----------------|----------------------|-----|
| CM-B-001 | CS 25.969 | Fuel tank expansion space | High | Ullage definition + transient analysis + pressure/vent control | Vent/relief sizing, pressure control specification, transient simulation (boil-off budget) | Analysis |
| CM-B-002 | CS 25.975 | Fuel tank vents and relief | Very High | Vent/relief sizing + plume analysis | Relief valve sizing, vent routing, plume/ingestion analysis | Analysis + Test |

**Delta LH₂:** LH2 boil-off phenomenology, pressure control at
operating pressures (~255–351 kPa), relief/vent sizing, ullage
management, and phase transition behaviour.

---

## C) Fire, Explosion and Ignition Prevention

| Req ID | CS-25 Ref | Topic | Applicability | Strategy (MoC) | Evidence / Artefacts | V&V |
|--------|-----------|-------|---------------|----------------|----------------------|-----|
| CM-C-001 | CS 25.981 | Fuel tank ignition prevention | Critical | FHA/SSA + zonal safety + ignition source control + bonding/earthing | FHA/SSA (ATA 28-11), Zonal Hazard Analysis, ignition source control, CDCCLs/limitations | Analysis + Inspection |
| CM-C-002 | CS 25.1309 | System safety — catastrophic/hazardous | Critical | ARP4761: FHA → PSSA → SSA + DAL/IDAL allocation | FHA/PSSA/SSA pack, fault trees, FMEA, requirements trace | Analysis |

**Delta LH₂:** H₂ ignition energy and diffusivity; detection,
ventilation, and ignition-source elimination.  14 CFR 25.981 requires
no ignition source where catastrophic failure could occur.

---

## D) Materials, Processes and Inspection

| Req ID | CS-25 Ref | Topic | Applicability | Strategy (MoC) | Evidence / Artefacts | V&V |
|--------|-----------|-------|---------------|----------------|----------------------|-----|
| CM-D-001 | CS 25.603 / CS 25.605 | Materials / fabrication | Very High | Cryogenic-compatible material selection (embrittlement, permeation) | Material allowables (Al-Li 2195 at 20 K), M&P specification, welding qualification | Analysis + Test |
| CM-D-002 | CS 25.1529 | Instructions for Continued Airworthiness | High | LH₂-specific ICA: vacuum checks, inspections, leak checks, sensors | ICA draft, maintenance tasks (vacuum servicing), inspection intervals | Inspection + Review |

---

## Special Conditions — LH₂ Gaps Beyond CS-25

These items fall outside the literal CS-25 text (or are only indirectly
covered) and require explicit Special Conditions agreed with EASA:

| SC ID | Topic | Description | MoC |
|-------|-------|-------------|-----|
| SC-LH2-01 | Boil-off management | Pressure, vent, normal/abnormal modes, dispatch criteria | Analysis + Test |
| SC-LH2-02 | Hydrogen detection | Sensor locations, thresholds, alert logic, SIL/DAL allocation | Analysis + Test + Inspection |
| SC-LH2-03 | Cryogenic thermal shock | Structure + insulation + interface survivability | Analysis + Test |
| SC-LH2-04 | Vacuum integrity maintenance | MLI vacuum monitoring, degradation detection, servicing requirements | Analysis + Inspection |
| SC-LH2-05 | Crashworthiness | Two-layer safety approach (crashworthy airframe + crash-safe tank) for non-integral LH₂ tanks | Analysis + Test |

---

## Minimum Evidence Package (Certification-Ready)

| # | Artefact |
|---|----------|
| 1 | ATA28-11\_LH2\_PrimaryTank\_StructuralSpec.md |
| 2 | CS25\_compliance\_matrix.yaml |
| 3 | FHA\_PSSA\_SSA\_ATA28-11\_LH2.pdf |
| 4 | Tank\_Qualification\_TestPlan\_Report.pdf |
| 5 | VentingAndReliefSizing\_Report.pdf |
| 6 | MaterialsAndProcesses\_Cryogenic\_Qualification.pdf |
| 7 | ThermalBridge\_HeatLeak\_Decomposition.pdf |
| 8 | ICA\_ATA28-11\_LH2\_PrimaryTank\_Draft.pdf |

---

## Governance

This compliance matrix resides in `KDB/DEV/trade-studies/` and is **not
baselined**.  Promotion to `KDB/LM/SSOT/` requires:

- BREX validation
- Trace coverage verification
- STK_ENG / STK_SAF approval
- ECR submission via `GOVERNANCE/CHANGE_CONTROL/`
