# ESD Bonding and Grounding Requirements — LH₂ Fuel System
## ESD-28-00-00-bonding-grounding

**Work Package:** WP-28-07-02 ESD Bonding and Grounding  
**ATA Chapter:** 28-00-00 (H₂ Cryogenic Fuel — General)  
**Owner:** STK_SAF  
**Revision:** 0.1.0  
**Status:** Draft  
**Date:** 2026-02-18

---

## 1. Purpose and Scope

This document defines the system-level Electrostatic Discharge (ESD) bonding and
grounding requirements for the complete ATA 28 LH₂ cryogenic fuel system of the
AMPEL360 Q100. It is a cross-cutting safety document applicable to all ATA 28
subsystems and must be read in conjunction with the ATEX zone classification document
(ATX-28-41-00-atex-esd-zone-classification.md).

Scope includes:

- Structural bonding requirements for all H₂ system components
- Ground handling ESD control (refueling, defueling, maintenance)
- Airborne static management for the H₂ fuel system
- Composite airframe bonding considerations
- Test and acceptance criteria for bonding continuity
- Future-proofing provisions for next-generation standards

---

## 2. Background: ESD Hazard in LH₂ Systems

Liquid hydrogen systems present uniquely severe ESD ignition risks:

**Why ESD is critical for LH₂:**

1. **Ultra-low minimum ignition energy (MIE):** H₂ has an MIE of ~0.017 mJ, which is
   orders of magnitude lower than kerosene (~0.25 mJ) or methane (~0.28 mJ). A typical
   ungrounded person walking on a dry floor accumulates 10–100 mJ — sufficient to ignite
   H₂ thousands of times over.

2. **Wide flammability range:** The LEL–UEL window (4–75 % vol) means that even a brief
   H₂ release creates a large ignitable region. Small leaks that would be negligible for
   kerosene create significant ESD ignition hazards.

3. **Boil-off during ground operations:** LH₂ inevitably produces cryogenic boil-off
   (GH₂) during refueling and ground standby, creating a continuous Zone 1 atmosphere
   around fill points and vent lines.

4. **Cryogenic flow triboelectrification:** High-velocity LH₂ flow through pipes and
   hoses can generate significant electrostatic charge, analogous to petroleum system
   flow charging — but with far lower ignition energy required.

5. **Composite airframe concerns:** Modern composite aircraft structures (CFRP) are
   inherently poor electrical conductors. Without dedicated bonding provisions, composite
   H₂ system enclosures may accumulate charge rather than dissipate it.

---

## 3. Applicable Standards

| Standard | Application to This Document |
|----------|------------------------------|
| SAE ARP 1489 | Aircraft fuel systems bonding and grounding |
| NFPA 2 (2020), Chapter 7 | Hydrogen technologies — aircraft operations |
| NFPA 77 (2019) | Recommended practice on static electricity |
| IEC 60079-14:2013 | Electrical installation in explosive atmospheres |
| IEC 61340-4-3 | ESD footwear testing |
| IEC 61340-5-1:2016 | ESD control for electronic devices |
| MIL-B-5087B | Bonding, electrical, and lightning protection (heritage reference) |
| DO-160G, Section 22 | Aircraft lightning and ESD protection |
| CS-25 AMC 25.981 | Fuel tank ignition prevention (adapted for H₂) |
| SC-28-H2-001 | Hydrogen storage and distribution special conditions |

---

## 4. Bonding and Grounding Architecture

### 4.1 Ground Reference Hierarchy

All ATA 28 H₂ system components are bonded through a hierarchical grounding network:

```
Aircraft Structure (Primary Ground Reference)
    │
    ├── H₂ Primary Tank (28-11)    — Direct bond to structure (< 1 Ω)
    │       ├── Tank dome fittings  — Bonded through tank body
    │       ├── Tank isolation valves — Individual bonds (< 1 Ω)
    │       └── Tank instrumentation — Bonded via mounting flanges
    │
    ├── Transfer Lines (28-22)     — Bond at each support clamp (< 1 Ω)
    │
    ├── Pressure Control System (28-23) — Bond to structure (< 1 Ω)
    │
    ├── Boil-Off Management (28-30) — Bond at manifold entry (< 1 Ω)
    │
    ├── H₂ Leak Detectors (28-41) — Bond through mounting hardware (< 1 Ω)
    │
    ├── Pressure Relief Valves (28-42) — Bond to structure (< 1 Ω)
    │
    └── Refueling Receptacle        — Bond to structure; external ground cable (< 0.1 Ω)
            └── Ground Service Equipment — Bond cable to aircraft before H₂ flow
```

### 4.2 Bonding Point Requirements

| Component | Bond Path | Maximum Resistance | Bond Type |
|-----------|-----------|-------------------|-----------|
| LH₂ primary tank (28-11) | Tank shell → structure | ≤ 1 Ω | Direct metallic bond strap |
| LH₂ auxiliary tank (28-13) | Tank shell → structure | ≤ 1 Ω | Direct metallic bond strap |
| Vacuum-jacketed transfer lines | Each support clamp → structure | ≤ 1 Ω | Clamp continuity + strap |
| Pressure regulators / valves | Body → structure | ≤ 1 Ω | Body metallic bond |
| Refueling receptacle | Fitting → structure | ≤ 0.1 Ω | Dedicated low-resistance strap |
| Vent/relief piping | At pipe bracket → structure | ≤ 1 Ω | Direct strap |
| Sensor cable shields (28-41) | Shield → structure at both ends | ≤ 1 Ω | Shield termination |
| Boil-off vent stack | Stack flange → structure + earth | ≤ 1 Ω + earth rod | Earth termination at vent exit |
| LH₂ fill hose (GSE) | Hose outer braid → aircraft ground | ≤ 0.1 Ω | Pre-connect before H₂ flow |

### 4.3 Composite Airframe Bonding Provisions

The AMPEL360 Q100 uses carbon-fibre reinforced polymer (CFRP) for the primary airframe.
CFRP conductivity varies significantly:

| CFRP Type | Typical Through-Thickness Resistance | Bonding Approach |
|-----------|--------------------------------------|-----------------|
| Standard CFRP (no copper mesh) | 10³–10⁷ Ω/cm² | Insufficient for H₂ system direct bond; metallic insert required |
| CFRP + copper/bronze mesh | 10⁰–10² Ω/cm² | Suitable with co-cured metallic fastener at bond point |
| CFRP + metallic liner (H₂ tank) | < 1 Ω | Direct bond acceptable |

**Requirements for composite H₂ enclosures:**

- All H₂ system components mounted in CFRP structures must bond through **metallic
  fastener inserts** that pass through the composite to the structural ground network.
- Inserts must be co-cured or wet-installed with conductive sealant (e.g., PR-1776 B-2).
- Bond jumpers (minimum AWG 6 / 13 mm² cross-section) must be provided between metallic
  H₂ components and the nearest airframe ground bus where direct fastener continuity
  cannot be verified.
- Bond resistance must be verified at production FAI and at each D-check interval.

---

## 5. Ground Handling ESD Procedures

### 5.1 Refueling Operations

The following ESD sequence is mandatory before any LH₂ transfer:

1. **GSE earth:** Ground service vehicle earthed to airport ground point (< 25 Ω per
   NFPA 77) before approach to aircraft.
2. **Aircraft ground:** Verify aircraft is grounded to hangar or apron ground point
   (< 25 Ω).
3. **Bond cable:** Connect bonding cable between GSE and aircraft (< 0.1 Ω) before
   the refueling hose is positioned.
4. **Hose connection:** Connect cryogenic fill hose with integrated ground braid (< 0.1 Ω)
   before opening any valve.
5. **Personnel grounding:** All personnel within Zone 1 (1 m around fill receptacle) must
   be grounded via ESD wrist strap (10⁵–10⁷ Ω) connected to the aircraft ground point.
6. **ESD footwear check:** Footwear resistance verified at entry to Zone 1
   (10⁵–10⁸ Ω per IEC 61340-4-3).
7. **Only then:** Valves may be opened and H₂ flow initiated.

On completion: Close valves → isolate H₂ → disconnect hose → disconnect bond cable →
disconnect aircraft ground → release GSE earth (reverse order).

### 5.2 Maintenance Operations

| Task | ESD Pre-Requisite |
|------|-------------------|
| Sensor replacement (Zone 1 area) | Wrist strap + ESD-rated footwear; sensor circuit de-energized |
| Valve maintenance | Bonding verified; no H₂ in system or purged inert |
| Transfer line coupling work | Bonding verified; line purged; work permit issued |
| Tank instrumentation work | Tank vented and purged; bonding verified |
| Any work in CFRP H₂ enclosure | Verify metallic insert bond continuity before and after |

### 5.3 Non-Sparking Tool Requirements

In Zone 1 and Zone 2 areas, the following tool restrictions apply:

- Steel tools and steel-tipped screwdrivers: **PROHIBITED** in Zone 1.
- Beryllium-copper (BeCu) non-sparking tools: **REQUIRED** in Zone 1.
- Aluminium-alloy hand tools (non-anodized): Acceptable in Zone 2 only.
- Power tools (battery or pneumatic): Only if ATEX-certified for Zone 2 minimum.
- All tools must be tracked in the ESD tool register for the H₂ system.

---

## 6. Airborne Static Management

During flight, the LH₂ fuel system must not accumulate dangerous charge levels:

### 6.1 Static Dissipation During LH₂ Flow

- LH₂ flow velocities in transfer lines are limited to ≤ 2 m/s during normal operation
  to minimise triboelectric charge generation (per ARP 1489 guidance for cryogenic flows).
- Transfer line inner surfaces shall be stainless steel (non-insulating); PTFE inner
  liners are prohibited due to triboelectric charge accumulation risk.
- Flow-induced charge shall be calculated per the method in ARP 1489 Section 5.3 and
  verified against the H₂ MIE with a safety factor of ≥ 100.

### 6.2 Lightning and HIRF

- All H₂ system components must demonstrate lightning protection per DO-160G Section 22
  and satisfy HIRF requirements per DO-160G Section 20.
- Lightning strike current must be shunted to structure before reaching H₂ wetted
  components. All bonding straps must carry the designated lightning current without
  fusing (minimum AWG 6 for primary bond straps).

---

## 7. Test and Acceptance Criteria

### 7.1 Production Acceptance Tests

| Test | Method | Acceptance Criterion |
|------|--------|---------------------|
| Bond resistance — tank to structure | 4-wire resistance measurement (Ducter or equivalent) | ≤ 1 Ω |
| Bond resistance — refueling receptacle | 4-wire resistance measurement | ≤ 0.1 Ω |
| Bond resistance — transfer line segment | 4-wire resistance per segment | ≤ 1 Ω per segment |
| Bond resistance — composite insert | 4-wire measurement through CFRP insert | ≤ 1 Ω |
| Sensor circuit energy (Zone 0 loops) | Calculated per IEC 60079-11 + measured | ≤ 20 µJ stored |
| ESD personnel footwear | Per IEC 61340-4-3 test method | 10⁵–10⁸ Ω |

### 7.2 In-Service Inspection Intervals

| Item | Inspection Interval | Method |
|------|--------------------|---------| 
| Tank-to-structure bonds | Annual (A-check or equivalent) | Visual + resistance measurement |
| Transfer line segment bonds | Annual | Visual + resistance spot check |
| Refueling receptacle bond | Before each refueling campaign | Resistance measurement |
| Composite insert bonds | D-check (structural inspection) | 4-wire resistance |
| ESD footwear | Before each Zone 1 entry | On-site resistance tester |

---

## 8. Future-Proofing Provisions

As H₂ aviation standards mature, the following provisions are built into this specification
to avoid costly redesign:

1. **SAE ARP 1216A watch:** The next revision of ARP 1216 may introduce lower resistance
   limits for composite aircraft (possibly ≤ 0.1 Ω for primary bonds). All primary bond
   straps in the current design are sized to meet ≤ 0.1 Ω to pre-empt this revision.

2. **IEC 61340 aviation sector annex:** An aviation-specific annex to IEC 61340-5-1 is
   expected. Current design exceeds the draft thresholds.

3. **ISO/TC 197 WG 13 (aircraft fueling):** Ground refueling ESD sequence in Section 5.1
   is designed to align with the draft ISO WG 13 protocol where known.

4. **EASA CS-25 H₂ SC revision:** When formal EASA special conditions for H₂ aircraft are
   published, this document will be reviewed against the new requirements within 3 months
   of publication, per WP-28-07-02 action FUT-003.

5. **Digital continuity checks:** Provisions for in-flight bonding resistance monitoring
   (via embedded resistance sensors at key bond points) are reserved in the system
   architecture for future enablement. The mounting provisions will be defined in a future
   28-41 controller interface specification (ICD-28-41-00-C2-CELL, TBD).

---

## 9. Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-02-18 | STK_SAF | Initial draft |

---

**End of Document**
