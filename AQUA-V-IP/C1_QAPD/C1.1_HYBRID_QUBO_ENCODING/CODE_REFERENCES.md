# Code References — C1.1 Hybrid QUBO Encoding

**Docket:** AQUA-V-C1.1-2026-001  
**Date:** 2026-02-19

---

## Supporting Implementation References

The following external code references provide evidentiary support for the C1.1 invention disclosure and claims. These references demonstrate reduction to practice of the hybrid QUBO encoding concept within the AQUA-V ecosystem.

---

### 1. AMPEL360-BWB-Q — CQEA Framework and Ontology

**Repository:** `AmedeoPelliccia/AMPEL360-BWB-Q`

| File / Artefact | Relevance |
|---|---|
| `ontology.jsonld` | Defines the aerospace constraint ontology including ATA chapter references, DAL levels, and material compatibility classes — maps directly to the constraint schema used in C1.1 QUBO penalty terms |
| CQEA framework documentation | Describes the Constraint-Qualified Engineering Analysis framework that provides the physical basis for penalty coefficient scaling |
| Structural parametrics module | Provides continuous design parameter ranges (panel thickness, bay dimensions) encoded as binary registers in C1.1 |

---

### 2. AEROSPACEMODEL — ASIT Constraint Schemas

**Repository:** `AmedeoPelliccia/AEROSPACEMODEL` (this repository)

| File / Artefact | Relevance |
|---|---|
| `schemas/ampel360_metadata_record.schema.json` | Defines the metadata schema for aerospace artefacts including ATA chapter, DAL level, and regulatory reference fields — used as the constraint schema backbone |
| `lifecycle/T_SUBDOMAIN_LC_ACTIVATION.yaml` | Specifies DAL requirements per technology subdomain (T/C2 = Cryogenic, T/P = Propulsion) — source of DAL failure probability bounds encoded as QUBO penalty terms |
| `OPT-IN_FRAMEWORK/T-TECHNOLOGIES.../ATA_28-FUEL/` | Cryogenic fuel system constraints (LH₂ at −253°C; material compatibility) — directly encoded as cryogenic penalty terms in C1.1 QUBO formulation |

---

### 3. A-Q-U-A_V — System Requirements Specification

**Repository:** `AmedeoPelliccia/A-Q-U-A_V`

| File / Artefact | Relevance |
|---|---|
| SyRS v1.0 | System requirements for the AQUA-V architecture; Section on QAPD encoding specifies the variable types and constraint categories addressed in C1.1 |
| PRD v6.0 | Product Requirements Document; specifies precision requirements for continuous design parameters encoded as binary registers |

---

## Key Constraint Types Traceable to Repository Artefacts

| Constraint Type | Source in Repository | QUBO Penalty Term |
|---|---|---|
| Cryogenic thermal (−253°C) | `ATA_28-FUEL` directory; `T_SUBDOMAIN_LC_ACTIVATION.yaml` T/C2 | `lambda_cryo × Σ material_selection × thermal_incompatibility` |
| Material compatibility (H₂) | `ATA_28-FUEL` SAFETY-H2-002 constraint | `lambda_mat × Σ incompatible_material × h2_exposure` |
| DAL failure probability bounds | `T_SUBDOMAIN_LC_ACTIVATION.yaml` T/P DAL-A | `lambda_dal × max(0, P_fail − P_dal_req)²` |
| Geometric packaging (CG) | `AMPEL360-BWB-Q` structural parametrics | `lambda_geom × max(0, CG_dev − CG_tol)²` |

---

*These references support the reduction-to-practice requirement for patent prosecution.*  
*All repositories are maintained under ASIT governance (AmedeoPelliccia organisation).*
