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
    mode: str  # overwrite | safe | fail
    now_iso: str
    date_short: str
    written: List[Path]


class GenerationError(Exception):
    """Raised for generation-time conflicts and invalid inputs."""


def _norm(content: str) -> str:
    """Normalize multiline literals: dedent and remove leading blank lines."""
    return textwrap.dedent(content).lstrip("\n")


def _atomic_write_text(path: Path, content: str) -> None:
    """
    Atomically write UTF-8 text with LF newlines.

    Ensures file content is either old or fully new, never partial.
    """
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
    """
    Write a file under ctx.base using collision policy:
      - fail: raise if exists
      - safe: skip if exists
      - overwrite: replace if exists
    """
    p = ctx.base / rel_path

    if p.exists():
        if ctx.mode == "fail":
            raise GenerationError(f"Collision in mode=fail: {p}")
        if ctx.mode == "safe":
            return
        if ctx.mode != "overwrite":
            raise GenerationError(f"Unknown mode: {ctx.mode}")

    _atomic_write_text(p, _norm(content))
    ctx.written.append(p)


def gen_root(ctx: GenContext) -> None:
    """Generate ATA 00 root docs."""
    _write(
        ctx,
        "00-00-general/README.md",
        f"""\
        # ATA 00-00 — KISS

        - `GENESIS/` — Knowledge Determination Space
        - `SSOT/` — Authoritative Information Source
        - `PUB/ATDP/` — Aircraft Technical Data Product umbrella

        Generated: {ctx.date_short}
        """,
    )

    _write(
        ctx,
        "00-00-general/00_INDEX.md",
        """\
        # ATA 00-00 — Index
        - GENESIS
        - SSOT
        - CSDB_REF
        - PUB/ATDP
        - ../00-90-tables-schemas-index
        """,
    )


def gen_genesis(ctx: GenContext) -> None:
    """Generate GENESIS knowledge space seed."""
    _write(
        ctx,
        "00-00-general/GENESIS/README.md",
        """\
        # GENESIS — Knowledge Determination Space
        O-KNOT -> Y-KNOT -> KNOT. No _executions allowed.
        """,
    )

    _write(
        ctx,
        "00-00-general/GENESIS/_registry/o-knot_registry.csv",
        """\
        O_KNOT_ID,Title,ATA_Chapter,ATA_Section,Status,Discovery_Date,Owner_AoR,Heritage_Ref,Notes
        O-KNOT-00-00-001,KISS Ontology Foundation,00,00,OPEN,,STK_DATA,,Seed
        """,
    )


def gen_ssot(ctx: GenContext, phases: Dict[str, Any]) -> None:
    """
    Generate SSOT structure and canonical LC README stubs.

    `phases` can include optional internal key `_ordered_lc_ids`.
    If absent, LC keys are inferred and sorted lexicographically.
    """
    _write(
        ctx,
        "00-00-general/SSOT/README.md",
        """\
        # SSOT — Authoritative Information Source
        Executions must be under `_executions/<UTC>/`.
        """,
    )

    _write(
        ctx,
        "00-00-general/SSOT/LC01_PROBLEM_STATEMENT/KNOTS.csv",
        """\
        KNOT_ID,Title,Status
        KNOT-00-00-005,KISS Baseline Definition,OPEN
        """,
    )

    safe_ts = ctx.now_iso.replace(":", "-")
    _write(
        ctx,
        f"00-00-general/SSOT/LC02_SYSTEM_REQUIREMENTS/"
        f"KNU-00-00-005-LC02-KISS-SYS_REQ/_executions/{safe_ts}/artifact.md",
        f"""\
        # Execution
        Execution: {ctx.now_iso}
        Status: DRAFT
        """,
    )

    ordered_ids = phases.get("_ordered_lc_ids")
    if not isinstance(ordered_ids, list):
        ordered_ids = sorted([k for k in phases.keys() if k.startswith("LC")])

    for lc_id in ordered_ids:
        if lc_id not in phases:
            continue
        spec = phases[lc_id]
        if not isinstance(spec, dict):
            raise GenerationError(f"{lc_id} spec must be object; got {type(spec).__name__}")

        canonical_name = spec.get("canonical_name", "")
        ssot_dir = spec.get("ssot_dir", "")
        phase_type = spec.get("phase_type", "")

        _write(
            ctx,
            f"00-00-general/SSOT/{lc_id}/README.md",
            f"""\
            # {lc_id}
            Canonical name: {canonical_name}
            Canonical registry path: {ssot_dir}
            Phase type: {phase_type}
            """,
        )


def gen_csdb_pub(ctx: GenContext, atdp_cfg: Dict[str, Any]) -> None:
    """Generate CSDB_REF and PUB/ATDP structure."""
    products = atdp_cfg.get("products")
    common_csdb_dirs = atdp_cfg.get("common_csdb_dirs")

    if not isinstance(products, list) or not all(isinstance(x, str) for x in products):
        raise GenerationError("atdp_cfg['products'] must be list[str]")
    if not isinstance(common_csdb_dirs, list) or not all(isinstance(x, str) for x in common_csdb_dirs):
        raise GenerationError("atdp_cfg['common_csdb_dirs'] must be list[str]")

    _write(ctx, "00-00-general/CSDB_REF/README.md", "# CSDB_REF — Reference Dataset\n")
    _write(ctx, "00-00-general/CSDB_REF/NU/.gitkeep", "")

    _write(
        ctx,
        "00-00-general/PUB/README.md",
        """\
        # PUB — Publication Surface
        ATDP is umbrella; CSDB is not AMM-only.
        """,
    )
    _write(ctx, "00-00-general/PUB/ATDP/README.md", "# ATDP — Aircraft Technical Data Product\n")
    _write(ctx, "00-00-general/PUB/ATDP/COMMON_CSDB/README.md", "# COMMON_CSDB\n")

    for d in common_csdb_dirs:
        _write(ctx, f"00-00-general/PUB/ATDP/COMMON_CSDB/{d}/.gitkeep", "")

    for product in products:
        _write(ctx, f"00-00-general/PUB/ATDP/PRODUCTS/{product}/README.md", f"# {product}\n")
        _write(ctx, f"00-00-general/PUB/ATDP/PRODUCTS/{product}/.gitkeep", "")

    _write(ctx, "00-00-general/PUB/ATDP/EXPORT/.gitkeep", "")
    _write(ctx, "00-00-general/PUB/ATDP/IETP/.gitkeep", "")


def gen_0090(ctx: GenContext, phases: Dict[str, Any], atdp_cfg: Dict[str, Any]) -> None:
    """Generate ATA 00-90 tables/index artifacts."""
    _write(ctx, "00-90-tables-schemas-index/README.md", "# ATA 00-90 — Tables, Schemas & Index\n")

    ordered_ids = phases.get("_ordered_lc_ids")
    if not isinstance(ordered_ids, list):
        ordered_ids = sorted([k for k in phases.keys() if k.startswith("LC")])

    lines = ["LC_ID,Phase_Type,Canonical_Name,Canonical_SSOT_Dir"]
    for lc_id in ordered_ids:
        if lc_id not in phases:
            continue
        s = phases[lc_id]
        lines.append(f"{lc_id},{s.get('phase_type','')},{s.get('canonical_name','')},{s.get('ssot_dir','')}")
    _write(
        ctx,
        "00-90-tables-schemas-index/tables/canonical_lifecycle_registry.csv",
        "\n".join(lines) + "\n",
    )

    products = atdp_cfg.get("products", [])
    p_lines = ["Product_Code,Uses_Common_CSDB"]
    for p in products:
        p_lines.append(f"{p},TRUE")
    _write(ctx, "00-90-tables-schemas-index/tables/atdp_products.csv", "\n".join(p_lines) + "\n")
