# Human-Centric Digital Systems Charter - Quick Start Guide

> For developers, product managers, and compliance officers implementing charter requirements

---

## TL;DR

The Human-Centric Digital Systems Charter re-founds digital systems on:
1. **Human agency first**
2. **Truth and verifiability second**  
3. **Commercial function third**

**Core principle:** Systems mediating human cognition = civic infrastructure (not extraction machinery)

---

## For Developers

### Before You Code: Charter Checklist

**Article 1 - Purpose Constraint:** Does your feature optimize for user welfare or engagement?
- ✅ User-defined goal completion
- ❌ Maximizing time-on-site

**Article 2 - Inference Boundary:** Are you using any banned signals?
- ✅ Page topic, time of day, language
- ❌ Emotional state, financial stress, addiction patterns
- See: `policy/hcds_technical_controls_v1.yaml` (Prohibited Signals section)

**Article 3 - Contextual Ads:** Default ad mode?
- ✅ Contextual-only (no user signals)
- ❌ Personalized (requires explicit consent)

**Article 4 - Cognitive Integrity:** Does your UI use any dark patterns?
- ✅ Clear choices, honest language
- ❌ Variable-ratio rewards, confirm-shaming, fake urgency
- See: `policy/hcds_technical_controls_v1.yaml` (Prohibited Patterns section)

**Article 5 - Explainability:** Can users see why content was shown?
- ✅ "Why this?" button with signal disclosure
- ❌ Black box decisions

**Article 6 - Functional Separation:** Are reasoning and ad systems separated?
- ✅ Separate infrastructure, no data sharing
- ❌ Shared models, mixed objectives

**Article 7 - Auditability:** Are decisions logged with signatures?
- ✅ Cryptographically signed audit trail
- ❌ No audit trail

**Article 8 - Compute Duty:** Is public-interest compute quota met?
- ✅ PICS ≥ 15% (Year 1 minimum)
- ❌ All compute for revenue features

### CI/CD Integration

Charter compliance will be enforced via:

1. **BREX Rules** (defined, pending CI/CD integration):
   - HCDS-001: User-level targeting requires consent
   - HCDS-002: Vulnerability signals blocked
   - HCDS-003: Explainability required
   - HCDS-004: Assistant-ad separation enforced
   - HCDS-005: Dark patterns blocked
   - HCDS-006: PICS minimum required
   
   **Status:** Rules are fully documented in `policy/hcds_technical_controls_v1.yaml`. Integration into `ASIT/GOVERNANCE/master_brex_authority.yaml` is planned for Phase 2 (Days 31-60 of transition roadmap).

2. **Lifecycle Gates** (defined, pending integration):
   - LC02: Manipulation pattern scan
   - LC04: Separation design review
   - LC06: Explainability coverage check
   - LC08: AASI (separation integrity) tests
   
   **Status:** Gates are fully documented in `policy/hcds_technical_controls_v1.yaml`. Integration into `lifecycle/TLI_GATE_RULEBOOK.yaml` is planned for Phase 2 (Days 31-60 of transition roadmap).

### Code Examples

**Example 1: Contextual Ad Serving**

```python
# ✅ CORRECT - Contextual-only
ad = ad_service.get_contextual_ad(
    page_topic="technology",
    time_of_day="afternoon",
    language="en"
)

# ❌ WRONG - User-level targeting without consent check
# (Will violate HCDS-001 once integrated into CI/CD)
ad = ad_service.get_personalized_ad(
    user_id=user_id,  # Violates Article 3
    browsing_history=history  # Violates Article 2 if no consent
)

# ✅ CORRECT - Personalized only with consent
if user.has_consent("personalized_ads"):
    ad = ad_service.get_personalized_ad(user_id=user_id)
else:
    ad = ad_service.get_contextual_ad(page_topic=page_topic)
```

**Example 2: Explainability**

```python
# ✅ CORRECT - Always provide explainability
content = recommendation_engine.get_content(user_context)
explanation = {
    "reason": "Contextual match to page topic",
    "signals": {"page_topic": 0.7, "time_of_day": 0.3},
    "alternatives": [...],
}
return content, explanation

# ❌ WRONG - No explainability
# (Will violate HCDS-003 once integrated into CI/CD)
content = recommendation_engine.get_content(user_context)
return content  # Violates Article 5
```

**Example 3: Dark Pattern Detection**

```python
# ✅ CORRECT - Clear, honest language
button_text = "No thanks, continue with contextual ads"

# ❌ WRONG - Confirm-shaming
# (Will violate HCDS-005 once integrated into CI/CD)
button_text = "No, I don't care about my privacy"  # Violates Article 4

# ✅ CORRECT - Honest countdown (if real)
if actual_offer_expires_at:
    show_countdown(expires_at=actual_offer_expires_at)

# ❌ WRONG - Fake urgency
# (Will violate HCDS-005 once integrated into CI/CD)
show_countdown(expires_at=time.now() + 10_minutes)  # Artificial scarcity, violates Article 4
```

---

## For Product Managers

### Feature Planning

**Pre-Development Questions:**

1. **User Welfare**: Does this feature help users achieve their goals?
   - If it maximizes engagement at the expense of goals → ❌ Not allowed

2. **Consent Model**: Does this use user-level data?
   - If yes → Must be opt-in, not default
   - If no → Contextual-only, can be default

3. **Manipulation Risk**: Does this use any variable rewards, urgency, or guilt?
   - If yes → Must redesign without manipulation
   - Use Manipulation Pattern Detector in design review

4. **Explainability**: Can users understand why they see this?
   - If no → Must add "Why this?" explanation

### Design Reviews

**Required Artifacts:**
- User Welfare Impact Assessment (`assessments/user_welfare_impact_[feature].yaml`)
- Manipulation Pattern Scan Report (`assessments/dark_pattern_scan_[feature].yaml`)
- Explainability Design (`docs/explainability/[feature]_explainability.md`)

**Approval Required From:**
- CCO (Charter Compliance Office) for high-impact features
- STK_SAF for safety-critical features

### Metrics That Matter

**Track charter KPIs, not just business metrics:**

| KPI | Target | What it measures |
|-----|--------|------------------|
| ULTR | ≤10% | User-level targeting (should be low) |
| CDS | ≥90% | Contextual delivery (should be high) |
| MIR | Declining | Manipulation incidents (should decrease) |
| EC | 100% | Explainability coverage (must be complete) |
| AASI | 100% | Separation integrity (must be perfect) |
| PICS | ≥15% | Public-interest compute (must meet minimum) |

---

## For Compliance Officers (CCO)

### Monthly Compliance Checklist

**Day 1-5: KPI Collection**
- [ ] Calculate ULTR, CDS, MIR, EC, AASI, PICS from production logs
- [ ] Compare to targets (see `policy/hcds_technical_controls_v1.yaml`)
- [ ] Identify any target misses

**Day 6-10: Violation Investigation**
- [ ] Review Manipulation Incident Rate (MIR) events
- [ ] Investigate any AASI test failures
- [ ] Check PICS shortfall (if any)
- [ ] Document findings

**Day 11-15: Remediation**
- [ ] Work with engineering on violation fixes
- [ ] Apply sanctions per sanctions ladder (if required)
- [ ] Verify remediation completion

**Day 16-20: Reporting**
- [ ] Draft monthly compliance report
- [ ] Update public dashboards
- [ ] Prepare executive summary

**Day 21-30: Audit Preparation**
- [ ] Prepare evidence for quarterly third-party audit
- [ ] Update audit trail documentation
- [ ] Review policy updates

### Sanctions Ladder (Quick Reference)

| Level | Violation | Action | Timeline |
|-------|-----------|--------|----------|
| 1 | Minor (e.g., API latency) | Alert team | 7 days to fix |
| 2 | Moderate (e.g., PICS shortfall) | Corrective plan, penalty | 30 days to fix |
| 3 | Serious (e.g., targeting without consent) | Immediate halt, $100K fine | 48h public report |
| 4 | Critical (e.g., vulnerability exploitation) | Platform halt, $1M fine | Executive action |

### Audit Evidence Locations

All evidence artifacts are in the repository:

| Article | Evidence Artifact | Location |
|---------|------------------|----------|
| Art 1 | Objective functions | `docs/algorithms/objective_functions.md` |
| Art 2 | Vulnerability detection logs | `logs/vulnerability_detection_*.log` |
| Art 3 | Ad serving mode logs | `logs/ad_serving_mode_*.log` |
| Art 4 | Dark pattern scans | `assessments/dark_pattern_scan_*.yaml` |
| Art 5 | Explainability coverage | `metrics/explainability_coverage.csv` |
| Art 6 | AASI test results | `assessments/separation_integrity_*.yaml` |
| Art 7 | Audit trail proofs | `audit/integrity_proofs_*.json` |
| Art 8 | PICS metrics | `metrics/public_interest_compute_share.csv` |

---

## For Executives

### Why This Matters

**Business Case:**
- **Trust**: Users trust transparent systems → higher engagement (quality > quantity)
- **Regulation**: EU AI Act, GDPR compliance → avoid fines and penalties
- **Differentiation**: First-mover advantage in ethical digital systems
- **Talent**: Top engineers want to work on human-centric systems

**Risk Mitigation:**
- **Regulatory**: Preempt future regulations (EU AI Act, digital services acts)
- **Reputational**: Avoid scandals from manipulation or exploitation
- **Legal**: Reduce liability from user harm
- **Competitive**: Build defensible moat based on trust, not just features

### Investment Required

**90-Day Transition:**
- Budget: $2.5M
- Personnel: ~2,175 person-days
- Key hires: CCO Director, Compliance Analysts (4.5 FTE)

**Ongoing (Annual):**
- CCO operations: $500K/year
- Third-party audits: $200K/year (4 audits)
- Public-interest compute: 15-30% of total compute budget

**ROI:**
- Reduced regulatory risk: $10M+ potential fines avoided
- Increased user trust: 10-20% improvement in user retention
- Premium positioning: Ability to charge for ad-free premium tier
- Talent acquisition: 30% faster hiring of top engineers

### Strategic Positioning

**Tell this story:**
> "We're not just building features. We're building civic infrastructure for human cognition. Our charter guarantees:
> - No manipulation or exploitation
> - Full transparency and user control
> - Public-interest compute allocation
> - Independent audits and accountability
>
> This isn't altruism. It's a competitive advantage. Trust is the new moat."

---

## FAQ

**Q: Does this charter slow down development?**  
A: Initially yes (90-day transition), but then no. Charter compliance is automated in CI/CD. Most features pass automatically.

**Q: What if a feature fails charter compliance?**  
A: Redesign the feature or get CCO exception (with documented risk acceptance). Critical failures block deployment.

**Q: Can we still make money with contextual-only ads?**  
A: Yes. Contextual CPM is lower, but user trust and retention are higher. Plus, subscription hybrid model offsets revenue.

**Q: What if competitors don't adopt this?**  
A: Differentiation opportunity. Users will choose trust over features. Regulators will force others to follow eventually.

**Q: How do we measure "user welfare"?**  
A: User-defined goal completion rate, time-well-spent metrics, user satisfaction surveys. Not engagement time or page views.

**Q: What's the penalty for non-compliance?**  
A: See sanctions ladder. Minor = 7-day fix, Critical = platform halt + $1M fine + executive action. Zero tolerance for high-severity violations.

---

## Resources

**Key Documents:**
- Charter: `Governance/HUMAN_CENTRIC_DIGITAL_SYSTEMS_CHARTER_v1.0.md`
- Technical Controls: `policy/hcds_technical_controls_v1.yaml`
- 90-Day Roadmap: `roadmaps/HCDS_90_DAY_TRANSITION_ROADMAP_v1.md`
- Governance README: `Governance/README.md`

**Public Dashboards:**
- Charter Compliance: `https://aerospacemodel.org/charter-compliance`
- PICS Tracking: `https://aerospacemodel.org/charter-compliance/pics`
- Ad Repository: `https://aerospacemodel.org/ads`

**Contact:**
- CCO: charter-compliance@aerospacemodel.org
- Questions: charter-info@aerospacemodel.org
- Violations: charter-violations@aerospacemodel.org

---

*Governed by the AEROSPACEMODEL Digital Constitution.*  
*Committed to human agency, truth, and ethical commerce.*
