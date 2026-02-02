# =============================================================================
# BREX Decision Engine
# Guided Reasoning Through BREX Logic Decision Points
# Version: 2.0.0
# =============================================================================
"""
BREX Decision Engine

Implements deterministic, cascading decision trees based on BREX rules.
The AEROSPACEMODEL Agent's reasoning is constrained, guided, and explainable
through this BREX ruleset. Every step is a validated decision node.

Key Principles:
    - No free-form autonomy exists
    - Every path is finite
    - No branching without rules
    - No generative freedom outside defined rule branches
    - All decisions logged with timestamps

Architecture:
    BREX Decision Node:
        IF <condition> AND <authority> AND <baseline> THEN <permitted_action>
        ELSE <deterministic failure mode>

Compliance:
    - S1000D Issue 4.x / 5.0 BREX semantics
    - ASIT governance
    - DO-178C traceability
    - Deterministic replay capability
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
import yaml
import json

logger = logging.getLogger(__name__)


# =============================================================================
# ENUMERATIONS
# =============================================================================

class BREXDecisionAction(Enum):
    """Actions that can be taken based on BREX decision evaluation."""
    ALLOW = "allow"           # Permitted - proceed with execution
    BLOCK = "block"           # Prohibited - stop execution
    ESCALATE = "escalate"     # Requires human approval
    REQUIRE = "require"       # Requires additional validation/data
    WARN = "warn"             # Proceed with warning logged
    UNDEFINED = "undefined"   # Unruled condition - halt


class BREXConditionType(Enum):
    """Types of BREX conditions for decision evaluation."""
    CONTRACT_REQUIRED = "contract_required"
    BASELINE_REQUIRED = "baseline_required"
    ATA_DOMAIN_VALID = "ata_domain_valid"
    SAFETY_IMPACT = "safety_impact"
    AUTHORITY_VALID = "authority_valid"
    LIFECYCLE_STATE_VALID = "lifecycle_state_valid"
    CONTENT_APPROVED = "content_approved"
    TRACE_COMPLETE = "trace_complete"
    BREX_COMPLIANT = "brex_compliant"
    CUSTOM = "custom"


class BREXDecisionSeverity(Enum):
    """Severity levels for BREX decision logging."""
    CRITICAL = "critical"     # Must be fixed - blocks all operations
    ERROR = "error"           # Must be fixed - blocks publication
    WARNING = "warning"       # Should be fixed - may require waiver
    INFO = "info"             # Informational - logged for audit


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class BREXCondition:
    """
    A single condition in a BREX decision rule.

    Attributes:
        condition_type: Type of condition to evaluate
        parameter: Parameter name to check
        expected_value: Expected value or pattern
        custom_validator: Optional custom validation function name
    """
    condition_type: BREXConditionType
    parameter: str
    expected_value: Optional[Any] = None
    custom_validator: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "condition_type": self.condition_type.value,
            "parameter": self.parameter,
            "expected_value": self.expected_value,
            "custom_validator": self.custom_validator,
        }


@dataclass
class BREXDecisionRule:
    """
    A BREX decision rule defining a single decision node in the cascade.

    Attributes:
        rule_id: Unique identifier (e.g., "DM-001", "STRUCT-007")
        name: Human-readable rule name
        description: Detailed description of the rule
        conditions: List of conditions to evaluate
        action_if_true: Action when all conditions pass
        action_if_false: Action when any condition fails
        escalation_target: Who to escalate to (if action is ESCALATE)
        required_authority: Required authority level to execute
        severity: Severity level of violations
        message: Message template for logging
    """
    rule_id: str
    name: str
    description: str
    conditions: List[BREXCondition]
    action_if_true: BREXDecisionAction = BREXDecisionAction.ALLOW
    action_if_false: BREXDecisionAction = BREXDecisionAction.BLOCK
    escalation_target: Optional[str] = None
    required_authority: Optional[str] = None
    severity: BREXDecisionSeverity = BREXDecisionSeverity.ERROR
    message: str = ""

    def __post_init__(self):
        if not self.message:
            self.message = f"BREX rule '{self.rule_id}' ({self.name})"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "description": self.description,
            "conditions": [c.to_dict() for c in self.conditions],
            "action_if_true": self.action_if_true.value,
            "action_if_false": self.action_if_false.value,
            "escalation_target": self.escalation_target,
            "required_authority": self.required_authority,
            "severity": self.severity.value,
            "message": self.message,
        }


@dataclass
class BREXDecisionResult:
    """
    Result of a single BREX decision evaluation.

    Attributes:
        rule_id: ID of the evaluated rule
        rule_name: Name of the evaluated rule
        action: Resulting action
        passed: Whether all conditions passed
        timestamp: When the decision was made
        context: Context data at decision time
        message: Decision message
        evidence: Evidence supporting the decision
    """
    rule_id: str
    rule_name: str
    action: BREXDecisionAction
    passed: bool
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    context: Dict[str, Any] = field(default_factory=dict)
    message: str = ""
    evidence: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "action": self.action.value,
            "passed": self.passed,
            "timestamp": self.timestamp,
            "context": self.context,
            "message": self.message,
            "evidence": self.evidence,
        }

    def to_log_entry(self) -> str:
        """Generate audit log entry format."""
        status = "OK" if self.passed else "FAILED"
        return f"{self.timestamp} | RULE {self.rule_id} | {self.rule_name} | {status} | {self.message}"


@dataclass
class BREXCascadeResult:
    """
    Result of a complete BREX decision cascade evaluation.

    Attributes:
        cascade_id: Unique identifier for this cascade run
        success: Overall success status
        final_action: Final action after all rules evaluated
        decisions: List of individual decision results
        blocked_by: Rule that blocked execution (if any)
        escalation_required: Whether human approval is needed
        escalation_rules: Rules requiring escalation
        started_at: Cascade start time
        completed_at: Cascade completion time
    """
    cascade_id: str
    success: bool = True
    final_action: BREXDecisionAction = BREXDecisionAction.ALLOW
    decisions: List[BREXDecisionResult] = field(default_factory=list)
    blocked_by: Optional[str] = None
    escalation_required: bool = False
    escalation_rules: List[str] = field(default_factory=list)
    started_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    completed_at: Optional[str] = None

    def add_decision(self, decision: BREXDecisionResult) -> None:
        """Add a decision result and update cascade status."""
        self.decisions.append(decision)

        if decision.action == BREXDecisionAction.BLOCK:
            self.success = False
            self.final_action = BREXDecisionAction.BLOCK
            if self.blocked_by is None:
                self.blocked_by = decision.rule_id

        elif decision.action == BREXDecisionAction.ESCALATE:
            self.escalation_required = True
            self.escalation_rules.append(decision.rule_id)
            if self.final_action != BREXDecisionAction.BLOCK:
                self.final_action = BREXDecisionAction.ESCALATE

        elif decision.action == BREXDecisionAction.UNDEFINED:
            self.success = False
            self.final_action = BREXDecisionAction.UNDEFINED
            if self.blocked_by is None:
                self.blocked_by = decision.rule_id

    def complete(self) -> None:
        """Mark the cascade as complete."""
        self.completed_at = datetime.utcnow().isoformat() + "Z"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "cascade_id": self.cascade_id,
            "success": self.success,
            "final_action": self.final_action.value,
            "decisions": [d.to_dict() for d in self.decisions],
            "blocked_by": self.blocked_by,
            "escalation_required": self.escalation_required,
            "escalation_rules": self.escalation_rules,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }

    def generate_audit_log(self) -> str:
        """Generate complete audit log for the cascade."""
        lines = [
            "=" * 80,
            "BREX DECISION CASCADE AUDIT LOG",
            f"Cascade ID: {self.cascade_id}",
            f"Started: {self.started_at}",
            f"Completed: {self.completed_at}",
            f"Final Action: {self.final_action.value.upper()}",
            f"Success: {self.success}",
            "=" * 80,
            "",
            "DECISION SEQUENCE:",
            "-" * 80,
        ]

        for decision in self.decisions:
            lines.append(decision.to_log_entry())

        lines.extend([
            "-" * 80,
            "",
            "SUMMARY:",
            f"  Total rules evaluated: {len(self.decisions)}",
            f"  Rules passed: {sum(1 for d in self.decisions if d.passed)}",
            f"  Rules failed: {sum(1 for d in self.decisions if not d.passed)}",
        ])

        if self.blocked_by:
            lines.append(f"  Blocked by: {self.blocked_by}")

        if self.escalation_required:
            lines.append(f"  Escalation required for: {', '.join(self.escalation_rules)}")

        lines.extend(["", "=" * 80])

        return "\n".join(lines)


# =============================================================================
# BREX DECISION ENGINE
# =============================================================================

class BREXDecisionEngine:
    """
    BREX Decision Engine - Guided Reasoning Through BREX Logic Decision Points.

    The AEROSPACEMODEL Agent's reasoning is constrained, guided, and explainable
    through this BREX ruleset. Every step is a validated decision node.
    No free-form autonomy exists.

    This creates a deterministic agent whose reasoning can be:
        - Audited
        - Replayed
        - Certified

    Attributes:
        rules: Dictionary of loaded BREX decision rules
        custom_validators: Registered custom validation functions
        cascade_history: History of cascade evaluations

    Example:
        >>> engine = BREXDecisionEngine()
        >>> engine.load_rules_from_file("ASIT/GOVERNANCE/master_brex_authority.yaml")
        >>>
        >>> context = {
        ...     "contract_id": "KITDM-CTR-LM-CSDB_ATA28",
        ...     "ata_domain": "ATA 28",
        ...     "baseline_id": "FBL-2026-Q1-003",
        ... }
        >>>
        >>> result = engine.evaluate_cascade(context)
        >>> if result.success:
        ...     print("All rules passed - execution permitted")
        ... elif result.escalation_required:
        ...     print(f"Human approval required for: {result.escalation_rules}")
        ... else:
        ...     print(f"Blocked by rule: {result.blocked_by}")
    """

    def __init__(self, rules_path: Optional[Path] = None):
        """
        Initialize the BREX Decision Engine.

        Args:
            rules_path: Optional path to BREX rules file
        """
        self.rules: Dict[str, BREXDecisionRule] = {}
        self.custom_validators: Dict[str, Callable] = {}
        self.cascade_history: List[BREXCascadeResult] = []
        self._cascade_counter = 0

        # Register built-in validators
        self._register_builtin_validators()

        # Load default rules
        self._load_default_rules()

        # Load rules from file if provided
        if rules_path:
            self.load_rules_from_file(rules_path)

        logger.info(
            f"BREXDecisionEngine initialized: rules={len(self.rules)}, "
            f"validators={len(self.custom_validators)}"
        )

    def evaluate_cascade(
        self,
        context: Dict[str, Any],
        rule_ids: Optional[List[str]] = None,
    ) -> BREXCascadeResult:
        """
        Evaluate a cascade of BREX decision rules.

        Args:
            context: Execution context containing all relevant data
            rule_ids: Optional list of specific rule IDs to evaluate
                     (if None, all rules are evaluated in order)

        Returns:
            BREXCascadeResult with complete evaluation results
        """
        self._cascade_counter += 1
        cascade_id = f"CASCADE-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}-{self._cascade_counter:04d}"

        result = BREXCascadeResult(cascade_id=cascade_id)

        # Determine which rules to evaluate
        rules_to_evaluate = (
            [self.rules[rid] for rid in rule_ids if rid in self.rules]
            if rule_ids
            else list(self.rules.values())
        )

        logger.info(f"Starting BREX cascade {cascade_id}: {len(rules_to_evaluate)} rules")

        for rule in rules_to_evaluate:
            decision = self._evaluate_rule(rule, context)
            result.add_decision(decision)

            # Log the decision
            logger.info(decision.to_log_entry())

            # Stop cascade on BLOCK or UNDEFINED
            if decision.action in (BREXDecisionAction.BLOCK, BREXDecisionAction.UNDEFINED):
                logger.warning(f"Cascade {cascade_id} blocked by rule {rule.rule_id}")
                break

        result.complete()
        self.cascade_history.append(result)

        logger.info(
            f"Cascade {cascade_id} complete: success={result.success}, "
            f"action={result.final_action.value}"
        )

        return result

    def evaluate_single_rule(
        self,
        rule_id: str,
        context: Dict[str, Any],
    ) -> BREXDecisionResult:
        """
        Evaluate a single BREX decision rule.

        Args:
            rule_id: ID of the rule to evaluate
            context: Execution context

        Returns:
            BREXDecisionResult for the evaluated rule

        Raises:
            KeyError: If rule_id is not found
        """
        if rule_id not in self.rules:
            raise KeyError(f"BREX rule not found: {rule_id}")

        rule = self.rules[rule_id]
        return self._evaluate_rule(rule, context)

    def add_rule(self, rule: BREXDecisionRule) -> None:
        """Add a BREX decision rule to the engine."""
        self.rules[rule.rule_id] = rule
        logger.debug(f"Added BREX decision rule: {rule.rule_id}")

    def remove_rule(self, rule_id: str) -> bool:
        """Remove a BREX decision rule by ID."""
        if rule_id in self.rules:
            del self.rules[rule_id]
            return True
        return False

    def get_rule(self, rule_id: str) -> Optional[BREXDecisionRule]:
        """Get a rule by ID."""
        return self.rules.get(rule_id)

    def list_rules(self) -> List[BREXDecisionRule]:
        """List all loaded rules."""
        return list(self.rules.values())

    def register_validator(
        self,
        name: str,
        validator: Callable[[Dict[str, Any], BREXCondition], bool],
    ) -> None:
        """
        Register a custom validator function.

        Args:
            name: Validator name (referenced in rules)
            validator: Function taking (context, condition) and returning bool
        """
        self.custom_validators[name] = validator
        logger.debug(f"Registered custom validator: {name}")

    def load_rules_from_file(self, path: Path) -> int:
        """
        Load BREX decision rules from a YAML file.

        Args:
            path: Path to YAML file

        Returns:
            Number of rules loaded
        """
        path = Path(path)
        if not path.exists():
            logger.warning(f"BREX rules file not found: {path}")
            return 0

        with open(path, "r") as f:
            data = yaml.safe_load(f)

        count = 0
        rules_data = data.get("brex_decision_rules", data.get("rules", []))

        for rule_data in rules_data:
            try:
                rule = self._parse_rule(rule_data)
                self.add_rule(rule)
                count += 1
            except (KeyError, ValueError, TypeError) as e:
                logger.error(f"Failed to parse BREX rule: {e}")

        logger.info(f"Loaded {count} BREX decision rules from {path}")
        return count

    def export_rules_to_file(self, path: Path) -> None:
        """Export all rules to a YAML file."""
        data = {
            "brex_decision_rules": [rule.to_dict() for rule in self.rules.values()]
        }
        with open(path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    def get_cascade_history(self, limit: int = 100) -> List[BREXCascadeResult]:
        """Get recent cascade evaluation history."""
        return self.cascade_history[-limit:]

    def clear_history(self) -> None:
        """Clear cascade history."""
        self.cascade_history.clear()

    def _evaluate_rule(
        self,
        rule: BREXDecisionRule,
        context: Dict[str, Any],
    ) -> BREXDecisionResult:
        """Evaluate a single rule against context."""
        all_conditions_pass = True
        evidence = {}

        for condition in rule.conditions:
            passed, condition_evidence = self._evaluate_condition(condition, context)
            evidence[condition.parameter] = condition_evidence

            if not passed:
                all_conditions_pass = False
                break

        # Determine action
        if all_conditions_pass:
            action = rule.action_if_true
            message = f"{rule.message} | conditions satisfied"
        else:
            action = rule.action_if_false
            message = f"{rule.message} | conditions not satisfied"

        return BREXDecisionResult(
            rule_id=rule.rule_id,
            rule_name=rule.name,
            action=action,
            passed=all_conditions_pass,
            context=context.copy(),
            message=message,
            evidence=evidence,
        )

    def _evaluate_condition(
        self,
        condition: BREXCondition,
        context: Dict[str, Any],
    ) -> Tuple[bool, Dict[str, Any]]:
        """Evaluate a single condition against context."""
        evidence = {
            "condition_type": condition.condition_type.value,
            "parameter": condition.parameter,
            "expected": condition.expected_value,
        }

        # Use custom validator if specified
        if condition.custom_validator and condition.custom_validator in self.custom_validators:
            validator = self.custom_validators[condition.custom_validator]
            try:
                passed = validator(context, condition)
                evidence["validator"] = condition.custom_validator
                evidence["passed"] = passed
                return passed, evidence
            except (KeyError, ValueError, TypeError, AttributeError) as e:
                logger.error(f"Custom validator '{condition.custom_validator}' failed: {e}")
                evidence["error"] = str(e)
                return False, evidence

        # Built-in condition evaluation
        actual_value = context.get(condition.parameter)
        evidence["actual"] = actual_value

        if condition.condition_type == BREXConditionType.CONTRACT_REQUIRED:
            passed = actual_value is not None and actual_value != ""

        elif condition.condition_type == BREXConditionType.BASELINE_REQUIRED:
            passed = actual_value is not None and actual_value != ""

        elif condition.condition_type == BREXConditionType.ATA_DOMAIN_VALID:
            # Validate ATA domain format (e.g., "ATA 27", "ATA 28")
            if isinstance(actual_value, str) and actual_value:
                passed = actual_value.upper().startswith("ATA")
            else:
                passed = False

        elif condition.condition_type == BREXConditionType.SAFETY_IMPACT:
            # Check if safety impact is flagged
            passed = actual_value in (True, "true", "yes", 1)

        elif condition.condition_type == BREXConditionType.AUTHORITY_VALID:
            # Check authority level
            if condition.expected_value:
                passed = actual_value == condition.expected_value
            else:
                passed = actual_value is not None

        elif condition.condition_type == BREXConditionType.LIFECYCLE_STATE_VALID:
            # Valid lifecycle states
            valid_states = ["LC01", "LC02", "LC03", "LC04", "LC05", "LC06",
                           "LC07", "LC08", "LC09", "LC10", "LC11", "LC12",
                           "LC13", "LC14"]
            if condition.expected_value:
                valid_states = [condition.expected_value] if isinstance(
                    condition.expected_value, str
                ) else condition.expected_value
            passed = actual_value in valid_states

        elif condition.condition_type == BREXConditionType.CONTENT_APPROVED:
            passed = actual_value in (True, "APPROVED", "approved")

        elif condition.condition_type == BREXConditionType.TRACE_COMPLETE:
            # Expect trace coverage percentage
            if isinstance(actual_value, (int, float)):
                threshold = condition.expected_value or 100
                passed = actual_value >= threshold
            else:
                passed = actual_value in (True, "complete", "COMPLETE")

        elif condition.condition_type == BREXConditionType.BREX_COMPLIANT:
            passed = actual_value in (True, "PASS", "pass", "compliant")

        else:
            # Default: check if value matches expected
            if condition.expected_value is not None:
                passed = actual_value == condition.expected_value
            else:
                passed = actual_value is not None

        evidence["passed"] = passed
        return passed, evidence

    def _register_builtin_validators(self) -> None:
        """Register built-in custom validators."""

        def validate_contract_status(context: Dict[str, Any], condition: BREXCondition) -> bool:
            """Validate contract is in APPROVED status."""
            status = context.get("contract_status", "")
            return status.upper() == "APPROVED"

        def validate_baseline_established(context: Dict[str, Any], condition: BREXCondition) -> bool:
            """Validate baseline is ESTABLISHED."""
            status = context.get("baseline_status", "")
            return status.upper() == "ESTABLISHED"

        def validate_ccb_approval(context: Dict[str, Any], condition: BREXCondition) -> bool:
            """Validate CCB approval exists."""
            ccb_ref = context.get("ccb_reference")
            return ccb_ref is not None and ccb_ref != ""

        def validate_ata_chapter_scope(context: Dict[str, Any], condition: BREXCondition) -> bool:
            """Validate ATA chapter is within contract scope."""
            ata_chapter = context.get("ata_chapter")
            allowed_chapters = context.get("contract_ata_chapters", [])
            return ata_chapter in allowed_chapters

        self.register_validator("validate_contract_status", validate_contract_status)
        self.register_validator("validate_baseline_established", validate_baseline_established)
        self.register_validator("validate_ccb_approval", validate_ccb_approval)
        self.register_validator("validate_ata_chapter_scope", validate_ata_chapter_scope)

    def _load_default_rules(self) -> None:
        """Load default BREX decision rules."""
        default_rules = [
            # DM-001: Contract Required
            BREXDecisionRule(
                rule_id="DM-001",
                name="Contract Required",
                description="Content generation requires valid ASIT contract",
                conditions=[
                    BREXCondition(
                        condition_type=BREXConditionType.CONTRACT_REQUIRED,
                        parameter="contract_id",
                    ),
                    BREXCondition(
                        condition_type=BREXConditionType.CUSTOM,
                        parameter="contract_status",
                        custom_validator="validate_contract_status",
                    ),
                ],
                action_if_true=BREXDecisionAction.ALLOW,
                action_if_false=BREXDecisionAction.BLOCK,
                severity=BREXDecisionSeverity.CRITICAL,
                message="ASIT contract validation",
            ),

            # DM-002: Baseline Required
            BREXDecisionRule(
                rule_id="DM-002",
                name="Baseline Required",
                description="Content generation requires established baseline",
                conditions=[
                    BREXCondition(
                        condition_type=BREXConditionType.BASELINE_REQUIRED,
                        parameter="baseline_id",
                    ),
                    BREXCondition(
                        condition_type=BREXConditionType.CUSTOM,
                        parameter="baseline_status",
                        custom_validator="validate_baseline_established",
                    ),
                ],
                action_if_true=BREXDecisionAction.ALLOW,
                action_if_false=BREXDecisionAction.BLOCK,
                severity=BREXDecisionSeverity.CRITICAL,
                message="Baseline validation",
            ),

            # STRUCT-007: ATA Domain Valid
            BREXDecisionRule(
                rule_id="STRUCT-007",
                name="ATA Domain Valid",
                description="ATA domain must be valid and within scope",
                conditions=[
                    BREXCondition(
                        condition_type=BREXConditionType.ATA_DOMAIN_VALID,
                        parameter="ata_domain",
                    ),
                ],
                action_if_true=BREXDecisionAction.ALLOW,
                action_if_false=BREXDecisionAction.BLOCK,
                severity=BREXDecisionSeverity.ERROR,
                message="ATA domain validation",
            ),

            # SAFETY-002: Safety Impact Check
            BREXDecisionRule(
                rule_id="SAFETY-002",
                name="Safety Impact Check",
                description="Safety-impacting changes require human approval",
                conditions=[
                    BREXCondition(
                        condition_type=BREXConditionType.SAFETY_IMPACT,
                        parameter="safety_impact",
                    ),
                ],
                action_if_true=BREXDecisionAction.ESCALATE,
                action_if_false=BREXDecisionAction.ALLOW,
                escalation_target="STK_SAF",
                severity=BREXDecisionSeverity.CRITICAL,
                message="Safety impact assessment",
            ),

            # AUTHOR-002: Authority Validation
            BREXDecisionRule(
                rule_id="AUTHOR-002",
                name="Authority Validation",
                description="Content generation requires ASIT-approved contract authority",
                conditions=[
                    BREXCondition(
                        condition_type=BREXConditionType.AUTHORITY_VALID,
                        parameter="authority",
                    ),
                ],
                action_if_true=BREXDecisionAction.ALLOW,
                action_if_false=BREXDecisionAction.BLOCK,
                required_authority="ASIT",
                severity=BREXDecisionSeverity.ERROR,
                message="Authority validation",
            ),

            # TRACE-001: Traceability Requirement
            BREXDecisionRule(
                rule_id="TRACE-001",
                name="Traceability Requirement",
                description="Output must maintain 100% trace coverage",
                conditions=[
                    BREXCondition(
                        condition_type=BREXConditionType.TRACE_COMPLETE,
                        parameter="trace_coverage",
                        expected_value=100,
                    ),
                ],
                action_if_true=BREXDecisionAction.ALLOW,
                action_if_false=BREXDecisionAction.WARN,
                severity=BREXDecisionSeverity.WARNING,
                message="Trace coverage validation",
            ),

            # BREX-001: BREX Compliance
            BREXDecisionRule(
                rule_id="BREX-001",
                name="BREX Compliance",
                description="Content must pass BREX validation",
                conditions=[
                    BREXCondition(
                        condition_type=BREXConditionType.BREX_COMPLIANT,
                        parameter="brex_status",
                    ),
                ],
                action_if_true=BREXDecisionAction.ALLOW,
                action_if_false=BREXDecisionAction.BLOCK,
                severity=BREXDecisionSeverity.ERROR,
                message="BREX compliance validation",
            ),
        ]

        for rule in default_rules:
            self.rules[rule.rule_id] = rule

    def _parse_rule(self, data: Dict[str, Any]) -> BREXDecisionRule:
        """Parse a rule from dictionary data."""
        conditions = []
        for cond_data in data.get("conditions", []):
            conditions.append(BREXCondition(
                condition_type=BREXConditionType(cond_data.get("condition_type", "custom")),
                parameter=cond_data.get("parameter", ""),
                expected_value=cond_data.get("expected_value"),
                custom_validator=cond_data.get("custom_validator"),
            ))

        return BREXDecisionRule(
            rule_id=data.get("rule_id", data.get("id", "UNKNOWN")),
            name=data.get("name", ""),
            description=data.get("description", ""),
            conditions=conditions,
            action_if_true=BREXDecisionAction(data.get("action_if_true", "allow")),
            action_if_false=BREXDecisionAction(data.get("action_if_false", "block")),
            escalation_target=data.get("escalation_target"),
            required_authority=data.get("required_authority"),
            severity=BREXDecisionSeverity(data.get("severity", "error")),
            message=data.get("message", ""),
        )


# =============================================================================
# AUDITABLE EXPLAINABILITY LOG
# =============================================================================

class BREXAuditLog:
    """
    Auditable Explainability Log for BREX Decision Cascade.

    Provides:
        - Deterministic replay capability
        - Evidence generation (DO-178C traceability)
        - Certification outputs
        - Timestamped decision records
    """

    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize the audit log.

        Args:
            output_dir: Directory for log files (default: current directory)
        """
        self.output_dir = Path(output_dir) if output_dir else Path(".")
        self.entries: List[Dict[str, Any]] = []

    def log_cascade(self, result: BREXCascadeResult) -> None:
        """Log a complete cascade result."""
        entry = {
            "type": "cascade",
            "cascade_id": result.cascade_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "result": result.to_dict(),
        }
        self.entries.append(entry)

    def log_decision(self, decision: BREXDecisionResult) -> None:
        """Log a single decision."""
        entry = {
            "type": "decision",
            "timestamp": decision.timestamp,
            "rule_id": decision.rule_id,
            "rule_name": decision.rule_name,
            "action": decision.action.value,
            "passed": decision.passed,
            "message": decision.message,
            "evidence": decision.evidence,
        }
        self.entries.append(entry)

    def export_to_file(self, filename: str = "brex_audit_log.json") -> Path:
        """Export log to JSON file."""
        path = self.output_dir / filename
        with open(path, "w") as f:
            json.dump(self.entries, f, indent=2, default=str)
        return path

    def export_to_csv(self, filename: str = "brex_audit_log.csv") -> Path:
        """Export log to CSV file."""
        import csv
        path = self.output_dir / filename

        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp", "type", "rule_id", "rule_name",
                "action", "passed", "message"
            ])

            for entry in self.entries:
                if entry["type"] == "decision":
                    writer.writerow([
                        entry.get("timestamp", ""),
                        entry.get("type", ""),
                        entry.get("rule_id", ""),
                        entry.get("rule_name", ""),
                        entry.get("action", ""),
                        entry.get("passed", ""),
                        entry.get("message", ""),
                    ])

        return path

    def generate_certification_report(self) -> str:
        """Generate a certification-ready report."""
        lines = [
            "=" * 80,
            "BREX DECISION ENGINE - CERTIFICATION REPORT",
            f"Generated: {datetime.utcnow().isoformat()}Z",
            "=" * 80,
            "",
            "COMPLIANCE STATEMENT:",
            "  This report documents all BREX decision cascade evaluations",
            "  performed by the AEROSPACEMODEL system. All decisions are:",
            "    - Deterministic (same inputs produce same outputs)",
            "    - Traceable (linked to BREX rules)",
            "    - Auditable (timestamped and logged)",
            "",
            "-" * 80,
            "DECISION SUMMARY:",
            "",
        ]

        # Group by cascade
        cascades = [e for e in self.entries if e["type"] == "cascade"]
        for cascade in cascades:
            result = cascade["result"]
            lines.extend([
                f"Cascade: {result['cascade_id']}",
                f"  Started: {result['started_at']}",
                f"  Completed: {result['completed_at']}",
                f"  Final Action: {result['final_action']}",
                f"  Success: {result['success']}",
                f"  Rules Evaluated: {len(result['decisions'])}",
                "",
            ])

        lines.extend([
            "-" * 80,
            "TRACEABILITY MATRIX:",
            "",
            "Rule ID          | Name                      | Result | Timestamp",
            "-" * 80,
        ])

        decisions = [e for e in self.entries if e["type"] == "decision"]
        for decision in decisions:
            lines.append(
                f"{decision['rule_id']:<16} | "
                f"{decision['rule_name'][:25]:<25} | "
                f"{'PASS' if decision['passed'] else 'FAIL':<6} | "
                f"{decision['timestamp']}"
            )

        lines.extend(["", "=" * 80])
        return "\n".join(lines)

    def clear(self) -> None:
        """Clear all log entries."""
        self.entries.clear()


# =============================================================================
# FACTORY FUNCTION
# =============================================================================

def create_brex_engine(
    rules_path: Optional[Path] = None,
    with_audit_log: bool = True,
    audit_output_dir: Optional[Path] = None,
) -> Tuple[BREXDecisionEngine, Optional[BREXAuditLog]]:
    """
    Factory function to create a BREX Decision Engine with optional audit log.

    Args:
        rules_path: Path to BREX rules YAML file
        with_audit_log: Whether to create an audit log
        audit_output_dir: Directory for audit log output

    Returns:
        Tuple of (BREXDecisionEngine, BREXAuditLog or None)
    """
    engine = BREXDecisionEngine(rules_path)

    audit_log = None
    if with_audit_log:
        audit_log = BREXAuditLog(audit_output_dir)

    return engine, audit_log
