# AeroParts International — Baseline Management

## Overview

This document defines baseline management for the **LGA-5000 Landing Gear Actuator** program at AeroParts International.

## Supplier Baseline Strategy

As a Tier-1 supplier, baseline management must align with:
1. Internal product development
2. OEM aircraft program baselines
3. Regulatory certification milestones

```
              Internal                    OEM Alignment
                 │                              │
   ┌─────────────┼─────────────┐   ┌───────────┼───────────┐
   ▼             ▼             ▼   ▼           ▼           ▼
┌──────┐    ┌──────┐    ┌──────┐  OEM-A      OEM-B      OEM-C
│ DBL  │───▶│ CBL  │───▶│ PBL  │  Type-X    Type-Y     Type-Z
│Design│    │Comp. │    │Prod. │  Baseline  Baseline   Baseline
└──────┘    └──────┘    └──────┘
```

## Active Baselines

| ID | Type | Status | Description |
|----|------|--------|-------------|
| DBL-LGA5000-2025-Q2 | Design | Frozen | Design freeze |
| CBL-LGA5000-2025-Q3 | Component | Frozen | Initial production |
| CBL-LGA5000-2026-Q1 | Component | Active | Current production |
| SBL-LGA5000-SB001 | Service Bulletin | Active | Field modification |

## Customer Baseline Mapping

### OEM-A (Aircraft Type-X)

| LGA-5000 Baseline | OEM-A Baseline | Status |
|-------------------|----------------|--------|
| CBL-LGA5000-2025-Q3 | OEM-A-BL-2025-R2 | Approved |
| CBL-LGA5000-2026-Q1 | OEM-A-BL-2026-R1 | Pending |

### OEM-B (Aircraft Type-Y)

| LGA-5000 Baseline | OEM-B Baseline | Status |
|-------------------|----------------|--------|
| CBL-LGA5000-2025-Q3 | OEM-B-BL-2025-P3 | Approved |
| CBL-LGA5000-2026-Q1 | OEM-B-BL-2026-P1 | In Review |

## Baseline Types

### DBL — Design Baseline

- Engineering design freeze
- Drawing release
- Analysis completion

### CBL — Component Baseline

- Production-ready configuration
- FAA-PMA/EASA Part 21G approval
- CMM/IPC release

### SBL — Service Bulletin Baseline

- Field modification package
- Retrofit instructions
- Affected serial numbers

### PBL — Production Baseline

- Manufacturing configuration
- Process specifications
- Quality requirements

## Change Control

### Internal Changes

1. Engineering Change Request (ECR)
2. Impact assessment (all customers)
3. CCB approval
4. Customer notification
5. Documentation update

### Customer-Driven Changes

1. OEM change notification received
2. Impact assessment
3. Internal ECR (if required)
4. CCB approval
5. Customer response

## AS9100 Traceability

All baselines support AS9100D requirements:
- Configuration identification
- Change control records
- Traceability to serial numbers
- Customer approval evidence
