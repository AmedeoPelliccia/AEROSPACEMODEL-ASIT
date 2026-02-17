# LC03 — Safety & Reliability

**Phase:** LC03 — Safety Assessment & Reliability  
**Subject:** 28-11-00 LH₂ Primary Tank  
**Purpose:** Safety assessment and reliability analysis for C2 cryogenic
hydrogen primary tank per ARP4761, CS-25, and EASA Special Conditions.

## Scope

Functional Hazard Assessment (FHA), Preliminary System Safety
Assessment (PSSA), and System Safety Assessment (SSA) for the
LH₂ primary tank within a modular circular cryogenic cell.

## Contents

| Path | Description |
|------|-------------|
| `PACKAGES/SAFETY/` | Safety assessment plan and findings |
| `PACKAGES/HAZARD_MGMT/` | Hazard register with full traceability |
| `PACKAGES/RELIABILITY/` | Reliability assessment and critical items |
| `TRACE_LC03.csv` | Hazard → requirement → mitigation traces |

## Trade Study Inputs

| Trade Study | Key Safety Finding |
|---|---|
| TS-28-11-TS01 (Architecture) | Cylindrical selected — uniform stress, mature cert precedent |
| TS-28-11-TS02 (Materials) | Al-Li 2195 selected — embrittlement risk at weld zones (RISK-03) |
| TS-28-11-TS03 (Insulation) | Vacuum+MLI selected — vacuum sensitivity is primary safety concern (RISK-01) |

## Governance

- Inherits governance from `GOV-LC01-ATA28-11`
- Safety precedence per `SAFETY_AND_HUMAN_HARM_PRECEDENCE.yaml`
- All safety content requires STK_SAF review (SAFETY-H2-001 escalation)
- Baseline pending CCB approval
