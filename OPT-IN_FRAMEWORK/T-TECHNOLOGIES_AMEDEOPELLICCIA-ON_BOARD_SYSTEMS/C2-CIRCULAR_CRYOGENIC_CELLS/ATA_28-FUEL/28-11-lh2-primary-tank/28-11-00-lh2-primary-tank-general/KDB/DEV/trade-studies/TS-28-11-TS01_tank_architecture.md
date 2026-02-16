# TS-28-11-TS01 — Tank Architecture: Spherical vs Cylindrical vs Conformal

| Key | Value |
|-----|-------|
| Trade Study ID | TS-28-11-TS01 |
| ATA Code | 28-11-00 |
| Technology Domain | C2 — Circular Cryogenic Cells |
| Aircraft Programme | AMPEL360 Q100 |
| Lifecycle Phase | LC04 (Design Definition) |
| Status | Preliminary |
| Author | STK_ENG |
| Date | 2026-02-16 |

## Objective

Determine optimal primary tank architecture for LH2 storage
within a circular cryogenic cell, comparing spherical,
cylindrical (hemispherical endcaps), and conformal/integral
geometries for mass, boil-off, certification risk, and
integration efficiency.

### Reference Assumptions

| Parameter | Value |
|-----------|-------|
| Stored LH₂ mass | 5 000 kg |
| LH₂ density | 70.8 kg/m³ |
| Required volume | 70.6 m³ |
| LH₂ bulk temperature | 20.3 K |
| Warm boundary temperature | 300 K |
| Reference heat flux | 1.3 W/m² |

---

## Options Considered

| Option | Name | Structural Efficiency | Thermal Behaviour | Integration | Certification Risk |
|--------|------|-----------------------|-------------------|-------------|--------------------|
| A | Spherical Non-Integral | Best | Optimal — minimum surface area | Packaging hardest | Moderate |
| B | Cylindrical with Hemispherical Endcaps | High | Very good (+11–32 % area vs sphere) | Best for modular cells | Low |
| C | Conformal / Integral | Low–Medium | Worst — highest area and thermal bridges | Best envelope usage | Highest |

### Option A — Spherical Non-Integral

- **Surface area:** ~83 m²
- **Boil-off:** 0.2–0.6 %/day
- **Gravimetric efficiency:** 0.50–0.80
- **Stress model:** Uniform membrane stress (best pressure vessel efficiency)
- **Heritage:** NASA cryogenic tank programmes
- **Mass efficiency:** HIGH
- **CG management:** Complex — spherical geometry constrains placement

### Option B — Cylindrical with Hemispherical Endcaps

- **Surface area penalty:** +11–32 % vs sphere
- **Boil-off:** 0.3–0.7 %/day
- **Gravimetric efficiency:** 0.50–0.75
- **Stress model:** Hoop stress in cylinder + membrane stress in endcaps
- **Heritage:** NASA, Airbus ZEROe concepts, conventional cryogenic industry
- **Mass efficiency:** HIGH
- **Manufacturing:** Scalable; well-understood weld qualification
- **Modular compatibility:** Natural fit for repeatable cell layout

### Option C — Conformal / Integral

- **Boil-off:** 1 to >5 %/day (unless active cooling)
- **Gravimetric efficiency:** 0.30–0.60
- **Stress model:** Complex load paths
- **Manufacturing:** Highest QA burden
- **Certification uncertainty:** Less mature crashworthiness and inspection narrative
- **Inspection access:** Difficult — structural integration complicates repairs

---

## Preliminary Selection

**Selected Option:** B — Cylindrical with Hemispherical Endcaps
**Baseline Name:** Cylindrical Hemispherical Non-Integral Tank

### Rationale

- Lowest overall certification risk for near-term implementation
- Scalable manufacturing with well-understood weld qualification
- Natural fit for modular circular cryogenic cell layout
- Leverages measured ~1.3 W/m² class system heat flux when thermal bridges are managed
- Compatible with 5D addressable tank states and deterministic modelling

---

## Feeds

| Lifecycle | Artifact |
|-----------|----------|
| LC03 | Safety FHA update (ATA 28-11 tank architecture) |
| LC05 | FEM comparative analysis (cylindrical vs spherical geometries) |
| LC05 | CG and packaging integration study |

## Traceability

- **Derives from:** TS-28-10-TS01
