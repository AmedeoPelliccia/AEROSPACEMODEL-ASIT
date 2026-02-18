# Engineering SSOT Front-End

**Program:** AMPEL360 Q100  
**Authority:** ASIT (Aircraft Systems Information Transponder)

---

## Overview

The **Engineering SSOT** (Single Source of Truth) front-end provides a web-based interface for navigating and querying engineering SSOT registry entries across all technology domains of the AMPEL360 Q100 program.

It is a self-contained, CDN-free HTML front-end that resides within the OPT-IN_FRAMEWORK and enables:

- Browsing the SSOT registry (`00_SSOT_REGISTRY.yaml`) in a structured table
- Filtering entries by free-text (ID/title), technology domain, and status
- Submitting Custom Information Data Sheets linked to SSOT entries
- Cross-referencing novel-technology entries with their special conditions

---

## Files

| File | Purpose |
|------|---------|
| `index.html` | Self-contained front-end with SSOT registry table and data-sheet form |
| `00_SSOT_REGISTRY.yaml` | SSOT registry with all program engineering SSOT entries |
| `README.md` | This file |

---

## SSOT Registry (`00_SSOT_REGISTRY.yaml`)

The registry captures the canonical SSOT entries for the AMPEL360 Q100 program. Each entry includes:

- `id` — Unique SSOT identifier (e.g., `SSOT-Q100-C2-001`)
- `title` — Human-readable title
- `ata_chapter` — ATA chapter (e.g., `28`)
- `technology_domain` — Technology subdomain (e.g., `C2-CIRCULAR_CRYOGENIC_CELLS`)
- `baseline_ref` — Reference to the controlling baseline
- `lifecycle_phase` — Primary lifecycle phase (LC01–LC14)
- `status` — `draft`, `in_review`, or `approved`
- `special_conditions` — Applicable special conditions (if any)

---

## Usage

Open `index.html` in a web browser. No server or external dependencies required.

---

## Related Documents

- [OPT-IN_FRAMEWORK README](../README.md)
- [OPT-IN_FRAMEWORK Index](../00_INDEX.md)
- [Lifecycle Phase Registry](../../lifecycle/LC_PHASE_REGISTRY.yaml)

---
