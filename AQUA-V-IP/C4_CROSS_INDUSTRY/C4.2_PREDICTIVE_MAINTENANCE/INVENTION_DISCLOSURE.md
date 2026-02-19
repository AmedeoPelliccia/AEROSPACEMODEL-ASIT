# Invention Disclosure — C4.2 Predictive Maintenance with Quantum Feature Encoding

**Title:** Predictive Maintenance System Using Quantum Feature Encoding of Aircraft Sensor Time-Series Data  
**Docket:** AQUA-V-C4.2-2026-001  
**Parent Docket:** AQUA-V-P0-2026-001  
**Date:** 2026-02-19

---

## 1. Inventors

| Name | Role | Contribution |
|---|---|---|
| **Amedeo Pelliccia** | Primary Inventor | Quantum feature encoding for sensor data; predictive maintenance QUBO scheduling; EU AI Act compliance integration |

---

## 2. Technical Problem

Predictive maintenance for aircraft fleets requires:
1. **High-dimensional feature encoding**: Thousands of sensor channels, each producing time-series data — classical feature engineering loses temporal structure
2. **Multi-fleet optimisation**: Maintenance slot allocation across a fleet is a combinatorial scheduling problem
3. **EU AI Act compliance**: Predictive maintenance AI for safety-critical aircraft systems may qualify as high-risk AI under EU AI Act Annex III — requires transparency, human oversight, and documentation
4. **Operational integration**: Maintenance predictions must integrate with the operational digital twin and trigger QAOS workloads for schedule optimisation

---

## 3. Description of the Invention

### 3.1 Quantum Feature Encoding

Aircraft sensor time-series data (vibration, temperature, pressure, electrical) is encoded into quantum states using amplitude encoding or angle encoding:
- **Amplitude encoding**: A vector of n sensor values is encoded as the amplitudes of log₂(n) qubits
- **Angle encoding**: Each sensor value is encoded as a rotation angle in a parameterised quantum circuit

The encoded quantum state is processed by a variational quantum circuit (VQC) trained to classify component health states.

### 3.2 Maintenance Scheduling QUBO

Fleet maintenance slot allocation is encoded as a QUBO instance:
- Binary variables: maintenance slot assignment for each aircraft × maintenance type × hangar
- Penalty terms: hangar capacity, technician availability, minimum flight hours between checks, regulatory inspection intervals (EASA Part M)

### 3.3 EU AI Act Integration

The predictive maintenance system implements EU AI Act Article 14 (human oversight) by requiring human confirmation before scheduling a maintenance event triggered by a quantum classification result with confidence below a configurable threshold.

---

## 4. Embodiment

**Primary:** BWB-H₂ fuel cell health monitoring — quantum classifier trained on fuel cell stack voltage and temperature data to predict stack degradation before cell failure.

**Secondary:** LH₂ tank insulation integrity monitoring — quantum anomaly detection on boil-off rate time-series.

---

*EP independent application at EPO (Munich, EU) — target: 2029.*
