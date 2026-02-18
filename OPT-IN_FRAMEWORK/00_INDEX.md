# OPT-IN_FRAMEWORK Index

**AIRCRAFT TLI v2.1 Canonical Architecture**

---

## Domain Structure

| Domain | Code | Path | ATA Scope | Description |
|--------|------|------|-----------|-------------|
| **O-ORGANIZATIONS** | O | `O-ORGANIZATIONS/` | ATA 00–05 | Organizational and governance documentation |
| **P-PROGRAMS** | P | `P-PROGRAMS/` | ATA 06–12 | Program-level procedures and servicing |
| **T-TECHNOLOGIES** | T | `T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS/` | ATA 20–80, 95–97 | Complete on-board systems (15 subdomains) |
| **I-INFRASTRUCTURES** | I | `I-INFRASTRUCTURES/` | Infrastructure | Ground support and supply chain |
| **N-NEURAL_NETWORKS** | N | `N-NEURAL_NETWORKS/` | Governance | AI governance and traceability |

---

## Technology Subdomains (T-TECHNOLOGIES)

| Subdomain | Code | ATA Chapters | Technology Type |
|-----------|------|--------------|-----------------|
| Airframe & Cabins | A | 20, 25, 44, 50–57 | Standard |
| Mechanics | M | 27, 29, 32 | Standard |
| Environment | E1 | 21, 26, 30, 35–38, 47 | Standard |
| Data | D | 31, 45 | Standard |
| Information | I | 46 | Standard |
| Energy | E2 | 24, 49 | Standard |
| Electrics | E3 | 33, 39 | Standard |
| Logics | L1 | Reserved | Future |
| Links | L2 | 34 | Standard |
| Comms | C1 | 23 | Standard |
| **Cryogenic Cells** | **C2** | **28** | **Novel Technology** ⭐ |
| **Intelligence** | **I2** | **95, 97** | **Novel Technology** ⭐ |
| Avionics | A2 | 22, 42 | Standard |
| Operating Systems | O | 40 | Standard |
| **Propulsion** | **P** | **60–61, 71–80** | **Novel Technology** ⭐ |

⭐ **Novel Technology** = Full LC01–LC14 lifecycle activation with Special Conditions

---

## Organization Subdomains (O-ORGANIZATIONS)

| Subdomain | Code | ATA Chapters | Description |
|-----------|------|--------------|-------------|
| Authoritative | **A** | 00, 04, 05 | Agency, regulatory, and legal-derived requirements |
| Business Enforcement | **B** | 01, 02, 03 | Operator business policies and enforcement |

---

## Program Subdomains (P-PROGRAMS)

| Subdomain | Code | ATA Chapters | Description |
|-----------|------|--------------|-------------|
| Product Definition | **P** | 06, 08, 11 | What the product is — dimensions, weight, markings |
| Service Instruction | **S** | 07, 09, 10, 12 | How to handle it — lifting, towing, servicing |

---

## Infrastructure Subdomains (I-INFRASTRUCTURES)

| Subdomain | Code | Categories | Description |
|-----------|------|------------|-------------|
| Manufacturing Facilities | **M1** | ATA 85 | Production lines, test rigs, assembly benches |
| Maintenance Environments | **M2** | ATA 08I, 10I, 12I | In-line, hangars, shops |
| Operations & Service Structures | **O** | ATA 03I, ATA IN H2 GSE | Airport facilities, fuel logistics, ground services |

---

## Neural Network Subdomains (N-NEURAL_NETWORKS)

| Subdomain | Code | ATA / Scope | Description |
|-----------|------|-------------|-------------|
| Digital Thread & Traceability | **D** | ATA 96 | Ledger, DPP, hash chain, identifiers, schemas, audit packs |
| AI Governance & Assurance | **A** | Governance | Certification pathway, ethics, human authority protocols, explainability |
| Program Reserved | **P*** | ATA 98 | Expansion slot for future systems |

---

## Quick Navigation

### Organizational & Governance
- [O-ORGANIZATIONS README](O-ORGANIZATIONS/README.md)

### Programs
- [P-PROGRAMS README](P-PROGRAMS/README.md)

### On-Board Systems
- [T-TECHNOLOGIES README](T-TECHNOLOGIES_AMEDEOPELLICCIA-ON_BOARD_SYSTEMS/README.md)

### Infrastructure
- [I-INFRASTRUCTURES README](I-INFRASTRUCTURES/README.md)

### Neural Networks & AI Governance
- [N-NEURAL_NETWORKS README](N-NEURAL_NETWORKS/README.md)

### Engineering SSOT Front-End
- [ENGINEERING_SSOT README](ENGINEERING_SSOT/README.md)
- [SSOT Registry Browser (front-end)](ENGINEERING_SSOT/index.html)

---

## Total Coverage

- **5** Top-Level Domains
- **15** Technology Subdomains within T-TECHNOLOGIES
- **2** Organization Subdomains within O-ORGANIZATIONS (A, B)
- **2** Program Subdomains within P-PROGRAMS (P, S)
- **3** Infrastructure Subdomains within I-INFRASTRUCTURES (M1, M2, O)
- **3** Neural Network Subdomains within N-NEURAL_NETWORKS (D, A, P*)
- **75+** ATA Chapter Directories
- **3** Novel Technology Designations

---

*Refer to main [OPT-IN_FRAMEWORK README](README.md) for detailed information.*
