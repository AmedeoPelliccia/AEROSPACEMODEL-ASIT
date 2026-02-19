# Filing Strategy — AQUA-V Patent Portfolio

**Portfolio:** AQUA-V (QAPD + QAOS)  
**Authority:** ASIT / CCB  
**Governance Framework:** EU — GAIA-X Data Sovereignty / EASA / EU AI Act  
**Version:** 2.0 (revised: EU-first IP registry mandate)  
**Date:** 2026-02-19

---

## 0. EU Framework Mandate

> **BINDING CONSTRAINT:** All intellectual property registries for the AQUA-V portfolio must reside in the European Union.

This mandate follows directly from the AEROSPACEMODEL repository mission:
*"European-governed digital continuity infrastructure … aligned with EASA certification principles, GAIA-X data sovereignty, and the EU AI Act risk-based approach."*

Practical implications:
- The **primary IP registry** is the **European Patent Office (EPO)**, headquartered in Munich, Germany (EU).
- EU-wide protection is obtained via the **Unitary Patent (UP)** system under EU Regulation No 1257/2012, administered by the EPO and enforceable through the **Unified Patent Court (UPC)** (operational since June 2023).
- National patent offices of EU member states (INPI France, DPMA Germany, EPO) are acceptable secondary registries for validation states.
- The USPTO is a secondary jurisdiction accessible via PCT; it is **not** the primary registry.
- No IP right shall be registered exclusively with a non-EU authority without a co-pending EU registration.

---

## 1. Strategic Objective

Secure broad, defensible patent protection anchored in EU law for the AQUA-V architecture, with EU-registry primacy, covering:
- EU member states via Unitary Patent (18 states at UP launch, expanding)
- EPC validation states not yet in UP (e.g., CH, NO, TR) via traditional EP validation
- US and other jurisdictions as secondary markets via PCT → national phase

---

## 2. Jurisdiction Analysis

### 2.1 Primary Jurisdiction — EU / EPO

| Instrument | Registry | Coverage | Status |
|---|---|---|---|
| **Unitary Patent (UP)** | EPO — Munich, Germany 🇩🇪 (EU) | 18+ EU member states via single grant | ✅ Operational since June 2023 |
| **Traditional EP validation** | EPO + national IP offices (EU member states) | EPC contracting states not in UP; CH, NO, TR | ✅ Available |
| **UPC (Unified Patent Court)** | UPC Central Division (Paris/Munich/Milan) 🇫🇷🇩🇪🇮🇹 (EU) | Litigation for UP and opted-in EP patents | ✅ Operational since June 2023 |

**The EPO is the mandatory primary registry for all AQUA-V applications.**

### 2.2 Secondary Jurisdictions (via PCT)

| Jurisdiction | Rationale | Registry | Timeline |
|---|---|---|---|
| **United Kingdom** | Post-Brexit UKIPO; Airbus, Rolls-Royce, BAE key partners | UKIPO (London) | Month 31 PCT national phase |
| **United States** | FAA certification market; major quantum hardware vendors | USPTO (Alexandria, VA) | Month 30 PCT national phase |
| **Canada** | Bombardier; growing aerospace cluster | CIPO (Gatineau) | Month 30 PCT national phase |
| **Japan** | JAXA; Mitsubishi aerospace | JPO (Tokyo) | Month 30 PCT national phase |

---

## 3. Recommended Filing Path (EU-First)

### Phase 1 — EU Priority Establishment (Months 0–1)

**Step 1.1: Direct EP Application for P0 at EPO (Month 0)**
- File a European Patent Application directly at the EPO under EPC Art. 75
- Language of proceedings: English (one of the three EPO languages)
- Establishes the EU-based priority date under the Paris Convention
- EPO filing confers immediate designation in all 39 EPC contracting states
- Cost: ~€7,000–€10,000 (attorney fees + EPO official fees)
- **This is the priority-setting filing — all children claim this date**

**Step 1.2: EP Applications for C1.2 + C2.1 (Month 0–1)**
- C1.2 (Deterministic Reproducibility): strongest novel claim — file within 7 days of P0
- C2.1 (Resource Orchestrator): backed by existing QAOS.py implementation — file within 14 days
- Both filed at EPO, claiming internal priority from P0 where applicable

**Step 1.3: Unitary Patent Request**
- After EP grant, file Unitary Patent request at EPO within one month of grant mention in European Patent Bulletin
- Single annual renewal fee replaces 18+ national renewal fees
- UPC has exclusive jurisdiction for UP unless opt-out is filed

### Phase 2 — PCT Umbrella with EPO as ISA (Month 12)

**Step 2.1: PCT Application(s) claiming EP priority**
- File PCT application(s) within 12 months of Phase 1 EP filings
- **Designate EPO as International Searching Authority (ISA)** — ensures highest-quality ISR aligned with EPC standards
- Designates all PCT member states (~157 countries) for secondary markets
- 18-month publication from priority date
- Cost: ~€6,000–€9,000 per PCT filing

**Step 2.2: Recommended PCT structure**
- Single PCT for P0 with broadest claims → continuation strategy for children in US/JP/CA
- Separate PCTs for C1.2 and C2.1 if budget permits (stronger per-application protection)
- **All PCTs claim priority from Phase 1 EP applications**

### Phase 3 — Unitary Patent Grant + Non-EU National Phase (Month 30)

**Priority actions:**
1. **Unitary Patent request** at EPO → EU-wide protection in single step
2. **Traditional EP validation** in EPC states not participating in UP (CH, NO, TR)
3. **UK national phase** via UKIPO (separate post-Brexit)
4. **US national phase** via USPTO (secondary market)
5. **Other national phases** (CA, JP) as commercially justified

### Phase 4 — Divisionals and Continuation-in-Part (Ongoing, EU-first)

- C3.1 (LH₂ Tank Topology): file as EP divisional when BWB-H₂ structural design matures (EPO primary)
- C3.2 (Flight Energy Optimisation): file as EP divisional after first simulation validation
- C4.x: file as EP divisionals or independents; US continuations as secondary filings

---

## 4. Filing Vehicle Decision Matrix

| Factor | EP-First (✅ SELECTED) | PCT-Only | US Provisional First |
|---|---|---|---|
| **EU registry compliance** | ✅ Full — EPO is EU institution | ✅ EPO can be ISA | ❌ USPTO is non-EU |
| **GAIA-X sovereignty alignment** | ✅ EU-governed registry | Partial | ❌ Non-EU primary registry |
| **Cost at Month 0** | Medium (~€8–10k) | Medium (~€8k) | Low (~$3.5k) |
| **Coverage at Month 0** | 39 EPC states | Global (pending) | US only |
| **Unitary Patent eligibility** | ✅ Yes — direct EP → UP | ✅ Yes — PCT → EP → UP | ❌ Requires separate EP filing |
| **ISR quality** | EPO direct examination | EPO as ISA (best option) | USPTO (variable quality) |
| **Priority date for EU market** | ✅ Immediate | Deferred to national phase | ❌ Requires EP filing within 12 months |
| **Recommended for AQUA-V** | ✅ **PRIMARY** | ✅ Phase 2 umbrella | Secondary only |

**Decision: EP-first at EPO (EU registry) → Unitary Patent → PCT at month 12 (EPO as ISA) → non-EU national phases at month 30.**

---

## 5. EPO / Unitary Patent Specific Considerations

### Technical Effect Requirement (Art. 52 EPC)
AQUA-V claims must demonstrate a **technical effect** beyond the mental act or mathematical method:
- "Deterministic cryptographic evidence record enabling bit-exact reconstruction of quantum computation" — concrete technical effect
- "Latency-bounded criticality-aware backend selection enforcing a 5 ms response deadline" — measurable real-time technical constraint
- "Promotion gate conditioning SSOT write access on cryptographic evidence validity" — specific system behaviour

### Software/AI Claims (EPO Guidelines, G 1/19; T 0489/14)
- Method claims are allowable where they produce "a technical effect going beyond the normal physical interactions between a program and the computer"
- AQUA-V framing: "A computer-implemented method for controlling a hybrid quantum-classical processing system to generate a deterministic evidence record for use in aerospace certification…"
- Avoid: "A method of optimising a design problem" (reads as mathematical method per se)

### Unitary Patent Renewal Fees
- Single annual renewal fee paid to EPO replaces individual national fees in all UP states
- Fee scale based on the 4th to 20th year fees of the four EPO states with the highest national renewal fees
- Significant cost saving vs. validating in 18+ individual states

### UPC Opt-Out Strategy
- During the transitional period (7 years from June 2023), traditional EP patents can be opted out of UPC jurisdiction
- **For AQUA-V, do NOT opt out** — UPC provides uniform EU-wide enforcement with central litigation, aligning with EU governance mandate

---

## 6. EU AI Act Alignment

As an AI/ML system (ATA 95 domain), AQUA-V components that qualify as **high-risk AI systems** under EU AI Act Annex III must have their technical documentation registered in the EU. Patent prosecution at the EPO ensures that:
- The invention disclosure is lodged with an EU institution
- The technical claims are publicly registered in the European Patent Register (EU-accessible)
- Compliance artefacts can reference the EP application number as a public EU record

---

## 7. Freedom-to-Operate (FTO) in the EU

**Key risks identified:**
1. Siemens / PTC digital twin patents (EP registered) — differentiate on quantum computation + cryptographic evidence binding
2. Airbus Group SE aerospace optimisation EP patents — differentiate on hybrid QUBO with cryogenic constraints and deterministic seeding
3. IBM / Google quantum computing EP patents — avoid apparatus-agnostic method claims; tie to specific system architecture

**EU FTO clearance (EPO register search + national validation search) must be completed before UP request is filed.**

---

## 8. EP Application Filing Checklist

Each EP application at the EPO must include:
1. Request for grant (EPO Form 1001)
2. Description in English matching the Invention Disclosure
3. At least one claim (formal claims per EPC Rule 43)
4. Abstract
5. Drawings (block diagrams of AQUA-V architecture)
6. Designation of inventor(s) (EPO Form 1002)
7. Priority document (if claiming internal priority from earlier EP application)
8. Payment of filing fee, search fee, and designation fee

---

*All filing decisions require CCB approval per BREX rule BL-002.*  
*EU framework mandate is non-waivable. Any request to file exclusively with a non-EU registry must be escalated to STK_CM.*
