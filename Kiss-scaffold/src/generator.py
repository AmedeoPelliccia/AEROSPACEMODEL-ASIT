from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List
import textwrap


@dataclass
class GenContext:
    base: Path
    mode: str
    now_iso: str
    date_short: str
    written: List[Path]


class GenerationError(Exception):
    pass


def _norm(content: str) -> str:
    return textwrap.dedent(content).lstrip("\n")

def _atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)

def _write(ctx: GenContext, rel_path: str, content: str) -> None:
    p = ctx.base / rel_path
    if p.exists():
        if ctx.mode == "fail":
            raise GenerationError(f"Collision in mode=fail: {p}")
        if ctx.mode == "safe":
            return

    _atomic_write_text(p, _norm(content))
    ctx.written.append(p)


def gen_root(ctx: GenContext) -> None:
    _write(ctx, "00-00-general/README.md", f"""\
    # ATA 00-00 — KISS
    This is the root for a KISS (Keep It Super Simple) scaffolded aerospace project.
    """)


def gen_genesis(ctx: GenContext) -> None:
    _write(ctx, "00-00-general/GENESIS/README.md", f"""\
    # GENESIS
    Source of truth templates and frozen project definitions.
    """)


def gen_ssot(ctx: GenContext, phases: Dict[str, Any]) -> None:
    base_path = "00-00-general/SSOT"
    _write(
        ctx,
        f"{base_path}/README.md",
        f"""\
        # SSOT
        Single Source of Truth for lifecycle artifacts.
        """,
    )
    _write(
        ctx,
        f"{base_path}/EXECUTION_MANIFEST.md",
        f"# Execution\nExecution: {ctx.now_iso}\nStatus: DRAFT\n",
    )

    ordered_ids = phases.get("_ordered_lc_ids")
    if not isinstance(ordered_ids, list):
        ordered_ids = sorted([k for k in phases.keys() if k.startswith("LC")])

    for lc_id in ordered_ids:
        if lc_id not in phases:
            continue
        spec = phases[lc_id]
        _write(
            ctx,
            f"{base_path}/{lc_id}/README.md",
            f"""\
            # {lc_id}
            **Canonical Name**: {spec['canonical_name']}
            **Phase Type**: {spec['phase_type']}
            """,
        )


def gen_csdb_pub(ctx: GenContext, atdp: Dict[str, Any]) -> None:
    for prod in atdp.get("products", []):
        for cdir in atdp.get("common_csdb_dirs", []):
            _write(ctx, f"00-00-general/IDB/PUB/{prod}/CSDB/{cdir}/.gitkeep", "")


def gen_0090(ctx: GenContext, phases: Dict[str, Any], atdp: Dict[str, Any]) -> None:
    _write(ctx, "00-90-monitoring/README.md", "# ATA 00-90 Monitoring\n")
