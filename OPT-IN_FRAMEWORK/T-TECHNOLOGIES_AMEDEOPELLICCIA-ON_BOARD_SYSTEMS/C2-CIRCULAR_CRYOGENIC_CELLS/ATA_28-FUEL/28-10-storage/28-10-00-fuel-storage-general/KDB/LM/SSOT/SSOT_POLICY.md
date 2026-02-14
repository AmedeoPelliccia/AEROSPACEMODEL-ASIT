# SSOT Policy — 28-10-00

## What Qualifies as SSOT

A knowledge artifact qualifies as Single Source of Truth (SSOT) when:

1. **Baselined** — registered in `GOVERNANCE/BASELINE_REGISTER.csv`
2. **BREX-compliant** — passes all applicable BREX rules
3. **Traceable** — has complete forward and backward traces
4. **Approved** — signed off by the designated authority

## Promotion Rules

To promote content from DEV to LM/SSOT:

- Pass BREX validation (all applicable rules)
- Have complete trace links (requirements ↔ design ↔ test)
- Approved by **STK_ENG** for engineering content
- Approved by **STK_SAF** for safety-critical content
- Registered in the baseline register

## Dispute Resolution

Conflicts between SSOT sources are resolved by the CCB
per the change control process in `GOVERNANCE/CHANGE_CONTROL/`.
