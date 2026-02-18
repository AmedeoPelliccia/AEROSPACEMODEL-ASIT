# ATEX Zone Classification and ESD Control — H₂ Leak Detection System
## ATX-28-41-00-atex-esd-zone-classification

**Work Package:** WP-28-07-01 ATEX/ESD Zone Classification  
**ATA Chapter:** 28-41-00 (H₂ Leak Detection)  
**Owner:** STK_SAF  
**Revision:** 0.1.0  
**Status:** Draft  
**Date:** 2026-02-18

---

## 1. Purpose and Scope

This document defines the ATEX (Atmospheres Explosibles) zone classification and
Electrostatic Discharge (ESD) control requirements for all areas in and around the
AMPEL360 Q100 hydrogen fuel system where an explosive or flammable atmosphere may
be present. It applies to the H₂ leak detection subsystem (ATA 28-41) and interfaces
with the complete cryogenic LH₂ fuel system (ATA 28).

The objectives are to:

- Classify all H₂ zones per ATEX Directive 2014/34/EU (and IECEx equivalent) and
  ensure all installed equipment meets zone requirements.
- Define ESD bonding, grounding, and personnel protection requirements to prevent
  electrostatic ignition of hydrogen.
- Provide future-proofing guidance aligned with emerging hydrogen standards
  (ISO/TC 197, EN 13463, SAE ARP 1216A).

---

## 2. Regulatory Basis

| Standard / Directive | Scope |
|----------------------|-------|
| ATEX Directive 2014/34/EU | Equipment and protective systems in explosive atmospheres (EU) |
| IECEx System (IEC 60079 series) | International explosive-atmosphere certification |
| IEC 60079-10-1:2020 | Classification of areas — explosive gas atmospheres |
| IEC 60079-14:2013 | Electrical installations design, selection, and erection |
| IEC 61340-4-3 | ESD — footwear for personnel protection |
| ISO 26142:2010 | Hydrogen detection apparatus — stationary applications |
| NFPA 2 (2020 ed.) | Hydrogen Technologies Code — zone classification |
| SAE ARP 1489 | Electrostatic Hazard Assessment for Aircraft Fuel Systems |
| CS-25 + SC-28-H2-001 | Aircraft airworthiness + H₂ special conditions |
| DO-160G | Environmental conditions for airborne equipment |

> **Note:** For airborne applications, ATEX/IECEx zone classifications are used as
> a *design input*. The aircraft certification basis (CS-25, Special Conditions) takes
> precedence. All installed equipment must additionally satisfy DO-160G environmental
> qualification for the relevant zones.

---

## 3. Hydrogen Explosive Atmosphere Properties

Understanding H₂ flammability limits is fundamental to zone classification:

| Property | Value |
|----------|-------|
| Lower Explosive Limit (LEL) | 4.0 % vol in air |
| Upper Explosive Limit (UEL) | 75.0 % vol in air |
| Auto-ignition temperature | 500–571 °C |
| Minimum ignition energy (MIE) | 0.017 mJ (extremely low — far below most ESD events) |
| Gas group (IEC 60079) | Group IIC |
| Temperature class | T1 (auto-ignition > 450 °C) |
| Density relative to air | 0.07 (highly buoyant — concentrates at top of enclosures) |

> **Critical:** Hydrogen's MIE is ~16× lower than methane. Any ESD event above
> ~0.02 mJ in an H₂-air mixture within the LEL–UEL range is a potential ignition
> source. Strict ESD control is mandatory in all Zone 1 and Zone 2 areas.

---

## 4. Zone Classification — AMPEL360 Q100 LH₂ System

Zone boundaries are defined per IEC 60079-10-1. Locations are classified based on
frequency and duration of explosive atmosphere occurrence:

| Zone | Definition | ATEX Equipment Category |
|------|------------|------------------------|
| Zone 0 | Explosive atmosphere present continuously or for long periods | Category 1G |
| Zone 1 | Explosive atmosphere likely to occur in normal operation | Category 1G or 2G |
| Zone 2 | Explosive atmosphere not likely to occur; if it does, only briefly | Category 1G, 2G, or 3G |

### 4.1 Zone 0 Locations

| Location ID | Description | Justification |
|-------------|-------------|---------------|
| Z0-28-11-INT | Interior of LH₂ primary tank (28-11) | Continuous LH₂/GH₂ atmosphere |
| Z0-28-13-INT | Interior of LH₂ auxiliary tank (28-13) | Continuous LH₂/GH₂ atmosphere |
| Z0-28-21-PUMP | Inside cryogenic transfer pump housing (28-21) | Continuous H₂ contact |
| Z0-28-30-VENT | Interior of boil-off management vent lines (28-30) | Continuous GH₂ flow |

Equipment in Zone 0 locations: Category 1G minimum (IECEx Ex ia or Ex ma).

### 4.2 Zone 1 Locations

| Location ID | Description | Radius / Extent | Justification |
|-------------|-------------|-----------------|---------------|
| Z1-28-11-DOME | Tank dome area, fittings, and valve cluster | 0.5 m from fittings | High probability of small H₂ release during normal operations (valve cycling, boil-off) |
| Z1-28-22-LINES | Insulated transfer line service points | 0.5 m from each connection | Potential release at couplings |
| Z1-28-41-SENS | Sensor enclosures in H₂-monitored bays | Sensor bay volume | Sensors designed for leak detection; background H₂ may be present |
| Z1-28-42-VENT | Pressure relief valve outlet (stack or pipe discharge) | 1.0 m sphere | Discharge of H₂ to vent path |
| Z1-28-43-DET | Fire/gas detector heads near tank | Detector housing | Proximity to potential H₂ source |
| Z1-GH-FILL | Ground handling refueling receptacle | 1.0 m sphere | Release during fill coupling/decoupling |

Equipment in Zone 1 locations: Category 2G minimum (IECEx Ex d, Ex e, Ex ia, or Ex n).

### 4.3 Zone 2 Locations

| Location ID | Description | Radius / Extent |
|-------------|-------------|-----------------|
| Z2-28-11-ADJ | Tank bay outer boundary | 1.0–3.0 m from Z1 boundary |
| Z2-28-30-BOG | Boil-off gas management compartment (ventilated) | Entire compartment |
| Z2-MAINT-AREA | Ground maintenance platform / refueling apron | 3.0 m radius from refueling point |
| Z2-28-41-CTRL | Leak detection controller housing | Controller enclosure |
| Z2-AUX-BAY | Auxiliary system bay adjacent to fuel system | Entire bay volume |

Equipment in Zone 2 locations: Category 3G acceptable (IECEx Ex n, Ex e, or Ex d).

### 4.4 Non-Hazardous (Safe) Areas

All areas outside the Zone 2 boundaries are classified as non-hazardous provided
adequate forced ventilation is maintained. The minimum ventilation rate to maintain
a non-hazardous classification outside Zone 2 will be defined in the Ventilation Design
Specification (VDS-28-XX-XX, TBD).

---

## 5. ATEX Equipment Marking Requirements

All electrical and electronic equipment installed within hazardous zones must carry
appropriate ATEX/IECEx marking:

```
Ex  [Category]  [Gas group]  [Temperature class]
Ex  II 2 G      IIC          T1
```

For the AMPEL360 Q100 LH₂ system, the minimum marking for Zone 1 equipment is:

```
II 2 G Ex db IIC T1 Gb
```

Key marking elements:

| Element | Value | Meaning |
|---------|-------|---------|
| Equipment group | II | Surface industry (incl. aviation) |
| Category | 2G | Zone 1 suitable |
| Gas group | IIC | Hydrogen (most demanding) |
| Temperature class | T1 | Max surface temp ≤ 450°C |
| Protection concept | db (or ia, eb, nA) | Flameproof enclosure (or intrinsic safety) |
| EPL | Gb | Equipment Protection Level b, gas |

> All sensors selected per SEN-28-41-00-selection-record must carry IIC T1 (or T2+)
> certification and be verified for Zone 1 installation before baseline lock.

---

## 6. ESD (Electrostatic Discharge) Control Requirements

### 6.1 Ignition Risk from ESD

Hydrogen's MIE of ~0.017 mJ makes it uniquely susceptible to electrostatic ignition.
The following events generate energies that exceed the H₂ MIE and must be controlled:

| ESD Source | Typical Energy | Risk in H₂ Zone |
|------------|---------------|-----------------|
| Personnel body discharge (ungrounded) | 10–100 mJ | CRITICAL — always exceeds MIE |
| Sliding clothing / PPE removal | 1–50 mJ | HIGH |
| Plastic container / tool discharge | 0.1–10 mJ | HIGH |
| Ungrounded metal tool | 0.05–5 mJ | HIGH |
| Sensor cable connector plug/unplug (unisolated) | 0.01–1 mJ | MODERATE (close to MIE) |

### 6.2 Bonding and Grounding Requirements

All conductive elements within Zone 0 and Zone 1 areas must be bonded and grounded
per SAE ARP 1489 and NFPA 2 Chapter 7:

**Mandatory bonding points:**

| Item | Bond Requirement | Resistance Target |
|------|-----------------|-------------------|
| LH₂ tank (primary and auxiliary) | Bond to aircraft structure | < 1 Ω |
| Cryogenic transfer lines | Bond at each support point, max 1 m spacing | < 1 Ω each segment |
| Refueling receptacle / coupling | Bond to aircraft before H₂ flow; ground cable to refueling cart | < 0.1 Ω |
| Pressure relief valve bodies | Bond to aircraft structure | < 1 Ω |
| Leak detection sensor housings | Bond through mounting hardware | < 1 Ω |
| Boil-off vent stack / piping | Bond to structure, earthed at vent outlet | < 1 Ω |
| Maintenance platforms / ground vehicles | Bond to aircraft before approach to Zone 1 | < 25 Ω (NFPA 77) |

**Personnel ESD control (Ground operations — Zone 1 / Zone 2):**

- Personnel must wear ESD-dissipative footwear (IEC 61340-4-3, resistance 10⁵–10⁸ Ω).
- Wrist straps (10⁵–10⁷ Ω) required when handling electronic sensor equipment.
- No synthetic clothing in Zone 1 areas during H₂ operations; natural fibers or
  ESD-rated coveralls required.
- Personnel grounding point (ESD post) mandatory at Zone 1 entry.

**Airborne operations:**

- Aircraft structure must be at a known static potential relative to ground
  (lightning protection bonding per ATA 24 / DO-160G Section 22 applies).
- All H₂ system components integrated into aircraft static dissipation network.
- Intrinsically safe sensor circuits must have energy limitation per IEC 60079-11
  (Ex ia: max stored energy ≤ 20 µJ, max voltage ≤ 30 V in Zone 0 circuits).

### 6.3 ESD Control During Maintenance

The following procedural controls apply to H₂ system maintenance in Zones 1 and 2:

1. **Pre-work check:** Verify bonding strap on ground service equipment (GSE).
2. **Personnel grounding:** Technician grounds self at ESD post before entering Zone 1.
3. **Tool selection:** Use non-sparking (beryllium-copper or ESD-rated) hand tools.
4. **Cable handling:** All H₂ sensor cables must be handled with ESD precautions;
   connector mating/de-mating only performed with sensor circuit de-energized or
   confirmed intrinsically safe.
5. **PPE:** Cryogenic gloves and coverall must be ESD-rated (see Section 6.2).
6. **Re-inspection:** After any maintenance in Zone 1/2, verify bonding continuity
   before H₂ system re-energization.

---

## 7. Future-Proofing: Emerging Standards and Technology Watch

The hydrogen aviation regulatory landscape is evolving rapidly. The following standards
and initiatives should be monitored for impact on zone classification and ESD requirements:

| Standard / Initiative | Status | Expected Impact |
|-----------------------|--------|-----------------|
| IEC 60079-10-1 Rev (next ed.) | Under revision (TC 31) | Possible updates to zone extent calculation for buoyant gases; may reduce Zone 2 extent for LH₂ in ventilated compartments |
| ISO/TC 197 WG 13 (H₂ aircraft fueling) | Active | Ground refueling procedure standardization; zone extents for aircraft refueling points |
| EN 13463-1 (Non-electrical ATEX equipment) | Active revision | Expanded scope for non-electrical valves, couplings in Zone 0/1 |
| SAE ARP 1216A (Aircraft bonding/grounding) | Under review | May update resistance limits for composite aircraft structures (relevant to AMPEL360 Q100 composite airframe) |
| CS-25 Hydrogen Special Conditions (EASA NPA) | In consultation | Formal special conditions for H₂ aircraft; may supersede SC-28-H2-001 |
| FAA Issue Paper (H₂ propulsion) | Draft | US certification basis for H₂ aircraft; harmonization with EASA expected |
| IEC 61340-5-1 Rev | Under revision | ESD control for electronics in industrial/aerospace; watch for aviation sector annex |
| NFPA 2 (2024/2027 ed.) | Active | Chapter 7 (Aircraft) updates for LH₂ airport infrastructure; may change ground-service zone extents |
| ISO 14687-2 (H₂ fuel purity) | Stable | Currently referenced; watch for aircraft-specific addendum |

### 7.1 Design Provisions for Regulatory Evolution

To future-proof the H₂ system design against standard evolution:

1. **Zone extent margins:** Apply 20 % additional margin beyond current IEC 60079-10-1
   zone extents at design stage. This buffer accommodates likely increases from upcoming
   standards revisions.
2. **Sensor over-specification:** Select sensors rated two zones above the installed zone
   (e.g., Zone 0 rated sensors for Zone 1 installations) to allow reclassification without
   hardware replacement.
3. **Bonding resistance target:** Design to < 0.1 Ω for primary H₂ system bonds (versus
   the 1 Ω mandatory minimum), providing margin for composite structure degradation and
   tightened SAE ARP 1216A limits.
4. **IIC T1 as minimum:** Even in Zone 2, use IIC T1 rated equipment. As zone boundaries
   shift, no hardware reclassification is needed.
5. **ESD post density:** Install personnel ESD grounding posts at all Zone 2 entry points
   (not just Zone 1), anticipating expanded zone extents from buoyant gas revisions.
6. **Documentation versioning:** This document shall be reviewed against current standards
   at each major lifecycle gate (LC04, LC06, LC08) and updated within 6 months of any
   superseding standard release.

---

## 8. Compliance Matrix

| Requirement | Standard Reference | Compliance Method | Status |
|-------------|-------------------|-------------------|--------|
| Zone classification per IEC 60079-10-1 | IEC 60079-10-1:2020 | Analysis + Zone Map (this doc) | Draft |
| Equipment marking Group IIC T1 | IEC 60079-0 / ATEX 2014/34/EU | Equipment selection record + datasheet review | Draft |
| ESD bonding ≤ 1 Ω | SAE ARP 1489 / NFPA 2 Ch.7 | Design specification + acceptance test | Draft |
| Sensor ATEX certification for Zone 1 | IEC 60079-14 | Sensor qualification record (SEN-28-41-00) | Draft |
| Personnel ESD footwear IEC 61340-4-3 | IEC 61340-4-3 | PPE procurement spec + training record | Draft |
| Intrinsic safety for Zone 0 circuits | IEC 60079-11 (Ex ia) | Circuit energy analysis | Draft |
| Future standards review schedule | Project governance | This doc Section 7 + lifecycle gate checklist | Draft |

---

## 9. Open Actions

| ID | Action | Owner | Target Date |
|----|--------|-------|-------------|
| ATX-001 | Complete zone boundary map / CAD drawing (Z0/Z1/Z2 extents) | STK_SE | LC04 gate |
| ATX-002 | Confirm sensor IIC T1 certification for selected sensors (PGS4100, HLD) | STK_SAF | LC04 gate |
| ATX-003 | Define ventilation rate for non-hazardous zone outside Zone 2 | STK_SE | LC04 gate |
| ATX-004 | Review and update this doc against IEC 60079-10-1 next edition when published | STK_SAF | 6 months post-publication |
| ESD-001 | Define bonding test procedure and acceptance criteria | STK_SE | LC05 gate |
| ESD-002 | Select and specify ESD-rated PPE for maintenance personnel | STK_SAF | LC07 gate |
| ESD-003 | Evaluate composite structure bonding resistance for AMPEL360 Q100 airframe | STK_SE | LC04 gate |

---

## 10. Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-02-18 | STK_SAF | Initial draft — zone classification, ESD requirements, future-proofing |

---

**End of Document**
