# Human-Centric Digital Systems Charter - 90-Day Transition Roadmap

> **Document ID:** AEROSPACEMODEL-GOV-HCDS-ROADMAP-001  
> **Version:** 1.0.0  
> **Status:** ACTIVE  
> **Authority:** ASIT  
> **Date:** 2026-02-12

---

## Executive Summary

This document provides a detailed 90-day transition plan for implementing the Human-Centric Digital Systems Charter v1.0. The transition follows a phased approach:

- **Days 0-30:** Freeze, inventory, and classify
- **Days 31-60:** Disable prohibited features and deploy compliant systems
- **Days 61-90:** Audit, enforce, and report

**Success Criteria:**
- Contextual Delivery Share (CDS) ≥ 90%
- User-Level Targeting Rate (ULTR) ≤ 10% (protected surfaces)
- All 8 charter articles operational
- First third-party audit completed
- Public transparency dashboard live

---

## Phase 1: Freeze and Inventory (Days 0-30)

### Week 1: Freeze and Foundation (Days 1-7)

**Key Actions:**
- Executive leadership approval of charter
- Establish Charter Compliance Office (CCO)
- Freeze all new personalized persuasion feature development
- Organization-wide training on charter principles

### Week 2-3: Signal Inventory and Classification (Days 8-21)

**Key Actions:**
- Document all signals used across all systems
- Classify signals as allowed, allowed-with-consent, or banned
- Audit existing targeting systems for Article 2 violations

### Week 4: Feature Classification and Baseline Metrics (Days 22-30)

**Key Actions:**
- Create definitive list of prohibited targeting features
- Begin development of contextual-only ad serving pipeline
- Establish baseline KPI measurements (ULTR, CDS, MIR, EC, AASI, PICS)

**Public Deliverables:** Signal inventory, Baseline metrics report

---

## Phase 2: Disable and Enforce (Days 31-60)

### Week 5-6: Disable Prohibited Features (Days 31-45)

**Key Actions:**
- Remove banned vulnerability signals from production
- Deploy policy firewall between reasoning and ad systems
- Implement contextual-only serving on core surfaces

### Week 7: Launch Transparency Features (Days 46-52)

**Key Actions:**
- Launch public ad repository (all ads with targeting basis)
- Implement "Why this ad?" transparency feature
- Deploy explainability API

### Week 8: Measure and Report (Days 53-60)

**Key Actions:**
- Calculate first month compliance metrics
- Address technical debt from rapid migration
- Launch user education campaign

**Public Deliverables:** Public ad repository, First month compliance report

---

## Phase 3: Audit and Enforce (Days 61-90)

### Week 9: Third-Party Audit (Days 61-67)

**Key Actions:**
- Contract independent audit firm
- Conduct first external audit (AASI, ULTR, CDS, MIR, EC, PICS)
- Red team exercise on manipulation detection

### Week 10: Compute and Enforcement (Days 68-74)

**Key Actions:**
- Publish compute allocation report (PICS tracking)
- Deploy public PICS dashboard
- Finalize enforcement runbook and sanctions ladder

### Week 11-12: Remediation and Reporting (Days 75-86)

**Key Actions:**
- Address external audit findings
- Conduct internal compliance review
- Prepare 90-day transition retrospective

### Week 13: Publish and Celebrate (Days 87-90)

**Key Actions:**
- Publish comprehensive 90-day transition report
- Celebrate milestones and recognize contributors
- Plan next 90-day iteration

**Public Deliverables:** Compute allocation report, Public PICS dashboard, 90-day transition report

---

## Resource Requirements

- **Personnel:** ~2,175 person-days across 90 days
- **Budget:** $2.5M (includes CCO operations, engineering, infrastructure, external audit)
- **Key Roles:** CCO (4.5 FTE), Engineering (31 FTE peak), Product (5 FTE), Data Science (5 FTE)

---

## Success Metrics (Day 90 Targets)

| KPI | Baseline | Target | Status |
|-----|----------|--------|--------|
| ULTR | ~65% | ≤ 10% | TBM |
| CDS | ~35% | ≥ 90% | TBM |
| MIR | Baseline | Declining | TBM |
| EC | ~12% | 100% (ads) | TBM |
| AASI | ~78% | 100% | TBM |
| PICS | ~8% | ≥ 15% | TBM |

---

## Related Documents

| Document | Location |
|----------|----------|
| Human-Centric Digital Systems Charter | `Governance/HUMAN_CENTRIC_DIGITAL_SYSTEMS_CHARTER_v1.0.md` |
| Technical Controls | `policy/hcds_technical_controls_v1.yaml` |
| Full 90-Day Roadmap Details | [See full document for detailed day-by-day plan] |

---

*Governed by the AEROSPACEMODEL Digital Constitution.*  
*Committed to human agency, truth, and ethical commerce.*
