# ATA Specifications

## Overview

This directory contains reference data and schemas related to ATA (Air Transport Association) specifications, primarily ATA iSpec 2200 for aircraft system numbering and organization.

## Directory Structure

```
ata/
├── README.md           # This file
└── ispec2200/          # ATA iSpec 2200 reference data
```

## ATA iSpec 2200

ATA iSpec 2200 is the industry standard for aircraft documentation, defining:

- **ATA Chapter Numbering** (Chapters 00-99)
- **System/Subsystem breakdown**
- **Document type codes**
- **Standard maintenance practices**

## Obtaining ATA iSpec 2200

ATA iSpec 2200 is maintained by A4A (Airlines for America) and is available through:

1. **A4A Direct**: [https://www.airlines.org](https://www.airlines.org)
2. **ATA Publications**: Contact A4A publications department

> **Note**: ATA iSpec 2200 is a licensed specification. Users must obtain appropriate licenses for production use.

## Usage in AEROSPACEMODEL

ATA chapter mapping is used throughout ASIT-ASIGT for:

- Organizing content by aircraft system
- Validating ATA chapter assignments
- Mapping engineering data to publication structure
- Cross-referencing between publications

### Configuration Reference

```yaml
# ASIT/STRUCTURE/ATA_MAPPING.yaml
# Defines the ATA chapter structure for the program
```

## ATA Chapter Overview

| Range | Domain |
|-------|--------|
| 00-19 | General |
| 20-29 | Airframe Systems |
| 30-49 | Power Systems |
| 50-59 | Auxiliary Systems |
| 60-69 | Propellers/Rotors |
| 70-79 | Power Plant |
| 80-89 | Starting/Ignition |
| 90-99 | Reserved |

## Integration Points

The ATA reference data is used by:

1. **ASIT STRUCTURE**: Defines valid ATA chapter assignments
2. **ASIGT Generators**: Maps content to correct chapters
3. **Validators**: Verifies ATA chapter compliance
4. **Pipelines**: Organizes publication scope by chapter

## License

ATA iSpec 2200 is copyright of A4A. Users must obtain appropriate licenses for production use.
