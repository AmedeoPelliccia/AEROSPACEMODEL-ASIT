from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple


class ValidationError(Exception):
    pass


def validate_locked_rules_and_lifecycle(base: Path, phases: Dict[str, Any], atdp_cfg: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errs: List[str] = []
    phase_keys = {k for k in phases.keys() if k.startswith("LC")}

    genesis = base / "00-00-general" / "GENESIS"
    ssot = base / "00-00-general" / "SSOT"
    pub = base / "00-00-general" / "PUB"

    for root in [genesis, ssot, pub]:
        if not root.exists():
            errs.append(f"Missing required root: {root}")

    if errs:
        return (False, errs)

    # Rule 1: no _executions in GENESIS
    if genesis.exists():
        for p in genesis.rglob("*"):
            if "_executions" in p.parts:
                errs.append(f"Locked Rule 1 violation: {p}")

    # Rule 2: no _executions in PUB
    if pub.exists():
        for p in pub.rglob("*"):
            if "_executions" in p.parts:
                errs.append(f"Locked Rule 2 violation: {p}")

    # Canonical LC set exact match
    expected_lc = phase_keys
    existing_lc = {d.name for d in ssot.iterdir() if d.is_dir() and d.name.startswith("LC")} if ssot.exists() else set()
    missing = expected_lc - existing_lc
    extra = existing_lc - expected_lc
    if missing:
        errs.append(f"Missing LC dirs in SSOT: {sorted(missing)}")
    if extra:
        errs.append(f"Extra LC dirs in SSOT: {sorted(extra)}")

    return (len(errs) == 0, errs)
