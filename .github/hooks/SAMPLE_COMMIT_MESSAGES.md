# Sample Constitutional Commit Messages

This file demonstrates valid commit messages that comply with the Model Digital Constitution.

## Example 1: Feature Addition

```
INTENT: Add pre-commit hooks for constitutional enforcement

RATIONALE: Operationalize Model Digital Constitution by enforcing governance structure at commit time. Currently no automated validation of constitutional principles exists, leading to inconsistent adherence.

HUMAN_IMPACT: Positive impact on developer accountability. Requires 2-3 minutes additional time per commit for documentation. No workforce reduction. Increases visibility of decisions affecting people. All developers retain roles with enhanced responsibility.

REVERSIBILITY: Hooks can be bypassed with --no-verify flag in emergency situations. Can be disabled by removing .pre-commit-config.yaml. If harm detected from enforcement (e.g., blocking critical fixes), escalate to repository steward for immediate review and potential temporary bypass approval.

AUTHOR: Constitutional Governance Implementation Team (Jane Developer, John Engineer)
```

## Example 2: Bug Fix

```
INTENT: Fix calculation error in LH2 tank pressure relief validation

RATIONALE: Current implementation incorrectly calculates pressure threshold, potentially causing false alerts. Bug identified in code review of MTP-28-11-CERT-001.

HUMAN_IMPACT: Positive - reduces false alerts that distract operators. No change to operator roles or responsibilities. Improves operator experience by reducing alert fatigue.

REVERSIBILITY: Can be reverted via git revert if regression detected. If issues arise, system will degrade to conservative (lower) threshold automatically. Escalate to STK_SAF if safety concerns emerge during testing.

AUTHOR: Safety Engineering Team (Alice Smith)
```

## Example 3: Documentation Update

```
INTENT: Update README with installation instructions for new contributors

RATIONALE: Feedback from 3 new contributors indicated confusion about setup process. Missing steps for virtual environment and dependency installation.

HUMAN_IMPACT: Positive - reduces onboarding time for new contributors by approximately 30 minutes. No impact on existing workforce. Facilitates knowledge transfer and community growth.

REVERSIBILITY: Documentation changes can be reverted or updated at any time without system risk. If instructions cause confusion, escalate to maintainer team for clarification.

AUTHOR: Documentation Team (Bob Writer)
```

## Example 4: Refactoring (Automation Addition)

```
INTENT: Add automated validation for MTL token library schema

RATIONALE: Manual validation of 58 MTL tokens is error-prone and time-consuming. Automation reduces validation time from 2 hours to 5 minutes per release.

HUMAN_IMPACT: Reduces manual validation workload for 2 validation engineers. Reabsorption plan: Engineers transition to schema evolution and design review roles. 6-month training program begins Q3 2026. New capacity: Engineers gain authority over schema governance decisions previously delegated to external consultants.

REVERSIBILITY: Automated validation can be disabled by removing test suite. Manual validation procedures remain documented. If automation produces false negatives, escalate to STK_CM for immediate manual review and automation suspension until fixed.

AUTHOR: Quality Engineering Team (Charlie QA Lead) - Reabsorption plan approved by HR and Constitution Steward
```

## Example 5: Emergency Fix (with justification)

```
INTENT: Emergency patch for production cryogenic sensor reading anomaly

RATIONALE: Production system showing intermittent sensor reading failures affecting 12% of LH2 tank temperature measurements. Traced to buffer overflow in sensor data parsing. Immediate fix required per safety protocol SP-28-11-EMERG-001.

HUMAN_IMPACT: No direct workforce impact. Positive impact on operator safety - restores reliable temperature monitoring critical for cryogenic system safety. Operators maintain all current responsibilities.

REVERSIBILITY: Patch can be reverted if regression detected. System has hardware-level fallback temperature sensors per ARP4761 redundancy requirements. If patch causes issues, system will automatically degrade to hardware fallback sensors and escalate to STK_SAF for immediate review.

AUTHOR: Emergency Response Team (Diana Engineer) - Emergency protocol SP-28-11-EMERG-001 invoked, Constitution Steward notified
```

## Example 6: Efficiency Improvement (Labor-Positive)

```
INTENT: Optimize MTL token generation pipeline to reduce build time

RATIONALE: Current pipeline takes 45 minutes per build, blocking rapid iteration. Optimization through parallel processing and caching reduces to 12 minutes.

HUMAN_IMPACT: Positive - gives developers 33 minutes back per build cycle, enabling more design iteration time. No workforce reduction. Engineers gain capacity for higher-value activities: architecture design, code review, and mentoring. Build engineer role expands to include pipeline architecture responsibilities.

REVERSIBILITY: Optimization can be disabled via build flag BUILD_PARALLEL=false to revert to sequential processing. If optimization causes build instability, degrade to original pipeline automatically. Escalate to STK_CM if build failures exceed 5% threshold.

AUTHOR: DevOps Team (Eve Build Engineer) - Capacity expansion plan documented in CAPACITY_EXPANSION_Q2_2026.md
```

## Invalid Examples (Will Be Rejected)

### Invalid Example 1: Missing Required Sections

```
Add new feature for MTL validation

This adds automated validation to improve quality.
```

**Rejection Reason:** Missing INTENT, RATIONALE, HUMAN_IMPACT, REVERSIBILITY, AUTHOR sections. Violates Articles 4 and 7.

### Invalid Example 2: Workforce Reduction Without Reabsorption

```
INTENT: Automate manual validation process

RATIONALE: Reduce costs by eliminating manual validation bottleneck

HUMAN_IMPACT: Workforce reduction: 2 validation engineers eliminated. Cost savings $200K/year.

REVERSIBILITY: Can revert automation if needed, escalate to management

AUTHOR: Cost Optimization Team
```

**Rejection Reason:** Article 8 violation - workforce reduction without reabsorption pathway. Must specify how engineers will be reabsorbed, retrained, or transitioned to new roles.

### Invalid Example 3: Missing Reversibility Details

```
INTENT: Update safety-critical flight control logic

RATIONALE: Improve response time by 15%

HUMAN_IMPACT: No direct human impact, operators use same interface

REVERSIBILITY: Can be reverted

AUTHOR: Flight Control Team
```

**Rejection Reason:** Article 6 violation - REVERSIBILITY lacks specific degrade/pause/escalate mechanisms. Safety-critical changes must specify harm-mitigation paths.

### Invalid Example 4: Empty Sections

```
INTENT: Fix bug

RATIONALE: Bug exists

HUMAN_IMPACT: None

REVERSIBILITY: Revert

AUTHOR: Dev
```

**Rejection Reason:** Sections too short (< 10 characters). Lacks meaningful content required for accountability per Article 4.

## Template for Quick Copy

```
INTENT: <What this commit aims to improve - be specific>

RATIONALE: <Why this change is necessary - include context and justification>

HUMAN_IMPACT: <Effect on people: workers, users, operators - must address workforce if relevant>

REVERSIBILITY: <How to degrade/pause/escalate if harm occurs - be specific about mechanisms>

AUTHOR: <Accountable human agent(s) with name and role>
```

## Notes

1. **Section Order:** Order doesn't matter as long as all sections are present.

2. **Multi-line Sections:** Sections may span multiple lines for human readability, but the current validator only reliably checks the first line of each section. Put the key information for each section on its first line.

3. **Additional Sections:** You can add extra sections (e.g., `REFERENCES:`, `TESTING:`); they will be parsed using the same "first-line-checked" behavior, and the five required sections must still be present.

4. **Article 11 Exceptions:** If a commit violates the foundational axiom (e.g., unavoidable workforce reduction), the repository steward must issue an "axiom-responsibility commit" explicitly accepting responsibility, documenting rationale, scope, and remediation timeline.

5. **Merge Commits:** Merge commits typically inherit documentation from the PR. Constitution steward may grant blanket exception for automated merge commits.

6. **Bot Commits:** Automated commits (e.g., dependabot) may be excepted via `.constitution-ignore` with steward approval.

---

*These examples demonstrate the constitutional principle that "Legitimacy accumulates through committed responsibility, not outputs alone."*
