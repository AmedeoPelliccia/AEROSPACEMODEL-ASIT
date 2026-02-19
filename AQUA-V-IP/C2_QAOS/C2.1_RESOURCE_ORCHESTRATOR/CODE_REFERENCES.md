# Code References — C2.1 Criticality-Aware Quantum Resource Orchestrator

**Docket:** AQUA-V-C2.1-2026-001  
**Date:** 2026-02-19

---

## Primary Implementation References

### 1. GAIA-AIR — QAOS.py (Direct Reduction to Practice)

**Repository:** `AmedeoPelliccia/GAIA-AIR`

| File | URL | Key Classes / Functions | Relevance to C2.1 Claims |
|---|---|---|---|
| `QAOS.py` | `https://github.com/AmedeoPelliccia/GAIA-AIR/blob/main/QAOS.py` | `WorkloadClass` enum; `QuantumResource`; `QuantumWorkload`; orchestrator logic | Direct implementation of QW1–QW4 classification (Claim 4); backend scoring (Claim 7); fallback logic (Claim 6) |
| `qaos_master_ui/qaos_master_ui.py` | `https://github.com/AmedeoPelliccia/GAIA-AIR/blob/main/qaos_master_ui/qaos_master_ui.py` | Master UI; workload status display; human oversight dashboard | Human oversight hook (Claim 9); demonstrates operational deployment |
| `QAOS-Technical-documentation.md` | `https://github.com/AmedeoPelliccia/GAIA-AIR/blob/main/QAOS-Technical-documentation.md` | Full architecture documentation; QW1–QW4 definitions; backend selection rationale | Complete technical context for all claims |

**Key QAOS.py structures (excerpt mapping):**

```python
# WorkloadClass — maps to claim 4 (QW1–QW4 classification)
class WorkloadClass(Enum):
    QW1 = "safety_critical"   # ≤5 ms; claim 4, 5, 12
    QW2 = "mission_critical"  # ≤100 ms; claim 4
    QW3 = "operational"       # ≤1,000 ms; claim 4
    QW4 = "background"        # best-effort; claim 4

# QuantumResource — maps to claim 1(b) backend metrics
@dataclass
class QuantumResource:
    resource_id: str
    backend_type: str          # "gate_qpu", "annealer", "simulator", "classical"
    available: bool
    queue_depth: int           # claim 1(b) queue depth
    p50_latency_ms: float      # claim 10 latency measurement
    gate_error_rate: float     # claim 1(b) noise metric
    max_qubits: int

# QuantumWorkload — maps to claim 1(a) workload descriptor
@dataclass
class QuantumWorkload:
    workload_id: str
    workload_class: WorkloadClass  # claim 1(a) safety criticality indicator
    circuit: Any
    deadline_ms: Optional[float]   # claim 1(a) response deadline
    circuit_depth: int             # claim 7 composite score input
```

---

### 2. AEROSPACEMODEL — Governance Framework

**Repository:** `AmedeoPelliccia/AEROSPACEMODEL` (this repository)

| File | Relevance to C2.1 |
|---|---|
| `ASIT/GOVERNANCE/master_brex_authority.yaml` | SAFETY-002 BREX rule that triggers STK_SAF escalation — maps to human oversight hook (Claim 9) |
| `lifecycle/T_SUBDOMAIN_LC_ACTIVATION.yaml` | QW1 workloads for T/P (Propulsion) and T/C2 (Cryogenic) subdomains require DAL-A evidence — claim 8 evidence record DAL indicator |

---

### 3. EU AI Act Alignment (Regulatory Reference)

The human oversight hook in Claim 9 implements EU AI Act Article 14 (Human Oversight) for high-risk AI systems. Relevant reference:

- EU Regulation 2024/1689 (EU AI Act), Article 14: "High-risk AI systems shall be designed and developed in such a way ... that they can be effectively overseen by natural persons during the period in which the AI system is in use."
- AQUA-V QW1 orchestrator with human approval gate = technical implementation of Art. 14 for quantum AI in safety-critical aerospace operations

---

*EU framework note: QAOS.py is maintained in a GitHub repository (public cloud). For production deployment, the QAOS orchestrator must run on an EU-hosted infrastructure node compliant with GAIA-X data sovereignty requirements.*
