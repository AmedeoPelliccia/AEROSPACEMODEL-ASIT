# MTL-28-11-00 — Method Token Library

**ATA 28-11-00 LH₂ Primary Tank General**

| Key | Value |
|-----|-------|
| MTL ID | MTL-28-11-00 |
| ATA Code | 28-11-00 |
| Technology Domain | C2 — Circular Cryogenic Cells |
| Aircraft Programme | AMPEL360 Q100 |
| Lifecycle Phase | LC04 (Design Definition) |
| Status | Preliminary |
| Token Pattern | `MTK-28-11-{DOMAIN}-{SEQ}` |
| Total Tokens | 19 |

## Purpose

Tokenises every subject title under ATA 28-11-00 into a deterministic
method identifier for model programming, parametric analysis pipelines,
and automated traceability.  Each token maps 1-to-1 to a trade-study
section, compliance requirement group, evaluation criterion, or special
condition.

---

## Token Inventory

### Domain: TS — Trade Studies (3 tokens)

| Token | Subject | Source | Method Class |
|-------|---------|--------|--------------|
| MTK-28-11-TS-001 | Tank Architecture | TS-28-11-TS01 | `geometry_selection` |
| MTK-28-11-TS-002 | Containment Materials | TS-28-11-TS02 | `material_selection` |
| MTK-28-11-TS-003 | Insulation and Thermal Control | TS-28-11-TS03 | `thermal_selection` |

#### MTK-28-11-TS-001 — Tank Architecture

- **Inputs:** `stored_lh2_mass_kg`, `lh2_density_kg_per_m3`, `required_volume_m3`, `reference_heat_flux_W_per_m2`
- **Outputs:** `selected_geometry`, `surface_area_m2`, `boil_off_pct_per_day`, `gravimetric_efficiency`
- Geometry trade: compare spherical, cylindrical (hemispherical endcaps), and conformal architectures.

#### MTK-28-11-TS-002 — Containment Materials

- **Inputs:** `cryogenic_temperature_K`, `operating_pressure_kPa`, `fatigue_cycle_count`
- **Outputs:** `selected_material`, `yield_strength_20K_MPa`, `uts_20K_MPa`, `permeation_risk_class`
- Material trade: compare Al-Li 2195, austenitic stainless 304L, and composite overwrap.

#### MTK-28-11-TS-003 — Insulation and Thermal Control

- **Inputs:** `warm_boundary_K`, `cold_boundary_K`, `surface_area_m2`, `penetration_count`
- **Outputs:** `selected_insulation`, `heat_flux_W_per_m2`, `boil_off_rate_kg_per_day`, `vacuum_requirement_Pa`
- Insulation trade: compare vacuum-jacket MLI, foam, and hybrid active cooling.

---

### Domain: CM — Compliance Matrix (4 tokens)

| Token | Subject | Source | Method Class | CS-25 Refs |
|-------|---------|--------|--------------|------------|
| MTK-28-11-CM-001 | Tank Structural Integrity and Loads | § A | `structural_compliance` | 25.963, 25.965, 25.967, 25.571 |
| MTK-28-11-CM-002 | Pressure Venting and Boil-Off Management | § B | `pressure_vent_compliance` | 25.969, 25.975 |
| MTK-28-11-CM-003 | Fire Explosion and Ignition Prevention | § C | `ignition_prevention_compliance` | 25.981, 25.1309 |
| MTK-28-11-CM-004 | Materials Processes and Inspection | § D | `materials_inspection_compliance` | 25.603, 25.605, 25.1529 |

---

### Domain: SC — Special Conditions (5 tokens)

| Token | Subject | Source | Method Class |
|-------|---------|--------|--------------|
| MTK-28-11-SC-001 | Boil-Off Management | SC-LH2-01 | `boil_off_management` |
| MTK-28-11-SC-002 | Hydrogen Detection | SC-LH2-02 | `h2_detection` |
| MTK-28-11-SC-003 | Cryogenic Thermal Shock | SC-LH2-03 | `thermal_shock` |
| MTK-28-11-SC-004 | Vacuum Integrity Maintenance | SC-LH2-04 | `vacuum_integrity` |
| MTK-28-11-SC-005 | Crashworthiness | SC-LH2-05 | `crashworthiness` |

---

### Domain: EC — Evaluation Criteria (7 tokens)

| Token | Subject | Weight | Method Class |
|-------|---------|--------|--------------|
| MTK-28-11-EC-001 | Boil-Off Performance | 20 % | `scoring_boiloff` |
| MTK-28-11-EC-002 | Structural Mass Efficiency | 20 % | `scoring_mass` |
| MTK-28-11-EC-003 | Safety | 20 % | `scoring_safety` |
| MTK-28-11-EC-004 | Certification Risk | 15 % | `scoring_certification` |
| MTK-28-11-EC-005 | Manufacturability | 10 % | `scoring_manufacturing` |
| MTK-28-11-EC-006 | Maintainability | 10 % | `scoring_maintainability` |
| MTK-28-11-EC-007 | Cost | 5 % | `scoring_cost` |

---

## Token Count Summary

| Domain | Name | Tokens |
|--------|------|--------|
| TS | Trade Studies | 3 |
| CM | Compliance Matrix | 4 |
| SC | Special Conditions | 5 |
| EC | Evaluation Criteria | 7 |
| | **Total** | **19** |

---

## Traceability

- **Derives from:** TS-28-11-TS01, TS-28-11-TS02, TS-28-11-TS03, CM-28-11-CS25

## Feeds

| Lifecycle | Artifact |
|-----------|----------|
| LC05 | Parametric model integration (method tokens as API) |
| LC05 | Automated trade-study scoring pipelines |
| LC06 | Verification test matrix (token-to-test mapping) |

---

## Governance

This MTL resides in `KDB/DEV/mtl/` and is **not baselined**.
Promotion to `KDB/LM/SSOT/` requires:

- BREX validation
- Trace coverage verification
- STK_ENG approval
- ECR submission via `GOVERNANCE/CHANGE_CONTROL/`
