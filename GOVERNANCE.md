# GOVERNANCE.md

## Purpose

This document defines **operational governance** for the AEROSPACEMODEL
repository. It connects the [Digital Constitution](Model_Digital_Constitution.md)
to enforceable engineering constraints embedded in CI/CD pipelines,
PR workflows, and governance code.

---

## 1. Governing Documents

| Document | Scope | Location |
|----------|-------|----------|
| Digital Constitution | Foundational axiom, articles, limits | [`Model_Digital_Constitution.md`](Model_Digital_Constitution.md) |
| **Human-Centric Digital Systems Charter** | **Re-founding framework for digital ecosystems** | [`Governance/HUMAN_CENTRIC_DIGITAL_SYSTEMS_CHARTER_v1.0.md`](Governance/HUMAN_CENTRIC_DIGITAL_SYSTEMS_CHARTER_v1.0.md) |
| **Domain Bifurcation & Boundary Rules Charter** | **Canonical boundary rules for aircraftmodel.eu / aerospacemodel.com domain separation** | [`Governance/GOV-CHARTER-SPLIT-001.md`](Governance/GOV-CHARTER-SPLIT-001.md) |
| Contributing Guide | Contribution process, CoDevOps model | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Master BREX Authority | BREX decision rules | [`ASIT/GOVERNANCE/master_brex_authority.yaml`](ASIT/GOVERNANCE/master_brex_authority.yaml) |
| Contract Schema | Contract structure | [`ASIT/CONTRACTS/CONTRACT_SCHEMA.yaml`](ASIT/CONTRACTS/CONTRACT_SCHEMA.yaml) |
| HCDS Technical Controls | Testable controls for charter compliance | [`policy/hcds_technical_controls_v1.yaml`](policy/hcds_technical_controls_v1.yaml) |
| HCDS 90-Day Roadmap | Transition implementation plan | [`roadmaps/HCDS_90_DAY_TRANSITION_ROADMAP_v1.md`](roadmaps/HCDS_90_DAY_TRANSITION_ROADMAP_v1.md) |

---

## 2. Enforcement Mechanisms

### 2.1 Commit-as-Contract (Art. 4)

Every commit is a human commitment. The CI pipeline validates:

- **Authorship**: Commits must have a verified author identity.
- **Rationale**: PRs must include declared intent per the
  [PR template](.github/PULL_REQUEST_TEMPLATE.md).
- **Traceability**: Changes must be linked to issues, contracts, or
  governance decisions.

### 2.2 Labor Reabsorption (Art. 1 & 8)

The PR template includes a **LABOR-REABSORPTION** section requiring:

| Field | Description |
|-------|-------------|
| Roles displaced (FTE-equivalent) | Quantified human roles affected |
| Roles created or capacity expanded | New roles or expanded capacity |
| Transition pathway | How affected contributors transition |
| Net displacement | Must be ≤ 0 for merge without override |

**Enforcement**: PRs with net displacement > 0 require an explicit
governance override commit by the repository steward, per Art. 11.

### 2.3 Constitutional Compliance Checklist

Every PR includes a constitutional compliance checklist covering
Articles 1–9. This is validated by CI as a structural check.

### 2.4 Harm Precedence (Art. 6)

When uncertainty exists and human harm is plausible:

- **Escalation target**: A named stakeholder role (STK_SAF) with
  response SLA, not a queue.
- **Threshold**: Bayesian confidence < 0.92 on safety-critical
  outputs triggers auto-escalation.
- **Response SLA**: 48 hours for safety content review.

### 2.5 Constitutional Boundary Protection (Art. 10)

To prevent drift that violates the foundational axiom:

- **Constitution hash**: The SHA-256 hash of
  `Model_Digital_Constitution.md` is validated in CI on every PR.
  Changes to the constitution require explicit rationale.
- **Downstream attestation**: Derivative works should include a
  DCO-style attestation affirming compliance with the Digital
  Constitution.

---

## 3. Conflict Resolution (Art. 11)

When capital demands contradict the foundational axiom:

1. The repository steward issues an explicit commit accepting
   responsibility for the axiom deviation, with documented rationale
   and remediation timeline; **or**
2. The capital contributor withdraws the conflicting demand.

**No silent override is permitted.** See Art. 11 of the
[Digital Constitution](Model_Digital_Constitution.md).

---

## 4. Metrics and Measurement

### 4.1 Operational Metrics

| Metric | Target | Rationale |
|--------|--------|-----------|
| Mean time to human intervention | Track downward trend | Detects over-automation (Art. 3) |
| Contributor role diversity | Cognitive, creative, maintenance roles represented | Prevents role erosion (Art. 8) |
| Reversibility latency | < 1 business day | Time to roll back harmful change (Art. 6) |
| Constitution hash stability | Hash unchanged unless explicit commit | Boundary protection (Art. 10) |

### 4.2 ROC (Return on Contribution)

See [CONTRIBUTING.md §6](CONTRIBUTING.md) for the ROC framework,
including UAF calibration and anti-gaming guardrails.

---

## 5. Escalation Procedures

| Trigger | Target | SLA | Reference |
|---------|--------|-----|-----------|
| Safety-critical content | STK_SAF | 48 hours | BREX SAFETY-002 |
| Baseline modification | CCB | 5 business days | BREX BL-002 |
| Undefined BREX condition | STK_CM | HALT until resolved | Master BREX |
| Capital-axiom conflict | Repository steward | Per Art. 11 | Constitution Art. 11 |
| Labor displacement > 0 | Repository steward | Before merge | Constitution Art. 1, 8 |

---

## 6. Regulatory Alignment

This governance framework preempts regulatory requirements:

| Regulation | Alignment |
|------------|-----------|
| EU AI Act (Art. 13–14) | Human oversight baked into commit-as-contract model |
| EASA AI Roadmap | Traceability to design intent via BREX + constitution |
| DO-178C | Contract-governed transformations with audit trails |
| ARP4761 | Safety-critical escalation with named stakeholders |

---

## 7. Evolution

This governance document evolves through explicit commits with
documented rationale, consistent with the Digital Constitution's
[Foundational Intent and Evolution](Model_Digital_Constitution.md)
clause.

Changes require:
- Compatibility with the foundational axiom
- Clear benefit to affected stakeholders
- No introduction of human harm, exclusion, or accountability loss

---

*Governed by the AEROSPACEMODEL Digital Constitution.*
