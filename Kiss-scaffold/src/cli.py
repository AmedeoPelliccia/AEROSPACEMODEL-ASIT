"""Command-line interface parsing for Kiss-scaffold."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="Kiss-scaffold",
        description=(
            "Aircraft GenKISS (General Knowledge and Information Standard Systems) "
            "Scaffold Generator for aerospace projects"
        ),
    )

    parser.add_argument(
        "--base",
        type=str,
        default="./OUT",
        help="Base directory for scaffold output (default: ./OUT)",
    )
    parser.add_argument(
        "--config-dir",
        type=str,
        default="./config",
        help="Directory containing lifecycle.yaml and atdp.yaml (default: ./config)",
    )
    parser.add_argument(
        "--mode",
        choices=["fail", "safe", "overwrite"],
        default="overwrite",
        help="Write mode: fail on collision, safe (skip existing), or overwrite (default)",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Run validation after generation",
    )
    parser.add_argument(
        "--manifest",
        action="store_true",
        help="Write SCAFFOLD_MANIFEST.txt manifest file",
    )
    parser.add_argument(
        "--timestamp",
        type=str,
        default=None,
        help="UTC timestamp, e.g. 2026-02-16T10:00:00Z (default: now UTC)",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level (default: INFO)",
    )

    args = parser.parse_args()

    # Normalize paths early for downstream modules.
    args.base = str(Path(args.base).expanduser())
    args.config_dir = str(Path(args.config_dir).expanduser())

    return args


def parse_timestamp(timestamp_str: Optional[str]) -> datetime:
    """
    Parse a timestamp string into a timezone-aware UTC datetime.

    Accepted inputs:
    - None -> current UTC time
    - ISO8601 with 'Z' or explicit offset, e.g. '2026-02-16T10:00:00Z'
    - Naive datetime/date forms:
        * YYYY-MM-DDTHH:MM:SS
        * YYYY-MM-DD HH:MM:SS
        * YYYY-MM-DD
      (interpreted as UTC)

    Args:
        timestamp_str: ISO-like timestamp string or None.

    Returns:
        Timezone-aware datetime in UTC.

    Raises:
        ValueError: If the timestamp cannot be parsed.
    """
    if timestamp_str is None:
        return datetime.now(timezone.utc)

    raw = timestamp_str.strip()
    if not raw:
        raise ValueError("Empty timestamp string is not valid.")

    # Handle ISO 'Z' suffix explicitly.
    iso_candidate = raw.replace("Z", "+00:00")

    # 1) Try direct ISO parse first.
    try:
        dt = datetime.fromisoformat(iso_candidate)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        pass

    # 2) Fallback formats.
    fmts = [
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ]
    for fmt in fmts:
        try:
            dt = datetime.strptime(raw, fmt).replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue

    raise ValueError(
        f"Invalid timestamp format: {timestamp_str}. "
        "Use ISO8601, e.g. 2026-02-16T10:00:00Z"
    )
