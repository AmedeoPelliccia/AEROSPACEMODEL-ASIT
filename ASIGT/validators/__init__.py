# =============================================================================
# ASIGT Validators Module
# S1000D validation engines under ASIT contract authority
# Version: 2.0.0
# =============================================================================
"""
ASIGT Validators Package

This package provides validation engines for S1000D content that operate
exclusively under ASIT contract authority. Validators ensure that all
generated content meets:
- BREX (Business Rules Exchange) compliance
- XML Schema conformance (S1000D Issue 5.0)
- Traceability completeness requirements

Validators:
    - brex_validator: Business Rules Exchange enforcement
    - schema_validator: XML schema validation
    - trace_validator: Traceability completeness verification

Usage:
    from asigt.validators import BREXValidator, SchemaValidator, TraceValidator
    
    # All validators require an ASIT contract
    validator = BREXValidator(contract=contract, config=config)
    result = validator.validate(dm_content)
"""

from .brex_validator import BREXValidator, BREXRule, BREXSeverity
from .schema_validator import SchemaValidator, SchemaValidationResult
from .trace_validator import TraceValidator, TraceValidationResult

__all__ = [
    "BREXValidator",
    "BREXRule",
    "BREXSeverity",
    "SchemaValidator",
    "SchemaValidationResult",
    "TraceValidator",
    "TraceValidationResult",
]

__version__ = "2.0.0"
