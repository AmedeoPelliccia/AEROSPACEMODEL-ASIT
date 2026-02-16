# CSDB_REF — Reference Dataset

> Atomic, traceable reference layer for GenKISS (not a replacement for SSOT authority).

---

## Purpose

`CSDB_REF` stores **NU (Atomic Reference Units)** derived from validated SSOT executions, so downstream consumers can reuse distilled technical knowledge without traversing full lifecycle trees.

This directory belongs to the ATA 00 KISS scaffold:

- **GENESIS** → Knowledge Determination Space (uncertain, exploratory)
- **SSOT** → Authoritative Information Source (validated, lifecycle-bound)
- **CSDB_REF** → Derived atomic references for controlled reuse
- **PUB/ATDP** → Delivery surface for Aircraft Technical Data Products

---

## Governance Position

`CSDB_REF` is a **derived layer**:

- It **must trace back** to SSOT execution artifacts.
- It **must not host** primary certification authority.
- It **must not contain** raw GENESIS exploratory artifacts.
- It is **ATDP-agnostic** and can feed AMM, IPC, SRM, TSM, WDM, FIM, MMEL, MPD.

---

## Structure

```text
CSDB_REF/
└── NU/
    ├── index.csv
    ├── schema/
    │   └── nu_source.schema.yaml
    └── NU-<ID>/
        ├── content.*        # atomic distilled reference
        ├── _source.yaml     # mandatory provenance to SSOT execution
        └── metadata.yaml    # optional classification/effectivity
```

---

## Mandatory Rules

1. Every `NU-<ID>/` shall include `_source.yaml`.
2. `_source.yaml` shall reference a valid SSOT path under:
   - `.../SSOT/.../_executions/<timestamp>/`
3. No orphan NU directories (must appear in `index.csv`).
4. NU content is derivative and must never replace SSOT authority.

---

**GenKISS**: General Knowledge and Information Standard Systems
