# =============================================================================
# ASIGT BREX Validator
# S1000D Business Rules Exchange validation
# Version: 2.0.0
# =============================================================================
"""
BREX Validator

Validates S1000D Data Modules against Business Rules Exchange (BREX)
rules. BREX defines project-specific constraints on top of the base
S1000D schema, including:
- Allowed elements and attributes
- Required metadata values
- Content structure rules
- Naming conventions
- Cross-reference requirements

Operates exclusively under ASIT contract authority.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Union
from xml.etree import ElementTree as ET

logger = logging.getLogger(__name__)


class BREXSeverity(Enum):
    """BREX rule violation severity levels."""
    ERROR = "error"           # Must be fixed - blocks publication
    WARNING = "warning"       # Should be fixed - review required
    INFO = "info"            # Informational - no action required
    CAUTION = "caution"      # May cause issues in some contexts


class BREXRuleType(Enum):
    """Types of BREX rules."""
    STRUCTURE = "structure"           # Element/attribute presence
    CONTENT = "content"               # Text content validation
    ATTRIBUTE = "attribute"           # Attribute value validation
    REFERENCE = "reference"           # Cross-reference validation
    NOTATION = "notation"             # Notation/naming rules
    CONTEXT = "context"               # Context-dependent rules
    CUSTOM = "custom"                 # Custom validation logic


@dataclass
class BREXRule:
    """
    BREX rule definition.
    
    Defines a single business rule for S1000D content validation.
    """
    id: str                             # Rule identifier (e.g., "BREX-001")
    name: str                           # Human-readable name
    description: str                    # Rule description
    rule_type: BREXRuleType            # Type of rule
    severity: BREXSeverity             # Violation severity
    xpath: Optional[str] = None         # XPath expression for target
    pattern: Optional[str] = None       # Regex pattern for validation
    allowed_values: List[str] = field(default_factory=list)
    required: bool = False              # Is this a required element/attribute
    context: Optional[str] = None       # Context XPath (when rule applies)
    message: str = ""                   # Error message template
    auto_fix: bool = False              # Can be automatically fixed
    
    def __post_init__(self):
        if not self.message:
            self.message = f"BREX rule '{self.id}' violated: {self.description}"


@dataclass
class BREXViolation:
    """Record of a BREX rule violation."""
    rule_id: str
    rule_name: str
    severity: BREXSeverity
    message: str
    location: str                       # XPath to violation location
    element: Optional[str] = None       # Element name
    attribute: Optional[str] = None     # Attribute name (if applicable)
    actual_value: Optional[str] = None  # Actual value found
    expected: Optional[str] = None      # Expected value/pattern
    dm_code: Optional[str] = None       # Data Module code
    line_number: Optional[int] = None   # Line number in source
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "severity": self.severity.value,
            "message": self.message,
            "location": self.location,
            "element": self.element,
            "attribute": self.attribute,
            "actual_value": self.actual_value,
            "expected": self.expected,
            "dm_code": self.dm_code,
            "line_number": self.line_number,
        }


@dataclass
class BREXValidationResult:
    """Result of BREX validation."""
    valid: bool
    dm_code: str
    total_rules_checked: int = 0
    violations: List[BREXViolation] = field(default_factory=list)
    errors: int = 0
    warnings: int = 0
    infos: int = 0
    validated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    brex_version: str = "S1000D_5.0"
    
    def add_violation(self, violation: BREXViolation) -> None:
        """Add a violation and update counts."""
        self.violations.append(violation)
        if violation.severity == BREXSeverity.ERROR:
            self.errors += 1
            self.valid = False
        elif violation.severity == BREXSeverity.WARNING:
            self.warnings += 1
        elif violation.severity == BREXSeverity.INFO:
            self.infos += 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "valid": self.valid,
            "dm_code": self.dm_code,
            "total_rules_checked": self.total_rules_checked,
            "errors": self.errors,
            "warnings": self.warnings,
            "infos": self.infos,
            "violations": [v.to_dict() for v in self.violations],
            "validated_at": self.validated_at,
            "brex_version": self.brex_version,
        }


class BREXValidator:
    """
    S1000D BREX (Business Rules Exchange) Validator.
    
    Validates Data Modules against BREX rules defined by the project.
    Operates under ASIT contract authority with rules defined in
    the contract's validation requirements.
    
    Attributes:
        contract: ASIT transformation contract
        config: Validator configuration
        rules: Loaded BREX rules
        
    Example:
        >>> validator = BREXValidator(contract=contract, config=config)
        >>> result = validator.validate(dm_xml_content)
        >>> if not result.valid:
        ...     for v in result.violations:
        ...         print(f"{v.severity.value}: {v.message}")
    """
    
    # S1000D Issue 5.0 namespace
    S1000D_NS = {"s1000d": "http://www.s1000d.org/S1000D_5-0"}
    
    def __init__(
        self,
        contract: Dict[str, Any],
        config: Dict[str, Any],
        rules_path: Optional[Path] = None,
    ):
        """
        Initialize BREX Validator.
        
        Args:
            contract: ASIT transformation contract (required)
            config: Validator configuration
            rules_path: Path to BREX rules file
            
        Raises:
            ValueError: If contract is missing
        """
        if not contract:
            raise ValueError("ASIT contract is required for BREX validation")
        
        self.contract = contract
        self.config = config
        self.rules_path = rules_path
        
        # Contract parameters
        self.contract_id = contract.get("id", "UNKNOWN")
        self.severity_threshold = BREXSeverity(
            config.get("severity_threshold", "error").lower()
        )
        
        # Load rules
        self.rules: Dict[str, BREXRule] = {}
        self._load_default_rules()
        if rules_path:
            self._load_rules_from_file(rules_path)
        
        # Custom validators
        self._custom_validators: Dict[str, Callable] = {}
        self._register_custom_validators()
        
        # Validation statistics
        self._validation_count = 0
        self._total_violations = 0
        
        logger.info(
            f"BREXValidator initialized: contract={self.contract_id}, "
            f"rules={len(self.rules)}"
        )
    
    def validate(
        self,
        content: Union[str, ET.Element],
        dm_code: str = "UNKNOWN",
    ) -> BREXValidationResult:
        """
        Validate content against BREX rules.
        
        Args:
            content: XML content (string or ElementTree)
            dm_code: Data Module code for reporting
            
        Returns:
            BREXValidationResult with violations
        """
        self._validation_count += 1
        result = BREXValidationResult(valid=True, dm_code=dm_code)
        
        # Parse XML if string
        if isinstance(content, str):
            try:
                root = ET.fromstring(content)
            except ET.ParseError as e:
                result.valid = False
                result.add_violation(BREXViolation(
                    rule_id="BREX-XML-PARSE",
                    rule_name="XML Parse Error",
                    severity=BREXSeverity.ERROR,
                    message=f"Failed to parse XML: {e}",
                    location="/",
                    dm_code=dm_code,
                ))
                return result
        else:
            root = content
        
        # Run all applicable rules
        for rule in self.rules.values():
            violations = self._check_rule(rule, root, dm_code)
            for violation in violations:
                result.add_violation(violation)
            result.total_rules_checked += 1
        
        # Run custom validators
        for validator_name, validator_func in self._custom_validators.items():
            try:
                violations = validator_func(root, dm_code)
                for violation in violations:
                    result.add_violation(violation)
            except Exception as e:
                logger.error(f"Custom validator '{validator_name}' failed: {e}")
        
        self._total_violations += len(result.violations)
        return result
    
    def validate_batch(
        self,
        contents: List[Dict[str, Any]],
    ) -> List[BREXValidationResult]:
        """
        Validate multiple Data Modules.
        
        Args:
            contents: List of dicts with 'content' and 'dm_code' keys
            
        Returns:
            List of BREXValidationResult
        """
        results = []
        for item in contents:
            result = self.validate(
                content=item.get("content", ""),
                dm_code=item.get("dm_code", "UNKNOWN"),
            )
            results.append(result)
        return results
    
    def add_rule(self, rule: BREXRule) -> None:
        """Add a custom BREX rule."""
        self.rules[rule.id] = rule
        logger.debug(f"Added BREX rule: {rule.id}")
    
    def remove_rule(self, rule_id: str) -> bool:
        """Remove a BREX rule by ID."""
        if rule_id in self.rules:
            del self.rules[rule_id]
            return True
        return False
    
    def get_rule(self, rule_id: str) -> Optional[BREXRule]:
        """Get a rule by ID."""
        return self.rules.get(rule_id)
    
    def list_rules(
        self,
        rule_type: Optional[BREXRuleType] = None,
        severity: Optional[BREXSeverity] = None,
    ) -> List[BREXRule]:
        """List rules with optional filtering."""
        rules = list(self.rules.values())
        
        if rule_type:
            rules = [r for r in rules if r.rule_type == rule_type]
        if severity:
            rules = [r for r in rules if r.severity == severity]
        
        return rules
    
    def _load_default_rules(self) -> None:
        """Load default S1000D 5.0 BREX rules."""
        default_rules = [
            # Identification rules
            BREXRule(
                id="BREX-IDENT-001",
                name="DMC Required",
                description="Data Module must have a valid DMC",
                rule_type=BREXRuleType.STRUCTURE,
                severity=BREXSeverity.ERROR,
                xpath=".//dmCode",
                required=True,
                message="Data Module Code (dmCode) is required",
            ),
            BREXRule(
                id="BREX-IDENT-002",
                name="Issue Info Required",
                description="Data Module must have issue information",
                rule_type=BREXRuleType.STRUCTURE,
                severity=BREXSeverity.ERROR,
                xpath=".//issueInfo",
                required=True,
                message="Issue information (issueInfo) is required",
            ),
            BREXRule(
                id="BREX-IDENT-003",
                name="Language Required",
                description="Data Module must specify language",
                rule_type=BREXRuleType.STRUCTURE,
                severity=BREXSeverity.ERROR,
                xpath=".//language",
                required=True,
                message="Language specification is required",
            ),
            
            # Security rules
            BREXRule(
                id="BREX-SEC-001",
                name="Security Classification",
                description="Security classification must be valid",
                rule_type=BREXRuleType.ATTRIBUTE,
                severity=BREXSeverity.ERROR,
                xpath=".//security/@securityClassification",
                allowed_values=["01", "02", "03", "04", "05"],
                message="Invalid security classification value",
            ),
            
            # Status rules
            BREXRule(
                id="BREX-STAT-001",
                name="Issue Type Valid",
                description="Issue type must be valid",
                rule_type=BREXRuleType.ATTRIBUTE,
                severity=BREXSeverity.ERROR,
                xpath=".//@issueType",
                allowed_values=["new", "changed", "deleted", "rinstatement", "status"],
                message="Invalid issue type value",
            ),
            BREXRule(
                id="BREX-STAT-002",
                name="Quality Assurance",
                description="QA status must be specified",
                rule_type=BREXRuleType.STRUCTURE,
                severity=BREXSeverity.WARNING,
                xpath=".//qualityAssurance",
                required=True,
                message="Quality assurance status should be specified",
            ),
            
            # Content rules
            BREXRule(
                id="BREX-CONT-001",
                name="Content Section",
                description="Data Module must have content section",
                rule_type=BREXRuleType.STRUCTURE,
                severity=BREXSeverity.ERROR,
                xpath=".//content",
                required=True,
                message="Content section is required",
            ),
            BREXRule(
                id="BREX-CONT-002",
                name="Empty Para Check",
                description="Paragraphs should not be empty",
                rule_type=BREXRuleType.CONTENT,
                severity=BREXSeverity.WARNING,
                xpath=".//para",
                pattern=r".+",  # Must have content
                message="Empty paragraph found",
            ),
            
            # Reference rules
            BREXRule(
                id="BREX-REF-001",
                name="DM Reference Format",
                description="DM references must be properly formatted",
                rule_type=BREXRuleType.REFERENCE,
                severity=BREXSeverity.ERROR,
                xpath=".//dmRef//dmCode",
                required=True,
                context=".//dmRef",
                message="DM reference missing dmCode",
            ),
            BREXRule(
                id="BREX-REF-002",
                name="ICN Reference Format",
                description="Graphics must have valid ICN reference",
                rule_type=BREXRuleType.REFERENCE,
                severity=BREXSeverity.ERROR,
                xpath=".//graphic/@infoEntityIdent",
                pattern=r"^ICN-.+",
                context=".//graphic",
                message="Invalid ICN reference format",
            ),
            
            # Notation rules
            BREXRule(
                id="BREX-NOT-001",
                name="Figure ID Format",
                description="Figure IDs must follow naming convention",
                rule_type=BREXRuleType.NOTATION,
                severity=BREXSeverity.WARNING,
                xpath=".//figure/@id",
                pattern=r"^fig-\d{3}",
                message="Figure ID should follow 'fig-NNN' format",
            ),
            BREXRule(
                id="BREX-NOT-002",
                name="Step ID Format",
                description="Procedural step IDs must follow convention",
                rule_type=BREXRuleType.NOTATION,
                severity=BREXSeverity.WARNING,
                xpath=".//proceduralStep/@id",
                pattern=r"^step-\d{3}",
                message="Step ID should follow 'step-NNN' format",
            ),
            
            # Metadata rules
            BREXRule(
                id="BREX-META-001",
                name="Responsible Partner",
                description="Responsible partner company required",
                rule_type=BREXRuleType.STRUCTURE,
                severity=BREXSeverity.WARNING,
                xpath=".//responsiblePartnerCompany",
                required=True,
                message="Responsible partner company should be specified",
            ),
            BREXRule(
                id="BREX-META-002",
                name="Originator",
                description="Originator should be specified",
                rule_type=BREXRuleType.STRUCTURE,
                severity=BREXSeverity.INFO,
                xpath=".//originator",
                required=True,
                message="Originator should be specified",
            ),
        ]
        
        for rule in default_rules:
            self.rules[rule.id] = rule
    
    def _load_rules_from_file(self, path: Path) -> None:
        """Load BREX rules from YAML file."""
        # Implementation would load from YAML
        # For now, this is a placeholder
        logger.info(f"Loading BREX rules from: {path}")
    
    def _register_custom_validators(self) -> None:
        """Register custom validation functions."""
        self._custom_validators["cross_reference_check"] = self._validate_cross_references
        self._custom_validators["applicability_check"] = self._validate_applicability
    
    def _check_rule(
        self,
        rule: BREXRule,
        root: ET.Element,
        dm_code: str,
    ) -> List[BREXViolation]:
        """Check a single BREX rule against content."""
        violations = []
        
        # Check context if specified
        context_elements = [root]
        if rule.context:
            context_elements = root.findall(rule.context, self.S1000D_NS)
            if not context_elements:
                context_elements = root.findall(rule.context)
        
        for context in context_elements:
            # Find target elements
            if rule.xpath:
                targets = context.findall(rule.xpath, self.S1000D_NS)
                if not targets:
                    targets = context.findall(rule.xpath)
                
                # Check required rule
                if rule.required and not targets:
                    violations.append(BREXViolation(
                        rule_id=rule.id,
                        rule_name=rule.name,
                        severity=rule.severity,
                        message=rule.message,
                        location=rule.xpath,
                        dm_code=dm_code,
                    ))
                    continue
                
                # Check each target
                for target in targets:
                    violation = self._check_target(rule, target, dm_code)
                    if violation:
                        violations.append(violation)
        
        return violations
    
    def _check_target(
        self,
        rule: BREXRule,
        target: Union[ET.Element, str],
        dm_code: str,
    ) -> Optional[BREXViolation]:
        """Check a specific target against a rule."""
        # Get value to check
        if isinstance(target, str):
            value = target
            location = rule.xpath or "/"
        elif isinstance(target, ET.Element):
            value = target.text or ""
            location = rule.xpath or target.tag
        else:
            return None
        
        # Check allowed values
        if rule.allowed_values:
            if value not in rule.allowed_values:
                return BREXViolation(
                    rule_id=rule.id,
                    rule_name=rule.name,
                    severity=rule.severity,
                    message=f"{rule.message}. Got '{value}', expected one of: {rule.allowed_values}",
                    location=location,
                    actual_value=value,
                    expected=str(rule.allowed_values),
                    dm_code=dm_code,
                )
        
        # Check pattern
        if rule.pattern:
            if not re.match(rule.pattern, value):
                return BREXViolation(
                    rule_id=rule.id,
                    rule_name=rule.name,
                    severity=rule.severity,
                    message=f"{rule.message}. Value '{value}' does not match pattern '{rule.pattern}'",
                    location=location,
                    actual_value=value,
                    expected=rule.pattern,
                    dm_code=dm_code,
                )
        
        return None
    
    def _validate_cross_references(
        self,
        root: ET.Element,
        dm_code: str,
    ) -> List[BREXViolation]:
        """Custom validator for cross-references."""
        violations = []
        
        # Check internal references
        internal_refs = root.findall(".//*[@internalRefId]")
        for ref in internal_refs:
            ref_id = ref.get("internalRefId")
            # Check if target exists
            target = root.find(f".//*[@id='{ref_id}']")
            if target is None:
                violations.append(BREXViolation(
                    rule_id="BREX-XREF-001",
                    rule_name="Broken Internal Reference",
                    severity=BREXSeverity.ERROR,
                    message=f"Internal reference target not found: {ref_id}",
                    location=f".//*[@internalRefId='{ref_id}']",
                    actual_value=ref_id,
                    dm_code=dm_code,
                ))
        
        return violations
    
    def _validate_applicability(
        self,
        root: ET.Element,
        dm_code: str,
    ) -> List[BREXViolation]:
        """Custom validator for applicability annotations."""
        violations = []
        
        # Check that applicability annotations have display text
        applic_elements = root.findall(".//applic")
        for applic in applic_elements:
            display_text = applic.find(".//displayText")
            if display_text is None:
                violations.append(BREXViolation(
                    rule_id="BREX-APPLIC-001",
                    rule_name="Missing Applicability Display Text",
                    severity=BREXSeverity.WARNING,
                    message="Applicability annotation missing display text",
                    location=".//applic",
                    dm_code=dm_code,
                ))
        
        return violations
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get validation statistics."""
        return {
            "contract_id": self.contract_id,
            "total_rules": len(self.rules),
            "validation_count": self._validation_count,
            "total_violations": self._total_violations,
            "rules_by_type": {
                rt.value: len([r for r in self.rules.values() if r.rule_type == rt])
                for rt in BREXRuleType
            },
            "rules_by_severity": {
                sev.value: len([r for r in self.rules.values() if r.severity == sev])
                for sev in BREXSeverity
            },
        }
    
    def generate_report(
        self,
        results: List[BREXValidationResult],
    ) -> str:
        """Generate a validation report."""
        lines = [
            "=" * 70,
            "BREX VALIDATION REPORT",
            f"Contract: {self.contract_id}",
            f"Generated: {datetime.now().isoformat()}",
            "=" * 70,
            "",
        ]
        
        total_valid = sum(1 for r in results if r.valid)
        total_errors = sum(r.errors for r in results)
        total_warnings = sum(r.warnings for r in results)
        
        lines.extend([
            f"Total Data Modules: {len(results)}",
            f"Valid: {total_valid}",
            f"Invalid: {len(results) - total_valid}",
            f"Total Errors: {total_errors}",
            f"Total Warnings: {total_warnings}",
            "",
            "-" * 70,
        ])
        
        for result in results:
            if not result.valid or result.warnings > 0:
                lines.extend([
                    "",
                    f"DM: {result.dm_code}",
                    f"  Status: {'INVALID' if not result.valid else 'VALID (with warnings)'}",
                    f"  Errors: {result.errors}, Warnings: {result.warnings}",
                ])
                
                for v in result.violations:
                    lines.append(f"    [{v.severity.value.upper()}] {v.rule_id}: {v.message}")
        
        lines.extend(["", "=" * 70])
        return "\n".join(lines)
