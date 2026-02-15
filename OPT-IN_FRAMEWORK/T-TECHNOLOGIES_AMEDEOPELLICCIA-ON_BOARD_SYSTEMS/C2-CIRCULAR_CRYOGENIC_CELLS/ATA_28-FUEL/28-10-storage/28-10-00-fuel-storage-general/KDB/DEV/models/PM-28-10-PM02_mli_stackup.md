# PM-28-10-PM02 — MLI Thermal Stack-Up Model

| Key | Value |
|-----|-------|
| Model ID | PM-28-10-PM02 |
| ATA Code | 28-10-00 |
| Technology Domain | C2 — Circular Cryogenic Cells |
| Aircraft Programme | AMPEL360 Q100 |
| Lifecycle Phase | LC05 (Detail Design) |
| Status | Preliminary |
| Author | STK_ENG |
| Date | 2026-02-15 |

## Objective

Define the thermal stack-up model for vacuum-jacketed multi-layer
insulation on circular cryogenic cells.  The model predicts total heat
leak as a function of MLI layer count, layer density, vacuum level,
boundary temperatures, and integration losses (seams and penetrations)
to enable boil-off rate estimation and insulation sizing per the
selected baseline (TS-28-10-TS03, Option A).

---

## Design Parameters

| Symbol | Name | Unit | Range | Description |
|--------|------|------|-------|-------------|
| $N$ | Number of reflective shields | – | 20–100 | Aluminised Mylar or DAM layers |
| $N^*$ | Layer density | layers/cm | 5–20 | Optimal ≈ 8–12 layers/cm |
| $T_h$ | Warm boundary temperature | K | 235–320 | Vacuum jacket outer wall |
| $T_c$ | Cold boundary temperature | K | 20–25 | LH₂ tank wall (~20 K) |
| $P_{\mathrm{vac}}$ | Vacuum pressure | torr | 10⁻⁶–10⁻³ | Residual gas pressure |
| $A_{\mathrm{CCC}}$ | CCC external surface area | m² | 5–80 | Total insulated area per cell |
| $L_{\mathrm{seam}}$ | Total seam length | m | 0–50 | Cumulative blanket joint length |
| $n_{\mathrm{pen}}$ | Penetration count | – | 2–20 | Strut / feedthrough penetrations |

---

## Governing Equations

### Radiation (modified Lockheed MLI model)

$$
q_{\mathrm{rad}} = \frac{C_r\,\varepsilon_{\mathrm{eff}}\,(T_h^{4.67} - T_c^{4.67})}{N}
$$

### Solid conduction (Dacron spacer)

$$
q_{\mathrm{cond}} = \frac{C_s\,{N^*}^{2.63}\,(T_h - T_c)}{N}
$$

### Residual gas conduction (free-molecule regime)

$$
q_{\mathrm{gas}} = C_g\,P_{\mathrm{vac}}\,(T_h - T_c)
$$

### Total blanket heat flux

$$
q_{\mathrm{MLI}} = q_{\mathrm{rad}} + q_{\mathrm{cond}} + q_{\mathrm{gas}}
$$

### Integration losses

$$
\dot Q_{\mathrm{seam}} = k_{\mathrm{seam}} \cdot L_{\mathrm{seam}}
\quad (k_{\mathrm{seam}} \approx 0.169\;\text{W/m})
$$

$$
\dot Q_{\mathrm{pen}} = n_{\mathrm{pen}} \cdot q_{\mathrm{pen,avg}}
\quad (q_{\mathrm{pen,avg}} \approx 0.31\text{–}0.50\;\text{W})
$$

### Total cell heat leak

$$
\dot Q_{\mathrm{total}} = A_{\mathrm{CCC}}\,q_{\mathrm{MLI}} + \dot Q_{\mathrm{seam}} + \dot Q_{\mathrm{pen}}
$$

### Boil-off rate

$$
\dot m_{\mathrm{boil}} = \frac{\dot Q_{\mathrm{total}}}{h_{fg}}
\quad (h_{fg} \approx 447\;\text{kJ/kg for para-H}_2\text{ at 20 K})
$$

---

## Reference Cases

| Case | $T_h$ (K) | $T_c$ (K) | $P_{\mathrm{vac}}$ (torr) | Notes |
|------|-----------|-----------|---------------------------|-------|
| Ground hot-day | 320 | 20 | 10⁻⁵ | Worst-case boil-off |
| Cruise | 250 | 20 | 10⁻⁵ | Nominal operations |
| Degraded vacuum | 280 | 20 | 10⁻⁴ | Vacuum-loss sensitivity |

---

## Optimisation

**Minimise:** $\dot Q_{\mathrm{total}}$

**Subject to:**

- $N \le N_{\max}$ (envelope thickness limit)
- $N^* \in [8, 12]$ layers/cm (optimal density band)
- Boil-off rate $\le 0.1\;\%/\text{h}$ of stored mass under cruise
- Total MLI mass $\le m_{\mathrm{MLI,budget}}$

**Design variables:** $N$, $N^*$

---

## Outputs

| Output | Description |
|--------|-------------|
| Optimal layer count $N^*$ | Layer count at heat-leak knee (~55 ± 15 layers) |
| Heat flux vs $N$ curve | $q_{\mathrm{MLI}}(N)$ for each reference case |
| Boil-off rate map | $\dot m_{\mathrm{boil}}$ vs $N$ for each reference case |
| Seam / penetration budget | Max allowable seam length and penetration count |
| Vacuum sensitivity | $\dot Q_{\mathrm{total}}$ vs $P_{\mathrm{vac}}$ at nominal $N$ |

---

## Feeds

| Lifecycle | Artifact |
|-----------|----------|
| LC06 | Thermal vacuum qualification test plan |
| LC05 | Boil-off rate prediction for mission profile |

## Traceability

- **Derives from:** TS-28-10-TS03, FBL-Q100-ATA28-001, KNU-C2-001
- **Satisfies:** FBL-REQ-003
