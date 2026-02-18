# 05 — Warehouse Inventory

**Subdomain:** M1 / Warehouse, Inventory & Logistics  
**Lifecycle Phases:** LC10, LC12

---

## Scope

The **Warehouse Inventory** subdomain establishes requirements for material receiving, storage, inventory management, and traceability in AMPEL360 Q100 production facilities. Special emphasis is placed on critical parts traceability, calibration management, and material handling for cryogenic and hydrogen systems.

---

## Applicable Standards

### Traceability (RFID/QR Tagging)
- **Scope:** Unique identification and tracking of parts, materials, and assemblies throughout production and lifecycle
- **Why it applies to M1:** Critical for aerospace traceability requirements (material certs, heat lots, serial numbers)
- **Evidence expected:** Serialization Register, RFID/QR Database, Traceability Matrix
- **Special Requirements:**
  - Batch traceability for hydrogen storage materials (aluminum alloys, composites)
  - Serial number tracking for fuel cell stacks and power electronics
  - Material certification tracking (mill certs, test reports)

### ISO/IEC 17025 — Calibration & Metrology (where applicable)
- **Scope:** Competence requirements for testing and calibration laboratories
- **Why it applies to M1:** Measurement and test equipment (MTE) used for inspection and quality control must be calibrated
- **Evidence expected:** Calibration Certificates, Calibration Schedule, MTE Register
- **Equipment Examples:**
  - Cryogenic temperature sensors
  - Pressure gauges (hydrogen systems)
  - Dimensional inspection equipment (CMM, calipers)
  - Leak detectors

---

## Controls & Checklists

Located in `controls/`:

- **Receiving Inspection Procedure** — Incoming material and part inspection checklist
  - Verify part number, quantity, and material certification
  - Inspect for damage or contamination
  - RFID/QR tag assignment
  - Quarantine non-conforming materials

- **FIFO/FEFO Rules** — First-In-First-Out (FIFO) and First-Expired-First-Out (FEFO) inventory rotation
  - Shelf life management for adhesives, sealants, and chemicals
  - Lot rotation for composite materials
  - Date code tracking

- **Stock Accuracy KPI Dashboard** — Inventory accuracy metrics and cycle counting
  - Cycle count schedule
  - Inventory discrepancy tracking
  - Stock accuracy targets (>99% for critical parts)

---

## Interface Notes

### Lifecycle Phases
- **LC10 (Industrial & Supply Chain):** Primary activation — material procurement, supplier coordination, inventory setup
- **LC12 (Continued Airworthiness & MRO):** Spare parts inventory, traceability continuity

### OPT-IN Domains
- **T/C2-CIRCULAR_CRYOGENIC_CELLS:** LH₂ tank material traceability
- **T/P-PROPULSION:** Fuel cell component traceability
- **I/M2-MAINTENANCE_ENVIRONMENTS:** Spare parts coordination

---

## Audit Questions

1. Are all critical parts and materials uniquely identified with RFID/QR tags or serial numbers?
2. Is material traceability maintained from receiving through installation (batch, heat lot, certification)?
3. Are all measurement and test equipment (MTE) calibrated per schedule with valid certificates?
4. Are FIFO/FEFO rules enforced for shelf-life-limited materials?
5. Is stock accuracy monitored with cycle counting and corrective actions?
6. Are receiving inspection procedures followed for all incoming materials?
7. Are material certifications (mill certs, test reports) retained and traceable to installed parts?

---

*End of 05_WAREHOUSE_INVENTORY README*
