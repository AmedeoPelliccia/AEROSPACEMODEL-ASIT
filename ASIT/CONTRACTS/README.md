# ASIT Contracts

## Overview

The **CONTRACTS** module defines the transformation contracts that govern how ASIGT transforms KDB knowledge into IDB publications. Every ASIGT execution requires an approved contract.

> **No transformation without a contract. No contract without authority.**

---

## Purpose

| Function | Description |
|----------|-------------|
| **Define Scope** | What sources to transform, what outputs to produce |
| **Specify Rules** | Mapping rules, validation requirements |
| **Establish Authority** | Who approves, which baseline |
| **Enable Traceability** | Contract ID links inputs to outputs |

---

## Directory Structure

```
CONTRACTS/
├── README.md                       # This file
├── CONTRACT_SCHEMA.yaml            # Contract structure definition
├── templates/                      # Contract templates
│   ├── KITDM-CTR-LM-CSDB.template.yaml
│   ├── KITDM-CTR-LM-EXPORT.template.yaml
│   ├── KITDM-CTR-OPS-SB.template.yaml
│   └── KITDM-CTR-OPS-REPAIR.template.yaml
└── active/                         # Approved contracts
    └── .gitkeep
```

---

## Contract Lifecycle

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   DRAFT     │────▶│   REVIEW    │────▶│  APPROVED   │────▶│   ACTIVE    │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
   Editable           CCB Review          Locked for          Executable
                                          execution           by ASIGT
```

### States

| State | Description | ASIGT Executable |
|-------|-------------|------------------|
| DRAFT | Under development | No |
| REVIEW | Submitted for approval | No |
| APPROVED | CCB approved | Yes |
| ACTIVE | Currently in use | Yes |
| SUPERSEDED | Replaced by newer version | No |
| WITHDRAWN | Cancelled | No |

---

## Contract Types

### LM — Lifecycle Management

| Contract | Purpose |
|----------|---------|
| KITDM-CTR-LM-CSDB | Generate S1000D CSDB content |
| KITDM-CTR-LM-EXPORT | Export to PDF/HTML/IETP |
| KITDM-CTR-LM-DELTA | Generate delta publications |

### OPS — Operations

| Contract | Purpose |
|----------|---------|
| KITDM-CTR-OPS-SB | Generate Service Bulletins |
| KITDM-CTR-OPS-REPAIR | Generate repair procedures |
| KITDM-CTR-OPS-MEL | Generate MEL/CDL content |

### MRO — Maintenance

| Contract | Purpose |
|----------|---------|
| KITDM-CTR-MRO-AMM | Generate AMM content |
| KITDM-CTR-MRO-SRM | Generate SRM content |
| KITDM-CTR-MRO-IPC | Generate IPC content |

---

## Contract ID Format

```
<PREFIX>-CTR-<CATEGORY>-<TARGET>[-<SCOPE>][-<VERSION>]

Examples:
  KITDM-CTR-LM-CSDB                 # Base contract
  KITDM-CTR-LM-CSDB_ATA28           # Scoped to ATA 28
  KITDM-CTR-LM-CSDB_ATA28-v1.2.0    # Versioned
```

---

## Contract Execution

### Invocation

```bash
# Execute contract
aerospacemodel run \
  --contract KITDM-CTR-LM-CSDB_ATA28 \
  --baseline FBL-2026-Q1-003

# Dry run (validation only)
aerospacemodel validate \
  --contract KITDM-CTR-LM-CSDB_ATA28 \
  --dry-run
```

### Execution Flow

```
1. Contract loaded and validated
2. Baseline resolved and locked
3. Sources collected per scope
4. ASIGT generators invoked
5. Outputs validated (BREX, schema)
6. Trace matrix generated
7. Run artifacts archived
8. Metrics recorded
```

---

## Key Principles

### Principle 1: Contract Completeness

A contract must fully specify:
- Source scope (what to transform)
- Target scope (what to produce)
- Mapping rules (how to transform)
- Validation rules (what to check)
- Authority (who approved)

### Principle 2: Contract Immutability

Once APPROVED, a contract is immutable. Changes require:
- New version
- New approval cycle
- Previous version superseded

### Principle 3: Contract Traceability

Every output artifact references:
- Contract ID
- Contract version
- Execution run ID

---

## Related Documents

- [CONTRACT_SCHEMA.yaml](CONTRACT_SCHEMA.yaml) — Schema definition
- [templates/](templates/) — Contract templates
- [active/](active/) — Approved contracts
- [../GOVERNANCE/APPROVALS/](../GOVERNANCE/APPROVALS/) — Approval process
