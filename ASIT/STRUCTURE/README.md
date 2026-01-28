# ASIT Structure

## Overview

The **STRUCTURE** module defines the system breakdown, information partitioning, lifecycle phases, and naming conventions that govern all artifacts within the ASIT-ASIGT framework.

> **Structure precedes content. No generation without structural definition.**

---

## Purpose

| Function | Description |
|----------|-------------|
| **ATA Mapping** | Aircraft system breakdown per ATA iSpec 2200 |
| **KDB/IDB Partition** | Separation of engineering knowledge from operational information |
| **Lifecycle Phases** | LC01–LC14 phase definitions and transitions |
| **Naming Conventions** | ID grammar for all artifacts |

---

## Directory Structure

```
STRUCTURE/
├── README.md                       # This file
├── ATA_MAPPING.yaml                # ATA iSpec 2200 chapter mapping
├── KDB_IDB_PARTITION.md            # Knowledge vs Information separation
├── LIFECYCLE_PHASES.yaml           # LC01–LC14 definitions
└── NAMING_CONVENTIONS.md           # ID grammar
```

---

## Key Concepts

### ATA iSpec 2200

The ATA iSpec 2200 standard defines the chapter/section/subject breakdown for aircraft documentation:

| Level | Description | Example |
|-------|-------------|---------|
| Chapter | Major system | 28 - Fuel |
| Section | Subsystem | 28-10 - Storage |
| Subject | Component/topic | 28-10-01 - Fuel Tanks |

### Knowledge Database (KDB) vs Information Database (IDB)

| Database | Contains | Owner |
|----------|----------|-------|
| **KDB** | Engineering truth (SSOT) | Engineering |
| **IDB** | Operational publications | Publications |

### Lifecycle Phases (LC01–LC14)

The lifecycle model spans from concept through disposal:

| Phase | Name | Description |
|-------|------|-------------|
| LC01 | Concept | Initial concept definition |
| LC02 | Requirements | System requirements |
| LC03 | Design | Preliminary and detailed design |
| LC04 | Development | Build and integration |
| LC05 | Verification | Test and validation |
| LC06 | Certification | Type certificate |
| LC07 | Production | Serial manufacturing |
| LC08 | Delivery | Customer acceptance |
| LC09 | Operations | In-service use |
| LC10 | Maintenance | Scheduled/unscheduled MRO |
| LC11 | Modification | In-service changes |
| LC12 | Storage | Preservation |
| LC13 | Retirement | End of service |
| LC14 | Disposal | Decommissioning |

---

## Related Documents

- [ATA_MAPPING.yaml](ATA_MAPPING.yaml) — Complete ATA chapter mapping
- [KDB_IDB_PARTITION.md](KDB_IDB_PARTITION.md) — Database partitioning rules
- [LIFECYCLE_PHASES.yaml](LIFECYCLE_PHASES.yaml) — Lifecycle definitions
- [NAMING_CONVENTIONS.md](NAMING_CONVENTIONS.md) — ID grammar
