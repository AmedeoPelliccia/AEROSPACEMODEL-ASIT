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
        # ATA 00-00 — GenKISS

        - `GENESIS/` — Knowledge Determination Space
        - `SSOT/` — Authoritative Information Source
        - `PUB/ATDP/` — Aircraft Technical Data Product umbrella

        **GenKISS**: General Knowledge and Information Standard Systems
        
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

        > Epistemic workspace for uncertainty discovery, justification, and framing before SSOT commitment.

        ---

        ## Purpose

        `GENESIS` is the **knowledge domain** of Aircraft GenKISS.  
        It captures what is not yet authoritative:

        - unknowns
        - assumptions
        - decision alternatives
        - framing boundaries
        - acceptance intent prior to lifecycle execution

        GENESIS artifacts are **pre-authoritative** and exist to make epistemic state explicit before information enters SSOT.

        ---

        ## Epistemic Position

        | Attribute | GENESIS |
        |---|---|
        | Nature | Uncertain, exploratory, contextual |
        | Authority | Pre-authoritative |
        | Mutability | High (iterative knowledge work) |
        | Primary Function | Determine what must be resolved and why |
        | Output | Graduatable KNOT framing for SSOT entry |

        ---

        ## Locked Governance Rule

        **Locked Rule 1**  
        `GENESIS` must not contain executed lifecycle artifacts.

        ### Forbidden in GENESIS
        - `_executions/` directories
        - certification evidence packages
        - production release artifacts
        - authoritative compliance records

        ### Allowed in GENESIS
        - O-KNOT, Y-KNOT, KNOT records
        - rationale, options analysis, boundary framing
        - registries describing knowledge progression
        - schema-conformant pre-authoritative metadata

        ---

        ## Canonical Knowledge Pipeline

        ```text
        O-KNOT  ->  Y-KNOT  ->  KNOT  ->  (graduation)  ->  SSOT/LC01+
        Discovery   Justify     Frame                        Authoritative lifecycle
        ```

        ### O-KNOT (Discovery)

        **Question**: What is unknown?  
        **Outputs**: uncertainty statement, context, initial trace anchors.

        ### Y-KNOT (Justification)

        **Question**: Why does it matter, and which option is preferable?  
        **Outputs**: options analysis, decision rationale, tradeoff basis.

        ### KNOT (Framing)

        **Question**: What exactly will be resolved and how acceptance is defined?  
        **Outputs**: bounded scope, acceptance criteria, planned downstream KNUs.

        ---

        ## Directory Layout

        ```text
        GENESIS/
        ├── README.md
        ├── _registry/
        │   ├── o-knot_registry.csv
        │   ├── y-knot_registry.csv
        │   └── knot_registry.csv
        ├── O-KNOT/
        │   └── O-KNOT-<ID>/
        ├── Y-KNOT/
        │   └── Y-KNOT-<ID>/
        └── KNOT/
            └── KNOT-<ID>/
        ```

        ---

        **GenKISS**: General Knowledge and Information Standard Systems
        """,
    )

    _write(
        ctx,
        "00-00-general/GENESIS/_registry/o-knot_registry.csv",
        """\
        O_KNOT_ID,Title,ATA_Chapter,ATA_Section,Status,Discovery_Date,Owner_AoR,Heritage_Ref,Notes
        O-KNOT-00-00-001,GenKISS Ontology Foundation,00,00,OPEN,,STK_DATA,,Seed
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
        KNOT-00-00-005,GenKISS Baseline Definition,OPEN
        """,
    )

    safe_ts = ctx.now_iso.replace(":", "-")
    _write(
        ctx,
        f"00-00-general/SSOT/LC02_SYSTEM_REQUIREMENTS/"
        f"KNU-00-00-005-LC02-GenKISS-SYS_REQ/_executions/{safe_ts}/artifact.md",
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

    _write(ctx, "00-00-general/CSDB_REF/README.md", """\
        # CSDB_REF — Reference Dataset

        > Atomic, traceable reference layer for GenKISS (not a replacement for SSOT authority).

        ---

        ## Purpose

        `CSDB_REF` stores **NU (Atomic Reference Units)** derived from validated SSOT executions, so downstream consumers can reuse distilled technical knowledge without traversing full lifecycle trees.

        This directory belongs to the ATA 00 KISS scaffold:

        - **GENESIS** → Knowledge Determination Space (uncertain, exploratory)
        - **SSOT** → Authoritative Information Source (validated, lifecycle-bound)
        - **CSDB_REF** → Derived atomic references for controlled reuse
        - **PUB/ATDP** → Delivery surface for Aircraft Technical Data Products

        ---

        ## Governance Position

        `CSDB_REF` is a **derived layer**:

        - It **must trace back** to SSOT execution artifacts.
        - It **must not host** primary certification authority.
        - It **must not contain** raw GENESIS exploratory artifacts.
        - It is **ATDP-agnostic** and can feed AMM, IPC, SRM, TSM, WDM, FIM, MMEL, MPD.

        ---

        ## Structure

        ```text
        CSDB_REF/
        └── NU/
            ├── index.csv
            ├── schema/
            │   └── nu_source.schema.yaml
            └── NU-<ID>/
                ├── content.*        # atomic distilled reference
                ├── _source.yaml     # mandatory provenance to SSOT execution
                └── metadata.yaml    # optional classification/effectivity
        ```

        ---

        ## Mandatory Rules

        1. Every `NU-<ID>/` shall include `_source.yaml`.
        2. `_source.yaml` shall reference a valid SSOT path under:
           - `.../SSOT/.../_executions/<timestamp>/`
        3. No orphan NU directories (must appear in `index.csv`).
        4. NU content is derivative and must never replace SSOT authority.

        ---

        **GenKISS**: General Knowledge and Information Standard Systems
        """)
    _write(ctx, "00-00-general/CSDB_REF/NU/.gitkeep", "")
    _write(
        ctx,
        "00-00-general/CSDB_REF/NU/README.md",
        """\
        # CSDB_REF / NU — Atomic Reference Units

        This directory stores **atomic consumable reference units (NU)** derived from SSOT executions.

        ## Role in GenKISS

        - **GENESIS**: knowledge determination (uncertain)
        - **SSOT**: authoritative lifecycle information (validated)
        - **CSDB_REF/NU**: distilled reference units for downstream consumption

        NU content is derivative and must never replace SSOT authority.

        ## Rules

        1. Every `NU-<ID>/` must contain `_source.yaml`.
        2. `_source.yaml` must point to an SSOT execution artifact path.
        3. No orphan NU directories (must appear in `index.csv`).
        4. NU is ATDP-agnostic: can feed AMM, IPC, SRM, TSM, WDM, FIM, MMEL, MPD.

        ## Minimal Unit Structure

        ```text
        NU-<ID>/
        ├── content.*            # atomic reference content
        ├── _source.yaml         # provenance from SSOT execution
        └── metadata.yaml        # optional classification/tags/effectivity
        ```

        ## Example index.csv

        ```csv
        NU_ID,Title,Source_KNU_ID,Source_SSOT_Path,Status,Created_UTC,Owner_AoR,Notes
        NU-28-10-001,Tank Geometry Reference,KNU-28-10-001,SSOT/LC05/.../artifact.yaml,ACTIVE,2026-01-15T10:00:00Z,ENG_STRUCT,
        ```

        ## Example _source.yaml Schema

        ```yaml
        nu_id: NU-28-10-001
        source_knu_id: KNU-28-10-001
        source_ssot_execution_path: SSOT/LC05_ANALYSIS_MODELS/KNU-28-10-001/_executions/2026-01-15T10-00-00Z/artifact.yaml
        derived_utc: 2026-01-15T10:30:00Z
        transformation_contract: CNT-SSOT-TO-NU-001
        ```

        ---

        **GenKISS**: General Knowledge and Information Standard Systems
        """,
    )
    _write(
        ctx,
        "00-00-general/CSDB_REF/NU/index.csv",
        """\
        NU_ID,Title,Source_KNU_ID,Source_SSOT_Path,Status,Created_UTC,Owner_AoR,Notes
        """,
    )
    _write(
        ctx,
        "00-00-general/CSDB_REF/NU/schema/nu_source.schema.yaml",
        """\
        $schema: "http://json-schema.org/draft-07/schema#"
        title: "NU Source Record"
        description: "Traceability record for CSDB_REF atomic units"
        type: object
        required:
          - nu_id
          - source_knu_id
          - source_ssot_execution_path
          - derived_utc
        properties:
          nu_id:
            type: string
            pattern: "^NU-[A-Z0-9\\-]+$"
          source_knu_id:
            type: string
          source_ssot_execution_path:
            type: string
            description: "Path to SSOT _executions/<timestamp>/ artifact"
          derived_utc:
            type: string
            format: date-time
          transformation_contract:
            type: string
            description: "Contract ID governing SSOT->NU transformation"
        """,
    )

    _write(
        ctx,
        "00-00-general/PUB/README.md",
        """\
        # PUB — Publication Surface
        ATDP is umbrella; CSDB is not AMM-only.
        """,
    )
    _write(ctx, "00-00-general/PUB/ATDP/README.md", "# ATDP — Aircraft Technical Data Product\n")
    _write(
        ctx,
        "00-00-general/PUB/ATDP/COMMON_CSDB/README.md",
        """\
        # COMMON_CSDB — Shared CSDB Components for ATDP

        > Reusable, product-agnostic CSDB building blocks for Aircraft Technical Data Products (ATDP).

        ---

        ## Purpose

        `PUB/ATDP/COMMON_CSDB` contains **shared publication primitives** used across ATDP products (AMM, IPC, SRM, TSM, WDM, FIM, MMEL, MPD, etc.).

        This layer avoids duplication and enforces consistency in:

        - data module structures
        - publication module composition
        - business rules (BREX)
        - applicability logic
        - common warnings/cautions/notes
        - graphics and reusable assets

        ---

        ## Position in GenKISS

        ```text
        GENESIS (knowledge determination)
            -> SSOT (authoritative lifecycle information)
                -> CSDB_REF (atomic references)
                    -> PUB/ATDP/COMMON_CSDB (shared publication components)
                        -> PUB/ATDP/PRODUCTS/<AMM|IPC|SRM|...> (final publications)
        ```

        ---

        ## Structure

        ```text
        COMMON_CSDB/
        ├── DM/              # Data Modules (reusable content units)
        ├── PM/              # Publication Modules (composition logic)
        ├── ICN/             # Illustrations (graphics, diagrams)
        ├── BREX/            # Business Rules Exchange (validation rules)
        └── APL/             # Applicability (effectivity, configuration)
        ```

        ---

        ## Governance Rules

        1. **Shared primitives only**: No product-specific content.
        2. **Traceability required**: All DM/PM must trace to CSDB_REF or SSOT.
        3. **Version control**: Changes to COMMON_CSDB require CCB approval.
        4. **Reuse mandatory**: Products must use COMMON_CSDB when available.

        ---

        ## Example Use Cases

        - **Common Warning DM**: "High Voltage Warning" used in AMM, IPC, WDM
        - **Standard Procedure PM**: "Lockout/Tagout Procedure" composition
        - **Generic Illustration**: "Tool Kit Assembly" graphic
        - **Applicability Rule**: "A320 Series with Winglet" effectivity

        ---

        **GenKISS**: General Knowledge and Information Standard Systems
        """,
    )

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
