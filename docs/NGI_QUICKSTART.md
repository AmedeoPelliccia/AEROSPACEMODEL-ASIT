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

**Current project score: 63/100 (WARN)**

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
- Track carbon impact

**Impact: +2 points → 65/100**

### Reach PASS (70/100)
Combine improvements:
1. D8: 2 → 4 (+2.0 points)
2. D1: 3 → 4 (+3.0 points)
3. D2: 3 → 4 (+2.0 points)

**Result: 70/100 → PASS ✅**

## Evidence Checklist

### Quick Wins for D8 (Sustainability)

- [ ] Create `ops/resource_metrics.yaml` with CPU/memory per service
- [ ] Add `docs/optimization_strategy.md` documenting efficiency goals
- [ ] Generate `ops/carbon_estimate.csv` from cloud provider data
- [ ] Update assessment: D8 score to 3 or 4

### Quick Wins for D1 (Verificability)

- [ ] Document commit signing policy
- [ ] Create artifact hash manifest
- [ ] Add release verification guide
- [ ] Update assessment: D1 score to 4

### Quick Wins for D2 (Transparency)

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
