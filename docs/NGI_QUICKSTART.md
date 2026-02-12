# NGI Policy Compliance - Quick Start Guide

## 5-Minute Setup

### 1. Check Your Current Score

```bash
python scripts/ngi_evaluator.py \
  --policy policy/ngi_policy_v1.yaml \
  --assessment assessments/ngi_assessment.yaml \
  --out /tmp/result.yaml

cat /tmp/result.yaml
```

**Current project score: 70/100 (PASS)** ✅

### 2. Understanding Your Assessment

Open `assessments/ngi_assessment.yaml` to see:
- Current scores per domain (0-5)
- Evidence supporting each score
- Notes explaining the rating

### 3. Run Tests

```bash
python -m pytest tests/test_ngi_evaluator.py -v
```

All tests should pass ✅

### 4. Try the Workflow

The workflow runs automatically on PRs to `main`, or trigger manually:

```bash
# Via GitHub UI: Actions → NGI Autoassessment → Run workflow
```

## Decision Guide

### PASS ✅ (Score >= 70, all hard gates pass)
- ✅ PR can merge
- ✅ Can deploy to staging
- ✅ Can deploy to production
- 🎖️ Trust badge awarded

### WARN ⚠️ (Score < 70, but hard gates pass)
- ✅ PR can merge
- ✅ Can deploy to staging
- ❌ Cannot deploy to production
- 📊 Improvement tracking enabled

### BLOCK 🛑 (Any hard gate fails)
- ❌ PR cannot merge
- ❌ No deployment allowed
- 🚨 Immediate action required

## Hard Gates (Must be >= 3)

1. **D1 - Verificability**: Claims must be traceable
2. **D3 - Privacy**: Data protection required
3. **D4 - Security**: Security controls mandatory
4. **D7 - Identity**: Legal entity verified

## Quick Improvements

### Boost 1 Point (~2 points)
Pick any domain with score 3 and improve to 4:
- Add KPI tracking
- Implement monitoring
- Document metrics

**Example: Improve D2 (Transparency)**
- Current: 3 (basic documentation)
- Target: 4 (KPI-tracked)
- Action: Add documentation coverage metrics
- Impact: +2 points → 65/100

### Boost 2 Points (~2 points)
Improve D8 (Sustainability) from 2 to 4:
- Add resource metrics per service
- Document optimization strategies
## Current Status

**Project score: 70/100 (PASS)** ✅  
**Maturity level: L3 - Operación Gobernada**

### Recent Improvements

1. **D8 Sustainability: 2 → 3** (+1.0 point)
   - Added per-service resource metrics
   - Documented optimization strategy (30% reduction target)
   - Established carbon impact baseline (438 kg CO2e/year)

2. **D1 Verificability: 3 → 4** (+3.0 points)
   - Implemented KPI tracking (10 strategic metrics)
   - Added real-time monitoring dashboards
   - Created comprehensive metrics reference

3. **D4 Security: 3 → 4** (+3.0 points)
   - Established security KPIs and SLAs
   - Deployed 24/7 threat monitoring
   - Documented vulnerability tracking

### Maintain PASS Status

To keep 70/100 score:
- Review metrics quarterly
- Track KPIs monthly
- Update evidence as improvements are made
- Address any degradation immediately

### Reach L4 (75+)

To advance to L4 (Gestión Avanzada Metricas):
1. D2 Transparency: 3 → 4 (+2.0 points)
2. D7 Identity: 3 → 4 (+2.0 points)
3. D9 Anti-misinformation: 3 → 4 (+2.0 points)

**Result: 76/100 → L4 ✅**

## Evidence Checklist

### Current Evidence for D8 (Sustainability)

- [x] Resource metrics: `docs/sustainability/RESOURCE_METRICS.md`
- [x] Optimization strategy: `docs/sustainability/OPTIMIZATION_STRATEGY.md`
- [x] Carbon analysis: `docs/sustainability/CARBON_IMPACT_ANALYSIS.md`

### Current Evidence for D1 (Verificability)

- [x] KPI tracking: `docs/verification/KPI_TRACKING.md`
- [x] Monitoring dashboard: `docs/verification/MONITORING_DASHBOARD.md`
- [x] Metrics reference: `docs/verification/METRICS.md`

### Current Evidence for D4 (Security)

- [x] KPI tracking: `docs/security/KPI_TRACKING.md`
- [x] Monitoring: `docs/security/MONITORING.md`
- [x] Metrics: `docs/security/METRICS.md`

### Future Evidence for D2 (Transparency)

- [ ] Add documentation coverage report
- [ ] Create API changelog
- [ ] Add decision log (ADRs)
- [ ] Update assessment: D2 score to 4

## Update Your Assessment

1. Edit `assessments/ngi_assessment.yaml`
2. Update scores based on improvements
3. Add new evidence file paths
4. Add notes explaining the upgrade

```yaml
D8_sustainability:
  score: 3  # Changed from 2
  evidence:
    - "GOVERNANCE.md"
    - "ops/resource_metrics.yaml"  # New
    - "docs/optimization_strategy.md"  # New
  notes: "Added resource tracking and optimization documentation"
```

5. Re-evaluate:

```bash
python scripts/ngi_evaluator.py \
  --policy policy/ngi_policy_v1.yaml \
  --assessment assessments/ngi_assessment.yaml \
  --out /tmp/result.yaml
```

6. Check the decision:

```bash
grep publish_decision /tmp/result.yaml
```

## Next Steps

1. **Review** the [complete documentation](NGI_POLICY_SYSTEM.md)
2. **Improve** domains with low scores
3. **Monitor** CI/CD workflow results
4. **Track** progress toward PASS status

## Common Questions

**Q: Can I change the policy?**
A: Yes, but requires consensus. Policy changes affect all projects.

**Q: Can I override BLOCK?**
A: No. BLOCK means critical requirements are not met. Fix the issues first.

**Q: How often should I reassess?**
A: The workflow runs on every PR. Manual reassessment when you make improvements.

**Q: What if evidence doesn't exist yet?**
A: Create it! The system guides you toward building necessary artifacts.

**Q: Can I skip a domain?**
A: No. All 9 domains require minimum score of 2. Hard gates require 3.

## Help & Support

- 📖 Documentation: `docs/NGI_POLICY_SYSTEM.md`
- 🔍 Policy Details: `policy/README.md`
- 📝 Assessment Guide: `assessments/README.md`
- 🧪 Run Tests: `pytest tests/test_ngi_evaluator.py -v`
