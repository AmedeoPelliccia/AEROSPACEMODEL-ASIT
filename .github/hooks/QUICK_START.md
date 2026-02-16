# Constitutional Pre-Commit Hooks - Quick Start

This guide gets you up and running with constitutional enforcement hooks in 5 minutes.

## Installation (30 seconds)

```bash
# 1. Install pre-commit framework
pip install pre-commit

# 2. Install git hooks
pre-commit install
pre-commit install --hook-type commit-msg

# 3. (Optional) Install Pylint for code checks
pip install pylint
```

## Your First Constitutional Commit (2 minutes)

### Step 1: Make a change
```bash
echo "# Test change" >> README.md
git add README.md
```

### Step 2: Write a constitutional commit message

When you run `git commit`, use this template:

```
INTENT: <What this commit aims to improve>

RATIONALE: <Why this change is necessary>

HUMAN_IMPACT: <Effect on people - workers, users, operators>

REVERSIBILITY: <How to degrade/pause/escalate if harm occurs>

AUTHOR: <Your name and role>
```

### Step 3: Example compliant message

```bash
git commit
```

In your editor, write:
```
INTENT: Update README with quick start guide for constitutional hooks

RATIONALE: New contributors need clear onboarding instructions. Current README lacks installation steps for pre-commit hooks.

HUMAN_IMPACT: Positive - reduces onboarding time for new contributors by ~30 minutes. No workforce impact. All contributors benefit from clearer documentation.

REVERSIBILITY: Documentation can be updated anytime without system risk. If instructions cause confusion, escalate to documentation team for clarification.

AUTHOR: Jane Developer, Documentation Team
```

Save and exit. The hooks will automatically validate your message.

## What Happens Next?

### ✅ If your message is valid:
```
✅ Constitutional commit validated
   INTENT: Update README with quick start guide...
   AUTHOR: Jane Developer, Documentation Team
```

Your commit succeeds!

### ❌ If your message is missing sections:
```
❌ CONSTITUTION VIOLATION (Article 4, Article 7)
Missing required sections: HUMAN_IMPACT, REVERSIBILITY

Every commit must declare its legitimacy through explicit sections:
Template:
INTENT: What this commit aims to improve
...
```

Fix your message and try again.

## Common Scenarios

### Scenario 1: Bug Fix
```
INTENT: Fix calculation error in LH2 pressure validation

RATIONALE: Current code incorrectly calculates threshold, causing false alerts

HUMAN_IMPACT: Positive - reduces alert fatigue for operators. No workforce changes.

REVERSIBILITY: Can revert via git revert. If regression detected, system degrades to conservative threshold and escalates to STK_SAF.

AUTHOR: Alice Engineer, Safety Team
```

### Scenario 2: Adding Automation
```
INTENT: Automate MTL token validation

RATIONALE: Manual validation takes 2 hours per release, is error-prone

HUMAN_IMPACT: Reduces validation workload for 2 engineers. Reabsorption: Engineers transition to schema governance roles with 3-month training starting Q3 2026.

REVERSIBILITY: Automation can be disabled. Manual procedures remain documented. If false negatives occur, escalate to STK_CM and suspend automation until fixed.

AUTHOR: Bob DevOps, approved by HR Reabsorption Committee
```

### Scenario 3: Documentation Update
```
INTENT: Update API documentation with new examples

RATIONALE: Users reporting confusion about authentication flow

HUMAN_IMPACT: Positive - improves user experience. No workforce impact.

REVERSIBILITY: Documentation can be updated anytime. If examples cause confusion, escalate to doc team for immediate clarification.

AUTHOR: Charlie Tech Writer
```

## Emergency Bypass (Use Sparingly!)

In true emergencies, you can bypass hooks:

```bash
git commit --no-verify
```

**Warning:** You MUST:
1. Have invoked emergency protocol (e.g., SP-EMERG-001)
2. Notify Constitution Steward within 1 hour
3. Submit follow-up constitutional commit within 24 hours
4. Document in post-incident review

Casual use of `--no-verify` violates Article 4 and will be flagged in audits.

## Troubleshooting

### "Hook not running"
```bash
# Reinstall hooks
pre-commit uninstall
pre-commit install
pre-commit install --hook-type commit-msg
```

### "Permission denied"
```bash
chmod +x .github/hooks/constitutional_commit_validator.py
```

### "I don't understand REVERSIBILITY"

REVERSIBILITY must specify how the system responds to harm:
- **degrade**: System reduces to safe baseline (e.g., "degrade to manual mode")
- **pause**: System stops operation (e.g., "pause data processing, alert operators")
- **escalate**: System hands control to humans (e.g., "escalate to human supervisor")

Example:
```
REVERSIBILITY: System will degrade to baseline algorithm if accuracy drops below 95%. Operators can pause processing via emergency stop button. Critical paths escalate to human review automatically.
```

### "What about merge commits?"

GitHub merge commits are excepted (see `.constitution-ignore`). The PR itself contains constitutional documentation.

## Learn More

- **Full Documentation**: [README.md](README.md)
- **Sample Messages**: [SAMPLE_COMMIT_MESSAGES.md](SAMPLE_COMMIT_MESSAGES.md)
- **Constitution**: [Model_Digital_Constitution.md](../../Model_Digital_Constitution.md)
- **Pre-commit Framework**: https://pre-commit.com/

## Philosophy (30 seconds)

These hooks enforce one principle:

> **"Legitimacy accumulates through committed responsibility, not outputs alone."**  
> — Model Digital Constitution, Article 4

Every commit is a human commitment. These hooks ensure:
- ✅ Explicit intention (what you're doing)
- ✅ Clear rationale (why it matters)
- ✅ Documented human impact (who's affected)
- ✅ Planned reversibility (harm mitigation)
- ✅ Accountable authorship (who's responsible)

This makes violations **visible, traceable, and blockable** at the point of creation.

## Next Steps

1. ✅ Make your first constitutional commit
2. 📖 Review sample messages for your use case
3. 🎯 Bookmark this guide for reference
4. 🤝 Share with your team

Welcome to constitutional software development! 🚀
