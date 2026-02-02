"""
CNOT (Control Neural Origin Transaction) Gates Module

Implements quantum-circuit-inspired control gates for lifecycle transformations.
Gates execute only when authoritative control state is valid and authorized.

Key Principles:
    - If control assertions fail, the gate does not fire
    - Explicit state collapse (ambiguity → concrete artifact)
    - Full provenance tracking
    - Integration with BREX decision engine

Components:
    - gates: Core gate implementations (ContractGate, BaselineGate, etc.)
    - chain: CNOTChain for unified application chains
    - state: State management (QuantumState, CollapsedState, ProvenanceVector)
    - integration: ASIT/ASIGT integration layer

From README.md Section 17:
    "CNOT – Control Neural Origin Transaction: A transformation gate that executes
    only when the authoritative control state is valid and authorized. If control
    assertions fail, the gate does not fire."
"""

from .gates import (
    CNOTGate,
    ContractGate,
    BaselineGate,
    AuthorityGate,
    BREXGate,
    TraceGate,
    SafetyGate,
    HITLGate,
    GateResult,
    GateStatus,
)

from .chain import (
    CNOTChain,
    ChainResult,
)

from .state import (
    QuantumState,
    CollapsedState,
    ProvenanceVector,
    StateType,
)

__all__ = [
    # Gates
    "CNOTGate",
    "ContractGate",
    "BaselineGate",
    "AuthorityGate",
    "BREXGate",
    "TraceGate",
    "SafetyGate",
    "HITLGate",
    "GateResult",
    "GateStatus",
    # Chain
    "CNOTChain",
    "ChainResult",
    # State
    "QuantumState",
    "CollapsedState",
    "ProvenanceVector",
    "StateType",
]

__version__ = "2.0.0"
