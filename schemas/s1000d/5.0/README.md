# S1000D Issue 5.0 Schemas

## Overview

This directory should contain S1000D Issue 5.0 XML schemas for validating generated content.

**Status**: Primary supported issue for AEROSPACEMODEL 2.0.x

## Schema Package Information

| Property | Value |
|----------|-------|
| Issue | 5.0 |
| Release Date | 2018 |
| Namespace | `http://www.s1000d.org/S1000D_5-0` |
| Schema Count | ~127 XSD files |
| Source | [s1000d.org](https://www.s1000d.org) |

## Installation

### Step 1: Obtain Schemas

1. Visit [https://www.s1000d.org](https://www.s1000d.org)
2. Register/login to access downloads
3. Download "S1000D Issue 5.0 XML Schemas"

### Step 2: Extract to This Directory

```bash
# Extract schema package
unzip S1000D_Issue_5-0_Schemas.zip -d .

# Or copy from downloaded location
cp -r /path/to/S1000D_5-0/* .
```

### Step 3: Verify Installation

```bash
# Check schema files are present
ls -la *.xsd

# Or use AEROSPACEMODEL verification
aerospacemodel doctor --check-schemas --issue 5.0
```

## Expected Contents

After installation, this directory should contain:

```
5.0/
├── README.md                       # This file
├── S1000D_5-0.xsd                  # Main schema entry point
│
├── appliccrossreftable.xsd         # ACT schema
├── brex.xsd                        # BREX schema
├── comment.xsd                     # Comment schema
├── condcrossreftable.xsd           # CCT schema
├── container.xsd                   # Container DM schema
├── descript.xsd                    # Descriptive DM schema
├── dml.xsd                         # Data Module List schema
├── faultiso.xsd                    # Fault Isolation schema
├── frontmatter.xsd                 # Front matter schema
├── icnmetadatafile.xsd             # ICN metadata schema
├── ipd.xsd                         # IPD schema
├── learning.xsd                    # Learning DM schema
├── pmc.xsd                         # PMC schema
├── pm.xsd                          # Publication Module schema
├── proced.xsd                      # Procedural DM schema
├── prodcrossreftable.xsd           # PCT schema
├── sb.xsd                          # Service Bulletin schema
├── scormcontentpackage.xsd         # SCORM package schema
├── scocontent.xsd                  # SCO content schema
├── schedul.xsd                     # Scheduled maintenance schema
├── wrngdata.xsd                    # Wiring data schema
│
├── common/                         # Common type definitions
│   ├── S1000D_common.xsd
│   ├── dc.xsd
│   ├── rdf.xsd
│   └── ...
│
├── xlink/                          # XLink schemas
│   └── xlink.xsd
│
└── xml/                            # XML base schemas
    └── xml.xsd
```

## Key Changes in Issue 5.0

### New Features
- Enhanced applicability model
- Improved BREX capabilities
- Extended ICN metadata
- New learning module types
- SCORM 2004 support

### Schema Changes from 4.2
- Additional element types for digital content
- Extended attribute groups
- New cross-reference mechanisms
- Enhanced validation capabilities

## Usage with ASIGT

### Schema Validator Configuration

```yaml
# ASIT/config/asit_config.yaml
validation:
  s1000d:
    primary_issue: "5.0"
    schema_path: "schemas/s1000d/5.0/"
    strict_mode: true
```

### Validation Example

```python
from aerospacemodel.asigt.validators import SchemaValidator

validator = SchemaValidator(
    schema_path="schemas/s1000d/5.0/",
    strict=True
)

# Validate a descriptive data module
result = validator.validate(
    "IDB/CSDB/AMM/DMC-DEMO-A-00-00-00-00A-040A-A.xml",
    schema_type="descript"
)

if result.is_valid:
    print("Validation passed")
else:
    for error in result.errors:
        print(f"Error: {error.message} at {error.line}")
```

## Namespace Declaration

Data modules targeting Issue 5.0 must include the correct namespace:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<dmodule xmlns="http://www.s1000d.org/S1000D_5-0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.s1000d.org/S1000D_5-0 
                             ../../../schemas/s1000d/5.0/descript.xsd">
  <!-- Data module content -->
</dmodule>
```

## Troubleshooting

### Schema Files Missing

```
Error: Schema file not found: schemas/s1000d/5.0/descript.xsd
```

**Solution**: Download and extract schemas from s1000d.org

### Namespace Mismatch

```
Error: Namespace 'http://www.s1000d.org/S1000D_4-2' does not match schema
```

**Solution**: Ensure data module uses Issue 5.0 namespace

### Validation Timeout

```
Warning: Schema validation timeout after 30s
```

**Solution**: Increase timeout or validate smaller batches

## License

S1000D schemas are copyright of ASD and subject to their licensing terms. Obtain proper license before use.
