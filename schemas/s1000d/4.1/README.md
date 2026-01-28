# S1000D Issue 4.1 Schemas

## Overview

This directory should contain S1000D Issue 4.1 XML schemas for legacy support.

**Status**: Legacy support only

## Schema Package Information

| Property | Value |
|----------|-------|
| Issue | 4.1 |
| Release Date | 2010 |
| Namespace | `http://www.s1000d.org/S1000D_4-1` |
| Schema Count | ~118 XSD files |
| Source | [s1000d.org](https://www.s1000d.org) |

## Installation

### Step 1: Obtain Schemas

1. Visit [https://www.s1000d.org](https://www.s1000d.org)
2. Register/login to access downloads
3. Download "S1000D Issue 4.1 XML Schemas"

### Step 2: Extract to This Directory

```bash
# Extract schema package
unzip S1000D_Issue_4-1_Schemas.zip -d .
```

### Step 3: Verify Installation

```bash
aerospacemodel doctor --check-schemas --issue 4.1
```

## Expected Contents

After installation, this directory should contain:

```
4.1/
├── README.md                       # This file
├── S1000D_4-1.xsd                  # Main schema entry point
│
├── appliccrossreftable.xsd         # ACT schema
├── brex.xsd                        # BREX schema
├── comment.xsd                     # Comment schema
├── condcrossreftable.xsd           # CCT schema
├── container.xsd                   # Container DM schema
├── descript.xsd                    # Descriptive DM schema
├── dml.xsd                         # Data Module List schema
├── faultiso.xsd                    # Fault Isolation schema
├── ipd.xsd                         # IPD schema
├── pm.xsd                          # Publication Module schema
├── proced.xsd                      # Procedural DM schema
├── prodcrossreftable.xsd           # PCT schema
│
├── common/                         # Common type definitions
└── xml/                            # XML base schemas
```

## Usage Notes

Issue 4.1 is provided for legacy support only. Use when:

- Importing legacy Issue 4.1 content for migration
- Validating archived data modules
- Supporting older customer requirements

> **Recommendation**: Migrate Issue 4.1 content to Issue 5.0 when possible.

## Migration Path

```
Issue 4.1 → Issue 4.2 → Issue 5.0
```

AEROSPACEMODEL provides migration utilities:

```bash
aerospacemodel migrate --from 4.1 --to 5.0 path/to/dm.xml
```

## Namespace Declaration

```xml
<?xml version="1.0" encoding="UTF-8"?>
<dmodule xmlns="http://www.s1000d.org/S1000D_4-1"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <!-- Data module content -->
</dmodule>
```

## Key Differences from Later Issues

| Feature | Issue 4.1 | Issue 4.2+ |
|---------|-----------|------------|
| Applicability model | Basic | Enhanced |
| BREX capabilities | Limited | Extended |
| Learning modules | No | Yes (5.0) |
| SCORM support | No | Yes (5.0) |

## License

S1000D schemas are copyright of ASD and subject to their licensing terms.
