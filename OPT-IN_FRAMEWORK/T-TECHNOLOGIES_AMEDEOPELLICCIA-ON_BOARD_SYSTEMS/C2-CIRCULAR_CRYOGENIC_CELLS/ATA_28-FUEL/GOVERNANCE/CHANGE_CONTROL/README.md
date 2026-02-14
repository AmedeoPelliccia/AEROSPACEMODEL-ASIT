# ATA 28 – Change Control Process

**System:** AMPEL360 Q100 LH₂ Fuel System (C2 Circular Cryogenic Cells)
**ATA Chapter:** 28 – Fuel
**Version:** 1.0.0

## Process Overview

All changes to baselined ATA 28 artifacts follow this workflow:

1. **ECR Submission** – Requestor submits an Engineering Change Request.
2. **Impact Assessment** – STK_ENG evaluates technical, schedule, and cost impact.
3. **CCB Review** – Configuration Control Board reviews and dispositions.
4. **ECO Issuance** – Approved changes are formalized as an Engineering Change Order.
5. **Implementation** – Changes are implemented per the ECO instructions.
6. **Verification** – Changes are verified and baselines updated.

## Hydrogen Safety Changes

Changes affecting H₂ safety require **STK_SAF review within 72 hours**
of ECR submission. The CCB shall not disposition safety-related ECRs
without STK_SAF concurrence.

## Templates

- [ECR Template](ECR_TEMPLATE.md)
- [ECO Template](ECO_TEMPLATE.md)

## Registers

- [ECR Register](ECR/ECR_REGISTER.csv)
- [ECO Register](ECO/ECO_REGISTER.csv)

## Sub-directories

| Directory       | Purpose                     |
|-----------------|-----------------------------|
| `ECR/`          | ECR register and records    |
| `ECO/`          | ECO register and records    |
| `CCB_MINUTES/`  | CCB meeting minutes         |
