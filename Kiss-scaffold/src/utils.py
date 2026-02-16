"""Utility functions for Kiss-scaffold."""
from __future__ import annotations

from pathlib import Path
from typing import List


def write_manifest(base: Path) -> Path:
    """Write manifest file listing all generated files.
    
    Args:
        base: Base directory containing generated files
        
    Returns:
        Path to the manifest file
        
    Raises:
        IOError: If manifest cannot be written
    """
    manifest_path = base / "SCAFFOLD_MANIFEST.txt"
    
    # Collect all files recursively
    files: List[Path] = []
    if base.exists():
        for item in base.rglob("*"):
            if item.is_file() and item != manifest_path:
                files.append(item)
    
    # Sort for consistent output
    files.sort()
    
    # Write manifest
    with manifest_path.open("w", encoding="utf-8") as f:
        f.write("# Kiss-scaffold Manifest\n")
        f.write(f"# Base: {base}\n")
        f.write(f"# Files: {len(files)}\n\n")
        
        for file_path in files:
            rel_path = file_path.relative_to(base)
            f.write(f"{rel_path}\n")
    
    return manifest_path
