"""
CNOT State Management

Implements state collapse mechanics for transformation control.

From README.md:
    Section 18: "State Collapse - The explicit, authorized resolution of lifecycle
                 ambiguity into a concrete artifact."
    Section 19: "Provenance Vector - A machine-readable record linking outputs to
                 sources, transformation contracts, execution context, and human decisions."

Key Concepts:
    - QuantumState: Represents uncollapsed lifecycle ambiguity
    - CollapsedState: Represents explicit, authorized resolution
    - ProvenanceVector: Machine-readable record linking outputs to sources
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class StateType(Enum):
    """State types in CNOT transformation process."""
    UNCOLLAPSED = "uncollapsed"  # Ambiguous, not yet resolved
    COLLAPSED = "collapsed"      # Resolved into concrete artifact
    BLOCKED = "blocked"          # Cannot collapse - gate failed
    PENDING_HITL = "pending_hitl"  # Awaiting human decision


@dataclass
class ProvenanceVector:
    """
    Machine-readable record linking outputs to sources.
    
    From README.md Section 19:
        "A machine-readable record linking outputs to sources, transformation
        contracts, execution context, and human decisions."
    
    Attributes:
        vector_id: Unique identifier for this provenance vector
        source_artifacts: Input artifacts and their identifiers
        transformation_contract: Contract ID governing transformation
        execution_context: Context data at execution time
        human_decisions: Record of HITL decisions made
        timestamp: When this vector was created
        gate_decisions: Decisions made by each gate in the chain
        collapsed_artifact: Final artifact ID (if state collapsed)
    """
    vector_id: str
    source_artifacts: List[str] = field(default_factory=list)
    transformation_contract: Optional[str] = None
    execution_context: Dict[str, Any] = field(default_factory=dict)
    human_decisions: List[Dict[str, Any]] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    gate_decisions: List[Dict[str, Any]] = field(default_factory=list)
    collapsed_artifact: Optional[str] = None
    
    def add_gate_decision(
        self,
        gate_id: str,
        gate_name: str,
        passed: bool,
        message: str,
        evidence: Optional[Dict[str, Any]] = None
    ) -> None:
        """Record a gate decision in the provenance vector."""
        decision = {
            "gate_id": gate_id,
            "gate_name": gate_name,
            "passed": passed,
            "message": message,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "evidence": evidence or {},
        }
        self.gate_decisions.append(decision)
    
    def add_human_decision(
        self,
        decision_type: str,
        decision: str,
        rationale: str,
        decider: str
    ) -> None:
        """Record a human-in-the-loop decision."""
        hitl_decision = {
            "decision_type": decision_type,
            "decision": decision,
            "rationale": rationale,
            "decider": decider,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        self.human_decisions.append(hitl_decision)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "vector_id": self.vector_id,
            "source_artifacts": self.source_artifacts,
            "transformation_contract": self.transformation_contract,
            "execution_context": self.execution_context,
            "human_decisions": self.human_decisions,
            "timestamp": self.timestamp,
            "gate_decisions": self.gate_decisions,
            "collapsed_artifact": self.collapsed_artifact,
        }


@dataclass
class QuantumState:
    """
    Represents uncollapsed lifecycle ambiguity.
    
    From README.md Section 18:
        "State Collapse - The explicit, authorized resolution of lifecycle
        ambiguity into a concrete artifact."
    
    A QuantumState represents the ambiguous, not-yet-determined state before
    transformation gates have validated and authorized the transformation.
    
    Attributes:
        state_id: Unique identifier for this state
        state_type: Type of state (always UNCOLLAPSED for QuantumState)
        context: Context data describing the ambiguous state
        possible_artifacts: Possible output artifacts (not yet determined)
        provenance: Provenance vector tracking this state
        created_at: When this state was created
    """
    state_id: str
    state_type: StateType = StateType.UNCOLLAPSED
    context: Dict[str, Any] = field(default_factory=dict)
    possible_artifacts: List[str] = field(default_factory=list)
    provenance: Optional[ProvenanceVector] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "state_id": self.state_id,
            "state_type": self.state_type.value,
            "context": self.context,
            "possible_artifacts": self.possible_artifacts,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "created_at": self.created_at,
        }


@dataclass
class CollapsedState:
    """
    Represents explicit, authorized resolution.
    
    From README.md Section 18:
        "State Collapse - The explicit, authorized resolution of lifecycle
        ambiguity into a concrete artifact."
    
    A CollapsedState represents the concrete, determined artifact after all
    transformation gates have validated and authorized the transformation.
    
    Attributes:
        state_id: Unique identifier (same as source QuantumState)
        state_type: Type of state (COLLAPSED or BLOCKED)
        artifact: Concrete artifact produced (if collapsed successfully)
        artifact_id: Unique identifier for the artifact
        provenance: Complete provenance vector for audit trail
        collapsed_at: When state collapse occurred
        collapsed_by: What triggered the collapse (gate chain ID)
    """
    state_id: str
    state_type: StateType = StateType.COLLAPSED
    artifact: Optional[Any] = None
    artifact_id: Optional[str] = None
    provenance: Optional[ProvenanceVector] = None
    collapsed_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    collapsed_by: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "state_id": self.state_id,
            "state_type": self.state_type.value,
            "artifact": str(self.artifact) if self.artifact else None,
            "artifact_id": self.artifact_id,
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "collapsed_at": self.collapsed_at,
            "collapsed_by": self.collapsed_by,
        }
