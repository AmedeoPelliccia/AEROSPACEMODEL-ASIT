# Prior Art Matrix — C2.1 Criticality-Aware Quantum Resource Orchestrator

**Docket:** AQUA-V-C2.1-2026-001  
**Date:** 2026-02-19

---

| Reference | Date | What It Covers | What It Does NOT Cover (AQUA-V Gap) | Risk Level |
|---|---|---|---|---|
| **IBM Qiskit Runtime** ([IBM Quantum](https://docs.quantum.ibm.com/api/qiskit-ibm-runtime)) | 2021–2025 | Hybrid quantum-classical job primitives; session management; error mitigation; job priority tiers | Safety criticality classification (QW1–QW4); 5 ms hard deadline enforcement; pre-validated classical fallback; safety hold on deadline miss; cryptographic evidence log | Medium |
| **AWS Braket Hybrid Jobs** ([AWS](https://docs.aws.amazon.com/braket/latest/developerguide/braket-jobs.html)) | 2022–2025 | Hybrid classical-quantum job management; multi-backend support; job priority; timeout settings | Safety criticality classes; 5 ms deadline for safety-critical; multi-objective noise+latency+queue scoring; aerospace operational integration; evidence log | Medium |
| **Azure Quantum job management** ([Microsoft](https://learn.microsoft.com/en-us/azure/quantum/)) | 2022–2025 | Job submission; backend selection; target configuration; hybrid workflows | Safety criticality; hard deadline enforcement for safety-critical workloads; fallback chain; evidence records for regulatory compliance | Medium |
| **ARINC 653 — Avionics Application Software Standard Interface** | 2006/2015 | Partitioned real-time OS for avionics; time partitioning; spatial partitioning; health monitoring | Quantum backend integration; noise-aware backend selection; quantum workload scheduling | Low |
| **ARINC 664 (AFDX)** | 2002 | Avionics network resource partitioning; end-system bandwidth allocation; virtual links | Quantum circuit scheduling; QPU backend selection; noise metrics | Low |
| **Real-time task scheduling literature** (Liu & Layland 1973; Buttazzo 2011) | 1973–2011 | Rate Monotonic Scheduling; Earliest Deadline First; real-time guarantees; preemption | Quantum circuit execution; noise-aware selection; quantum/classical hybrid scheduling | Low |
| **Digital twins in aerospace** ([Nature 2024](https://www.nature.com/articles/s43588-024-00613-8)) | 2024 | Digital twin operational updates; real-time synchronisation; sensor data integration | Quantum workload orchestration; safety criticality classification; fallback mechanisms | Low |
| **EuroQuIC quantum patent landscape** ([EuroQuIC 2025](https://www.euroquic.org/wp-content/uploads/2025/02/A-Portrait-of-The-Global-Patent-Landscape-in-Quantum-Technologies-2025.pdf)) | 2025 | Quantum patent landscape survey; categories of quantum IP; filing trends | Not prior art to the invention; landscape context only | Low |
| **DLA Piper quantum patents** ([DLA Piper 2025](https://www.dlapiper.com/en-us/insights/publications/intellectual-property-news/2025/patenting-quantum-computing-challenges-trends-and-future-prospects)) | 2025 | Quantum patent prosecution strategy; § 101 / Art. 52 considerations | Not prior art; prosecution strategy guidance only | Low |

---

## Gap Analysis

The critical gap: no existing quantum job scheduler implements **safety criticality classification with hard deadline enforcement and pre-validated classical fallback for aerospace operational use**. The combination of QW1 5 ms deadline + noise-aware multi-objective scoring + pre-validated fallback + evidence log is novel as a combination.

The IBM/AWS/Azure references are medium risk because they implement backend selection with some priority support. Key differentiation:
- They have no "safety criticality class" concept
- They have no "5 ms hard deadline" for any workload class
- They have no "pre-validated classical fallback designation"
- They have no "evidence log" for regulatory purposes

*Full Espacenet / Derwent Innovation search to be completed by European Patent Attorney.*
