# Standard Token Procedures (STP) — ATA 28-11-00 LH₂ Primary Tank

**Version:** 0.1.0 | **Status:** Preliminary (DEV) | **Date:** 2026-02-16

> **A model consuming one STP token receives the full end-to-end
> procedure — inputs, sequenced steps, intermediate hand-offs,
> terminal outputs, and acceptance gates.**

## Procedure Index

| STP Token | Title | Class | Steps | Tokens Consumed |
|-----------|-------|-------|------:|----------------:|
| STP-28-11-001 | LH₂ Tank Sizing | sizing | 7 | 7 |
| STP-28-11-002 | Structural Substantiation | structural | 6 | 6 |
| STP-28-11-003 | Trade Evaluation | evaluation | 5 | 5 |
| STP-28-11-004 | CS 25 Compliance Assessment | compliance | 11 | 10 |
| STP-28-11-005 | Vent and Relief Sizing | sizing | 4 | 4 |

**Total:** 5 procedures composing 40 token references (12 unique MTK + 16 unique MTP).

---

## STP-28-11-001 — LH₂ Tank Sizing

**Class:** sizing | **Steps:** 7

Complete tank sizing from fuel mass requirement through geometry,
surface area, heat leak, boil-off rate, daily percentage, and
gravimetric efficiency.

### Inputs

| Parameter | Unit | Reference |
|-----------|------|-----------|
| stored_lh2_mass_kg | kg | Per cell requirement |
| lh2_density_kg_per_m3 | kg/m³ | 70.8 |
| lh2_latent_heat_kJ_per_kg | kJ/kg | 445.5 |
| system_heat_flux_W_per_m2 | W/m² | 1.3 |
| tank_mass_kg | kg | Structural estimate |
| system_mass_kg | kg | System estimate |

### Step Sequence

```
Step 1: MTP-28-11-GEOM-001  →  required_volume_m3
Step 2: MTP-28-11-GEOM-002  →  surface_area_m2 (sphere baseline)
Step 3: MTP-28-11-GEOM-003  →  adjusted_area_m2 (cylinder penalty)
Step 4: MTP-28-11-THRM-002  →  total_heat_leak_W
Step 5: MTP-28-11-THRM-001  →  boil_off_rate_kg_per_s
Step 6: MTP-28-11-THRM-003  →  boil_off_pct_per_day
Step 7: MTP-28-11-GEOM-004  →  gravimetric_efficiency
```

### Acceptance Gates

- `boil_off_pct_per_day ≤ 1.0%` (mission viability)
- `gravimetric_efficiency ≥ 0.50` (aircraft application threshold)

---

## STP-28-11-002 — Structural Substantiation

**Class:** structural | **Steps:** 6

Complete structural substantiation: stress analysis → weld derating →
ultimate factor → thermal contraction → cryogenic material anchor →
damage tolerance.

### Step Sequence

```
Step 1: MTP-28-11-MATL-002  →  hoop_stress_Pa
Step 2: MTP-28-11-MATL-004  →  weld_allowable_MPa
Step 3: MTP-28-11-CERT-001  →  ultimate_margin
Step 4: MTP-28-11-MATL-005  →  differential_contraction_mm
Step 5: MTP-28-11-MATL-001  →  cryogenic_allowables
Step 6: MTP-28-11-CERT-003  →  inspection_interval_cycles
```

### Acceptance Gates

- `ultimate_margin ≥ 1.0`
- `hoop_stress < weld_allowable`
- `inspection_interval meets ICA programme`

---

## STP-28-11-003 — Trade Evaluation

**Class:** evaluation | **Steps:** 5

Complete trade evaluation: execute three trade studies, score via
weighted-sum MCDA, and assess risks.

### Step Sequence

```
Step 1: MTK-28-11-TS-001   →  geometry_selection
Step 2: MTK-28-11-TS-002   →  material_selection
Step 3: MTK-28-11-TS-003   →  thermal_selection
Step 4: MTP-28-11-EVAL-001 →  total_weighted_scores
Step 5: MTP-28-11-EVAL-002 →  risk_levels
```

### Acceptance Gates

- `winning score > all alternatives`
- `no risk_level == 'unacceptable'`

---

## STP-28-11-004 — CS 25 Compliance Assessment

**Class:** compliance | **Steps:** 11

Full CS 25 compliance matrix evaluation: four regulatory sections
(§A–§D), five LH₂ special conditions, and ARP4761 safety assessment.

### Step Sequence

```
Step  1: MTK-28-11-CM-001  →  structural_compliance
Step  2: MTK-28-11-CM-002  →  pressure_compliance
Step  3: MTK-28-11-CM-003  →  ignition_compliance
Step  4: MTK-28-11-CM-004  →  materials_compliance
Step  5: MTP-28-11-CERT-002 → safety_assessment (FHA→PSSA→SSA)
Step  6: MTK-28-11-SC-001  →  SC boil-off management
Step  7: MTK-28-11-SC-002  →  SC hydrogen detection
Step  8: MTK-28-11-SC-003  →  SC cryogenic thermal shock
Step  9: MTK-28-11-SC-004  →  SC vacuum integrity
Step 10: MTK-28-11-SC-005  →  SC crashworthiness
Step 11: Aggregate          →  compliance_status
```

### Acceptance Gates

- `all compliance_status ≠ 'fail'`
- `cdccl_list complete`
- `all special conditions addressed`

---

## STP-28-11-005 — Vent and Relief Sizing

**Class:** sizing | **Steps:** 4

Vent/relief design from thermal environment to relief valve sizing
and dispatch verification.

### Step Sequence

```
Step 1: MTP-28-11-THRM-002 →  total_heat_leak_W
Step 2: MTP-28-11-THRM-001 →  max_boil_off_rate_kg_per_s
Step 3: MTP-28-11-CERT-004 →  vent_area_m2
Step 4: MTK-28-11-SC-001   →  dispatch_go_no_go
```

### Acceptance Gates

- `vent_area within packaging constraints`
- `dispatch_go_no_go == true for target turnaround`

---

## Traceability

| Relation | Artifacts |
|----------|-----------|
| Derives from | MTL-28-11-00, MTL-28-11-00-PROC |
| Feeds (LC05) | Parametric model pipelines — each STP = one model entry point |
| Feeds (LC06) | Verification test sequences — each STP = one test procedure |
| Feeds (LC08) | S1000D procedural data modules — each STP = one DM procedure |
