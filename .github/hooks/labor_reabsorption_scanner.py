#!/usr/bin/env python3
"""
Labor Reabsorption Pattern Scanner

Enforces Articles 1 & 8 (Human Labor Foundation + No Exclusion by Efficiency)
by scanning for labor-displacing patterns that require reabsorption documentation.

This script scans files for patterns indicating labor displacement and warns
when such patterns are detected without proper reabsorption documentation.
"""

import sys
import re
from pathlib import Path


# Patterns indicating potential labor displacement
LABOR_DISPLACEMENT_PATTERNS = [
    r"remove.*role",
    r"eliminate.*position",
    r"workforce\s+reduction",
    r"job\s+elimination",
    r"autonomous.*override",
    r"staff\s+reduction",
    r"headcount\s+reduction",
    r"layoff",
    r"termination",
]


def scan_file(filepath: str) -> list[str]:
    """
    Scan a file for labor-displacement patterns.
    
    Args:
        filepath: Path to file to scan
        
    Returns:
        List of matched patterns found in the file
    """
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().lower()
            
        matches = []
        for pattern in LABOR_DISPLACEMENT_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                matches.append(pattern)
        
        return matches
    except Exception as e:
        # Silently skip files that can't be read
        return []


def main():
    """Main entry point for labor pattern scanner."""
    if len(sys.argv) < 2:
        # No files to scan
        sys.exit(0)
    
    files_with_patterns = []
    
    for filepath in sys.argv[1:]:
        matches = scan_file(filepath)
        if matches:
            files_with_patterns.append((filepath, matches))
    
    if files_with_patterns:
        print("⚠️  LABOR PATTERN DETECTED in:")
        for filepath, patterns in files_with_patterns:
            print(f"   {filepath}")
        print()
        print("Article 1 & 8 require labor reabsorption documentation.")
        print("Add LABOR_REABSORPTION_PLAN.md or justify in commit HUMAN_IMPACT.")
        print("See Model_Digital_Constitution.md Articles 1, 8, 11.")
        # Don't block the commit, just warn
        sys.exit(0)
    
    # No patterns detected
    sys.exit(0)


if __name__ == "__main__":
    main()
