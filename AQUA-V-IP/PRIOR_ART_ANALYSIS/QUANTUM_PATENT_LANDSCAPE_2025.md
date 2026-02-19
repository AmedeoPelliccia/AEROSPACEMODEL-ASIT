# Quantum Patent Landscape 2025

**Portfolio:** AQUA-V  
**Date:** 2026-02-19  
**Scope:** Global quantum technology patent landscape; EU quantum IP strategy  
**Sources:** EuroQuIC 2025; DLA Piper 2025; EPO patent register; Espacenet

---

## 1. Global Quantum Patent Landscape Overview

*Based on: EuroQuIC "A Portrait of The Global Patent Landscape in Quantum Technologies" (2025)*  
*Source: [euroquic.org/wp-content/uploads/2025/02/A-Portrait-of-The-Global-Patent-Landscape-in-Quantum-Technologies-2025.pdf](https://www.euroquic.org/wp-content/uploads/2025/02/A-Portrait-of-The-Global-Patent-Landscape-in-Quantum-Technologies-2025.pdf)*

### 1.1 Filing Volume

| Category | 2024 Global Quantum Patent Filings (est.) | Key Filers |
|---|---|---|
| Quantum hardware (QPU, qubit) | ~4,200 | IBM, Google, IonQ, D-Wave, Quantinuum |
| Quantum algorithms / software | ~1,800 | IBM, Google, 1QBit, QC Ware |
| Quantum sensing | ~2,100 | Honeywell, Bosch, multiple European startups |
| Quantum communications / QKD | ~1,500 | ID Quantique, Toshiba, Chinese nationals |
| Quantum + AI hybrid | ~600 | IBM, Fujitsu, several European academic spinouts |
| **Quantum + aerospace applications** | **~120** | Boeing, Airbus, DLR, Lockheed Martin, D-Wave |

**Key observation:** The quantum + aerospace application space has only ~120 global filings as of 2024 — a thin landscape. AQUA-V has ample room for novel claims.

### 1.2 EU Filing Position

| Region | % of Global Quantum Filings | Trend |
|---|---|---|
| USA | 35% | Stable |
| China | 30% | Growing rapidly |
| **EU/EPC** | **18%** | **Growing; EuroQuIC programme driving EU filing** |
| Japan | 10% | Stable |
| South Korea | 5% | Growing |
| Other | 2% | — |

**EU strategic note:** EuroQuIC aims to increase EU quantum patent share. Filing AQUA-V at EPO positions the portfolio within EU quantum IP strategy.

---

## 2. Key Competitor Patent Families

### 2.1 IBM Quantum (US + EP)

| Patent Family | Scope | Relevance to AQUA-V |
|---|---|---|
| Hybrid quantum-classical computation methods | Variational algorithms; error mitigation; circuit execution | Claims apparatus and method for QPU execution — avoid apparatus-agnostic claims |
| Quantum job scheduling | Queue management; job priority | No safety criticality classification; no hard deadline enforcement; AQUA-V C2.1 differentiated |
| Quantum circuit compiler optimisation | Circuit depth reduction; noise mitigation | Circuit compilation only; no QUBO aerospace encoding; no evidence records |

**AQUA-V differentiation from IBM portfolio:** IBM patents focus on hardware and algorithm infrastructure. AQUA-V claims the *application layer* with aerospace-specific constraints, deterministic evidence records, and certification integration — a different layer of the stack.

### 2.2 D-Wave Systems (US + EP)

| Patent Family | Scope | Relevance to AQUA-V |
|---|---|---|
| QUBO formulation for industrial optimisation | Binary variable encoding; penalty methods; annealing | Generic QUBO — no aerospace constraints; no deterministic seeding; no evidence chain |
| Quantum annealing hardware | Qubit topology; coupling; flux biasing | Hardware patents — not relevant to AQUA-V software/method claims |
| Aerospace scheduling via annealing | Flight scheduling; crew rostering | Scheduling only; no design topology; no cryogenic constraints |

**AQUA-V differentiation from D-Wave portfolio:** D-Wave's scheduling applications are operational only (not design-time). D-Wave's QUBO patents cover generic formulations without aerospace-specific constraint types.

### 2.3 Airbus SE (EP + US)

| Patent Family | Scope | Relevance to AQUA-V |
|---|---|---|
| Digital twin for aircraft design | Structural DT; aerodynamic DT; manufacturing DT | No quantum computation; no QUBO; no cryptographic evidence; DT only |
| Hydrogen propulsion system design | LH₂ tank; fuel cell integration; ATA 28 | Structural design methods only — no quantum; C3.1 must differentiate from any structural topology claims |
| Generative design for aerospace structures | AI-assisted structural optimisation | Classical AI only; no quantum; no certification evidence chain |

**Key risk:** Airbus may have pending EP patent applications on LH₂ structural integration that overlap with C3.1 claim scope. Priority EP filing for C3.1 should be expedited once BWB-H₂ design matures.

---

## 3. Prosecution Strategy Implications

### 3.1 EPO Examination Practice (Quantum Claims)

Based on DLA Piper 2025 analysis (*[dlapiper.com/en-us/insights/publications/intellectual-property-news/2025/patenting-quantum-computing-challenges-trends-and-future-prospects](https://www.dlapiper.com/en-us/insights/publications/intellectual-property-news/2025/patenting-quantum-computing-challenges-trends-and-future-prospects)*):

| Issue | EPO Practice | AQUA-V Strategy |
|---|---|---|
| Mathematical method exception (Art. 52(2)(a) EPC) | QUBO formulation per se = mathematical method → not allowable | Frame claims as "method for controlling a quantum processing system to…" with concrete technical effect |
| Technical effect requirement (T 0258/03) | Claims must achieve technical effect beyond normal program-computer interaction | "Deterministic evidence record enabling aerospace certification audit" = concrete technical effect |
| Inventive step for software claims (Art. 56 EPC) | Must show non-obvious technical contribution | "Two-expert problem" argument: requires quantum + aerospace + certification expertise simultaneously |
| Abstract idea rejection (equivalent to Alice at EPO) | EPO applies T 0489/14 Comvik approach | Ensure all claim elements contribute to technical solution; no purely mental steps |

### 3.2 Claim Drafting Recommendations (EU-First)

1. **Lead independent claims** with "A computer-implemented method for controlling a quantum processing system to generate a deterministic evidence record…" — grounds in concrete technical implementation
2. **Include EU regulatory references** in dependent claims (EASA CS-25, EU AI Act Article 14, eIDAS) — demonstrates technical alignment with EU legal framework, relevant to EU market relevance
3. **Use "EPO three-part claim format"** for method claims: preamble (known state) + characterising portion (novel elements) per EPC Rule 43(1)(b)
4. **File in English** at EPO (one of the three official languages) — avoid translation costs and errors at filing stage

---

## 4. Freedom-to-Operate Risk Assessment

| Risk | Severity | Probability | AQUA-V Mitigation |
|---|---|---|---|
| IBM QPU method patents block apparatus-agnostic quantum method claims | High | Medium | Tie all method claims to specific system architecture (QPU + evidence record + SSOT) |
| Airbus LH₂ structural EP patents block C3.1 | High | Low–Medium | Expedite C3.1 EP divisional filing; differentiate on QUBO encoding + evidence record |
| D-Wave QUBO formulation patents block C1.1 | Medium | Low | D-Wave QUBO patents are generic; C1.1 aerospace-specific constraints are not covered |
| Autodesk certification DT patents block C1.3/C2.2 | Medium | Low–Medium | Autodesk = classical simulation; C1.3/C2.2 = quantum provenance — different technical problems |
| Google/IBM quantum error correction patents | Low | Low | AQUA-V does not claim error correction mechanisms |

---

*This landscape document is for strategic planning only. It does not constitute a formal FTO opinion.*  
*Formal FTO analysis should be conducted by a European Patent Attorney (EPA) using Espacenet, Derwent Innovation, and EPO file inspection.*  
*EU framework mandate: All patent filings targeting EU market protection must be filed at EPO as the primary registry.*
