# HydrogenJet-100 — Baseline Management

## Overview

This document defines baseline management for the **HydrogenJet-100 (HJ1)** hydrogen-powered aircraft program.

## Certification Timeline

```
2025-Q3         2025-Q4         2026-Q1         2026-Q3         2027-Q2
   │               │               │               │               │
   ▼               ▼               ▼               ▼               ▼
┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐
│Concept │───▶│  PDR   │───▶│  CDR   │───▶│  TRR   │───▶│  TC    │
│ Review │    │        │    │        │    │        │    │ Issue  │
└────────┘    └────────┘    └────────┘    └────────┘    └────────┘
     │             │             │             │             │
   DBL-Q3       DBL-Q4       FBL-Q1        FBL-Q3        PBL-Q2
```

## Active Baselines

| ID | Type | Status | Description |
|----|------|--------|-------------|
| DBL-HJ1-2025-Q3 | Design | Frozen | Concept selection (fuel cell) |
| DBL-HJ1-2025-Q4 | Design | Frozen | Preliminary design (PDR) |
| FBL-HJ1-2026-Q1 | Functional | Active | Development baseline |
| CBL-HJ1-2026-Q1 | Component | Active | Fuel cell qualification |

## Hydrogen-Specific Baselines

### CBL-HJ1-2026-Q1 (Component - Fuel Cell)

The fuel cell stack follows a separate qualification baseline due to:
- Novel technology qualification requirements
- Independent certification path
- Supplier qualification coordination

| Component | Status | Qualification |
|-----------|--------|---------------|
| Fuel Cell Stack | In Test | Environmental qualification |
| LH2 Tank | In Review | Pressure vessel certification |
| H2 Vaporizer | Qualified | SC-H2-02 compliance |
| Leak Detection | In Test | SC-H2-03 compliance |

## Special Conditions Baseline Mapping

| Special Condition | Baseline Required | Status |
|-------------------|-------------------|--------|
| SC-H2-01: Fuel System Safety | FBL-HJ1-2026-Q1 | In Progress |
| SC-H2-02: Cryogenic Design | FBL-HJ1-2026-Q1 | In Progress |
| SC-H2-03: Leak Detection | FBL-HJ1-2026-Q1 | In Progress |
| SC-H2-04: Fuel Cell Installation | CBL-HJ1-2026-Q1 | In Progress |
| SC-H2-05: Ground Operations | FBL-HJ1-2026-Q1 | Planned |

## Gate Reviews

### Concept Review
- **Date:** 2025-07-15
- **Status:** ✓ Passed
- **Key Decision:** PEM fuel cell selected over hydrogen turbine for initial variant

### PDR — Preliminary Design Review
- **Date:** 2025-10-15
- **Status:** ✓ Passed
- **Key Decisions:**
  - Dual cryogenic tank configuration approved
  - Fuel cell stack architecture frozen
  - Hydrogen safety architecture reviewed

### CDR — Critical Design Review
- **Date:** 2026-03-15 (Scheduled)
- **Status:** In Preparation
- **Prerequisites:**
  - Fuel cell qualification data available
  - Cryogenic tank test data
  - Safety analysis complete

## Hydrogen Safety Baseline Requirements

All baselines affecting hydrogen systems must include:

1. **Hazard Analysis Review** - Updated FHA/PSSA
2. **Safety Requirements Trace** - To certification basis
3. **Ground Operations Review** - Airport compatibility
4. **Emergency Procedures Review** - H2 leak/fire response
