# WBS Meta File Generator

This directory contains tools for managing Work Breakdown Structure (WBS) metadata files for the ATA 28 LH₂ Fuel System.

## Overview

The WBS Level 2 specification (`WBS_LEVEL_2.yaml`) defines work packages with detailed outputs, file formats, and verification requirements. Each output specifies a set of deliverable files and a corresponding `.meta.yaml` sidecar file that contains metadata about those deliverables.

## Generated Structure

The expanded WBS_LEVEL_2.yaml now includes:

- **8 Work Packages** (5 for Tank Development, 3 for Leak Detection)
- **23 Output Definitions** with detailed format specifications
- **23 Generated .meta.yaml files** with complete metadata

### Work Packages

#### WP-28-03: Tank Development
- **WP-28-03-01**: Cell Design (geometry, structural models, ICDs)
- **WP-28-03-02**: Insulation (MLI architecture, thermal models, test plans)
- **WP-28-03-03**: Pressure Systems (architecture, relief/vent sizing, FMEA)
- **WP-28-03-04**: Materials Qualification (test plans, qualification datasets)
- **WP-28-03-05**: Manufacturing Process (manufacturing flow, tooling, FAI plans)

#### WP-28-06: Leak Detection
- **WP-28-06-01**: Sensor Selection (trade studies, sensor baseline)
- **WP-28-06-02**: System Architecture (architecture, sensor placement, reliability)
- **WP-28-06-03**: Threshold Calibration (threshold specs, procedures, performance)

## Files

### WBS_LEVEL_2.yaml
The expanded WBS specification containing:
- Work package definitions
- Output specifications with file lists
- Format registry
- Verification requirements

### scripts/generate_wbs_meta_files.py
Python script that generates `.meta.yaml` sidecar files for all outputs defined in WBS_LEVEL_2.yaml.

## Usage

### Generate All Meta Files

```bash
python scripts/generate_wbs_meta_files.py
```

This will generate all 23 `.meta.yaml` files in their respective lifecycle directories (LC03-LC07).

### Dry Run (Preview Only)

```bash
python scripts/generate_wbs_meta_files.py --dry-run
```

This shows what files would be generated without actually creating them.

### Custom Paths

```bash
python scripts/generate_wbs_meta_files.py \
  --wbs-file path/to/WBS_LEVEL_2.yaml \
  --base-path path/to/output/directory
```

## Meta File Structure

Each `.meta.yaml` file contains:

```yaml
output_id: <output identifier>
work_package: <WP-ID>
title: <Work Package Title - Output ID>
owner: <STK_ENG or STK_SAF>
revision: <version>
status: <draft|released|...>
lc_phase: <LC03|LC04|LC05|LC06|LC07>
ata: <ATA chapter code>
domain: <technical domain>
created_on: <ISO timestamp>
last_updated_on: <ISO timestamp>
integrity:
  checksum: to be generated upon baseline finalization
  algorithm: sha256
links:
  reqs: []
  safety: []
  work_package: <WP-ID>
  verification: [<verification IDs>]
tags: [<tags>]
formats: [<format list>]
files:
  - file: <file path>
    id: <file ID>
    type: <file type>
```

## Directory Structure

Generated files are organized by lifecycle phase and ATA chapter:

```
ATA_28-FUEL/
├── LC03_SAFETY_RELIABILITY/
│   └── ATA_28-41-00/
├── LC04_DESIGN_DEFINITION/
│   ├── ATA_28-10-00/
│   ├── ATA_28-11-00/
│   └── ATA_28-41-00/
├── LC05_VERIFICATION_VALIDATION/
│   ├── ATA_28-10-00/
│   ├── ATA_28-11-00/
│   └── ATA_28-41-00/
├── LC06_CERTIFICATION_EVIDENCE/
│   ├── ATA_28-11-00/
│   └── ATA_28-41-00/
└── LC07_INDUSTRIALIZATION/
    └── ATA_28-11-00/
```

## Meta File Fields

### Required Fields
- `output_id`: Unique identifier for the output
- `work_package`: Parent work package ID
- `title`: Human-readable title
- `owner`: Responsible stakeholder (STK_ENG, STK_SAF)
- `revision`: Version number (semver)
- `status`: Current lifecycle status
- `lc_phase`: Lifecycle phase (LC03-LC07)

### Integrity Fields
- `integrity.checksum`: SHA-256 checksum (placeholder until baseline)
- `integrity.algorithm`: Hashing algorithm (sha256)

### Link Fields
- `links.reqs`: Links to requirements (empty by default)
- `links.safety`: Links to safety items (empty by default)
- `links.work_package`: Parent work package
- `links.verification`: Verification activities

### Metadata Fields
- `ata`: ATA chapter code (e.g., "28-11-00")
- `domain`: Technical domain (C2-CIRCULAR_CRYOGENIC_CELLS)
- `tags`: Searchable tags
- `formats`: List of file formats in this output
- `files`: List of deliverable files with metadata

## Conventions

### Naming Conventions
- Meta files use the pattern: `<PREFIX>-<ATA>-<ID>.meta.yaml`
- File IDs are extracted from the primary file name
- Types are determined from file extensions

### Lifecycle Phases
- **LC03**: Safety & Reliability (trade studies, safety cases)
- **LC04**: Design Definition (CAD, analysis, requirements)
- **LC05**: Verification & Validation (test plans, analysis reports)
- **LC06**: Certification Evidence (qualification reports, manufacturing)
- **LC07**: Industrialization (FAI, production)

### Ownership
- **STK_ENG**: Engineering stakeholder (design, manufacturing)
- **STK_SAF**: Safety stakeholder (leak detection, safety assessment)

## Regeneration

To regenerate meta files after updating WBS_LEVEL_2.yaml:

1. Update the WBS_LEVEL_2.yaml with new outputs or changes
2. Run the generator: `python scripts/generate_wbs_meta_files.py`
3. Review generated files for correctness
4. Commit changes to version control

## Integration

These meta files integrate with:
- **ASIT (Aircraft Systems Information Transponder)**: Metadata management
- **BREX validation**: Business rule exchange compliance
- **Lifecycle management**: Phase transitions and approvals
- **Traceability**: Requirements and verification linkage

## References

- [ASIT Core Specification](../../ASIT/ASIT_CORE.md)
- [S1000D Issue 5.0](https://www.s1000d.org)
- [ATA iSpec 2200](https://www.ata.org)
- [WBS_LEVEL_1.yaml](WBS_LEVEL_1.yaml) - Parent work breakdown structure

---

*Generated: 2026-02-17*  
*Version: 1.0.0*
