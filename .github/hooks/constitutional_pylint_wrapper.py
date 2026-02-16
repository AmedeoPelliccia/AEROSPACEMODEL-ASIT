#!/usr/bin/env python3
"""
Constitutional Pylint Wrapper

Cross-platform wrapper for running Pylint with the constitutional plugin.
Provides graceful degradation when Pylint is not installed.
"""

import sys
import subprocess
import shutil
import os
from pathlib import Path


def main():
    """Main entry point for constitutional Pylint wrapper."""
    if len(sys.argv) < 2:
        # No files to check
        sys.exit(0)
    
    # Check if pylint is available
    if not shutil.which('pylint'):
        print("⚠️  Pylint not installed - skipping constitutional code checks.")
        print("   Install with: pip install pylint")
        sys.exit(0)
    
    # Get repository root to set PYTHONPATH
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent
    plugins_dir = script_dir.parent / 'plugins'
    
    # Set up environment
    env = os.environ.copy()
    current_pythonpath = env.get('PYTHONPATH', '')
    env['PYTHONPATH'] = f"{plugins_dir}:{current_pythonpath}" if current_pythonpath else str(plugins_dir)
    
    # Run pylint with constitutional plugin
    cmd = [
        'pylint',
        '--load-plugins=constitutional_pylint_plugin',
        '--disable=all',
        '--enable=constitution-violation-harm-precedence,constitution-violation-autonomous-override',
    ] + sys.argv[1:]
    
    try:
        # Run pylint and capture result, but don't fail the commit
        result = subprocess.run(cmd, env=env, capture_output=False)
        # Always exit 0 to not block commits (warnings only)
        sys.exit(0)
    except Exception as e:
        print(f"⚠️  Error running pylint: {e}")
        sys.exit(0)


if __name__ == "__main__":
    main()
