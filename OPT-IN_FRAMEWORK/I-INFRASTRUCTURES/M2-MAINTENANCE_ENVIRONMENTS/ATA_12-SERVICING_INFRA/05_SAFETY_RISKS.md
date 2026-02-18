# ATA 12 — Servicing Infrastructure: Safety & Risk Assessment

**Section:** 6 — Safety & Risk Assessment  
**Parent:** [`README.md`](README.md) | **Crosswalk:** [`../CROSSWALK.md`](../CROSSWALK.md)

> **Escalation:** Any update to this section requires review by **STK_SAF** per BREX rules `SAFETY-002`, `SAFETY-H2-001`, and `SAFETY-H2-002`.

---

## Hazard Identification

### H12-01 — H₂ Leak During LH₂ Refuelling (Explosion / Asphyxiation) ⭐

| Attribute | Detail |
|---|---|
| **Hazard** | H₂ leak during fuelling accumulates to explosive concentration (4–75% vol in air) |
| **Severity** | Catastrophic |
| **Probability** | Very Low with Zone 1/2 classification and controls |
| **Root causes** | Defective coupling, hose rupture, overpressure, coupling connect/disconnect error |
| **Mitigations** | Zone 1/2 ATEX classification; fixed H₂ detection (alarm 10%, evacuation 25% LEL); forced ventilation ≥ 15 ACH; bonding/earthing; personal H₂ detectors; no ignition sources within 7.5 m; slow coupling connect/disconnect procedure |
| **Residual risk** | ALARP — STK_SAF sign-off required per BREX SAFETY-H2-001 |
| **Reference** | [`../../../../.github/instructions/ata28_h2_cryogenic.instructions.md`](../../../../.github/instructions/ata28_h2_cryogenic.instructions.md) |

---

### H12-02 — Cryogenic Burn During Coupling or LH₂ Cart Operation ⭐

| Attribute | Detail |
|---|---|
| **Hazard** | Skin or eye contact with LH₂ at −253 °C causing cryogenic burn / frostbite |
| **Severity** | Major |
| **Probability** | Low with correct PPE and coupling procedure |
| **Mitigations** | Mandatory PPE: EN 511 cryogenic gloves, EN 166 face shield, cryogenic apron; slow coupling procedure (no forced connection); personnel training on cryogenic hazards; emergency shower within 10 m of fuelling bay |
| **Residual risk** | ALARP |

---

### H12-03 — LH₂ Purity Non-Conformance (Fuel Contamination) ⭐

| Attribute | Detail |
|---|---|
| **Hazard** | Off-spec LH₂ (CO, CO₂, or hydrocarbon contamination) damages fuel cell membranes or causes system failure |
| **Severity** | Hazardous |
| **Probability** | Low with ISO 14687-2 verification |
| **Mitigations** | In-line purity sensor with ISO 14687-2 thresholds as hard hold; CoA required for each delivery; sensor calibrated every 6 months; fuel upload halted on any purity exceedance |
| **Residual risk** | ALARP |

---

### H12-04 — High-Pressure Hydraulic Line Failure

| Attribute | Detail |
|---|---|
| **Hazard** | Hydraulic fluid injected into skin or eyes during servicing; fire risk from Skydrol vapour |
| **Severity** | Major |
| **Probability** | Low with correct cart and hose condition |
| **Mitigations** | Hose rated ≥ 1.5× working pressure; pre-use visual inspection; face shield mandatory during hydraulic connections; work clothing covers all skin |
| **Residual risk** | ALARP |

---

## Emergency Procedures

### H₂ Alarm During LH₂ Fuelling
> **DANGER: Do not operate any electrical switch.**
1. Close LH₂ supply valve on servicing cart (manual lever — approved for Zone 1 operation).
2. Sound evacuation alarm.
3. All personnel evacuate to upwind muster point (≥ 15 m).
4. Contact Safety Officer and ATA 28 responsible engineer.
5. Do not re-enter bay until H₂ < 10% LEL confirmed.

### Cryogenic Spill / Contact
1. Move away from spill area immediately.
2. If skin/eye contact: irrigate immediately with copious water for ≥ 15 min; seek medical attention.
3. Do not attempt to blot or remove frozen LH₂ from clothing; allow to evaporate.
4. Contact Safety Officer and escalate to emergency services if burn is severe.

---

## PPE Requirements Summary

| Service | Required PPE |
|---|---|
| Standard fluid servicing | Safety shoes, gloves, safety glasses |
| LH₂ fuelling / defuelling | EN 511 cryogenic gloves, EN 166 face shield, cryogenic apron, safety shoes, personal H₂ detector |

---

*End of ATA 12 — Safety & Risk Assessment*
