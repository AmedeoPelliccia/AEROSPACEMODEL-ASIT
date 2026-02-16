# TS-28-11-TS03 — Insulation and Thermal Control: Vacuum+MLI vs Foam vs Active Cooling

| Key | Value |
|-----|-------|
| Trade Study ID | TS-28-11-TS03 |
| ATA Code | 28-11-00 |
| Technology Domain | C2 — Circular Cryogenic Cells |
| Aircraft Programme | AMPEL360 Q100 |
| Lifecycle Phase | LC04 (Design Definition) |
| Status | Preliminary |
| Author | STK_ENG |
| Date | 2026-02-16 |

## Objective

Evaluate insulation and thermal control concepts for the LH2
primary tank comparing vacuum-jacketed MLI, foam, and active
cooling approaches for heat flux, boil-off performance,
system complexity, and vacuum integrity sensitivity.

### Reference Thermal Data

| Parameter | Value |
|-----------|-------|
| Measured system heat flux | 1.26–1.36 W/m² |
| LH₂ latent heat | 445.5 kJ/kg |
| MLI vacuum requirement | 0.0133–0.266 Pa |
| Degraded vacuum threshold | ~1.33 Pa |
| Warm boundary | 300 K |
| Cold boundary | 20.3 K |

---

## Options Considered

| Option | Name | Type | Heat Flux | TRL | Mass | Maintainability | Risk |
|--------|------|------|-----------|-----|------|-----------------|------|
| A | Vacuum Jacket + MLI | Passive | 1.26–1.36 W/m² (measured) | High | Medium | Medium | Medium |
| B | Foam Insulation | Passive | Higher than vacuum systems | Medium | High | High | Low |
| C | Hybrid Active Cooling | Active | Can approach zero boil-off | Low | High | Low | High |

### Option A — Vacuum Jacket + MLI

- **Vacuum sensitivity:** High — slight vacuum loss can erode MLI advantage
- **Required vacuum:** 0.0133–0.266 Pa
- **Penetration impact:** Supports and man-way conduction can dominate heat leak
- **Heritage:** NASA IRAS tank testing, aerospace cryogenic systems
- **Boil-off driver:** Broad-area MLI + thermal bridges (supports, penetrations)

### Option B — Foam Insulation

- **Simplicity:** No vacuum system required
- **Boil-off penalty:** Markedly higher evaporation than vacuum systems
- **Operational impact:** May require operational venting or active systems
- **Heritage:** Non-aircraft large-scale LH2 storage evaluations

### Option C — Hybrid Active Cooling

- **Power requirement:** Significant cryocooler power draw
- **Failure mode:** Loss of active cooling requires fallback to passive
- **Certification:** Requires MoC for active safety-critical thermal controls
- **Heritage:** NASA zero boil-off research programmes

---

> **Critical Design Insight:** Supports and penetrations can dominate heat
> leak.  NASA IRAS analysis shows that despite small conduction areas,
> support-pad conduction can be comparable to or exceed the MLI
> contribution, and large man-way penetrations can represent a substantial
> fraction of total heat leak.

---

## Preliminary Selection

**Selected Option:** A — Vacuum Jacket + MLI
**Baseline Name:** Vacuum Jacket + MLI with Engineered Thermal Bridges

### Rationale

- Heritage from NASA cryogenic tank programmes
- Measured system heat flux ~1.3 W/m² achievable when thermal bridges are managed
- Predictable boil-off modelling (steady-state Q/h\_fg method)
- Thermal bridge engineering (supports, penetrations) is the primary design lever

---

## Feeds

| Lifecycle | Artifact |
|-----------|----------|
| LC05 | Thermal transient simulation (mission profile) |
| LC05 | Support and penetration heat-leak decomposition analysis |
| LC06 | Vacuum integrity test programme |

## Traceability

- **Derives from:** TS-28-10-TS03
