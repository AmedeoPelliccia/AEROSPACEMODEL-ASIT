# S1000D XML Schemas

## Overview

This directory contains S1000D XML schema files used for validating generated data modules, publication modules, and other S1000D artifacts.

## Supported Issues

| Issue | Directory | Status | Release Date |
|-------|-----------|--------|--------------|
| 5.0 | `5.0/` | **Primary** | 2018 |
| 4.2 | `4.2/` | Supported | 2014 |
| 4.1 | `4.1/` | Legacy | 2010 |

## Schema Categories

Each issue directory should contain the following schema categories:

```
<issue>/
├── descript/           # Descriptive data module schemas
├── proced/             # Procedural data module schemas
├── faultiso/           # Fault isolation schemas
├── ipd/                # Illustrated parts data schemas
├── appliccrossref/     # Applicability cross-reference
├── pm/                 # Publication module schemas
├── dml/                # Data module list schemas
├── comment/            # Comment schemas
├── icnmetadata/        # ICN metadata schemas
├── brex/               # Business rules exchange schemas
├── container/          # Container data module schemas
├── common/             # Common elements and types
├── xlink/              # XLink schemas
└── xml/                # XML base schemas
```

## Key Schema Files

### Data Module Schemas

| Schema | Purpose |
|--------|---------|
| `descript.xsd` | Descriptive content (descriptions, theory) |
| `proced.xsd` | Procedural content (tasks, steps) |
| `faultiso.xsd` | Fault isolation (troubleshooting) |
| `ipd.xsd` | Illustrated parts data |
| `crew.xsd` | Crew/operator procedures |
| `process.xsd` | Process data modules |
| `wrngdata.xsd` | Wiring data |
| `sched.xsd` | Scheduled maintenance |

### Publication Schemas

| Schema | Purpose |
|--------|---------|
| `pm.xsd` | Publication module structure |
| `dml.xsd` | Data module list |
| `icnmetadatafile.xsd` | ICN (graphic) metadata |
| `comment.xsd` | Comments and annotations |

### Support Schemas

| Schema | Purpose |
|--------|---------|
| `brex.xsd` | Business rules exchange |
| `appliccrossreftable.xsd` | ACT (Applicability Cross-reference Table) |
| `condcrossreftable.xsd` | CCT (Condition Cross-reference Table) |
| `prodcrossreftable.xsd` | PCT (Product Cross-reference Table) |

## Installation Instructions

### From S1000D.org

1. Go to [https://www.s1000d.org](https://www.s1000d.org)
2. Navigate to Downloads → Schemas
3. Download the schema package for each required issue
4. Extract to the appropriate directory

### Expected Directory Contents

After extraction, each issue directory should contain:

**S1000D Issue 5.0** (`5.0/`):
- ~127 XSD files
- Common type definitions
- Namespace: `http://www.s1000d.org/S1000D_5-0`

**S1000D Issue 4.2** (`4.2/`):
- ~124 XSD files
- Common type definitions
- Namespace: `http://www.s1000d.org/S1000D_4-2`

**S1000D Issue 4.1** (`4.1/`):
- ~118 XSD files
- Common type definitions
- Namespace: `http://www.s1000d.org/S1000D_4-1`

## Validation Usage

### Command Line

```bash
# Validate a data module against Issue 5.0
aerospacemodel validate --schema 5.0 path/to/datamodule.xml

# Validate all DMs in a CSDB
aerospacemodel validate --schema 5.0 --recursive IDB/CSDB/AMM/
```

### Python API

```python
from aerospacemodel.asigt.validators import SchemaValidator

# Initialize validator with specific issue
validator = SchemaValidator(
    schema_path="schemas/s1000d/5.0/",
    issue="5.0"
)

# Validate single data module
result = validator.validate_file("path/to/dm.xml")

# Validate multiple data modules
results = validator.validate_batch(["dm1.xml", "dm2.xml", "dm3.xml"])

# Get validation report
report = validator.generate_report(results)
```

## Schema Customization

S1000D allows project-specific schema customizations through BREX. Custom schemas should be placed in:

```
schemas/s1000d/<issue>/custom/
```

Reference custom schemas in your BREX configuration:

```yaml
# ASIGT/brex/project_brex.yaml
schema_customizations:
  base_issue: "5.0"
  custom_schemas:
    - "schemas/s1000d/5.0/custom/project_types.xsd"
```

## Troubleshooting

### Common Issues

**Schema not found errors:**
- Verify schema files are extracted to correct directory
- Check file permissions
- Run `aerospacemodel doctor --check-schemas`

**Namespace mismatch:**
- Ensure data module declares correct namespace for target issue
- Check schema version matches data module issue number

**Validation failures:**
- Review BREX rules for project-specific constraints
- Check S1000D issue compatibility

## References

- [S1000D Specification](https://www.s1000d.org)
- [S1000D Issue 5.0 Documentation](https://www.s1000d.org/Downloads/Pages/S1000DDownloads.aspx)
- [ASD S1000D Steering Committee](https://www.asd-europe.org)
