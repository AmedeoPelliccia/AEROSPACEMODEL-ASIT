# RegionalJet-700 — Baseline Management

## Overview

This document defines baseline management for the **RegionalJet-700 (RJ7)** program.

## Active Baselines

| ID | Type | Status | Description |
|----|------|--------|-------------|
| DBL-RJ7-2025-Q4 | Design | Frozen | Initial design after PDR |
| FBL-RJ7-2026-Q1 | Functional | Active | Development baseline after CDR |
| PBL-RJ7-2026-Q1 | Product | Active | Parts data for IPC |
| PBL-RJ7-2026-Q2 | Product | Draft | Production baseline (pending) |

## Baseline Timeline

```
2025-Q4                    2026-Q1                    2026-Q2
   │                          │                          │
   ▼                          ▼                          ▼
┌─────────┐              ┌─────────┐              ┌─────────┐
│DBL-2025 │─────────────▶│FBL-2026 │─────────────▶│PBL-2026 │
│  -Q4    │     PDR      │  -Q1    │     CDR      │  -Q2    │
│ Design  │              │  Func   │              │  Prod   │
└─────────┘              └─────────┘              └─────────┘
     │                        │                        │
     └──── Frozen ────────────┴──── Active ────────────┴── Draft
```

## Gate Reviews

### PDR — Preliminary Design Review
- **Date:** 2025-10-15
- **Status:** ✓ Passed
- **Baseline:** DBL-RJ7-2025-Q4 established
- **Attendees:** Engineering, QA, PM, Customer

### CDR — Critical Design Review
- **Date:** 2026-01-10
- **Status:** ✓ Passed
- **Baseline:** FBL-RJ7-2026-Q1 established
- **Attendees:** Engineering, QA, PM, Certification, Customer

### TRR — Test Readiness Review
- **Date:** 2026-03-15 (Scheduled)
- **Status:** Pending
- **Prerequisites:** All test procedures approved

### PRR — Production Readiness Review
- **Date:** 2026-06-01 (Planned)
- **Status:** Planned
- **Prerequisites:** TRR pass, tooling complete

## Baseline Content

### DBL-RJ7-2025-Q4 (Design)
- System requirements
- Preliminary design data
- Interface definitions
- Safety analysis (preliminary)

### FBL-RJ7-2026-Q1 (Functional)
- Detailed requirements
- Design specifications
- Test requirements
- Maintenance task analysis

### PBL-RJ7-2026-Q1 (Product - Parts)
- Parts catalog data
- Bill of materials
- Vendor part numbers
- Interchangeability data

### PBL-RJ7-2026-Q2 (Product - Production)
- Production configuration
- Manufacturing data
- Final parts list
- Effectivity assignments
