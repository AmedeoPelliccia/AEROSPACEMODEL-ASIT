# =============================================================================
# ASIGT BREX Module
# Business Rules Exchange for S1000D governance
# Version: 2.0.0
# =============================================================================
"""
ASIGT BREX Module

This module provides BREX (Business Rules Exchange) functionality for the
AEROSPACEMODEL system, including:

    - BREXDecisionEngine: Guided reasoning through BREX logic decision points
    - BREXAuditLog: Auditable explainability logging
    - BREX rule loading and validation

The AEROSPACEMODEL Agent's reasoning is constrained, guided, and explainable
through the BREX ruleset. Every step is a validated decision node.
No free-form autonomy exists.

Usage:
    >>> from ASIGT.brex import BREXDecisionEngine, create_brex_engine
    >>> 
    >>> engine, audit_log = create_brex_engine()
    >>> context = {
    ...     "contract_id": "KITDM-CTR-LM-CSDB_ATA28",
    ...     "contract_status": "APPROVED",
    ...     "baseline_id": "FBL-2026-Q1-003",
    ...     "baseline_status": "ESTABLISHED",
    ...     "ata_domain": "ATA 28",
    ... }
    >>> result = engine.evaluate_cascade(context)
    >>> print(f"Success: {result.success}, Action: {result.final_action.value}")
"""

from .brex_decision_engine import (
    # Enumerations
    BREXDecisionAction,
    BREXConditionType,
    BREXDecisionSeverity,
    
    # Data Classes
    BREXCondition,
    BREXDecisionRule,
    BREXDecisionResult,
    BREXCascadeResult,
    
    # Main Classes
    BREXDecisionEngine,
    BREXAuditLog,
    
    # Factory Function
    create_brex_engine,
)

__all__ = [
    # Enumerations
    "BREXDecisionAction",
    "BREXConditionType",
    "BREXDecisionSeverity",
    
    # Data Classes
    "BREXCondition",
    "BREXDecisionRule",
    "BREXDecisionResult",
    "BREXCascadeResult",
    
    # Main Classes
    "BREXDecisionEngine",
    "BREXAuditLog",
    
    # Factory Function
    "create_brex_engine",
]

__version__ = "2.0.0"
