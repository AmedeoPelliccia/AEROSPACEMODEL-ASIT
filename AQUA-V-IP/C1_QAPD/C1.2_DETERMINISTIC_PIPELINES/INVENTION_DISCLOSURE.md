# Invention Disclosure — C1.2 Deterministic Reproducibility Pipelines

**Title:** Deterministic Reproducibility Pipeline for Quantum-Assisted Design Computations in Safety-Critical Systems  
**Docket:** AQUA-V-C1.2-2026-001  
**Parent Docket:** AQUA-V-P0-2026-001  
**Date:** 2026-02-19  
**Priority:** ★ HIGHEST PRIORITY CHILD APPLICATION

---

## 1. Inventors

| Name | Role | Contribution |
|---|---|---|
| **Amedeo Pelliccia** | Primary Inventor | Deterministic seeding architecture; cryptographic evidence record schema; lifecycle phase binding; SSOT promotion gate design |

---

## 2. Technical Problem

### 2.1 The Non-Determinism Problem in Quantum Certification

Quantum computers are **inherently probabilistic**. A given quantum circuit, executed twice on the same hardware with the same inputs, may return different bitstring measurement outcomes due to:
- Shot noise (finite number of circuit measurements)
- Gate errors and decoherence
- Variational algorithm convergence to different local minima (QAOA)
- Backend-level scheduling and noise fluctuations

This non-determinism is **incompatible** with aerospace certification standards:
- **DO-178C** (Software Considerations in Airborne Systems): requires that "the software, when executed, performs its intended function with the independence and integrity required to satisfy airworthiness requirements"
- **ARP4754A** (Guidelines for Development of Civil Aircraft and Systems): requires design evidence to be traceable, repeatable, and independently verifiable
- **EASA CS-25** and **FAA FAR Part 25**: require that design decisions be documented with sufficient information to allow independent verification

No existing quantum cloud service (IBM Quantum, AWS Braket, Google Quantum AI, IonQ) provides a mechanism to reconstruct the exact result set of a past computation from a compact evidence record.

### 2.2 Gap in Prior Art

Existing approaches to reproducibility in quantum computing address:
- **Circuit reproducibility**: same circuit → same measurement outcomes only if noise model is identical (not achievable in practice)
- **Simulation reproducibility**: seeded simulators → reproducible, but does not help with real QPU runs
- **Result logging**: store all results → scalable problem (exponentially large result space for large QUBO)

None of these approaches generate a **compact, cryptographically verifiable evidence record** that enables:
1. Independent reconstruction of the top-k ranked solutions at any future time
2. Binding of the reconstruction to a specific solver version and noise configuration
3. Packaging of the evidence in a format suitable for submission to EASA/FAA as a design justification artefact

---

## 3. Description of the Invention

### 3.1 The Deterministic Evidence Record (DER)

The core invention is a **Deterministic Evidence Record (DER)** — a compact data structure that captures sufficient information to deterministically reconstruct the top-k ranked solutions of a quantum-assisted optimisation computation:

```python
@dataclass
class DeterministicEvidenceRecord:
    # Identity
    record_id: str              # UUID v4
    lc_phase: str               # Lifecycle phase (LC03–LC08)
    ata_reference: str          # ATA chapter of the system being designed

    # Deterministic seed
    global_seed: int            # 64-bit seed derived from SHA-256(canonical_inputs)
    
    # Input traceability
    input_hash: str             # SHA-256 of canonical serialisation of all QUBO inputs
    input_schema_version: str   # Version of the aerospace constraint schema used
    
    # Solver configuration
    solver_name: str            # e.g., "qaoa", "simulated_annealing", "dwave_advantage"
    solver_version: str         # e.g., "qiskit-aer==0.15.1"
    backend_id: str             # e.g., "ibm_kyoto", "dwave_advantage_6.4"
    circuit_depth: int          # QAOA circuit depth p (if applicable)
    circuit_hash: str           # SHA-256 of compiled QASM circuit
    noise_model_hash: str       # SHA-256 of noise model configuration (if simulator)
    
    # Results
    top_k: int                  # Number of ranked solutions recorded
    top_k_results: list         # List of (bitstring, energy) tuples
    result_hash: str            # SHA-256 of canonical serialisation of top_k_results
    
    # Provenance
    timestamp_utc: str          # ISO 8601 timestamp
    ssot_ref: str               # Reference to SSOT entry if design was promoted
    
    # Integrity
    digital_signature: str      # ECDSA-P384 signature over all other fields
    signing_key_id: str         # Reference to HSM key used for signing
```

### 3.2 Global Seed Generation

The global seed is derived deterministically from the input data:

```python
def generate_global_seed(qubo_inputs: dict) -> tuple[int, str]:
    """
    Returns (global_seed, input_hash).
    The seed is the first 64 bits of the SHA-256 hash of the canonical
    JSON serialisation of all QUBO inputs (sorted keys, no whitespace).
    """
    canonical = json.dumps(qubo_inputs, sort_keys=True, separators=(',', ':'))
    input_hash = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
    global_seed = int(input_hash[:16], 16)  # First 16 hex chars = 64 bits
    return global_seed, input_hash
```

This ensures that the same input data always produces the same seed, enabling independent parties to verify the seed from the input data alone.

### 3.3 Seeded Execution

The global seed is applied to all pseudo-random number generators in the quantum computation:

```python
def execute_with_deterministic_seed(
    qubo_matrix: np.ndarray,
    global_seed: int,
    solver_config: SolverConfig,
    top_k: int = 10
) -> list[tuple[str, float]]:
    """
    Execute QUBO with deterministic seeding.
    For QAOA: seeds the parameter initialisation and shot sampling.
    For simulated annealing: seeds the Metropolis PRNG.
    For D-Wave: records the random_seed parameter in the DER (hardware is non-deterministic,
    but the evidence record captures the hardware-returned result for reconstruction).
    """
    np.random.seed(global_seed)
    random.seed(global_seed)
    # ... execute solver with seeded PRNG
    # Return top-k (bitstring, energy) pairs
```

### 3.4 Evidence Record Generation and Signing

After execution, the DER is generated and digitally signed under an HSM-protected key:

```python
def generate_der(
    qubo_inputs: dict,
    solver_config: SolverConfig,
    top_k_results: list,
    lc_phase: str,
    ata_reference: str
) -> DeterministicEvidenceRecord:
    global_seed, input_hash = generate_global_seed(qubo_inputs)
    result_hash = hashlib.sha256(
        json.dumps(top_k_results, sort_keys=True).encode()
    ).hexdigest()
    
    der = DeterministicEvidenceRecord(
        record_id=str(uuid.uuid4()),
        lc_phase=lc_phase,
        ata_reference=ata_reference,
        global_seed=global_seed,
        input_hash=input_hash,
        ...
        result_hash=result_hash,
        timestamp_utc=datetime.utcnow().isoformat() + 'Z'
    )
    
    # Sign with HSM
    der.digital_signature = hsm.sign_ecdsa_p384(
        payload=der.canonical_bytes_without_signature()
    )
    return der
```

### 3.5 Exact Reconstruction from Evidence Record

The key capability: given only the DER, the exact top-k results can be reconstructed:

```python
def reconstruct_from_der(der: DeterministicEvidenceRecord) -> list:
    """
    Reconstruct top-k results from evidence record.
    For seeded simulators: re-execute with der.global_seed → identical results.
    For real QPU runs: top_k_results are stored directly in the DER.
    Verify by computing SHA-256(top_k_results) == der.result_hash.
    """
    reconstructed = der.top_k_results  # Directly available from DER
    # Verify integrity
    computed_hash = hashlib.sha256(
        json.dumps(reconstructed, sort_keys=True).encode()
    ).hexdigest()
    assert computed_hash == der.result_hash, "Integrity check failed"
    return reconstructed
```

### 3.6 Lifecycle Phase Binding

DERs are bound to specific lifecycle phases per the AMPEL360 framework:
- **LC03** (System Architecture): DERs for high-level design topology decisions
- **LC04** (Detailed Design): DERs for component-level QUBO computations
- **LC06** (Verification): DERs used as evidence in verification records
- **LC08** (Certification): DERs packaged as certification evidence artefacts

---

## 4. Advantages Over Prior Art

| Prior Art Approach | C1.2 Advantage |
|---|---|
| Quantum cloud logging (IBM, AWS) | DER is a compact, cryptographically verifiable record; not raw shot data |
| Classical seeded PRNG | Handles real QPU (non-deterministic hardware) via result storage + hash |
| DO-178C tool qualification | DER provides evidence of quantum tool output, complementing classical TQR |
| Manual result documentation | DER is machine-generated, tamper-evident, and independently verifiable |

---

## 5. Embodiments

### Primary: QAOA for BWB Structural Topology (LC04)
DER generated for each QAOA run during detailed design of BWB structural topology. DER stored in SSOT with reference to the design decision it supports.

### Secondary: Simulated Annealing Fallback with Same Seed
When QPU is unavailable, the same global seed is applied to the classical fallback solver. The DER records the fallback event, maintaining certification evidence continuity.

### Tertiary: Multi-Run Consensus
Multiple DERs from independent runs with different seeds are generated and compared. The consensus solution is promoted to SSOT with all constituent DERs as supporting evidence.

---

*Confidential — ★ HIGHEST PRIORITY for EP filing. Target filing: within 14 days of Day 0 (by 2026-03-05 at EPO).*
