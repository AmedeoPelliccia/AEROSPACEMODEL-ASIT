# S1000D Issue 4.2 Schemas

## Overview

This directory should contain S1000D Issue 4.2 XML schemas for backward compatibility validation.

**Status**: Supported (backward compatibility)

## Schema Package Information

| Property | Value |
|----------|-------|
| Issue | 4.2 |
| Release Date | 2014 |
| Namespace | `http://www.s1000d.org/S1000D_4-2` |
| Schema Count | ~124 XSD files |
| Source | [s1000d.org](https://www.s1000d.org) |

## Installation

### Step 1: Obtain Schemas

1. Visit [https://www.s1000d.org](https://www.s1000d.org)
2. Register/login to access downloads
3. Download "S1000D Issue 4.2 XML Schemas"

### Step 2: Extract to This Directory

```bash
# Extract schema package
unzip S1000D_Issue_4-2_Schemas.zip -d .
```

### Step 3: Verify Installation

```bash
aerospacemodel doctor --check-schemas --issue 4.2
```

## Expected Contents

After installation, this directory should contain:

```
4.2/
├── README.md                       # This file
├── S1000D_4-2.xsd                  # Main schema entry point
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
├── schedul.xsd                     # Scheduled maintenance schema
├── wrngdata.xsd                    # Wiring data schema
│
├── common/                         # Common type definitions
└── xml/                            # XML base schemas
```

## Usage Notes

Issue 4.2 is widely deployed in the aerospace industry. Use this schema set when:

- Delivering to customers requiring Issue 4.2 compliance
- Migrating legacy content to newer formats
- Validating imported Issue 4.2 data modules

## Namespace Declaration

```xml
<?xml version="1.0" encoding="UTF-8"?>
<dmodule xmlns="http://www.s1000d.org/S1000D_4-2"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <!-- Data module content -->
</dmodule>
```

## License

S1000D schemas are copyright of ASD and subject to their licensing terms.
