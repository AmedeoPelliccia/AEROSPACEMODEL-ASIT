"""
CNOT Chain - Unified Application Chain

Implements quantum-circuit-inspired execution model where transformations
behave like explicit gates rather than implicit data flows.

From README.md Section 16 & 17:
    "Quantum-Circuit–Inspired Logic: A control-theoretic execution model in
    which lifecycle transformations behave like explicit gates rather than
    implicit data flows."
    
    "CNOT – Control Neural Origin Transaction: A transformation gate that
    executes only when the authoritative control state is valid and authorized.
    If control assertions fail, the gate does not fire."

Key Principles:
    - Chains multiple gates in sequence
    - Stops execution at first failing gate (no partial execution)
    - Produces provenance vectors for all decisions
    - Integrates with existing BREX Decision Engine
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from .gates import CNOTGate, GateResult, GateStatus
from .state import (
    CollapsedState,
    ProvenanceVector,
    QuantumState,
    StateType,
)

logger = logging.getLogger(__name__)


@dataclass
class ChainResult:
    """
    Result of a complete CNOT chain execution.
    
    Attributes:
        chain_id: Unique identifier for this chain execution
        success: Whether chain completed successfully
        collapsed: Whether state collapsed to concrete artifact
        blocked_by: Gate that blocked execution (if any)
        gate_results: Results from each gate execution
        provenance: Complete provenance vector
        quantum_state: Input quantum state
        collapsed_state: Output collapsed state (if successful)
        started_at: Chain execution start time
        completed_at: Chain execution completion time
    """
    chain_id: str
    success: bool = False
    collapsed: bool = False
    blocked_by: Optional[str] = None
    gate_results: List[GateResult] = field(default_factory=list)
    provenance: Optional[ProvenanceVector] = None
    quantum_state: Optional[QuantumState] = None
    collapsed_state: Optional[CollapsedState] = None
    started_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    completed_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "chain_id": self.chain_id,
            "success": self.success,
            "collapsed": self.collapsed,
            "blocked_by": self.blocked_by,
            "gate_results": [gr.to_dict() for gr in self.gate_results],
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "quantum_state": self.quantum_state.to_dict() if self.quantum_state else None,
            "collapsed_state": self.collapsed_state.to_dict() if self.collapsed_state else None,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }


class CNOTChain:
    """
    Unified Chain of CNOT Gates for transformation control.
    
    Implements explicit gate-based execution where transformations
    behave like explicit gates rather than implicit data flows.
    
    From README.md Section 16:
        "Quantum-Circuit–Inspired Logic: A control-theoretic execution model
        in which lifecycle transformations behave like explicit gates rather
        than implicit data flows."
    
    Example:
        >>> chain = CNOTChain()
        >>> chain.add_gate(ContractGate("KITDM-CTR-LM-CSDB_ATA28"))
        >>> chain.add_gate(BaselineGate("FBL-2026-Q1-003"))
        >>> chain.add_gate(BREXGate())
        >>> chain.add_gate(SafetyGate())
        >>> 
        >>> result = chain.execute(context)
        >>> if result.collapsed:
        ...     # State collapsed - proceed with transformation
        ...     artifact = result.collapsed_state.artifact
        >>> else:
        ...     # Gate blocked - check which gate failed
        ...     print(f"Blocked by: {result.blocked_by}")
    
    Attributes:
        chain_id: Unique identifier for this chain
        gates: List of gates in execution order
        provenance_enabled: Whether to track full provenance
    """
    
    def __init__(self, chain_id: Optional[str] = None, provenance_enabled: bool = True):
        """
        Initialize a CNOT chain.
        
        Args:
            chain_id: Unique identifier (auto-generated if not provided)
            provenance_enabled: Whether to track full provenance (default: True)
        """
        self.chain_id = chain_id or f"CNOT-CHAIN-{uuid.uuid4().hex[:8].upper()}"
        self.gates: List[CNOTGate] = []
        self.provenance_enabled = provenance_enabled
        logger.info(f"Created CNOT chain: {self.chain_id}")
    
    def add_gate(self, gate: CNOTGate) -> CNOTChain:
        """
        Add a gate to the chain.
        
        Args:
            gate: CNOT gate to add
            
        Returns:
            Self for method chaining
        """
        self.gates.append(gate)
        logger.debug(f"Added gate to chain {self.chain_id}: {gate.gate_id}")
        return self
    
    def execute(
        self,
        context: Dict[str, Any],
        quantum_state: Optional[QuantumState] = None
    ) -> ChainResult:
        """
        Execute the gate chain.
        
        From README.md Section 17:
            "A transformation gate that executes only when the authoritative
            control state is valid and authorized. If control assertions fail,
            the gate does not fire."
        
        Chain execution stops at the first failing gate. No partial execution
        occurs - either all gates pass and state collapses, or execution is
        blocked and state remains uncollapsed.
        
        Args:
            context: Execution context containing all necessary data
            quantum_state: Input quantum state (auto-created if not provided)
            
        Returns:
            ChainResult with complete execution details
        """
        logger.info(f"Executing CNOT chain: {self.chain_id} ({len(self.gates)} gates)")
        
        # Initialize result
        result = ChainResult(chain_id=self.chain_id)
        
        # Create or use provided quantum state
        if quantum_state is None:
            state_id = f"QS-{uuid.uuid4().hex[:8].upper()}"
            quantum_state = QuantumState(
                state_id=state_id,
                context=context.copy()
            )
        
        result.quantum_state = quantum_state
        
        # Initialize provenance vector
        provenance = None
        if self.provenance_enabled:
            provenance = ProvenanceVector(
                vector_id=f"PV-{self.chain_id}",
                source_artifacts=context.get("source_artifacts", []),
                transformation_contract=context.get("contract", {}).get("contract_id"),
                execution_context=context.copy()
            )
            quantum_state.provenance = provenance
            result.provenance = provenance
        
        # Execute each gate in sequence
        for gate in self.gates:
            logger.debug(f"Executing gate: {gate.gate_id}")
            
            try:
                gate_result = gate.execute(context)
                result.gate_results.append(gate_result)
                
                # Record gate decision in provenance
                if self.provenance_enabled and provenance:
                    provenance.add_gate_decision(
                        gate_id=gate_result.gate_id,
                        gate_name=gate_result.gate_name,
                        passed=gate_result.passed,
                        message=gate_result.message,
                        evidence=gate_result.evidence
                    )
                
                # Log gate result
                logger.info(gate_result.to_log_entry())
                
                # Check if gate blocked execution
                if gate_result.status == GateStatus.BLOCKED or (not gate_result.passed and gate_result.status != GateStatus.ESCALATE):
                    logger.warning(f"Chain blocked by gate: {gate.gate_id}")
                    result.success = False
                    result.collapsed = False
                    result.blocked_by = gate.gate_id
                    result.completed_at = datetime.utcnow().isoformat() + "Z"
                    
                    # Create blocked state
                    result.collapsed_state = CollapsedState(
                        state_id=quantum_state.state_id,
                        state_type=StateType.BLOCKED,
                        provenance=provenance,
                        collapsed_by=self.chain_id
                    )
                    
                    return result
                
                # Check if gate requires escalation
                if gate_result.status == GateStatus.ESCALATE:
                    logger.info(f"Chain requires escalation: {gate.gate_id}")
                    result.success = False
                    result.collapsed = False
                    result.blocked_by = gate.gate_id
                    result.completed_at = datetime.utcnow().isoformat() + "Z"
                    
                    # Create pending HITL state
                    result.collapsed_state = CollapsedState(
                        state_id=quantum_state.state_id,
                        state_type=StateType.PENDING_HITL,
                        provenance=provenance,
                        collapsed_by=self.chain_id
                    )
                    
                    return result
                
            except Exception as e:
                logger.error(f"Gate execution failed: {gate.gate_id}: {e}", exc_info=True)
                result.success = False
                result.collapsed = False
                result.blocked_by = gate.gate_id
                result.completed_at = datetime.utcnow().isoformat() + "Z"
                
                # Record error in provenance
                if self.provenance_enabled and provenance:
                    provenance.add_gate_decision(
                        gate_id=gate.gate_id,
                        gate_name=gate.gate_name,
                        passed=False,
                        message=f"Exception: {e}",
                        evidence={"exception": str(e)}
                    )
                
                # Create blocked state
                result.collapsed_state = CollapsedState(
                    state_id=quantum_state.state_id,
                    state_type=StateType.BLOCKED,
                    provenance=provenance,
                    collapsed_by=self.chain_id
                )
                
                return result
        
        # All gates passed - collapse state
        logger.info(f"All gates passed - collapsing state: {quantum_state.state_id}")
        
        result.success = True
        result.collapsed = True
        result.completed_at = datetime.utcnow().isoformat() + "Z"
        
        # Generate artifact (placeholder - actual artifact would come from context)
        artifact_id = context.get("artifact_id", f"ARTIFACT-{uuid.uuid4().hex[:8].upper()}")
        artifact = context.get("artifact")
        
        # Update provenance with collapsed artifact
        if self.provenance_enabled and provenance:
            provenance.collapsed_artifact = artifact_id
        
        # Create collapsed state
        result.collapsed_state = CollapsedState(
            state_id=quantum_state.state_id,
            state_type=StateType.COLLAPSED,
            artifact=artifact,
            artifact_id=artifact_id,
            provenance=provenance,
            collapsed_by=self.chain_id
        )
        
        logger.info(f"State collapsed successfully: {quantum_state.state_id} -> {artifact_id}")
        
        return result
    
    def validate_chain(self) -> bool:
        """
        Validate the chain configuration.
        
        Returns:
            True if chain is valid, False otherwise
        """
        if not self.gates:
            logger.warning(f"Chain {self.chain_id} has no gates")
            return False
        
        # Check for duplicate gate IDs
        gate_ids = [gate.gate_id for gate in self.gates]
        if len(gate_ids) != len(set(gate_ids)):
            logger.error(f"Chain {self.chain_id} has duplicate gate IDs")
            return False
        
        logger.info(f"Chain {self.chain_id} validated: {len(self.gates)} gates")
        return True
    
    def get_gate_count(self) -> int:
        """Get the number of gates in the chain."""
        return len(self.gates)
    
    def get_gate_ids(self) -> List[str]:
        """Get list of gate IDs in execution order."""
        return [gate.gate_id for gate in self.gates]
    
    def clear_gates(self) -> None:
        """Clear all gates from the chain."""
        logger.debug(f"Clearing gates from chain: {self.chain_id}")
        self.gates.clear()
