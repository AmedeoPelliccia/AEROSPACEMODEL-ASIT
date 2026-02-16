# Meta Transformation Layers (MTL) — Core Standard v1.0.0

| Field              | Value                                                 |
|--------------------|-------------------------------------------------------|
| Standard ID        | `MTL-META-CORE`                                       |
| Version            | `1.0.0`                                               |
| Status             | DRAFT                                                 |
| Authority          | ASIT (Aircraft Systems Information Transponder)        |
| Alias (physical)   | Motion Transmission Lever                              |
| Parent BREX        | `ASIT-BREX-MASTER-001`                                |
| BREX Rule Set      | `MTL-META-BREX-001`                                   |

---

## 1. Purpose

**Meta Transformation Layers (MTL)** is a domain-agnostic architecture that
transforms operational knowledge into executable, verifiable, and trainable
tokens organized in five semantic layers.

It generalizes the existing *Method Token Library* (ATA 28-11, 5D token
architecture) into a reusable meta-framework applicable to **any** learnable
or tokenizable process — aerospace, robotics, MRO, certification, or AI
training pipelines.

---

## 2. Definition

> MTL = a system of semantic stratification that converts a process (human,
> digital, or physical) into five layers with full traceability, governance,
> and AI training capability over the same artifacts used in execution.

---

## 3. Layer Architecture

```
┌────────────────────────────────────────────────────────┐
│  L5  Domain Context Token       CTX-{DOMAIN}-{SYS}    │
│       What system/problem is being solved              │
├────────────────────────────────────────────────────────┤
│  L4  Structure Resolver Token   STR-{DOMAIN}-{SYS}-…  │
│       What component/sub-process applies               │
├────────────────────────────────────────────────────────┤
│  L3  Procedure Composer Token   PRC-{DOMAIN}-{SYS}-…  │
│       E2E flow of steps, hand-offs, and gates          │
├────────────────────────────────────────────────────────┤
│  L2  Transformation Method      XFM-{DOMAIN}-…-{CLASS} │
│       Formulas, rules, models, heuristics              │
├────────────────────────────────────────────────────────┤
│  L1  Subject / Evidence Token   SBJ-{DOMAIN}-…-{CLASS} │
│       Facts, criteria, constraints, evidences          │
└────────────────────────────────────────────────────────┘
```

---

## 4. Universal Token Patterns

| Layer | Pattern                                  | Example                   |
|-------|------------------------------------------|---------------------------|
| L5    | `CTX-{DOMAIN}-{SYS}`                    | `CTX-AERO-28`             |
| L4    | `STR-{DOMAIN}-{SYS}-{COMP}`             | `STR-ROB-LINE-ST04`       |
| L3    | `PRC-{DOMAIN}-{SYS}-{SEQ}`              | `PRC-AERO-28-001`         |
| L2    | `XFM-{DOMAIN}-{SYS}-{CLASS}-{SEQ}`      | `XFM-ROB-LINE-KIN-003`    |
| L1    | `SBJ-{DOMAIN}-{SYS}-{CLASS}-{SEQ}`      | `SBJ-MRO-ENG-SAFE-003`    |

---

## 5. Minimum Token Contract

Every token — regardless of domain — must include:

```yaml
token_id: "XFM-ROB-LINE-KIN-003"
layer: "L2"
name: "Inverse Kinematics Envelope Check"
intent: "Validate reachable pose set under joint limits"
method_class: "KIN"                        # L2 only
inputs:
  - { name: "target_pose", type: "pose6d", unit: "SI" }
  - { name: "joint_limits", type: "array[rad]" }
outputs:
  - { name: "is_reachable", type: "bool" }
  - { name: "min_margin_rad", type: "float" }
assumptions:
  - "Rigid links"
constraints:
  - "No self-collision"
acceptance_gates:
  - "is_reachable == true"
  - "min_margin_rad >= 0.05"
failure_modes:
  - "singularity_nearby"
  - "joint_limit_violation"
governance:
  owner_role: "STK_ENG"
  status: "DEV"
  version: "0.1.0"
trace:
  derives_from: ["REQ-ROB-LINE-INT-007"]
  feeds: ["PRC-ROB-LINE-012"]
```

---

## 6. Method Class Taxonomy (L2)

| Code   | Name                        |
|--------|-----------------------------|
| `GEOM` | Geometry / Spatial          |
| `KIN`  | Kinematics                  |
| `DYN`  | Dynamics                    |
| `THRM` | Thermal                     |
| `MATL` | Materials                   |
| `CTRL` | Control                     |
| `QUAL` | Quality / Metrology         |
| `SAFE` | Safety                      |
| `CERT` | Certification               |
| `EVAL` | Evaluation / Optimization   |
| `OPS`  | Operations                  |
| `MRO`  | Maintenance / Repair        |

---

## 7. Domain Profiles

| Profile | Name                               | Notes                                 |
|---------|------------------------------------|---------------------------------------|
| `AERO`  | Aerospace (ATA-aligned)            | Existing ATA 28-11 5D implementation  |
| `ROB`   | Robotics / Motion Transmission Lever | Kinematics, actuators, mechatronic MRO |
| `MRO`   | Maintenance, Repair, Overhaul      | Cross-domain maintenance ops          |
| `CERT`  | Certification / Compliance         | Regulatory workflows                  |
| `PAL`   | Program Assembly Line              | Software & integration governance     |

`Motion Transmission Lever ⊂ Meta Transformation Layers`

---

## 8. Canonical Learning Rule

> **The model learns on the same tokens it later consumes in execution.**

Benefits:

* Zero semantic drift between training and deployment
* Deterministic replay by `token_id` + `version`
* Complete decision traceability
* Automatic evidence for audit and certification

---

## 9. Governance Policies

| ID        | Policy                              | Enforcement |
|-----------|-------------------------------------|-------------|
| `GOV-001` | Hard version lock                   | Block       |
| `GOV-002` | Deny by default for autonomy        | Block       |
| `GOV-003` | No silent gate override (safety)    | Escalate    |
| `GOV-004` | Labor continuity constraint         | Escalate    |

---

## 10. Invariants

| ID        | Property                     |
|-----------|------------------------------|
| `INV-001` | Deterministic replay         |
| `INV-002` | Full traceability            |
| `INV-003` | Machine-evaluable gates      |
| `INV-004` | Model-token version lock     |

---

## 11. ATA 28-11 Backward Compatibility

| MTL Layer | ATA 28-11 Equivalent          |
|-----------|-------------------------------|
| L5        | D5 / `SDR-{ATA}`             |
| L4        | D4 / `SCR-{ATA}-{SS}`        |
| L3        | D3 / `STP-{ATA}-{SS}-{SEQ}`  |
| L2        | D2 / `MTP-{ATA}-{SS}-{DOM}`  |
| L1        | D1 / `MTK-{ATA}-{SS}-{DOM}`  |

---

## 12. Files in This Directory

| File                               | Description                                  |
|------------------------------------|----------------------------------------------|
| `MTL_META_STANDARD_v1.0.0.yaml`   | Machine-readable standard definition (SSOT)  |
| `MTL_META_BREX.yaml`              | BREX-like governance rule set                |
| `README.md`                        | This document (human-readable overview)      |

---

## 13. Related Documents

| Document                    | Reference                                           |
|-----------------------------|-----------------------------------------------------|
| ASIT Core Specification     | `ASIT/ASIT_CORE.md`                                |
| Master BREX Authority       | `ASIT/GOVERNANCE/master_brex_authority.yaml`        |
| ATA 28-11 MTL (5D)         | `KDB/DEV/mtl/` in ATA 28-11-00                     |
| Contract Schema             | `ASIT/CONTRACTS/CONTRACT_SCHEMA.yaml`               |

---

## 14. Decision State Machine

All policy and gate evaluations SHALL resolve to one deterministic state:

| State      | Meaning                                               |
|------------|-------------------------------------------------------|
| `ALLOW`    | All required gates pass                               |
| `HOLD`     | Gate boundary uncertain — needs more data or review   |
| `REJECT`   | Blocking policy condition failed                      |
| `ESCALATE` | Escalation-class policy condition failed              |

No safety-relevant flow may transition directly to `ALLOW` after a failed
mandatory gate.

---

## 15. Layer-Specific Contract Enforcement

The minimum token contract is split into:

* **Core fields** (mandatory for L1–L5): `token_id`, `layer`, `name`, `intent`,
  `inputs`, `outputs`, `assumptions`, `constraints`, `acceptance_gates`,
  `governance`, `trace`
* **Layer-specific fields** (mandatory only for the indicated layer):
  * L5: `domain_scope`, `regulatory_basis`
  * L4: `resolver_rules`, `target_components`
  * L3: `procedure_steps`, `handoffs`, `terminal_outputs`
  * L2: `method_class`, `equation_or_rule`, `validity_range`
  * L1: `evidence_type`, `source_artifacts`, `confidence`

This avoids schema ambiguity and guarantees deterministic BREX validation.

---

## 16. Backward Mapping Rules

Legacy ATA 28-11 token IDs can be transformed to universal MTL IDs using
regex-based rules:

| Legacy Pattern | Universal Pattern   | Example                    |
|----------------|---------------------|----------------------------|
| `SDR-{ATA}`    | `CTX-AERO-{ATA}`   | `SDR-28` → `CTX-AERO-28`  |
| `SCR-{ATA}-{SS}` | `STR-AERO-{ATA}-{SS}` | `SCR-28-11` → `STR-AERO-28-11` |
| `STP-{ATA}-{SS}-{SEQ}` | `PRC-AERO-{ATA}{SS}-{SEQ}` | `STP-28-11-001` → `PRC-AERO-2811-001` |
| `MTP-{ATA}-{SS}-{DOM}-{SEQ}` | `XFM-AERO-{ATA}{SS}-{DOM}-{SEQ}` | `MTP-28-11-GEOM-001` → `XFM-AERO-2811-GEOM-001` |
| `MTK-{ATA}-{SS}-{DOM}-{SEQ}` | `SBJ-AERO-{ATA}{SS}-{DOM}-{SEQ}` | `MTK-28-11-TS-001` → `SBJ-AERO-2811-TS-001` |

---

*End of MTL Meta Standard v1.0.0 README*
