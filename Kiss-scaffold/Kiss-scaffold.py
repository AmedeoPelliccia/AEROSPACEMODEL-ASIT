#!/usr/bin/env python3
"""
Kiss-scaffold.py - KISS (Keep It Super Simple) Scaffold Generator
Generates standard aerospace project structure with lifecycle phases.
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
import argparse

from src.config_loader import load_configs, ConfigError
from src.generator import GenContext, gen_root, gen_genesis, gen_ssot, gen_csdb_pub, gen_0090
from src.validator import validate_locked_rules_and_lifecycle, ValidationError


def main():
    parser = argparse.ArgumentParser(description="KISS Scaffold Generator")
    parser.add_argument("--base", type=Path, required=True, help="Base directory for scaffold")
    parser.add_argument("--config-dir", type=Path, required=True, help="Configuration directory")
    parser.add_argument("--mode", choices=["fail", "safe", "overwrite"], default="fail", 
                        help="Write mode: fail on collision, safe (skip), or overwrite")
    parser.add_argument("--validate", action="store_true", help="Validate after generation")
    parser.add_argument("--manifest", action="store_true", help="Print manifest of written files")
    
    args = parser.parse_args()
    
    try:
        # Load configurations
        print(f"Loading configs from {args.config_dir}...")
        lifecycle, atdp = load_configs(args.config_dir)
        phases = lifecycle.get("phases", {})
        
        # Setup generation context
        now = datetime.utcnow()
        ctx = GenContext(
            base=args.base,
            mode=args.mode,
            now_iso=now.isoformat() + "Z",
            date_short=now.strftime("%Y-%m-%d"),
            written=[]
        )
        
        # Generate structure
        print(f"Generating scaffold at {args.base}...")
        gen_root(ctx)
        gen_genesis(ctx)
        gen_ssot(ctx, phases)
        gen_csdb_pub(ctx, atdp)
        gen_0090(ctx, phases, atdp)
        
        print(f"✓ Generated {len(ctx.written)} files")
        
        # Validate if requested
        if args.validate:
            print("Validating structure...")
            ok, errs = validate_locked_rules_and_lifecycle(args.base, phases, atdp)
            if not ok:
                print("✗ Validation failed:")
                for err in errs:
                    print(f"  - {err}")
                sys.exit(1)
            print("✓ Validation passed")
        
        # Print manifest if requested
        if args.manifest:
            print("\nManifest:")
            for p in sorted(ctx.written):
                print(f"  {p.relative_to(args.base)}")
        
        print("\n✓ Success!")
        
    except (ConfigError, ValidationError) as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
