"""
CNOT Gates - Control Neural Origin Transaction

Implements quantum-circuit-inspired control gates for lifecycle transformations.
Gates execute only when authoritative control state is valid and authorized.

From README.md Section 17:
    "CNOT – Control Neural Origin Transaction: A transformation gate that executes
    only when the authoritative control state is valid and authorized. If control
    assertions fail, the gate does not fire."

Key Principles:
    - If control assertions fail, the gate does not fire
    - Explicit state collapse (ambiguity → concrete artifact)
    - Full provenance tracking
    - Integration with BREX decision engine

Gate Types:
    - ContractGate: Validates contract is APPROVED/ACTIVE
    - BaselineGate: Validates baseline is ESTABLISHED
    - AuthorityGate: Validates execution authority
    - BREXGate: Validates BREX compliance
    - TraceGate: Validates traceability completeness
    - SafetyGate: Escalates safety-critical operations
    - HITLGate: Human-in-the-loop checkpoint
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class GateStatus(Enum):
    """Status of gate execution."""
    PASSED = "passed"      # Gate passed - allow execution
    BLOCKED = "blocked"    # Gate blocked - stop execution
    ESCALATE = "escalate"  # Requires human approval
    PENDING = "pending"    # Awaiting evaluation


@dataclass
class GateResult:
    """
    Result of a gate execution.
    
    Attributes:
        gate_id: Unique identifier for the gate
        gate_name: Human-readable gate name
        status: Execution status
        passed: Whether the gate passed
        message: Result message
        timestamp: When the gate was evaluated
        context: Context data at evaluation time
        evidence: Evidence supporting the decision
    """
    gate_id: str
    gate_name: str
    status: GateStatus
    passed: bool
    message: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    context: Dict[str, Any] = field(default_factory=dict)
    evidence: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "gate_id": self.gate_id,
            "gate_name": self.gate_name,
            "status": self.status.value,
            "passed": self.passed,
            "message": self.message,
            "timestamp": self.timestamp,
            "context": self.context,
            "evidence": self.evidence,
        }
    
    def to_log_entry(self) -> str:
        """Generate audit log entry format."""
        status_str = "PASSED" if self.passed else "BLOCKED"
        return f"{self.timestamp} | GATE {self.gate_id} | {self.gate_name} | {status_str} | {self.message}"


class CNOTGate(ABC):
    """
    Abstract base class for CNOT gates.
    
    All CNOT gates must implement the execute method which evaluates
    whether the gate passes or blocks execution.
    
    From README.md Section 17:
        "A transformation gate that executes only when the authoritative
        control state is valid and authorized. If control assertions fail,
        the gate does not fire."
    """
    
    def __init__(self, gate_id: str, gate_name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize a CNOT gate.
        
        Args:
            gate_id: Unique identifier for this gate instance
            gate_name: Human-readable name
            config: Configuration parameters for the gate
        """
        self.gate_id = gate_id
        self.gate_name = gate_name
        self.config = config or {}
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> GateResult:
        """
        Execute the gate evaluation.
        
        Args:
            context: Execution context containing all necessary data
            
        Returns:
            GateResult indicating whether gate passed or blocked
        """
        pass
    
    def _create_result(
        self,
        status: GateStatus,
        passed: bool,
        message: str,
        context: Dict[str, Any],
        evidence: Optional[Dict[str, Any]] = None
    ) -> GateResult:
        """Helper to create a GateResult."""
        return GateResult(
            gate_id=self.gate_id,
            gate_name=self.gate_name,
            status=status,
            passed=passed,
            message=message,
            context=context,
            evidence=evidence or {}
        )


class ContractGate(CNOTGate):
    """
    Validates contract is APPROVED/ACTIVE.
    
    Control Condition: Contract status must be APPROVED or ACTIVE
    
    This gate ensures that a valid transformation contract exists and is
    in an executable state before any transformation proceeds.
    """
    
    def __init__(self, contract_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        super().__init__(
            gate_id=f"CONTRACT-{contract_id or 'CHECK'}",
            gate_name="Contract Gate",
            config=config
        )
        self.contract_id = contract_id
        self.require_approved = config.get("require_approved", True) if config else True
    
    def execute(self, context: Dict[str, Any]) -> GateResult:
        """Execute contract validation."""
        logger.debug(f"Executing ContractGate: {self.gate_id}")
        
        # Extract contract from context
        contract = context.get("contract")
        if not contract:
            return self._create_result(
                status=GateStatus.BLOCKED,
                passed=False,
                message="No contract found in context",
                context=context,
                evidence={"required_field": "contract"}
            )
        
        # Check contract status
        contract_status = contract.get("status", "")
        valid_statuses = ["APPROVED", "ACTIVE"] if self.require_approved else ["REVIEW", "APPROVED", "ACTIVE"]
        
        if contract_status not in valid_statuses:
            return self._create_result(
                status=GateStatus.BLOCKED,
                passed=False,
                message=f"Contract status '{contract_status}' not in {valid_statuses}",
                context=context,
                evidence={
                    "contract_id": contract.get("contract_id"),
                    "contract_status": contract_status,
                    "required_statuses": valid_statuses
                }
            )
        
        # Validate contract ID if specified
        if self.contract_id:
            actual_contract_id = contract.get("contract_id")
            if actual_contract_id != self.contract_id:
                return self._create_result(
                    status=GateStatus.BLOCKED,
                    passed=False,
                    message=f"Contract ID mismatch: expected '{self.contract_id}', got '{actual_contract_id}'",
                    context=context,
                    evidence={
                        "expected_contract_id": self.contract_id,
                        "actual_contract_id": actual_contract_id
                    }
                )
        
        return self._create_result(
            status=GateStatus.PASSED,
            passed=True,
            message=f"Contract validated: {contract.get('contract_id')} ({contract_status})",
            context=context,
            evidence={
                "contract_id": contract.get("contract_id"),
                "contract_status": contract_status
            }
        )


class BaselineGate(CNOTGate):
    """
    Validates baseline is ESTABLISHED.
    
    Control Condition: Baseline state must be APPROVED or RELEASED
    
    This gate ensures that the referenced baseline exists and is in a
    locked, immutable state before transformation proceeds.
    """
    
    def __init__(self, baseline_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        super().__init__(
            gate_id=f"BASELINE-{baseline_id or 'CHECK'}",
            gate_name="Baseline Gate",
            config=config
        )
        self.baseline_id = baseline_id
        self.require_established = config.get("require_established", True) if config else True
    
    def execute(self, context: Dict[str, Any]) -> GateResult:
        """Execute baseline validation."""
        logger.debug(f"Executing BaselineGate: {self.gate_id}")
        
        # Extract baseline from context
        baseline = context.get("baseline")
        if not baseline:
            return self._create_result(
                status=GateStatus.BLOCKED,
                passed=False,
                message="No baseline found in context",
                context=context,
                evidence={"required_field": "baseline"}
            )
        
        # Check baseline state
        baseline_state = baseline.get("state", "")
        valid_states = ["APPROVED", "RELEASED"] if self.require_established else ["REVIEW", "APPROVED", "RELEASED"]
        
        if baseline_state not in valid_states:
            return self._create_result(
                status=GateStatus.BLOCKED,
                passed=False,
                message=f"Baseline state '{baseline_state}' not in {valid_states}",
                context=context,
                evidence={
                    "baseline_id": baseline.get("baseline_id"),
                    "baseline_state": baseline_state,
                    "required_states": valid_states
                }
            )
        
        # Validate baseline ID if specified
        if self.baseline_id:
            actual_baseline_id = baseline.get("baseline_id")
            if actual_baseline_id != self.baseline_id:
                return self._create_result(
                    status=GateStatus.BLOCKED,
                    passed=False,
                    message=f"Baseline ID mismatch: expected '{self.baseline_id}', got '{actual_baseline_id}'",
                    context=context,
                    evidence={
                        "expected_baseline_id": self.baseline_id,
                        "actual_baseline_id": actual_baseline_id
                    }
                )
        
        return self._create_result(
            status=GateStatus.PASSED,
            passed=True,
            message=f"Baseline validated: {baseline.get('baseline_id')} ({baseline_state})",
            context=context,
            evidence={
                "baseline_id": baseline.get("baseline_id"),
                "baseline_state": baseline_state
            }
        )


class AuthorityGate(CNOTGate):
    """
    Validates execution authority.
    
    Control Condition: Execution authority must meet required level
    
    This gate ensures that the executing agent/user has the required
    authority level to perform the transformation.
    """
    
    def __init__(self, required_authority: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        super().__init__(
            gate_id=f"AUTHORITY-{required_authority or 'CHECK'}",
            gate_name="Authority Gate",
            config=config
        )
        self.required_authority = required_authority or (config.get("required_authority") if config else None)
        
        # Authority hierarchy (higher index = higher authority)
        self.authority_levels = [
            "STK_TEST",
            "STK_OPS",
            "STK_ENG",
            "STK_QA",
            "STK_SAF",
            "STK_CM",
            "STK_SE",
            "STK_PM",
            "STK_CERT"
        ]
    
    def execute(self, context: Dict[str, Any]) -> GateResult:
        """Execute authority validation."""
        logger.debug(f"Executing AuthorityGate: {self.gate_id}")
        
        # Extract authority from context
        current_authority = context.get("execution_authority")
        if not current_authority:
            return self._create_result(
                status=GateStatus.BLOCKED,
                passed=False,
                message="No execution authority found in context",
                context=context,
                evidence={"required_field": "execution_authority"}
            )
        
        # Check if required authority is set
        if not self.required_authority:
            return self._create_result(
                status=GateStatus.PASSED,
                passed=True,
                message=f"Authority validated: {current_authority} (no specific requirement)",
                context=context,
                evidence={"current_authority": current_authority}
            )
        
        # Validate authority level
        try:
            current_level = self.authority_levels.index(current_authority)
            required_level = self.authority_levels.index(self.required_authority)
            
            if current_level >= required_level:
                return self._create_result(
                    status=GateStatus.PASSED,
                    passed=True,
                    message=f"Authority validated: {current_authority} >= {self.required_authority}",
                    context=context,
                    evidence={
                        "current_authority": current_authority,
                        "required_authority": self.required_authority,
                        "sufficient": True
                    }
                )
            else:
                return self._create_result(
                    status=GateStatus.BLOCKED,
                    passed=False,
                    message=f"Insufficient authority: {current_authority} < {self.required_authority}",
                    context=context,
                    evidence={
                        "current_authority": current_authority,
                        "required_authority": self.required_authority,
                        "sufficient": False
                    }
                )
        except ValueError as e:
            return self._create_result(
                status=GateStatus.BLOCKED,
                passed=False,
                message=f"Invalid authority level: {e}",
                context=context,
                evidence={
                    "current_authority": current_authority,
                    "required_authority": self.required_authority,
                    "error": str(e)
                }
            )


class BREXGate(CNOTGate):
    """
    Validates BREX compliance.
    
    Control Condition: BREX cascade result must be ALLOW
    
    This gate integrates with the BREX Decision Engine to validate
    that all BREX rules pass before transformation proceeds.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(
            gate_id="BREX-CASCADE",
            gate_name="BREX Gate",
            config=config
        )
        self.cascade_all = config.get("cascade_all", True) if config else True
    
    def execute(self, context: Dict[str, Any]) -> GateResult:
        """Execute BREX validation."""
        logger.debug(f"Executing BREXGate: {self.gate_id}")
        
        # Extract BREX result from context
        brex_result = context.get("brex_result")
        if not brex_result:
            return self._create_result(
                status=GateStatus.BLOCKED,
                passed=False,
                message="No BREX result found in context",
                context=context,
                evidence={"required_field": "brex_result"}
            )
        
        # Check BREX cascade success
        success = brex_result.get("success", False)
        final_action = brex_result.get("final_action", "UNDEFINED")
        
        if not success or final_action not in ["ALLOW", "WARN"]:
            blocked_by = brex_result.get("blocked_by", "Unknown")
            return self._create_result(
                status=GateStatus.BLOCKED,
                passed=False,
                message=f"BREX validation failed: blocked by {blocked_by}",
                context=context,
                evidence={
                    "success": success,
                    "final_action": final_action,
                    "blocked_by": blocked_by,
                    "brex_result": brex_result
                }
            )
        
        # Check for escalations
        if brex_result.get("escalation_required", False):
            escalation_rules = brex_result.get("escalation_rules", [])
            return self._create_result(
                status=GateStatus.ESCALATE,
                passed=False,
                message=f"BREX escalation required: {escalation_rules}",
                context=context,
                evidence={
                    "escalation_required": True,
                    "escalation_rules": escalation_rules,
                    "brex_result": brex_result
                }
            )
        
        return self._create_result(
            status=GateStatus.PASSED,
            passed=True,
            message=f"BREX validation passed: {final_action}",
            context=context,
            evidence={
                "success": success,
                "final_action": final_action,
                "brex_result": brex_result
            }
        )


class TraceGate(CNOTGate):
    """
    Validates traceability completeness.
    
    Control Condition: Trace coverage must meet threshold
    
    This gate ensures that all required traceability links exist
    and coverage meets the specified threshold.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(
            gate_id="TRACE-COVERAGE",
            gate_name="Trace Gate",
            config=config
        )
        self.coverage_threshold = config.get("coverage_threshold", 100) if config else 100
    
    def execute(self, context: Dict[str, Any]) -> GateResult:
        """Execute trace validation."""
        logger.debug(f"Executing TraceGate: {self.gate_id}")
        
        # Extract trace data from context
        trace_data = context.get("trace_data")
        if not trace_data:
            return self._create_result(
                status=GateStatus.BLOCKED,
                passed=False,
                message="No trace data found in context",
                context=context,
                evidence={"required_field": "trace_data"}
            )
        
        # Calculate coverage
        total_required = trace_data.get("total_required", 0)
        total_linked = trace_data.get("total_linked", 0)
        
        if total_required == 0:
            coverage = 100.0
        else:
            coverage = (total_linked / total_required) * 100
        
        if coverage < self.coverage_threshold:
            return self._create_result(
                status=GateStatus.BLOCKED,
                passed=False,
                message=f"Trace coverage {coverage:.1f}% < threshold {self.coverage_threshold}%",
                context=context,
                evidence={
                    "coverage": coverage,
                    "threshold": self.coverage_threshold,
                    "total_required": total_required,
                    "total_linked": total_linked,
                    "missing": total_required - total_linked
                }
            )
        
        return self._create_result(
            status=GateStatus.PASSED,
            passed=True,
            message=f"Trace coverage {coverage:.1f}% >= threshold {self.coverage_threshold}%",
            context=context,
            evidence={
                "coverage": coverage,
                "threshold": self.coverage_threshold,
                "total_required": total_required,
                "total_linked": total_linked
            }
        )


class SafetyGate(CNOTGate):
    """
    Escalates safety-critical operations.
    
    Control Condition: Safety impact check - escalates if safety-critical
    
    This gate identifies safety-critical operations and escalates them
    for human approval before proceeding.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(
            gate_id="SAFETY-CHECK",
            gate_name="Safety Gate",
            config=config
        )
        self.escalation_target = config.get("escalation_target", "STK_SAF") if config else "STK_SAF"
    
    def execute(self, context: Dict[str, Any]) -> GateResult:
        """Execute safety check."""
        logger.debug(f"Executing SafetyGate: {self.gate_id}")
        
        # Extract safety impact from context
        safety_impact = context.get("safety_impact")
        if not safety_impact:
            # No safety impact declared - pass by default
            return self._create_result(
                status=GateStatus.PASSED,
                passed=True,
                message="No safety impact declared",
                context=context,
                evidence={"safety_impact": None}
            )
        
        # Check if safety-critical
        is_safety_critical = safety_impact.get("is_safety_critical", False)
        safety_level = safety_impact.get("safety_level", "NONE")
        
        if is_safety_critical or safety_level in ["CATASTROPHIC", "HAZARDOUS", "MAJOR"]:
            return self._create_result(
                status=GateStatus.ESCALATE,
                passed=False,
                message=f"Safety-critical operation requires approval from {self.escalation_target}",
                context=context,
                evidence={
                    "is_safety_critical": is_safety_critical,
                    "safety_level": safety_level,
                    "escalation_target": self.escalation_target,
                    "safety_impact": safety_impact
                }
            )
        
        return self._create_result(
            status=GateStatus.PASSED,
            passed=True,
            message=f"Non-safety-critical operation: {safety_level}",
            context=context,
            evidence={
                "is_safety_critical": is_safety_critical,
                "safety_level": safety_level,
                "safety_impact": safety_impact
            }
        )


class HITLGate(CNOTGate):
    """
    Human-in-the-loop checkpoint.
    
    Control Condition: Non-inference boundary - requires human decision
    
    From README.md Section 6 & 7:
        "Non-Inference Boundary: A formally defined execution boundary where
        automation terminates because ambiguity cannot be resolved deterministically."
        
        "Human-in-the-Loop (HITL): An explicit, auditable human decision point
        invoked at predefined non-inference boundaries."
    
    This gate marks a non-inference boundary where human decision is required.
    """
    
    def __init__(self, checkpoint_id: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(
            gate_id=f"HITL-{checkpoint_id}",
            gate_name="Human-in-the-Loop Gate",
            config=config
        )
        self.checkpoint_id = checkpoint_id
        self.decision_type = config.get("decision_type", "APPROVAL") if config else "APPROVAL"
    
    def execute(self, context: Dict[str, Any]) -> GateResult:
        """Execute HITL checkpoint."""
        logger.debug(f"Executing HITLGate: {self.gate_id}")
        
        # Check if human decision has been made
        hitl_decision = context.get("hitl_decision")
        if not hitl_decision:
            # No decision yet - escalate for human input
            return self._create_result(
                status=GateStatus.ESCALATE,
                passed=False,
                message=f"Human decision required at checkpoint: {self.checkpoint_id}",
                context=context,
                evidence={
                    "checkpoint_id": self.checkpoint_id,
                    "decision_type": self.decision_type,
                    "awaiting_decision": True
                }
            )
        
        # Check decision result
        decision = hitl_decision.get("decision", "")
        if decision not in ["APPROVED", "PROCEED"]:
            return self._create_result(
                status=GateStatus.BLOCKED,
                passed=False,
                message=f"Human decision: {decision}",
                context=context,
                evidence={
                    "checkpoint_id": self.checkpoint_id,
                    "decision": decision,
                    "hitl_decision": hitl_decision
                }
            )
        
        return self._create_result(
            status=GateStatus.PASSED,
            passed=True,
            message=f"Human decision: {decision}",
            context=context,
            evidence={
                "checkpoint_id": self.checkpoint_id,
                "decision": decision,
                "hitl_decision": hitl_decision
            }
        )
