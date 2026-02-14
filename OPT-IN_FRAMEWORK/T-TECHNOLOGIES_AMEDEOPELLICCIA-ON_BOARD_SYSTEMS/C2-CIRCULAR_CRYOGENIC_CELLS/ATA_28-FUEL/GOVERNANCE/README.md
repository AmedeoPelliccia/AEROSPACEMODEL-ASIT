# ATA 28 – Fuel System Governance

**System:** AMPEL360 Q100 LH₂ Fuel System (C2 Circular Cryogenic Cells)
**ATA Chapter:** 28 – Fuel
**Version:** 1.0.0

## Overview

This directory defines the governance structure for ATA 28 fuel system
development on the AMPEL360 Q100 programme. All activities are subject to
BREX rule enforcement and ASIT authority.

## Roles

| Role      | Responsibility                                      |
|-----------|-----------------------------------------------------|
| CCB Chair | Approves baseline changes and ECOs                  |
| STK_SAF   | Safety oversight; approves all H₂ safety content    |
| STK_CM    | Configuration management and baseline control       |
| STK_ENG   | Engineering authority for design and test artifacts  |

## Escalation Paths

- **H₂ anomalies** → always escalate to STK_SAF (72 h response window).
- **Baseline changes** → CCB review required (5 business days).
- **Unruled conditions** → HALT and escalate to STK_CM.

## Inheritance

Subject-level governance inherits from system-level governance unless
explicitly overridden. Overrides must be documented in the change log.

## Sub-directories

| Directory          | Purpose                              |
|--------------------|--------------------------------------|
| `APPROVALS/`       | Approval matrices and gate reviews   |
| `CHANGE_CONTROL/`  | ECR/ECO process and registers        |
| `INCENTIVES/`      | Token incentive programme            |
| `RELEASES/`        | Release policy and register          |

## Related Documents

- [BASELINES.md](BASELINES.md)
- [CHANGE_LOG.md](CHANGE_LOG.md)
- [System-level Governance Policy](../GOVERNANCE_POLICY.md)
