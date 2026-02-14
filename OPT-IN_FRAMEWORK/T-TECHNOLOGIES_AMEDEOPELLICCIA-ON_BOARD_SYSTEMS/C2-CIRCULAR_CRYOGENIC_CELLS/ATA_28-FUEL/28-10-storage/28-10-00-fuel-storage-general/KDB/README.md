# Knowledge Database (KDB) — 28-10-00

The KDB holds all engineering knowledge for this subject,
organized into mutable development workspace and lifecycle-managed
baselined content.

## Structure

| Directory | Purpose | Policy |
|-----------|---------|--------|
| `DEV/` | Mutable workspace | Work-in-progress; not baselined |
| `LM/` | Lifecycle-managed | Baselined, BREX-compliant, traceable |

## Policies

- **DEV/** is for WIP content: prototypes, trade studies, working drafts.
  Content here is not authoritative and must not be referenced
  by publications or contracts.

- **LM/SSOT/** is the single source of truth. Content here is
  baselined, BREX-validated, and traceable through all lifecycle phases.

## Promotion

Promotion from `DEV/` → `LM/` requires:
1. BREX validation pass
2. Complete trace coverage
3. Approval by STK_ENG (or STK_SAF for safety content)
4. Baseline registration in `GOVERNANCE/BASELINE_REGISTER.csv`
