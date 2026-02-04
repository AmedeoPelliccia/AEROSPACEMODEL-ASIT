# CNOT Gates Architecture

## Overview

CNOT (Control Neural Origin Transaction) Gates implement a quantum-circuit-inspired control system for lifecycle transformations in the AEROSPACEMODEL framework. This architecture ensures that transformations execute only when authoritative control state is valid and authorized.

### From README.md Section 17

> **CNOT – Control Neural Origin Transaction**: A transformation gate that executes only when the authoritative control state is valid and authorized. If control assertions fail, the gate does not fire.

## Theoretical Foundation

### Quantum-Circuit-Inspired Logic

From README.md Section 16:

> **Quantum-Circuit–Inspired Logic**: A control-theoretic execution model in which lifecycle transformations behave like explicit gates rather than implicit data flows.

The CNOT gates architecture draws inspiration from quantum computing principles:

1. **State Superposition**: Before gate evaluation, the system exists in a `QuantumState` representing uncollapsed lifecycle ambiguity
2. **Gate Evaluation**: Each gate evaluates specific control conditions deterministically
3. **State Collapse**: When all gates pass, state collapses into a concrete `CollapsedState` with an artifact
4. **No Partial Execution**: If any gate fails, the entire chain stops—no partial transformations occur

### Key Principles

1. **If control assertions fail, the gate does not fire** - Gates block execution when conditions aren't met
2. **Explicit state collapse** - Ambiguity resolves into concrete artifacts only after full validation
3. **Full provenance tracking** - Every decision is recorded for audit trails
4. **Integration with BREX** - Seamless connection to BREX Decision Engine

## Gate Types

The CNOT module implements seven specialized gate types:

### 1. ContractGate

**Purpose**: Validates that a transformation contract is APPROVED or ACTIVE

**Control Condition**: `contract.status ∈ {APPROVED, ACTIVE}`

**Use Case**: Ensures only authorized contracts govern transformations

```python
from aerospacemodel.cnot import ContractGate

gate = ContractGate(contract_id="KITDM-CTR-LM-CSDB_ATA28")
result = gate.execute(context)

if result.passed:
    # Contract is valid - proceed
else:
    # Contract blocked - cannot transform
```

### 2. BaselineGate

**Purpose**: Validates that a baseline is APPROVED or RELEASED (established)

**Control Condition**: `baseline.state ∈ {APPROVED, RELEASED}`

**Use Case**: Ensures transformations reference locked, immutable baselines

```python
from aerospacemodel.cnot import BaselineGate

gate = BaselineGate(baseline_id="FBL-2026-Q1-003")
result = gate.execute(context)
```

### 3. AuthorityGate

**Purpose**: Validates execution authority meets required level

**Control Condition**: `execution_authority ≥ required_authority`

**Authority Hierarchy**:
- STK_TEST (lowest)
- STK_OPS
- STK_ENG
- STK_QA
- STK_SAF
- STK_CM
- STK_SE
- STK_PM
- STK_CERT (highest)

```python
from aerospacemodel.cnot import AuthorityGate

gate = AuthorityGate(required_authority="STK_CM")
result = gate.execute(context)
```

### 4. BREXGate

**Purpose**: Validates BREX (Business Rule Exchange) compliance

**Control Condition**: `brex_cascade.success == true AND final_action == ALLOW`

**Use Case**: Integrates with BREX Decision Engine for rule validation

```python
from aerospacemodel.cnot import BREXGate

gate = BREXGate(config={"cascade_all": True})
result = gate.execute(context)
```

### 5. TraceGate

**Purpose**: Validates traceability completeness

**Control Condition**: `trace_coverage >= threshold`

**Use Case**: Ensures DO-178C/ARP4754A traceability requirements

```python
from aerospacemodel.cnot import TraceGate

gate = TraceGate(config={"coverage_threshold": 100})
result = gate.execute(context)
```

### 6. SafetyGate

**Purpose**: Escalates safety-critical operations for human approval

**Control Condition**: Escalates if `is_safety_critical == true` OR `safety_level ∈ {CATASTROPHIC, HAZARDOUS, MAJOR}`

**Use Case**: Implements non-inference boundary for safety (see Section 6)

```python
from aerospacemodel.cnot import SafetyGate

gate = SafetyGate(config={"escalation_target": "STK_SAF"})
result = gate.execute(context)

if result.status == GateStatus.ESCALATE:
    # Safety-critical - requires human approval
```

### 7. HITLGate (Human-in-the-Loop)

**Purpose**: Marks non-inference boundaries requiring human decisions

**Control Condition**: Requires explicit human decision

**From README.md Sections 6 & 7**:

> **Non-Inference Boundary**: A formally defined execution boundary where automation terminates because ambiguity cannot be resolved deterministically.

> **Human-in-the-Loop (HITL)**: An explicit, auditable human decision point invoked at predefined non-inference boundaries.

```python
from aerospacemodel.cnot import HITLGate

gate = HITLGate(checkpoint_id="CHECKPOINT-001", config={"decision_type": "APPROVAL"})
result = gate.execute(context)

# Result depends on hitl_decision in context
```

## CNOTChain: Unified Application Chain

The `CNOTChain` class orchestrates multiple gates into a unified control flow.

### Chain Execution Model

```
┌─────────────┐
│ QuantumState│ (uncollapsed, ambiguous)
└──────┬──────┘
       │
       ├──→ Gate 1 → PASS
       │
       ├──→ Gate 2 → PASS
       │
       ├──→ Gate 3 → PASS
       │
       ├──→ Gate N → PASS
       │
       ↓
┌──────────────┐
│CollapsedState│ (concrete artifact)
└──────────────┘
```

If any gate BLOCKS or ESCALATES, execution stops immediately:

```
┌─────────────┐
│ QuantumState│
└──────┬──────┘
       │
       ├──→ Gate 1 → PASS
       │
       ├──→ Gate 2 → BLOCK ❌
       │
       ↓
┌──────────────┐
│ BlockedState │ (no artifact)
└──────────────┘
```

### Example: Standard Transformation Chain

```python
from aerospacemodel.cnot import CNOTChain
from aerospacemodel.cnot.integration import create_standard_transformation_chain

# Create a standard chain with common gates
chain = create_standard_transformation_chain(
    contract_id="KITDM-CTR-LM-CSDB_ATA28",
    baseline_id="FBL-2026-Q1-003",
    required_authority="STK_CM",
    include_safety_gate=True,
    include_trace_gate=True,
    trace_coverage_threshold=100
)

# Prepare context
context = {
    "contract": {
        "contract_id": "KITDM-CTR-LM-CSDB_ATA28",
        "status": "ACTIVE"
    },
    "baseline": {
        "baseline_id": "FBL-2026-Q1-003",
        "state": "APPROVED"
    },
    "execution_authority": "STK_CM",
    "brex_result": {
        "success": True,
        "final_action": "ALLOW"
    },
    "trace_data": {
        "total_required": 100,
        "total_linked": 100
    },
    "safety_impact": {
        "is_safety_critical": False,
        "safety_level": "NONE"
    }
}

# Execute chain
result = chain.execute(context)

if result.collapsed:
    print(f"✓ State collapsed: {result.collapsed_state.artifact_id}")
    print(f"✓ All {len(result.gate_results)} gates passed")
    # Proceed with transformation
else:
    print(f"✗ Blocked by gate: {result.blocked_by}")
    # Handle failure or escalation
```

## State Management

### QuantumState

Represents uncollapsed lifecycle ambiguity before gate validation.

```python
from aerospacemodel.cnot.state import QuantumState

quantum_state = QuantumState(
    state_id="QS-001",
    context={"source": "engineering_data"},
    possible_artifacts=["DM-001", "DM-002"]
)
```

### CollapsedState

Represents explicit, authorized resolution after successful gate validation.

```python
from aerospacemodel.cnot.state import CollapsedState, StateType

collapsed_state = CollapsedState(
    state_id="QS-001",
    state_type=StateType.COLLAPSED,
    artifact=data_module,
    artifact_id="DM-RESULT-001",
    collapsed_by="CNOT-CHAIN-001"
)
```

### ProvenanceVector

Machine-readable record linking outputs to sources.

From README.md Section 19:

> **Provenance Vector**: A machine-readable record linking outputs to sources, transformation contracts, execution context, and human decisions.

```python
from aerospacemodel.cnot.state import ProvenanceVector

provenance = ProvenanceVector(
    vector_id="PV-001",
    source_artifacts=["SRC-001", "SRC-002"],
    transformation_contract="KITDM-CTR-LM-CSDB_ATA28",
    execution_context=context
)

# Record gate decision
provenance.add_gate_decision(
    gate_id="CONTRACT-001",
    gate_name="Contract Gate",
    passed=True,
    message="Contract validated",
    evidence={"contract_id": "KITDM-CTR-LM-CSDB_ATA28"}
)

# Record human decision
provenance.add_human_decision(
    decision_type="SAFETY_APPROVAL",
    decision="APPROVED",
    rationale="All safety checks passed",
    decider="John Doe (STK_SAF)"
)
```

## Integration with ASIT/ASIGT

The CNOT module integrates seamlessly with existing AEROSPACEMODEL components:

### With BREX Decision Engine

```python
from aerospacemodel.cnot.integration import integrate_with_brex_engine

# Run BREX cascade and add result to context
context = integrate_with_brex_engine(context, brex_engine)

# BREXGate will use the result
brex_gate = BREXGate()
result = brex_gate.execute(context)
```

### With Contract Manager

```python
from aerospacemodel.cnot.integration import prepare_context_from_contract

# Load contract and prepare context
contract = contract_manager.load_contract("KITDM-CTR-LM-CSDB_ATA28")
context = prepare_context_from_contract(contract)

# Execute chain with prepared context
result = chain.execute(context)
```

### Pipeline Integration

The CNOT transformation pipeline (`pipelines/cnot_transformation_pipeline.yaml`) demonstrates complete integration:

- Gate definitions
- Transformation steps (execute only after gates pass)
- State collapse configuration
- Provenance tracking
- Error handling

## Certification Considerations

### DO-178C Traceability

The CNOT gates architecture supports DO-178C requirements:

1. **Deterministic Execution**: Same inputs → same outputs (replayable)
2. **Full Audit Trail**: Provenance vectors record all decisions
3. **Traceability**: TraceGate enforces coverage requirements
4. **Safety Gates**: HITLGate and SafetyGate mark safety-critical boundaries

### Audit Log Format

All gate executions produce structured audit logs:

```
{timestamp} | GATE {gate_id} | {gate_name} | {status} | {message}
```

Example:
```
2026-02-02T17:00:00.000Z | GATE CONTRACT-KITDM-CTR-LM-CSDB_ATA28 | Contract Gate | PASSED | Contract validated: KITDM-CTR-LM-CSDB_ATA28 (ACTIVE)
2026-02-02T17:00:00.100Z | GATE BASELINE-FBL-2026-Q1-003 | Baseline Gate | PASSED | Baseline validated: FBL-2026-Q1-003 (APPROVED)
2026-02-02T17:00:00.200Z | GATE BREX-CASCADE | BREX Gate | PASSED | BREX validation passed: ALLOW
```

### Retention Requirements

Provenance vectors and audit logs must be retained for 7 years minimum (certification requirement).

## Usage Patterns

### Pattern 1: Minimal Validation

Quick validation with only essential gates:

```python
from aerospacemodel.cnot.integration import create_brex_only_chain

chain = create_brex_only_chain(contract_id="KITDM-CTR-LM-CSDB_ATA28")
result = chain.execute(context)
```

### Pattern 2: Publication Generation

Strict validation for publication outputs:

```python
from aerospacemodel.cnot.integration import create_publication_chain

chain = create_publication_chain(
    contract_id="KITDM-CTR-LM-CSDB_ATA27",
    publication_type="AMM",
    ata_chapter="27",
    required_authority="STK_CM"
)
result = chain.execute(context)
```

### Pattern 3: Custom Chain

Build a custom chain for specific needs:

```python
from aerospacemodel.cnot import CNOTChain, ContractGate, BaselineGate, BREXGate

chain = CNOTChain(chain_id="CUSTOM-CHAIN")
chain.add_gate(ContractGate("KITDM-CTR-LM-CSDB_ATA28"))
chain.add_gate(BaselineGate("FBL-2026-Q1-003"))
chain.add_gate(BREXGate())

result = chain.execute(context)
```

## Error Handling

### Gate Failure

When a gate fails, the chain:
1. Stops execution immediately
2. Records which gate blocked
3. Creates a BlockedState
4. Returns full provenance

```python
result = chain.execute(context)

if not result.success:
    print(f"Chain blocked by: {result.blocked_by}")
    print(f"Failed gate: {result.gate_results[-1].message}")
```

### Escalation

When escalation is required:
1. Chain stops at escalation gate
2. Creates PENDING_HITL state
3. Waits for human decision

```python
if result.collapsed_state.state_type == StateType.PENDING_HITL:
    # Escalation required - await human decision
    print("Awaiting human-in-the-loop decision")
```

## Testing

The CNOT module includes comprehensive tests:

- `tests/test_cnot_gates.py`: Tests for each gate type
- `tests/test_cnot_chain.py`: Tests for chain execution and state collapse

Run tests:
```bash
pytest tests/test_cnot_gates.py tests/test_cnot_chain.py -v
```

## References

- README.md Section 16: Quantum-Circuit–Inspired Logic
- README.md Section 17: CNOT Definition
- README.md Section 18: State Collapse
- README.md Section 19: Provenance Vector
- `ASIGT/brex/brex_decision_engine.py`: BREX integration patterns
- `src/aerospacemodel/asit/contracts.py`: Contract validation
- `src/aerospacemodel/asit/governance.py`: Authority and governance

## Conclusion

The CNOT Gates architecture provides deterministic, auditable, and traceable control for aerospace transformations. By implementing quantum-circuit-inspired gates, it ensures:

✅ No unconstrained autonomy  
✅ No hallucination or guessing  
✅ Full reproducibility  
✅ Complete audit trail  
✅ Certification-ready traceability

All transformations are explicit, governed, and explainable.
