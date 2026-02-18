# 06 — Additive Manufacturing

**Subdomain:** M1 / Additive Manufacturing / On-Demand 3D Print  
**Lifecycle Phases:** LC04, LC06, LC07, LC10

---

## Scope

The **Additive Manufacturing** subdomain establishes quality, process control, and safety requirements for on-demand 3D printing of aerospace parts used in AMPEL360 Q100 production. This includes metal additive manufacturing (AM) for fuel system components, brackets, and lightweight structures, as well as polymer AM for tooling and fixtures.

---

## Applicable Standards

### AM Quality Gate Criteria
- **Scope:** Quality gates for additive manufacturing processes to ensure part integrity and repeatability
- **Why it applies to M1:** AM parts used in aerospace applications require rigorous process control and qualification
- **Evidence expected:** AM Process Specification, Build Parameter Records, Post-Processing Procedures
- **Quality Gates:**
  - Design for AM (DfAM) review — optimize part geometry for AM process
  - Powder quality verification — material certification, particle size distribution, moisture content
  - Build parameter approval — laser power, scan speed, layer thickness
  - Build monitoring — real-time anomaly detection (thermal imaging, acoustic)
  - Post-processing validation — heat treatment, HIP (Hot Isostatic Pressing), machining
  - Non-destructive testing (NDT) — CT scan, ultrasonic, dye penetrant
  - Dimensional inspection — verify final part geometry
  - Mechanical testing — tensile, fatigue, impact (for qualification)

### Material Batch Traceability
- **Scope:** Traceability of AM powder batches from procurement through part production
- **Why it applies to M1:** Critical for aerospace traceability requirements and failure investigation
- **Evidence expected:** Powder Batch Register, Material Certifications, Powder Recycling Log
- **Traceability Requirements:**
  - Powder lot number and certification
  - Build job number and date
  - Part serial number
  - Powder recycling history (max 5 cycles typical)

### NADCAP Special Process Qualification
- **Scope:** NADCAP accreditation for additive manufacturing as a special process (where applicable)
- **Why it applies to M1:** In aerospace, AM may require NADCAP special process qualification depending on the process and application (e.g., metal AM for flight-critical parts)
- **Evidence expected:** NADCAP Accreditation Certificate, Operator Qualification Records, Process Qualification Test Results
- **Note:** NADCAP requirements vary by application and customer contract. Not all AM processes require NADCAP, but flight-critical metal AM typically does.

---

## Controls & Checklists

Located in `controls/`:

- **Build Record Template** — Documentation for each AM build job
  - Build job number and date
  - Part numbers and quantities
  - Powder batch numbers and certifications
  - Build parameters (machine settings)
  - Build log (start/stop times, anomalies)
  - Post-processing records (heat treatment, machining)
  - Inspection results (dimensional, NDT)

- **Powder Handling Safety Procedure** — Safe handling of metal powders to prevent fire, explosion, and inhalation hazards
  - Inert atmosphere handling (nitrogen or argon)
  - Dust collection and filtration
  - Explosion-proof equipment
  - Personal protective equipment (respirators, gloves)
  - Powder storage and disposal

---

## Interface Notes

### Lifecycle Phases
- **LC04 (Design Definition):** DfAM review, part qualification
- **LC06 (Integration & Test):** AM part testing and validation
- **LC07 (QA & Process Compliance):** AM process qualification, operator training, quality audits
- **LC10 (Industrial & Supply Chain):** AM machine procurement, powder supply chain

### OPT-IN Domains
- **T/C2-CIRCULAR_CRYOGENIC_CELLS:** AM brackets and supports for LH₂ tanks
- **T/P-PROPULSION:** AM fuel cell bipolar plates and heat exchangers (potential future application)
- **M1/01_QUALITY:** AM quality gate integration with QMS

---

## Audit Questions

1. Are AM quality gates defined and enforced for all AM parts?
2. Is material batch traceability maintained from powder procurement through part installation?
3. Are AM build parameters validated and controlled (process specification)?
4. Are AM parts inspected per quality plan (dimensional, NDT)?
5. Are operators trained and qualified for AM equipment and processes?
6. Are powder handling safety procedures followed (inert atmosphere, PPE, dust control)?
7. Is NADCAP accreditation obtained for AM special processes (if required by contract)?
8. Are build records maintained for all AM jobs with full traceability?

---

*End of 06_ADDITIVE_MANUFACTURING README*
