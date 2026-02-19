# Code References — C1.2 Deterministic Reproducibility Pipelines

**Docket:** AQUA-V-C1.2-2026-001  
**Date:** 2026-02-19

---

## Supporting Implementation References

### 1. GAIA-AIR — QAOS.py (Primary Evidence of Reduction to Practice)

**Repository:** `AmedeoPelliccia/GAIA-AIR`

| File | URL | Relevance to C1.2 |
|---|---|---|
| `QAOS.py` | `https://github.com/AmedeoPelliccia/GAIA-AIR/blob/main/QAOS.py` | `WorkloadClass` enum defines QW1–QW4 criticality classes; `QuantumWorkload` and `QuantumResource` dataclasses define the workload–backend binding that the DER must reference; solver version and backend ID fields map directly to C1.2 claim elements |
| `qaos_master_ui/qaos_master_ui.py` | `https://github.com/AmedeoPelliccia/GAIA-AIR/blob/main/qaos_master_ui/qaos_master_ui.py` | Master UI showing workload lifecycle and evidence record status; demonstrates the human oversight hook for QW1 computations requiring DER before promotion |
| `QAOS-Technical-documentation.md` | `https://github.com/AmedeoPelliccia/GAIA-AIR/blob/main/QAOS-Technical-documentation.md` | Full technical documentation; Section on reproducibility describes the seed derivation and evidence record concept |

**Key classes directly supporting C1.2 claims:**

```python
# From QAOS.py — WorkloadClass enum (maps to QW1–QW4 criticality in claim 11)
class WorkloadClass(Enum):
    QW1 = "safety_critical"      # Requires DER with DAL-A indicator
    QW2 = "mission_critical"     # Requires DER with DAL-B indicator
    QW3 = "operational"          # Standard DER
    QW4 = "background"           # Lightweight DER

# From QAOS.py — QuantumWorkload (solver_version field → claim 1(b))
@dataclass
class QuantumWorkload:
    workload_id: str
    workload_class: WorkloadClass
    circuit: Any                 # The quantum circuit to execute
    deadline_ms: Optional[float] # Deadline enforcement (QW1 = 5ms)
    # ... solver_version would be added as part of DER generation
```

---

### 2. AEROSPACEMODEL — Lifecycle Framework (Lifecycle Phase Binding)

**Repository:** `AmedeoPelliccia/AEROSPACEMODEL` (this repository)

| File | Relevance to C1.2 |
|---|---|
| `lifecycle/T_SUBDOMAIN_LC_ACTIVATION.yaml` | Defines LC03–LC08 phases for novel technology subdomains; C1.2 DER `lc_phase` field references these identifiers |
| `schemas/ampel360_artifact_types.yaml` | 63 controlled artefact types across 14 LC phases; DER is a new artefact type in this schema |
| `src/aerospacemodel/ampel360/identifiers.py` | Canonical identifier grammar for AMPEL360 artefacts; DER `record_id` follows this grammar |

---

### 3. A-Q-U-A_V — System Requirements (Evidence Record Requirements)

**Repository:** `AmedeoPelliccia/A-Q-U-A_V`

| File | Relevance to C1.2 |
|---|---|
| SyRS v1.0 — Section on QAPD reproducibility | Specifies the requirement that all QAPD computations be reproducible and traceable; C1.2 is the technical realisation of this requirement |
| PRD v6.0 — Evidence record specification | Defines the fields required in a quantum computation evidence record; aligns with the DER dataclass in C1.2 |

---

## Mapping: Claim Elements → Code

| Claim Element | Code Reference | File |
|---|---|---|
| "global seed from cryptographic hash of input data" | `generate_global_seed()` function concept | QAOS.py + AEROSPACEMODEL pipeline |
| "solver version identifier" | `QuantumWorkload.circuit` + backend metadata | QAOS.py |
| "executing with global seed" | `WorkloadClass` + deadline enforcement | QAOS.py |
| "cryptographic evidence record" | `DeterministicEvidenceRecord` dataclass | C1.2 invention (reduce to practice pending) |
| "digital signature with HSM" | eIDAS-qualified signing in EU regulatory context | AEROSPACEMODEL governance framework |
| "lifecycle phase identifier LC03–LC08" | `T_SUBDOMAIN_LC_ACTIVATION.yaml` | AEROSPACEMODEL lifecycle/ |

---

*All referenced repositories are public GitHub repositories maintained by AmedeoPelliccia.*  
*EU framework note: primary evidence record storage registry must be an EU-hosted system (GAIA-X sovereign cloud node or EPO register).*
