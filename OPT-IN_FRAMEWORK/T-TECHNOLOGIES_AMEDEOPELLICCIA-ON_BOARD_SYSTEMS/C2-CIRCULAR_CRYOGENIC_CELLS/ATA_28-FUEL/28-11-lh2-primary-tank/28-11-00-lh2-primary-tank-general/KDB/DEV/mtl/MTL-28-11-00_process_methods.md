# MTL-28-11-00-PROC — Process and Scaling Method Tokens

**ATA 28-11-00 LH₂ Primary Tank General**

| Key | Value |
|-----|-------|
| MTL ID | MTL-28-11-00-PROC |
| ATA Code | 28-11-00 |
| Technology Domain | C2 — Circular Cryogenic Cells |
| Aircraft Programme | AMPEL360 Q100 |
| Lifecycle Phase | LC04 (Design Definition) |
| Status | Preliminary |
| Token Pattern | `MTP-28-11-{DOMAIN}-{SEQ}` |
| Total Tokens | 21 (13 process + 8 scaling) |

## Purpose

Extracts every standard industry process, analytical method, and
empirical scaling relationship from the 28-11-00 YAML artifacts.

- **Process** tokens encode closed-form methods with a known inference
  boundary (e.g., `V = m/ρ`, `σ = Pr/t`, `ṁ = Q̇/h_fg`).
- **Scaling** tokens encode empirical correlations or range-based
  relationships where no single closed-form inference boundary exists
  (e.g., MLI vacuum sensitivity, weld derating, gravimetric efficiency).

Companion to `MTL-28-11-00_method_token_library.yaml` which captures
subject-level tokens.  This file captures the *methods themselves*.

---

## Token Inventory

### Domain: GEOM — Geometry and Sizing (4 tokens)

| Token | Subject | Type | Method |
|-------|---------|------|--------|
| MTP-28-11-GEOM-001 | LH2 Volume Sizing | process | `V = m_fuel / rho_lh2` |
| MTP-28-11-GEOM-002 | Sphere Surface Area | process | `A = (36πV²)^(1/3)` |
| MTP-28-11-GEOM-003 | Cylinder Area Penalty Scaling | scaling | `A_cyl/A_sphere ≈ 1.11–1.32` |
| MTP-28-11-GEOM-004 | Gravimetric Efficiency | scaling | `η_g = m_f/(m_f+m_t+m_s)` range 0.3–0.9 |

#### MTP-28-11-GEOM-001 — LH2 Volume Sizing

- **Type:** Process (closed-form)
- **Method:** `V = m_fuel / rho_lh2`
- **Inputs:** `stored_lh2_mass_kg` (5000 kg), `lh2_density_kg_per_m3` (70.8)
- **Outputs:** `required_volume_m3` (70.6 m³)

#### MTP-28-11-GEOM-002 — Sphere Surface Area

- **Type:** Process (closed-form)
- **Method:** `A_sphere = (36 × π × V²)^(1/3)`
- **Inputs:** `required_volume_m3` (70.6)
- **Outputs:** `surface_area_m2` (83 m²)

#### MTP-28-11-GEOM-003 — Cylinder Area Penalty Scaling

- **Type:** Scaling (no single closed-form; aspect-ratio dependent)
- **Method:** `A_cyl / A_sphere ≈ 1.11 to 1.32`
- **Inputs:** `aspect_ratio_L_over_D` (range 1.5–4.0)
- **Outputs:** `area_penalty_factor` (range 1.11–1.32)

#### MTP-28-11-GEOM-004 — Gravimetric Efficiency

- **Type:** Scaling (empirical range)
- **Method:** `η_g = m_f / (m_f + m_t + m_s)`
- **Outputs:** range 0.30–0.90 (published aircraft LH₂ tanks)

---

### Domain: THRM — Thermal and Boil-Off (6 tokens)

| Token | Subject | Type | Method |
|-------|---------|------|--------|
| MTP-28-11-THRM-001 | Steady-State Boil-Off Rate | process | `ṁ_bo = Q̇ / h_fg` |
| MTP-28-11-THRM-002 | Total Heat Leak from Surface Flux | process | `Q̇ = q̇ × A` |
| MTP-28-11-THRM-003 | Daily Boil-Off Percentage | process | `bo%/day = (ṁ×86400/m)×100` |
| MTP-28-11-THRM-004 | MLI Vacuum Degradation Scaling | scaling | `q_mli = f(P_vacuum)` |
| MTP-28-11-THRM-005 | System Heat Flux Measured Anchor | scaling | `q ≈ 1.26–1.36 W/m²` |
| MTP-28-11-THRM-006 | Thermal Bridge Dominance | scaling | `Q_bridges ≥ Q_mli_broadarea` |

#### MTP-28-11-THRM-001 — Steady-State Boil-Off Rate

- **Type:** Process (closed-form)
- **Method:** `ṁ_bo = Q̇ / h_fg`
- **Inputs:** `total_heat_leak_W`, `lh2_latent_heat_kJ_per_kg` (445.5)
- **Outputs:** `boil_off_rate_kg_per_s`
- Industry-standard first-order cryogenic boil-off estimate.

#### MTP-28-11-THRM-002 — Total Heat Leak from Surface Flux

- **Type:** Process (closed-form)
- **Method:** `Q̇ = q̇ × A_wetted`
- **Inputs:** `heat_flux_W_per_m2` (1.3), `surface_area_m2`
- **Outputs:** `total_heat_leak_W`

#### MTP-28-11-THRM-003 — Daily Boil-Off Percentage

- **Type:** Process (closed-form)
- **Method:** `bo%/day = (ṁ_bo × 86400 / m_fuel) × 100`

#### MTP-28-11-THRM-004 — MLI Vacuum Degradation Scaling

- **Type:** Scaling (empirical nonlinear)
- **Inputs:** `vacuum_pressure_Pa` (0.0133–1.33 Pa)
- Slight degradation from ~0.266 Pa to ~1.33 Pa materially erodes MLI advantage.

#### MTP-28-11-THRM-005 — System Heat Flux Measured Anchor

- **Type:** Scaling (measured range from NASA IRAS)
- **Outputs:** `system_heat_flux_W_per_m2` (1.26–1.36 W/m²)
- Includes real penetration and support losses.

#### MTP-28-11-THRM-006 — Thermal Bridge Dominance

- **Type:** Scaling (empirical finding)
- Support-pad and man-way conduction can be comparable to or exceed MLI broad-area contribution.

---

### Domain: MATL — Materials and Structural (5 tokens)

| Token | Subject | Type | Method |
|-------|---------|------|--------|
| MTP-28-11-MATL-001 | Cryogenic Strength Increase (Al-Li) | scaling | σ\_y(20K) = 724 MPa |
| MTP-28-11-MATL-002 | Pressure Vessel Hoop Stress | process | `σ = Pr/t` |
| MTP-28-11-MATL-003 | Membrane Stress (Sphere) | process | `σ = Pr/2t` |
| MTP-28-11-MATL-004 | Weld Strength Derating | scaling | `k_weld ≈ 0.6–0.9` |
| MTP-28-11-MATL-005 | Thermal Contraction Mismatch | process | `ΔL = α × L × ΔT` |

#### MTP-28-11-MATL-002 — Pressure Vessel Hoop Stress

- **Type:** Process (closed-form — Barlow's formula)
- **Method:** `σ_hoop = P × r / t`

#### MTP-28-11-MATL-003 — Membrane Stress (Sphere)

- **Type:** Process (closed-form)
- **Method:** `σ_membrane = P × r / (2t)` — half the hoop stress of a cylinder.

#### MTP-28-11-MATL-005 — Thermal Contraction Mismatch

- **Type:** Process (closed-form)
- **Method:** `ΔL = α × L × ΔT`
- Reference ΔT ≈ 280 K (inner tank 20 K, jacket 300 K).

---

### Domain: CERT — Certification and Safety (4 tokens)

| Token | Subject | Type | Method |
|-------|---------|------|--------|
| MTP-28-11-CERT-001 | Ultimate Pressure Factor | process | `P_ult = 1.5 × P_limit` |
| MTP-28-11-CERT-002 | ARP4761 Safety Assessment | process | FHA → PSSA → SSA |
| MTP-28-11-CERT-003 | CS 25.571 Damage Tolerance | process | `a₀ → da/dN → a_crit → inspection` |
| MTP-28-11-CERT-004 | Vent Relief Sizing | process | `A = ṁ / (C_d × √(2ρΔP))` |

---

### Domain: EVAL — Evaluation and Scoring (2 tokens)

| Token | Subject | Type | Method |
|-------|---------|------|--------|
| MTP-28-11-EVAL-001 | Weighted Score Aggregation | process | `S = Σ(w_i × s_i)` |
| MTP-28-11-EVAL-002 | Risk Likelihood-Consequence Scaling | scaling | qualitative matrix |

---

## Summary

| Domain | Name | Tokens | Process | Scaling |
|--------|------|--------|---------|---------|
| GEOM | Geometry and Sizing | 4 | 2 | 2 |
| THRM | Thermal and Boil-Off | 6 | 3 | 3 |
| MATL | Materials and Structural | 5 | 3 | 2 |
| CERT | Certification and Safety | 4 | 4 | 0 |
| EVAL | Evaluation and Scoring | 2 | 1 | 1 |
| | **Total** | **21** | **13** | **8** |

---

## Traceability

- **Derives from:** TS-28-11-TS01, TS-28-11-TS02, TS-28-11-TS03, CM-28-11-CS25, MTL-28-11-00

## Feeds

| Lifecycle | Artifact |
|-----------|----------|
| LC05 | Parametric model implementation (process tokens as computation kernel) |
| LC05 | Automated sizing and boil-off estimation pipelines |
| LC06 | Verification method matrix (process-token-to-test mapping) |

---

## Governance

This MTL resides in `KDB/DEV/mtl/` and is **not baselined**.
Promotion to `KDB/LM/SSOT/` requires:

- BREX validation
- Trace coverage verification
- STK_ENG approval
- ECR submission via `GOVERNANCE/CHANGE_CONTROL/`
