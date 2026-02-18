# 04 — Machinery Process Safety

**Subdomain:** M1 / Machinery & Process Safety Operations  
**Lifecycle Phases:** LC07, LC10

---

## Scope

The **Machinery Process Safety** subdomain establishes safety requirements for machinery, equipment, and manufacturing processes in AMPEL360 Q100 production facilities, ensuring protection of personnel and prevention of accidents.

---

## Applicable Standards

### ISO 12100:2010 — Safety of Machinery — Risk Assessment
- **Scope:** General principles for risk assessment and risk reduction for machinery
- **Why it applies to M1:** Systematic approach to identify and mitigate machinery hazards in production lines
- **Evidence expected:** Machinery Risk Assessments, Hazard Register, Risk Reduction Measures

### ISO 13849-1:2015 — Safety-Related Parts of Control Systems — Functional Safety
- **Scope:** Safety requirements and guidance for design of safety-related parts of control systems (e.g., emergency stop circuits, light curtains, safety PLCs)
- **Why it applies to M1:** Ensures safety control systems achieve required performance levels (PLr)
- **Evidence expected:** Safety Circuit Diagrams, Performance Level Calculations, Validation Test Reports

### ISO 9241 — Ergonomics of Human-System Interaction — HMI
- **Scope:** Ergonomic principles for human-machine interface design
- **Why it applies to M1:** Ensures operator interfaces (HMIs, control panels) are intuitive and reduce human error
- **Evidence expected:** HMI Design Specifications, Usability Test Reports

---

## Controls & Checklists

Located in `controls/`:

- **Machine Guarding Checklist** — Verification that all machinery has appropriate guards and safety interlocks
  - Fixed guards (pinch points, rotating parts)
  - Interlocked guards (doors with safety switches)
  - Light curtains and presence sensors
  - Emergency stop buttons (accessible and functional)

- **Permit to Work Template** — Controlled access for high-risk maintenance or process operations
  - Hot work permits (welding, cutting, grinding)
  - Confined space entry permits
  - Electrical work permits
  - Cryogenic system work permits

- **Emergency Stop Validation Procedure** — Testing and validation of emergency stop circuits
  - Category 0/1 emergency stop per ISO 13850
  - Response time measurement
  - Periodic functional testing

---

## Interface Notes

### Lifecycle Phases
- **LC07 (QA & Process Compliance):** Safety system validation, functional safety testing
- **LC10 (Industrial & Supply Chain):** Production line design, machinery qualification

### OPT-IN Domains
- **M1/02_OHS_SAFETY_WORKPLACE:** Personnel safety coordination
- **M1/03_ENVIRONMENT_HAZMAT:** Hazardous process safety (hydrogen, cryogenics)

---

## Audit Questions

1. Are machinery risk assessments conducted per ISO 12100 for all production equipment?
2. Are safety-related control systems designed and validated per ISO 13849 (Performance Level requirements)?
3. Is all machinery equipped with appropriate guards and safety interlocks?
4. Are emergency stop circuits tested periodically and records maintained?
5. Are Permit to Work procedures in place for high-risk operations?
6. Are operators trained on machinery safety and emergency procedures?
7. Are HMIs designed and tested for usability and error prevention?

---

*End of 04_MACHINERY_PROCESS_SAFETY README*
