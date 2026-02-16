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
    # Note: Full ATDP README is generated later in _gen_atdp_readme()
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

    # Generate enhanced COMMON_CSDB structure with detailed subdirectories
    for d in common_csdb_dirs:
        _gen_common_csdb_dir(ctx, d)

    # Generate enhanced product structures with full CSDB hierarchy
    for product in products:
        _gen_product_structure(ctx, product)

    # Generate enhanced ATDP README
    _gen_atdp_readme(ctx)

    _write(ctx, "00-00-general/PUB/ATDP/EXPORT/.gitkeep", "")
    _write(ctx, "00-00-general/PUB/ATDP/IETP/.gitkeep", "")


def _gen_common_csdb_dir(ctx: GenContext, dir_name: str) -> None:
    """Generate enhanced COMMON_CSDB subdirectory with templates and schemas."""
    base_path = f"00-00-general/PUB/ATDP/COMMON_CSDB/{dir_name}"
    
    if dir_name == "DM":
        _write(ctx, f"{base_path}/.gitkeep", "")
        _write(ctx, f"{base_path}/README.md", f"""\
            # COMMON_CSDB / DM — Shared Data Module Layer

            This directory contains reusable, product-agnostic Data Module (DM) assets
            for ATDP products (AMM, IPC, SRM, TSM, WDM, FIM, MMEL, MPD).

            ## Purpose
            - Provide common DM templates and fragments
            - Enforce uniform metadata and traceability
            - Reduce duplication across product-specific publication trees

            ## Rules
            1. Every DM asset must be registered in `dm_index.csv`.
            2. Every DM metadata file must include SSOT/CSDB_REF provenance.
            3. No product-exclusive payload in COMMON DM.
            4. Naming must be deterministic and stable.

            ## Minimal naming convention
            - Content: `DM-<DOMAIN>-<CODE>.md`
            - Metadata: `DM-<DOMAIN>-<CODE>.meta.yaml`

            Example:
            - `DM-TEMPLATE-COMMON-0001.md`
            - `DM-TEMPLATE-COMMON-0001.meta.yaml`

            ---

            **GenKISS**: General Knowledge and Information Standard Systems
            """)
        _write(ctx, f"{base_path}/dm_index.csv", f"""\
            DM_ID,Title,Type,Language,Applicability,Source_Type,Source_Ref,Status,Owner_AoR,Last_Updated_UTC,Notes
            DM-TEMPLATE-COMMON-0001,Common DM Skeleton,TEMPLATE,EN,ALL,SSOT,KNU-00-00-005-LC02-GenKISS-SYS_REQ,ACTIVE,STK_DATA,{ctx.now_iso},Seed shared template
            """)
        _write(ctx, f"{base_path}/schema/dm_header.schema.yaml", """\
            $schema: "http://json-schema.org/draft-07/schema#"
            title: "Common DM Header Metadata"
            type: object
            required:
              - dm_id
              - title
              - type
              - language
              - applicability
            properties:
              dm_id:
                type: string
                pattern: "^DM-[A-Z0-9\\-]+$"
              title:
                type: string
              type:
                type: string
                enum: ["TEMPLATE", "FRAGMENT", "MODULE", "REFERENCE"]
              language:
                type: string
                pattern: "^[A-Z]{2}$"
              applicability:
                type: string
              version:
                type: string
              owner_aor:
                type: ["string", "null"]
              tags:
                type: array
                items: { type: string }
            """)
        _write(ctx, f"{base_path}/schema/dm_trace.schema.yaml", """\
            $schema: "http://json-schema.org/draft-07/schema#"
            title: "DM Traceability Schema"
            type: object
            required:
              - dm_id
              - source_type
              - source_ref
            properties:
              dm_id:
                type: string
              source_type:
                type: string
                enum: ["SSOT", "CSDB_REF", "COMMON_CSDB"]
              source_ref:
                type: string
              derived_utc:
                type: string
                format: date-time
            """)
        _write(ctx, f"{base_path}/templates/DM-TEMPLATE-COMMON-0001.md", """\
            # DM-TEMPLATE-COMMON-0001: Common DM Skeleton

            This is a seed template for common data modules.

            ## Content Structure
            - Introduction
            - Procedure/Description
            - References
            - Warnings/Cautions/Notes

            ---

            **GenKISS**: General Knowledge and Information Standard Systems
            """)
        _write(ctx, f"{base_path}/templates/DM-TEMPLATE-COMMON-0001.meta.yaml", """\
            dm_id: DM-TEMPLATE-COMMON-0001
            title: Common DM Skeleton
            type: TEMPLATE
            language: EN
            applicability: ALL
            version: 1.0.0
            owner_aor: STK_DATA
            tags: [template, common, seed]
            source_type: SSOT
            source_ref: KNU-00-00-005-LC02-GenKISS-SYS_REQ
            """)
    
    elif dir_name == "PM":
        _write(ctx, f"{base_path}/.gitkeep", "")
        _write(ctx, f"{base_path}/README.md", f"""\
            # COMMON_CSDB / PM — Shared Publication Module Layer

            This directory contains reusable, product-agnostic Publication Module (PM)
            assets for ATDP products (AMM, IPC, SRM, TSM, WDM, FIM, MMEL, MPD).

            ## Purpose
            - Provide common PM assembly templates
            - Standardize module composition order
            - Preserve traceability to SSOT/CSDB_REF sources

            ## Rules
            1. Every PM asset must be registered in `pm_index.csv`.
            2. Every PM metadata file must include provenance and derived UTC.
            3. COMMON PM must not include product-exclusive payload.
            4. PMs can reference COMMON_CSDB/DM modules only through declared refs.

            ## Minimal naming convention
            - Content: `PM-<DOMAIN>-<CODE>.md`
            - Metadata: `PM-<DOMAIN>-<CODE>.meta.yaml`

            Example:
            - `PM-TEMPLATE-COMMON-0001.md`
            - `PM-TEMPLATE-COMMON-0001.meta.yaml`

            ---

            **GenKISS**: General Knowledge and Information Standard Systems
            """)
        _write(ctx, f"{base_path}/pm_index.csv", f"""\
            PM_ID,Title,Type,Language,Applicability,Source_Type,Source_Ref,Status,Owner_AoR,Last_Updated_UTC,Notes
            PM-TEMPLATE-COMMON-0001,Common PM Skeleton,TEMPLATE,EN,ALL,SSOT,KNU-00-00-005-LC02-GenKISS-SYS_REQ,ACTIVE,STK_DATA,{ctx.now_iso},Seed shared publication module template
            """)
        _write(ctx, f"{base_path}/schema/pm_header.schema.yaml", """\
            $schema: "http://json-schema.org/draft-07/schema#"
            title: "Common PM Header Metadata"
            type: object
            required:
              - pm_id
              - title
              - type
              - language
              - applicability
            properties:
              pm_id:
                type: string
                pattern: "^PM-[A-Z0-9\\-]+$"
              title:
                type: string
              type:
                type: string
                enum: ["TEMPLATE", "ASSEMBLY", "REFERENCE"]
              language:
                type: string
                pattern: "^[A-Z]{2}$"
              applicability:
                type: string
              version:
                type: string
              owner_aor:
                type: ["string", "null"]
              tags:
                type: array
                items: { type: string }
            """)
        _write(ctx, f"{base_path}/schema/pm_trace.schema.yaml", """\
            $schema: "http://json-schema.org/draft-07/schema#"
            title: "PM Traceability Schema"
            type: object
            required:
              - pm_id
              - source_type
              - source_ref
            properties:
              pm_id:
                type: string
              source_type:
                type: string
                enum: ["SSOT", "CSDB_REF", "COMMON_CSDB"]
              source_ref:
                type: string
              derived_utc:
                type: string
                format: date-time
            """)
        _write(ctx, f"{base_path}/templates/PM-TEMPLATE-COMMON-0001.md", """\
            # PM-TEMPLATE-COMMON-0001: Common PM Skeleton

            This is a seed template for common publication modules.

            ## Composition Structure
            - Title Page
            - Table of Contents
            - Referenced DM Modules
            - Appendices

            ---

            **GenKISS**: General Knowledge and Information Standard Systems
            """)
        _write(ctx, f"{base_path}/templates/PM-TEMPLATE-COMMON-0001.meta.yaml", """\
            pm_id: PM-TEMPLATE-COMMON-0001
            title: Common PM Skeleton
            type: TEMPLATE
            language: EN
            applicability: ALL
            version: 1.0.0
            owner_aor: STK_DATA
            tags: [template, common, seed]
            source_type: SSOT
            source_ref: KNU-00-00-005-LC02-GenKISS-SYS_REQ
            """)
    else:
        _write(ctx, f"{base_path}/.gitkeep", "")


def _gen_product_structure(ctx: GenContext, product: str) -> None:
    """Generate comprehensive product-specific CSDB structure."""
    base_path = f"00-00-general/PUB/ATDP/PRODUCTS/{product}"
    
    _write(ctx, f"{base_path}/.gitkeep", "")
    _write(ctx, f"{base_path}/README.md", f"""\
        # ATDP / PRODUCTS / {product} — {_get_product_full_name(product)} Domain

        {product} product domain under `PUB/ATDP/PRODUCTS`.

        ## Scope
        This folder hosts {product}-specific publication assets and configuration.
        Shared reusable primitives must be consumed from:

        - `../../COMMON_CSDB/DM`
        - `../../COMMON_CSDB/PM`
        - `../../COMMON_CSDB/BREX`
        - `../../COMMON_CSDB/APPLICABILITY`
        - `../../COMMON_CSDB/COMMON`
        - `../../COMMON_CSDB/ICN`

        ## Governance
        - {product} content is publication-layer output and must trace to SSOT/CSDB_REF lineage.
        - No authority inversion: SSOT remains authoritative lifecycle source.
        - Product deltas must be explicit and versioned.

        ## Minimal Deliverables
        - {product} DM/PM seeds
        - DML seed
        - Applicability seed
        - Traceability lineage map
        - Export target configuration

        ---

        **GenKISS**: General Knowledge and Information Standard Systems
        """)
    
    # Generate index
    _write(ctx, f"{base_path}/{product.lower()}_index.csv", f"""\
        Asset_ID,Asset_Type,Path,Status,Source_Type,Source_Ref,Last_Updated_UTC,Owner_AoR,Notes
        {product}-DM-INTRO-0001,DM,CSDB/DM/{product}-DM-INTRO-0001.md,DRAFT,COMMON_CSDB,DM-TEMPLATE-COMMON-0001,{ctx.now_iso},STK_DATA,Seed {product} intro module
        {product}-PM-MAIN-0001,PM,CSDB/PM/{product}-PM-MAIN-0001.md,DRAFT,COMMON_CSDB,PM-TEMPLATE-COMMON-0001,{ctx.now_iso},STK_DATA,Seed {product} main publication module
        """)
    
    # CONFIG subdirectories
    _write(ctx, f"{base_path}/CONFIG/effectivity.yaml", f"""\
        # {product} Effectivity Configuration
        applicability_rules:
          - rule_id: {product}-EFF-001
            description: Default applicability for {product}
            condition: ALL
        """)
    _write(ctx, f"{base_path}/CONFIG/publication_profile.yaml", f"""\
        # {product} Publication Profile
        product_code: {product}
        language: EN
        output_formats: [PDF, HTML, IETP]
        brex_reference: {product}-BREX-0001
        """)
    _write(ctx, f"{base_path}/CONFIG/export_targets.yaml", f"""\
        # {product} Export Targets
        targets:
          - target_id: {product}-EXPORT-PDF
            format: PDF
            output_path: ../EXPORT/PDF
          - target_id: {product}-EXPORT-HTML
            format: HTML
            output_path: ../EXPORT/HTML
          - target_id: {product}-EXPORT-IETP
            format: IETP_PACKAGE
            output_path: ../EXPORT/IETP_PACKAGE
        """)
    
    # CSDB subdirectories
    _write(ctx, f"{base_path}/CSDB/DM/.gitkeep", "")
    _write(ctx, f"{base_path}/CSDB/DM/README.md", f"# {product} Data Modules\n\nProduct-specific DM content for {product}.\n")
    _write(ctx, f"{base_path}/CSDB/DM/{product}-DM-INTRO-0001.md", f"""\
        # {product}-DM-INTRO-0001: {product} Introduction

        This is the introductory data module for {product}.

        ## Purpose
        Provides overview and scope of {product} documentation.

        ---

        **GenKISS**: General Knowledge and Information Standard Systems
        """)
    
    _write(ctx, f"{base_path}/CSDB/PM/.gitkeep", "")
    _write(ctx, f"{base_path}/CSDB/PM/README.md", f"# {product} Publication Modules\n\nProduct-specific PM content for {product}.\n")
    _write(ctx, f"{base_path}/CSDB/PM/{product}-PM-MAIN-0001.md", f"""\
        # {product}-PM-MAIN-0001: {product} Main Publication

        Main publication module for {product}.

        ## Referenced Modules
        - {product}-DM-INTRO-0001

        ---

        **GenKISS**: General Knowledge and Information Standard Systems
        """)
    
    _write(ctx, f"{base_path}/CSDB/DML/.gitkeep", "")
    _write(ctx, f"{base_path}/CSDB/DML/{product}-DML-0001.csv", f"""\
        DML_Entry_ID,DM_ID,PM_ID,Sequence,Status
        {product}-DML-E001,{product}-DM-INTRO-0001,{product}-PM-MAIN-0001,1,ACTIVE
        """)
    
    _write(ctx, f"{base_path}/CSDB/BREX/.gitkeep", "")
    _write(ctx, f"{base_path}/CSDB/BREX/{product}-BREX-0001.md", f"""\
        # {product}-BREX-0001: {product} Business Rules

        Business rules and validation constraints for {product}.

        ---

        **GenKISS**: General Knowledge and Information Standard Systems
        """)
    
    _write(ctx, f"{base_path}/CSDB/ICN/.gitkeep", "")
    _write(ctx, f"{base_path}/CSDB/COMMON/.gitkeep", "")
    
    _write(ctx, f"{base_path}/CSDB/APPLICABILITY/.gitkeep", "")
    _write(ctx, f"{base_path}/CSDB/APPLICABILITY/{product}-ACT-0001.yaml", f"""\
        # {product} Applicability Table
        act_id: {product}-ACT-0001
        rules:
          - rule_id: {product}-APP-001
            description: Default applicability
            condition: ALL
        """)
    
    # TRACE subdirectories
    _write(ctx, f"{base_path}/TRACE/lineage.yaml", f"""\
        # {product} Lineage Tracking
        product: {product}
        ssot_sources:
          - LC02_SYSTEM_REQUIREMENTS
          - LC04_DESIGN_DEFINITION
        csdb_ref_sources:
          - NU/*
        """)
    _write(ctx, f"{base_path}/TRACE/compliance_map.csv", f"""\
        Requirement_ID,Source_LC,Target_DM,Compliance_Status,Verification_Method
        REQ-{product}-001,LC02,{product}-DM-INTRO-0001,PENDING,REVIEW
        """)
    
    # EXPORT subdirectories
    _write(ctx, f"{base_path}/EXPORT/.gitkeep", "")
    _write(ctx, f"{base_path}/EXPORT/PDF/.gitkeep", "")
    _write(ctx, f"{base_path}/EXPORT/HTML/.gitkeep", "")
    _write(ctx, f"{base_path}/EXPORT/IETP_PACKAGE/.gitkeep", "")


def _get_product_full_name(product: str) -> str:
    """Get full name for product code."""
    names = {
        "AMM": "Aircraft Maintenance Manual",
        "IPC": "Illustrated Parts Catalog",
        "SRM": "Structural Repair Manual",
        "CMM": "Component Maintenance Manual",
    }
    return names.get(product, product)


def _gen_atdp_readme(ctx: GenContext) -> None:
    """Generate enhanced PUB/ATDP README."""
    _write(ctx, "00-00-general/PUB/ATDP/README.md", """\
        # PUB / ATDP — Aircraft Technical Data Product Umbrella

        ATDP is the canonical publication umbrella for aircraft technical data products in the GenKISS scaffold.  
        Within ATDP, **CSDB is shared infrastructure** (COMMON_CSDB), and each product domain (AMM, IPC, SRM, CMM, etc.) provides product-specific deltas under `PRODUCTS/`.

        ---

        ## 1) Mission

        Provide a governed publication surface that:

        - Reuses shared CSDB primitives across products
        - Preserves product-specific specialization without duplicating common assets
        - Maintains strict lineage to SSOT and CSDB_REF
        - Supports deterministic export and IETP packaging flows

        ---

        ## 2) Canonical Structure

        ```text
        PUB/ATDP/
        ├── README.md
        ├── COMMON_CSDB/
        │   ├── README.md
        │   ├── DM/
        │   ├── PM/
        │   ├── DML/
        │   ├── BREX/
        │   ├── ICN/
        │   ├── COMMON/
        │   └── APPLICABILITY/
        ├── PRODUCTS/
        │   ├── AMM/
        │   ├── IPC/
        │   ├── SRM/
        │   ├── CMM/
        │   └── ...
        ├── EXPORT/
        │   ├── .gitkeep
        │   ├── PDF/
        │   ├── HTML/
        │   └── IETP_PACKAGE/
        └── IETP/
            └── .gitkeep
        ```

        ---

        ## 3) Governance Boundaries

        ### 3.1 Authority Model
        - SSOT remains the authoritative lifecycle source.
        - CSDB_REF provides atomic reference units derived from SSOT.
        - PUB/ATDP is delivery-oriented and must never become an upstream authority.

        ### 3.2 Non-Inversion Rule

        No product folder in `PUB/ATDP/PRODUCTS/*` may redefine lifecycle truth or bypass SSOT provenance.

        ### 3.3 Delta Rule

        Product directories contain only:
        - product-specific content,
        - product-specific applicability/configuration,
        - product-specific trace mappings.

        Shared templates and primitives belong in COMMON_CSDB.

        ---

        ## 4) Product Domains

        A product domain (e.g., PRODUCTS/AMM) should include:
        - `CONFIG/` (effectivity, publication profile, export targets)
        - `CSDB/` (DM, PM, DML, BREX, APPLICABILITY, etc.)
        - `TRACE/` (lineage + compliance mapping)
        - `EXPORT/` (product-local export outputs if enabled)

        Each product must carry explicit lineage to:
        - `../../SSOT`
        - `../../CSDB_REF/NU`
        - `../../COMMON_CSDB`

        ---

        ## 5) Reuse Philosophy

        COMMON_CSDB hosts:
        - Generic warnings, cautions, notes
        - Standard procedures and checklists
        - Reusable illustrations and graphics
        - Business rules (BREX) for validation
        - Applicability logic templates

        Products consume and specialize, but do not duplicate.

        ---

        **GenKISS**: General Knowledge and Information Standard Systems
        """)


def _gen_ietp_structure(ctx: GenContext) -> None:
    """Generate comprehensive IETP structure."""
    _write(ctx, "00-00-general/PUB/ATDP/IETP/README.md", f"""\
        # ATDP / IETP — Interactive Electronic Technical Publication

        IETP assembly and runtime packaging surface for ATDP products.

        ## Purpose
        This directory defines the deterministic packaging contract for interactive delivery
        of ATDP product content (AMM, IPC, SRM, CMM, etc.) while preserving lineage to
        SSOT and CSDB_REF.

        ## Inputs
        - `../COMMON_CSDB/*` shared publication primitives
        - `../PRODUCTS/*/CSDB/*` product-specific publication assets
        - `../PRODUCTS/*/TRACE/*` product traceability evidence

        ## Outputs
        - Package-ready IETP bundles in `packages/`
        - Navigation and applicability configuration
        - Search index configuration
        - Compliance mapping and lineage records
        """)
    
    _write(ctx, "00-00-general/PUB/ATDP/IETP/ietp_manifest.yaml", f"""\
        ietp:
          id: "ATDP-IETP-0001"
          version: "0.1.0"
          status: "DRAFT"
          generated_utc: "{ctx.now_iso}"
          owner_aor: "STK_DATA"

          source_roots:
            common_csdb: "../COMMON_CSDB"
            products: "../PRODUCTS"
            ssot_root: "../../../SSOT"
            csdb_ref_root: "../../../CSDB_REF/NU"

          products_in_scope:
            - "AMM"
            - "IPC"
            - "SRM"
            - "CMM"

          packaging:
            target_dir: "./packages"
            format: "IETP_PACKAGE"
            deterministic_build: true
            include_trace_bundle: true
        """)
    
    _write(ctx, "00-00-general/PUB/ATDP/IETP/profiles/desktop_profile.yaml", """\
        profile_id: "IETP-DESKTOP-0001"
        channel: "desktop"
        ui:
          navigation_mode: "tree"
          split_view: true
          preload_toc: true
        search:
          enable_fulltext: true
          fuzzy: true
        applicability:
          mode: "strict"
        status: "DRAFT"
        """)
    
    _write(ctx, "00-00-general/PUB/ATDP/IETP/profiles/mobile_profile.yaml", """\
        profile_id: "IETP-MOBILE-0001"
        channel: "mobile"
        ui:
          navigation_mode: "flat"
          split_view: false
          preload_toc: false
        search:
          enable_fulltext: true
          fuzzy: false
        applicability:
          mode: "filtered"
        status: "DRAFT"
        """)
    
    _write(ctx, "00-00-general/PUB/ATDP/IETP/navigation/toc_seed.yaml", """\
        toc:
          root_title: "ATDP IETP"
          products:
            - id: "AMM"
              title: "Aircraft Maintenance Manual"
              order: 1
            - id: "IPC"
              title: "Illustrated Parts Catalog"
              order: 2
            - id: "SRM"
              title: "Structural Repair Manual"
              order: 3
            - id: "CMM"
              title: "Component Maintenance Manual"
              order: 4
        """)
    
    _write(ctx, "00-00-general/PUB/ATDP/IETP/applicability/filter_rules.yaml", """\
        applicability:
          default_filter: "ALL"
          rules:
            - id: "RULE-001"
              description: "Base aircraft"
              filter: "MODEL:BASE"
            - id: "RULE-002"
              description: "Extended range variant"
              filter: "MODEL:ER"
        """)
    
    _write(ctx, "00-00-general/PUB/ATDP/IETP/search/index_config.yaml", """\
        search:
          indexing:
            fulltext: true
            metadata: true
            illustrations: false
          ranking:
            title_boost: 2.0
            keyword_boost: 1.5
          filters:
            - "product"
            - "ata_chapter"
            - "effectivity"
        """)
    
    _write(ctx, "00-00-general/PUB/ATDP/IETP/compliance/s1000d_mapping.csv", """\
        S1000D_Element,IETP_Element,Mapping_Type,Notes
        dataModule,dm_content,DIRECT,1:1 mapping
        publicationModule,pm_assembly,DIRECT,1:1 mapping
        dmodule,navigation_node,TRANSFORM,Flattened for IETP
        """)
    
    _write(ctx, "00-00-general/PUB/ATDP/IETP/trace/lineage.yaml", f"""\
        lineage:
          generated_utc: "{ctx.now_iso}"
          source_roots:
            - "../COMMON_CSDB"
            - "../PRODUCTS"
          validation:
            required: true
            strict_mode: true
        """)
    
    for subdir in ["packages", "navigation", "applicability", "search", "compliance", "trace"]:
        _write(ctx, f"00-00-general/PUB/ATDP/IETP/{subdir}/.gitkeep", "")


def _gen_export_structure(ctx: GenContext, products: List[str]) -> None:
    """Generate comprehensive EXPORT structure."""
    _write(ctx, "00-00-general/PUB/ATDP/EXPORT/README.md", f"""\
        # ATDP / EXPORT — Publication Export Surface

        Deterministic export surface for ATDP products (AMM, IPC, SRM, CMM).

        ## Purpose
        Provide controlled rendering and packaging outputs from governed ATDP inputs:
        - PDF
        - HTML
        - IETP_PACKAGE

        ## Governance
        - Export artifacts are delivery outputs, not authority sources.
        - Lineage must point to `PUB/ATDP` sources and upstream SSOT/CSDB_REF.
        - Rebuilds with identical inputs must produce reproducible outputs.

        ## Operational Areas
        - `jobs/` queue and retry control
        - `logs/` export execution history
        - `trace/` lineage and compliance mapping
        """)
    
    _write(ctx, "00-00-general/PUB/ATDP/EXPORT/export_manifest.yaml", f"""\
        export:
          id: "ATDP-EXPORT-0001"
          version: "0.1.0"
          status: "DRAFT"
          generated_utc: "{ctx.now_iso}"
          owner_aor: "STK_DATA"

          products: {products}

          formats:
            - "PDF"
            - "HTML"
            - "IETP_PACKAGE"

          output_roots:
            pdf: "./PDF"
            html: "./HTML"
            ietp_package: "./IETP_PACKAGE"

          reproducibility:
            deterministic_build: true
            manifest_required: true
        """)
    
    # PDF README
    _write(ctx, "00-00-general/PUB/ATDP/EXPORT/PDF/README.md", """\
        # EXPORT / PDF

        Rendered PDF outputs for ATDP products.

        ## Conventions
        - One PDF per product major release
        - Filename: `{PRODUCT}_{VERSION}_{DATE}.pdf`
        - Watermarking: DRAFT/RELEASED per publication state
        """)
    
    # HTML README  
    _write(ctx, "00-00-general/PUB/ATDP/EXPORT/HTML/README.md", """\
        # EXPORT / HTML

        Rendered HTML outputs for ATDP products.

        ## Structure
        - Static HTML generation with navigation
        - Responsive layout for desktop/mobile
        - Cross-references preserved as hyperlinks
        """)
    
    # IETP_PACKAGE README
    _write(ctx, "00-00-general/PUB/ATDP/EXPORT/IETP_PACKAGE/README.md", """\
        # EXPORT / IETP_PACKAGE

        Interactive Electronic Technical Publication packages.

        ## Contents
        - Self-contained IETP runtime bundles
        - Embedded navigation and search indices
        - Applicability filtering metadata
        """)
    
    # Create product subdirectories for each export format
    for fmt in ["PDF", "HTML", "IETP_PACKAGE"]:
        for product in products:
            _write(ctx, f"00-00-general/PUB/ATDP/EXPORT/{fmt}/{product}/.gitkeep", "")
    
    _write(ctx, "00-00-general/PUB/ATDP/EXPORT/jobs/export_jobs.csv", """\
        Job_ID,Product,Format,Status,Created_UTC,Completed_UTC,Output_Path,Notes
        JOB-001,AMM,PDF,PENDING,,,,"Seed job"
        """)
    
    _write(ctx, "00-00-general/PUB/ATDP/EXPORT/jobs/retry_queue.csv", """\
        Job_ID,Retry_Count,Last_Attempt_UTC,Next_Retry_UTC,Error_Message
        """)
    
    _write(ctx, "00-00-general/PUB/ATDP/EXPORT/logs/export_log.csv", """\
        Timestamp_UTC,Job_ID,Product,Format,Status,Duration_Sec,Notes
        """)
    
    _write(ctx, "00-00-general/PUB/ATDP/EXPORT/trace/lineage.yaml", f"""\
        lineage:
          generated_utc: "{ctx.now_iso}"
          source_roots:
            - "../COMMON_CSDB"
            - "../PRODUCTS"
          validation:
            required: true
            strict_mode: true
        """)
    
    _write(ctx, "00-00-general/PUB/ATDP/EXPORT/trace/compliance_map.csv", """\
        Export_Artifact,Source_DM_ID,Source_PM_ID,SSOT_Path,Compliance_Status,Notes
        """)
    
    for subdir in ["jobs", "logs", "trace"]:
        _write(ctx, f"00-00-general/PUB/ATDP/EXPORT/{subdir}/.gitkeep", "")


def _gen_ssot_lc_readmes(ctx: GenContext, phases: Dict[str, Any]) -> None:
    """Generate comprehensive READMEs for select SSOT LC phases."""
    # LC02 comprehensive README
    lc02_spec = phases.get("LC02_SYSTEM_REQUIREMENTS", {})
    _write(ctx, "00-00-general/SSOT/LC02_SYSTEM_REQUIREMENTS/README.md", f"""\
        # SSOT / LC02_SYSTEM_REQUIREMENTS — Functional Baseline (FBL)

        LC02 is the authoritative phase for **system requirements** and **interface control intent** in the GenKISS canonical lifecycle.  
        This phase is the **exclusive producer** of the **Functional Baseline (FBL)**.

        ---

        ## 1) Phase Identity

        | Field | Value |
        |---|---|
        | LC ID | LC02 |
        | Canonical Name | {lc02_spec.get('canonical_name', 'System Requirements')} |
        | Phase Type | {lc02_spec.get('phase_type', 'PLM')} |
        | Baseline Produced | **FBL** (Functional Baseline) |
        | Authority | Systems Engineering (with Configuration Control) |

        ---

        ## 2) Mission

        Define, structure, and govern system-level requirements so downstream phases can execute deterministically:

        - LC03 Safety & Reliability traces to LC02 requirements
        - LC04 Design Definition realizes LC02 requirements
        - LC06 Verification confirms requirement satisfaction
        - LC08 Certification uses LC02-linked evidence chain

        LC02 is where requirement ambiguity is converted into configuration-controlled intent.

        ---

        ## 3) Scope

        ### In Scope
        - System requirements authoring and control
        - External/internal interface requirements (ICD intent)
        - Requirement attributes (verification method, rationale, criticality, effectivity)
        - Trace seed creation for safety, design, and test
        - FBL release package assembly

        ### Out of Scope
        - Detailed design solutions (LC04)
        - Execution test evidence (LC06)
        - Certification issuance actions (LC08)
        - Production release authority (LC10)

        ---

        ## 4) Canonical Outputs

        - Requirement specifications (`REQ`)
        - Interface control definitions (`ICD`)
        - Compliance intent mapping (pre-cert trace intent)
        - FBL package under configuration control
        - Downstream trace links:
          - `LC02 REQ → LC03 SAFETY`
          - `LC02 REQ → LC04 DESIGN`
          - `LC04 DESIGN → LC06 TEST` (continued chain)
          - `LC06 TEST → LC08 COMPLIANCE`

        ---

        ## 5) Entry and Exit Criteria

        ### Entry
        - Program/problem framing approved (LC01 complete/accepted inputs)
        - Stakeholder requirement capture completed
        - Governance and AoR assignment active

        ### Exit
        - All system requirements captured and baselined
        - FBL package released and configuration controlled
        - Downstream trace links established
        - CCB approval obtained

        ---

        ## 6) Governance Rules

        - Requirements must be uniquely identified (REQ-XXXX)
        - All requirements must include verification method
        - Changes require ECR/ECO and CCB approval
        - FBL snapshots are immutable once released

        ---

        **GenKISS**: General Knowledge and Information Standard Systems
        """)


def gen_0090(ctx: GenContext, phases: Dict[str, Any], atdp_cfg: Dict[str, Any]) -> None:
    """Generate ATA 00-90 tables/index artifacts with comprehensive documentation."""
    _write(ctx, "00-90-tables-schemas-index/README.md", f"""\
        # ATA 00-90 — Tables, Schemas, and Canonical Index

        This directory is the governance control plane for the GenKISS scaffold.  
        It centralizes machine-readable contracts used to validate structure, lifecycle conformance, and publication integrity across:

        - `00-00-general/GENESIS` (Knowledge Determination Space)
        - `00-00-general/SSOT` (Authoritative Information Source)
        - `00-00-general/CSDB_REF` (Reference Dataset)
        - `00-00-general/PUB/ATDP` (Publication umbrella)

        ---

        ## 1) Purpose

        `00-90-tables-schemas-index` provides:

        1. **Canonical lifecycle registry materialization**  
           LC01–LC14 definitions exported as tabular index for deterministic checks.

        2. **Schema contracts**  
           Structural validation rules for YAML/CSV/metadata artifacts.

        3. **Controlled vocabularies and enumerations**  
           AoR, statuses, phase types, product codes, and trace semantics.

        4. **Cross-domain consistency layer**  
           Single validation reference for generator, validator, CI pipeline, and audits.

        ---

        ## 2) Canonical Contents

        ```text
        00-90-tables-schemas-index/
        ├── README.md
        ├── tables/
        │   ├── canonical_lifecycle_registry.csv
        │   ├── atdp_products.csv
        │   ├── aor_codes.csv
        │   ├── status_enumerations.csv
        │   └── epistemic_domains.csv
        ├── schemas/
        │   ├── discovery.schema.yaml
        │   ├── justification.schema.yaml
        │   ├── framing.schema.yaml
        │   ├── derivation.schema.yaml
        │   ├── downstream.schema.yaml
        │   └── tokenomics.schema.yaml
        └── index/
            ├── artifact_catalog.csv
            └── validation_profile.yaml
        ```

        If `index/` files are not yet generated, they are optional bootstrap targets and can be created by CI/bootstrap jobs.

        ---

        ## 3) Lifecycle Contract (LC01–LC14)

        `tables/canonical_lifecycle_registry.csv` is the deterministic phase reference used by validators.

        ### Required invariants
        - Exactly 14 lifecycle IDs (LC01..LC14)
        - Canonical naming only (no synthetic aliases)
        - Valid phase type per row: PLM or OPS
        - Canonical SSOT directory mapping present for each LC

        ### Validation implications
        - Generator must produce exactly these LC directories in SSOT
        - Validator rejects extra or missing LC directories
        - Trace tools use this registry to validate cross-phase references

        ---

        ## 4) Product Contract

        `tables/atdp_products.csv` defines product codes and COMMON_CSDB usage.

        ### Columns
        - `Product_Code`: AMM, IPC, SRM, CMM, etc.
        - `Uses_Common_CSDB`: TRUE if product consumes shared primitives

        ### Validation implications
        - Product directories under `PUB/ATDP/PRODUCTS` must match this list
        - Products with `Uses_Common_CSDB=TRUE` must reference `../../COMMON_CSDB`

        ---

        ## 5) Schema Directory (Optional Extension)

        Future extensions may include JSON Schema files for:
        - GENESIS O-KNOT/Y-KNOT/KNOT structures
        - CSDB_REF NU provenance records
        - SSOT KNU artifact metadata
        - PUB/ATDP traceability formats

        Schema files enable automated validation in CI pipelines.

        ---

        ## 6) Usage in Validation

        Validators should:
        1. Load `canonical_lifecycle_registry.csv`
        2. Assert SSOT has exactly those LC directories
        3. Assert no extra/missing directories
        4. Load `atdp_products.csv`
        5. Assert `PUB/ATDP/PRODUCTS` matches product list
        6. Validate product structure against schema (if present)

        ---

        **GenKISS**: General Knowledge and Information Standard Systems
        """)

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
    
    # Generate IETP, EXPORT, and SSOT phase documentation
    _gen_ietp_structure(ctx)
    _gen_export_structure(ctx, products)
    _gen_ssot_lc_readmes(ctx, phases)
