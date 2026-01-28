# Release Policy

## Overview

This document defines the policies governing the release of baselines, publications, and other controlled artifacts within the ASIT-ASIGT framework.

---

## 1. Release Authority

### 1.1 Authority Matrix

| Release Type | Primary Authority | Secondary Authority |
|--------------|-------------------|---------------------|
| Functional Baseline (FBL) | STK_CM | STK_ENG |
| Allocated Baseline (ABL) | STK_CM | STK_ENG |
| Product Baseline (PBL) | STK_CM | STK_QA |
| Operational Baseline (OBL) | STK_CM | STK_CERT + STK_OPS |
| Technical Publications | STK_CM | STK_CERT |
| Service Bulletins | STK_CM | STK_CERT |

### 1.2 Delegation

Release authority may be delegated only through formal written authorization documented in the approval matrix.

---

## 2. Release Prerequisites

### 2.1 Baseline Release Prerequisites

| Prerequisite | FBL | ABL | PBL | OBL |
|--------------|-----|-----|-----|-----|
| All CIs baselined | ✓ | ✓ | ✓ | ✓ |
| ECO approved (if changed) | ✓ | ✓ | ✓ | ✓ |
| Verification complete | ✓ | ✓ | ✓ | ✓ |
| Trace matrix complete | ✓ | ✓ | ✓ | ✓ |
| Gate review passed | ✓ | ✓ | ✓ | ✓ |
| Certification compliance | — | — | ✓ | ✓ |
| Operations approval | — | — | — | ✓ |

### 2.2 Publication Release Prerequisites

- [ ] ASIGT transformation complete
- [ ] BREX validation passed
- [ ] Schema validation passed
- [ ] Trace matrix generated
- [ ] Content review complete
- [ ] Authority approval obtained

---

## 3. Release Process

### 3.1 Standard Release Process

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  CANDIDATE  │────▶│   REVIEW    │────▶│  APPROVAL   │────▶│  RELEASED   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
   Proposed           Compliance          Authority            Published
   for release        verified            sign-off             & locked
```

### 3.2 Steps

1. **Candidate Preparation**
   - Complete all prerequisites
   - Generate release package
   - Document release notes

2. **Compliance Review**
   - Verify all prerequisites met
   - Validate trace completeness
   - Check regulatory compliance

3. **Authority Approval**
   - Obtain required signatures
   - Record approval in register
   - Archive approval evidence

4. **Publication**
   - Assign release identifier
   - Publish to distribution channels
   - Lock baseline (immutable)

---

## 4. Release Identification

### 4.1 Release Numbering

```
<BASELINE-ID>-R<RELEASE-NUMBER>

Examples:
  FBL-2026-Q1-001-R1    # First release of baseline
  PBL-2026-Q2-003-R2    # Second release (correction)
```

### 4.2 Version Semantics

| Component | Meaning |
|-----------|---------|
| Major | Breaking changes to interfaces or structure |
| Minor | Backward-compatible additions |
| Patch | Corrections and clarifications |

---

## 5. Release Types

### 5.1 Standard Release

| Attribute | Value |
|-----------|-------|
| Purpose | Normal scheduled release |
| Notice Period | ≥ 14 days |
| Approval | Standard authority matrix |

### 5.2 Urgent Release

| Attribute | Value |
|-----------|-------|
| Purpose | Safety or regulatory urgent |
| Notice Period | ≥ 24 hours |
| Approval | Expedited (documented justification) |

### 5.3 Emergency Release

| Attribute | Value |
|-----------|-------|
| Purpose | Immediate safety concern |
| Notice Period | Immediate |
| Approval | Post-hoc CCB ratification required |

---

## 6. Distribution

### 6.1 Distribution Channels

| Channel | Content | Recipients |
|---------|---------|------------|
| Internal Portal | All releases | Program team |
| Customer Portal | Approved publications | Operators |
| Regulatory Portal | Certification data | Authorities |
| Supplier Portal | Relevant specifications | Supply chain |

### 6.2 Distribution Record

All distributions must be recorded including:
- Release identifier
- Distribution date
- Recipients
- Acknowledgment status

---

## 7. Post-Release

### 7.1 Immutability

Released baselines are **immutable**. Any corrections require:
- New ECR/ECO cycle
- New baseline version
- New release

### 7.2 Retention

| Release Type | Retention Period |
|--------------|------------------|
| Active releases | Indefinite |
| Superseded releases | Life of program + 10 years |
| Archived releases | Per regulatory requirements |

---

## 8. Registration

All releases must be recorded in [RELEASE_REGISTER.csv](RELEASE_REGISTER.csv).

---

## Related Documents

- [../BASELINES.md](../BASELINES.md) — Baseline policies
- [RELEASE_REGISTER.csv](RELEASE_REGISTER.csv) — Release tracking
- [../APPROVALS/APPROVAL_MATRIX.csv](../APPROVALS/APPROVAL_MATRIX.csv) — Authority matrix
