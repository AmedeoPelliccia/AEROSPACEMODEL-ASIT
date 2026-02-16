# SCR-28 — Section / Component Resolution (Layer D4)

**ATA 28 Fuel System — Circular Cryogenic Cells**

| Key | Value |
|-----|-------|
| Token ID | `SCR-28` |
| ATA Code | 28 |
| Layer | D4 (Section / Component) |
| Token Pattern | `SCR-28-{SECTION_CODE}` |
| Total Sections | 12 |
| Sections with STPs | 1 (28-11) |
| Status | preliminary |

## Purpose

Layer D4 resolves which ATA 28 sub-system section a model request targets.
Each SCR token maps 1-to-1 to an ATA 28 section and enumerates the
Standard Token Procedures (STPs) available at that section.

## Section Map

| Token | Section | Title | Available STPs | Maturity |
|-------|---------|-------|:--------------:|----------|
| `SCR-28-00` | 28-00 | H₂ Cryogenic Fuel — General | 0 | scaffold |
| `SCR-28-10` | 28-10 | LH₂ Storage — General | 0 | parametric_models |
| `SCR-28-11` | 28-11 | LH₂ Primary Tank | 5 | trade_studies_complete |
| `SCR-28-13` | 28-13 | LH₂ Auxiliary Tank | 0 | scaffold |
| `SCR-28-21` | 28-21 | Cryogenic Transfer | 0 | scaffold |
| `SCR-28-22` | 28-22 | Insulated Transfer Lines | 0 | scaffold |
| `SCR-28-23` | 28-23 | Pressure Control | 0 | scaffold |
| `SCR-28-30` | 28-30 | Boil-Off Management | 0 | scaffold |
| `SCR-28-31` | 28-31 | Thermal Management | 0 | scaffold |
| `SCR-28-41` | 28-41 | H₂ Leak Detection | 0 | scaffold |
| `SCR-28-42` | 28-42 | Pressure Relief and Venting | 0 | scaffold |
| `SCR-28-43` | 28-43 | Fire Detection and Suppression | 0 | scaffold |

### SCR-28-11 Detail (trade_studies_complete)

| STP Token | Procedure | Class |
|-----------|-----------|-------|
| `STP-28-11-001` | LH₂ Tank Sizing | sizing |
| `STP-28-11-002` | Structural Substantiation | structural |
| `STP-28-11-003` | Trade Evaluation | evaluation |
| `STP-28-11-004` | CS 25 Compliance Assessment | compliance |
| `STP-28-11-005` | Vent and Relief Sizing | sizing |

## Routing

```
SDR-28 (D5) → SCR-28-{SECTION} (D4) → STP-28-{SECTION}-{SEQ} (D3)
                                        → MTP-28-{SECTION}-{DOMAIN}-{SEQ} (D2)
                                        → MTK-28-{SECTION}-{DOMAIN}-{SEQ} (D1)
```

## Traceability

- **Derives from**: `SDR-28`
- **Feeds**: D3 (STP-*), D2 (MTP-*), D1 (MTK-*)
