#!/usr/bin/env python3
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

from src.cli import parse_args, parse_timestamp
from src.config_loader import load_configs, ConfigError
from src.generator import (
    GenContext,
    gen_root,
    gen_genesis,
    gen_ssot,
    gen_csdb_pub,
    gen_0090,
    GenerationError,
)
from src.validator import validate_locked_rules_and_lifecycle
from src.utils import write_manifest


def main() -> int:
    args = parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    log = logging.getLogger("kiss-scaffold")

    try:
        dt = parse_timestamp(args.timestamp)
    except Exception as e:
        log.error("Invalid timestamp: %s", e)
        return 2

    base = Path(os.getenv("KISS_BASE", args.base)).resolve()
    config_dir = Path(os.getenv("KISS_CONFIG_DIR", args.config_dir)).resolve()

    try:
        lifecycle_cfg, atdp_cfg = load_configs(config_dir)
    except ConfigError as e:
        log.error("Config error: %s", e)
        return 3

    ctx = GenContext(
        base=base,
        mode=args.mode,
        now_iso=dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        date_short=dt.strftime("%Y-%m-%d"),
        written=[],
    )

    try:
        gen_root(ctx)
        gen_genesis(ctx)
        gen_ssot(ctx, lifecycle_cfg["phases"])
        gen_csdb_pub(ctx, atdp_cfg)
        gen_0090(ctx, lifecycle_cfg["phases"], atdp_cfg)
    except GenerationError as e:
        log.error("Generation conflict: %s", e)
        return 4
    except Exception as e:
        log.exception("Generation failed: %s", e)
        return 5

    if args.validate:
        ok, errs = validate_locked_rules_and_lifecycle(
            base,
            lifecycle_cfg["phases"],
            atdp_cfg,
        )
        if not ok:
            log.error("Validation failed")
            for err in errs:
                log.error(" - %s", err)
            return 6
        log.info("Validation passed")

    if args.manifest:
        try:
            mf = write_manifest(base)
            log.info("Manifest written: %s", mf)
        except Exception as e:
            log.exception("Manifest failed: %s", e)
            return 7

    log.info("Scaffold generated at %s", base)
    log.info("Files written: %d", len(ctx.written))
    return 0


if __name__ == "__main__":
    sys.exit(main())
