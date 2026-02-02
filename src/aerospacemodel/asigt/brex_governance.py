# =============================================================================
# BREX Decision-Driven Validation Integration
# Integrates BREX Decision Engine with ASIGT Validators
# Version: 2.0.0
# =============================================================================
"""
BREX Decision-Driven Validation

This module integrates the BREX Decision Engine with ASIGT validators to provide
guided reasoning through BREX logic decision points. The AEROSPACEMODEL Agent's
reasoning is constrained, guided, and explainable through this integration.

Key Components:
    - BREXGovernedValidator: Validates operations against BREX decision cascade
    - OperationContext: Context for governed operations
    - GovernedValidationResult: Result including decision cascade

Usage:
    >>> from aerospacemodel.asigt.brex_governance import BREXGovernedValidator
    >>> 
    >>> validator = BREXGovernedValidator(
    ...     contract_id="KITDM-CTR-LM-CSDB_ATA28",
    ...     baseline_id="FBL-2026-Q1-003"
    ... )
    >>> 
    >>> result = validator.validate_operation(
    ...     operation="generate_dm",
    ...     context={"ata_domain": "ATA 28"}
    ... )
    >>> 
    >>> if result.allowed:
    ...     # Proceed with operation
    ...     pass
    ... elif result.escalation_required:
    ...     # Wait for human approval
    ...     print(f"Escalation to: {result.escalation_target}")
    ... else:
    ...     # Operation blocked
    ...     print(f"Blocked by: {result.blocked_by}")
"""

from __future__ import annotations

import logging
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Import BREX Decision Engine from ASIGT brex module
# Note: This assumes the ASIGT/brex directory is accessible
_BREX_ENGINE_AVAILABLE = False
BREXDecisionEngine = None
BREXDecisionAction = None
BREXCascadeResult = None
BREXAuditLog = None
create_brex_engine = None

try:
    # Try to import from the ASIGT/brex directory
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "ASIGT" / "brex"))
    from brex_decision_engine import (
        BREXDecisionEngine,
        BREXDecisionAction,
        BREXCascadeResult,
        BREXAuditLog,
        create_brex_engine,
    )
    _BREX_ENGINE_AVAILABLE = True
except (ImportError, ModuleNotFoundError) as e:
    # Fallback if direct import fails - use None placeholders
    import warnings
    warnings.warn(
        f"BREX Decision Engine not available: {e}. "
        "Falling back to basic validation mode.",
        RuntimeWarning,
        stacklevel=2,
    )


logger = logging.getLogger(__name__)


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class OperationContext:
    """
    Context for a governed operation.

    Contains all information needed to evaluate BREX decision rules
    for a specific operation.
    """
    # Contract identification
    contract_id: str
    contract_status: str = "APPROVED"
    contract_version: str = "1.0.0"

    # Baseline identification
    baseline_id: str = ""
    baseline_status: str = "ESTABLISHED"

    # ATA domain
    ata_domain: str = ""
    ata_chapter: str = ""

    # Authority
    authority: str = "ASIT"
    invoker: str = ""

    # Safety
    safety_impact: bool = False
    safety_classification: str = ""

    # Lifecycle
    lifecycle_state: str = ""

    # Traceability
    trace_coverage: float = 100.0

    # BREX/Schema
    brex_status: str = "PASS"
    schema_status: str = "PASS"

    # Additional context
    additional_context: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for BREX evaluation."""
        ctx = {
            "contract_id": self.contract_id,
            "contract_status": self.contract_status,
            "contract_version": self.contract_version,
            "baseline_id": self.baseline_id,
            "baseline_status": self.baseline_status,
            "ata_domain": self.ata_domain,
            "ata_chapter": self.ata_chapter,
            "authority": self.authority,
            "invoker": self.invoker,
            "safety_impact": self.safety_impact,
            "safety_classification": self.safety_classification,
            "lifecycle_state": self.lifecycle_state,
            "trace_coverage": self.trace_coverage,
            "brex_status": self.brex_status,
            "schema_status": self.schema_status,
        }
        ctx.update(self.additional_context)
        return ctx


@dataclass
class GovernedValidationResult:
    """
    Result of a governed validation operation.

    Includes both the BREX decision cascade result and
    any additional validation results.
    """
    # Operation identification
    operation: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    # Decision result
    allowed: bool = False
    action: str = "block"

    # Escalation
    escalation_required: bool = False
    escalation_target: Optional[str] = None
    escalation_rules: List[str] = field(default_factory=list)

    # Blocking
    blocked_by: Optional[str] = None

    # Cascade details
    cascade_id: Optional[str] = None
    rules_evaluated: int = 0
    rules_passed: int = 0
    rules_failed: int = 0

    # Audit log
    audit_log: List[str] = field(default_factory=list)

    # Additional data
    context: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "operation": self.operation,
            "timestamp": self.timestamp,
            "allowed": self.allowed,
            "action": self.action,
            "escalation_required": self.escalation_required,
            "escalation_target": self.escalation_target,
            "escalation_rules": self.escalation_rules,
            "blocked_by": self.blocked_by,
            "cascade_id": self.cascade_id,
            "rules_evaluated": self.rules_evaluated,
            "rules_passed": self.rules_passed,
            "rules_failed": self.rules_failed,
            "audit_log": self.audit_log,
            "context": self.context,
        }


# =============================================================================
# OPERATION DEFINITIONS
# =============================================================================

# Map of operations to required BREX rules
OPERATION_RULES = {
    "generate_dm": ["CTR-001", "BL-001", "STRUCT-001", "AUTHOR-002"],
    "produce_publication": ["CTR-001", "STRUCT-001", "BREX-001", "LC-001"],
    "transform_content": ["CTR-001", "PIPELINE-004", "TRACE-001"],
    "modify_baseline": ["CTR-001", "BL-002", "AUTHOR-003"],
    "publish_content": ["CTR-001", "BREX-001", "LC-001", "SAFETY-002"],
    "validate_safety": ["CTR-001", "SAFETY-002", "SAFETY-001"],
    "create_trace": ["CTR-001", "TRACE-001"],
}


# =============================================================================
# BREX GOVERNED VALIDATOR
# =============================================================================

class BREXGovernedValidator:
    """
    BREX-Governed Validator for ASIGT Operations.

    This validator ensures all ASIGT operations are governed by BREX decision
    rules. The AEROSPACEMODEL Agent's reasoning is constrained, guided, and
    explainable through this validator.

    Principles:
        - Every operation must pass BREX decision cascade
        - No free-form autonomy exists
        - All decisions are logged and auditable
        - Deterministic, reproducible validation

    Attributes:
        contract_id: ASIT contract identifier
        baseline_id: Baseline identifier
        engine: BREX Decision Engine instance
        audit_log: Audit log instance

    Example:
        >>> validator = BREXGovernedValidator(
        ...     contract_id="KITDM-CTR-LM-CSDB_ATA28",
        ...     baseline_id="FBL-2026-Q1-003"
        ... )
        >>> 
        >>> # Validate a generate_dm operation
        >>> result = validator.validate_operation(
        ...     operation="generate_dm",
        ...     context=OperationContext(
        ...         contract_id="KITDM-CTR-LM-CSDB_ATA28",
        ...         ata_domain="ATA 28"
        ...     )
        ... )
        >>> 
        >>> if result.allowed:
        ...     print("Operation permitted - proceed with generation")
        >>> else:
        ...     print(f"Operation blocked by: {result.blocked_by}")
    """

    def __init__(
        self,
        contract_id: str,
        baseline_id: str = "",
        rules_path: Optional[Path] = None,
        enable_audit: bool = True,
    ):
        """
        Initialize the BREX-Governed Validator.

        Args:
            contract_id: ASIT contract identifier (required)
            baseline_id: Baseline identifier
            rules_path: Optional path to custom BREX rules
            enable_audit: Whether to enable audit logging
        """
        self.contract_id = contract_id
        self.baseline_id = baseline_id
        self.enable_audit = enable_audit

        # Initialize BREX Decision Engine
        if BREXDecisionEngine is not None and create_brex_engine is not None:
            self.engine, self.audit_log = create_brex_engine(
                rules_path=rules_path,
                with_audit_log=enable_audit,
            )
        else:
            # Fallback to None if engine not available
            self.engine = None
            self.audit_log = None
            logger.warning("BREX Decision Engine not available - using fallback mode")

        logger.info(
            f"BREXGovernedValidator initialized: contract={contract_id}, "
            f"baseline={baseline_id}"
        )

    def validate_operation(
        self,
        operation: str,
        context: Optional[Union[OperationContext, Dict[str, Any]]] = None,
    ) -> GovernedValidationResult:
        """
        Validate an operation against BREX decision rules.

        Args:
            operation: Operation name (e.g., "generate_dm", "publish_content")
            context: Operation context (OperationContext or dict)

        Returns:
            GovernedValidationResult with decision details
        """
        # Build context
        if isinstance(context, OperationContext):
            ctx_dict = context.to_dict()
        elif isinstance(context, dict):
            ctx_dict = context.copy()
        else:
            ctx_dict = {}

        # Add defaults
        ctx_dict.setdefault("contract_id", self.contract_id)
        ctx_dict.setdefault("baseline_id", self.baseline_id)
        ctx_dict.setdefault("contract_status", "APPROVED")
        ctx_dict.setdefault("baseline_status", "ESTABLISHED")
        ctx_dict.setdefault("authority", "ASIT")

        # Check if engine is available
        if self.engine is None or BREXDecisionAction is None:
            # Fallback: basic validation without decision engine
            return self._fallback_validate(operation, ctx_dict)

        # Get rules for this operation
        rule_ids = OPERATION_RULES.get(operation, None)

        # Evaluate BREX cascade
        cascade_result = self.engine.evaluate_cascade(ctx_dict, rule_ids)

        # Log to audit
        if self.audit_log is not None:
            self.audit_log.log_cascade(cascade_result)

        # Determine if operation is allowed
        allowed_actions = (BREXDecisionAction.ALLOW, BREXDecisionAction.WARN)
        is_allowed = cascade_result.success and cascade_result.final_action in allowed_actions

        # Build result
        result = GovernedValidationResult(
            operation=operation,
            allowed=is_allowed,
            action=cascade_result.final_action.value,
            escalation_required=cascade_result.escalation_required,
            escalation_target=self._get_escalation_target(cascade_result),
            escalation_rules=cascade_result.escalation_rules,
            blocked_by=cascade_result.blocked_by,
            cascade_id=cascade_result.cascade_id,
            rules_evaluated=len(cascade_result.decisions),
            rules_passed=sum(1 for d in cascade_result.decisions if d.passed),
            rules_failed=sum(1 for d in cascade_result.decisions if not d.passed),
            audit_log=[d.to_log_entry() for d in cascade_result.decisions],
            context=ctx_dict,
        )

        logger.info(
            f"Operation '{operation}' validated: allowed={result.allowed}, "
            f"action={result.action}"
        )

        return result

    def validate_generate_dm(
        self,
        ata_domain: str,
        safety_impact: bool = False,
        additional_context: Optional[Dict[str, Any]] = None,
    ) -> GovernedValidationResult:
        """
        Validate a Data Module generation operation.

        Args:
            ata_domain: ATA domain (e.g., "ATA 28")
            safety_impact: Whether this has safety impact
            additional_context: Additional context data

        Returns:
            GovernedValidationResult
        """
        context = OperationContext(
            contract_id=self.contract_id,
            baseline_id=self.baseline_id,
            ata_domain=ata_domain,
            safety_impact=safety_impact,
            additional_context=additional_context or {},
        )
        return self.validate_operation("generate_dm", context)

    def validate_publish(
        self,
        ata_domain: str,
        brex_status: str = "PASS",
        lifecycle_state: str = "LC10",
        safety_impact: bool = False,
    ) -> GovernedValidationResult:
        """
        Validate a content publication operation.

        Args:
            ata_domain: ATA domain
            brex_status: BREX validation status
            lifecycle_state: Current lifecycle state
            safety_impact: Whether this has safety impact

        Returns:
            GovernedValidationResult
        """
        context = OperationContext(
            contract_id=self.contract_id,
            baseline_id=self.baseline_id,
            ata_domain=ata_domain,
            brex_status=brex_status,
            lifecycle_state=lifecycle_state,
            safety_impact=safety_impact,
        )
        return self.validate_operation("publish_content", context)

    def validate_transform(
        self,
        pipeline_id: str,
        trace_coverage: float = 100.0,
    ) -> GovernedValidationResult:
        """
        Validate a content transformation operation.

        Args:
            pipeline_id: Pipeline identifier
            trace_coverage: Current trace coverage percentage

        Returns:
            GovernedValidationResult
        """
        context = OperationContext(
            contract_id=self.contract_id,
            baseline_id=self.baseline_id,
            trace_coverage=trace_coverage,
            additional_context={"pipeline_id": pipeline_id},
        )
        return self.validate_operation("transform_content", context)

    def get_audit_report(self) -> str:
        """
        Get the certification-ready audit report.

        Returns:
            Formatted audit report string
        """
        if self.audit_log is not None:
            return self.audit_log.generate_certification_report()
        return "Audit log not available"

    def export_audit_log(self, path: Path) -> Path:
        """
        Export audit log to file.

        Args:
            path: Output directory path

        Returns:
            Path to exported file
        """
        if self.audit_log is not None:
            return self.audit_log.export_to_file(str(path))
        raise RuntimeError("Audit log not available")

    def _get_escalation_target(self, cascade_result) -> Optional[str]:
        """Get the escalation target from cascade result."""
        if cascade_result is None or BREXDecisionAction is None:
            return None
            
        for decision in cascade_result.decisions:
            if decision.action == BREXDecisionAction.ESCALATE:
                # Get from rule if available
                if self.engine is not None:
                    rule = self.engine.get_rule(decision.rule_id)
                    if rule and rule.escalation_target:
                        return rule.escalation_target
        return None

    def _fallback_validate(
        self,
        operation: str,
        context: Dict[str, Any],
    ) -> GovernedValidationResult:
        """
        Fallback validation when BREX Decision Engine is not available.

        Performs basic contract and baseline checks.
        """
        allowed = True
        blocked_by = None

        # Check contract
        if not context.get("contract_id"):
            allowed = False
            blocked_by = "CTR-001"

        # Check contract status
        if context.get("contract_status") != "APPROVED":
            allowed = False
            blocked_by = blocked_by or "CTR-001"

        # Check baseline for operations that require it
        if operation in ("generate_dm", "transform_content", "publish_content"):
            if not context.get("baseline_id"):
                allowed = False
                blocked_by = blocked_by or "BL-001"

        return GovernedValidationResult(
            operation=operation,
            allowed=allowed,
            action="allow" if allowed else "block",
            blocked_by=blocked_by,
            rules_evaluated=2,
            rules_passed=2 if allowed else 0,
            rules_failed=0 if allowed else 2,
            audit_log=[
                f"{datetime.utcnow().isoformat()}Z | FALLBACK | Contract check | "
                f"{'OK' if context.get('contract_id') else 'FAILED'}",
                f"{datetime.utcnow().isoformat()}Z | FALLBACK | Baseline check | "
                f"{'OK' if context.get('baseline_id') else 'FAILED'}",
            ],
            context=context,
        )


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def validate_governed_operation(
    operation: str,
    contract_id: str,
    baseline_id: str = "",
    context: Optional[Dict[str, Any]] = None,
) -> GovernedValidationResult:
    """
    Quick validation of a governed operation.

    Args:
        operation: Operation name
        contract_id: ASIT contract identifier
        baseline_id: Baseline identifier
        context: Additional context

    Returns:
        GovernedValidationResult
    """
    validator = BREXGovernedValidator(contract_id, baseline_id)
    return validator.validate_operation(operation, context)


def is_operation_allowed(
    operation: str,
    contract_id: str,
    baseline_id: str = "",
    context: Optional[Dict[str, Any]] = None,
) -> bool:
    """
    Quick check if an operation is allowed.

    Args:
        operation: Operation name
        contract_id: ASIT contract identifier
        baseline_id: Baseline identifier
        context: Additional context

    Returns:
        True if operation is allowed
    """
    result = validate_governed_operation(operation, contract_id, baseline_id, context)
    return result.allowed


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    # Data classes
    "OperationContext",
    "GovernedValidationResult",

    # Main class
    "BREXGovernedValidator",

    # Convenience functions
    "validate_governed_operation",
    "is_operation_allowed",

    # Constants
    "OPERATION_RULES",
]
