# =============================================================================
# ASIGT Schema Validator
# S1000D XML Schema validation
# Version: 2.0.0
# =============================================================================
"""
Schema Validator

Validates S1000D Data Modules against official XML schemas.
Supports S1000D Issue 4.1, 4.2, and 5.0 schemas.

Validates:
- XML well-formedness
- Schema conformance
- Namespace declarations
- Element/attribute types
- Required elements

Operates exclusively under ASIT contract authority.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from xml.etree import ElementTree as ET

logger = logging.getLogger(__name__)


class S1000DIssue(Enum):
    """Supported S1000D issues."""
    ISSUE_4_1 = "4.1"
    ISSUE_4_2 = "4.2"
    ISSUE_5_0 = "5.0"


class SchemaErrorType(Enum):
    """Types of schema validation errors."""
    PARSE_ERROR = "parse_error"           # XML parsing failed
    WELLFORMED = "wellformed"             # Not well-formed XML
    NAMESPACE = "namespace"               # Namespace issue
    ELEMENT = "element"                   # Invalid element
    ATTRIBUTE = "attribute"               # Invalid attribute
    TYPE = "type"                         # Type mismatch
    REQUIRED = "required"                 # Missing required element
    PATTERN = "pattern"                   # Pattern constraint violation
    ENUMERATION = "enumeration"           # Enumeration constraint violation
    REFERENCE = "reference"               # ID/IDREF reference error


@dataclass
class SchemaError:
    """Schema validation error details."""
    error_type: SchemaErrorType
    message: str
    line: Optional[int] = None
    column: Optional[int] = None
    element: Optional[str] = None
    attribute: Optional[str] = None
    expected: Optional[str] = None
    actual: Optional[str] = None
    xpath: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "error_type": self.error_type.value,
            "message": self.message,
            "line": self.line,
            "column": self.column,
            "element": self.element,
            "attribute": self.attribute,
            "expected": self.expected,
            "actual": self.actual,
            "xpath": self.xpath,
        }


@dataclass
class SchemaValidationResult:
    """Result of schema validation."""
    valid: bool
    dm_code: str
    schema_issue: str = "5.0"
    errors: List[SchemaError] = field(default_factory=list)
    warnings: List[SchemaError] = field(default_factory=list)
    validated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    schema_path: Optional[str] = None
    
    @property
    def error_count(self) -> int:
        return len(self.errors)
    
    @property
    def warning_count(self) -> int:
        return len(self.warnings)
    
    def add_error(self, error: SchemaError) -> None:
        """Add an error."""
        self.errors.append(error)
        self.valid = False
    
    def add_warning(self, warning: SchemaError) -> None:
        """Add a warning."""
        self.warnings.append(warning)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "valid": self.valid,
            "dm_code": self.dm_code,
            "schema_issue": self.schema_issue,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "errors": [e.to_dict() for e in self.errors],
            "warnings": [w.to_dict() for w in self.warnings],
            "validated_at": self.validated_at,
            "schema_path": self.schema_path,
        }


class SchemaValidator:
    """
    S1000D XML Schema Validator.
    
    Validates Data Modules against S1000D XML schemas. Supports
    Issue 4.1, 4.2, and 5.0. Operates under ASIT contract authority.
    
    Attributes:
        contract: ASIT transformation contract
        config: Validator configuration
        schema_issue: S1000D issue version
        schema_path: Path to schema files
        
    Example:
        >>> validator = SchemaValidator(contract=contract, config=config)
        >>> result = validator.validate(dm_xml_content)
        >>> if not result.valid:
        ...     for error in result.errors:
        ...         print(f"Error: {error.message}")
    """
    
    # S1000D namespaces by issue
    NAMESPACES = {
        S1000DIssue.ISSUE_4_1: "http://www.s1000d.org/S1000D_4-1",
        S1000DIssue.ISSUE_4_2: "http://www.s1000d.org/S1000D_4-2",
        S1000DIssue.ISSUE_5_0: "http://www.s1000d.org/S1000D_5-0",
    }
    
    # Required elements by document type
    REQUIRED_ELEMENTS = {
        "dmodule": [
            "identAndStatusSection",
            "content",
        ],
        "pm": [
            "identAndStatusSection",
            "content",
        ],
        "dml": [
            "identAndStatusSection",
            "dmlContent",
        ],
    }
    
    # Required identification elements
    REQUIRED_IDENT = {
        "dmodule": ["dmAddress", "dmIdent", "dmCode", "language", "issueInfo"],
        "pm": ["pmAddress", "pmIdent", "pmCode", "language", "issueInfo"],
        "dml": ["dmlAddress", "dmlIdent", "dmlCode", "issueInfo"],
    }
    
    def __init__(
        self,
        contract: Dict[str, Any],
        config: Dict[str, Any],
        schema_path: Optional[Path] = None,
    ):
        """
        Initialize Schema Validator.
        
        Args:
            contract: ASIT transformation contract (required)
            config: Validator configuration
            schema_path: Path to S1000D schema files
            
        Raises:
            ValueError: If contract is missing
        """
        if not contract:
            raise ValueError("ASIT contract is required for schema validation")
        
        self.contract = contract
        self.config = config
        
        # Determine schema issue
        issue_str = config.get("schema_issue", "5.0")
        self.schema_issue = S1000DIssue(issue_str)
        
        # Schema path
        self.schema_path = schema_path or Path(f"schemas/s1000d/{issue_str}")
        
        # Contract parameters
        self.contract_id = contract.get("id", "UNKNOWN")
        self.strict_mode = config.get("strict_mode", True)
        
        # Validation tracking
        self._validation_count = 0
        self._error_count = 0
        
        # Try to load lxml for full schema validation
        self._lxml_available = False
        try:
            import lxml.etree as lxml_etree
            self._lxml = lxml_etree
            self._lxml_available = True
            self._load_schemas()
        except ImportError:
            logger.warning(
                "lxml not available - using basic validation only. "
                "Install lxml for full schema validation: pip install lxml"
            )
        
        logger.info(
            f"SchemaValidator initialized: contract={self.contract_id}, "
            f"issue={self.schema_issue.value}, lxml={self._lxml_available}"
        )
    
    def validate(
        self,
        content: Union[str, bytes],
        dm_code: str = "UNKNOWN",
    ) -> SchemaValidationResult:
        """
        Validate XML content against S1000D schema.
        
        Args:
            content: XML content (string or bytes)
            dm_code: Data Module code for reporting
            
        Returns:
            SchemaValidationResult with errors and warnings
        """
        self._validation_count += 1
        result = SchemaValidationResult(
            valid=True,
            dm_code=dm_code,
            schema_issue=self.schema_issue.value,
            schema_path=str(self.schema_path),
        )
        
        # Convert to bytes if string
        if isinstance(content, str):
            content = content.encode("utf-8")
        
        # Step 1: Check well-formedness
        try:
            if self._lxml_available:
                root = self._lxml.fromstring(content)
            else:
                root = ET.fromstring(content)
        except Exception as e:
            result.add_error(SchemaError(
                error_type=SchemaErrorType.PARSE_ERROR,
                message=f"XML parsing failed: {str(e)}",
            ))
            self._error_count += 1
            return result
        
        # Determine document type
        doc_type = root.tag.split("}")[-1] if "}" in root.tag else root.tag
        
        # Step 2: Check namespace
        namespace_error = self._check_namespace(root, doc_type)
        if namespace_error:
            result.add_error(namespace_error)
        
        # Step 3: Structural validation
        structural_errors = self._validate_structure(root, doc_type)
        for error in structural_errors:
            result.add_error(error)
        
        # Step 4: Full schema validation (if lxml available)
        if self._lxml_available and hasattr(self, "_schema"):
            schema_errors = self._validate_with_schema(root)
            for error in schema_errors:
                result.add_error(error)
        
        # Step 5: Custom validations
        custom_errors = self._custom_validations(root, doc_type)
        for error in custom_errors:
            if self.strict_mode:
                result.add_error(error)
            else:
                result.add_warning(error)
        
        self._error_count += result.error_count
        return result
    
    def validate_batch(
        self,
        contents: List[Dict[str, Any]],
    ) -> List[SchemaValidationResult]:
        """
        Validate multiple Data Modules.
        
        Args:
            contents: List of dicts with 'content' and 'dm_code' keys
            
        Returns:
            List of SchemaValidationResult
        """
        results = []
        for item in contents:
            result = self.validate(
                content=item.get("content", ""),
                dm_code=item.get("dm_code", "UNKNOWN"),
            )
            results.append(result)
        return results
    
    def validate_file(self, file_path: Path) -> SchemaValidationResult:
        """
        Validate an XML file.
        
        Args:
            file_path: Path to XML file
            
        Returns:
            SchemaValidationResult
        """
        dm_code = file_path.stem
        
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            return self.validate(content, dm_code)
        except Exception as e:
            result = SchemaValidationResult(
                valid=False,
                dm_code=dm_code,
                schema_issue=self.schema_issue.value,
            )
            result.add_error(SchemaError(
                error_type=SchemaErrorType.PARSE_ERROR,
                message=f"Failed to read file: {str(e)}",
            ))
            return result
    
    def _load_schemas(self) -> None:
        """Load XSD schema files for validation."""
        if not self._lxml_available:
            return
        
        # Schema file mapping
        schema_files = {
            "dmodule": "dmodule.xsd",
            "pm": "pm.xsd",
            "dml": "dml.xsd",
        }
        
        self._schemas = {}
        
        for doc_type, schema_file in schema_files.items():
            schema_path = self.schema_path / schema_file
            if schema_path.exists():
                try:
                    with open(schema_path, "rb") as f:
                        schema_doc = self._lxml.parse(f)
                    self._schemas[doc_type] = self._lxml.XMLSchema(schema_doc)
                    logger.debug(f"Loaded schema: {schema_path}")
                except Exception as e:
                    logger.warning(f"Failed to load schema {schema_path}: {e}")
    
    def _check_namespace(
        self,
        root: ET.Element,
        doc_type: str,
    ) -> Optional[SchemaError]:
        """Check namespace declaration."""
        expected_ns = self.NAMESPACES.get(self.schema_issue)
        
        # Get actual namespace
        actual_ns = None
        if "}" in root.tag:
            actual_ns = root.tag.split("}")[0].strip("{")
        
        # Check xmlns attribute as fallback
        if not actual_ns:
            actual_ns = root.get("xmlns")
        
        if expected_ns and actual_ns != expected_ns:
            return SchemaError(
                error_type=SchemaErrorType.NAMESPACE,
                message=f"Invalid namespace for S1000D Issue {self.schema_issue.value}",
                element=root.tag,
                expected=expected_ns,
                actual=actual_ns,
            )
        
        return None
    
    def _validate_structure(
        self,
        root: ET.Element,
        doc_type: str,
    ) -> List[SchemaError]:
        """Validate basic document structure."""
        errors = []
        
        # Check required top-level elements
        required = self.REQUIRED_ELEMENTS.get(doc_type, [])
        for element_name in required:
            found = self._find_element(root, element_name)
            if found is None:
                errors.append(SchemaError(
                    error_type=SchemaErrorType.REQUIRED,
                    message=f"Required element '{element_name}' not found",
                    element=element_name,
                    xpath=f"/{doc_type}/{element_name}",
                ))
        
        # Check required identification elements
        required_ident = self.REQUIRED_IDENT.get(doc_type, [])
        for element_name in required_ident:
            found = self._find_element(root, element_name)
            if found is None:
                errors.append(SchemaError(
                    error_type=SchemaErrorType.REQUIRED,
                    message=f"Required identification element '{element_name}' not found",
                    element=element_name,
                ))
        
        return errors
    
    def _validate_with_schema(
        self,
        root: ET.Element,
    ) -> List[SchemaError]:
        """Validate against XSD schema using lxml."""
        errors = []
        
        # Determine document type
        doc_type = root.tag.split("}")[-1] if "}" in root.tag else root.tag
        
        schema = self._schemas.get(doc_type)
        if not schema:
            return errors
        
        # Validate
        if not schema.validate(root):
            for error in schema.error_log:
                errors.append(SchemaError(
                    error_type=self._map_lxml_error_type(error),
                    message=error.message,
                    line=error.line,
                    column=error.column,
                ))
        
        return errors
    
    def _map_lxml_error_type(self, error) -> SchemaErrorType:
        """Map lxml error to SchemaErrorType."""
        message_lower = error.message.lower()
        
        if "element" in message_lower and "not expected" in message_lower:
            return SchemaErrorType.ELEMENT
        elif "attribute" in message_lower:
            return SchemaErrorType.ATTRIBUTE
        elif "type" in message_lower:
            return SchemaErrorType.TYPE
        elif "pattern" in message_lower:
            return SchemaErrorType.PATTERN
        elif "enumeration" in message_lower:
            return SchemaErrorType.ENUMERATION
        else:
            return SchemaErrorType.ELEMENT
    
    def _custom_validations(
        self,
        root: ET.Element,
        doc_type: str,
    ) -> List[SchemaError]:
        """Run custom validation checks."""
        errors = []
        
        # Check for empty required elements
        empty_check_elements = ["techName", "infoName", "para"]
        for elem_name in empty_check_elements:
            for elem in self._find_all_elements(root, elem_name):
                if elem.text is None or elem.text.strip() == "":
                    # Check if it has child elements
                    if len(elem) == 0:
                        errors.append(SchemaError(
                            error_type=SchemaErrorType.ELEMENT,
                            message=f"Element '{elem_name}' should not be empty",
                            element=elem_name,
                        ))
        
        # Check ID uniqueness
        ids_seen = set()
        for elem in root.iter():
            elem_id = elem.get("id")
            if elem_id:
                if elem_id in ids_seen:
                    errors.append(SchemaError(
                        error_type=SchemaErrorType.REFERENCE,
                        message=f"Duplicate ID found: '{elem_id}'",
                        element=elem.tag,
                        attribute="id",
                        actual=elem_id,
                    ))
                ids_seen.add(elem_id)
        
        # Check IDREF targets exist
        for elem in root.iter():
            for attr_name in ["internalRefId", "refId"]:
                ref_id = elem.get(attr_name)
                if ref_id and ref_id not in ids_seen:
                    errors.append(SchemaError(
                        error_type=SchemaErrorType.REFERENCE,
                        message=f"Reference target not found: '{ref_id}'",
                        element=elem.tag,
                        attribute=attr_name,
                        actual=ref_id,
                    ))
        
        return errors
    
    def _find_element(
        self,
        root: ET.Element,
        name: str,
    ) -> Optional[ET.Element]:
        """Find element by local name (ignoring namespace)."""
        # Try with namespace
        ns = self.NAMESPACES.get(self.schema_issue, "")
        if ns:
            found = root.find(f".//{{{ns}}}{name}")
            if found is not None:
                return found
        
        # Try without namespace
        found = root.find(f".//{name}")
        if found is not None:
            return found
        
        # Try iterating (handles namespace variations)
        for elem in root.iter():
            local_name = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
            if local_name == name:
                return elem
        
        return None
    
    def _find_all_elements(
        self,
        root: ET.Element,
        name: str,
    ) -> List[ET.Element]:
        """Find all elements by local name."""
        results = []
        for elem in root.iter():
            local_name = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
            if local_name == name:
                results.append(elem)
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get validation statistics."""
        return {
            "contract_id": self.contract_id,
            "schema_issue": self.schema_issue.value,
            "lxml_available": self._lxml_available,
            "strict_mode": self.strict_mode,
            "validation_count": self._validation_count,
            "total_errors": self._error_count,
        }
    
    def generate_report(
        self,
        results: List[SchemaValidationResult],
    ) -> str:
        """Generate a validation report."""
        lines = [
            "=" * 70,
            "SCHEMA VALIDATION REPORT",
            f"Contract: {self.contract_id}",
            f"S1000D Issue: {self.schema_issue.value}",
            f"Generated: {datetime.now().isoformat()}",
            "=" * 70,
            "",
        ]
        
        total_valid = sum(1 for r in results if r.valid)
        total_errors = sum(r.error_count for r in results)
        total_warnings = sum(r.warning_count for r in results)
        
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
            if not result.valid or result.warning_count > 0:
                lines.extend([
                    "",
                    f"DM: {result.dm_code}",
                    f"  Status: {'INVALID' if not result.valid else 'VALID (with warnings)'}",
                    f"  Errors: {result.error_count}, Warnings: {result.warning_count}",
                ])
                
                for error in result.errors:
                    loc = f" (line {error.line})" if error.line else ""
                    lines.append(f"    [ERROR] {error.error_type.value}: {error.message}{loc}")
                
                for warning in result.warnings:
                    lines.append(f"    [WARNING] {warning.error_type.value}: {warning.message}")
        
        lines.extend(["", "=" * 70])
        return "\n".join(lines)
