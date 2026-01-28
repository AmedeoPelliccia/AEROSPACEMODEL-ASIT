# ATA iSpec 2200 Reference Data

## Overview

This directory should contain ATA iSpec 2200 reference data used for validating ATA chapter assignments and system organization.

**Status**: Required for production use

## Specification Information

| Property | Value |
|----------|-------|
| Specification | ATA iSpec 2200 |
| Maintainer | A4A (Airlines for America) |
| Current Revision | Rev 2023 |
| Source | [airlines.org](https://www.airlines.org) |

## Installation

### Step 1: Obtain iSpec 2200

1. Contact A4A at [https://www.airlines.org](https://www.airlines.org)
2. Purchase or obtain license for iSpec 2200
3. Download reference data package

### Step 2: Extract Reference Data

```bash
# Extract to this directory
unzip ATA_iSpec2200_RefData.zip -d .
```

### Step 3: Verify Installation

```bash
aerospacemodel doctor --check-ata
```

## Expected Contents

After installation, this directory should contain:

```
ispec2200/
├── README.md                   # This file
├── ata_chapters.yaml           # Chapter definitions
├── ata_systems.yaml            # System/subsystem breakdown
├── ata_zones.yaml              # Aircraft zone definitions
├── ata_document_types.yaml     # Document type codes
└── validation/
    └── ata_rules.yaml          # Validation rules
```

## Reference Data Format

### ATA Chapters (ata_chapters.yaml)

```yaml
chapters:
  - chapter: "00"
    title: "General"
    description: "General information applicable to complete aircraft"
    
  - chapter: "05"
    title: "Time Limits/Maintenance Checks"
    description: "Scheduled maintenance requirements"
    
  - chapter: "20"
    title: "Standard Practices - Airframe"
    description: "Standard practices for airframe maintenance"
    
  # ... continues through chapter 99
```

### ATA Systems (ata_systems.yaml)

```yaml
systems:
  "21":
    title: "Air Conditioning"
    subsystems:
      "21-00": "General"
      "21-10": "Compression"
      "21-20": "Distribution"
      "21-30": "Pressurization Control"
      "21-40": "Heating"
      "21-50": "Cooling"
      "21-60": "Temperature Control"
      "21-70": "Moisture/Air Contaminant Control"
      
  "27":
    title: "Flight Controls"
    subsystems:
      "27-00": "General"
      "27-10": "Aileron"
      "27-20": "Rudder"
      "27-30": "Elevator"
      # ... etc
```

## ATA Chapter Reference

### Complete Chapter List

| Chapter | Title |
|---------|-------|
| 00 | General |
| 01-04 | Reserved |
| 05 | Time Limits/Maintenance Checks |
| 06 | Dimensions and Areas |
| 07 | Lifting and Shoring |
| 08 | Leveling and Weighing |
| 09 | Towing and Taxiing |
| 10 | Parking, Mooring, Storage and Return to Service |
| 11 | Placards and Markings |
| 12 | Servicing |
| 13-19 | Reserved |
| 20 | Standard Practices - Airframe |
| 21 | Air Conditioning |
| 22 | Auto Flight |
| 23 | Communications |
| 24 | Electrical Power |
| 25 | Equipment/Furnishings |
| 26 | Fire Protection |
| 27 | Flight Controls |
| 28 | Fuel |
| 29 | Hydraulic Power |
| 30 | Ice and Rain Protection |
| 31 | Indicating/Recording Systems |
| 32 | Landing Gear |
| 33 | Lights |
| 34 | Navigation |
| 35 | Oxygen |
| 36 | Pneumatic |
| 37 | Vacuum |
| 38 | Water/Waste |
| 39 | Electrical-Electronic Panels and Multipurpose Components |
| 40-44 | Reserved |
| 45 | Central Maintenance System (CMS) |
| 46 | Information Systems |
| 47 | Inert Gas System |
| 48 | In-Flight Fuel Dispensing |
| 49 | Airborne Auxiliary Power |
| 50 | Cargo and Accessory Compartments |
| 51 | Standard Practices and Structures - General |
| 52 | Doors |
| 53 | Fuselage |
| 54 | Nacelles/Pylons |
| 55 | Stabilizers |
| 56 | Windows |
| 57 | Wings |
| 58-59 | Reserved |
| 60 | Standard Practices - Propeller/Rotor |
| 61 | Propellers/Propulsors |
| 62 | Main Rotor(s) |
| 63 | Main Rotor Drive(s) |
| 64 | Tail Rotor |
| 65 | Tail Rotor Drive |
| 66 | Folding Blades/Pylon |
| 67 | Rotors Flight Control |
| 68-70 | Reserved |
| 71 | Power Plant - General |
| 72 | Engine - Turbine/Turboprop, Ducted Fan/Unducted Fan |
| 73 | Engine Fuel and Control |
| 74 | Ignition |
| 75 | Air |
| 76 | Engine Controls |
| 77 | Engine Indicating |
| 78 | Exhaust |
| 79 | Oil |
| 80 | Starting |
| 81 | Turbines |
| 82 | Water Injection |
| 83 | Accessory Gearboxes |
| 84 | Propulsion Augmentation |
| 85 | Fuel Cell Systems |
| 86-90 | Reserved |
| 91 | Charts |
| 92 | Electrical Installations |
| 93-96 | Reserved |
| 97 | Wiring Reporting |
| 98-99 | Reserved |

## Usage in ASIGT

### Validation Example

```python
from aerospacemodel.asigt.validators import ATAValidator

validator = ATAValidator(
    ata_path="schemas/ata/ispec2200/"
)

# Validate ATA chapter assignment
result = validator.validate_chapter("21-30-00")
# Returns: valid=True, title="Pressurization Control"

# Validate system breakdown
result = validator.validate_system_breakdown("27-10-05")
# Returns: valid=True, hierarchy=["Flight Controls", "Aileron", "Subsection"]
```

### Pipeline Reference

```yaml
# pipelines/amm_pipeline.yaml
scope:
  ata_chapters:
    - "21"  # Air Conditioning
    - "27"  # Flight Controls
    - "28"  # Fuel
```

## License

ATA iSpec 2200 is copyright of A4A (Airlines for America). Users must obtain appropriate licenses for production use.

## Support

- **A4A Publications**: publications@airlines.org
- **ATA Spec 2200 Queries**: Contact A4A technical support
