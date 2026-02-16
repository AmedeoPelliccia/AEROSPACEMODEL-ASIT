# Kiss-scaffold

**Aircraft GenKISS (General Knowledge and Information Standard Systems) Scaffold Generator** for aerospace project structures.

## Overview

Kiss-scaffold generates standard aerospace project structures with lifecycle phases compliant with industry standards. GenKISS provides a deterministic, traceable framework for organizing aerospace technical data following the "Keep It Super Simple" principle while maintaining rigorous governance.

It creates a complete directory hierarchy including:

- **GENESIS**: Frozen project definitions and templates
- **SSOT**: Single Source of Truth for lifecycle artifacts (LC01-LC14)
- **00-00-general/PUB/ATDP**: S1000D CSDB ATDP structure for publications
- **CSDB_REF**: Reference repository for cross-linked CSDB objects
- **00-90-tables-schemas-index**: ATA 00-90 monitoring, schemas, and tracking tables

## Features

- ✅ **14 Canonical Lifecycle Phases** (LC01-LC14)
- ✅ **Atomic File Writes** for transaction safety
- ✅ **Validation Rules** for structure integrity
- ✅ **Configurable** via YAML files
- ✅ **Tested** with integration tests
- ✅ **Logging Support** with configurable levels
- ✅ **Environment Variables** for deployment flexibility
- ✅ **Manifest Generation** for file tracking
- ✅ **Proper Exit Codes** for CI/CD integration

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Generate a scaffold:

```bash
python Kiss-scaffold.py --base ./OUT --config-dir ./config --validate --manifest
```

### Command-Line Options

- `--base`: Base directory for scaffold output
- `--config-dir`: Directory containing lifecycle.yaml and atdp.yaml
- `--mode`: Write mode - `fail` (default), `safe`, or `overwrite`
- `--validate`: Run validation after generation
- `--manifest`: Write manifest file with list of generated files
- `--timestamp`: ISO timestamp for generation (default: current UTC time)
- `--log-level`: Logging level - `DEBUG`, `INFO` (default), `WARNING`, `ERROR`, `CRITICAL`

### Environment Variables

Override command-line arguments with environment variables:

- `KISS_BASE`: Override `--base` argument
- `KISS_CONFIG_DIR`: Override `--config-dir` argument

Example:
```bash
export KISS_BASE=/opt/aerospace/scaffold
export KISS_CONFIG_DIR=/etc/kiss-scaffold
python Kiss-scaffold.py --base ./OUT --config-dir ./config
# Uses /opt/aerospace/scaffold and /etc/kiss-scaffold instead
```

### Exit Codes

- `0`: Success
- `2`: Invalid timestamp
- `3`: Configuration error
- `4`: Generation conflict (file collision in fail mode)
- `5`: Generation failure
- `6`: Validation failed
- `7`: Manifest write failed

## Configuration

### lifecycle.yaml

Defines the 14 lifecycle phases with metadata:

```yaml
phases:
  LC01_PROBLEM_STATEMENT:
    phase_type: PLM
    canonical_name: Problem Statement
    ssot_dir: 00-00-general/SSOT/LC01_PROBLEM_STATEMENT
  # ... LC02-LC14
```

### atdp.yaml

Defines ATDP (Authorized Technical Data Products) and CSDB structure:

```yaml
products:
  - AMM  # Aircraft Maintenance Manual
  - IPC  # Illustrated Parts Catalog
  - SRM  # Structural Repair Manual
  - CMM  # Component Maintenance Manual

common_csdb_dirs:
  - DM  # Data Modules
  - PM  # Publication Modules
```

## Lifecycle Phases

### PLM Phases (LC01-LC10)
1. **LC01**: Problem Statement
2. **LC02**: System Requirements
3. **LC03**: Safety & Reliability
4. **LC04**: Design Definition
5. **LC05**: Analysis Models
6. **LC06**: Verification
7. **LC07**: QA & Process Compliance
8. **LC08**: Configuration
9. **LC09**: ESG & Sustainability
10. **LC10**: Industrial & Supply Chain

### OPS Phases (LC11-LC14)
11. **LC11**: Operations Customization
12. **LC12**: Continued Airworthiness & MRO
13. **LC13**: Maintenance Source Data
14. **LC14**: End of Life

## Validation Rules

The validator enforces "Locked Rules":

1. **Rule 1**: No `_executions` directories in GENESIS (frozen templates)
2. **Rule 2**: `artifact.*` files are only allowed under `SSOT/**/_executions/**`
3. **Rule 3**: Required `PUB/ATDP` structure must exist (COMMON_CSDB, PRODUCTS, EXPORT, IETP)
4. **Canonical LC Set**: Exactly 14 lifecycle directories must exist in SSOT

## Testing

Run the test suite:

```bash
pytest -q
```

Run integration tests:

```bash
pytest tests/test_integration.py -v
```

## CI/CD

GitHub Actions workflow runs automatically on push/PR:

```yaml
- Install dependencies
- Run pytest
- Generate and validate scaffold
```

## License

Part of the AEROSPACEMODEL repository - see root LICENSE file.
