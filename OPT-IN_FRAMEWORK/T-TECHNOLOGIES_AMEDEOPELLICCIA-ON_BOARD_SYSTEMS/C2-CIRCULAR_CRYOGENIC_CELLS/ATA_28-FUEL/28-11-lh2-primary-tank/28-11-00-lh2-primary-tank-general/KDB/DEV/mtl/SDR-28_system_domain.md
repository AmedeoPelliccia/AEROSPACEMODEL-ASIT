# SDR-28 — System Domain Resolution (Layer D5)

**ATA 28 Fuel System — Circular Cryogenic Cells**

| Key | Value |
|-----|-------|
| Token ID | `SDR-28` |
| ATA Chapter | 28 — Fuel |
| Layer | D5 (System Domain — top) |
| Token Pattern | `SDR-{ATA_CHAPTER}` |
| Available Sections | 12 |
| Reachable STPs | 5 |
| Reachable MTP tokens | 21 |
| Reachable MTK tokens | 19 |
| Total tokens in model | 58 |
| Status | preliminary |

## Purpose

Layer D5 is the top-level entry point of the 5-dimensional token model.
A model consuming the `SDR-28` token receives the full system context
and can deterministically route through all five layers to reach any
individual method, process, or procedure in the ATA 28 Fuel System.

## 5-Dimensional Architecture

```
┌─────────────────────────────────────────────────────────┐
│  D5  SYSTEM DOMAIN          SDR-28                      │
│       └─ ATA 28 Fuel System (C2 Circular Cryogenic)     │
├─────────────────────────────────────────────────────────┤
│  D4  SECTION / COMPONENT    SCR-28-{SS}                 │
│       └─ 12 sections: 00, 10, 11, 13, 21–23, 30–31,    │
│          41–43                                          │
├─────────────────────────────────────────────────────────┤
│  D3  STANDARD PROCEDURE     STP-28-{SS}-{SEQ}           │
│       └─ 5 composed procedures (sizing, structural,     │
│          evaluation, compliance)                         │
├─────────────────────────────────────────────────────────┤
│  D2  PROCESS / SCALING      MTP-28-{SS}-{DOM}-{SEQ}     │
│       └─ 21 analytical methods and empirical             │
│          correlations (GEOM, THRM, MATL, CERT, EVAL)     │
├─────────────────────────────────────────────────────────┤
│  D1  SUBJECT                MTK-28-{SS}-{DOM}-{SEQ}     │
│       └─ 19 subject tokens (TS, CM, SC, EC)              │
└─────────────────────────────────────────────────────────┘
```

## System Context

**Mission:** Provide a safe, certifiable cryogenic hydrogen fuel system for
the AMPEL360 Q100 hydrogen-electric aircraft.

**Scope:**

- LH₂ storage (primary and auxiliary cryogenic tanks)
- Distribution (cryogenic transfer, insulated lines, pressure control)
- Boil-off management (BOG capture, venting, thermal management)
- Safety systems (H₂ leak detection, pressure relief, fire protection)
- Ground handling (refuelling, defuelling, purge, warm-up)
- Indication (fuel quantity, temperature, pressure monitoring)

**Regulatory Basis:** CS-25, S1000D 5.0, DO-160, ARP4754A, ARP4761, ISO 14687-2

**Special Conditions:**

| ID | Title |
|----|-------|
| SC-28-H2-001 | Hydrogen Storage and Distribution |
| SC-28-CRYO-002 | Cryogenic Temperature Handling |

## Available Sections

| SCR Token | Section | Title | STPs |
|-----------|---------|-------|:----:|
| `SCR-28-00` | 28-00 | H₂ Cryogenic Fuel — General | 0 |
| `SCR-28-10` | 28-10 | LH₂ Storage — General | 0 |
| `SCR-28-11` | 28-11 | LH₂ Primary Tank | 5 |
| `SCR-28-13` | 28-13 | LH₂ Auxiliary Tank | 0 |
| `SCR-28-21` | 28-21 | Cryogenic Transfer | 0 |
| `SCR-28-22` | 28-22 | Insulated Transfer Lines | 0 |
| `SCR-28-23` | 28-23 | Pressure Control | 0 |
| `SCR-28-30` | 28-30 | Boil-Off Management | 0 |
| `SCR-28-31` | 28-31 | Thermal Management | 0 |
| `SCR-28-41` | 28-41 | H₂ Leak Detection | 0 |
| `SCR-28-42` | 28-42 | Pressure Relief and Venting | 0 |
| `SCR-28-43` | 28-43 | Fire Detection and Suppression | 0 |

## Token Counts by Layer

| Layer | Prefix | Count | Description |
|-------|--------|------:|-------------|
| D5 | SDR- | 1 | System domain |
| D4 | SCR- | 12 | Sections/components |
| D3 | STP- | 5 | Standard procedures |
| D2 | MTP- | 21 | Process/scaling methods |
| D1 | MTK- | 19 | Subject tokens |
| **Total** | | **58** | |

## Routing Example

```
SDR-28                          → "Which system?"          → ATA 28 Fuel
  └─ SCR-28-11                  → "Which component?"       → LH₂ Primary Tank
       └─ STP-28-11-001         → "Which procedure?"       → Tank Sizing
            ├─ MTP-28-11-GEOM-001 → "Volume from mass"     → V = m / ρ
            ├─ MTP-28-11-GEOM-002 → "Sphere surface area"  → A = (36πV²)^(1/3)
            ├─ MTP-28-11-THRM-002 → "Total heat leak"      → Q = q × A
            ├─ MTP-28-11-THRM-001 → "Boil-off rate"        → ṁ = Q / h_fg
            └─ MTP-28-11-GEOM-004 → "Gravimetric eff."     → η = m_f/(m_f+m_t+m_s)
```

## Traceability

- **Derives from**: `ATA_28-FUEL/README.md`, `SCR-28`
- **Feeds**: D4 (SCR-28-\*), D3 (STP-\*), D2 (MTP-\*), D1 (MTK-\*)
