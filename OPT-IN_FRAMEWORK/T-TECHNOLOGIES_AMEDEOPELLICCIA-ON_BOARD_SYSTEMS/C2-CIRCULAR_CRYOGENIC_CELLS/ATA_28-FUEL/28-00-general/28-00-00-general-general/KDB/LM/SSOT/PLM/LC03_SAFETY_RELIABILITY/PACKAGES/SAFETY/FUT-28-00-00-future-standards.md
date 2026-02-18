# Future Standards Watch — Hydrogen and Fuel Cell Infrastructure
## FUT-28-00-00-future-standards

**Work Package:** WP-28-07-03 Future Standards and Regulatory Watch  
**ATA Chapter:** 28-00-00 (H₂ Cryogenic Fuel — General)  
**Owner:** STK_SAF  
**Revision:** 0.1.0  
**Status:** Draft  
**Date:** 2026-02-18

---

## 1. Purpose

This document provides a structured watch list for emerging standards, regulations,
and technology developments relevant to hydrogen and fuel cell infrastructure in
aviation. It supports future-proofing of the AMPEL360 Q100 H₂ system design (ATA 28)
and the fuel cell power plant (ATA 71) by identifying anticipated regulatory changes
and providing design provisions to accommodate them.

This document is a living record, reviewed at each lifecycle gate and updated within
6 months of any significant standard publication.

---

## 2. Standards Watch List

### 2.1 Explosive Atmosphere Standards (ATEX/IECEx)

| Standard | Current Edition | Status | Anticipated Change | Design Impact |
|----------|----------------|--------|-------------------|---------------|
| IEC 60079-10-1 (Zone classification — gas) | 2020 ed. | Under TC 31 revision | Revised zone extent calculation for buoyant gases (H₂); may reduce Zone 2 extent in ventilated compartments | Review ATX-28-41-00 zone map; potential zone reduction |
| IEC 60079-0 (General requirements) | 2017 ed. + AMD 1:2023 | Active | Ongoing minor amendments | Track for ATEX marking changes |
| IEC 60079-11 (Intrinsic safety Ex ia/ib) | 2011 ed. | Under revision | Energy limit calculations for hydrogen circuits may be revised | Review sensor circuit energy budgets |
| EN 13463-1 (Non-electrical ATEX equipment) | 2009 ed. | Active revision | Expanded scope for cryogenic valves and couplings | Review all non-electrical H₂ components |
| ISO 80079-36/37 (Non-electrical equipment) | 2016 ed. | Stable | Possible expansion to cryogenic fluid equipment | Monitor |

### 2.2 Hydrogen-Specific Standards

| Standard | Current Edition | Status | Anticipated Change | Design Impact |
|----------|----------------|--------|-------------------|---------------|
| ISO 26142 (H₂ detection apparatus) | 2010 ed. | Under revision (ISO/TC 197 WG 26) | Performance requirements for airborne H₂ sensors; cryogenic temperature range extension | May require re-qualification of selected sensors |
| ISO 14687 (H₂ fuel quality) | Part 2: 2012 | Active | Aircraft-specific H₂ purity addendum under development | Fuel quality specification may tighten |
| ISO/TC 197 WG 13 (Aircraft H₂ fueling) | New WG | Active drafting | First international standard for aircraft LH₂ ground fueling procedures and zone classification | Major input to ground operations procedures (ATA 28-00) |
| NFPA 2 (Hydrogen Technologies Code) | 2020 ed. | 2024 ed. in progress | Chapter 7 (Aircraft) expanded for LH₂ airport infrastructure; potential zone extent revisions for aircraft fill points | Review ground zone classification; coordinate with airport operators |
| SAE ARP 6464 (LH₂ aircraft fueling) | Draft | Active | First SAE standard specifically for LH₂ aircraft fueling (complements ISO/TC 197 WG 13) | Adoption may be mandated by EASA/FAA for CS-25 compliance |

### 2.3 ESD and Bonding Standards

| Standard | Current Edition | Status | Anticipated Change | Design Impact |
|----------|----------------|--------|-------------------|---------------|
| SAE ARP 1489 (Aircraft ESD) | Rev B | Under review | Possible lower resistance limits for composite aircraft; possible cryogenic fuel annex | All primary bonds designed to ≤ 0.1 Ω to anticipate this |
| SAE ARP 1216 (Aircraft bonding/grounding) | Rev A | Under review | Revised limits for CFRP structures; revised lightning current path requirements | Review composite insert bonding scheme |
| IEC 61340-5-1 (ESD control — electronics) | 2016 ed. | Under revision | Aviation sector annex expected; may set specific requirements for maintenance personnel in H₂ zones | PPE spec ESD-28-00 Section 6.2 covers anticipated draft requirements |
| NFPA 77 (Static electricity RP) | 2019 ed. | 2023 ed. published | Updated guidance for hydrogen systems; refueling bond resistance limits may change | Review GSE bonding procedure Section 5.1 of ESD-28-00 |

### 2.4 Airworthiness and Certification Standards

| Standard | Issuing Body | Status | Anticipated Change | Design Impact |
|----------|-------------|--------|-------------------|---------------|
| CS-25 Hydrogen Special Conditions | EASA | NPA in consultation (2025) | Formal CS-25 amendments for H₂ propulsion; replaces/formalizes SC-28-H2-001 | May require additional compliance demonstrations |
| FAA Issue Paper (H₂ propulsion) | FAA AIR-700 | Draft (2025) | US certification basis for H₂ aircraft; issue paper to become official guidance | Harmonization with EASA expected; dual compliance strategy required |
| AMC 25.981 revision (Fuel tank ignition) | EASA | Planned | Extension to cover H₂ fuel systems; ATEX zone classification may become AMC-referenced | Formal ATEX compliance may become mandatory via AMC |
| CS-E / FAR 33 (Engine certification) | EASA/FAA | Planned (H₂ fuel cell propulsion) | Fuel cell power plant certification basis; analogous to current CS-E provisions | ATA 71 fuel cell certification path |

### 2.5 Fuel Cell Specific Standards

| Standard | Current Edition | Status | Anticipated Change | Design Impact |
|----------|----------------|--------|-------------------|---------------|
| IEC 62282-3-100 (Stationary fuel cell systems) | 2019 ed. | Under revision | Aviation-relevant requirements being added by TC 105 | Review ATA 71 fuel cell stack safety requirements |
| SAE J2616 (Fuel cell systems for transportation) | 2017 ed. | Under review | Possible aviation-specific section; PEM fuel cell safety | ATA 71 fuel cell system design requirements |
| ISO 23273 (Fuel cell road vehicles — safety) | 2013 ed. | Active | Adapted principles being referenced in aviation; ATEX requirements for fuel cell bays | Fuel cell bay zone classification (ATA 71) |
| IEC 60068-2 series (Environmental testing) | Various | Active | Updates relevant to cryogenic environment testing for fuel cell components | ATA 71 environmental qualification |

---

## 3. Technology Watch

Beyond regulatory standards, the following technology areas are monitored for
potential impact on H₂/fuel cell infrastructure requirements:

### 3.1 Advanced Sensor Technologies

| Technology | Maturity | Potential Impact |
|------------|----------|-----------------|
| Nanomaterial H₂ sensors (graphene, metal oxide nanocomposites) | TRL 4–5 | Order-of-magnitude lower detection limits (< 10 ppm); faster response; lower power. May replace MEMS TCD baseline if qualified to ISO 26142 |
| Photoacoustic spectroscopy H₂ detection | TRL 4 | Highly selective, no cross-sensitivity; intrinsically safe (optical). Potential replacement for electrochemical backup sensor |
| Wireless sensor networks (WirelessHART / ZigBee ATEX) | TRL 6–7 | Simplifies sensor installation in remote zones; ATEX-certified wireless nodes now available for Zone 1; watch for aviation qualification |
| MEMS flow sensors for boil-off measurement | TRL 5–6 | Real-time boil-off measurement enables more precise Zone 2 boundary definition |

### 3.2 Digital Bonding Monitoring

| Technology | Maturity | Potential Impact |
|------------|----------|-----------------|
| Embedded bonding resistance sensors | TRL 5 | Continuous in-flight bond integrity monitoring; early warning of bond degradation. Architecture provision to be captured in bonding monitoring ICD (TBD) |
| Structural health monitoring (SHM) integration | TRL 5–6 | CFRP composite bond integrity correlated with SHM strain data; may reduce maintenance inspection frequency |

### 3.3 Hydrogen Storage Evolution

| Technology | Maturity | Potential Impact |
|------------|----------|-----------------|
| Type V composite pressure vessels (cryo-compressed H₂) | TRL 4–5 | Higher energy density; different boil-off profile; new zone classification considerations |
| Solid-state H₂ storage (metal hydrides) | TRL 3–4 | Minimal boil-off; potential zone classification simplification; very different thermal management |
| Slush hydrogen (SLH₂) | TRL 3 | Higher density; different thermal/pressure behaviour; new ATEX zone extents |

---

## 4. Action Register

| ID | Action | Trigger | Owner | Frequency |
|----|--------|---------|-------|-----------|
| FUT-001 | Review ATX-28-41-00 zone map against IEC 60079-10-1 next edition | Publication of new IEC 60079-10-1 | STK_SAF | Within 6 months of publication |
| FUT-002 | Review sensor selection (SEN-28-41-00) against revised ISO 26142 | Publication of revised ISO 26142 | STK_SAF | Within 6 months of publication |
| FUT-003 | Update ESD bonding spec (ESD-28-00-00) against revised SAE ARP 1489/1216 | Publication of revised ARP | STK_SAF | Within 6 months of publication |
| FUT-004 | Review all ATEX compliance against revised CS-25 H₂ Special Conditions | EASA NPA → AMC publication | STK_SAF + STK_SE | Within 3 months of AMC publication |
| FUT-005 | Assess ISO/TC 197 WG 13 aircraft fueling standard on ground ops procedures | Publication of new ISO standard | STK_SE | Within 6 months of publication |
| FUT-006 | Evaluate advanced sensor technologies (Section 3.1) for future block upgrade | Annual technology review | STK_SE | Annual — each lifecycle gate |
| FUT-007 | Review ATA 71 fuel cell zone classification against IEC 62282 revision | Publication of revised IEC 62282-3-100 | STK_SAF | Within 6 months of publication |
| FUT-008 | Maintain this document — add new standards as they emerge | Ongoing | STK_SAF | Minimum annual review |

---

## 5. Review History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-02-18 | STK_SAF | Initial draft |

---

**End of Document**
