"""
AEROSPACEMODEL Exceptions

Defines exception hierarchy for ASIT and ASIGT errors.
"""


class AerospaceModelError(Exception):
    """Base exception for all AEROSPACEMODEL errors."""
    pass


class ASITError(AerospaceModelError):
    """
    ASIT-specific errors.
    
    Raised when governance, baseline, or contract operations fail.
    """
    pass


class ASIGTError(AerospaceModelError):
    """
    ASIGT-specific errors.
    
    Raised when content generation fails.
    
    Common causes:
        - Attempting to execute without ASIT instance
        - Contract not approved
        - Baseline not found
        - Transformation failure
    """
    pass


class ContractError(ASITError):
    """Contract-specific errors."""
    pass


class BaselineError(ASITError):
    """Baseline-specific errors."""
    pass


class ValidationError(ASIGTError):
    """Validation failure errors."""
    pass


class TraceError(ASIGTError):
    """Traceability errors."""
    pass


__all__ = [
    "AerospaceModelError",
    "ASITError",
    "ASIGTError",
    "ContractError",
    "BaselineError",
    "ValidationError",
    "TraceError",
]
