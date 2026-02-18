# ATA 12 — Servicing Infrastructure: Procedures

**Section:** 5 — Procedures  
**Parent:** [`README.md`](README.md) | **Crosswalk:** [`../CROSSWALK.md`](../CROSSWALK.md)

---

## Overview

This document captures the step-by-step operational procedures for servicing the AMPEL360 Q100. Infrastructure-specific steps (cart positioning, bay setup, safety system checks) supplement the aircraft AMM ATA 12 task procedures.

> **Safety prerequisite:** Read [`05_SAFETY_RISKS.md`](05_SAFETY_RISKS.md) before starting any procedure.

---

## Procedure 12-PRO-001 — Standard Fluid Servicing (Hydraulic / Oil)

### Prerequisites
- [ ] Aircraft on ground, parking brake set, wheel chocks in place.
- [ ] Applicable service cart inspected and confirmed within calibration.
- [ ] AMM ATA 12 task reference identified.

### Steps
1. Position service cart adjacent to aircraft service point.
2. Connect bonding cable (cart to aircraft).
3. Connect service hose to aircraft servicing point.
4. Perform fluid sampling (if required by AMM) before replenishment.
5. Fill to quantity specified in AMM.
6. Disconnect hose; secure aircraft service point cap.
7. Remove bonding cable.
8. Discard sample (if applicable) per HAZMAT disposal procedure.
9. Record in aircraft technical log.

---

## Procedure 12-PRO-002 — LH₂ Refuelling ⭐

> **⭐ Special Condition — Hydrogen Hazard:** This procedure involves cryogenic liquid hydrogen at −253 °C. Personnel must have completed H₂ safety training. Read full hazard assessment in [`05_SAFETY_RISKS.md`](05_SAFETY_RISKS.md) before starting.

> **DANGER:** Hydrogen is extremely flammable (flammable in air between 4% and 75% by volume). No open flames or ignition sources within 7.5 m. Ensure forced ventilation is operating. Use approved ATEX equipment only.

### Prerequisites
- [ ] LH₂ fuelling bay ventilation confirmed running (≥ 15 ACH).
- [ ] H₂ fixed detection system confirmed operational (bump test within 24 h).
- [ ] All personnel equipped with personal H₂ detectors and cryogenic PPE.
- [ ] Aircraft bonded and grounded (resistance verified ≤ 1 Ω).
- [ ] LH₂ servicing cart bonded to aircraft.
- [ ] LH₂ certificate of analysis (CoA) available; purity confirmed per ISO 14687-2.
- [ ] Aircraft isolation valves confirmed in fuelling-open position (per AMM ATA 28).

### Steps
1. Position LH₂ servicing cart at fuelling port; verify hose length permits connection without strain.
2. Connect bonding cable: cart → aircraft fuelling port vicinity.
3. Slowly connect cryogenic coupling to aircraft fuelling port (per manufacturer coupling procedure).
4. Confirm boil-off recovery line connected (or vent stack open if recovery unavailable).
5. Open LH₂ supply valve slowly; monitor fuel quantity indication.
6. Monitor H₂ detectors throughout fuelling; halt if pre-alarm activates.
7. Close supply valve when target quantity reached (per dispatch fuel load).
8. Allow 30 s for pressure equalisation; confirm boil-off flow stops.
9. Disconnect boil-off recovery line; cap recovery port.
10. Slowly disconnect cryogenic coupling from aircraft.
11. **Immediately** purge aircraft fuelling port with GN₂ for ≥ 30 s.
12. Confirm fuelling port cap secure; log fuel mass and temperature in tech record.
13. Disconnect bonding cable.
14. Move servicing cart to safe distance (≥ 7.5 m).

### Post-Fuelling H₂ Purity Recording
- Record in-line purity sensor readings for CO, CO₂, and H₂O to aircraft tech record.
- If any parameter exceeds ISO 14687-2 limit: halt fuelling immediately; notify Safety Officer and ATA 28 responsible engineer.

---

## Procedure 12-PRO-003 — LH₂ Defuelling (Before Maintenance) ⭐

1. Position LH₂ servicing cart (reverse transfer mode) at fuelling port.
2. Bond and ground aircraft and cart.
3. Connect recovery hose from aircraft fuelling port to cart.
4. Reverse transfer LH₂ to cart Dewar (monitor pressure throughout).
5. When tank level < 5% (minimum residual), close transfer valve.
6. Initiate controlled boil-off of residual with vent stack open.
7. When quantity = 0 and pressure ≤ 0.05 MPa gauge, close isolation valves.
8. Purge with GN₂; verify H₂ concentration in tank < 1% by volume before handing over for maintenance.
9. Record defuelling in tech log.

---

*End of ATA 12 — Procedures*
