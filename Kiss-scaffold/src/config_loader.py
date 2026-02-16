from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Tuple
import yaml

CANONICAL_ORDER = [
    "LC01_PROBLEM_STATEMENT",
    "LC02_SYSTEM_REQUIREMENTS",
    "LC03_SAFETY_RELIABILITY",
    "LC04_DESIGN_DEFINITION",
    "LC05_ANALYSIS_MODELS",
    "LC06_VERIFICATION",
    "LC07_QA_PROCESS",
    "LC08_CONFIGURATION",
    "LC09_ESG_SUSTAINABILITY",
    "LC10_INDUSTRIAL_SUPPLY",
    "LC11_OPERATIONS_CUSTOMIZATION",
    "LC12_MAINTENANCE_REPAIR",
    "LC13_MAINTENANCE_SOURCE",
    "LC14_END_OF_LIFE",
]

class ConfigError(Exception):
    pass


def _read_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise ConfigError(f"Config file not found: {path}")
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        raise ConfigError(f"Invalid YAML object at root: {path}")
    return data


def load_configs(config_dir: Path) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    lifecycle = _read_yaml(config_dir / "lifecycle.yaml")
    atdp = _read_yaml(config_dir / "atdp.yaml")

    phases = lifecycle.get("phases")
    if not isinstance(phases, dict):
        raise ConfigError("lifecycle.yaml 'phases' must be an object.")

    got = set(phases.keys())
    exp = set(CANONICAL_ORDER)
    if got != exp:
        missing = sorted(exp - got)
        extra = sorted(got - exp)
        raise ConfigError(f"Lifecycle keys mismatch. Missing={missing} Extra={extra}")

    required_phase_keys = {"phase_type", "canonical_name", "ssot_dir"}
    for lc_id, spec in phases.items():
        if not isinstance(spec, dict):
            raise ConfigError(f"{lc_id} spec must be an object.")
        missing = required_phase_keys - set(spec.keys())
        if missing:
            raise ConfigError(f"{lc_id} missing keys: {sorted(missing)}")
        if spec["phase_type"] not in {"PLM", "OPS"}:
            raise ConfigError(f"{lc_id} phase_type must be PLM or OPS.")

    products = atdp.get("products")
    common_dirs = atdp.get("common_csdb_dirs")
    if not isinstance(products, list) or not all(isinstance(x, str) for x in products):
        raise ConfigError("atdp.yaml 'products' must be a list[str].")
    if not isinstance(common_dirs, list) or not all(isinstance(x, str) for x in common_dirs):
        raise ConfigError("atdp.yaml 'common_csdb_dirs' must be a list[str].")

    lifecycle["_ordered_lc_ids"] = CANONICAL_ORDER[:]
    return lifecycle, atdp
