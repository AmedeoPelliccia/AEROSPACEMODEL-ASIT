#!/usr/bin/env python3
"""
kiss-scaffold.py - Wrapper script for KISS Scaffold Generator
Run from OPT-IN_FRAMEWORK/O-ORGANIZATIONS/ATA_00-GENERAL directory

This script provides access to the Kiss-scaffold generator from the repository root.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Add repository root to path to import Kiss-scaffold modules
repo_root = Path(__file__).resolve().parents[3]
kiss_scaffold_path = repo_root / "Kiss-scaffold"
sys.path.insert(0, str(kiss_scaffold_path))

# Use subprocess to call the Kiss-scaffold.py script directly
# (no module import since Kiss-scaffold is a script-based tool)
import subprocess
script_path = kiss_scaffold_path / "Kiss-scaffold.py"
if not script_path.exists():
        print(f"Error: Kiss-scaffold.py not found at {script_path}", file=sys.stderr)
        print(f"Repository root: {repo_root}", file=sys.stderr)
        sys.exit(1)
    
    # Execute the Kiss-scaffold.py script with all arguments
    result = subprocess.run([sys.executable, str(script_path)] + sys.argv[1:])
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()