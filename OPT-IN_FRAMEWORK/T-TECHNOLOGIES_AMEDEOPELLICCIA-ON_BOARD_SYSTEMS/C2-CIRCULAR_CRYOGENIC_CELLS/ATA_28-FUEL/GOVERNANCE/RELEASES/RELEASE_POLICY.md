# ATA 28 – Release Policy

**System:** AMPEL360 Q100 LH₂ Fuel System (C2 Circular Cryogenic Cells)
**ATA Chapter:** 28 – Fuel
**Version:** 1.0.0

## Versioning

Releases follow Semantic Versioning (semver) `X.Y.Z`:

- **X (Major):** Baseline-breaking changes (new FBL, DBL, or PBL).
- **Y (Minor):** Backwards-compatible additions (new data modules, analyses).
- **Z (Patch):** Corrections and editorial updates.

## Release Criteria

A release may be issued only when **all** of the following are satisfied:

1. All applicable lifecycle gates have been passed.
2. BREX compliance validated — no unresolved violations.
3. Requirement traces are complete (100% coverage).
4. All open safety KNOTs are dispositioned.
5. CCB approval recorded.

## Rollback Rules

- Rollback of a released version requires **CCB approval**.
- The rollback ECR must reference the original release and affected baselines.
- Rolled-back content reverts to the prior baselined configuration.

## Register

See [RELEASE_REGISTER.csv](RELEASE_REGISTER.csv) for the current release history.
