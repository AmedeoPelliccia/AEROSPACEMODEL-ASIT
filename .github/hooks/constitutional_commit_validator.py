#!/usr/bin/env python3
"""
Constitutional Commit Message Validator

Enforces Article 4 (Commit as Unit of Legitimacy) + Article 7 (Explicit Purpose)
from the Model Digital Constitution.

This validator ensures that every commit message contains:
- INTENT: What the commit aims to improve
- RATIONALE: Why this change is necessary
- HUMAN_IMPACT: Effect on people (workers, users, operators)
- REVERSIBILITY: How to degrade/pause/escalate if harm occurs
- AUTHOR: Accountable human agent

Usage:
    python3 constitutional_commit_validator.py <commit-msg-file>
"""

import sys
import re
from pathlib import Path


# Required sections per Article 4 and Article 7
REQUIRED_SECTIONS = {"INTENT", "RATIONALE", "HUMAN_IMPACT", "REVERSIBILITY", "AUTHOR"}


def parse_commit_message(msg: str) -> dict[str, str]:
    """
    Parse commit message into sections.
    
    Expected format:
        INTENT: <text>
        RATIONALE: <text>
        HUMAN_IMPACT: <text>
        REVERSIBILITY: <text>
        AUTHOR: <text>
    
    Returns:
        Dictionary mapping section names to their content
    """
    sections = {}
    
    # Match section headers followed by content (up to next header or end)
    # Use lookahead to capture everything until next section header or end of string
    pattern = r'^([A-Z_]+):\s*(.*?)(?=^[A-Z_]+:|\Z)'
    
    for match in re.finditer(pattern, msg, re.MULTILINE | re.DOTALL):
        section_name = match.group(1)
        section_content = match.group(2).strip()
        sections[section_name] = section_content
    
    return sections


def validate_required_sections(sections: dict[str, str]) -> tuple[bool, str]:
    """
    Validate that all required sections are present.
    
    Returns:
        (is_valid, error_message)
    """
    missing = REQUIRED_SECTIONS - sections.keys()
    
    if missing:
        error = (
            f"❌ CONSTITUTION VIOLATION (Article 4, Article 7)\n"
            f"Missing required sections: {', '.join(sorted(missing))}\n\n"
            f"Every commit must declare its legitimacy through explicit sections:\n"
            f"Template:\n"
            f"INTENT: What this commit aims to improve\n"
            f"RATIONALE: Why this change is necessary\n"
            f"HUMAN_IMPACT: Effect on people (workers, users, operators)\n"
            f"REVERSIBILITY: How to degrade/pause/escalate if harm occurs\n"
            f"AUTHOR: Accountable human agent\n\n"
            f"See Model_Digital_Constitution.md for details."
        )
        return False, error
    
    return True, ""


def validate_article_8(sections: dict[str, str]) -> tuple[bool, str]:
    """
    Validate Article 8: Prohibition of Human Exclusion by Efficiency.
    
    Detects workforce reduction patterns without reabsorption pathways.
    
    Returns:
        (is_valid, error_message)
    """
    human_impact = sections.get("HUMAN_IMPACT", "").lower()
    
    # Forbidden patterns indicating human exclusion
    exclusion_patterns = [
        "workforce reduction",
        "eliminate position",
        "remove role",
        "job elimination",
        "staff reduction",
        "headcount reduction",
        "layoff",
        "termination"
    ]
    
    for pattern in exclusion_patterns:
        if pattern in human_impact:
            # Check if reabsorption pathway is mentioned
            reabsorption_indicators = [
                "reabsorption",
                "retraining",
                "role transition",
                "upskilling",
                "redeployment",
                "new capacity"
            ]
            
            has_reabsorption = any(indicator in human_impact for indicator in reabsorption_indicators)
            
            if not has_reabsorption:
                error = (
                    f"❌ ARTICLE 8 VIOLATION: Prohibition of Human Exclusion by Efficiency\n"
                    f"Detected '{pattern}' in HUMAN_IMPACT without reabsorption pathway.\n\n"
                    f"Article 8 requires that efficiency gains not justify workforce reduction.\n"
                    f"You must specify:\n"
                    f"  - How affected workers will be reabsorbed\n"
                    f"  - What new roles or capacity will be created\n"
                    f"  - Timeline for retraining and transition\n\n"
                    f"If this is unavoidable, the repository steward must issue an\n"
                    f"explicit axiom-responsibility commit per Article 11.\n\n"
                    f"See Model_Digital_Constitution.md Articles 1, 8, and 11."
                )
                return False, error
    
    return True, ""


def validate_article_6(sections: dict[str, str]) -> tuple[bool, str]:
    """
    Validate Article 6: Human Harm Precedence.
    
    Ensures REVERSIBILITY specifies degrade/pause/escalate paths.
    
    Returns:
        (is_valid, error_message)
    """
    reversibility = sections.get("REVERSIBILITY", "").lower()
    
    # Required patterns for harm scenarios
    required_patterns = ["degrade", "pause", "escalate"]
    
    if not any(pattern in reversibility for pattern in required_patterns):
        error = (
            f"❌ ARTICLE 6 VIOLATION: Human Harm Precedence\n"
            f"REVERSIBILITY must specify at least one harm-mitigation path:\n"
            f"  - degrade: System reduces functionality to safe baseline\n"
            f"  - pause: System stops operation pending review\n"
            f"  - escalate: System hands control to human authority\n\n"
            f"Article 6 requires that human harm has absolute precedence over\n"
            f"efficiency, profitability, and performance. Systems must degrade,\n"
            f"pause, or escalate when harm is plausible.\n\n"
            f"See Model_Digital_Constitution.md Article 6."
        )
        return False, error
    
    return True, ""


def validate_sections_not_empty(sections: dict[str, str]) -> tuple[bool, str]:
    """
    Validate that required sections contain meaningful content.
    
    Returns:
        (is_valid, error_message)
    """
    empty_sections = []
    
    for section in REQUIRED_SECTIONS:
        content = sections.get(section, "").strip()
        if not content or len(content) < 10:  # At least 10 characters
            empty_sections.append(section)
    
    if empty_sections:
        error = (
            f"❌ CONSTITUTION VIOLATION\n"
            f"The following sections are empty or too short: {', '.join(sorted(empty_sections))}\n\n"
            f"Each section must contain meaningful content (at least 10 characters).\n"
            f"Legitimacy requires explicit, documented intention and accountability."
        )
        return False, error
    
    return True, ""


def main():
    """Main validation entry point."""
    if len(sys.argv) < 2:
        print("Usage: constitutional_commit_validator.py <commit-msg-file>", file=sys.stderr)
        sys.exit(1)
    
    msg_file = Path(sys.argv[1])
    
    if not msg_file.exists():
        print(f"Error: Commit message file not found: {msg_file}", file=sys.stderr)
        sys.exit(1)
    
    msg = msg_file.read_text(encoding='utf-8')
    
    # Parse sections
    sections = parse_commit_message(msg)
    
    # Run all validations
    validations = [
        validate_required_sections,
        validate_sections_not_empty,
        validate_article_8,
        validate_article_6,
    ]
    
    for validation_func in validations:
        is_valid, error_msg = validation_func(sections)
        if not is_valid:
            print(error_msg, file=sys.stderr)
            sys.exit(1)
    
    # All validations passed
    print("✅ Constitutional commit validated")
    print(f"   INTENT: {sections['INTENT'][:60]}...")
    print(f"   AUTHOR: {sections['AUTHOR']}")
    sys.exit(0)


if __name__ == "__main__":
    main()
