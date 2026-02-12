# Verification Metrics Reference

## Overview

Comprehensive reference for all verification and traceability metrics tracked in the AEROSPACEMODEL project.

**Purpose**: Define metrics, formulas, thresholds, and interpretation guidelines  
**Audience**: QA Team, Engineers, Project Managers  
**Maintenance**: Updated quarterly

## Metric Categories

### 1. Coverage Metrics

#### 1.1 Traceability Coverage

**Definition**: Completeness of requirement-to-artifact trace links

**Formula**:
```
Coverage = (Requirements with forward traces / Total requirements) × 100
```

**Data Source**: Lifecycle Manager trace database

**Collection**: Automated, daily scan

**Thresholds**:
- 🔴 Critical: < 95%
- 🟡 Warning: 95-97.9%
- 🟢 Good: 98-99.9%
- ⭐ Excellence: 100%

**Current**: 97.5%

---

#### 1.2 Test Coverage

**Definition**: Percentage of code covered by automated tests

**Types**:
- Unit test coverage
- Integration test coverage
- End-to-end test coverage

**Formula**:
```
Coverage = (Lines executed in tests / Total lines of code) × 100
```

**Data Source**: pytest-cov, coverage.py

**Thresholds**:
- Unit: ≥ 90%
- Integration: ≥ 80%
- E2E: ≥ 70%

**Current**: 
- Unit: 94.2%
- Integration: 87.5%
- E2E: 78.3%

---

#### 1.3 Document Coverage

**Definition**: Percentage of code modules with complete documentation

**Formula**:
```
Coverage = (Modules with docs / Total modules) × 100
```

**Requirements**:
- Module docstring
- Function docstrings
- Complex algorithm explanation
- Usage examples

**Current**: 91.7%

---

### 2. Quality Metrics

#### 2.1 Gate Pass Rate

**Definition**: First-time pass rate for lifecycle gates

**Formula**:
```
Pass Rate = (Gates passed on first submission / Total submissions) × 100
```

**Data Source**: Lifecycle Manager

**Breakdown by Gate**:
```
LC02 (Requirements): 92.3%
LC04 (Design/DBL): 78.5%
LC06 (Conformity): 85.7%
LC08 (Integration): 80.1%
LC10 (Industrial): 88.9%
```

**Target**: > 80% overall

**Current**: 83.4%

---

#### 2.2 Defect Density

**Definition**: Defects per unit of work

**Formula**:
```
Defect Density = (Defects found / Size) × 1000
```

**Size Metrics**:
- Code: Lines of code (LOC)
- Docs: Words
- Requirements: Number of requirements

**Thresholds**:
- Code: < 2 defects/KLOC
- Docs: < 5 defects/1K words
- Specs: < 3 defects/100 req

**Current**:
- Code: 1.4 defects/KLOC
- Docs: 4.2 defects/1K words
- Specs: 2.8 defects/100 req

---

#### 2.3 Rework Rate

**Definition**: Artifacts requiring rework after verification

**Formula**:
```
Rework Rate = (Artifacts with rework / Total reviewed) × 100
```

**Data Source**: Verification review logs

**Target**: < 20%

**Current**: 16.6%

**Breakdown**:
- Code: 12.3%
- Documentation: 18.9%
- Specifications: 22.1%

---

### 3. Efficiency Metrics

#### 3.1 Verification Cycle Time

**Definition**: Time from artifact creation to verification completion

**Measurement**: Days (business days)

**Formula**:
```
Cycle Time = Verification Complete Date - Artifact Created Date
```

**Targets**:
- Critical: < 2 days
- Standard: < 5 days
- Documentation: < 10 days

**Current**:
- Critical: 1.8 days
- Standard: 6.2 days
- Documentation: 7.3 days

**Percentiles**:
- P50: 3.2 days
- P75: 5.8 days
- P90: 9.1 days
- P95: 12.4 days

---

#### 3.2 Review Throughput

**Definition**: Number of reviews completed per time period

**Formula**:
```
Throughput = Reviews Completed / Time Period
```

**Data Source**: Review system logs

**Current**: 
- Daily: 12.3 reviews
- Weekly: 86 reviews
- Monthly: 372 reviews

**Capacity**: 15 reviews/day (sustained)

---

#### 3.3 Automation Rate

**Definition**: Percentage of checks performed automatically

**Formula**:
```
Automation = (Automated checks / Total checks) × 100
```

**Breakdown**:
- Format validation: 100%
- Schema checks: 100%
- Hash verification: 100%
- Trace validation: 95%
- Code quality: 85%
- Design review: 20%
- Safety assessment: 10%

**Overall**: 68.5%

**Target**: 80% by Q4 2026

---

### 4. Integrity Metrics

#### 4.1 Baseline Integrity

**Definition**: Baselined items with verified cryptographic integrity

**Formula**:
```
Integrity = (Items with valid hash/sig / Total baselined) × 100
```

**Verification Methods**:
- SHA-256 hash
- GPG signature
- Timestamp verification

**Current**: 99.1%

**Issues**: 14 items pending hash generation

---

#### 4.2 Trace Link Validity

**Definition**: Trace links that are current and semantically correct

**Measurement**: Monthly audit of random sample (n=100)

**Criteria**:
- Link exists in database
- Referenced artifacts exist
- Semantic relationship correct
- No circular dependencies
- Timestamps current

**Current**: 96.8% valid

---

#### 4.3 Artifact Consistency

**Definition**: Agreement between artifact versions across systems

**Formula**:
```
Consistency = (Matching artifacts / Total checked) × 100
```

**Systems Checked**:
- Git repository
- Baseline database
- Archive storage
- Backup systems

**Current**: 99.5%

---

### 5. Compliance Metrics

#### 5.1 Standard Compliance

**Definition**: Adherence to regulatory and industry standards

**Standards Tracked**:

```
┌──────────────┬────────────┬──────────┬─────────┐
│ Standard     │ Compliance │ Gaps     │ Status  │
├──────────────┼────────────┼──────────┼─────────┤
│ S1000D 5.0   │ 98.5%      │ 12       │ 🟢      │
│ DO-178C      │ 96.2%      │ 28       │ 🟢      │
│ ARP4754A     │ 94.8%      │ 35       │ 🟡      │
│ ARP4761      │ 97.1%      │ 19       │ 🟢      │
│ EU AI Act    │ 92.3%      │ 47       │ 🟡      │
└──────────────┴────────────┴──────────┴─────────┘
```

**Overall**: 95.8% compliance

---

#### 5.2 Evidence Completeness

**Definition**: Required evidence artifacts present for certification

**Formula**:
```
Completeness = (Present artifacts / Required artifacts) × 100
```

**Categories**:
- Requirements: 98.2%
- Design: 95.7%
- Verification: 96.8%
- Safety: 94.3%
- Quality: 97.1%

**Overall**: 96.4%

---

### 6. Performance Metrics

#### 6.1 Tool Response Time

**Definition**: Average time for verification tools to complete

**Measurement**: Seconds

**Targets**:
- BREX Validator: < 3s
- Schema Checker: < 1s
- Trace Validator: < 2s
- Hash Generator: < 0.5s

**Current**:
- BREX Validator: 2.3s
- Schema Checker: 0.8s
- Trace Validator: 1.5s
- Hash Generator: 0.3s

---

#### 6.2 System Availability

**Definition**: Uptime of verification infrastructure

**Formula**:
```
Uptime = (Total time - Downtime) / Total time × 100
```

**Target**: 99.5%

**Current**: 99.7%

**MTTR** (Mean Time To Recovery): 1.2 hours

---

## Data Collection

### Automated Collection

**Frequency**: Every 5 minutes for most metrics

**Methods**:
- GitHub API polling
- CI/CD webhooks
- Database queries
- Log analysis
- Custom collectors

### Manual Collection

**Frequency**: Monthly audits

**Methods**:
- Sampling reviews
- Compliance checks
- Quality assessments

---

## Data Quality

### Accuracy

**Target**: > 99% accurate

**Validation**:
- Cross-reference multiple sources
- Spot-check against manual counts
- Automated sanity checks

**Last Audit**: 99.4% accurate (Feb 2026)

### Completeness

**Target**: 100% of required metrics collected

**Current**: 100%

### Timeliness

**Target**: Real-time or < 15 min delay

**Current**: 5 min average delay

---

## Reporting

### Dashboards

- Executive: Key metrics summary
- Operational: Real-time queues and checks
- Technical: Detailed breakdowns
- Compliance: Regulatory status

### Scheduled Reports

- Daily: Queue status, failed checks
- Weekly: KPI summary, trends
- Monthly: Comprehensive metrics report
- Quarterly: Performance review

---

## Related Documents

- [KPI Tracking](KPI_TRACKING.md)
- [Monitoring Dashboard](MONITORING_DASHBOARD.md)
- [TLI Gate Rulebook](../../lifecycle/TLI_GATE_RULEBOOK.yaml)

---

## Revision History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-02-12 | 1.0.0 | Initial metrics reference | QA Team |

---

**Next Review**: 2026-05-12  
**Contact**: qa@aerospacemodel.io
