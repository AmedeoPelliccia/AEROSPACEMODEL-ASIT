# SkyLift-200 — Baseline Management

## Overview

This document defines baseline management for the **SkyLift-200 (SL2)** eVTOL program.

## Certification Timeline

```
2025-Q3         2025-Q4         2026-Q1         2026-Q2         2026-Q4
   │               │               │               │               │
   ▼               ▼               ▼               ▼               ▼
┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐
│Concept │───▶│  PDR   │───▶│  CDR   │───▶│  TRR   │───▶│  TC    │
│ Review │    │        │    │        │    │        │    │ Issue  │
└────────┘    └────────┘    └────────┘    └────────┘    └────────┘
     │             │             │             │             │
   DBL-Q3       DBL-Q4       FBL-Q1        FBL-Q2        PBL-Q4
```

## Active Baselines

| ID | Type | Status | Description |
|----|------|--------|-------------|
| DBL-SL2-2025-Q3 | Design | Frozen | Concept design |
| DBL-SL2-2025-Q4 | Design | Frozen | Preliminary design (PDR) |
| FBL-SL2-2026-Q1 | Functional | Active | Development baseline |
| SBL-SL2-2026-Q1 | Software | Active | Flight software baseline |

## Software Baselines (DO-178C)

### SBL-SL2-2026-Q1

| Component | DAL | Version | Status |
|-----------|-----|---------|--------|
| Flight Control Computer (FCC) | A | 1.0.0 | Verified |
| Battery Management System (BMS) | B | 1.0.0 | Verified |
| Vehicle Management System (VMS) | B | 1.0.0 | In Review |
| Health Monitoring (HM) | C | 1.0.0 | Verified |

## Special Conditions Compliance

### SC-VTOL-01: High-Voltage Electrical Systems

- **Baseline:** FBL-SL2-2026-Q1
- **MoC:** Analysis, Test, Simulation
- **Status:** In Progress

### SC-VTOL-02: Distributed Propulsion

- **Baseline:** FBL-SL2-2026-Q1
- **MoC:** Analysis, Test
- **Status:** In Progress

### SC-VTOL-03: Battery Fire Protection

- **Baseline:** FBL-SL2-2026-Q1
- **MoC:** Test, Analysis
- **Status:** In Progress

### SC-VTOL-04: CSFL for DEP

- **Baseline:** FBL-SL2-2026-Q1
- **MoC:** Analysis, Simulation, Flight Test
- **Status:** Planned

## Gate Reviews

### Concept Review
- **Date:** 2025-07-15
- **Status:** ✓ Passed
- **Key Decisions:** Configuration frozen, 8-rotor DEP selected

### PDR — Preliminary Design Review
- **Date:** 2025-10-15
- **Status:** ✓ Passed
- **Key Decisions:** 800V architecture confirmed, DO-178C DAL assignments

### CDR — Critical Design Review
- **Date:** 2026-02-15 (Scheduled)
- **Status:** In Preparation
- **Prerequisites:** Software architecture review complete

### TRR — Test Readiness Review
- **Date:** 2026-06-01 (Planned)
- **Status:** Planned
- **Prerequisites:** Ground test article ready

### Type Certification
- **Target:** 2026-Q4
- **Basis:** Part 23 + Special Conditions
