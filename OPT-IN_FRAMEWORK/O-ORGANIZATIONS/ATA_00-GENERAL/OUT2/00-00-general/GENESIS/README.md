# GENESIS — Knowledge Determination Space

> Epistemic workspace for uncertainty discovery, justification, and framing before SSOT commitment.

---

## Purpose

`GENESIS` is the **knowledge domain** of Aircraft GenKISS.  
It captures what is not yet authoritative:

- unknowns
- assumptions
- decision alternatives
- framing boundaries
- acceptance intent prior to lifecycle execution

GENESIS artifacts are **pre-authoritative** and exist to make epistemic state explicit before information enters SSOT.

---

## Epistemic Position

| Attribute | GENESIS |
|---|---|
| Nature | Uncertain, exploratory, contextual |
| Authority | Pre-authoritative |
| Mutability | High (iterative knowledge work) |
| Primary Function | Determine what must be resolved and why |
| Output | Graduatable KNOT framing for SSOT entry |

---

## Locked Governance Rule

**Locked Rule 1**  
`GENESIS` must not contain executed lifecycle artifacts.

### Forbidden in GENESIS
- `_executions/` directories
- certification evidence packages
- production release artifacts
- authoritative compliance records

### Allowed in GENESIS
- O-KNOT, Y-KNOT, KNOT records
- rationale, options analysis, boundary framing
- registries describing knowledge progression
- schema-conformant pre-authoritative metadata

---

## Canonical Knowledge Pipeline

```text
O-KNOT  ->  Y-KNOT  ->  KNOT  ->  (graduation)  ->  SSOT/LC01+
Discovery   Justify     Frame                        Authoritative lifecycle
```

### O-KNOT (Discovery)

**Question**: What is unknown?  
**Outputs**: uncertainty statement, context, initial trace anchors.

### Y-KNOT (Justification)

**Question**: Why does it matter, and which option is preferable?  
**Outputs**: options analysis, decision rationale, tradeoff basis.

### KNOT (Framing)

**Question**: What exactly will be resolved and how acceptance is defined?  
**Outputs**: bounded scope, acceptance criteria, planned downstream KNUs.

---

## Directory Layout

```text
GENESIS/
├── README.md
├── _registry/
│   ├── o-knot_registry.csv
│   ├── y-knot_registry.csv
│   └── knot_registry.csv
├── O-KNOT/
│   └── O-KNOT-<ID>/
├── Y-KNOT/
│   └── Y-KNOT-<ID>/
└── KNOT/
    └── KNOT-<ID>/
```

---

**GenKISS**: General Knowledge and Information Standard Systems
