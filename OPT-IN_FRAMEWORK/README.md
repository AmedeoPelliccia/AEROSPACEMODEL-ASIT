# OPT-IN_FRAMEWORK

**Aircraft TLI v2.1 Canonical Architecture**  
**Program:** AMPEL360 Q100  
**Authority:** ASIT (Aircraft Systems Information Transponder)

---

## Overview

The **OPT-IN_FRAMEWORK** provides the structural foundation for organizing ATA iSpec 2200-aligned content across the complete aircraft lifecycle (LC01–LC14). This framework supports the GenLM v2.1 Canonical architecture by establishing a deterministic, traceable directory structure for all aircraft systems, technologies, and operational artifacts.

---

## Framework Structure

The OPT-IN_FRAMEWORK is organized into five top-level domains:

### 1. **O-ORGANIZATIONS** (ATA 00–05)
Organizational and governance documentation including maintenance policies, operational procedures, and airworthiness limitations. Organized into two subdomains:
- **A — Authoritative** (ATA 00, 04, 05): Agency, regulatory, and legal-derived requirements
- **B — Business Enforcement** (ATA 01, 02, 03): Operator business policies and enforcement

### 2. **P-PROGRAMS** (ATA 06–12)
Program-level documentation including dimensions, servicing, and operational procedures. Organized into two subdomains:
- **P — Product Definition** (ATA 06, 08, 11): What the product is — dimensions, weight, markings
- **S — Service Instruction** (ATA 07, 09, 10, 12): How you handle it — lifting, towing, servicing

### 3. **T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS**
Comprehensive on-board systems organized into 15 technology subdomains covering ATA 20–80, 95–97. This is the largest domain containing all aircraft systems from airframe to propulsion to intelligence systems.

**Technology Subdomains:**
- **A-AIRFRAME_CABINS**: Structural components, cabins, furnishings
- **M-MECHANICS**: Flight controls, hydraulics, landing gear
- **E1-ENVIRONMENT**: Air conditioning, fire protection, environmental control
- **D-DATA**: Indicating, recording, maintenance systems
- **I-INFORMATION**: Information systems and avionics data
- **E2-ENERGY**: Electrical power and auxiliary power
- **E3-ELECTRICS**: Lighting and electrical panels
- **L1-LOGICS**: Reserved for logical control systems
- **L2-LINKS**: Navigation systems
- **C1-COMMS**: Communications systems
- **C2-CIRCULAR_CRYOGENIC_CELLS**: Hydrogen cryogenic fuel systems (Novel Technology)
- **I2-INTELLIGENCE**: AI/ML models and synthetic data (Novel Technology)
- **A2-AVIONICS**: Auto-flight and integrated modular avionics
- **O-OPERATING_SYSTEMS**: Multisystem integration
- **P-PROPULSION**: Power plant and propulsion systems (Novel Technology for fuel cells)

### 4. **I-INFRASTRUCTURES**
Ground support equipment, servicing infrastructure, and hydrogen supply chain. Organized into three subdomains:
- **M1 — Manufacturing Facilities** (ATA 85): Production lines, test rigs, assembly benches
- **M2 — Maintenance Environments** (ATA 08I, 10I, 12I): In-line, hangars, shops
- **O — Operations & Service Structures** (ATA 03I, ATA IN H₂ GSE): Airport facilities, fuel logistics, ground services

### 5. **N-NEURAL_NETWORKS**
AI governance, traceability systems, Digital Product Passport (DPP), and ledger systems. Organized into three subdomains:
- **D — Digital Thread & Traceability** (ATA 96): Ledger, DPP, hash chain, identifiers, schemas, audit packs
- **A — AI Governance & Assurance**: Certification pathway, ethics, human authority protocols, explainability
- **P\* — Program Reserved** (ATA 98): Expansion slot for future systems

---

## Novel Technology Subdomains

Three subdomains are designated as **Novel Technology** with full LC01–LC14 lifecycle activation:

### C2-CIRCULAR_CRYOGENIC_CELLS (Hydrogen Cryogenic Fuel Systems)
- **ATA Scope:** ATA 28 – Fuel
- **Special Conditions:** SC-28-H2-001, SC-28-CRYO-002
- **Criticality:** CRITICAL
- **Lifecycle:** Full LC01–LC14 activation
- **Key Technologies:** LH₂ storage, cryogenic handling, boil-off management, leak detection

### P-PROPULSION (Advanced Propulsion Systems)
- **ATA Scope:** ATA 71 – Power Plant, ATA 72 – Engine, ATA 73 – Engine Fuel & Control
- **Special Conditions:** SC-71-FUELCELL-001
- **Criticality:** CRITICAL
- **Lifecycle:** Full LC01–LC14 activation
- **Key Technologies:** Fuel cell stacks, balance of plant, thermal management, power conditioning

### I2-INTELLIGENCE (AI/ML Models)
- **ATA Scope:** ATA 95 – AI/ML Models, ATA 97 – Synthetic Data Validation
- **Special Conditions:** SC-AI-ASSURANCE-001, EU AI Act compliance
- **Criticality:** VARIES (based on DAL classification)
- **Lifecycle:** Full LC01–LC14 activation
- **Key Technologies:** Model training, inference, explainability, adversarial testing

ASIT governance (contracts, baselines, BREX rules) before posting.

---

## Integration with Lifecycle Registry

This framework is directly tied to the canonical lifecycle phase registry:

- **LC01–LC10 (PLM Phases):** Content rooted at `KDB/LM/SSOT/PLM`
- **LC11–LC14 (OPS Phases):** Content rooted at `IDB/OPS/LM`

Each ATA chapter directory within the framework maps to specific lifecycle packages as defined in:
- `lifecycle/LC_PHASE_REGISTRY.yaml` – Canonical phase definitions
- `lifecycle/T_SUBDOMAIN_LC_ACTIVATION.yaml` – Technology subdomain activation rules
- `lifecycle/TLI_GATE_RULEBOOK.yaml` – Gate logic and compliance rules

---

## Directory Conventions

Each domain directory contains:
- **README.md** – Domain scope and purpose
- **00_INDEX.md** – Structured index of ATA chapters within the domain
- **ATA subdirectories** – Individual ATA chapter content with `.gitkeep` for version control

---

## Compliance and Standards

The OPT-IN_FRAMEWORK is designed to support:
- **S1000D Issue 5.0** – Technical publication specification
- **ATA iSpec 2200** – Industry standard chapter organization
- **DO-178C** – Software considerations in airborne systems
- **DO-160** – Environmental conditions and test procedures
- **ARP4754A** – Development of civil aircraft and systems
- **ARP4761** – Safety assessment process
- **EU AI Act** – High-risk AI system compliance

---

## Usage

### For Content Creators
1. Identify the appropriate ATA chapter for your content
2. Navigate to the corresponding domain and subdirectory
3. Follow lifecycle activation rules from `lifecycle/T_SUBDOMAIN_LC_ACTIVATION.yaml`
4. Use BREX-driven instruction files from `.github/instructions/`

### For Reviewers
1. Review content placement within correct ATA chapter
2. Validate lifecycle phase alignment
3. Check gate compliance per `lifecycle/TLI_GATE_RULEBOOK.yaml`
4. Verify traceability to upstream baselines

### For Automation (GenLM Agents)
1. Reference this framework for deterministic content placement
2. Use lifecycle registry for phase validation
3. Execute gate checks before content generation
4. Maintain audit trail per BREX requirements

---

## Related Documentation

| Document | Path | Purpose |
|----------|------|---------|
| LC Phase Registry | `lifecycle/LC_PHASE_REGISTRY.yaml` | Canonical LC01–LC14 definitions |
| Gate Rulebook | `lifecycle/TLI_GATE_RULEBOOK.yaml` | Gate logic and compliance rules |
| T-Subdomain Activation | `lifecycle/T_SUBDOMAIN_LC_ACTIVATION.yaml` | Technology lifecycle activation |
| ATA 27 BREX Instructions | `.github/instructions/ata27_flight_controls.instructions.md` | Flight controls domain |
| ATA 28 BREX Instructions | `.github/instructions/ata28_fuel.instructions.md` | Fuel systems domain |
| ATA 95 BREX Instructions | `.github/instructions/ata95_ai_ml.instructions.md` | AI/ML systems domain |
| ATA 28 H2 BREX Instructions | `.github/instructions/ata28_h2_cryogenic.instructions.md` | H2 cryogenic domain |
| ATA 71 BREX Instructions | `.github/instructions/ata71_fuel_cell.instructions.md` | Fuel cell propulsion domain |

---

## Governance

- **Owner:** ASIT (Aircraft Systems Information Transponder)
- **Authority:** Program Configuration Manager
- **Change Control:** ECR/ECO via Configuration Control Board
- **Version Control:** Git-based with full audit trail

---

## Change History

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0.0 | 2026-02-12 | ASIT | Initial OPT-IN_FRAMEWORK creation for TLI v2.1 |
| 1.1.0 | 2026-02-17 | ASIT | Add P/I/N subdomain structure (P/S, M1/M2/O, D/A/P*) |
| 1.2.0 | 2026-02-17 | ASIT | Add O-ORGANIZATIONS subdomain split (A/B) |

---

*End of OPT-IN_FRAMEWORK README*
