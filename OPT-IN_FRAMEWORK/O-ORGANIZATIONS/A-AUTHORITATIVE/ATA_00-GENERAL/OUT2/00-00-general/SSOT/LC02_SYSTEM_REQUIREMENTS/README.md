# SSOT / LC02_SYSTEM_REQUIREMENTS — Functional Baseline (FBL)

LC02 is the authoritative phase for **system requirements** and **interface control intent** in the GenKISS canonical lifecycle.  
This phase is the **exclusive producer** of the **Functional Baseline (FBL)**.

---

## 1) Phase Identity

| Field | Value |
|---|---|
| LC ID | LC02 |
| Canonical Name | System Requirements |
| Phase Type | PLM |
| Baseline Produced | **FBL** (Functional Baseline) |
| Authority | Systems Engineering (with Configuration Control) |

---

## 2) Mission

Define, structure, and govern system-level requirements so downstream phases can execute deterministically:

- LC03 Safety & Reliability traces to LC02 requirements
- LC04 Design Definition realizes LC02 requirements
- LC06 Verification confirms requirement satisfaction
- LC08 Certification uses LC02-linked evidence chain

LC02 is where requirement ambiguity is converted into configuration-controlled intent.

---

## 3) Scope

### In Scope
- System requirements authoring and control
- External/internal interface requirements (ICD intent)
- Requirement attributes (verification method, rationale, criticality, effectivity)
- Trace seed creation for safety, design, and test
- FBL release package assembly

### Out of Scope
- Detailed design solutions (LC04)
- Execution test evidence (LC06)
- Certification issuance actions (LC08)
- Production release authority (LC10)

---

## 4) Canonical Outputs

- Requirement specifications (`REQ`)
- Interface control definitions (`ICD`)
- Compliance intent mapping (pre-cert trace intent)
- FBL package under configuration control
- Downstream trace links:
  - `LC02 REQ → LC03 SAFETY`
  - `LC02 REQ → LC04 DESIGN`
  - `LC04 DESIGN → LC06 TEST` (continued chain)
  - `LC06 TEST → LC08 COMPLIANCE`

---

## 5) Entry and Exit Criteria

### Entry
- Program/problem framing approved (LC01 complete/accepted inputs)
- Stakeholder requirement capture completed
- Governance and AoR assignment active

### Exit
- All system requirements captured and baselined
- FBL package released and configuration controlled
- Downstream trace links established
- CCB approval obtained

---

## 6) Governance Rules

- Requirements must be uniquely identified (REQ-XXXX)
- All requirements must include verification method
- Changes require ECR/ECO and CCB approval
- FBL snapshots are immutable once released

---

**GenKISS**: General Knowledge and Information Standard Systems
