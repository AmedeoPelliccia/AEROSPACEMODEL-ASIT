# COMMON_CSDB — Shared CSDB Components for ATDP

> Reusable, product-agnostic CSDB building blocks for Aircraft Technical Data Products (ATDP).

---

## Purpose

`PUB/ATDP/COMMON_CSDB` contains **shared publication primitives** used across ATDP products (AMM, IPC, SRM, TSM, WDM, FIM, MMEL, MPD, etc.).

This layer avoids duplication and enforces consistency in:

- data module structures
- publication module composition
- business rules (BREX)
- applicability logic
- common warnings/cautions/notes
- graphics and reusable assets

---

## Position in GenKISS

```text
GENESIS (knowledge determination)
    -> SSOT (authoritative lifecycle information)
        -> CSDB_REF (atomic references)
            -> PUB/ATDP/COMMON_CSDB (shared publication components)
                -> PUB/ATDP/PRODUCTS/<AMM|IPC|SRM|...> (final publications)
```

---

## Structure

```text
COMMON_CSDB/
├── DM/              # Data Modules (reusable content units)
├── PM/              # Publication Modules (composition logic)
├── ICN/             # Illustrations (graphics, diagrams)
├── BREX/            # Business Rules Exchange (validation rules)
└── APL/             # Applicability (effectivity, configuration)
```

---

## Governance Rules

1. **Shared primitives only**: No product-specific content.
2. **Traceability required**: All DM/PM must trace to CSDB_REF or SSOT.
3. **Version control**: Changes to COMMON_CSDB require CCB approval.
4. **Reuse mandatory**: Products must use COMMON_CSDB when available.

---

## Example Use Cases

- **Common Warning DM**: "High Voltage Warning" used in AMM, IPC, WDM
- **Standard Procedure PM**: "Lockout/Tagout Procedure" composition
- **Generic Illustration**: "Tool Kit Assembly" graphic
- **Applicability Rule**: "A320 Series with Winglet" effectivity

---

**GenKISS**: General Knowledge and Information Standard Systems
