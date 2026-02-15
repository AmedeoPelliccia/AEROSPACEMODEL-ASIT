# KDB/DEV Prototypes — 28-10-00 Fuel Storage General

This directory holds **development prototypes** for the ATA 28-10-00
Fuel Storage General subject area. Content here is mutable,
work-in-progress, and **NOT baselined**.

> **Policy:** Prototypes must not be referenced by publications or
> contracts. Promotion to `KDB/LM/` requires BREX validation,
> trace coverage, and STK_ENG approval (see `KDB/README.md`).

## Contents

| File | Description |
|------|-------------|
| `CRYO_TANK_CUTAWAY.html` | Interactive 3-D cutaway of C2 circular cryogenic LH₂ storage tank |

## CRYO_TANK_CUTAWAY.html

Self-contained HTML prototype using React 18 and Three.js (r162) for
an interactive WebGL visualisation of the circular cryogenic cell
liquid-hydrogen storage tank.

### Layers Visualised

1. **Inner Pressure Vessel** — Al-Li, 3 mm wall, 20 K / 3.5 bar
2. **Liquid Hydrogen (LH₂)** — 20.28 K, 70.8 kg/m³
3. **MLI Blanket (60 layers)** — aluminised Mylar + Dacron spacers
4. **Vacuum Annulus** — 10⁻⁵ torr
5. **Outer Vacuum Jacket** — CFRP composite, ~290 K
6. **Ring Cradle Mounts** — PTFE slide pads, shear pins, tension straps
7. **Bipod Composite Struts** — G10-CR fiberglass on spherical bearings
8. **Feed-through Penetration** — bayonet coupling with bellows

### Controls

- **Drag** — Orbit the model
- **Scroll** — Zoom in/out
- **Cutaway slider** — Adjust the angular section cut (30°–360°)
- **Label dots** — Click to show/hide component descriptions
- **Legend sidebar** — Click any layer to highlight it

### Usage

Open `CRYO_TANK_CUTAWAY.html` directly in a modern browser
(Chrome, Firefox, Edge, Safari). No build step or local server required.

### Technology Domain

- **ATA Chapter:** 28-10 (Fuel Storage)
- **Technology:** C2 — Circular Cryogenic Cells
- **Special Conditions:** SC-28-H2-001, SC-28-CRYO-002
