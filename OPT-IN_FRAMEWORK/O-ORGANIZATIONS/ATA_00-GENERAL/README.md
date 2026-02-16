# ATA 00-GENERAL - KISS Scaffold Generator

This directory contains the KISS (Keep It Super Simple) Scaffold Generator for creating standard aerospace project structures.

## Usage

Run the script from this directory:

```bash
python kiss-scaffold.py --base ./OUT --config-dir ./config --validate --manifest
```

### Options

- `--base`: Base directory for scaffold output (e.g., `./OUT`)
- `--config-dir`: Directory containing configuration files (default: `./config`)
- `--mode`: Write mode - `fail` (default), `safe`, or `overwrite`
- `--validate`: Run validation after generation
- `--manifest`: Print list of generated files

## Configuration

Configuration files in `./config/`:

- **lifecycle.yaml**: Defines 14 lifecycle phases (LC01-LC14) with phase types (PLM/OPS)
- **atdp.yaml**: Defines ATDP products (AMM, IPC, SRM, CMM) and CSDB structure

## Generated Structure

The script generates a complete aerospace project structure:

```
OUT/
├── 00-00-general/
│   ├── GENESIS/              # Frozen templates
│   ├── SSOT/                 # Single Source of Truth
│   │   ├── LC01_PROBLEM_STATEMENT/
│   │   ├── LC02_SYSTEM_REQUIREMENTS/
│   │   ├── ...
│   │   └── LC14_END_OF_LIFE/
│   ├── CSDB_REF/             # Atomic reference units
│   └── PUB/ATDP/             # Publications (AMM, IPC, SRM, CMM)
│       ├── COMMON_CSDB/      # Shared CSDB components
│       ├── PRODUCTS/         # Product-specific content
│       ├── EXPORT/           # Export outputs
│       └── IETP/             # IETP packaging
└── 00-90-tables-schemas-index/  # ATA 00-90 governance tables
```

## Example

```bash
# Generate scaffold with validation
python kiss-scaffold.py --base ./OUT --config-dir ./config --validate

# Regenerate (overwrite existing)
python kiss-scaffold.py --base ./OUT --config-dir ./config --mode overwrite --validate
```

## Implementation

This script is a wrapper that calls the main Kiss-scaffold component located at:
`/Kiss-scaffold/` in the repository root.
