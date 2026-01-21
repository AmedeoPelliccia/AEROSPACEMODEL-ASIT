# AEROSPACEMODEL-ASIT
## Aircraft Systems Information Transponder (ASIT)

<p align="center">
  <img src="https://img.shields.io/badge/Version-2.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/S1000D-Issue%205.0-teal" alt="S1000D">
  <img src="https://img.shields.io/badge/ATA-iSpec%202200-orange" alt="ATA">
  <img src="https://img.shields.io/badge/Traceability-Evidence%20Ready-green" alt="Traceability Evidence Ready">
</p>

<p align="center">
  <strong>Organization-agnostic framework for transforming governed aerospace engineering knowledge into industry-standard technical publications and operational projections.</strong>
</p>

<p align="center">
  <a href="#why-asit">Why ASIT</a> •
  <a href="#key-principles">Key Principles</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#contracts">Contracts</a> •
  <a href="#pipelines">Pipelines</a> •
  <a href="#examples">Examples</a>
</p>

---

## Why ASIT?

Starting a new aircraft development program requires transforming engineering knowledge into **certifiable, configuration-aware technical publications**. ASIT provides:

| Challenge | ASIT Capability |
|-----------|------------------|
| S1000D compliance is complex | Templates + schema validation + BREX-style rule enforcement |
| Certification traceability | Deterministic trace matrices and evidence bundles |
| Multiple publication types (AMM, SRM, CMM, IPC, SB) | Unified pipeline + contract model |
| Reproducible builds for audits | Immutable run evidence with hashes/manifests |
| Program-specific business rules | Extensible rule engine (applicability, naming, quality gates) |
| ATA chapter organization | ATA iSpec 2200-aligned scoping and mapping |

### Who Is This For?

- OEMs starting new aircraft programs
- MROs building publication + sustainment pipelines
- Tier-1 suppliers delivering component documentation
- Startups in eVTOL/UAM/hydrogen aviation
- Certification and compliance engineering teams

---

## Key Principles

### 1) Authority Boundary (Non-Authoritative by Design)

ASIT is a **non-authoritative transformer**. It must never corrupt or overwrite your truth sources.

**ASIT MUST NOT**
- write to `KDB/LM/SSOT/**`
- bypass governance by running ad-hoc transforms outside contracts

**ASIT MAY**
- read from `KDB/LM/SSOT/**` (authoritative inputs)
- read contextual inputs from `IDB/OPS/LM/**` (operator/config/MRO context)
- write only to:
  - `IDB/**` (projections)
  - `runs/**` (immutable evidence)

### 2) Contract-First Execution

ASIT runs only what a contract authorizes:

- **Contract** = what to transform, what inputs are allowed, what outputs are produced, what gates must pass, what evidence is required
- **Pipeline** = how steps execute
- **Rules** = applicability, mapping, validations, naming constraints

### 3) Deterministic Evidence

Every run produces an immutable evidence package:

- INPUT_MANIFEST (hashes, counts, lineage)
- OUTPUT_MANIFEST (artifacts + hashes)
- TRACE_MATRIX (trace coverage)
- VALIDATION_REPORT (BREX/schema/quality gates)
- METRICS + logs

---

## Quick Start

### Install

```bash
pip install aerospacemodel-asit
asit --version
asit doctor
````

### Initialize a Program Workspace

```bash
asit init \
  --program "MyAircraft" \
  --model-code "MA" \
  --s1000d-issue "5.0" \
  --ata-scope "21-80" \
  --output ./MyAircraft-ASIT
```

### Execute a Contract (Example)

```bash
cd MyAircraft-ASIT
asit run --contract KITDM-CTR-LM-CSDB_ATA28-10-00 --verbose
```

---

## Architecture

### The KDB → IDB Model

ASIT implements a governed transformation model:

* **KDB (Knowledge Data Base)**: authoritative truth
* **IDB (Information Data Base)**: projections for consumption (PUB/OPS/INDEX)
* **ASIT**: contract-driven transformer + evidence generator

```
KDB/LM/SSOT/PLM (Truth) ──▶ ASIT (Contracts + Pipelines + Rules) ──▶ IDB (Projections)
                                   │
                                   └────────▶ runs/ (Immutable Evidence)
```

### Two Deployment Modes

1. **Product Mode (this repo/package):** provides engine, CLI, templates, schemas, validators
2. **Subject Mode (inside an ATA subject):** `.../<subject>/ASIT/` executes transformations for that subject with strict authority boundaries

---

## Repository Structure (Product Mode)

```
AEROSPACEMODEL-ASIT/
├── README.md
├── LICENSE
├── pyproject.toml
│
├── src/
│   └── asit/
│       ├── cli.py
│       ├── engine.py
│       ├── contracts.py
│       ├── pipelines.py
│       ├── rules.py
│       ├── validators/
│       │   ├── brex.py
│       │   ├── schema.py
│       │   └── trace.py
│       ├── generators/
│       │   ├── dm.py
│       │   ├── pm.py
│       │   └── dml.py
│       └── utils/
│           ├── hashing.py
│           ├── xml.py
│           └── archive.py
│
├── schemas/
│   ├── s1000d/
│   │   ├── 5.0/
│   │   ├── 4.2/
│   │   └── 4.1/
│   └── ata/
│       └── ispec2200/
│
├── templates/
│   ├── program/
│   ├── pipelines/
│   ├── rules/
│   ├── s1000d/
│   └── ata/
│
├── examples/
├── docs/
├── tests/
└── .github/workflows/
```

---

## Configuration

### Master Configuration (`asit_config.yaml`)

`asit_config.yaml` defines: program identifiers, S1000D issue, ATA scope, source roots, output targets, validation thresholds, archival policy.

Key requirements for audit-safe operation:

* all source roots are **read-only**
* outputs are restricted to **IDB/** (or configured output root)
* `runs/` evidence is immutable

---

## Contracts

Contracts define **what** gets transformed and the governance constraints.

### Canonical Contract Naming (Recommended)

Subject-level (ATAxx-yy-00 scope):

* `KITDM-CTR-LM-CSDB_ATA28-10-00.yaml`
* `KITDM-CTR-LM-EXPORT_ATA28-10-00.yaml`
* `KITDM-CTR-LM-IETP_ATA28-10-00.yaml`
* `KITDM-CTR-OPS-SB_ATA28-10-00.yaml`
* `KITDM-CTR-OPS-REPAIR_ATA28-10-00.yaml`

System-level aggregators (optional, if you define them explicitly):

* `KITDM-CTR-LM-CSDB_ATA28.yaml` (aggregates subject outputs)

### Contract Lifecycle

```
DRAFT → REVIEW → APPROVED → SUPERSEDED
```

ASIT executes **only APPROVED** contracts unless explicitly overridden in a controlled environment.

---

## Pipelines

Pipelines define **how** transformations execute: load → resolve refs → applicability → transform → validate → trace → archive.

Pipelines are deterministic when:

* inputs are fixed (by contract)
* ordering is stable
* hashing is enforced
* outputs are produced via templates/rules only

---

## BREX / Rules Customization

ASIT supports a BREX-style rule structure for:

* structure constraints
* naming constraints
* reference resolution requirements
* program custom rules (e.g., H2 safety warnings)

Rule outcomes must be captured in `VALIDATION_REPORT`.

---

## Examples

* `examples/minimal/` minimal traceable AMM output
* `examples/regional_jet/` multi-chapter pipeline
* `examples/evtol/` custom chapter extensions
* `examples/hydrogen_aircraft/` H2 safety rules and cryogenic procedures

---

## CLI Reference

```bash
asit init --program <name> --model-code <code> [options]
asit run --contract <contract-id> [--dry-run] [--verbose]
asit validate --contract <contract-id>
asit list contracts|pipelines|runs|chapters
asit show contract|pipeline|run <id>
asit export --run <run-id> --format csv|json|pdf
asit verify --run <run-id>
asit doctor
```

---

## License

Creative Commons Zero v1.0 Universal — See `LICENSE`.

---

## Support

Project support channels are intentionally not hardcoded here unless the endpoints are operational.
If you publish official support endpoints, list them in `docs/getting-started.md` and keep this section minimal.

---

<p align="center">
  <strong>AEROSPACEMODEL-ASIT</strong><br/>
  Transform governed engineering knowledge into certified technical publications and auditable evidence.
</p>
```

---
