# AQUA-V v1.0 — Foundational Architecture Paper

**Title:** AQUA-V: A Hybrid Quantum–Classical Architecture for Deterministic,
Governance-Bound Aerospace Product Development and Operations

**Author:** Amedeo Pelliccia  
**Affiliation:** AEROSPACEMODEL / ASIT  
**Version:** 1.0.0  
**Date:** 2026-02-19  
**Status:** Definitive Edition — Canonical Reference  
**Repository:** <https://github.com/AmedeoPelliccia/AEROSPACEMODEL>

> **How to Cite:**
> Pelliccia, A. (2026). *AQUA-V v1.0: Foundational Architecture for
> Quantum-Assisted Aerospace Product Development and Operations.*
> AEROSPACEMODEL Repository.
> <https://github.com/AmedeoPelliccia/AEROSPACEMODEL/blob/main/AQUA-V-IP/AQUA_V_FOUNDATIONAL_PAPER_v1.0.md>

---

## Abstract

We present AQUA-V (Artificial Quantum Unified Architectures Venture), a
formally governed hybrid architecture that integrates quantum-assisted
computation into safety-critical aerospace product development and operations.
The central contribution is a mechanism for **deterministic, bit-reproducible
quantum computation records** — enabling use of quantum solvers within
certification frameworks (EASA CS-25, DO-178C, ARP4754A) that mandate
auditable, traceable design decisions.

AQUA-V comprises two coupled subsystems: **QAPD** (Quantum Accelerated Product
Development) for design-time hybrid optimisation, and **QAOS** (Quantum Assisted
Operation Services) for criticality-aware operational scheduling. Both
subsystems share a common Digital Thread governed by BREX decision rules,
aligned with GAIA-X data sovereignty principles, and compliant with the EU AI
Act (Regulation (EU) 2024/1689).

We introduce four canonical concepts that together constitute the AQUA-V
architecture: the **Deterministic Governance Tuple**, the **Hybrid
Discrete–Continuous Encoding Layer**, the **Certification-Bound Quantum
Pipeline**, and the **Operational Evidence Ledger**.

---

## 1. Formal Problem Definition

### 1.1 The Dual Incompatibility

Quantum computation offers asymptotic advantages for combinatorial
optimisation problems that dominate aerospace design — structural topology
selection, multi-objective aerodynamic optimisation, and fleet maintenance
scheduling. However, two fundamental incompatibilities prevent direct adoption
in certified aerospace systems:

**Incompatibility I — Non-determinism:** A quantum circuit C executed on
hardware H produces a probability distribution P(x) over measurement outcomes.
Two executions of C on H with identical inputs return different samples. This
violates the reproducibility requirements of DO-178C § 6.4 (output
consistency) and ARP4754A § 5.3 (traceability of design decisions).

**Incompatibility II — Context blindness:** Generic quantum optimisation
algorithms (QAOA, VQE, quantum annealing) operate on abstract QUBO instances
with no representation of domain-specific physical constraints. They cannot
natively encode cryogenic temperature bounds, material compatibility matrices,
or DAL-classified failure probability thresholds that characterise
safety-critical aerospace design spaces.

### 1.2 Problem Statement

*Given:*
- A set of design parameters **d** ∈ ℝ^p × {0,1}^q
- A set of aerospace domain constraints **C** = {C_structural, C_thermal, C_dal, C_geometric}
- A certification framework **F** requiring: reproducibility, traceability, auditability
- An operational environment with latency and criticality requirements

*Required:*
A computation architecture A such that:
1. A encodes (**d**, **C**) into a solvable optimisation instance
2. A executes the computation with a mechanism guaranteeing exact reconstruction
   of the top-k ranked solutions from a compact evidence record
3. A classifies operational workloads by safety criticality and enforces
   hard deadline constraints
4. A maintains a cryptographically linked chain from design decisions to
   operational digital twin state
5. Every transformation in A is governed by a BREX decision rule and logged in
   an append-only audit record

---

## 2. Terminology — Canonical Definitions

The following terms are introduced as stable coined terminology for the AQUA-V
field. Authors and implementers who build on this architecture should adopt
these definitions to enable coherent attribution and citation.

---

### 2.1 Deterministic Governance Tuple (DGT)

**Definition:** A five-element record

```
DGT = (s, H_in, v, R_k, σ)
```

where:
- **s** ∈ ℤ≥0 is the global seed, derived as the first 64 bits of
  SHA-256(serialise(**d**) ‖ ISO-8601 timestamp)
- **H_in** = SHA-256(serialise(**d**, **C**, config)) is the input dataset hash
- **v** is the solver version string (quantum SDK + backend + circuit compiler,
  e.g., `"qiskit-aer==0.15.1+ibm-runtime==0.28.0"`)
- **R_k** = (r_1, r_2, …, r_k) is the ordered list of top-k solution vectors
  returned by the solver when seeded with s
- **σ** = ECDSA-P384(private_key, SHA-256(s ‖ H_in ‖ v ‖ SHA-256(R_k))) is
  the digital signature binding all fields

**Property:** Given DGT, any auditor possessing the solver at version v can
reproduce R_k from s and H_in without access to the original hardware.

**Lifecycle binding:** Each DGT is tagged with the lifecycle phase (LC03–LC08)
at which it was generated and promoted to SSOT only after regulatory review.

---

### 2.2 Hybrid Discrete–Continuous Encoding Layer (HDCEL)

**Definition:** A mapping

```
φ: ℝ^p × {0,1}^q → {0,1}^n
```

that encodes a mixed-type design parameter vector (**d_c** ∈ ℝ^p, **d_b** ∈
{0,1}^q) into a pure binary vector **x** ∈ {0,1}^n suitable for QUBO
formulation, via:
1. **Binary encoding of continuous variables:** d_c[i] → b_i ∈ {0,1}^(B_i)
   using a configurable-precision fixed-point representation with B_i bits
2. **Passthrough of binary variables:** d_b[j] → x[offset_j]
3. **Aerospace constraint penalty injection:** For each constraint c ∈ **C**,
   a quadratic penalty term λ_c · P_c(**x**) is added to the QUBO objective

**Aerospace constraint schema:** The HDCEL is parameterised by an
`AerospaceConstraintSchema` that maps S1000D Data Module parameters to QUBO
penalty coefficients. Current schema version: `ACS-v1.0`. Penalty families:

| Penalty Family | Physical Basis | Applicable Domain |
|---|---|---|
| `cryogenic_thermal` | LH₂ at −253°C; material embrittlement bounds | ATA 28, C3.1 |
| `h2_material_compat` | Hydrogen compatibility galvanic matrix | ATA 28, C3.1 |
| `dal_prob_bound` | ARP4761 failure probability thresholds | All DAL A/B systems |
| `geometric_packaging` | BWB internal volume; CG envelope | C3.1, C3.2 |
| `eu_reach_compliance` | EU REACH Annex XVII substance constraints | C4.1 |

**Novelty:** The HDCEL is not generic QUBO encoding. The penalty schema
creates a direct, machine-readable linkage between S1000D-governed design
data and the objective function of the quantum solver.

---

### 2.3 Certification-Bound Quantum Pipeline (CBQP)

**Definition:** A computation pipeline

```
CBQP = (Φ, Γ, Δ, Ψ)
```

where:
- **Φ** is the HDCEL encoding step (Section 2.2)
- **Γ** is the solver execution step, which: (a) initialises the quantum
  circuit sampler with seed s from DGT, (b) executes the circuit on the
  selected backend, (c) collects measurement statistics
- **Δ** is the DGT generation step (Section 2.1)
- **Ψ** is the SSOT promotion gate, which: (a) validates the DGT digital
  signature, (b) checks lifecycle phase eligibility, (c) invokes human
  oversight hook for DAL A/B results, (d) writes the DGT to the Operational
  Evidence Ledger

**Invariant:** A CBQP is *valid* if and only if:
- Every step in (Φ, Γ, Δ, Ψ) has a corresponding BREX rule authorising it
- The DGT produced by Δ is verifiable against the inputs of Φ
- The OEL entry written by Ψ is append-only and references the triggering
  design session identifier

**Distinction from classical pipelines:** Classical design pipelines (MBSE,
PLM) do not produce DGTs. They record human-authored design decisions but
cannot guarantee bit-level reconstruction of computational results from a
compact evidence record.

---

### 2.4 Operational Evidence Ledger (OEL)

**Definition:** An append-only, cryptographically linked sequence

```
OEL = {DGT_i, τ_i, ref_i}_{i=1}^{N}
```

where:
- **DGT_i** is the Deterministic Governance Tuple for the i-th computation
- **τ_i** = SHA-256(DGT_i ‖ DGT_{i-1} ‖ τ_{i-1}) is the chain hash
  linking entry i to entry i−1 (τ_0 = 0^256)
- **ref_i** is the reference to the SSOT design record or digital twin state
  that was updated as a result of this computation

**Properties:**
1. **Append-only:** Entries cannot be deleted or modified; only new entries
   can be appended
2. **Chain integrity:** Tampering with any DGT_i invalidates all τ_j for j > i
3. **EU residence:** The OEL is stored on GAIA-X sovereign EU infrastructure;
   no replication to non-EU jurisdictions without explicit CCB approval
4. **Retention:** Minimum 7 years per EASA CS-25 Amendment 27 record-keeping
   requirements

**Distinction from blockchain:** The OEL does not require decentralised
consensus. It is a governed, authority-controlled ledger under ASIT jurisdiction,
auditable by EASA-authorised Design Organisation Approval (DOA) holders.

---

## 3. Architecture — QAPD + QAOS = AQUA-V

```
┌─────────────────────────────────────────────────────────────────────┐
│                         AQUA-V Architecture                         │
│                                                                     │
│  ┌─────────────────────────────┐  ┌──────────────────────────────┐  │
│  │  QAPD — Design Time         │  │  QAOS — Operations           │  │
│  │                             │  │                              │  │
│  │  Input: design params d     │  │  Input: operational event e  │  │
│  │      ↓ HDCEL (φ)            │  │      ↓ QW classification     │  │
│  │  QUBO instance Q(d,C)       │  │  Workload class QW1–QW4      │  │
│  │      ↓ CBQP (Γ)             │  │      ↓ Backend selection     │  │
│  │  Solver execution (seeded)  │  │  Latency/noise scoring       │  │
│  │      ↓ CBQP (Δ)             │  │      ↓ Execution + DGT       │  │
│  │  DGT generated              │  │  Result + evidence record    │  │
│  │      ↓ CBQP (Ψ)             │  │      ↓ DT synchronisation    │  │
│  │  SSOT promotion gate        │  │  Provenance-linked DT update │  │
│  └──────────┬──────────────────┘  └──────────────┬───────────────┘  │
│             │                                     │                  │
│             └──────────────┬────────────────────--┘                  │
│                            ↓                                        │
│              Operational Evidence Ledger (OEL)                      │
│              GAIA-X EU sovereign infrastructure                     │
│                            ↓                                        │
│              Digital Thread: DEV → SSOT → Ops                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.1 QAPD — Quantum Accelerated Product Development

QAPD governs the design-time half of AQUA-V. Its three functional layers are:

**Layer A — HDCEL (Hybrid Discrete–Continuous Encoding Layer):** Translates
mixed-type aerospace design parameters into QUBO instances using the
`AerospaceConstraintSchema`. Encoding is schema-versioned; changes to
`ACS-v1.0` require a CCB-approved ECR.

**Layer B — CBQP Execution (Γ):** Executes the QUBO instance on the
selected quantum or hybrid-classical backend with deterministic seeding.
Supports QAOA, quantum annealing (D-Wave), and classical fallback (simulated
annealing, tabu search) with identical DGT generation in all cases.

**Layer C — SSOT Promotion (Ψ):** Validates the DGT, packages it with the
lifecycle phase tag, and writes to the OEL. Human oversight is mandatory for
DAL A/B results (BREX rule SAFETY-AI-001).

### 3.2 QAOS — Quantum Assisted Operation Services

QAOS governs the operational half of AQUA-V. Its workload classification
system is the defining innovation:

**Workload Classification:**

| Class | Label | Deadline | DAL | Examples |
|---|---|---|---|---|
| QW1 | Safety-critical | ≤ 5 ms | A/B | Real-time flight envelope monitoring |
| QW2 | Mission-critical | ≤ 100 ms | B/C | Route optimisation, weather rerouting |
| QW3 | Operational | ≤ 1 s | C/D | Maintenance scheduling, supply chain |
| QW4 | Background | Best-effort | D | Training data processing, analytics |

**Backend selection scoring function:**

```
score(b, w) = w_lat · (1 − lat(b)/lat_max)
            + w_noise · (1 − noise(b)/noise_max)
            + w_queue · (1 − queue(b)/queue_max)
```

where weights (w_lat, w_noise, w_queue) are tuned per workload class. QW1
enforces a hard constraint: if no backend meets the 5 ms deadline, execution
falls back to a pre-validated classical solver.

**Digital Twin synchronisation:** Each QAOS result updates the operational
digital twin via a provenance-linked record that references the generating DGT.
Human oversight hooks are invoked for QW1 state changes (EU AI Act Art. 14
human oversight obligation for high-risk AI systems).

### 3.3 The DEV → SSOT → Ops Digital Thread

The AQUA-V Digital Thread is the unbroken, auditable causal chain:

```
Design Parameters (DEV)
    ↓  [HDCEL: φ(d,C) → QUBO]
QUBO Instance
    ↓  [CBQP Γ: seeded execution → R_k]
    ↓  [CBQP Δ: DGT = (s, H_in, v, R_k, σ)]
Deterministic Governance Tuple
    ↓  [CBQP Ψ: human review → OEL append]
Single Source of Truth (SSOT) + OEL entry
    ↓  [QAOS DT sync: provenance-linked update]
Operational Digital Twin
    ↓  [Continuous monitoring → triggers QAOS workloads]
    ↑  [Updated operational parameters → feeds back to DEV]
```

Every arrow in this chain corresponds to a BREX-governed transformation.
No step occurs without a contract-authorised pipeline (BREX rule PIPELINE-004).

---

## 4. Governance Model

AQUA-V operates within the ASIT (Aircraft Systems Information Transponder)
governance framework. Every operation is subject to BREX decision rules:

| BREX Rule | Scope | Enforcement |
|---|---|---|
| STRUCT-001 | ATA domain classification required | Block |
| AUTHOR-002 | Contract-gated content generation | Require contract |
| SAFETY-AI-001 | DAL A/B AI results require human approval | Escalate to STK_SAF |
| SAFETY-AI-002 | Training data governance required | Block |
| PIPELINE-004 | Contract-approved transformations only | Require approval |
| BL-002 | Baseline modifications require CCB | Escalate to CCB |

**EU regulatory alignment:**

| Framework | AQUA-V Integration |
|---|---|
| EASA CS-25 / AMC-20 | DGT satisfies reproducibility requirement; OEL satisfies record-keeping |
| DO-178C | CBQP lifecycle phase tagging maps to DO-178C software level evidence |
| EU AI Act (Reg. 2024/1689) | QW1 human oversight hook satisfies Art. 14; Art. 13 transparency via OEL |
| GAIA-X | OEL stored on EU-sovereign infrastructure; no cross-border replication without CCB |
| eIDAS (Reg. 910/2014) | DGT digital signature uses eIDAS-qualified certificate for EU legal standing |

---

## 5. Mathematical Formulation Summary

### 5.1 QUBO Objective

The general AQUA-V QUBO instance for a design problem with n binary variables:

```
minimise   x^T Q x + c^T x
subject to x ∈ {0,1}^n
```

where the objective matrix Q = Q_cost + Σ_c λ_c Q_c includes:
- **Q_cost**: the primary engineering objective (e.g., structural mass, drag)
- **Q_c**: penalty matrix for constraint c ∈ C, derived from
  `AerospaceConstraintSchema ACS-v1.0`
- **λ_c**: penalty coefficient for constraint c (set by domain expert per ECR)

### 5.2 DGT Construction

```python
import hashlib, json
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class DeterministicGovernanceTuple:
    record_id:   str   # UUID4
    global_seed: int   # First 64 bits of SHA-256(inputs || timestamp)
    input_hash:  str   # SHA-256 of serialised (d, C, config)
    solver_ver:  str   # "sdk==x.y.z+backend==a.b.c"
    circuit_hash: str  # SHA-256 of compiled QASM
    top_k:       list  # Ranked solution vectors
    result_hash: str   # SHA-256 of serialised top_k
    lc_phase:    str   # e.g. "LC04"
    timestamp:   str   # ISO 8601 UTC
    signature:   str   # ECDSA-P384 over all fields

def build_dgt(inputs, top_k, solver_ver, lc_phase, private_key):
    ts  = datetime.now(timezone.utc).isoformat()
    raw = json.dumps(inputs, sort_keys=True).encode()
    h_in = hashlib.sha256(raw).hexdigest()
    seed = int(hashlib.sha256(raw + ts.encode()).hexdigest()[:16], 16)
    r_h  = hashlib.sha256(json.dumps(top_k).encode()).hexdigest()
    payload = f"{seed}{h_in}{solver_ver}{r_h}{lc_phase}{ts}"
    sig = private_key.sign(hashlib.sha256(payload.encode()).digest())
    return DeterministicGovernanceTuple(
        record_id=str(__import__("uuid").uuid4()),
        global_seed=seed, input_hash=h_in, solver_ver=solver_ver,
        circuit_hash="", top_k=top_k, result_hash=r_h,
        lc_phase=lc_phase, timestamp=ts, signature=sig.hex()
    )
```

### 5.3 OEL Chain Integrity

```
τ_0 = 0^256
τ_i = SHA-256( serialise(DGT_i) || serialise(DGT_{i-1}) || τ_{i-1} )
```

An auditor verifies OEL integrity by recomputing all τ_i from i = 1 to N and
confirming τ_N matches the ledger's published root hash. Any modification to
any DGT_i produces a detectable divergence at τ_i and all subsequent entries.

---

## 6. Applications and Embodiments

### 6.1 Blended Wing Body with Liquid Hydrogen Propulsion (BWB-H₂)

The primary embodiment applies AQUA-V to the simultaneous optimisation of
BWB structural topology, LH₂ tank geometry, and thermal insulation thickness.
The HDCEL encodes:
- Structural member topology as binary variables (member present/absent)
- LH₂ tank volume fraction as continuous variables discretised to 10 bits
- `cryogenic_thermal` penalties for material embrittlement at −253°C
- `h2_material_compat` penalties from the H₂ galvanic compatibility matrix
- `dal_prob_bound` penalties derived from ARP4761 FMEA for DAL B fuel system

DGTs are generated at LC04 (Design) and promoted to SSOT at LC06 (Verification)
after EASA Design Organisation Approval review.

### 6.2 Supply Chain Optimisation (Cross-Industry)

Multi-tier aerospace supply chain scheduling with disruption recovery. The
HDCEL encodes supplier selection and schedule allocation, with `eu_reach_compliance`
penalties for REACH Annex XVII restricted substances and conflict-mineral
sourcing constraints. QAOS orchestrates the computation as a QW3 workload.

### 6.3 Predictive Maintenance

Fleet maintenance scheduling optimised with quantum feature encoding of
sensor time-series. QAOS classifies as QW3. The resulting schedule is
promoted to the operational digital twin and monitored against the OEL for
schedule adherence drift detection. EU AI Act Art. 14 human oversight is
applied to maintenance deferral decisions.

---

## 7. What This Architecture Is Not

To prevent terminological dilution, we explicitly delimit the AQUA-V scope:

| Out of scope | Why excluded |
|---|---|
| Generic QAOA for combinatorial optimisation | No DGT, no domain constraint schema, no OEL — not CBQP |
| Generic digital twin for aerospace design | No quantum computation, no DGT provenance linkage — not AQUA-V |
| Generic generative AI in engineering | No deterministic reproducibility, no certification evidence — not QAPD |
| Quantum computing without deterministic seeding | Violates DGT invariant; incompatible with CBQP definition |
| Evidence ledger without EU-sovereign hosting | Violates OEL property 3 — not a conformant OEL instance |

---

## 8. Versioning and Evolution

| Version | Date | Change |
|---|---|---|
| **1.0.0** | 2026-02-19 | Initial definitive edition. Establishes DGT, HDCEL, CBQP, OEL as canonical terms. Formalises QAPD + QAOS = AQUA-V equation. |

**Policy:** Minor versions (1.x) refine definitions without breaking
compatibility. Major versions (2.x) may redefine canonical terms and require
a CCB-approved change notice. The SHA-256 of this document at v1.0.0
constitutes the canonical identity anchor for all derivative works.

---

## 9. How to Cite

**Plain text (APA style):**
> Pelliccia, A. (2026). *AQUA-V v1.0: Foundational Architecture for
> Quantum-Assisted Aerospace Product Development and Operations* (Version 1.0.0).
> AEROSPACEMODEL Repository.
> https://github.com/AmedeoPelliccia/AEROSPACEMODEL/blob/main/AQUA-V-IP/AQUA_V_FOUNDATIONAL_PAPER_v1.0.md

**BibTeX:**
```bibtex
@techreport{pelliccia2026aquav,
  author      = {Pelliccia, Amedeo},
  title       = {{AQUA-V} v1.0: Foundational Architecture for
                 Quantum-Assisted Aerospace Product Development and Operations},
  institution = {AEROSPACEMODEL / ASIT},
  year        = {2026},
  month       = {02},
  version     = {1.0.0},
  url         = {https://github.com/AmedeoPelliccia/AEROSPACEMODEL/blob/main/AQUA-V-IP/AQUA_V_FOUNDATIONAL_PAPER_v1.0.md},
  note        = {Canonical reference for: Deterministic Governance Tuple (DGT),
                 Hybrid Discrete--Continuous Encoding Layer (HDCEL),
                 Certification-Bound Quantum Pipeline (CBQP),
                 Operational Evidence Ledger (OEL).}
}
```

**CITATION.cff:** See [`/CITATION.cff`](../CITATION.cff) at the repository root
for machine-readable citation metadata compatible with GitHub's "Cite this
repository" feature and Zenodo deposit workflows.

---

## 10. Related Documents

| Document | Role |
|---|---|
| [`AQUA-V-IP/README.md`](README.md) | Patent portfolio overview and filing strategy summary |
| [`AQUA-V-IP/P0_PARENT_ARCHITECTURE/CLAIMS_DRAFT.md`](P0_PARENT_ARCHITECTURE/CLAIMS_DRAFT.md) | Formal EPO/USPTO claims derived from this paper |
| [`AQUA-V-IP/C1_QAPD/C1.2_DETERMINISTIC_PIPELINES/`](C1_QAPD/C1.2_DETERMINISTIC_PIPELINES/) | DGT and CBQP detailed claims (highest priority child) |
| [`AQUA-V-IP/C2_QAOS/C2.1_RESOURCE_ORCHESTRATOR/`](C2_QAOS/C2.1_RESOURCE_ORCHESTRATOR/) | QW1–QW4 workload classification detailed claims |
| [`AQUA-V-IP/PRIOR_ART_ANALYSIS/`](PRIOR_ART_ANALYSIS/) | QUBO aerospace landscape, DT certification landscape |
| [`CITATION.cff`](../CITATION.cff) | Machine-readable citation metadata (GitHub / Zenodo) |

---

*Amedeo Pelliccia — AEROSPACEMODEL / ASIT — 2026-02-19*  
*This document constitutes the canonical reference anchor for the AQUA-V architecture.*  
*SHA-256 of this file at v1.0.0 release is the authoritative version identity.*
