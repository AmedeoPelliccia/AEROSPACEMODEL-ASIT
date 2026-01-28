"""
ASIT — Aircraft Systems Information Transponder

Governance, structure, and lifecycle authority layer.

ASIT defines:
    - What can be transformed
    - From which baseline
    - Under what authority
    - For which lifecycle state
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional, List
from datetime import datetime

# Import governance components
from .governance import (
    BaselineType,
    BaselineState,
    Baseline,
    BaselineContent,
    BaselineEffectivity,
    BaselineAuthority,
    ChangeRequest,
    ChangeRequestStatus,
    ChangeOrder,
    ChangeOrderStatus,
    ChangeClassification,
    ApprovalState,
    StakeholderRole,
    Stakeholder,
    ApprovalMatrix,
    ApprovalRequirement,
    ApprovalRecord,
    GovernanceController,
    GovernanceError,
    BaselineNotFoundError,
    AuthorizationError,
)

# Import contracts components
from .contracts import (
    Contract,
    ContractStatus,
    ContractCategory,
    ContractHeader,
    ContractAuthority,
    ContractManager,
    ContractError,
    ContractNotFoundError,
    ContractValidationError,
    ExecutionMode,
    ErrorHandling,
    SeverityThreshold,
    PublicationType,
    OutputType,
    S1000DVersion,
    BaselineReference,
    ScopeFilters,
    SourceScope,
    SourceSpecification,
    OutputFormat,
    NamingConfiguration,
    TargetSpecification,
    MappingRule,
    DMGenerationOptions,
    SecurityConfiguration,
    TransformationOptions,
    TransformationSpecification,
    BREXValidation,
    SchemaValidation,
    TraceValidation,
    CustomValidationRule,
    ValidationSpecification,
    NotificationConfig,
    ExecutionSpecification,
    ArchiveConfiguration,
    MetadataConfiguration,
    OutputSpecification,
    RevisionEntry,
)

# Import baselines components (enhanced baseline management)
from .baselines import (
    BaselineArtifact,
    BaselineScope,
    BaselineDelta,
    ArtifactStatus,
    BaselineManager,
    BaselineError,
    BaselineIntegrityError,
    BaselineStateError,
)


class Governance:
    """
    ASIT Governance controller.
    
    Manages baselines, contracts, and change control.
    Delegates to GovernanceController for full functionality.
    """
    
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self._controller: Optional[GovernanceController] = None
        self._contract_manager: Optional[ContractManager] = None
        self._baseline_manager: Optional[BaselineManager] = None
        
    @property
    def controller(self) -> GovernanceController:
        """Lazy-load the governance controller."""
        if self._controller is None:
            # Resolve ASIT root from config path
            asit_root = self.config_path.parent.parent
            self._controller = GovernanceController(asit_root)
        return self._controller
    
    @property
    def contracts(self) -> ContractManager:
        """Lazy-load the contract manager."""
        if self._contract_manager is None:
            asit_root = self.config_path.parent.parent
            self._contract_manager = ContractManager(asit_root / "CONTRACTS")
        return self._contract_manager
    
    @property
    def baselines(self) -> BaselineManager:
        """Lazy-load the baseline manager."""
        if self._baseline_manager is None:
            asit_root = self.config_path.parent.parent
            self._baseline_manager = BaselineManager(asit_root / "GOVERNANCE")
        return self._baseline_manager
        
    def get_contract(self, contract_id: str) -> Contract:
        """Retrieve contract by ID."""
        return self.contracts.get_contract(contract_id)
        
    def get_baseline(self, baseline_id: str) -> Baseline:
        """Retrieve baseline by ID."""
        return self.baselines.get_baseline(baseline_id)
        
    def validate_execution_authority(
        self, 
        contract: Contract, 
        baseline: Baseline
    ) -> bool:
        """
        Validate that execution is authorized.
        
        ASIGT calls this before any generation.
        """
        return self.controller.can_execute_transformation(
            contract_id=contract.id,
            contract_status=contract.status.value,
            baseline_id=baseline.id
        )


class ASIT:
    """
    Main ASIT interface.
    
    The governance, structure, and lifecycle authority layer.
    
    Usage:
        >>> asit = ASIT(config_path="ASIT/config/asit_config.yaml")
        >>> contract = asit.get_contract("KITDM-CTR-LM-CSDB_ATA28")
        >>> if contract.is_executable():
        ...     # Pass to ASIGT for execution
        ...     pass
    """
    
    def __init__(self, config_path: Path | str):
        self.config_path = Path(config_path)
        self.governance = Governance(self.config_path)
        
    def get_contract(self, contract_id: str) -> Contract:
        """Get contract by ID."""
        return self.governance.get_contract(contract_id)
        
    def get_baseline(self, baseline_id: str) -> Baseline:
        """Get baseline by ID."""
        return self.governance.get_baseline(baseline_id)
        
    def authorize_execution(
        self, 
        contract: Contract, 
        baseline: Baseline
    ) -> bool:
        """
        Authorize ASIGT execution.
        
        Returns True only if:
        - Contract is APPROVED
        - Baseline exists and is valid
        - Authority requirements are met
        """
        return self.governance.validate_execution_authority(contract, baseline)


__all__ = [
    # Main interface
    "ASIT",
    "Governance",
    
    # Re-exported from governance module
    "Baseline",
    "BaselineType",
    "BaselineState",
    "BaselineContent",
    "BaselineEffectivity",
    "BaselineAuthority",
    "ChangeRequest",
    "ChangeRequestStatus",
    "ChangeOrder",
    "ChangeOrderStatus",
    "ChangeClassification",
    "ApprovalState",
    "StakeholderRole",
    "Stakeholder",
    "ApprovalMatrix",
    "ApprovalRequirement",
    "ApprovalRecord",
    "GovernanceController",
    "GovernanceError",
    "BaselineNotFoundError",
    "AuthorizationError",
    
    # Re-exported from contracts module
    "Contract",
    "ContractStatus",
    "ContractCategory",
    "ContractHeader",
    "ContractAuthority",
    "ContractManager",
    "ContractError",
    "ContractNotFoundError",
    "ContractValidationError",
    "ExecutionMode",
    "ErrorHandling",
    "SeverityThreshold",
    "PublicationType",
    "OutputType",
    "S1000DVersion",
    "BaselineReference",
    "ScopeFilters",
    "SourceScope",
    "SourceSpecification",
    "OutputFormat",
    "NamingConfiguration",
    "TargetSpecification",
    "MappingRule",
    "DMGenerationOptions",
    "SecurityConfiguration",
    "TransformationOptions",
    "TransformationSpecification",
    "BREXValidation",
    "SchemaValidation",
    "TraceValidation",
    "CustomValidationRule",
    "ValidationSpecification",
    "NotificationConfig",
    "ExecutionSpecification",
    "ArchiveConfiguration",
    "MetadataConfiguration",
    "OutputSpecification",
    "RevisionEntry",
    
    # Re-exported from baselines module
    "BaselineArtifact",
    "BaselineScope",
    "BaselineDelta",
    "ArtifactStatus",
    "BaselineManager",
    "BaselineError",
    "BaselineIntegrityError",
    "BaselineStateError",
]
