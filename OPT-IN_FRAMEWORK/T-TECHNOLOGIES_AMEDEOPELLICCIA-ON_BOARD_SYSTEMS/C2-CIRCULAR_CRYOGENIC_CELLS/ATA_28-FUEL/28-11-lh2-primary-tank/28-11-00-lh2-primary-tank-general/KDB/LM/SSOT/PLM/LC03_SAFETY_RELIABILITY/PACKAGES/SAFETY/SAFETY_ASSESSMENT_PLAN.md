# Safety Assessment Plan — ATA 28-11-00 LH₂ Primary Tank

| Key | Value |
|-----|-------|
| Document ID | SAP-28-11-00-001 |
| ATA Code    | 28-11-00 |
| Programme   | AMPEL360 Q100 |
| Phase       | LC03 — Safety & Reliability |
| Status      | DEV (pending STK_SAF review) |
| Date        | 2026-02-16 |

---

## 1. Methodology

Safety assessment follows **ARP4761** for hydrogen cryogenic systems:

1. **FHA** — Functional Hazard Assessment at aircraft and system level  
2. **PSSA** — Preliminary System Safety Assessment during design (LC04)  
3. **SSA** — System Safety Assessment during verification (LC05)  

All assessments require **STK_SAF** review and approval.
Safety content generation requires escalation per **SAFETY-H2-001**.

---

## 2. Hydrogen-Specific Hazards (from Trade Studies)

### 2.1 Catastrophic (< 1E-9/FH)

| ID            | Hazard                                   | Source                            |
|---------------|-------------------------------------------|-----------------------------------|
| SAF-28-11-001 | LH₂ tank structural failure / leak        | CM-A-001..004, TS-28-11-TS01/02    |
| SAF-28-11-002 | H₂ ignition / explosion in tank bay | CM-C-001, SC-LH2-02              |
| SAF-28-11-006 | Crashworthiness failure (non-integral tank) | SC-LH2-05                   |

### 2.2 Hazardous (< 1E-7/FH)

| ID            | Hazard                                        | Source                         |
|---------------|------------------------------------------------|--------------------------------|
| SAF-28-11-003 | Excessive boil-off → fuel exhaustion   | CM-B-001..002, TS-28-11-TS03     |
| SAF-28-11-004 | Pressure relief valve failure          | CM-B-002, SC-LH2-01             |
| SAF-28-11-007 | Cryogenic thermal shock (structure/interface) | SC-LH2-03, TS-28-11-TS02         |
| SAF-28-11-008 | Hydrogen embrittlement (Al-Li weld zones) | CM-A-004, TS-28-11-TS02, RISK-03 |

### 2.3 Major (< 1E-5/FH)

| ID            | Hazard                                    | Source                       |
|---------------|--------------------------------------------|------------------------------|
| SAF-28-11-005 | Vacuum loss → MLI insulation degradation | TS-28-11-TS03, SC-LH2-04, RISK-01 |

---

## 3. Trade Study Safety Findings Summary

### TS-28-11-TS01 (Tank Architecture)
- **Selected:** Cylindrical hemispherical (Option B)
- **Safety implication:** Uniform stress distribution, mature certification precedent
- **Open risk:** SC timeline for LH₂-specific certification (RISK-05)

### TS-28-11-TS02 (Materials)
- **Selected:** Al-Li 2195 (Option A)
- **Safety implication:** Cryogenic-compatible, but embrittlement risk at weld zones under cyclic loading (20 K)
- **Open risk:** Cryogenic fatigue in Al-Li weld zones (RISK-03)
- **Required evidence:** Material allowables at 20 K, weld qualification, crack growth assumptions

### TS-28-11-TS03 (Insulation & Thermal)
- **Selected:** Vacuum + MLI (Option A)
- **Safety implication:** Vacuum sensitivity — slight loss erodes MLI advantage
- **Open risks:** Vacuum integrity degradation (RISK-01), support-pad heat leak dominance (RISK-02)
- **Required vacuum:** 0.0133–0.266 Pa; degraded threshold ~1.33 Pa

---

## 4. Compliance Mapping (CS-25 + Special Conditions)

| Domain | Req IDs | Severity | MoC |
|--------|---------|----------|-----|
| Structural integrity | CM-A-001..004 | Very High | Analysis + Test |
| Pressure/venting | CM-B-001..002 | High–Very High | Analysis + Test |
| Fire/explosion prevention | CM-C-001..002 | Critical | Analysis + Inspection |
| Materials/processes | CM-D-001..002 | High–Very High | Analysis + Test |
| Boil-off management | SC-LH2-01 | Special Condition | Analysis + Test |
| H₂ detection | SC-LH2-02 | Special Condition | Analysis + Test + Inspection |
| Cryogenic thermal shock | SC-LH2-03 | Special Condition | Analysis + Test |
| Vacuum integrity | SC-LH2-04 | Special Condition | Analysis + Inspection |
| Crashworthiness | SC-LH2-05 | Special Condition | Analysis + Test |

---

## 5. Minimum Evidence Package (Certification-Ready)

| # | Artifact | Status |
|---|----------|--------|
| 1 | FHA_PSSA_SSA_ATA28-11_LH2.pdf | To be developed |
| 2 | Zonal Hazard Analysis (tank bay) | To be developed |
| 3 | Fault trees + FMEA | To be developed |
| 4 | DAL/IDAL allocation matrix | To be developed |
| 5 | CDCCLs and limitations | To be developed |
| 6 | Ignition source control analysis | To be developed |

---

## 6. Traceability

Hazards trace to requirements (LC02) and mitigations (LC04).
All safety content inherits governance from **GOV-LC01-ATA28-11**.

---

## 7. Approval

| Role | Action | Status |
|------|--------|--------|
| STK_SAF | Review + Approve | Pending |
| CCB | Baseline (FBL) | Pending |
