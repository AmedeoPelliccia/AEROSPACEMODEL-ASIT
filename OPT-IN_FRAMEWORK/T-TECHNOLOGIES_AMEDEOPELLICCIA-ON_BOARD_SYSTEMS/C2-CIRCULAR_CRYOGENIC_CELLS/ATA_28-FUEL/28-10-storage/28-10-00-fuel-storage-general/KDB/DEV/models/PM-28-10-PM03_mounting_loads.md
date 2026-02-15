# PM-28-10-PM03 — Mounting / Load Path Analysis

| Key | Value |
|-----|-------|
| Model ID | PM-28-10-PM03 |
| ATA Code | 28-10-00 |
| Technology Domain | C2 — Circular Cryogenic Cells |
| Aircraft Programme | AMPEL360 Q100 |
| Lifecycle Phase | LC05 (Detail Design) |
| Status | Preliminary |
| Author | STK_ENG |
| Date | 2026-02-15 |

## Objective

Define the structural analysis model for cryogenic cell mounting and
load paths.  The model evaluates vibration response, crash loads, and
thermal cycling effects on the support structure to ensure compliance
with CS 25.561, CS 25.571, and DO-160 vibration requirements while
accommodating cryogenic thermal contraction.

---

## Load Cases

### Vibration

| ID | Name | Standard | Spectrum | Frequency Range |
|----|------|----------|----------|-----------------|
| LC-VIB-01 | Random vibration (flight) | DO-160G §8 | Cat S2 | 10–2000 Hz |
| LC-VIB-02 | Ground taxi vibration | DO-160G §8 | Cat T | 5–500 Hz |

### Crash (CS 25.561)

| ID | Direction | Load Factor | Standard |
|----|-----------|-------------|----------|
| LC-CRASH-01 | Forward | 9.0 g | CS 25.561 |
| LC-CRASH-02 | Downward | 6.0 g | CS 25.561 |
| LC-CRASH-03 | Lateral | 3.0 g | CS 25.561 |
| LC-CRASH-04 | Aft | 1.5 g | CS 25.561 |

### Thermal Cycling

| ID | Name | $\Delta T$ | Cycles |
|----|------|------------|--------|
| LC-THERM-01 | Cryogenic cool-down | 293 → 20 K (−273 K) | – |
| LC-THERM-02 | Mission thermal cycle | 293 ↔ 20 K | 20 000 over service life |

### Combined

| ID | Name | Components |
|----|------|------------|
| LC-COMB-01 | Crash + cryogenic | LC-CRASH-01 + LC-THERM-01 |

---

## Mount Concepts

| ID | Name | Thermal Contraction | Crash Retention | Heritage |
|----|------|---------------------|-----------------|----------|
| MNT-A | Ring cradle + PTFE pads | Sliding interface | Shear pins + straps | LNG marine |
| MNT-B | Bipod strut frame | Bearing articulation | Strut ultimate capacity | Spacecraft cryo |
| MNT-C | Skirt / ring-frame | Bellows / flex joints | Frame shear-web | Aircraft fuselage |

---

## Analysis Methods

| Method | Tool | Output |
|--------|------|--------|
| Modal analysis | FEA SOL 103 | Natural frequencies, mode shapes |
| Random vibration response | FEA SOL 111 | RMS stress, acceleration at mounts |
| Static crash analysis | FEA SOL 101 | Reactions, stress, margins of safety |
| Thermal stress analysis | FEA SOL 153 | Interface forces, sliding displacements |
| Fatigue & damage tolerance | Miner's rule + crack growth | Fatigue life, inspection intervals |

---

## Acceptance Criteria

| Criterion | Standard |
|-----------|----------|
| Natural frequency > 25 Hz (mounted) | DO-160G |
| Positive margin of safety — all crash cases | CS 25.561 |
| Thermal cycling life ≥ 2× design service life | CS 25.571 |
| Mount heat leak ≤ thermal budget (PM-28-10-PM02) | Thermal ICD |
| No yielding — combined crash + cryogenic | CS 25.305 |

---

## Outputs

| Output | Description |
|--------|-------------|
| Mount concept trade matrix | Weighted evaluation of MNT-A / MNT-B / MNT-C |
| Reaction force envelopes | Max mount forces per load case |
| Thermal displacement map | Contraction displacements at each mount station |
| Fatigue life prediction | Cycles to crack initiation at critical locations |
| Vibration response spectra | Tank acceleration vs frequency under DO-160 |

---

## Feeds

| Lifecycle | Artifact |
|-----------|----------|
| LC06 | Vibration and static load qualification tests |
| LC05 | Mount detail design drawings |
| LC03 | Safety FHA update — mount failure modes |

## Traceability

- **Derives from:** TS-28-10-TS01, TS-28-10-TS02, FBL-Q100-ATA28-001
- **Satisfies:** FBL-REQ-001, FBL-REQ-004, FBL-REQ-010
