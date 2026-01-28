# Baseline Types and Policies

## Overview

Baselines are **immutable, versioned snapshots** of configuration items that serve as the authoritative reference for all downstream transformations.

> **ASIGT operates exclusively against approved baselines.**

---

## Baseline Types

### FBL — Functional Baseline

| Attribute | Value |
|-----------|-------|
| **Definition** | Requirements and functional specifications |
| **Established** | After System Requirements Review (SRR) |
| **Contains** | System requirements, functional specifications |
| **Authority** | STK_ENG + STK_CM |

### ABL — Allocated Baseline

| Attribute | Value |
|-----------|-------|
| **Definition** | Design allocated to components/subsystems |
| **Established** | After Preliminary Design Review (PDR) |
| **Contains** | Design specifications, interface definitions |
| **Authority** | STK_ENG + STK_CM |

### PBL — Product Baseline

| Attribute | Value |
|-----------|-------|
| **Definition** | As-built configuration |
| **Established** | After Critical Design Review (CDR) |
| **Contains** | Production drawings, manufacturing specs |
| **Authority** | STK_ENG + STK_CM + STK_QA |

### OBL — Operational Baseline

| Attribute | Value |
|-----------|-------|
| **Definition** | In-service configuration |
| **Established** | After Type Certification |
| **Contains** | Operational publications, maintenance data |
| **Authority** | STK_CM + STK_OPS + STK_CERT |

---

## Baseline Naming Convention

```
<TYPE>-<YEAR>-<QUARTER>-<SEQUENCE>

Examples:
  FBL-2026-Q1-001    # First functional baseline of Q1 2026
  PBL-2026-Q2-003    # Third product baseline of Q2 2026
  OBL-2026-Q3-001    # First operational baseline of Q3 2026
```

---

## Baseline Lifecycle

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   DRAFT     │────▶│   REVIEW    │────▶│  APPROVED   │────▶│  RELEASED   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │                   │
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
   Editable            CCB Review          Locked             Immutable
```

### State Definitions

| State | Description | Editable |
|-------|-------------|----------|
| DRAFT | Under development | Yes |
| REVIEW | Submitted to CCB | No (pending) |
| APPROVED | CCB approved | No |
| RELEASED | Published for use | No (immutable) |

---

## Baseline Policies

### Policy 1: Immutability

Once a baseline reaches **RELEASED** state, it is **immutable**. Any changes require a new baseline version.

### Policy 2: Traceability

Every baseline must reference:
- Source baselines (if derived)
- Approval authority (ECO reference)
- Effective date

### Policy 3: Delta Documentation

When creating a new baseline version, the delta from the previous version must be documented.

### Policy 4: Retention

| Baseline Type | Retention Period |
|---------------|------------------|
| FBL | Life of program + 10 years |
| ABL | Life of program + 10 years |
| PBL | Life of type certificate + 10 years |
| OBL | Life of type certificate + 10 years |

---

## Baseline Registration

All baselines must be registered in [BASELINE_REGISTER.csv](BASELINE_REGISTER.csv).

### Required Fields

| Field | Description |
|-------|-------------|
| baseline_id | Unique identifier |
| type | FBL/ABL/PBL/OBL |
| version | Semantic version |
| state | DRAFT/REVIEW/APPROVED/RELEASED |
| created_date | ISO 8601 date |
| released_date | ISO 8601 date (if released) |
| authority | Approving authority |
| eco_ref | ECO reference (if applicable) |
| description | Brief description |

---

## Related Documents

- [BASELINE_REGISTER.csv](BASELINE_REGISTER.csv) — Active baselines
- [CHANGE_CONTROL/ECO_TEMPLATE.md](CHANGE_CONTROL/ECO_TEMPLATE.md) — Change order template
- [RELEASES/RELEASE_POLICY.md](RELEASES/RELEASE_POLICY.md) — Release policies
