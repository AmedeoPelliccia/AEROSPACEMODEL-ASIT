"""Command-line interface parsing for Kiss-scaffold."""
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="Kiss-scaffold",
        description="Aircraft GenKISS (General Knowledge and Information Standard Systems) Scaffold Generator for aerospace projects",
    )
    parser.add_argument(
        "--base",
        type=str,
        required=True,
        help="Base directory for scaffold output",
    )
    parser.add_argument(
        "--config-dir",
        type=str,
        required=True,
        help="Configuration directory containing lifecycle.yaml and atdp.yaml",
    )
    parser.add_argument(
        "--mode",
        choices=["fail", "safe", "overwrite"],
        default="fail",
        help="Write mode: fail on collision (default), safe (skip existing), or overwrite",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Run validation after generation",
    )
    parser.add_argument(
        "--manifest",
        action="store_true",
        help="Write manifest file with list of generated files",
    )
    parser.add_argument(
        "--timestamp",
        type=str,
        default=None,
        help="ISO timestamp for generation (default: current UTC time)",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level (default: INFO)",
    )
    return parser.parse_args()


def parse_timestamp(timestamp_str: str | None) -> datetime:
    """Parse timestamp string or return current UTC time.
    
    Args:
        timestamp_str: ISO format timestamp string or None
        
    Returns:
        datetime object
        
    Raises:
        ValueError: If timestamp string is invalid
    """
    if timestamp_str is None:
        return datetime.utcnow()
    
    # Try parsing ISO format
    try:
        return datetime.fromisoformat(timestamp_str.rstrip("Z"))
    except ValueError:
        # Try other common formats
        for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
            try:
                return datetime.strptime(timestamp_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"Invalid timestamp format: {timestamp_str}")
