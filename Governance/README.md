# AEROSPACEMODEL Governance Directory

This directory contains governance charters, standards, and policy frameworks that guide the AEROSPACEMODEL project.

---

## Core Governance Documents

### 1. Human-Centric Digital Systems Charter v1.0
**File:** `HUMAN_CENTRIC_DIGITAL_SYSTEMS_CHARTER_v1.0.md`  
**Purpose:** Constitutional framework for re-founding digital ecosystems around human agency, truth, and verifiability.

**Key Articles:**
- Article 1: Purpose Constraint — Optimize for user welfare, not attention extraction
- Article 2: Inference Boundary — No psychological vulnerability exploitation
- Article 3: Contextual Ads Default — Contextual-only unless explicit consent
- Article 4: Cognitive Integrity — No manipulative interaction loops
- Article 5: Explainability Right — Users can see why content was shown
- Article 6: Functional Separation — Reasoning and ad systems must be separated
- Article 7: Auditability by Design — Tamper-evident audit trails required
- Article 8: Compute Allocation Duty — Minimum public-interest compute share

**Related Documents:**
- Technical Controls: `../policy/hcds_technical_controls_v1.yaml`
- 90-Day Roadmap: `../roadmaps/HCDS_90_DAY_TRANSITION_ROADMAP_v1.md`

---

### 2. EAARF Charter (DRAFT)
**File:** `EAARF_CHARTER_DRAFT.md`  
**Purpose:** European Aviation AI Requirements Framework forum charter for harmonizing AI requirements in aviation.

**Scope:**
- AI certification and assurance
- Human–AI interaction standards
- AI safety assessment
- AI data governance

---

### 3. EASA/ESA AI Governance Standard v1.0 (DRAFT)
**File:** `EASA_ESA_AI_GOVERNANCE_STANDARD_v1.0.md`  
**Purpose:** Governance requirements for AI systems within AEROSPACEMODEL framework, aligned with EASA and ESA regulatory guidance.

**Compliance:**
- EU AI Act (Art. 6, 9, 13-14)
- EASA AI Roadmap 2.0
- ESA ECSS-E-ST-40C
- DO-178C, ARP4754A

---

### 4. NPA 2025-07 Response
**File:** `NPA_2025-07_RESPONSE.md`  
**Purpose:** Response to EASA Notice of Proposed Amendment 2025-07 on AI in aviation.

---

## Governance Framework Hierarchy

```
Digital Constitution (Foundational)
        ↓
Human-Centric Digital Systems Charter (Re-founding)
        ↓
EASA/ESA AI Governance Standard (Aviation-Specific)
        ↓
EAARF Charter (Industry Collaboration)
        ↓
Technical Controls & Roadmaps (Implementation)
```

---

## Key Principles

### From Digital Constitution:
- **Human labor founds** → Capital finances → Technology serves → The person progresses
- Human harm has absolute precedence
- Automation proposes; humans authorize
- No responsibility gaps

### From Human-Centric Digital Systems Charter:
1. **Human agency first**
2. **Truth and verifiability second**
3. **Commercial function third**

**One-line doctrine:**  
*Systems that mediate human cognition must be governed as civic infrastructure, not optimized as extraction machinery.*

---

## Implementation Status

| Document | Status | Version | Last Updated |
|----------|--------|---------|--------------|
| Human-Centric Digital Systems Charter | ✅ ACTIVE | 1.0.0 | 2026-02-12 |
| HCDS Technical Controls | ✅ ACTIVE | 1.0.0 | 2026-02-12 |
| HCDS 90-Day Roadmap | ✅ ACTIVE | 1.0.0 | 2026-02-12 |
| EAARF Charter | 📝 DRAFT | 0.1 | [Date] |
| EASA/ESA AI Governance Standard | 📝 DRAFT | 1.0 | [Date] |
| NPA 2025-07 Response | 📝 DRAFT | - | [Date] |

---

## Compliance and Audit

### Human-Centric Digital Systems Charter

**KPIs (Tracked Monthly):**
1. **ULTR** (User-Level Targeting Rate): Target ≤ 10% Year 1, → 0% Year 4
2. **CDS** (Contextual Delivery Share): Target ≥ 90% Year 1, → 98% Year 4
3. **MIR** (Manipulation Incident Rate): Continuous decline
4. **EC** (Explainability Coverage): Target 100% for all decisions
5. **AASI** (Ad/Assist Separation Integrity): Target 100% (zero tolerance)
6. **PICS** (Public-Interest Compute Share): Target 15% Year 1, → 30% Year 4

**Audit Frequency:**
- Internal audits: Monthly (CCO)
- Third-party audits: Quarterly
- Public reporting: Monthly (KPIs), Quarterly (comprehensive)

**Public Dashboards:**
- Charter Compliance: `https://aerospacemodel.org/charter-compliance`
- PICS Tracking: `https://aerospacemodel.org/charter-compliance/pics`
- Ad Repository: `https://aerospacemodel.org/ads`

---

## Integration with Existing Governance

### Digital Constitution Mapping

| HCDS Charter | Digital Constitution |
|--------------|---------------------|
| Human agency first | Article 1 (Human Labor as Foundation) |
| Purpose Constraint | Article 3 (Technology as Servant) |
| Inference Boundary | Article 6 (Human Harm Precedence) |
| Cognitive Integrity | Article 8 (Prohibition of Human Exclusion) |
| Explainability Right | Article 5 (Traceability and Accountability) |
| Functional Separation | Article 10 (Governance by Explicit Limits) |

### BREX Decision Rules

New BREX rules for charter compliance:
- **HCDS-001:** User-level targeting requires explicit consent (Article 3)
- **HCDS-002:** Vulnerability signals must not be used (Article 2)
- **HCDS-003:** Explainability must be available (Article 5)
- **HCDS-004:** Assistant and ad systems must be separated (Article 6)
- **HCDS-005:** Dark patterns must not be deployed (Article 4)
- **HCDS-006:** PICS minimum must be met (Article 8)

### Lifecycle Gates

New charter compliance gates:
- **LC02:** G-HCDS-MANIPULATION-SCAN (Article 4 compliance)
- **LC04:** G-HCDS-SEPARATION-DESIGN (Article 6 compliance)
- **LC06:** G-HCDS-EXPLAINABILITY-COVERAGE (Article 5 compliance)
- **LC08:** G-HCDS-AASI-TESTS (Article 6 compliance)

---

## Charter Compliance Office (CCO)

**Contact:** charter-compliance@aerospacemodel.org

**Responsibilities:**
- Monitor all charter KPIs
- Conduct internal audits and investigations
- Coordinate third-party audits
- Manage public reporting and transparency
- Enforce sanctions for violations

**Authority:**
- Can halt non-compliant features pending review
- Reports to executive leadership and board
- Independent from product and engineering teams

**Reporting:**
- Monthly: KPI dashboards (public)
- Quarterly: Comprehensive compliance reports (public)
- Annual: Year-end report and next year targets (public)

---

## Legal and Regulatory Alignment

### EU AI Act
- High-Risk systems: Full Article 8-15 compliance
- Limited-Risk systems: Article 13 transparency compliance
- Prohibited practices: Article 5 alignment (no vulnerability exploitation)

### GDPR
- Data minimization: Contextual-only default (Art. 5(1)(c))
- Purpose limitation: Purpose constraint enforced (Art. 5(1)(b))
- Transparency: Explainability exceeds requirements (Art. 12-14)
- Data subject rights: Portable preferences (Art. 15-22)

### Aviation-Specific
- EASA AI Roadmap 2.0: Safety-critical AI governance
- DO-178C: Software certification for airborne systems
- ARP4761: Safety assessment processes
- CS-25: Certification specifications for large aeroplanes

---

## Related Documents

| Document | Location |
|----------|----------|
| Root Governance | `../GOVERNANCE.md` |
| Digital Constitution | `../Model_Digital_Constitution.md` |
| NGI Policy System | `../policy/ngi_policy_v1.yaml` |
| Master BREX Authority | `../ASIT/GOVERNANCE/master_brex_authority.yaml` |
| HCDS Technical Controls | `../policy/hcds_technical_controls_v1.yaml` |
| HCDS 90-Day Roadmap | `../roadmaps/HCDS_90_DAY_TRANSITION_ROADMAP_v1.md` |

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-02-12 | AEROSPACEMODEL Project | Initial governance directory structure |

---

*Governed by the AEROSPACEMODEL Digital Constitution.*  
*Committed to human agency, truth, and ethical commerce.*
