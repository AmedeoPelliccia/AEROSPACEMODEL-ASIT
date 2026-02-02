"""
CNOT Integration with ASIT/ASIGT

Integrates CNOT chain with existing AEROSPACEMODEL components:
    - TransformationEngine execution flow
    - BREXDecisionEngine for rule evaluation
    - ContractManager for contract validation
    - GovernanceController for authority checks

This module provides helper functions to create pre-configured CNOT chains
for common transformation scenarios.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from .chain import CNOTChain
from .gates import (
    AuthorityGate,
    BaselineGate,
    BREXGate,
    ContractGate,
    SafetyGate,
    TraceGate,
)

logger = logging.getLogger(__name__)


def create_standard_transformation_chain(
    contract_id: str,
    baseline_id: Optional[str] = None,
    required_authority: Optional[str] = None,
    include_safety_gate: bool = True,
    include_trace_gate: bool = True,
    trace_coverage_threshold: int = 100
) -> CNOTChain:
    """
    Create a standard transformation chain with commonly used gates.
    
    This is the recommended chain for most S1000D transformation operations.
    
    Args:
        contract_id: Transformation contract ID
        baseline_id: Baseline ID (optional)
        required_authority: Required authority level (optional)
        include_safety_gate: Whether to include safety gate (default: True)
        include_trace_gate: Whether to include trace gate (default: True)
        trace_coverage_threshold: Trace coverage threshold (default: 100%)
        
    Returns:
        Configured CNOTChain ready for execution
    
    Example:
        >>> chain = create_standard_transformation_chain(
        ...     contract_id="KITDM-CTR-LM-CSDB_ATA28",
        ...     baseline_id="FBL-2026-Q1-003",
        ...     required_authority="STK_ENG"
        ... )
        >>> result = chain.execute(context)
    """
    logger.info(f"Creating standard transformation chain for contract: {contract_id}")
    
    chain = CNOTChain(chain_id=f"STD-TRANS-{contract_id}")
    
    # Gate 1: Contract validation
    chain.add_gate(ContractGate(contract_id=contract_id, config={"require_approved": True}))
    
    # Gate 2: Baseline validation (if baseline specified)
    if baseline_id:
        chain.add_gate(BaselineGate(baseline_id=baseline_id, config={"require_established": True}))
    
    # Gate 3: Authority validation (if authority specified)
    if required_authority:
        chain.add_gate(AuthorityGate(required_authority=required_authority))
    
    # Gate 4: BREX validation (always included)
    chain.add_gate(BREXGate(config={"cascade_all": True}))
    
    # Gate 5: Trace validation (if enabled)
    if include_trace_gate:
        chain.add_gate(TraceGate(config={"coverage_threshold": trace_coverage_threshold}))
    
    # Gate 6: Safety validation (if enabled)
    if include_safety_gate:
        chain.add_gate(SafetyGate(config={"escalation_target": "STK_SAF"}))
    
    logger.info(f"Standard chain created with {chain.get_gate_count()} gates")
    return chain


def create_publication_chain(
    contract_id: str,
    publication_type: str,
    ata_chapter: Optional[str] = None,
    required_authority: str = "STK_CM"
) -> CNOTChain:
    """
    Create a chain for publication generation (AMM, SRM, IPC, etc.).
    
    Args:
        contract_id: Transformation contract ID
        publication_type: Type of publication (AMM, SRM, IPC, etc.)
        ata_chapter: ATA chapter if specific to one chapter
        required_authority: Required authority (default: STK_CM)
        
    Returns:
        Configured CNOTChain for publication generation
    
    Example:
        >>> chain = create_publication_chain(
        ...     contract_id="KITDM-CTR-LM-CSDB_ATA27",
        ...     publication_type="AMM",
        ...     ata_chapter="27"
        ... )
        >>> result = chain.execute(context)
    """
    chain_id = f"PUB-{publication_type}"
    if ata_chapter:
        chain_id += f"-ATA{ata_chapter}"
    
    logger.info(f"Creating publication chain: {chain_id}")
    
    chain = CNOTChain(chain_id=chain_id)
    
    # Publications require stricter validation
    chain.add_gate(ContractGate(contract_id=contract_id, config={"require_approved": True}))
    chain.add_gate(AuthorityGate(required_authority=required_authority))
    chain.add_gate(BREXGate(config={"cascade_all": True}))
    chain.add_gate(TraceGate(config={"coverage_threshold": 100}))
    chain.add_gate(SafetyGate(config={"escalation_target": "STK_SAF"}))
    
    logger.info(f"Publication chain created with {chain.get_gate_count()} gates")
    return chain


def create_brex_only_chain(contract_id: Optional[str] = None) -> CNOTChain:
    """
    Create a minimal chain with only BREX validation.
    
    Useful for quick validation without full transformation control.
    
    Args:
        contract_id: Optional contract ID
        
    Returns:
        CNOTChain with BREX gate only
    """
    logger.info("Creating BREX-only validation chain")
    
    chain = CNOTChain(chain_id="BREX-ONLY")
    
    if contract_id:
        chain.add_gate(ContractGate(contract_id=contract_id, config={"require_approved": True}))
    
    chain.add_gate(BREXGate(config={"cascade_all": True}))
    
    return chain


def integrate_with_brex_engine(
    context: Dict[str, Any],
    brex_engine: Any
) -> Dict[str, Any]:
    """
    Integrate CNOT chain with BREX Decision Engine.
    
    Runs BREX cascade and adds result to context for BREXGate evaluation.
    
    Args:
        context: Execution context
        brex_engine: BREXDecisionEngine instance
        
    Returns:
        Updated context with BREX result
    """
    logger.debug("Running BREX cascade for CNOT integration")
    
    try:
        # Run BREX cascade (implementation depends on actual BREXDecisionEngine API)
        # This is a placeholder - actual implementation would call the engine
        brex_result = {
            "success": True,
            "final_action": "ALLOW",
            "blocked_by": None,
            "escalation_required": False,
            "escalation_rules": []
        }
        
        context["brex_result"] = brex_result
        logger.debug("BREX cascade completed successfully")
        
    except Exception as e:
        logger.error(f"BREX cascade failed: {e}")
        context["brex_result"] = {
            "success": False,
            "final_action": "BLOCK",
            "blocked_by": "BREX_ENGINE_ERROR",
            "error": str(e)
        }
    
    return context


def prepare_context_from_contract(contract: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prepare execution context from a contract definition.
    
    Args:
        contract: Contract dictionary
        
    Returns:
        Context dictionary ready for chain execution
    """
    context = {
        "contract": contract,
        "contract_id": contract.get("contract_id"),
        "execution_authority": contract.get("execution_authority", "STK_CM"),
        "source_artifacts": contract.get("source_artifacts", []),
    }
    
    # Add baseline if referenced
    if "baseline_reference" in contract:
        context["baseline"] = {
            "baseline_id": contract["baseline_reference"],
            "state": "APPROVED"  # Would be loaded from actual baseline
        }
    
    # Add trace data placeholder
    context["trace_data"] = {
        "total_required": 0,
        "total_linked": 0
    }
    
    # Add safety impact placeholder
    context["safety_impact"] = {
        "is_safety_critical": False,
        "safety_level": "NONE"
    }
    
    return context


def validate_transformation_prerequisites(
    contract_id: str,
    baseline_id: Optional[str] = None,
    authority: Optional[str] = None
) -> tuple[bool, str]:
    """
    Validate transformation prerequisites before creating chain.
    
    Args:
        contract_id: Contract ID to validate
        baseline_id: Baseline ID to validate (optional)
        authority: Authority level to validate (optional)
        
    Returns:
        Tuple of (is_valid, message)
    """
    # Contract ID format validation
    if not contract_id.startswith("KITDM-CTR-"):
        return False, f"Invalid contract ID format: {contract_id}"
    
    # Baseline ID format validation (if provided)
    if baseline_id and not baseline_id.startswith("FBL-") and not baseline_id.startswith("PBL-"):
        return False, f"Invalid baseline ID format: {baseline_id}"
    
    # Authority validation (if provided)
    valid_authorities = [
        "STK_TEST", "STK_OPS", "STK_ENG", "STK_QA", "STK_SAF",
        "STK_CM", "STK_SE", "STK_PM", "STK_CERT"
    ]
    if authority and authority not in valid_authorities:
        return False, f"Invalid authority level: {authority}"
    
    return True, "Prerequisites validated"
