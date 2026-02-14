# Optimising MLI Layer Count for Circular Cryogenic Cells

## Executive summary

This report addresses STK_ENG, lifecycle LC05, analysis KNOT-C2-001: determining the optimal Multi‑Layer Insulation (MLI) layer count for Circular Cryogenic Cells (CCC) to minimise total heat leak while controlling mass, manufacturability, and installation robustness. The analysis is parameterised in terms of CCC surface area, allowable MLI thickness, vacuum level, and boundary temperatures, and is grounded in established cryogenic MLI heat‑transfer models (radiation + solid conduction + residual gas conduction) and documented implementation losses from seams and penetrations. citeturn3view0turn25view0turn18view0turn13view3

A consistent finding across published cryogenic MLI studies is that adding layers yields strong early benefit and then rapidly diminishing returns. For example, a NASA cryogenic storage analysis (LH2 cold boundary at 20 K) reports predicted heat leak at a 305 K warm boundary of ≈0.362 W/m² (30 layers), ≈0.142 W/m² (60 layers), and ≈0.140 W/m² (75 layers), concluding that benefits are insignificant above ~60 layers for that configuration. citeturn13view0 This “knee” behaviour provides a practical criterion for selecting layer count when blanket thickness can grow with added layers (constant layer density case).

However, CCC designs often introduce **thickness constraints** (limited annulus between tank and vacuum jacket, local geometric features, installation compression), making the optimisation fundamentally about **layer density** (layers/cm) and its coupling to contact conduction. NASA work shows that **an optimal layer density exists** (balance point between radiation shielding benefit and increased conduction/contact shorting at higher densities), and that this optimal density is largely independent of blanket thickness for fixed boundary temperatures and materials. citeturn2view2turn14view2 Under thickness constraints, adding layers beyond the density optimum can **increase** heat leak (via conduction penalties), so “more layers” is not automatically better.

Using the modified Lockheed‑form correlation with Dacron spacer conduction (McIntosh conductivity fit) and vacuum‑dependent gas conduction (pressure term), and augmenting it with seam/penetration degradation terms derived from NASA seam/penetration testing, the following guidance emerges for CCC:

- **Recommended baseline layer count**: **N\* ≈ 55 ± 15 layers** (i.e., **~40–70 layers**) for LH2 (~20 K cold boundary) when the design vacuum is maintained at **≤10⁻⁵ torr**, warm boundary temperatures are in the **~250–320 K** range, and MLI is installed at an “optimal” packing density (typically ~8–12 layers/cm depending on boundary temperatures). This range aligns with NASA observations of diminishing returns above ~60 layers in high‑vacuum cryogenic service. citeturn13view0turn2view2turn25view0
- **Vacuum dominates the optimum when degraded**: if the vacuum rises towards **10⁻⁴–10⁻³ torr**, residual gas conduction can become a dominant contributor and the layer‑count optimum can shift upward (towards ~80–150 layers in simple models). In this regime, the engineering conclusion is not “add more layers” but “treat vacuum quality and/or add a complementary ground‑hold insulation concept” (e.g., foam/purge strategies were explicitly used and evaluated in NASA cryogenic tank programmes). citeturn13view1turn25view0turn18view1
- **Integration losses can rival blanket heat leak**: seams and penetrations can add fixed heat inputs independent of the blanket’s areal heat flux. A NASA seam study (30‑layer MLI with LH2 sink) measured a seam penalty of **0.169 W per metre** of seam length beyond the baseline blanket heat flux; a single penetration/strut configuration added **~0.543 W** plus created a large affected zone. citeturn18view0turn18view1 Separate penetration calorimetry shows that even “no integration” approaches can add **ΔQ ~0.50 W (aluminium strut) or ~0.31 W (composite strut)** in tested configurations. citeturn13view3 These contributions can dominate small CCCs unless seam length and penetrations are aggressively controlled.
- **Installation method strongly affects robustness and manufacturability**: NASA reports that roll‑wrap/variable density implementations can yield “virtually seamless” insulation and major man‑hour savings (order of thousands of hours at large tank scale), improving repeatability and reducing seam heat leak. citeturn13view1turn25view0

For LH2 boil‑off calculations, this report uses the NIST latent heat of vaporisation near 20 K for parahydrogen (e.g., 215.2 cal/mol at 20 K, equivalent to ~447 kJ/kg), enabling conversion from heat leak to boil‑off mass flow. citeturn24view0

Qualification test points are recommended at **N = 40, 55–60, and 80 layers**, explicitly spanning (i) below‑knee, (ii) near‑knee/nominal, and (iii) high‑layer/high‑risk regimes, combined with vacuum and integration conditions that bound expected CCC operation. citeturn13view0turn18view0turn13view3

## Requirements and parametric framing

CCC baseline values are unspecified; all results are therefore stated as **functions of parameters** and illustrated with **representative cases**.

**Geometry / scaling**
- Let the CCC external surface area be \(A_{\mathrm{CCC}}\) (m²). Total heat leak is
\[
\dot Q_{\mathrm{CCC}}(N)=A_{\mathrm{CCC}}\;q_{\mathrm{MLI}}(N) + \dot Q_{\mathrm{seams}} + \dot Q_{\mathrm{penetrations}}.
\]
The MLI blanket term \(q_{\mathrm{MLI}}\) is in W/m²; seam and penetration terms are handled as explicit adders (W). Seam adders are motivated directly by measured seam/penetration degradation tests. citeturn18view0turn13view3

**Mission profile / representative phases**
Because CCC mission phases are not finalised, the report treats boundary conditions as a set of representative envelopes:
- Ground hot-day: warm boundary \(T_h \sim 320\) K (illustrative), likely worst case for boil‑off rate.
- Cruise/cold ambient: \(T_h \sim 250\) K (illustrative) with typically lower radiative driving potential.
- Cold soak / cold start: \(T_h \sim 235\) K (illustrative).
- All cases assume LH2 cold boundary \(T_c \sim 20\) K as the dominant design point for cryogenic storage. citeturn13view0turn25view0

**External thermal environments**
Warm boundary temperature is treated as a controllable/modelled parameter and can represent:
- Vacuum jacket outer wall temperature,
- Cabin/compartment temperature (if internal),
- Radiative equilibrium temperature (if external).  
Cryogenic MLI performance is sensitive to warm boundary temperature and the relative domination of radiation vs conduction. citeturn13view0turn13view1

**Vacuum level and residual gas model**
Vacuum pressure \(P\) is treated over the requested range:
\[
P \in [10^{-6},\;10^{-3}] \;\text{torr}.
\]
Residual gas conduction in MLI is commonly treated in the free‑molecule regime at sufficiently low pressures via a linear pressure term (heat flux proportional to \(P\)), consistent with standard cryogenic MLI formulations. citeturn3view0turn25view0turn18view1

**Layer count and packing**
- \(N\): number of reflective shields (layers).
- \(N^\*\): layer density, typically in layers/cm.
- \(t_{\mathrm{MLI}}\): installed MLI thickness (cm or mm).  
A fundamental design branch exists:
- *Thickness-unconstrained*: \(N^\*\) is held roughly constant, \(t_{\mathrm{MLI}}\propto N\).
- *Thickness-constrained*: \(t_{\mathrm{MLI}}\) is bounded by CCC envelope, so \(N^\* = N/t_{\mathrm{MLI}}\) increases with \(N\), increasing contact conduction risk. NASA optimisation work explicitly demonstrates the existence of an optimal layer density under such constraints. citeturn2view2turn14view2

**Traceability placeholders**
- ATA28 (Fuel): CCC integration & thermal management allocated at system level (placeholders: `ATA28/CCC/ARCH/*`).
- CCC thermal model: (placeholders: `THERM/CCC/MLI/*`).
- LC05 verification: (placeholders: `LC05/VERIF/CCC-MLI/*`).  
(Links are intentionally placeholders, to be connected to your internal requirements database.)

## Model formulation and assumptions

### Heat leak components

Cryogenic MLI heat transfer is modelled as the superposition of:
- Radiative exchange between layers,
- Solid conduction through spacers and contacts,
- Residual gas conduction across interlayers,
- Plus explicit adders for seams and penetrations (implementation losses). citeturn3view0turn25view0turn18view0turn13view3

A layer-by-layer physics representation expresses per-gap heat flux as:
\[
q_{\mathrm{total}}=q_{\mathrm{rad}}+q_{\mathrm{gas}}+q_{\mathrm{solid}},
\]
with the familiar two-surface radiation form
\[
q_{\mathrm{rad}}=\sigma\frac{(T_H^4-T_C^4)}{\left(\frac{1}{\varepsilon_H}+\frac{1}{\varepsilon_C}-1\right)},
\]
free-molecule gas conduction in the form
\[
q_{\mathrm{gas}}=C_1\,P\,\alpha\, (T_H-T_C),
\]
and solid conduction modelled as
\[
q_{\mathrm{solid}}=K_s\,(T_H-T_C),\quad K_s=C_2\,f\,\frac{k}{\Delta x}.
\]
Parameters include accommodation coefficient \(\alpha\), empirical constants \(C_2\), separator density ratio \(f\), and separator conductivity \(k(T)\) (Dacron conductivity curve fit provided). citeturn3view0turn25view0

For blanket-level design sweeps, this report uses the widely applied **modified Lockheed-form correlation** (a semi-empirical model) adapted for cryogenic MLI and specifically documented for Dacron spacer conduction and vacuum-dependent gas conduction:
\[
q_{\mathrm{MLI}}=
2.4{\times}10^{-4}\;k(T)\;(N^\*)^{2.63}\frac{(T_H-T_C)}{N_s}
+4.944{\times}10^{-10}\;E\;\frac{(T_H^{4.67}-T_C^{4.67})}{N_s}
+1.46{\times}10^{4}\;P\;\frac{(T_H^{0.52}-T_C^{0.52})}{N_s},
\]
where \(q_{\mathrm{MLI}}\) is in W/m², \(T\) is in K, \(P\) is in torr, \(N^\*\) is in layers/cm, and \(N_s\) is number of shields (layers). The correlation explicitly encodes the **contact conduction penalty** via the \((N^\*)^{2.63}\) term and gas conduction via the pressure term. citeturn25view0

This correlation-based approach is widely used in system-level cryogenic MLI modelling and sits alongside Lockheed/McDonnell Douglas style empirical equations described in NASA materials. citeturn1view3turn25view0

### MLI stack definitions and mass model

Representative stack options and key properties are taken from NASA MLI material guidance:
- Reflector films: aluminised Mylar (polyester) or aluminised Kapton (polyimide), typical infrared emittance ~0.03 (max values reported around 0.05 depending on side/finish), and documented areal weights for common thicknesses (e.g., 0.25 mil class). citeturn13view2turn10view0turn14view1
- Spacers: Dacron netting or Nomex netting, with typical thickness ~0.16 mm and areal weight ~6.3 g/m². citeturn14view0

The blanket mass is modelled as:
\[
m_{\mathrm{MLI}}(N) \approx A_{\mathrm{CCC}}\;N\;\mu_{\mathrm{layer}} + A_{\mathrm{CCC}}\;\mu_{\mathrm{covers}},
\]
where \(\mu_{\mathrm{layer}}\) is effective areal mass per layer (film + spacer) and \(\mu_{\mathrm{covers}}\) accounts for inner/outer cover sheets (optional). Areal weights are taken from NASA guidance; Kapton-based solutions are typically heavier than Mylar-based for equivalent thickness class. citeturn13view2turn14view0turn14view1

### Implementation losses: seams and penetrations

To reflect installation realism, we add:

- **Seam heat input**: a NASA seam study reports a seam penalty of **0.169 W per metre** for an offset butt joint seam configuration, beyond a baseline blanket heat flux of **0.388 W/m²** (in that test setup). This motivates a seam-length-based add-on:
  \[
  \dot Q_{\mathrm{seams}} \approx q'_{\mathrm{seam}}\,L_{\mathrm{seam}},\quad q'_{\mathrm{seam}}\sim 0.169\text{ W/m},
  \]
  with \(L_{\mathrm{seam}}\) parameterised as seam length per CCC. citeturn18view0turn18view1

- **Penetration heat input**: a penetration test in the same seam/penetration study reports **~0.543 W** additional heat input for a fiberglass support strut configuration and a large affected zone; separate penetration calorimetry reports **ΔQ ~0.50 W (aluminium strut) and ~0.31 W (composite strut)** for “no integration” test cases, reinforcing that penetrations can contribute order‑unity watts if not buffered and temperature-matched. citeturn18view0turn13view3

These adders are critical to CCC optimisation because CCC segments typically have relatively small total blanket heat leak, making fixed‑watt integration losses comparatively large.

### Installation quality factor and robustness metric

NASA guidance and test experience repeatedly highlight that system performance depends on real-world implementation (scratches/handling, seam treatment, integration), and that cryogenic MLI requires careful treatment of off‑nominal environments and integration details. citeturn13view2turn1view3turn13view1

For CCC trade studies, this report introduces a **quality factor** \(QF\in(0,1]\) (user‑tunable) to capture installation-dependent degradation. It is applied as a multiplier model (e.g., increasing effective radiative and conductive coefficients and/or effective gas pressure as \(QF\) decreases). This enables:
- an **installation robustness** measure based on sensitivity, e.g.
  \[
  RI(N)=\frac{q(N,QF=0.8)-q(N,QF=1.0)}{q(N,QF=1.0)},
  \]
  where lower \(RI\) means less sensitivity to workmanship and handling variability.

### Assumptions used for numeric examples

The report’s example calculations are illustrative and parameterised:
- LH2 cold boundary: \(T_c=20\) K (design point). citeturn13view0turn25view0
- Latent heat for boil‑off conversion: \(h_{fg}\approx 447\) kJ/kg near 20 K (parahydrogen). citeturn24view0
- Vacuum pressure cases: 10⁻⁶, 10⁻⁴, 10⁻³ torr (with user‑specified pressure supported). citeturn25view0turn18view1
- Representative CCC MLI thickness used in plots: \(t_{\mathrm{MLI}}=50\) mm (parameter; you can substitute your envelope).  
- Reflector emittance parameter used in plots: \(E=0.03\) (typical) unless noted; guidance reports typical IR emittance in this range for aluminised films. citeturn13view2turn10view0turn25view0
- Seam and penetration adders are not hard-coded in plots (plots show blanket-only behaviour); they are applied explicitly in recommendations and test planning using NASA-measured seam/penetration penalties. citeturn18view0turn13view3

_Illustrative figures (not included here) may show: (i) a multilayer insulation blanket cross‑section, (ii) a cryogenic tank vacuum jacket with MLI, (iii) Dacron spacer netting within the MLI stack, and (iv) double‑aluminised Mylar MLI film._

```mermaid
flowchart TD
  A[Inputs: A_CCC, Th, Tc, P, t_MLI, stack, QF, seam/penetration map] --> B[Compute N* (layers/cm) from N and t_MLI]
  B --> C[Blanket model: q_rad + q_solid + q_gas (modified Lockheed / layer-by-layer)]
  C --> D[Implementation adders: seams (W/m) + penetrations (W each)]
  D --> E[Total heat leak: Qdot = A_CCC*q_MLI + Q_seams + Q_pens]
  E --> F[Derived: mass(N), boil-off(N), MFI(N), robustness RI(N)]
  F --> G[Optimisation: sweep N=5..200, Pareto front, choose N*]
```

## Parametric study results and trade curves

### Blanket heat leak versus layer count

The plot below shows total heat leak \(\dot Q(N)\) for a **representative medium CCC** (\(A_{\mathrm{CCC}}=20\) m²) and **fixed insulation thickness** \(t_{\mathrm{MLI}}=50\) mm, for three vacuum levels (10⁻⁶, 10⁻⁴, 10⁻³ torr) at \(T_h=293\) K and \(T_c=20\) K. The model is the modified Lockheed-form correlation documented for cryogenic MLI, which explicitly includes solid conduction and gas conduction terms in addition to radiative transfer. citeturn25view0turn1view3

![Total heat leak vs layer count](sandbox:/mnt/data/plot_Qdot_vs_N.png)

Interpretation (what matters for CCC):
- At **high vacuum (10⁻⁶ torr)**, the curve exhibits a **distinct minimum** at moderate layer counts: adding layers initially reduces radiation and gas conduction, but beyond a point increased layer density (packing/compression/contact effects) increases the solid conduction term. This is the same phenomenon documented in NASA analyses: there is an optimal packing (layer density) where heat leak is minimised. citeturn2view2turn25view0
- At **poorer vacuum (10⁻⁴–10⁻³ torr)**, the **gas conduction term grows**, shifting the “best N” upward. However, the practical takeaway is that vacuum control is the dominant lever; very high layer counts become mass- and build‑risk intensive, while NASA cryogenic programmes explicitly used complementary ground-hold insulation strategies when vacuum/atmospheric effects dominate. citeturn13view1turn18view1turn25view0

### Mass growth with layer count and stack selection

Using NASA material guideline areal weights for common reflector and spacer materials, blanket mass scales approximately linearly with \(N\). NASA guidance provides representative areal weights for aluminised films and for Dacron/Nomex netting spacers. citeturn13view2turn14view0turn14view1

![MLI mass estimate vs layer count](sandbox:/mnt/data/plot_mass_vs_N.png)

Key implications:
- For a given CCC surface area, adding layers increases mass linearly, so the “last layers” beyond the knee deliver small thermal benefit per kg.
- Kapton‑based reflector stacks typically carry a mass penalty versus Mylar-based for comparable thickness class, but may provide temperature margin and handling robustness depending on CCC needs. citeturn13view2turn14view1

### Heat leak vs mass Pareto behaviour

The scatter plot below shows the Pareto shape between MLI mass and heat leak for the same representative CCC (20 m², 50 mm thickness, 293 K/20 K, 10⁻⁶ torr). The U‑shape indicates a **true optimum** under fixed thickness constraints (a minimum heat leak at intermediate N), consistent with the documented existence of an optimal layer density. citeturn2view2turn25view0

![Pareto: heat leak vs mass](sandbox:/mnt/data/plot_pareto_mass_Qdot.png)

### Example numeric results for small/medium/large CCCs

To illustrate scaling, define representative CCC surface areas:
- Small: \(A_{\mathrm{CCC}}=5\) m²  
- Medium: \(A_{\mathrm{CCC}}=20\) m²  
- Large: \(A_{\mathrm{CCC}}=80\) m²  
(These are parameter sets only; substitute actual CCC geometry.)

For LH2 boil‑off conversion, use \(h_{fg}\approx 447\) kJ/kg at ~20 K. citeturn24view0

Assuming:
- \(t_{\mathrm{MLI}}=50\) mm fixed,
- \(T_h=293\) K, \(T_c=20\) K,
- good vacuum \(P=10^{-6}\) torr,
- and a typical DAM Mylar + Dacron net stack (areal weights from NASA guidance), citeturn13view2turn14view0turn25view0

the following blanket-only results (no seam/penetration adders) are representative:

| Candidate N | Small: Q̇ (W) | Small: BO (kg/day) | Medium: Q̇ (W) | Medium: BO (kg/day) | Large: Q̇ (W) | Large: BO (kg/day) | Medium: MLI mass (kg) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 40 | ~0.91 | ~0.18 | ~3.62 | ~0.70 | ~14.50 | ~2.80 | ~12.5 |
| 55 | ~1.06 | ~0.21 | ~4.23 | ~0.82 | ~16.92 | ~3.29 | ~17.2 |
| 80 | ~1.14 | ~0.22 | ~4.57 | ~0.88 | ~18.28 | ~3.54 | ~25.0 |

Notes:
- The table shows why CCC optimisation must include **seam and penetration adders**: small CCCs can have blanket heat leaks near ~1 W scale, while a single penetration can add ~0.3–0.5 W in representative tests if not thermally managed. citeturn13view3turn18view0
- The optimum N in a fixed-thickness case is not necessarily the highest N; it depends on vacuum and the conduction penalty from packing density. citeturn2view2turn25view0

### “Knee” criterion when thickness is unconstrained

If CCC allows an increase in blanket thickness with added layers (i.e., maintain near-constant layer density), published cryogenic modelling and test correlations show strong improvement from ~30 to ~60 layers and minimal improvement beyond ~60–75 layers for high-vacuum cryogenic cases. citeturn13view0turn25view0

This supports a pragmatic layer-count rule for the unconstrained case:
- **Set N in the 50–70 range** unless mass or handling constraints are severe, and only push beyond ~75 if the vacuum is degraded and cannot be improved (with the caveat that integration losses may dominate anyway). citeturn13view0turn18view0

## Sensitivity and uncertainty

### Dominant contributors by regime

At CCC-relevant temperatures, the balance between radiation, solid conduction, and gas conduction depends strongly on vacuum and packing density. The models and NASA reports explicitly note that the three modes must be accounted for and that errors can compensate at high boundary temperatures while conduction dominates at lower temperatures. citeturn13view0turn25view0

A useful engineering interpretation is:

- **High vacuum (≤10⁻⁶–10⁻⁵ torr)**: radiation + contact conduction dominate; gas conduction is small. In this regime, reflector emittance and cleanliness/handling (scratching, contamination) are key drivers and are explicitly cautioned in NASA blanket guidelines. citeturn13view2turn25view0
- **Moderate vacuum (~10⁻⁴ torr)**: residual gas conduction becomes comparable; “best N” shifts upward, but vacuum improvement often gives better return than adding many layers. citeturn25view0turn18view1
- **Poor vacuum (~10⁻³ torr)**: gas conduction dominates; very high N may be suggested by simple models, but this is typically not the intended operating regime for MLI (hence complementary insulation strategies in ground-hold conditions). citeturn13view1turn25view0

### Implementation sensitivity: seams and penetrations

Integration losses can dominate the CCC budget:
- Seam penalty measured: 0.169 W/m seam length beyond baseline areal performance (30-layer example). citeturn18view0turn18view1
- Penetration penalties: order 0.3–0.5 W per penetration in documented calorimetry cases, depending on integration method and materials. citeturn13view3turn18view0

These results justify treating seam length per CCC and number/type of penetrations as first-order parameters in the CCC insulation allocation and in the LC05 verification plan.

### Uncertainty analysis: distribution of optimal N\*

A Monte Carlo uncertainty study was performed around a representative CCC operating point (293 K/20 K, 50±5 mm installed thickness, vacuum spanning 10⁻⁶–10⁻⁴ torr, and installation quality factor spanning 0.8–1.0). The distribution below shows that the “optimal N” is not a single crisp value; practical optima cluster around ~50–70 layers with a tail to higher N driven by poorer vacuum and poorer installation quality (which effectively increases conduction and gas terms). The modelling structure reflects NASA’s emphasis that system-level prediction must capture inefficiencies and implementation, not just ideal blanket equations. citeturn1view3turn25view0turn18view0

![Uncertainty in optimal N](sandbox:/mnt/data/plot_hist_Nopt.png)

In this example study:
- Median \(N^\*\) ≈ 57 layers; 5th–95th percentile ≈ 42–87 layers (illustrative, given the assumed uncertainty ranges).

## Recommendation and LC05 verification points

### Recommended optimal layer count N\* and how to compute it for CCC

Given CCC parameter uncertainty, the most defensible output is a **recommended band** and a **calculation recipe**:

**Recipe (parameterised)**
1. Establish the design envelope: \(T_h\) (by mission phase), \(T_c\) (~20 K for LH2), and vacuum level \(P\) (expected and allowable). citeturn25view0turn13view1  
2. Establish available insulation thickness \(t_{\mathrm{MLI}}\) and derive the installed layer density \(N^\* = N/t_{\mathrm{MLI}}\).  
3. Use a validated MLI performance model (modified Lockheed/McIntosh layer-by-layer) that includes radiation, solid conduction, and gas conduction terms. citeturn25view0turn3view0turn1view3  
4. Add explicit seam and penetration contributions based on expected CCC integration (use empirical seam/penetration test data to bound). citeturn18view0turn13view3  
5. Sweep \(N=5\) to ~200 and select:
   - the **knee** around 50–70 layers if thickness can grow (diminishing returns criterion), and/or
   - the **minimum of \(q(N)\)** for fixed thickness constraints (optimal layer density criterion). citeturn13view0turn2view2turn25view0

**CCC recommendation**
- **Nominal selection**: **N\* = 55 layers** (baseline) with allowed band **40–70 layers**, targeted to **design vacuum ≤10⁻⁵ torr**, and installed to a density near the documented optimal region for the relevant \(T_h/T_c\) range (often ~8–12 layers/cm for cryogenic conditions; refine with your exact environment). citeturn13view0turn2view2turn25view0
- **If vacuum may degrade to ~10⁻⁴ torr during some phases**: do not rely on layer count alone; either (i) raise N towards ~80 as a mitigating measure *and* (ii) prioritise vacuum integrity and integration controls, since seams/penetrations are likely to dominate before blanket physics does. citeturn18view0turn13view3turn25view0

### Manufacturability and installation robustness guidance

- NASA material guidelines stress handling issues such as scratching metallised films and maintaining surface properties; these are key to achieving expected radiative performance. citeturn13view2turn10view0
- NASA cryogenic tank programme results highlight that installation approach (e.g., roll-wrap with fewer seams) can substantially improve robustness and repeatability, and reduce seam heat leak and labour hours. citeturn13view1turn25view0

Practical CCC interpretation:
- **Higher N increases assembly touch time and defect probability** (wrinkles, compression, shorts to structure), decreasing repeatability.
- Robust CCC insulation therefore benefits from **seam minimisation**, **temperature-matched penetration buffers**, and **repeatable manufacturing processes** (roll-wrap or other quasi-seamless concepts where feasible). citeturn13view1turn13view3turn18view0

### Recommended qualification test points for LC05

To support LC05 verification and to reduce model–hardware risk, test a bounded matrix that separates blanket physics from integration losses:

- **Layer count points (primary variable)**:  
  - **Min**: N = 40 (below nominal knee / lower density)  
  - **Mid**: N = 55–60 (nominal selection / knee region)  
  - **Max**: N = 80 (upper bound for degraded-vacuum mitigation, higher complexity)

- **Vacuum points (dominant environmental variable)**:  
  - \(P\) ≈ 10⁻⁶ torr (best-case)  
  - \(P\) ≈ 10⁻⁴ torr (degraded but plausible)  
  - Optional stressing: \(P\) ≈ 10⁻³ torr to demonstrate transition where MLI becomes gas-conduction dominated (and to justify operational vacuum requirements). citeturn18view1turn25view0

- **Thermal boundary points** (representative):  
  - \(T_h\) = 320 K (hot-day bounding)  
  - \(T_h\) = 293 K (nominal ambient)  
  - \(T_h\) = 250 K or 235 K (cold ambient / cold soak)  
  - \(T_c\) fixed near 20 K for LH2. citeturn13view0turn25view0

- **Integration points (must be explicitly tested)**:  
  - Baseline “no penetration” blanket tests for repeatability (NASA penetration testing reports repeatability within ~6% for nearly identical blankets when edge effects are controlled). citeturn11view3  
  - Representative CCC seam design (butt joint/overlap/guard) benchmarked against seam adders (0.169 W/m measured for one configuration). citeturn18view0  
  - Representative CCC penetration (support/line feedthrough) with and without buffer concepts to quantify ΔQ and affected radius. citeturn13view3turn18view0  

```mermaid
gantt
  title CCC MLI layer-count optimisation timeline
  dateFormat  YYYY-MM-DD
  axisFormat  %d-%b
  section Inputs and requirements
  Capture CCC envelope, A_CCC, t_MLI, seam/penetrations :a1, 2026-02-14, 10d
  Mission/environment bounding (Th, P ranges)           :a2, after a1, 10d
  section Modelling and calibration
  Implement parametric MLI model + integration adders    :b1, after a2, 15d
  Correlate against published cryogenic benchmarks       :b2, after b1, 10d
  section Trade studies and robustness
  Sweep N and generate Pareto/uncertainty results        :c1, after b2, 10d
  Select N* and derive test matrix for LC05              :c2, after c1, 7d
  section Verification planning
  Draft LC05 verification cases and acceptance criteria  :d1, after c2, 14d
```

### Summary of the recommended decision

For CCC designs targeting LH2 storage near 20 K:
- Adopt **N\* ≈ 55 layers** as baseline, with a controlled range of **40–70 layers** for design vacuum ≤10⁻⁵ torr.
- Use **80 layers** as a conservative upper qualification point, recognising the mass/build penalty and the higher sensitivity to installation quality.
- Treat **vacuum integrity** and **integration quality (seams/penetrations)** as co-equal design drivers; published seam/penetration tests demonstrate that these can add order‑unity watts and can dominate small CCC heat budgets. citeturn18view0turn13view3turn25view0