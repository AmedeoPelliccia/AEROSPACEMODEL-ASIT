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
| $t_w$ | Wall thickness | mm | 1.5–6.0 | Nominal wall thickness; equations use $t_{w,m}$ in meters |
| $t_{w,m}$ | Wall thickness (SI) | m | derived | $t_{w,m} = t_w \times 10^{-3}$ |
| $P_{\mathrm{limit}}$ | Limit pressure | bar | 2.0–6.0 | Design max operating pressure incl. margins |
| $P_{\mathrm{ultimate}}$ | Ultimate pressure | bar | derived | $1.5 \times P_{\mathrm{limit}}$ per CS 25.305 |
| $L$ | Cylinder length | m | 1.0–6.0 | Barrel length excluding end-caps |
| $\sigma_{\mathrm{allow,limit}}$ | Allowable stress (limit) | MPa | 120–450 | Material allowable at −253 °C, limit case |
| $\sigma_{\mathrm{allow,ult}}$ | Allowable stress (ultimate) | MPa | 120–450 | Material allowable at −253 °C, ultimate case |
| $\rho_{\mathrm{mat}}$ | Material density | kg/m³ | 2700–8000 | Structural material density range |
| $\eta_j$ | Joint efficiency | – | 0.6–1.0 | Weld / joint efficiency knockdown |

---

## Governing Equations

### Pressure convention (CS 25.305)

- $P_{\mathrm{limit}}$ = design max operating pressure including margins
- $P_{\mathrm{ultimate}} = 1.5\,P_{\mathrm{limit}}$
- Allowables defined separately for limit and ultimate checks
- Pressure conversion: $P\;[\mathrm{Pa}] = P\;[\mathrm{bar}] \times 10^5$
- Wall thickness conversion: $t_{w,m}\;[\mathrm{m}] = t_w\;[\mathrm{mm}] \times 10^{-3}$

All stress equations below use SI units (Pa, m).

### Thin-wall validity gate

$$
\frac{t_{w,m}}{r_i} \le 0.10
$$

If violated, switch to thick-wall (Lamé) model.

### Membrane stresses (thin-wall, closed ends)

$$
\sigma_{\theta} = \frac{P\,r_i}{t_{w,m}}
\qquad
\sigma_{z} = \frac{P\,r_i}{2\,t_{w,m}}
$$

### Von Mises equivalent stress

$$
\sigma_{\mathrm{vM}}
= \sqrt{\sigma_{\theta}^2 + \sigma_{z}^2 - \sigma_{\theta}\,\sigma_{z}}
= \frac{\sqrt{3}}{2}\,\frac{P\,r_i}{t_{w,m}}
$$

Constraints:

$$
\sigma_{\mathrm{vM}}(P_{\mathrm{limit}}) \le \sigma_{\mathrm{allow,limit}}
$$

$$
\sigma_{\mathrm{vM}}(P_{\mathrm{ultimate}}) \le \sigma_{\mathrm{allow,ult}}
$$

### Minimum wall thickness (von Mises, limit, with joint efficiency)

$$
t_{w,m,\min} = \frac{\sqrt{3}}{2}\,\frac{P_{\mathrm{limit}}\,r_i}{\eta_j\,\sigma_{\mathrm{allow,limit}}}
$$

Applied thickness:

$$
t_{w,m} \ge \max\!\big(t_{w,m,\min},\; t_{\mathrm{mfg}},\; t_{\mathrm{NDE}},\; t_{\mathrm{corr}}\big)
$$

### Shell mass (barrel + hemispherical end-caps)

$$
m_{\mathrm{barrel}} = 2\pi\, r_i\, t_{w,m}\, L\, \rho_{\mathrm{mat}}
$$

$$
m_{\mathrm{endcap}} = 4\pi\, r_i^2\, t_{w,m}\, \rho_{\mathrm{mat}}
$$

$$
m_{\mathrm{total}} = 2\pi\,\rho_{\mathrm{mat}}\,t_{w,m}\!\left(r_i\,L + 2\,r_i^2\right)
$$

### Internal volume

$$
V_{\mathrm{int}} = \pi\, r_i^2\, L + \tfrac{4}{3}\pi\, r_i^3
$$

### External surface area

$$
A_{\mathrm{ext}} = 2\pi\,r_i\,L + 4\pi\,r_i^2
$$

Relevant for thermal/MLI trade (links to PM-28-10-PM02 / KNU-C2-001).

### Thick-wall model (Lamé, if $t_{w,m}/r_i > 0.10$)

With $r_o = r_i + t_{w,m}$:

**Hoop stress at ID:**

$$
\sigma_{\theta,\mathrm{ID}} = P\,\frac{r_o^2 + r_i^2}{r_o^2 - r_i^2}
$$

**Radial stress at ID:**

$$
\sigma_{r,\mathrm{ID}} = -P
$$

**Von Mises at ID (Lamé):**

$$
\sigma_{\mathrm{vM,Lamé}} = \sqrt{\sigma_{\theta,\mathrm{ID}}^2 + \sigma_{r,\mathrm{ID}}^2 - \sigma_{\theta,\mathrm{ID}}\,\sigma_{r,\mathrm{ID}}}
$$

---

## Optimisation Formulation

**Minimise:**

$$
J = m_{\mathrm{total}}
+ \lambda_L\,\max(0,\,L - L_{\max})^2
+ \lambda_A\,(A_{\mathrm{ext}} - A_{\mathrm{target}})^2
$$

The area penalty connects directly to the KNU-C2-001 MLI layer optimisation
workstream (heat leak scales with $A_{\mathrm{ext}}$ and vacuum/MLI quality).

> **Note:** Under pure stress-limited thin-wall sizing ($t_w \propto P\,r_i/\sigma$),
> mass scales as $V/\pi + \tfrac{2}{3}r_i^3$, which is monotonic increasing in
> $r_i$.  The optimum therefore collapses to min-radius unless additional
> constraints (max length, max area, bay geometry, feed hardware clearance) are
> active.  Multi-objective formulation is required.

**Subject to:**

- $\sigma_{\mathrm{vM}}(P_{\mathrm{limit}}) \le \sigma_{\mathrm{allow,limit}}$
- $\sigma_{\mathrm{vM}}(P_{\mathrm{ultimate}}) \le \sigma_{\mathrm{allow,ult}}$
- $t_w / r_i \le 0.10$ (thin-wall validity; uses $t_{w,m}$)
- $t_{w,m} \ge \max(t_{w,m,\min},\,t_{\mathrm{mfg}},\,t_{\mathrm{NDE}},\,t_{\mathrm{corr}})$
- $V_{\mathrm{int}} \ge V_{\mathrm{required}}$
- Fatigue life $\ge N_{\mathrm{cycles}}$ (CS 25.571 pressure cycle spectrum)
- $r_i \le r_{\mathrm{envelope}}$ (BWB bay clearance)
- $L \le L_{\max}$ (bay length constraint)
- Leak-before-burst / fracture control at cryo (damage tolerance philosophy)
- $P_{\mathrm{proof}}$, $P_{\mathrm{burst}}$ margins tied to relief set points
- Buckling under external pressure (vacuum jacket outer shell)
- Thermal contraction mismatch at bi-material interfaces

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
| Pareto-derived r/L ratio | Ratio from multi-objective Pareto front under active constraints (not a unique analytic optimum) |
| Wall thickness map | $t_w$ vs $P_{\mathrm{limit}}$ for each material candidate |
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
