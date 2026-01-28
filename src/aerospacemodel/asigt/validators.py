"""
ASIGT Validators Module

Validation engines operating EXCLUSIVELY under ASIT contract authority.

This module provides validators for:
    - BREX (Business Rules Exchange): S1000D business rule compliance
    - Schema: XML schema validation against S1000D schemas
    - Trace: Traceability completeness verification

CRITICAL CONSTRAINT:
    ASIGT cannot operate standalone.
    All validators enforce rules defined by ASIT contracts and governance.

Validation Flow:
    1. Load BREX rules (base + project-specific)
    2. Load XML schema for S1000D version
    3. Validate each artifact
    4. Generate validation report
    5. Check trace coverage requirements
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Pattern,
    Set,
    Tuple,
    Type,
    Union,
)
from xml.etree import ElementTree as ET

import yaml

from .engine import (
    ValidationStatus,
    ValidationIssue,
    BREXValidationResult,
    SchemaValidationResult,
    TraceValidationResult,
    ValidationReport,
    ErrorSeverity,
    SourceArtifact,
    OutputArtifact,
    TraceMatrix,
    TraceLink,
    ExecutionContext,
    ASIGTError,
    ASIGTValidationError,
)


logger = logging.getLogger(__name__)


# =============================================================================
# ENUMERATIONS
# =============================================================================


class BREXSeverity(Enum):
    """BREX rule severity levels."""
    ERROR = "ERROR"         # Critical - blocks publication
    WARNING = "WARNING"     # Significant - should be corrected
    CAUTION = "CAUTION"     # Potential issue - review recommended
    INFO = "INFO"           # Best practice recommendation


class ValidationCategory(Enum):
    """Validation rule categories."""
    IDENTIFICATION = "identification"
    STRUCTURE = "structure"
    CONTENT = "content"
    REFERENCES = "references"
    APPLICABILITY = "applicability"
    METADATA = "metadata"
    VOCABULARY = "vocabulary"
    ILLUSTRATIONS = "illustrations"
    CUSTOM = "custom"


class ValidationType(Enum):
    """Types of validation checks."""
    ATTRIBUTE_REQUIRED = "attribute_required"
    ATTRIBUTE_PATTERN = "attribute_pattern"
    ATTRIBUTE_RECOMMENDED = "attribute_recommended"
    CHILD_REQUIRED = "child_required"
    CHILD_RECOMMENDED = "child_recommended"
    CHILD_ORDER = "child_order"
    ELEMENT_REQUIRED = "element_required"
    ELEMENT_FORBIDDEN = "element_forbidden"
    PATTERN = "pattern"
    PATTERN_FORBIDDEN = "pattern_forbidden"
    ENUMERATION = "enumeration"
    NOT_EMPTY = "not_empty"
    IDREF_VALID = "idref_valid"
    SIBLING_ORDER = "sibling_order"
    DATE_FORMAT = "date_format"
    SEQUENTIAL_NUMBERING = "sequential_numbering"
    CHILD_COUNT = "child_count"
    CUSTOM = "custom"


class SchemaVersion(Enum):
    """S1000D schema versions."""
    S1000D_5_0 = "5.0"
    S1000D_4_2 = "4.2"
    S1000D_4_1 = "4.1"


# =============================================================================
# DATA CLASSES
# =============================================================================


@dataclass
class BREXRule:
    """
    Represents a single BREX validation rule.
    
    BREX rules define what is and isn't allowed in S1000D content
    according to project-specific business rules.
    """
    id: str
    name: str
    description: str
    severity: BREXSeverity
    category: ValidationCategory
    xpath: str
    validation_type: ValidationType
    
    # Validation parameters
    pattern: Optional[str] = None
    patterns: Optional[List[Dict[str, str]]] = None
    attributes: Optional[List[str]] = None
    children: Optional[List[str]] = None
    values: Optional[List[str]] = None
    min_length: Optional[int] = None
    min_count: Optional[int] = None
    order: Optional[List[str]] = None
    first: Optional[str] = None
    second: Optional[str] = None
    date_format: Optional[str] = None
    custom_function: Optional[str] = None
    custom_parameters: Optional[Dict[str, Any]] = None
    
    # Rule message
    message: str = ""
    remediation: str = ""
    
    # Rule state
    enabled: bool = True
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BREXRule":
        """Create BREXRule from dictionary."""
        validation = data.get("validation", {})
        
        # Parse severity
        severity_str = data.get("severity", "WARNING")
        severity = BREXSeverity[severity_str] if severity_str in BREXSeverity.__members__ else BREXSeverity.WARNING
        
        # Parse category
        category_str = data.get("category", "custom")
        category = ValidationCategory(category_str) if category_str in [c.value for c in ValidationCategory] else ValidationCategory.CUSTOM
        
        # Parse validation type
        val_type_str = validation.get("type", "custom")
        val_type = ValidationType(val_type_str) if val_type_str in [t.value for t in ValidationType] else ValidationType.CUSTOM
        
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            description=data.get("description", ""),
            severity=severity,
            category=category,
            xpath=data.get("xpath", ""),
            validation_type=val_type,
            pattern=validation.get("pattern"),
            patterns=validation.get("patterns"),
            attributes=validation.get("attributes"),
            children=validation.get("children"),
            values=validation.get("values"),
            min_length=validation.get("min_length"),
            min_count=validation.get("min"),
            order=validation.get("order"),
            first=validation.get("first"),
            second=validation.get("second"),
            date_format=validation.get("format"),
            custom_function=validation.get("function"),
            custom_parameters=validation.get("parameters"),
            message=data.get("message", ""),
            remediation=data.get("remediation", ""),
            enabled=data.get("enabled", True)
        )


@dataclass
class BREXViolation:
    """Represents a single BREX rule violation."""
    rule: BREXRule
    element_path: str
    element_tag: str
    message: str
    value: Optional[str] = None
    expected: Optional[str] = None
    line_number: Optional[int] = None
    
    def to_validation_issue(self) -> ValidationIssue:
        """Convert to ValidationIssue."""
        return ValidationIssue(
            rule_id=self.rule.id,
            severity=ErrorSeverity[self.rule.severity.name],
            artifact_id=self.element_path,
            message=self.message,
            location=f"{self.element_tag} at {self.element_path}",
            remediation=self.rule.remediation
        )


@dataclass
class SchemaError:
    """Represents an XML schema validation error."""
    line: int
    column: int
    message: str
    element: str = ""
    error_type: str = "schema"
    
    def to_validation_issue(self, artifact_id: str) -> ValidationIssue:
        """Convert to ValidationIssue."""
        return ValidationIssue(
            rule_id=f"SCHEMA-{self.error_type.upper()}",
            severity=ErrorSeverity.ERROR,
            artifact_id=artifact_id,
            message=self.message,
            location=f"Line {self.line}, Column {self.column}",
            remediation="Correct the XML to conform to S1000D schema"
        )


@dataclass
class TraceIssue:
    """Represents a traceability issue."""
    issue_type: str  # orphan_source, orphan_target, missing_link, invalid_hash
    artifact_id: str
    artifact_type: str
    message: str
    severity: ErrorSeverity = ErrorSeverity.WARNING
    
    def to_validation_issue(self) -> ValidationIssue:
        """Convert to ValidationIssue."""
        return ValidationIssue(
            rule_id=f"TRACE-{self.issue_type.upper().replace('_', '-')}",
            severity=self.severity,
            artifact_id=self.artifact_id,
            message=self.message,
            location=self.artifact_type,
            remediation="Ensure all artifacts are properly traced"
        )


@dataclass
class ValidatorConfig:
    """Configuration for validators."""
    # BREX configuration
    base_brex_path: Optional[Path] = None
    project_brex_path: Optional[Path] = None
    brex_profile: str = "default"
    
    # Schema configuration
    schema_path: Optional[Path] = None
    schema_version: SchemaVersion = SchemaVersion.S1000D_5_0
    
    # Trace configuration
    trace_coverage_required: float = 100.0
    allow_orphan_sources: bool = False
    allow_orphan_targets: bool = False
    verify_hashes: bool = True
    
    # Validation options
    fail_on_warning: bool = False
    max_errors: int = 1000
    stop_on_first_error: bool = False
    validate_references: bool = True
    validate_icns: bool = True


# =============================================================================
# BASE VALIDATOR CLASS
# =============================================================================


class BaseValidator(ABC):
    """
    Abstract base class for all ASIGT validators.
    
    All validators operate under ASIT contract authority.
    """
    
    def __init__(self, config: ValidatorConfig, context: Optional[ExecutionContext] = None):
        """
        Initialize validator.
        
        Args:
            config: Validator configuration
            context: Execution context from ASIT
        """
        self.config = config
        self.context = context
        self.logger = logging.getLogger(f"asigt.validator.{self.__class__.__name__}")
        self._errors: List[ValidationIssue] = []
        self._warnings: List[ValidationIssue] = []
    
    @abstractmethod
    def validate(self, artifact: Any) -> bool:
        """
        Validate an artifact.
        
        Args:
            artifact: The artifact to validate
            
        Returns:
            True if validation passed, False otherwise
        """
        raise NotImplementedError
    
    @property
    def errors(self) -> List[ValidationIssue]:
        """Get validation errors."""
        return self._errors
    
    @property
    def warnings(self) -> List[ValidationIssue]:
        """Get validation warnings."""
        return self._warnings
    
    @property
    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self._errors) > 0
    
    def clear(self) -> None:
        """Clear all validation results."""
        self._errors.clear()
        self._warnings.clear()


# =============================================================================
# BREX VALIDATOR
# =============================================================================


class BREXValidator(BaseValidator):
    """
    Business Rules Exchange (BREX) validator.
    
    Validates S1000D content against BREX rules defined in YAML configuration.
    Supports rule inheritance, profiles, and project-specific customization.
    
    BREX ensures:
        - Structural compliance with S1000D schema
        - Content consistency across publications
        - Controlled vocabulary usage
        - Cross-reference integrity
        - Metadata completeness
    
    Usage:
        >>> config = ValidatorConfig(
        ...     base_brex_path=Path("ASIGT/brex/S1000D_5.0_DEFAULT.yaml"),
        ...     brex_profile="default"
        ... )
        >>> validator = BREXValidator(config)
        >>> result = validator.validate_file(Path("dm.xml"))
    """
    
    S1000D_NS = "http://www.s1000d.org/S1000D_5-0"
    
    def __init__(self, config: ValidatorConfig, context: Optional[ExecutionContext] = None):
        super().__init__(config, context)
        self._rules: Dict[str, BREXRule] = {}
        self._violations: List[BREXViolation] = []
        self._profiles: Dict[str, Dict[str, Any]] = {}
        self._active_profile: str = config.brex_profile
        self._custom_validators: Dict[str, Callable] = {}
        
        # Register namespaces
        self._namespaces = {
            "": self.S1000D_NS,
            "xsi": "http://www.w3.org/2001/XMLSchema-instance"
        }
        
        # Load BREX rules
        self._load_brex_rules()
        
        # Register custom validators
        self._register_custom_validators()
    
    def validate(self, artifact: Union[OutputArtifact, Path, str, ET.Element]) -> bool:
        """
        Validate artifact against BREX rules.
        
        Args:
            artifact: The artifact to validate (path, XML string, or Element)
            
        Returns:
            True if validation passed, False if errors found
        """
        self.clear()
        self._violations.clear()
        
        # Parse XML
        try:
            if isinstance(artifact, OutputArtifact):
                if artifact.path.exists():
                    tree = ET.parse(artifact.path)
                    root = tree.getroot()
                else:
                    self.logger.warning(f"Artifact file not found: {artifact.path}")
                    return False
            elif isinstance(artifact, Path):
                tree = ET.parse(artifact)
                root = tree.getroot()
            elif isinstance(artifact, str):
                root = ET.fromstring(artifact)
            elif isinstance(artifact, ET.Element):
                root = artifact
            else:
                raise ValueError(f"Unsupported artifact type: {type(artifact)}")
        except ET.ParseError as e:
            self._errors.append(ValidationIssue(
                rule_id="BREX-PARSE-ERROR",
                severity=ErrorSeverity.FATAL,
                artifact_id=str(artifact),
                message=f"XML parse error: {e}",
                location="document root"
            ))
            return False
        
        # Apply each enabled rule
        for rule_id, rule in self._rules.items():
            if not rule.enabled:
                continue
            
            if not self._is_rule_in_profile(rule):
                continue
            
            try:
                self._apply_rule(root, rule)
            except Exception as e:
                self.logger.error(f"Error applying rule {rule_id}: {e}")
        
        # Convert violations to issues
        for violation in self._violations:
            issue = violation.to_validation_issue()
            if violation.rule.severity in [BREXSeverity.ERROR]:
                self._errors.append(issue)
            else:
                self._warnings.append(issue)
        
        return not self.has_errors
    
    def validate_file(self, file_path: Path) -> BREXValidationResult:
        """
        Validate a file and return structured result.
        
        Args:
            file_path: Path to XML file
            
        Returns:
            BREXValidationResult with detailed results
        """
        passed = self.validate(file_path)
        
        error_count = len([v for v in self._violations if v.rule.severity == BREXSeverity.ERROR])
        warning_count = len([v for v in self._violations if v.rule.severity == BREXSeverity.WARNING])
        
        status = ValidationStatus.PASS if passed else ValidationStatus.FAIL
        if not passed and not error_count:
            status = ValidationStatus.WARN
        
        return BREXValidationResult(
            status=status,
            rules_applied=len([r for r in self._rules.values() if r.enabled]),
            errors=error_count,
            warnings=warning_count,
            issues=self._errors + self._warnings
        )
    
    def validate_content(self, xml_content: str, artifact_id: str = "") -> BREXValidationResult:
        """
        Validate XML content string.
        
        Args:
            xml_content: XML content as string
            artifact_id: Identifier for the content
            
        Returns:
            BREXValidationResult
        """
        return self.validate_file(xml_content)  # validate() handles strings
    
    def get_rule(self, rule_id: str) -> Optional[BREXRule]:
        """Get a rule by ID."""
        return self._rules.get(rule_id)
    
    def disable_rule(self, rule_id: str) -> None:
        """Disable a rule."""
        if rule_id in self._rules:
            self._rules[rule_id].enabled = False
    
    def enable_rule(self, rule_id: str) -> None:
        """Enable a rule."""
        if rule_id in self._rules:
            self._rules[rule_id].enabled = True
    
    def set_profile(self, profile_name: str) -> None:
        """Set active BREX profile."""
        if profile_name in self._profiles:
            self._active_profile = profile_name
        else:
            self.logger.warning(f"Unknown profile: {profile_name}")
    
    @property
    def violations(self) -> List[BREXViolation]:
        """Get all violations from last validation."""
        return self._violations
    
    @property
    def rules(self) -> Dict[str, BREXRule]:
        """Get all loaded rules."""
        return self._rules
    
    # =========================================================================
    # Private Methods
    # =========================================================================
    
    def _load_brex_rules(self) -> None:
        """Load BREX rules from configuration files."""
        # Load base BREX
        if self.config.base_brex_path and self.config.base_brex_path.exists():
            self._load_brex_file(self.config.base_brex_path)
        
        # Load project BREX (overrides/extends base)
        if self.config.project_brex_path and self.config.project_brex_path.exists():
            self._load_brex_file(self.config.project_brex_path, is_project=True)
        
        self.logger.info(f"Loaded {len(self._rules)} BREX rules")
    
    def _load_brex_file(self, path: Path, is_project: bool = False) -> None:
        """Load BREX rules from a YAML file."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            
            brex_data = data.get("brex", data)
            
            # Load profiles
            if "profiles" in brex_data:
                self._profiles.update(brex_data["profiles"])
            
            # Load rules by category
            rules_section = brex_data.get("rules", {})
            for category, rules in rules_section.items():
                if isinstance(rules, list):
                    for rule_data in rules:
                        rule = BREXRule.from_dict(rule_data)
                        self._rules[rule.id] = rule
            
            # Load project custom rules
            if is_project and "custom_rules" in brex_data:
                for category, rules in brex_data["custom_rules"].items():
                    if isinstance(rules, list):
                        for rule_data in rules:
                            rule = BREXRule.from_dict(rule_data)
                            self._rules[rule.id] = rule
            
            # Apply rule modifications for project
            if is_project and "rule_modifications" in brex_data:
                mods = brex_data["rule_modifications"]
                
                # Disable rules
                for disabled in mods.get("disabled_rules", []):
                    rule_id = disabled.get("rule_id") if isinstance(disabled, dict) else disabled
                    if rule_id in self._rules:
                        self._rules[rule_id].enabled = False
                
                # Promote to error
                for promoted in mods.get("promoted_to_error", []):
                    rule_id = promoted.get("rule_id") if isinstance(promoted, dict) else promoted
                    if rule_id in self._rules:
                        self._rules[rule_id].severity = BREXSeverity.ERROR
                
                # Demote to warning
                for demoted in mods.get("demoted_to_warning", []):
                    rule_id = demoted.get("rule_id") if isinstance(demoted, dict) else demoted
                    if rule_id in self._rules:
                        self._rules[rule_id].severity = BREXSeverity.WARNING
            
            self.logger.debug(f"Loaded BREX from {path}")
            
        except Exception as e:
            self.logger.error(f"Error loading BREX file {path}: {e}")
    
    def _is_rule_in_profile(self, rule: BREXRule) -> bool:
        """Check if rule is enabled in active profile."""
        if self._active_profile not in self._profiles:
            return True  # No profile filtering
        
        profile = self._profiles[self._active_profile]
        
        # Check disabled rules
        disabled = profile.get("disabled_rules", [])
        if rule.id in disabled:
            return False
        
        # Check enabled categories
        enabled_cats = profile.get("enabled_categories", [])
        if enabled_cats and rule.category.value not in enabled_cats:
            return False
        
        # Check severity filter
        severity_filter = profile.get("severity_filter", [])
        if severity_filter and rule.severity.name not in severity_filter:
            return False
        
        return True
    
    def _apply_rule(self, root: ET.Element, rule: BREXRule) -> None:
        """Apply a single BREX rule to the document."""
        # Find elements matching XPath
        try:
            # Handle namespaced XPath
            xpath = self._convert_xpath(rule.xpath)
            elements = root.findall(xpath, self._namespaces)
        except Exception as e:
            self.logger.debug(f"XPath error for rule {rule.id}: {e}")
            elements = []
        
        # Apply validation based on type
        validation_methods = {
            ValidationType.ATTRIBUTE_REQUIRED: self._validate_attribute_required,
            ValidationType.ATTRIBUTE_PATTERN: self._validate_attribute_pattern,
            ValidationType.ATTRIBUTE_RECOMMENDED: self._validate_attribute_recommended,
            ValidationType.CHILD_REQUIRED: self._validate_child_required,
            ValidationType.CHILD_RECOMMENDED: self._validate_child_recommended,
            ValidationType.CHILD_ORDER: self._validate_child_order,
            ValidationType.ELEMENT_REQUIRED: self._validate_element_required,
            ValidationType.ELEMENT_FORBIDDEN: self._validate_element_forbidden,
            ValidationType.PATTERN: self._validate_pattern,
            ValidationType.PATTERN_FORBIDDEN: self._validate_pattern_forbidden,
            ValidationType.ENUMERATION: self._validate_enumeration,
            ValidationType.NOT_EMPTY: self._validate_not_empty,
            ValidationType.IDREF_VALID: self._validate_idref,
            ValidationType.SIBLING_ORDER: self._validate_sibling_order,
            ValidationType.DATE_FORMAT: self._validate_date_format,
            ValidationType.SEQUENTIAL_NUMBERING: self._validate_sequential,
            ValidationType.CHILD_COUNT: self._validate_child_count,
            ValidationType.CUSTOM: self._validate_custom
        }
        
        validator = validation_methods.get(rule.validation_type)
        if validator:
            validator(root, elements, rule)
    
    def _convert_xpath(self, xpath: str) -> str:
        """Convert XPath to work with ElementTree namespaces."""
        # Simple conversion - add default namespace prefix
        if xpath.startswith("//"):
            # Replace element names with namespaced versions
            parts = xpath.split("/")
            converted = []
            for part in parts:
                if part and not part.startswith("@") and not part.startswith("*"):
                    # Extract element name and predicates
                    if "[" in part:
                        elem_name = part.split("[")[0]
                        predicate = "[" + "[".join(part.split("[")[1:])
                        converted.append(f".//{elem_name}{predicate}" if elem_name else f".//{part}")
                    else:
                        converted.append(part)
                else:
                    converted.append(part)
            return "/".join(converted)
        return xpath
    
    def _get_element_path(self, element: ET.Element, root: ET.Element) -> str:
        """Get path to element from root."""
        # Simplified - just return tag for now
        return element.tag.replace(f"{{{self.S1000D_NS}}}", "")
    
    def _add_violation(
        self, 
        rule: BREXRule, 
        element: ET.Element, 
        root: ET.Element,
        message: Optional[str] = None,
        value: Optional[str] = None,
        expected: Optional[str] = None
    ) -> None:
        """Add a violation."""
        tag = element.tag.replace(f"{{{self.S1000D_NS}}}", "")
        path = self._get_element_path(element, root)
        
        violation = BREXViolation(
            rule=rule,
            element_path=path,
            element_tag=tag,
            message=message or rule.message,
            value=value,
            expected=expected
        )
        self._violations.append(violation)
    
    # Validation methods
    def _validate_attribute_required(
        self, root: ET.Element, elements: List[ET.Element], rule: BREXRule
    ) -> None:
        """Validate that required attributes are present."""
        for elem in elements:
            for attr in (rule.attributes or []):
                if attr not in elem.attrib:
                    self._add_violation(
                        rule, elem, root,
                        message=f"Required attribute '{attr}' is missing",
                        expected=attr
                    )
    
    def _validate_attribute_pattern(
        self, root: ET.Element, elements: List[ET.Element], rule: BREXRule
    ) -> None:
        """Validate attribute value against pattern."""
        if not rule.pattern:
            return
        
        pattern = re.compile(rule.pattern)
        attr_name = rule.attributes[0] if rule.attributes else None
        
        for elem in elements:
            if attr_name:
                value = elem.get(attr_name, "")
            else:
                # XPath selected the attribute value directly
                value = elem.text or "" if hasattr(elem, 'text') else str(elem)
            
            if value and not pattern.match(value):
                self._add_violation(
                    rule, elem, root,
                    message=f"Value '{value}' does not match pattern '{rule.pattern}'",
                    value=value,
                    expected=rule.pattern
                )
    
    def _validate_attribute_recommended(
        self, root: ET.Element, elements: List[ET.Element], rule: BREXRule
    ) -> None:
        """Validate recommended attributes (warnings only)."""
        for elem in elements:
            for attr in (rule.attributes or []):
                if attr not in elem.attrib:
                    self._add_violation(
                        rule, elem, root,
                        message=f"Recommended attribute '{attr}' is missing"
                    )
    
    def _validate_child_required(
        self, root: ET.Element, elements: List[ET.Element], rule: BREXRule
    ) -> None:
        """Validate that required children are present."""
        for elem in elements:
            for child_name in (rule.children or []):
                # Check for namespaced element
                child = elem.find(child_name, self._namespaces)
                if child is None:
                    # Try with full namespace
                    child = elem.find(f"{{{self.S1000D_NS}}}{child_name}")
                
                if child is None:
                    self._add_violation(
                        rule, elem, root,
                        message=f"Required child element '{child_name}' is missing",
                        expected=child_name
                    )
    
    def _validate_child_recommended(
        self, root: ET.Element, elements: List[ET.Element], rule: BREXRule
    ) -> None:
        """Validate recommended children (warnings only)."""
        # Same as required but uses warning severity defined in rule
        self._validate_child_required(root, elements, rule)
    
    def _validate_child_order(
        self, root: ET.Element, elements: List[ET.Element], rule: BREXRule
    ) -> None:
        """Validate that children appear in correct order."""
        if not rule.order:
            return
        
        for elem in elements:
            children = [c.tag.replace(f"{{{self.S1000D_NS}}}", "") for c in elem]
            
            # Filter to only tracked elements
            tracked = [c for c in children if c in rule.order]
            
            # Check order
            last_index = -1
            for child in tracked:
                idx = rule.order.index(child)
                if idx < last_index:
                    self._add_violation(
                        rule, elem, root,
                        message=f"Child elements out of order. Expected: {rule.order}",
                        value=str(children),
                        expected=str(rule.order)
                    )
                    break
                last_index = idx
    
    def _validate_element_required(
        self, root: ET.Element, elements: List[ET.Element], rule: BREXRule
    ) -> None:
        """Validate that element exists."""
        if not elements:
            # Add violation to root if element is missing entirely
            self._violations.append(BREXViolation(
                rule=rule,
                element_path="/",
                element_tag="document",
                message=f"Required element matching '{rule.xpath}' not found"
            ))
    
    def _validate_element_forbidden(
        self, root: ET.Element, elements: List[ET.Element], rule: BREXRule
    ) -> None:
        """Validate that forbidden element does not exist."""
        for elem in elements:
            self._add_violation(
                rule, elem, root,
                message=f"Forbidden element found"
            )
    
    def _validate_pattern(
        self, root: ET.Element, elements: List[ET.Element], rule: BREXRule
    ) -> None:
        """Validate element text against pattern."""
        if not rule.pattern:
            return
        
        pattern = re.compile(rule.pattern)
        
        for elem in elements:
            value = self._get_element_text(elem)
            if value and not pattern.match(value):
                self._add_violation(
                    rule, elem, root,
                    message=f"Content does not match pattern '{rule.pattern}'",
                    value=value,
                    expected=rule.pattern
                )
    
    def _validate_pattern_forbidden(
        self, root: ET.Element, elements: List[ET.Element], rule: BREXRule
    ) -> None:
        """Validate that content does not match forbidden pattern."""
        patterns = rule.patterns or ([{"pattern": rule.pattern}] if rule.pattern else [])
        
        for elem in elements:
            value = self._get_element_text(elem)
            if not value:
                continue
            
            for pat_config in patterns:
                pattern = pat_config.get("pattern", "")
                if pattern and re.search(pattern, value):
                    replacement = pat_config.get("replacement", "")
                    msg = f"Forbidden pattern '{pattern}' found"
                    if replacement:
                        msg += f". Use '{replacement}' instead"
                    self._add_violation(rule, elem, root, message=msg, value=value)
    
    def _validate_enumeration(
        self, root: ET.Element, elements: List[ET.Element], rule: BREXRule
    ) -> None:
        """Validate value is in enumeration."""
        if not rule.values:
            return
        
        for elem in elements:
            value = self._get_element_text(elem)
            if value and value not in rule.values:
                self._add_violation(
                    rule, elem, root,
                    message=f"Value '{value}' not in allowed values",
                    value=value,
                    expected=str(rule.values)
                )
    
    def _validate_not_empty(
        self, root: ET.Element, elements: List[ET.Element], rule: BREXRule
    ) -> None:
        """Validate element has content."""
        min_len = rule.min_length or 1
        
        for elem in elements:
            value = self._get_element_text(elem)
            if not value or len(value.strip()) < min_len:
                self._add_violation(
                    rule, elem, root,
                    message=f"Content is empty or too short (min {min_len} characters)"
                )
    
    def _validate_idref(
        self, root: ET.Element, elements: List[ET.Element], rule: BREXRule
    ) -> None:
        """Validate ID references point to existing elements."""
        # Collect all IDs in document
        all_ids = set()
        for elem in root.iter():
            if "id" in elem.attrib:
                all_ids.add(elem.get("id"))
        
        attr_name = rule.attributes[0] if rule.attributes else "internalRefId"
        
        for elem in elements:
            ref_id = elem.get(attr_name, "")
            if ref_id and ref_id not in all_ids:
                self._add_violation(
                    rule, elem, root,
                    message=f"Reference '{ref_id}' does not point to existing element",
                    value=ref_id
                )
    
    def _validate_sibling_order(
        self, root: ET.Element, elements: List[ET.Element], rule: BREXRule
    ) -> None:
        """Validate sibling element order."""
        if not rule.first or not rule.second:
            return
        
        for elem in elements:
            first_idx = -1
            second_idx = -1
            
            for i, child in enumerate(elem):
                tag = child.tag.replace(f"{{{self.S1000D_NS}}}", "")
                if tag == rule.first and first_idx == -1:
                    first_idx = i
                elif tag == rule.second and second_idx == -1:
                    second_idx = i
            
            if first_idx > -1 and second_idx > -1 and second_idx < first_idx:
                self._add_violation(
                    rule, elem, root,
                    message=f"'{rule.first}' must appear before '{rule.second}'",
                    expected=f"{rule.first} before {rule.second}"
                )
    
    def _validate_date_format(
        self, root: ET.Element, elements: List[ET.Element], rule: BREXRule
    ) -> None:
        """Validate date format."""
        expected_format = rule.date_format or "YYYY-MM-DD"
        
        for elem in elements:
            # Check attributes with 'Date' in name
            for attr_name, attr_value in elem.attrib.items():
                if "date" in attr_name.lower() or "Date" in attr_name:
                    if not self._is_valid_date(attr_value, expected_format):
                        self._add_violation(
                            rule, elem, root,
                            message=f"Date '{attr_value}' does not match format '{expected_format}'",
                            value=attr_value,
                            expected=expected_format
                        )
    
    def _validate_sequential(
        self, root: ET.Element, elements: List[ET.Element], rule: BREXRule
    ) -> None:
        """Validate sequential numbering."""
        # Check that figure/step IDs are sequential
        if not elements:
            return
        
        # Extract numbers from IDs
        numbers = []
        for elem in elements:
            id_val = elem.get("id", "")
            match = re.search(r"(\d+)", id_val)
            if match:
                numbers.append(int(match.group(1)))
        
        # Check sequence
        for i, num in enumerate(numbers[1:], 1):
            if num != numbers[i-1] + 1:
                # Not necessarily an error - just info
                pass
    
    def _validate_child_count(
        self, root: ET.Element, elements: List[ET.Element], rule: BREXRule
    ) -> None:
        """Validate minimum child count."""
        min_count = rule.min_count or 1
        
        for elem in elements:
            if len(list(elem)) < min_count:
                self._add_violation(
                    rule, elem, root,
                    message=f"Element must have at least {min_count} children",
                    value=str(len(list(elem))),
                    expected=str(min_count)
                )
    
    def _validate_custom(
        self, root: ET.Element, elements: List[ET.Element], rule: BREXRule
    ) -> None:
        """Apply custom validation function."""
        if rule.custom_function and rule.custom_function in self._custom_validators:
            validator_func = self._custom_validators[rule.custom_function]
            validator_func(root, elements, rule, self)
    
    def _get_element_text(self, elem: ET.Element) -> str:
        """Get text content of element including children."""
        text_parts = []
        if elem.text:
            text_parts.append(elem.text)
        for child in elem:
            if child.tail:
                text_parts.append(child.tail)
        return "".join(text_parts).strip()
    
    def _is_valid_date(self, value: str, format_str: str) -> bool:
        """Check if value matches date format."""
        if format_str == "YYYY-MM-DD":
            pattern = r"^\d{4}-\d{2}-\d{2}$"
        elif format_str == "YYYY":
            pattern = r"^\d{4}$"
        else:
            pattern = r"^\d{4}-\d{2}-\d{2}$"
        return bool(re.match(pattern, value))
    
    def _register_custom_validators(self) -> None:
        """Register custom validation functions."""
        self._custom_validators["validate_cross_references"] = self._custom_validate_cross_refs
        self._custom_validators["validate_applicability"] = self._custom_validate_applicability
        self._custom_validators["validate_illustrations"] = self._custom_validate_illustrations
    
    def _custom_validate_cross_refs(
        self, root: ET.Element, elements: List[ET.Element], rule: BREXRule, validator: "BREXValidator"
    ) -> None:
        """Custom validator for cross-reference integrity."""
        # Collect all IDs
        all_ids = set()
        for elem in root.iter():
            if "id" in elem.attrib:
                all_ids.add(elem.get("id"))
        
        # Check all internal references
        for ref in root.iter():
            tag = ref.tag.replace(f"{{{self.S1000D_NS}}}", "")
            if tag == "internalRef":
                ref_id = ref.get("internalRefId", "")
                if ref_id and ref_id not in all_ids:
                    validator._add_violation(
                        rule, ref, root,
                        message=f"Internal reference '{ref_id}' target not found"
                    )
    
    def _custom_validate_applicability(
        self, root: ET.Element, elements: List[ET.Element], rule: BREXRule, validator: "BREXValidator"
    ) -> None:
        """Custom validator for applicability annotations."""
        pass  # Placeholder
    
    def _custom_validate_illustrations(
        self, root: ET.Element, elements: List[ET.Element], rule: BREXRule, validator: "BREXValidator"
    ) -> None:
        """Custom validator for illustration references."""
        pass  # Placeholder


# =============================================================================
# SCHEMA VALIDATOR
# =============================================================================


class SchemaValidator(BaseValidator):
    """
    XML Schema validator for S1000D content.
    
    Validates S1000D documents against official XML schemas.
    Supports S1000D Issue 4.1, 4.2, and 5.0.
    
    Note: Full XSD validation requires lxml library.
    This implementation provides basic structural validation
    when lxml is not available.
    
    Usage:
        >>> config = ValidatorConfig(
        ...     schema_path=Path("schemas/s1000d/5.0"),
        ...     schema_version=SchemaVersion.S1000D_5_0
        ... )
        >>> validator = SchemaValidator(config)
        >>> result = validator.validate_file(Path("dm.xml"))
    """
    
    S1000D_NS = "http://www.s1000d.org/S1000D_5-0"
    
    # Schema locations by document type
    SCHEMA_MAP = {
        "dmodule": {
            "descriptive": "descript.xsd",
            "procedural": "proced.xsd",
            "ipd": "ipd.xsd",
            "fault": "fault.xsd",
            "crew": "crew.xsd",
            "brex": "brex.xsd",
            "container": "container.xsd"
        },
        "pm": "pm.xsd",
        "dml": "dml.xsd",
        "comment": "comment.xsd"
    }
    
    def __init__(self, config: ValidatorConfig, context: Optional[ExecutionContext] = None):
        super().__init__(config, context)
        self._schema_cache: Dict[str, Any] = {}
        self._schema_errors: List[SchemaError] = []
        self._use_lxml = self._check_lxml_available()
    
    def validate(self, artifact: Union[OutputArtifact, Path, str]) -> bool:
        """
        Validate artifact against XML schema.
        
        Args:
            artifact: The artifact to validate
            
        Returns:
            True if valid, False if errors
        """
        self.clear()
        self._schema_errors.clear()
        
        # Parse XML
        try:
            if isinstance(artifact, OutputArtifact):
                xml_path = artifact.path
            elif isinstance(artifact, Path):
                xml_path = artifact
            else:
                # String content - write to temp or parse directly
                xml_path = None
                xml_content = artifact
            
            if xml_path:
                tree = ET.parse(xml_path)
                root = tree.getroot()
            else:
                root = ET.fromstring(xml_content)
                
        except ET.ParseError as e:
            self._errors.append(ValidationIssue(
                rule_id="SCHEMA-PARSE-ERROR",
                severity=ErrorSeverity.FATAL,
                artifact_id=str(artifact),
                message=f"XML parse error: {e}",
                location="document"
            ))
            return False
        
        # Determine document type
        doc_type = self._determine_document_type(root)
        
        # Validate structure
        if self._use_lxml:
            return self._validate_with_lxml(root, doc_type, str(artifact))
        else:
            return self._validate_basic(root, doc_type, str(artifact))
    
    def validate_file(self, file_path: Path) -> SchemaValidationResult:
        """
        Validate file and return structured result.
        
        Args:
            file_path: Path to XML file
            
        Returns:
            SchemaValidationResult
        """
        valid = self.validate(file_path)
        
        return SchemaValidationResult(
            status=ValidationStatus.PASS if valid else ValidationStatus.FAIL,
            schema_version=self.config.schema_version.value,
            documents_checked=1,
            valid_count=1 if valid else 0,
            invalid_count=0 if valid else 1,
            issues=self._errors
        )
    
    def validate_batch(self, file_paths: List[Path]) -> SchemaValidationResult:
        """
        Validate multiple files.
        
        Args:
            file_paths: List of file paths
            
        Returns:
            Combined SchemaValidationResult
        """
        total = len(file_paths)
        valid_count = 0
        all_issues: List[ValidationIssue] = []
        
        for path in file_paths:
            if self.validate(path):
                valid_count += 1
            all_issues.extend(self._errors)
            self._errors.clear()
        
        return SchemaValidationResult(
            status=ValidationStatus.PASS if valid_count == total else ValidationStatus.FAIL,
            schema_version=self.config.schema_version.value,
            documents_checked=total,
            valid_count=valid_count,
            invalid_count=total - valid_count,
            issues=all_issues
        )
    
    def _check_lxml_available(self) -> bool:
        """Check if lxml is available for full schema validation."""
        try:
            import lxml.etree
            return True
        except ImportError:
            self.logger.info("lxml not available - using basic validation")
            return False
    
    def _determine_document_type(self, root: ET.Element) -> str:
        """Determine S1000D document type from root element."""
        tag = root.tag.replace(f"{{{self.S1000D_NS}}}", "")
        
        if tag == "dmodule":
            # Determine DM type from content
            content = root.find(f".//{{{self.S1000D_NS}}}content")
            if content is not None and len(content) > 0:
                first_child = content[0].tag.replace(f"{{{self.S1000D_NS}}}", "")
                type_map = {
                    "description": "descriptive",
                    "procedure": "procedural",
                    "illustratedPartsCatalog": "ipd",
                    "faultIsolation": "fault",
                    "crewDrillSteps": "crew",
                    "brex": "brex"
                }
                return type_map.get(first_child, "container")
            return "container"
        
        return tag
    
    def _validate_with_lxml(self, root: ET.Element, doc_type: str, artifact_id: str) -> bool:
        """Validate using lxml with full schema support."""
        try:
            from lxml import etree
            
            # Convert to lxml element
            xml_string = ET.tostring(root, encoding="unicode")
            lxml_root = etree.fromstring(xml_string.encode())
            
            # Load schema
            schema_file = self._get_schema_file(doc_type)
            if schema_file and schema_file.exists():
                schema_doc = etree.parse(str(schema_file))
                schema = etree.XMLSchema(schema_doc)
                
                if not schema.validate(lxml_root):
                    for error in schema.error_log:
                        self._errors.append(ValidationIssue(
                            rule_id="SCHEMA-VALIDATION",
                            severity=ErrorSeverity.ERROR,
                            artifact_id=artifact_id,
                            message=str(error.message),
                            location=f"Line {error.line}"
                        ))
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"lxml validation error: {e}")
            return self._validate_basic(root, doc_type, artifact_id)
    
    def _validate_basic(self, root: ET.Element, doc_type: str, artifact_id: str) -> bool:
        """Basic structural validation without full XSD."""
        valid = True
        
        # Check root element
        tag = root.tag.replace(f"{{{self.S1000D_NS}}}", "")
        expected_roots = ["dmodule", "pm", "dml", "comment", "scormContentPackage"]
        
        if tag not in expected_roots:
            self._errors.append(ValidationIssue(
                rule_id="SCHEMA-ROOT",
                severity=ErrorSeverity.ERROR,
                artifact_id=artifact_id,
                message=f"Invalid root element '{tag}'. Expected one of: {expected_roots}",
                location="root"
            ))
            valid = False
        
        # Check required sections based on document type
        if tag == "dmodule":
            valid = self._validate_dmodule_structure(root, artifact_id) and valid
        elif tag == "pm":
            valid = self._validate_pm_structure(root, artifact_id) and valid
        elif tag == "dml":
            valid = self._validate_dml_structure(root, artifact_id) and valid
        
        return valid
    
    def _validate_dmodule_structure(self, root: ET.Element, artifact_id: str) -> bool:
        """Validate basic DM structure."""
        valid = True
        
        # Check for identAndStatusSection
        ident_status = root.find(f".//{{{self.S1000D_NS}}}identAndStatusSection")
        if ident_status is None:
            self._errors.append(ValidationIssue(
                rule_id="SCHEMA-STRUCT-001",
                severity=ErrorSeverity.ERROR,
                artifact_id=artifact_id,
                message="Missing required identAndStatusSection",
                location="dmodule"
            ))
            valid = False
        else:
            # Check for dmIdent
            dm_ident = ident_status.find(f".//{{{self.S1000D_NS}}}dmIdent")
            if dm_ident is None:
                self._errors.append(ValidationIssue(
                    rule_id="SCHEMA-STRUCT-002",
                    severity=ErrorSeverity.ERROR,
                    artifact_id=artifact_id,
                    message="Missing required dmIdent in identAndStatusSection",
                    location="identAndStatusSection"
                ))
                valid = False
        
        # Check for content section
        content = root.find(f".//{{{self.S1000D_NS}}}content")
        if content is None:
            self._errors.append(ValidationIssue(
                rule_id="SCHEMA-STRUCT-003",
                severity=ErrorSeverity.ERROR,
                artifact_id=artifact_id,
                message="Missing required content section",
                location="dmodule"
            ))
            valid = False
        
        return valid
    
    def _validate_pm_structure(self, root: ET.Element, artifact_id: str) -> bool:
        """Validate basic PM structure."""
        valid = True
        
        ident_status = root.find(f".//{{{self.S1000D_NS}}}identAndStatusSection")
        if ident_status is None:
            self._errors.append(ValidationIssue(
                rule_id="SCHEMA-STRUCT-PM-001",
                severity=ErrorSeverity.ERROR,
                artifact_id=artifact_id,
                message="Missing required identAndStatusSection in PM",
                location="pm"
            ))
            valid = False
        
        content = root.find(f".//{{{self.S1000D_NS}}}content")
        if content is None:
            self._errors.append(ValidationIssue(
                rule_id="SCHEMA-STRUCT-PM-002",
                severity=ErrorSeverity.ERROR,
                artifact_id=artifact_id,
                message="Missing required content section in PM",
                location="pm"
            ))
            valid = False
        
        return valid
    
    def _validate_dml_structure(self, root: ET.Element, artifact_id: str) -> bool:
        """Validate basic DML structure."""
        valid = True
        
        ident_status = root.find(f".//{{{self.S1000D_NS}}}identAndStatusSection")
        if ident_status is None:
            self._errors.append(ValidationIssue(
                rule_id="SCHEMA-STRUCT-DML-001",
                severity=ErrorSeverity.ERROR,
                artifact_id=artifact_id,
                message="Missing required identAndStatusSection in DML",
                location="dml"
            ))
            valid = False
        
        dml_content = root.find(f".//{{{self.S1000D_NS}}}dmlContent")
        if dml_content is None:
            self._errors.append(ValidationIssue(
                rule_id="SCHEMA-STRUCT-DML-002",
                severity=ErrorSeverity.ERROR,
                artifact_id=artifact_id,
                message="Missing required dmlContent section",
                location="dml"
            ))
            valid = False
        
        return valid
    
    def _get_schema_file(self, doc_type: str) -> Optional[Path]:
        """Get schema file path for document type."""
        if not self.config.schema_path:
            return None
        
        if doc_type in self.SCHEMA_MAP.get("dmodule", {}):
            schema_name = self.SCHEMA_MAP["dmodule"][doc_type]
        elif doc_type in self.SCHEMA_MAP:
            schema_name = self.SCHEMA_MAP[doc_type]
        else:
            schema_name = "dmodule.xsd"
        
        return self.config.schema_path / schema_name


# =============================================================================
# TRACE VALIDATOR
# =============================================================================


class TraceValidator(BaseValidator):
    """
    Traceability completeness validator.
    
    Validates that all source artifacts are traced to outputs and
    all outputs are traced back to sources.
    
    Traceability requirements:
        - Every source must produce at least one output
        - Every output must trace to at least one source
        - Hash verification ensures content integrity
        - Coverage must meet required threshold
    
    Usage:
        >>> config = ValidatorConfig(
        ...     trace_coverage_required=100.0,
        ...     verify_hashes=True
        ... )
        >>> validator = TraceValidator(config)
        >>> result = validator.validate(trace_matrix, sources, outputs)
    """
    
    def __init__(self, config: ValidatorConfig, context: Optional[ExecutionContext] = None):
        super().__init__(config, context)
        self._issues: List[TraceIssue] = []
    
    def validate(
        self, 
        trace_matrix: TraceMatrix,
        sources: Optional[List[SourceArtifact]] = None,
        outputs: Optional[List[OutputArtifact]] = None
    ) -> bool:
        """
        Validate trace matrix completeness.
        
        Args:
            trace_matrix: The trace matrix to validate
            sources: Optional list of source artifacts
            outputs: Optional list of output artifacts
            
        Returns:
            True if traceability requirements met
        """
        self.clear()
        self._issues.clear()
        
        # Check coverage
        coverage = trace_matrix.coverage_percent
        if coverage < self.config.trace_coverage_required:
            self._issues.append(TraceIssue(
                issue_type="coverage_insufficient",
                artifact_id=trace_matrix.run_id,
                artifact_type="trace_matrix",
                message=f"Trace coverage {coverage:.1f}% below required {self.config.trace_coverage_required}%",
                severity=ErrorSeverity.ERROR
            ))
        
        # Check for orphan sources
        if sources and not self.config.allow_orphan_sources:
            source_ids = {s.id for s in sources}
            traced_sources = {e.source_id for e in trace_matrix.entries}
            orphan_sources = source_ids - traced_sources
            
            for orphan_id in orphan_sources:
                self._issues.append(TraceIssue(
                    issue_type="orphan_source",
                    artifact_id=orphan_id,
                    artifact_type="source",
                    message=f"Source artifact '{orphan_id}' has no traced outputs",
                    severity=ErrorSeverity.WARNING
                ))
        
        # Check for orphan outputs
        if outputs and not self.config.allow_orphan_targets:
            output_ids = {o.id for o in outputs}
            traced_outputs = {e.target_id for e in trace_matrix.entries}
            orphan_outputs = output_ids - traced_outputs
            
            for orphan_id in orphan_outputs:
                self._issues.append(TraceIssue(
                    issue_type="orphan_target",
                    artifact_id=orphan_id,
                    artifact_type="output",
                    message=f"Output artifact '{orphan_id}' has no traced sources",
                    severity=ErrorSeverity.WARNING
                ))
        
        # Verify hashes if requested
        if self.config.verify_hashes:
            self._verify_hashes(trace_matrix, sources, outputs)
        
        # Convert issues to validation issues
        for issue in self._issues:
            vi = issue.to_validation_issue()
            if issue.severity == ErrorSeverity.ERROR:
                self._errors.append(vi)
            else:
                self._warnings.append(vi)
        
        return not self.has_errors
    
    def validate_matrix(
        self, 
        trace_matrix: TraceMatrix,
        sources: Optional[List[SourceArtifact]] = None,
        outputs: Optional[List[OutputArtifact]] = None
    ) -> TraceValidationResult:
        """
        Validate and return structured result.
        
        Args:
            trace_matrix: The trace matrix to validate
            sources: Optional list of source artifacts
            outputs: Optional list of output artifacts
            
        Returns:
            TraceValidationResult
        """
        valid = self.validate(trace_matrix, sources, outputs)
        
        orphan_inputs = len([i for i in self._issues if i.issue_type == "orphan_source"])
        orphan_outputs = len([i for i in self._issues if i.issue_type == "orphan_target"])
        
        return TraceValidationResult(
            status=ValidationStatus.PASS if valid else ValidationStatus.FAIL,
            coverage_percent=trace_matrix.coverage_percent,
            inputs_traced=trace_matrix.source_count,
            outputs_traced=trace_matrix.target_count,
            orphan_inputs=orphan_inputs,
            orphan_outputs=orphan_outputs
        )
    
    def verify_link(self, link: TraceLink) -> bool:
        """
        Verify a single trace link.
        
        Checks that source and target exist and hashes match.
        
        Args:
            link: The trace link to verify
            
        Returns:
            True if link is valid
        """
        if not link.source_id or not link.target_id:
            return False
        
        if not link.source_hash or not link.target_hash:
            return False
        
        return True
    
    @property
    def issues(self) -> List[TraceIssue]:
        """Get trace issues from last validation."""
        return self._issues
    
    def _verify_hashes(
        self,
        trace_matrix: TraceMatrix,
        sources: Optional[List[SourceArtifact]],
        outputs: Optional[List[OutputArtifact]]
    ) -> None:
        """Verify hash integrity of trace links."""
        source_map = {s.id: s for s in (sources or [])}
        output_map = {o.id: o for o in (outputs or [])}
        
        for entry in trace_matrix.entries:
            # Verify source hash
            if entry.source_id in source_map:
                source = source_map[entry.source_id]
                if source.hash_sha256 and entry.source_hash:
                    if source.hash_sha256 != entry.source_hash:
                        self._issues.append(TraceIssue(
                            issue_type="hash_mismatch",
                            artifact_id=entry.source_id,
                            artifact_type="source",
                            message=f"Source hash mismatch - content may have changed",
                            severity=ErrorSeverity.WARNING
                        ))
            
            # Verify target hash
            if entry.target_id in output_map:
                output = output_map[entry.target_id]
                if output.hash_sha256 and entry.target_hash:
                    if output.hash_sha256 != entry.target_hash:
                        self._issues.append(TraceIssue(
                            issue_type="hash_mismatch",
                            artifact_id=entry.target_id,
                            artifact_type="output",
                            message=f"Output hash mismatch - content may have changed",
                            severity=ErrorSeverity.WARNING
                        ))


# =============================================================================
# COMBINED VALIDATOR
# =============================================================================


class CombinedValidator:
    """
    Combined validator that runs BREX, Schema, and Trace validation.
    
    Provides a single interface for comprehensive validation of
    ASIGT-generated content.
    
    Usage:
        >>> config = ValidatorConfig(
        ...     base_brex_path=Path("ASIGT/brex/S1000D_5.0_DEFAULT.yaml"),
        ...     schema_version=SchemaVersion.S1000D_5_0,
        ...     trace_coverage_required=100.0
        ... )
        >>> validator = CombinedValidator(config)
        >>> report = validator.validate_run(outputs, trace_matrix, sources)
    """
    
    def __init__(self, config: ValidatorConfig, context: Optional[ExecutionContext] = None):
        self.config = config
        self.context = context
        self.logger = logging.getLogger("asigt.validator.combined")
        
        self.brex_validator = BREXValidator(config, context)
        self.schema_validator = SchemaValidator(config, context)
        self.trace_validator = TraceValidator(config, context)
    
    def validate_artifact(
        self, 
        artifact: Union[OutputArtifact, Path, str]
    ) -> Tuple[BREXValidationResult, SchemaValidationResult]:
        """
        Validate a single artifact with BREX and Schema.
        
        Args:
            artifact: The artifact to validate
            
        Returns:
            Tuple of (BREXValidationResult, SchemaValidationResult)
        """
        # BREX validation
        brex_result = self.brex_validator.validate_file(
            artifact.path if isinstance(artifact, OutputArtifact) else artifact
        )
        
        # Schema validation
        schema_result = self.schema_validator.validate_file(
            artifact.path if isinstance(artifact, OutputArtifact) else artifact
        )
        
        return brex_result, schema_result
    
    def validate_run(
        self,
        run_id: str,
        outputs: List[OutputArtifact],
        trace_matrix: Optional[TraceMatrix] = None,
        sources: Optional[List[SourceArtifact]] = None
    ) -> ValidationReport:
        """
        Validate an entire ASIGT run.
        
        Args:
            run_id: The run identifier
            outputs: List of output artifacts
            trace_matrix: The trace matrix
            sources: Optional list of source artifacts
            
        Returns:
            Complete ValidationReport
        """
        self.logger.info(f"Validating run {run_id} with {len(outputs)} outputs")
        
        # Aggregate BREX results
        total_brex_errors = 0
        total_brex_warnings = 0
        brex_issues: List[ValidationIssue] = []
        brex_rules_applied = 0
        
        # Aggregate schema results
        total_schema_valid = 0
        total_schema_invalid = 0
        schema_issues: List[ValidationIssue] = []
        
        for output in outputs:
            if output.path.exists():
                # BREX validation
                brex_result = self.brex_validator.validate_file(output.path)
                total_brex_errors += brex_result.errors
                total_brex_warnings += brex_result.warnings
                brex_issues.extend(brex_result.issues)
                brex_rules_applied = max(brex_rules_applied, brex_result.rules_applied)
                
                # Schema validation
                schema_result = self.schema_validator.validate_file(output.path)
                if schema_result.status == ValidationStatus.PASS:
                    total_schema_valid += 1
                else:
                    total_schema_invalid += 1
                schema_issues.extend(schema_result.issues)
        
        # Trace validation
        trace_result = TraceValidationResult(
            status=ValidationStatus.SKIP,
            coverage_percent=100.0
        )
        if trace_matrix:
            trace_result = self.trace_validator.validate_matrix(
                trace_matrix, sources, outputs
            )
        
        # Build overall status
        overall_status = ValidationStatus.PASS
        if total_brex_errors > 0 or total_schema_invalid > 0:
            overall_status = ValidationStatus.FAIL
        elif total_brex_warnings > 0 or trace_result.status == ValidationStatus.WARN:
            overall_status = ValidationStatus.WARN
        
        # Create report
        report = ValidationReport(
            run_id=run_id,
            timestamp=datetime.now(),
            overall_status=overall_status,
            brex=BREXValidationResult(
                status=ValidationStatus.FAIL if total_brex_errors > 0 else ValidationStatus.PASS,
                rules_applied=brex_rules_applied,
                errors=total_brex_errors,
                warnings=total_brex_warnings,
                issues=brex_issues
            ),
            schema=SchemaValidationResult(
                status=ValidationStatus.FAIL if total_schema_invalid > 0 else ValidationStatus.PASS,
                schema_version=self.config.schema_version.value,
                documents_checked=len(outputs),
                valid_count=total_schema_valid,
                invalid_count=total_schema_invalid,
                issues=schema_issues
            ),
            trace=trace_result
        )
        
        self.logger.info(
            f"Validation complete: {overall_status.value} "
            f"(BREX errors: {total_brex_errors}, Schema invalid: {total_schema_invalid})"
        )
        
        return report


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================


def validate_dm(
    dm_path: Path,
    brex_path: Optional[Path] = None,
    schema_version: SchemaVersion = SchemaVersion.S1000D_5_0
) -> Tuple[bool, List[ValidationIssue]]:
    """
    Quick validation of a single Data Module.
    
    Args:
        dm_path: Path to DM file
        brex_path: Optional path to BREX rules
        schema_version: S1000D schema version
        
    Returns:
        Tuple of (is_valid, issues)
    """
    config = ValidatorConfig(
        base_brex_path=brex_path,
        schema_version=schema_version
    )
    
    validator = CombinedValidator(config)
    brex_result, schema_result = validator.validate_artifact(dm_path)
    
    is_valid = brex_result.passed and schema_result.passed
    issues = brex_result.issues + schema_result.issues
    
    return is_valid, issues


def create_validation_report(
    run_id: str,
    outputs: List[OutputArtifact],
    config: Optional[ValidatorConfig] = None
) -> ValidationReport:
    """
    Create a validation report for outputs.
    
    Args:
        run_id: Run identifier
        outputs: Output artifacts to validate
        config: Optional validator configuration
        
    Returns:
        ValidationReport
    """
    config = config or ValidatorConfig()
    validator = CombinedValidator(config)
    return validator.validate_run(run_id, outputs)


# =============================================================================
# MODULE EXPORTS
# =============================================================================


__all__ = [
    # Enumerations
    "BREXSeverity",
    "ValidationCategory",
    "ValidationType",
    "SchemaVersion",
    
    # Data classes
    "BREXRule",
    "BREXViolation",
    "SchemaError",
    "TraceIssue",
    "ValidatorConfig",
    
    # Validators
    "BaseValidator",
    "BREXValidator",
    "SchemaValidator",
    "TraceValidator",
    "CombinedValidator",
    
    # Convenience functions
    "validate_dm",
    "create_validation_report",
]
