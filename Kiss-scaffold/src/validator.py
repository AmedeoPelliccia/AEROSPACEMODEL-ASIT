from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple


class ValidationError(Exception):
    """Reserved for future strict validation exceptions."""


def validate_locked_rules_and_lifecycle(
    base: Path,
    phases: Dict[str, Any],
    atdp_cfg: Dict[str, Any],
) -> Tuple[bool, List[str]]:
    """
    Validate generated scaffold against KISS locked rules + canonical structure.

    Rules enforced:
      1) GENESIS must not contain any `_executions` directory.
      2) Any SSOT artifact file named `artifact.*` must be under `_executions`.
      3) SSOT LC directories must exactly match configured canonical LC keys.
      4) PUB/ATDP must include required structure from atdp_cfg.

    Returns:
      (ok, errors)
    """
    errs: List[str] = []

    # Normalize expected LC keys (ignore non-LC helper keys such as _ordered_lc_ids)
    expected_lc = {k for k in phases.keys() if isinstance(k, str) and k.startswith("LC")}

    genesis = base / "00-00-general" / "GENESIS"
    ssot = base / "00-00-general" / "SSOT"
    pub = base / "00-00-general" / "PUB" / "ATDP"

    # Required roots must exist
    for root in (genesis, ssot, pub):
        if not root.exists():
            errs.append(f"Missing required root: {root}")

    # If roots are missing, stop early to avoid cascaded noise
    if errs:
        return (False, errs)

    # Locked Rule 1: no _executions anywhere under GENESIS
    for p in genesis.rglob("*"):
        if p.is_dir() and p.name == "_executions":
            errs.append(f"Locked Rule 1 violation: {p}")

    # Locked Rule 2: artifact.* files under SSOT must live inside _executions
    for p in ssot.rglob("*"):
        if p.is_file() and p.name.startswith("artifact.") and "_executions" not in p.parts:
            errs.append(f"Locked Rule 2 violation: artifact outside _executions: {p}")

    # Canonical LC set exact match
    existing_lc = {d.name for d in ssot.iterdir() if d.is_dir() and d.name.startswith("LC")}
    missing = expected_lc - existing_lc
    extra = existing_lc - expected_lc

    if missing:
        errs.append(f"Missing canonical LC dirs: {sorted(missing)}")
    if extra:
        errs.append(f"Non-canonical LC dirs present: {sorted(extra)}")

    # ATDP required structure
    products = atdp_cfg.get("products")
    common_csdb_dirs = atdp_cfg.get("common_csdb_dirs")

    if not isinstance(products, list) or not all(isinstance(x, str) and x.strip() for x in products):
        errs.append("Invalid atdp_cfg['products']: must be list[str] with non-empty values.")
        products = []

    if not isinstance(common_csdb_dirs, list) or not all(
        isinstance(x, str) and x.strip() for x in common_csdb_dirs
    ):
        errs.append("Invalid atdp_cfg['common_csdb_dirs']: must be list[str] with non-empty values.")
        common_csdb_dirs = []

    required_paths = [
        pub / "COMMON_CSDB",
        pub / "PRODUCTS",
        pub / "EXPORT",
        pub / "IETP",
    ]
    required_paths.extend(pub / "COMMON_CSDB" / d for d in common_csdb_dirs)
    required_paths.extend(pub / "PRODUCTS" / p for p in products)

    for r in required_paths:
        if not r.exists():
            errs.append(f"Missing ATDP path: {r}")

    return (len(errs) == 0, errs)
