# PM-28-10-PM01 — Tank Geometry: Circular Cross-Section Optimisation

| Key | Value |
|-----|-------|
| Model ID | PM-28-10-PM01 |
| ATA Code | 28-10-00 |
| Technology Domain | C2 — Circular Cryogenic Cells |
| Aircraft Programme | AMPEL360 Q100 |
| Lifecycle Phase | LC05 (Detail Design) |
| Status | Preliminary |
| Author | STK_ENG |
| Date | 2026-02-15 |

## Objective

Define the parametric model for circular cryogenic cell cross-section
optimisation.  The model captures geometry, structural sizing, and
volumetric efficiency as functions of internal radius, operating
pressure, wall thickness, and material properties in order to minimise
structural mass while meeting pressure containment and fatigue
requirements per CS 25.571.

---

## Design Parameters

| Symbol | Name | Unit | Range | Description |
|--------|------|------|-------|-------------|
| $r_i$ | Internal radius | m | 0.3–1.2 | Inner radius of the circular cylindrical shell |
| $t_w$ | Wall thickness | mm | 1.5–6.0 | Minimum wall driven by hoop stress and fatigue |
| $P_{\mathrm{design}}$ | Design pressure | bar | 2.0–6.0 | Max operating pressure incl. relief margin |
| $L$ | Cylinder length | m | 1.0–6.0 | Barrel length excluding end-caps |
| $\sigma_{\mathrm{allow}}$ | Allowable stress | MPa | 120–450 | Material allowable at −253 °C |
| $\rho_{\mathrm{mat}}$ | Material density | kg/m³ | 2700–8000 | Structural material density range |

---

## Governing Equations

### Hoop stress (thin-wall)

$$
\sigma_{\mathrm{hoop}} = \frac{P_{\mathrm{design}} \cdot r_i}{t_w}
\;\le\; \frac{\sigma_{\mathrm{allow}}}{\mathrm{SF}}
$$

SF = 1.5 (limit), 2.0 (ultimate) per CS 25.305.

### Minimum wall thickness

$$
t_{w,\min} = \frac{P_{\mathrm{design}} \cdot r_i \cdot \mathrm{SF}}{\sigma_{\mathrm{allow}}}
$$

### Shell mass (barrel + hemispherical end-caps)

$$
m_{\mathrm{barrel}} = 2\pi\, r_i\, t_w\, L\, \rho_{\mathrm{mat}}
$$

$$
m_{\mathrm{endcap}} = 2\pi\, r_i^2\, t_w\, \rho_{\mathrm{mat}}
$$

### Internal volume

$$
V_{\mathrm{int}} = \pi\, r_i^2\, L + \tfrac{4}{3}\pi\, r_i^3
$$

---

## Optimisation Formulation

**Minimise:** $m_{\mathrm{total}} = m_{\mathrm{barrel}} + m_{\mathrm{endcap}}$

**Subject to:**

- $\sigma_{\mathrm{hoop}} \le \sigma_{\mathrm{allow}} / \mathrm{SF}$
- $t_w \ge t_{w,\min}$
- $V_{\mathrm{int}} \ge V_{\mathrm{required}}$
- Fatigue life $\ge N_{\mathrm{cycles}}$ (CS 25.571 target)
- $r_i \le r_{\mathrm{envelope}}$ (BWB bay clearance)

**Design variables:** $r_i$, $L$, $t_w$

---

## Material Candidates

| ID | Material | $\sigma_{\mathrm{allow}}$ (cryo) | $\rho$ | Notes |
|----|----------|----------------------------------|--------|-------|
| MAT-A | Al 5083-H321 | 350 MPa | 2660 kg/m³ | Heritage cryogenic alloy |
| MAT-B | 316L Stainless Steel | 450 MPa | 8000 kg/m³ | Excellent cryogenic toughness |
| MAT-C | Al 2219-T87 | 340 MPa | 2840 kg/m³ | Shuttle ET heritage |

---

## Outputs

| Output | Description |
|--------|-------------|
| Optimal r/L ratio | Radius-to-length ratio that minimises mass for given volume |
| Wall thickness map | $t_w$ vs $P_{\mathrm{design}}$ for each material candidate |
| Mass sensitivity | $\partial m / \partial r_i$, $\partial m / \partial L$ partial derivatives |
| Fatigue margin | Cryogenic cycle count at design thickness vs CS 25.571 target |

---

## Feeds

| Lifecycle | Artifact |
|-----------|----------|
| LC06 | FEA verification of selected geometry |
| LC05 | Mass model update (WBS level 3) |

## Traceability

- **Derives from:** TS-28-10-TS01, FBL-Q100-ATA28-001
- **Satisfies:** FBL-REQ-001, FBL-REQ-010
