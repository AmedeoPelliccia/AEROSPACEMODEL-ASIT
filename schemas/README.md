# Schemas Directory

## Overview

This directory contains industry-standard XML schemas used for validation of generated S1000D content and ATA iSpec 2200 compliance.

> **Note**: The actual schema files are **not distributed** with this repository due to licensing restrictions. This directory provides the structure and instructions for obtaining and installing the required schemas.

## Directory Structure

```
schemas/
├── README.md                   # This file
├── s1000d/                     # S1000D XML Schemas
│   ├── 5.0/                    # Issue 5.0 (primary)
│   ├── 4.2/                    # Issue 4.2 (backward compatibility)
│   └── 4.1/                    # Issue 4.1 (legacy support)
└── ata/                        # ATA Specifications
    └── ispec2200/              # iSpec 2200 reference data
```

## Schema Sources

### S1000D Schemas

S1000D XML schemas are maintained by ASD (AeroSpace and Defence Industries Association of Europe) and distributed through the S1000D website.

| Issue | Source | Notes |
|-------|--------|-------|
| 5.0 | [s1000d.org](https://www.s1000d.org) | Current issue, recommended |
| 4.2 | [s1000d.org](https://www.s1000d.org) | Widely deployed |
| 4.1 | [s1000d.org](https://www.s1000d.org) | Legacy support |

**To obtain S1000D schemas:**
1. Visit [https://www.s1000d.org](https://www.s1000d.org)
2. Register for access (free for ASD members, fee for others)
3. Download the schema package for each required issue
4. Extract to the appropriate subdirectory

### ATA iSpec 2200

ATA iSpec 2200 is maintained by A4A (Airlines for America) and provides the standard for aircraft system numbering.

**To obtain ATA iSpec 2200:**
1. Contact A4A at [https://www.airlines.org](https://www.airlines.org)
2. Purchase or obtain license for iSpec 2200
3. Extract reference data to `ata/ispec2200/`

## Installation

### Automatic Installation

```bash
# Install schemas using the CLI (requires valid credentials)
aerospacemodel schemas install --issue 5.0 --username <user> --password <pass>
```

### Manual Installation

1. Download schema packages from official sources
2. Extract to appropriate directories:

```bash
# S1000D Issue 5.0
unzip S1000D_5-0_Schemas.zip -d schemas/s1000d/5.0/

# S1000D Issue 4.2
unzip S1000D_4-2_Schemas.zip -d schemas/s1000d/4.2/

# S1000D Issue 4.1
unzip S1000D_4-1_Schemas.zip -d schemas/s1000d/4.1/
```

## Schema Verification

After installation, verify schemas are correctly installed:

```bash
aerospacemodel doctor --check-schemas
```

Expected output:
```
Checking schemas...
  ✓ S1000D 5.0: 127 schemas found
  ✓ S1000D 4.2: 124 schemas found
  ✓ S1000D 4.1: 118 schemas found
  ✓ ATA iSpec 2200: Reference data found
All schema checks passed.
```

## Usage in ASIGT

Schemas are automatically referenced during validation:

```python
from aerospacemodel.asigt.validators import SchemaValidator

validator = SchemaValidator(schema_path="schemas/s1000d/5.0/")
result = validator.validate(data_module)
```

## Version Compatibility

| AEROSPACEMODEL Version | S1000D 5.0 | S1000D 4.2 | S1000D 4.1 |
|------------------------|------------|------------|------------|
| 2.0.x | ✓ Primary | ✓ Supported | ✓ Legacy |
| 1.x.x | - | ✓ Primary | ✓ Supported |

## License Notes

- **S1000D Schemas**: Subject to ASD licensing terms
- **ATA iSpec 2200**: Subject to A4A licensing terms
- **This repository**: Does not include copyrighted schema content

Users are responsible for obtaining appropriate licenses for schema use in their projects.

## Support

For schema-related issues:
- S1000D: Contact ASD S1000D Steering Committee
- ATA: Contact A4A Technical Operations
- AEROSPACEMODEL integration: Open a GitHub issue
