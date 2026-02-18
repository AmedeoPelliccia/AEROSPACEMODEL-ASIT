# ENGINEERING_SSOT

**Engineering Single Source of Truth (SSOT) Front-End**  
**Program:** AMPEL360 Q100  
**Authority:** ASIT (Aircraft Systems Information Transponder)

---

## Overview

The **ENGINEERING_SSOT** directory provides the authoritative registry of engineering data sources and a self-contained front-end interface for the AMPEL360 Q100 program.

It serves as the single point of reference for all engineering data — linking ATA chapter artifacts, lifecycle phases, technology domains, and Custom Information Data Sheets to their canonical locations within the OPT-IN_FRAMEWORK.

---

## Contents

| File | Description |
|------|-------------|
| `index.html` | Self-contained front-end for browsing the SSOT registry |
| `00_SSOT_REGISTRY.yaml` | Authoritative YAML registry of all SSOT entries |
| `README.md` | This file |

---

## SSOT Registry Structure

The `00_SSOT_REGISTRY.yaml` file contains:

- **metadata** — Program identification and version information
- **ssot_entries** — One entry per ATA chapter / technology domain combination
- **custom_data_sheets** — Custom Information Data Sheet (CIDS) index

Each SSOT entry provides:
- Unique identifier (`id`)
- Title and ATA chapter reference
- Technology domain classification
- Baseline reference and lifecycle phase
- Status (`draft`, `in_review`, or `approved`)
- Special conditions (where applicable)

---

## Front-End Usage

Open `index.html` directly in a browser — no server or external dependencies required.

The front-end provides:
- Browsable SSOT registry table
- Custom Information Data Sheet submission form
- Links to canonical OPT-IN_FRAMEWORK paths

---

## Related Documentation

| Document | Path |
|----------|------|
| OPT-IN_FRAMEWORK Index | `../00_INDEX.md` |
| OPT-IN_FRAMEWORK README | `../README.md` |
| LC Phase Registry | `../../lifecycle/LC_PHASE_REGISTRY.yaml` |

---

*End of ENGINEERING_SSOT README*
