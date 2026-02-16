# Engineering Change Request (ECR)

## Header

| Field               | Value                                                              |
|---------------------|--------------------------------------------------------------------|
| **ECR ID**          | ECR-ATA28-11-CS25-SSOT-001                                        |
| **Title**           | CS-25 compliance matrix and SSOT promotion for LH₂ primary tank   |
| **Requestor**       | STK_ENG                                                            |
| **Date**            | 2026-02-16                                                         |
| **Affected ATA**    | 28-11-00                                                           |
| **Priority**        | High                                                               |
| **Status**          | Open                                                               |

## Description of Change

Promote the CS-25 compliance matrix (`CS25_compliance_matrix.yaml`) from
`KDB/DEV/trade-studies/` to `KDB/LM/SSOT/` as the single source of truth for
LH₂ primary tank certification compliance.

### Scope

The compliance matrix covers:

| Section | Title                                | Requirements |
|---------|--------------------------------------|:------------:|
| A       | Tank Structural Integrity and Loads  | CM-A-001 … CM-A-004 |
| B       | Pressure, Venting and Boil-Off       | CM-B-001 … CM-B-002 |
| C       | Fire, Explosion and Ignition Prevention | CM-C-001 … CM-C-002 |
| D       | Materials, Processes and Inspection  | CM-D-001 … CM-D-002 |

Plus 5 LH₂-specific Special Conditions (SC-LH2-01 through SC-LH2-05).

### Affected Items

| Artifact                         | Current Location        | Proposed Location      |
|----------------------------------|-------------------------|------------------------|
| CS25_compliance_matrix.yaml      | KDB/DEV/trade-studies/  | KDB/LM/SSOT/ (copy)   |
| CS25_compliance_matrix.md        | KDB/DEV/trade-studies/  | KDB/LM/SSOT/ (copy)   |

The DEV copies remain as the working baseline; the SSOT copies become the
authoritative reference for downstream lifecycle phases (LC05–LC08).

## Rationale

The CS-25 compliance matrix has reached sufficient maturity for SSOT promotion:

1. **Complete requirement coverage** — 10 requirements spanning all 4 CS-25
   sections applicable to LH₂ primary tanks, plus 5 Special Conditions
   addressing hydrogen-specific gaps.
2. **Trade study traceability** — derives from TS-28-11-TS01 (architecture),
   TS-28-11-TS02 (materials), TS-28-11-TS03 (insulation/thermal).
3. **Evidence package defined** — 8 certification-ready evidence items
   identified with clear V&V methods (Analysis, Test, Inspection, Review).
4. **5D MTL integration** — all compliance subjects tokenised as MTK-28-11-CM-*
   tokens with process methods (MTP-*) and standard procedures (STP-*) tracing
   back to each requirement.
5. **Lifecycle readiness** — feeds LC03 (safety pack), LC05 (verification),
   LC06 (qualification), and LC08 (type certification).

## Safety Impact

- [x] Yes — requires STK_SAF review within 72 h

**Justification:** The compliance matrix governs certification of a cryogenic
hydrogen fuel tank, which is safety-critical (DAL A/B). Special Conditions
SC-LH2-01 through SC-LH2-05 directly address explosion prevention,
crashworthiness, and thermal shock — all of which have catastrophic failure
consequences.

## Affected Baselines

- [x] FBL-Q100-ATA28-001 — Functional Baseline (compliance requirements)
- [ ] DBL-Q100-ATA28-001 — Design Baseline (not yet established)
- [ ] PBL-Q100-ATA28-001 — Product Baseline (not yet established)

## Impact Assessment

### Technical Impact

- **Positive:** Establishes single authoritative compliance reference for all
  downstream engineering activities (structural analysis, test planning, ICA
  development).
- **Risk:** None — this is a promotion of an existing validated artifact, not a
  content change.

### Schedule Impact

- **None** — promotion can proceed immediately upon STK_SAF review.

### Cost Impact

- **None** — no new development required.

## Approval Status

| Role      | Decision  | Date       | Signature          |
|-----------|-----------|------------|--------------------|
| STK_ENG   | Approve   | 2026-02-16 | *(pending)*        |
| STK_SAF   | *(pending — 72 h review window)* | | |
| CCB Chair | *(pending)* | | |

## References

- `KDB/DEV/trade-studies/CS25_compliance_matrix.yaml` — source artifact
- `KDB/DEV/trade-studies/CS25_compliance_matrix.md` — companion documentation
- `KDB/LM/SSOT/SSOT_POLICY.md` — promotion rules
- `KDB/DEV/mtl/MTL-28-11-00_method_token_library.yaml` — MTK-28-11-CM-* tokens
- `KDB/DEV/mtl/STP-28-11-00_standard_procedures.yaml` — STP-28-11-004 (CS 25
  Compliance Assessment procedure)

## Revision History

| Rev | Date       | Author  | Description                |
|-----|------------|---------|----------------------------|
| 0.1 | 2026-02-16 | STK_ENG | Initial ECR creation       |
