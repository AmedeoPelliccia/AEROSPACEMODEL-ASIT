# Invention Disclosure — C2.1 Criticality-Aware Quantum Resource Orchestrator

**Title:** Criticality-Aware Quantum Resource Orchestrator with Latency-Bounded Backend Selection and Controlled Degradation  
**Docket:** AQUA-V-C2.1-2026-001  
**Parent Docket:** AQUA-V-P0-2026-001  
**Date:** 2026-02-19  
**Priority:** ★ HIGH PRIORITY — backed by existing QAOS.py implementation

---

## 1. Inventors

| Name | Role | Contribution |
|---|---|---|
| **Amedeo Pelliccia** | Primary Inventor | QAOS architecture; QW1–QW4 workload classification; latency-bounded scheduling; fallback mechanism design |

---

## 2. Technical Problem

As quantum computing services become available for aerospace operational tasks, a critical problem emerges: **how to safely multiplex safety-critical, mission-critical, operational, and background quantum workloads across heterogeneous quantum/classical backends**, while guaranteeing that safety-critical workloads are served within hard deadline constraints and that system failure modes are controlled.

Specific technical challenges:
1. **Deadline heterogeneity**: Real-time flight envelope monitoring requires ≤5 ms response; supply chain optimisation can tolerate ≥1 s — these cannot share a backend queue without priority management
2. **Backend heterogeneity**: Different QPU platforms (gate-based, annealing), simulators, and classical solvers have different latency, noise, and queue characteristics
3. **Graceful degradation**: When quantum backends are unavailable, safety-critical functions must fall back to classical equivalents without service interruption
4. **Controlled non-determinism for safety**: QW1 workloads require deterministic evidence records (C1.2) even under fallback conditions

No existing quantum cloud scheduler (IBM Qiskit Runtime, AWS Braket Hybrid Jobs, Azure Quantum) provides criticality-aware scheduling with hard deadline enforcement and controlled degradation.

---

## 3. Description of the Invention

### 3.1 Workload Classification (QW1–QW4)

Operational quantum workloads are classified into four classes based on safety criticality and response deadline:

```python
class WorkloadClass(Enum):
    QW1 = "safety_critical"    # ≤5 ms deadline; DAL A/B; requires DER
    QW2 = "mission_critical"   # ≤100 ms deadline; mission impact if missed
    QW3 = "operational"        # ≤1,000 ms deadline; operational degradation if missed
    QW4 = "background"         # Best-effort; no hard deadline
```

Classification is determined at workload submission time based on:
- The safety assessment reference (ARP4761 function hazard category)
- The operational context (flight phase, system state)
- The requesting subsystem's DAL level

### 3.2 Backend Scoring and Selection

For each submitted workload, the orchestrator scores available backends using a multi-objective function:

```python
def score_backend(
    backend: QuantumResource,
    workload: QuantumWorkload
) -> float:
    """
    Composite score: lower is better.
    Components:
      - latency_score: measured p50 execution latency normalised to deadline
      - noise_score: gate error rate × circuit depth (proxy for result quality)
      - queue_score: current queue depth × estimated time-per-job
      - availability_score: 0 if backend is unavailable, 1 otherwise
    """
    latency_score = backend.p50_latency_ms / workload.deadline_ms
    noise_score = backend.gate_error_rate * workload.circuit_depth
    queue_score = backend.queue_depth * backend.avg_job_duration_ms / workload.deadline_ms
    
    if not backend.available or latency_score > 1.0:
        return float('inf')  # Backend cannot meet deadline
    
    return latency_score + 0.3 * noise_score + 0.2 * queue_score
```

### 3.3 Hard Deadline Enforcement for QW1

For QW1 workloads, the orchestrator enforces the 5 ms deadline:
- Preemptively selects a classical fallback backend before submitting to QPU
- If QPU result is not received within deadline window, classical fallback is activated
- The fallback event is recorded in the DER (per C1.2) as a controlled degradation event

### 3.4 Automatic Fallback and Controlled Degradation

The degradation chain:
```
QW1: QPU (best QPU) → QPU (alternate QPU) → Classical (pre-validated) → Alert + Safe Hold
QW2: QPU (optimal) → Classical (optimal) → Classical (fallback) → Alert
QW3: QPU (any available) → Classical (any) → Queue (with timeout)
QW4: QPU (idle) → Classical (idle) → Queue (no timeout)
```

### 3.5 Human Oversight Hooks

For QW1 workloads in flight-critical contexts, the orchestrator invokes a human oversight hook before promoting results to operational digital twin state. This satisfies EU AI Act Article 14 of Regulation (EU) 2024/1689 (human oversight of high-risk AI systems).

---

## 4. Advantages Over Prior Art

| Prior Art | C2.1 Advantage |
|---|---|
| IBM Qiskit Runtime job scheduler | No safety criticality classes; no deadline enforcement; no classical fallback chain |
| AWS Braket Hybrid Jobs | Hybrid classical-quantum but no criticality classification; no 5 ms SLA |
| Classical real-time schedulers (ARINC 653) | No quantum backend integration; no noise-aware backend selection |
| Generic cloud load balancers | No quantum circuit awareness; no noise/latency/queue multi-objective scoring |

---

## 5. Embodiment

**Primary:** Aerospace operational QAOS deployment where QW1 handles real-time structural health monitoring triggers, QW2 handles route optimisation, QW3 handles maintenance scheduling, and QW4 handles background fleet analytics.

**Implementation evidence:** See `AmedeoPelliccia/GAIA-AIR` — `QAOS.py` for existing Python implementation.

---

*Confidential — ★ HIGH PRIORITY EP filing target: 2026-03-05 at EPO (Munich, EU).*
