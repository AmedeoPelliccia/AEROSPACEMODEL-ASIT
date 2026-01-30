"""
ASIGT — Aircraft Systems Information Generative Transponder

Content generation layer operating EXCLUSIVELY under ASIT control.

CONSTRAINT:
    ASIGT cannot operate standalone.
    It executes ONLY through ASIT contracts, baselines, and governance rules.

ASIGT performs:
    - S1000D artifact generation (DM, PM, DML)
    - BREX validation (including BREX Decision Engine governance)
    - Schema validation
    - Trace matrix creation
    - Output rendering (PDF, HTML, IETP)

BREX-Driven Reasoning:
    The AEROSPACEMODEL Agent's reasoning is constrained, guided, and explainable
    through a BREX ruleset. Every step is a validated decision node.
    No free-form autonomy exists.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

# Import engine components
from .engine import (
    # Exceptions
    ASIGTError,
    ASIGTContractError,
    ASIGTBaselineError,
    ASIGTAuthorizationError,
    ASIGTTransformationError,
    ASIGTValidationError,
    ASIGTSourceLoadError,
    ASIGTRenderError,
    
    # Enumerations
    RunStatus,
    StageStatus,
    ValidationStatus,
    ArtifactType,
    ErrorSeverity,
    
    # Artifacts
    SourceArtifact,
    OutputArtifact,
    
    # Traceability
    TraceLink,
    TraceMatrix,
    
    # Validation
    ValidationIssue,
    BREXValidationResult,
    SchemaValidationResult,
    TraceValidationResult,
    ValidationReport,
    
    # Manifests
    InputManifest,
    OutputManifest,
    
    # Execution
    ExecutionMetrics,
    ExecutionContext,
    StageResult,
    RunResult,
    
    # Pipeline
    PipelineStage,
    
    # Engine
    ASIGTEngine,
    
    # Helpers
    create_execution_context,
)

# Import BREX governance components
from .brex_governance import (
    OperationContext,
    GovernedValidationResult,
    BREXGovernedValidator,
    validate_governed_operation,
    is_operation_allowed,
    OPERATION_RULES,
)

# Conditional imports to avoid circular dependencies
if TYPE_CHECKING:
    from aerospacemodel.asit import ASIT, Contract, Baseline


class ASIGT:
    """
    Main ASIGT interface — Content Generation Engine.
    
    CONSTRAINT:
        ASIGT cannot operate standalone.
        It MUST be initialized with an ASIT instance.
        It can ONLY execute approved contracts.
    
    This class provides a high-level interface to the ASIGTEngine,
    handling ASIT integration and contract validation.
    
    Usage:
        >>> from aerospacemodel import ASIT, ASIGT, Contract
        >>> 
        >>> # ASIT governs
        >>> asit = ASIT(config_path="ASIT/config/asit_config.yaml")
        >>> contract = asit.get_contract("KITDM-CTR-LM-CSDB_ATA28")
        >>> 
        >>> # ASIGT executes under ASIT control
        >>> asigt = ASIGT(asit_instance=asit)
        >>> result = asigt.execute(contract, baseline_id="FBL-2026-Q1-003")
        >>> 
        >>> if result.success:
        ...     print(f"Generated {result.output_count} artifacts")
    """
    
    VERSION = "2.0.0"
    
    def __init__(self, asit_instance: "ASIT"):
        """
        Initialize ASIGT with ASIT governance instance.
        
        Args:
            asit_instance: The ASIT instance that governs this ASIGT.
                           ASIGT cannot be created without ASIT.
        
        Raises:
            ASIGTError: If asit_instance is None.
        """
        if asit_instance is None:
            raise ASIGTError(
                "ASIGT cannot operate standalone. "
                "It must be initialized with an ASIT instance."
            )
        self.asit = asit_instance
        self._engine = ASIGTEngine()
        self._runs: List[RunResult] = []
    
    @property
    def engine(self) -> ASIGTEngine:
        """Access the underlying engine."""
        return self._engine
    
    def execute(
        self, 
        contract: "Contract",
        baseline_id: str = "LATEST",
        dry_run: bool = False,
        render_outputs: bool = True,
        **kwargs
    ) -> RunResult:
        """
        Execute content generation under ASIT contract.
        
        This is the main entry point for ASIGT operations.
        
        Args:
            contract: The ASIT contract defining the transformation.
            baseline_id: The baseline to use (or "LATEST").
            dry_run: If True, validate only without writing outputs.
            render_outputs: If True, generate PDF/HTML/IETP outputs.
            **kwargs: Additional execution options.
        
        Returns:
            RunResult with execution status and metrics.
        
        Raises:
            ASIGTError: If contract is not approved or baseline doesn't exist.
        """
        # 1. Validate contract is approved
        if not contract.is_executable():
            raise ASIGTContractError(
                f"Contract {contract.id} is not approved. "
                f"Current status: {contract.status.value}. "
                "ASIGT can only execute APPROVED contracts."
            )
        
        # 2. Load and validate baseline
        baseline = self.asit.get_baseline(baseline_id)
        if baseline is None:
            raise ASIGTBaselineError(f"Baseline not found: {baseline_id}")
        
        # 3. Verify ASIT authorization
        if not self.asit.authorize_execution(contract, baseline):
            raise ASIGTAuthorizationError("ASIT authorization failed")
        
        # 4. Build execution context
        context = self._build_execution_context(
            contract=contract,
            baseline=baseline,
            dry_run=dry_run,
            render_outputs=render_outputs,
            **kwargs
        )
        
        # 5. Execute via engine
        result = self._engine.execute(context)
        
        # 6. Store result
        self._runs.append(result)
        
        return result
    
    def validate(
        self, 
        contract: "Contract", 
        baseline_id: str
    ) -> ValidationReport:
        """
        Validate without generating outputs.
        
        Equivalent to execute() with dry_run=True.
        
        Args:
            contract: The ASIT contract defining the transformation.
            baseline_id: The baseline to use.
            
        Returns:
            ValidationReport with validation results.
        """
        result = self.execute(contract, baseline_id, dry_run=True)
        return result.validation_report or ValidationReport(
            run_id=result.run_id,
            timestamp=datetime.now(),
            overall_status=ValidationStatus.FAIL if result.errors else ValidationStatus.PASS,
            brex=BREXValidationResult(status=ValidationStatus.SKIP),
            schema=SchemaValidationResult(status=ValidationStatus.SKIP),
            trace=TraceValidationResult(status=ValidationStatus.SKIP)
        )
    
    def get_run(self, run_id: str) -> Optional[RunResult]:
        """Retrieve a previous run by ID."""
        # Check local cache first
        for run in self._runs:
            if run.run_id == run_id:
                return run
        # Check engine history
        return self._engine.get_run(run_id)
    
    def list_runs(self, limit: int = 10) -> List[RunResult]:
        """List recent run results."""
        return self._runs[-limit:]
    
    def _build_execution_context(
        self,
        contract: "Contract",
        baseline: "Baseline",
        dry_run: bool = False,
        render_outputs: bool = True,
        **kwargs
    ) -> ExecutionContext:
        """Build execution context from contract and baseline."""
        # Get paths from ASIT config
        config_path = self.asit.config_path
        asit_root = config_path.parent.parent
        project_root = asit_root.parent
        
        # Default paths
        kdb_root = kwargs.get("kdb_root", project_root / "KDB")
        idb_root = kwargs.get("idb_root", project_root / "IDB")
        output_path = kwargs.get("output_path", idb_root / "CSDB")
        run_archive_path = kwargs.get("run_archive_path", project_root / "ASIGT" / "runs")
        
        # Extract ATA chapters from contract scope if available
        ata_chapters = kwargs.get("ata_chapters", [])
        if hasattr(contract, "source") and contract.source:
            if hasattr(contract.source, "scope") and contract.source.scope:
                ata_chapters = contract.source.scope.ata_chapters or []
        
        # Get authority reference
        authority_ref = ""
        if hasattr(contract, "authority") and contract.authority:
            authority_ref = contract.authority.approval_reference or ""
        
        return ExecutionContext(
            contract_id=contract.id,
            contract_version=getattr(contract, "version", "1.0.0"),
            baseline_id=baseline.id,
            authority_reference=authority_ref,
            invocation_timestamp=datetime.now(),
            kdb_root=kdb_root,
            idb_root=idb_root,
            output_path=output_path,
            run_archive_path=run_archive_path,
            s1000d_version=kwargs.get("s1000d_version", "S1000D_5.0"),
            brex_rules_path=kwargs.get("brex_rules_path"),
            schema_path=kwargs.get("schema_path"),
            ata_chapters=ata_chapters,
            effectivity=kwargs.get("effectivity"),
            dry_run=dry_run,
            render_outputs=render_outputs,
            trace_coverage_required=kwargs.get("trace_coverage_required", 100.0)
        )


__all__ = [
    # Main interface
    "ASIGT",
    
    # Re-exported from engine
    "ASIGTEngine",
    
    # Exceptions
    "ASIGTError",
    "ASIGTContractError",
    "ASIGTBaselineError",
    "ASIGTAuthorizationError",
    "ASIGTTransformationError",
    "ASIGTValidationError",
    "ASIGTSourceLoadError",
    "ASIGTRenderError",
    
    # Enumerations
    "RunStatus",
    "StageStatus",
    "ValidationStatus",
    "ArtifactType",
    "ErrorSeverity",
    
    # Artifacts
    "SourceArtifact",
    "OutputArtifact",
    
    # Traceability
    "TraceLink",
    "TraceMatrix",
    
    # Validation
    "ValidationIssue",
    "BREXValidationResult",
    "SchemaValidationResult",
    "TraceValidationResult",
    "ValidationReport",
    
    # Manifests
    "InputManifest",
    "OutputManifest",
    
    # Execution
    "ExecutionMetrics",
    "ExecutionContext",
    "StageResult",
    "RunResult",
    
    # Pipeline
    "PipelineStage",
    
    # Helpers
    "create_execution_context",
    
    # BREX Governance (Guided Reasoning)
    "OperationContext",
    "GovernedValidationResult",
    "BREXGovernedValidator",
    "validate_governed_operation",
    "is_operation_allowed",
    "OPERATION_RULES",
]
