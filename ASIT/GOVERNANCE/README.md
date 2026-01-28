# ASIT Governance

## Overview

The **GOVERNANCE** module defines the authority, control, and approval mechanisms for all information transformations within the ASIT-ASIGT framework.

> **No content propagates without governance authority.**

---

## Purpose

| Function | Description |
|----------|-------------|
| **Baselines** | Define and control configuration baselines |
| **Change Control** | Manage ECRs, ECOs, and CCB processes |
| **Approvals** | Authority matrix and gate reviews |
| **Releases** | Release policies and tracking |

---

## Directory Structure

```
GOVERNANCE/
├── README.md                       # This file
├── BASELINES.md                    # Baseline types and policies
├── BASELINE_REGISTER.csv           # Active baselines
├── CHANGE_CONTROL/
│   ├── ECR_TEMPLATE.md             # Engineering Change Request template
│   ├── ECO_TEMPLATE.md             # Engineering Change Order template
│   ├── ECR/                        # Submitted ECRs
│   ├── ECO/                        # Approved ECOs
│   └── CCB_MINUTES/                # Configuration Control Board minutes
├── APPROVALS/
│   ├── APPROVAL_MATRIX.csv         # Authority matrix
│   └── GATE_REVIEWS/               # Gate review records
└── RELEASES/
    ├── RELEASE_POLICY.md           # Release policies
    └── RELEASE_REGISTER.csv        # Release tracking
```

---

## Key Concepts

### Baseline Types

| Type | Code | Purpose |
|------|------|---------|
| Functional Baseline | FBL | Requirements and functional specifications |
| Allocated Baseline | ABL | Design allocation to components |
| Product Baseline | PBL | As-built configuration |
| Operational Baseline | OBL | In-service configuration |

### Authority Levels

| Role | Authority |
|------|-----------|
| STK_ENG | Engineering approval |
| STK_CM | Configuration management |
| STK_QA | Quality assurance |
| STK_CERT | Certification authority |
| STK_OPS | Operations approval |

---

## Governance Principles

1. **Traceability** — Every change is traceable to its source
2. **Authority** — Changes require appropriate approval authority
3. **Auditability** — All decisions are recorded and auditable
4. **Baseline Integrity** — Baselines are immutable once released

---

## Related Documents

- [BASELINES.md](BASELINES.md) — Baseline definitions and policies
- [CHANGE_CONTROL/ECR_TEMPLATE.md](CHANGE_CONTROL/ECR_TEMPLATE.md) — ECR template
- [CHANGE_CONTROL/ECO_TEMPLATE.md](CHANGE_CONTROL/ECO_TEMPLATE.md) — ECO template
- [APPROVALS/APPROVAL_MATRIX.csv](APPROVALS/APPROVAL_MATRIX.csv) — Authority matrix
- [RELEASES/RELEASE_POLICY.md](RELEASES/RELEASE_POLICY.md) — Release policy
