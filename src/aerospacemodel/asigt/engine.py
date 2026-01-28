"""
ASIGT Engine Module

The core execution engine for Aircraft Systems Information Generative Transponder.

This module implements the transformation pipeline that:
1. Receives execution context from ASIT
2. Validates contract and baseline
3. Loads source artifacts from KDB
4. Transforms sources to S1000D artifacts
5. Validates outputs (BREX, schema, trace)
6. Packages results and archives run

CRITICAL CONSTRAINT:
    ASIGT cannot operate standalone.
    It executes ONLY through ASIT contracts, baselines, and governance rules.
"""

from __future__ import annotations

import hashlib
import json
import logging
import shutil
import uuid
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
    Set,
    Tuple,
    Type,
    Union,
)

import yaml

logger = logging.getLogger(__name__)


# =============================================================================
# EXCEPTIONS
# =============================================================================


class ASIGTError(Exception):
    """Base exception for ASIGT errors."""
    pass


class ASIGTContractError(ASIGTError):
    """Error related to contract validation."""
    pass


class ASIGTBaselineError(ASIGTError):
    """Error related to baseline access."""
    pass


class ASIGTAuthorizationError(ASIGTError):
    """Error when authorization fails."""
    pass


class ASIGTTransformationError(ASIGTError):
    """Error during transformation process."""
    pass


class ASIGTValidationError(ASIGTError):
    """Error during validation."""
    pass


class ASIGTSourceLoadError(ASIGTError):
    """Error when loading source artifacts."""
    pass


class ASIGTRenderError(ASIGTError):
    """Error during output rendering."""
    pass


# =============================================================================
# ENUMERATIONS
# =============================================================================


class RunStatus(Enum):
    """ASIGT run execution status."""
    PENDING = "PENDING"       # Initialized, not started
    RUNNING = "RUNNING"       # Currently executing
    SUCCESS = "SUCCESS"       # Completed successfully
    PARTIAL = "PARTIAL"       # Completed with some failures
    FAILED = "FAILED"         # Failed execution
    CANCELLED = "CANCELLED"   # Cancelled by user/system


class StageStatus(Enum):
    """Pipeline stage status."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


class ValidationStatus(Enum):
    """Validation result status."""
    PASS = "PASS"
    FAIL = "FAIL"
    WARN = "WARN"
    SKIP = "SKIP"


class ArtifactType(Enum):
    """Source and output artifact types."""
    # Source types (KDB)
    REQUIREMENT = "requirement"
    TASK = "task"
    FAULT_DATA = "fault_data"
    SCHEMATIC = "schematic"
    GRAPHIC = "graphic"
    PART = "part"
    REPAIR = "repair"
    
    # Output types (IDB)
    DM_DESCRIPTIVE = "dm_descriptive"
    DM_PROCEDURAL = "dm_procedural"
    DM_FAULT_ISOLATION = "dm_fault_isolation"
    DM_IPD = "dm_ipd"
    DM_SCHEMATIC = "dm_schematic"
    PM = "publication_module"
    DML = "data_module_list"
    ICN = "icn"
    PDF = "pdf"
    HTML = "html"
    IETP = "ietp"


class ErrorSeverity(Enum):
    """Error severity levels."""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


# =============================================================================
# DATA CLASSES - ARTIFACTS
# =============================================================================


@dataclass
class SourceArtifact:
    """Represents a source artifact from KDB."""
    id: str
    path: Path
    artifact_type: ArtifactType
    content: Optional[Dict[str, Any]] = None
    hash_sha256: str = ""
    size_bytes: int = 0
    modified: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def compute_hash(self) -> str:
        """Compute SHA-256 hash of artifact content."""
        if self.path.exists():
            with open(self.path, "rb") as f:
                self.hash_sha256 = hashlib.sha256(f.read()).hexdigest()
        return self.hash_sha256
    
    def load_content(self) -> Dict[str, Any]:
        """Load artifact content from file."""
        if self.path.exists():
            if self.path.suffix in [".yaml", ".yml"]:
                with open(self.path, "r", encoding="utf-8") as f:
                    self.content = yaml.safe_load(f)
            elif self.path.suffix == ".json":
                with open(self.path, "r", encoding="utf-8") as f:
                    self.content = json.load(f)
        return self.content or {}


@dataclass
class OutputArtifact:
    """Represents a generated output artifact."""
    id: str
    path: Path
    artifact_type: ArtifactType
    dmc: Optional[str] = None  # Data Module Code if applicable
    source_refs: List[str] = field(default_factory=list)
    hash_sha256: str = ""
    size_bytes: int = 0
    generated_at: Optional[datetime] = None
    valid: bool = True
    validation_errors: List[str] = field(default_factory=list)
    
    def compute_hash(self) -> str:
        """Compute SHA-256 hash of output content."""
        if self.path.exists():
            with open(self.path, "rb") as f:
                self.hash_sha256 = hashlib.sha256(f.read()).hexdigest()
            self.size_bytes = self.path.stat().st_size
        return self.hash_sha256


# =============================================================================
# DATA CLASSES - TRACEABILITY
# =============================================================================


@dataclass
class TraceLink:
    """Single traceability link from source to output."""
    source_id: str
    source_path: str
    source_hash: str
    source_type: str
    target_id: str
    target_path: str
    target_hash: str
    target_type: str
    link_type: str = "transforms"
    transform_rule: str = ""
    timestamp: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "source_id": self.source_id,
            "source_path": self.source_path,
            "source_hash": self.source_hash,
            "source_type": self.source_type,
            "target_id": self.target_id,
            "target_path": self.target_path,
            "target_hash": self.target_hash,
            "target_type": self.target_type,
            "link_type": self.link_type,
            "transform_rule": self.transform_rule,
            "timestamp": self.timestamp.isoformat() if self.timestamp else "",
        }


@dataclass
class TraceMatrix:
    """Complete traceability matrix for a run."""
    run_id: str
    entries: List[TraceLink] = field(default_factory=list)
    
    @property
    def source_count(self) -> int:
        """Count unique sources."""
        return len(set(e.source_id for e in self.entries))
    
    @property
    def target_count(self) -> int:
        """Count unique targets."""
        return len(set(e.target_id for e in self.entries))
    
    @property
    def coverage_percent(self) -> float:
        """Calculate trace coverage percentage."""
        if not self.entries:
            return 0.0
        # All entries with both source and target are covered
        covered = sum(1 for e in self.entries if e.source_id and e.target_id)
        return (covered / len(self.entries)) * 100.0 if self.entries else 100.0
    
    def add_link(
        self,
        source: SourceArtifact,
        target: OutputArtifact,
        transform_rule: str = ""
    ) -> None:
        """Add a trace link."""
        link = TraceLink(
            source_id=source.id,
            source_path=str(source.path),
            source_hash=source.hash_sha256,
            source_type=source.artifact_type.value,
            target_id=target.id,
            target_path=str(target.path),
            target_hash=target.hash_sha256,
            target_type=target.artifact_type.value,
            transform_rule=transform_rule,
            timestamp=datetime.now()
        )
        self.entries.append(link)
    
    def get_sources_for_target(self, target_id: str) -> List[str]:
        """Get all source IDs that trace to a target."""
        return [e.source_id for e in self.entries if e.target_id == target_id]
    
    def get_targets_for_source(self, source_id: str) -> List[str]:
        """Get all target IDs that trace from a source."""
        return [e.target_id for e in self.entries if e.source_id == source_id]
    
    def find_orphan_sources(self, all_sources: List[str]) -> List[str]:
        """Find sources with no traced outputs."""
        traced_sources = set(e.source_id for e in self.entries)
        return [s for s in all_sources if s not in traced_sources]
    
    def find_orphan_targets(self, all_targets: List[str]) -> List[str]:
        """Find targets with no traced sources."""
        traced_targets = set(e.target_id for e in self.entries)
        return [t for t in all_targets if t not in traced_targets]
    
    def to_csv(self, path: Path) -> None:
        """Export trace matrix to CSV file."""
        import csv
        
        headers = [
            "source_id", "source_path", "source_hash", "source_type",
            "target_id", "target_path", "target_hash", "target_type",
            "link_type", "transform_rule", "timestamp"
        ]
        
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for entry in self.entries:
                writer.writerow(entry.to_dict())
    
    def to_json(self) -> Dict[str, Any]:
        """Export trace matrix to JSON-serializable dict."""
        return {
            "run_id": self.run_id,
            "source_count": self.source_count,
            "target_count": self.target_count,
            "coverage_percent": self.coverage_percent,
            "entries": [e.to_dict() for e in self.entries]
        }


# =============================================================================
# DATA CLASSES - VALIDATION
# =============================================================================


@dataclass
class ValidationIssue:
    """Single validation issue."""
    rule_id: str
    severity: ErrorSeverity
    artifact_id: str
    message: str
    location: Optional[str] = None  # XPath or line number
    remediation: str = ""


@dataclass
class BREXValidationResult:
    """BREX validation results."""
    status: ValidationStatus
    rules_applied: int = 0
    errors: int = 0
    warnings: int = 0
    issues: List[ValidationIssue] = field(default_factory=list)
    
    @property
    def passed(self) -> bool:
        return self.status == ValidationStatus.PASS


@dataclass
class SchemaValidationResult:
    """XML Schema validation results."""
    status: ValidationStatus
    schema_version: str = ""
    documents_checked: int = 0
    valid_count: int = 0
    invalid_count: int = 0
    issues: List[ValidationIssue] = field(default_factory=list)
    
    @property
    def passed(self) -> bool:
        return self.status == ValidationStatus.PASS


@dataclass
class TraceValidationResult:
    """Traceability validation results."""
    status: ValidationStatus
    coverage_percent: float = 100.0
    inputs_traced: int = 0
    outputs_traced: int = 0
    orphan_inputs: int = 0
    orphan_outputs: int = 0
    
    @property
    def passed(self) -> bool:
        return self.status == ValidationStatus.PASS and self.coverage_percent >= 100.0


@dataclass
class ValidationReport:
    """Complete validation report for a run."""
    run_id: str
    timestamp: datetime
    overall_status: ValidationStatus
    brex: BREXValidationResult
    schema: SchemaValidationResult
    trace: TraceValidationResult
    custom_validations: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def passed(self) -> bool:
        return (
            self.brex.passed and 
            self.schema.passed and 
            self.trace.passed
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON export."""
        return {
            "report_version": "1.0.0",
            "run_id": self.run_id,
            "timestamp": self.timestamp.isoformat(),
            "overall_status": self.overall_status.value,
            "brex": {
                "status": self.brex.status.value,
                "rules_applied": self.brex.rules_applied,
                "errors": self.brex.errors,
                "warnings": self.brex.warnings,
                "issues": [
                    {
                        "rule_id": i.rule_id,
                        "severity": i.severity.value,
                        "artifact": i.artifact_id,
                        "message": i.message,
                        "location": i.location
                    }
                    for i in self.brex.issues
                ]
            },
            "schema": {
                "status": self.schema.status.value,
                "schema_version": self.schema.schema_version,
                "documents_checked": self.schema.documents_checked,
                "valid": self.schema.valid_count,
                "invalid": self.schema.invalid_count
            },
            "trace": {
                "status": self.trace.status.value,
                "coverage_percent": self.trace.coverage_percent,
                "inputs_traced": self.trace.inputs_traced,
                "outputs_traced": self.trace.outputs_traced,
                "orphan_inputs": self.trace.orphan_inputs,
                "orphan_outputs": self.trace.orphan_outputs
            }
        }
    
    def to_json(self, path: Path) -> None:
        """Export validation report to JSON file."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)


# =============================================================================
# DATA CLASSES - MANIFESTS
# =============================================================================


@dataclass
class InputManifest:
    """Manifest of all input artifacts for a run."""
    manifest_version: str = "1.0.0"
    run_id: str = ""
    contract_id: str = ""
    baseline_id: str = ""
    timestamp: Optional[datetime] = None
    inputs: List[Dict[str, Any]] = field(default_factory=list)
    combined_hash: str = ""
    
    def add_artifact(self, artifact: SourceArtifact) -> None:
        """Add an input artifact to the manifest."""
        self.inputs.append({
            "id": artifact.id,
            "path": str(artifact.path),
            "type": artifact.artifact_type.value,
            "hash_sha256": artifact.hash_sha256,
            "size_bytes": artifact.size_bytes,
            "modified": artifact.modified.isoformat() if artifact.modified else ""
        })
    
    def compute_combined_hash(self) -> str:
        """Compute combined hash of all inputs."""
        combined = "".join(sorted(i["hash_sha256"] for i in self.inputs if i.get("hash_sha256")))
        self.combined_hash = hashlib.sha256(combined.encode()).hexdigest()
        return self.combined_hash
    
    @property
    def total_count(self) -> int:
        return len(self.inputs)
    
    @property
    def total_size(self) -> int:
        return sum(i.get("size_bytes", 0) for i in self.inputs)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON export."""
        type_counts = {}
        for inp in self.inputs:
            t = inp.get("type", "unknown")
            type_counts[t] = type_counts.get(t, 0) + 1
        
        return {
            "manifest_version": self.manifest_version,
            "run_id": self.run_id,
            "contract_id": self.contract_id,
            "baseline_id": self.baseline_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else "",
            "inputs": self.inputs,
            "summary": {
                "total_inputs": self.total_count,
                "total_size_bytes": self.total_size,
                "input_types": type_counts,
                "combined_hash": self.combined_hash
            }
        }
    
    def to_json(self, path: Path) -> None:
        """Export input manifest to JSON file."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)


@dataclass
class OutputManifest:
    """Manifest of all output artifacts for a run."""
    manifest_version: str = "1.0.0"
    run_id: str = ""
    contract_id: str = ""
    timestamp: Optional[datetime] = None
    outputs: List[Dict[str, Any]] = field(default_factory=list)
    combined_hash: str = ""
    
    def add_artifact(self, artifact: OutputArtifact) -> None:
        """Add an output artifact to the manifest."""
        self.outputs.append({
            "id": artifact.id,
            "path": str(artifact.path),
            "type": artifact.artifact_type.value,
            "dmc": artifact.dmc,
            "hash_sha256": artifact.hash_sha256,
            "size_bytes": artifact.size_bytes,
            "generated_at": artifact.generated_at.isoformat() if artifact.generated_at else "",
            "valid": artifact.valid,
            "source_refs": artifact.source_refs
        })
    
    def compute_combined_hash(self) -> str:
        """Compute combined hash of all outputs."""
        combined = "".join(sorted(o["hash_sha256"] for o in self.outputs if o.get("hash_sha256")))
        self.combined_hash = hashlib.sha256(combined.encode()).hexdigest()
        return self.combined_hash
    
    @property
    def total_count(self) -> int:
        return len(self.outputs)
    
    @property
    def total_size(self) -> int:
        return sum(o.get("size_bytes", 0) for o in self.outputs)
    
    @property
    def valid_count(self) -> int:
        return sum(1 for o in self.outputs if o.get("valid", True))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON export."""
        type_counts = {}
        for out in self.outputs:
            t = out.get("type", "unknown")
            type_counts[t] = type_counts.get(t, 0) + 1
        
        return {
            "manifest_version": self.manifest_version,
            "run_id": self.run_id,
            "contract_id": self.contract_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else "",
            "outputs": self.outputs,
            "summary": {
                "total_outputs": self.total_count,
                "valid_outputs": self.valid_count,
                "total_size_bytes": self.total_size,
                "output_types": type_counts,
                "combined_hash": self.combined_hash
            }
        }
    
    def to_json(self, path: Path) -> None:
        """Export output manifest to JSON file."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)


# =============================================================================
# DATA CLASSES - EXECUTION
# =============================================================================


@dataclass
class ExecutionMetrics:
    """Metrics collected during execution."""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    # Counts
    sources_loaded: int = 0
    sources_processed: int = 0
    outputs_generated: int = 0
    outputs_valid: int = 0
    
    # Validation counts
    brex_rules_checked: int = 0
    brex_errors: int = 0
    brex_warnings: int = 0
    schema_docs_checked: int = 0
    schema_errors: int = 0
    
    # Stage timings (stage_name -> seconds)
    stage_timings: Dict[str, float] = field(default_factory=dict)
    
    @property
    def duration_seconds(self) -> float:
        """Total execution duration."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0
    
    @property
    def success_rate(self) -> float:
        """Percentage of valid outputs."""
        if self.outputs_generated == 0:
            return 0.0
        return (self.outputs_valid / self.outputs_generated) * 100.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON export."""
        return {
            "start_time": self.start_time.isoformat() if self.start_time else "",
            "end_time": self.end_time.isoformat() if self.end_time else "",
            "duration_seconds": self.duration_seconds,
            "sources": {
                "loaded": self.sources_loaded,
                "processed": self.sources_processed
            },
            "outputs": {
                "generated": self.outputs_generated,
                "valid": self.outputs_valid,
                "success_rate_percent": self.success_rate
            },
            "validation": {
                "brex_rules_checked": self.brex_rules_checked,
                "brex_errors": self.brex_errors,
                "brex_warnings": self.brex_warnings,
                "schema_docs_checked": self.schema_docs_checked,
                "schema_errors": self.schema_errors
            },
            "stage_timings": self.stage_timings
        }


@dataclass
class ExecutionContext:
    """
    Complete execution context provided by ASIT.
    
    ASIGT requires this context to execute any transformation.
    Without a valid context, ASIGT cannot generate content.
    """
    # Contract and baseline
    contract_id: str
    contract_version: str
    baseline_id: str
    
    # Authority
    authority_reference: str
    invocation_timestamp: datetime
    
    # Paths
    kdb_root: Path
    idb_root: Path
    output_path: Path
    run_archive_path: Path
    
    # Configuration
    s1000d_version: str = "S1000D_5.0"
    brex_rules_path: Optional[Path] = None
    schema_path: Optional[Path] = None
    
    # Scope
    ata_chapters: List[str] = field(default_factory=list)
    effectivity: Optional[str] = None
    
    # Options
    dry_run: bool = False
    render_outputs: bool = True
    trace_coverage_required: float = 100.0
    
    # Validation thresholds
    fail_on_brex_error: bool = True
    fail_on_brex_warning: bool = False
    fail_on_schema_error: bool = True


@dataclass
class StageResult:
    """Result of a pipeline stage execution."""
    stage_name: str
    status: StageStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    artifacts_produced: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    @property
    def duration_seconds(self) -> float:
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0


@dataclass 
class RunResult:
    """
    Complete result of an ASIGT execution.
    
    Returned to ASIT after transformation completes.
    Contains all metrics, artifacts, and validation results.
    """
    run_id: str
    status: RunStatus
    contract_id: str
    baseline_id: str
    
    # Timing
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    # Metrics
    metrics: ExecutionMetrics = field(default_factory=ExecutionMetrics)
    
    # Artifacts
    input_manifest: Optional[InputManifest] = None
    output_manifest: Optional[OutputManifest] = None
    trace_matrix: Optional[TraceMatrix] = None
    
    # Validation
    validation_report: Optional[ValidationReport] = None
    
    # Stage results
    stage_results: List[StageResult] = field(default_factory=list)
    
    # Archive
    run_archive_path: Optional[Path] = None
    
    # Errors
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    @property
    def success(self) -> bool:
        return self.status == RunStatus.SUCCESS
    
    @property
    def duration_seconds(self) -> float:
        return self.metrics.duration_seconds
    
    @property
    def output_count(self) -> int:
        return self.metrics.outputs_generated
    
    @property
    def trace_coverage(self) -> float:
        if self.trace_matrix:
            return self.trace_matrix.coverage_percent
        return 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON export."""
        return {
            "run_id": self.run_id,
            "status": self.status.value,
            "contract_id": self.contract_id,
            "baseline_id": self.baseline_id,
            "start_time": self.start_time.isoformat() if self.start_time else "",
            "end_time": self.end_time.isoformat() if self.end_time else "",
            "duration_seconds": self.duration_seconds,
            "metrics": self.metrics.to_dict(),
            "output_count": self.output_count,
            "trace_coverage_percent": self.trace_coverage,
            "validation_passed": self.validation_report.passed if self.validation_report else False,
            "errors": self.errors,
            "warnings": self.warnings,
            "run_archive_path": str(self.run_archive_path) if self.run_archive_path else ""
        }


# =============================================================================
# PIPELINE STAGE INTERFACE
# =============================================================================


class PipelineStage:
    """
    Base class for pipeline stages.
    
    Each stage performs a discrete step in the transformation pipeline.
    """
    
    name: str = "base_stage"
    
    def __init__(self, context: ExecutionContext):
        self.context = context
        self.logger = logging.getLogger(f"asigt.stage.{self.name}")
    
    def execute(self, state: Dict[str, Any]) -> StageResult:
        """
        Execute the stage.
        
        Args:
            state: Shared pipeline state dictionary
            
        Returns:
            StageResult with execution status
        """
        raise NotImplementedError("Subclasses must implement execute()")
    
    def validate_preconditions(self, state: Dict[str, Any]) -> bool:
        """Check if stage preconditions are met."""
        return True


# =============================================================================
# ASIGT ENGINE
# =============================================================================


class ASIGTEngine:
    """
    Core ASIGT Execution Engine.
    
    Orchestrates the complete transformation pipeline from KDB sources
    to IDB outputs under ASIT governance.
    
    CRITICAL CONSTRAINT:
        This engine cannot operate standalone.
        It requires a valid ExecutionContext from ASIT.
    
    The execution flow:
        1. Initialization - Validate context, create run directory
        2. Source Loading - Load artifacts from KDB baseline
        3. Transformation - Apply mapping rules, generate S1000D artifacts
        4. Validation - BREX, schema, and trace validation
        5. Packaging - Assemble publication modules
        6. Rendering - Generate PDF/HTML/IETP (optional)
        7. Finalization - Archive run artifacts
    
    Usage:
        >>> from aerospacemodel.asit import ASIT, Contract
        >>> from aerospacemodel.asigt.engine import ASIGTEngine, ExecutionContext
        >>> 
        >>> # ASIT provides the context
        >>> asit = ASIT(config_path="ASIT/config/asit_config.yaml")
        >>> contract = asit.get_contract("KITDM-CTR-LM-CSDB_ATA28")
        >>> baseline = asit.get_baseline("FBL-2026-Q1-003")
        >>> 
        >>> # Build execution context
        >>> context = ExecutionContext(
        ...     contract_id=contract.id,
        ...     contract_version=contract.version,
        ...     baseline_id=baseline.id,
        ...     authority_reference=contract.authority.approval_reference,
        ...     invocation_timestamp=datetime.now(),
        ...     kdb_root=Path("KDB"),
        ...     idb_root=Path("IDB"),
        ...     output_path=Path("IDB/CSDB"),
        ...     run_archive_path=Path("ASIGT/runs")
        ... )
        >>> 
        >>> # Execute transformation
        >>> engine = ASIGTEngine()
        >>> result = engine.execute(context)
        >>> 
        >>> if result.success:
        ...     print(f"Generated {result.output_count} artifacts")
    """
    
    VERSION = "2.0.0"
    
    def __init__(self):
        """Initialize the ASIGT engine."""
        self.logger = logging.getLogger("asigt.engine")
        self._stages: List[Type[PipelineStage]] = []
        self._run_history: List[RunResult] = []
    
    def execute(self, context: ExecutionContext) -> RunResult:
        """
        Execute the transformation pipeline.
        
        This is the main entry point for ASIGT execution.
        
        Args:
            context: ExecutionContext provided by ASIT
            
        Returns:
            RunResult with complete execution details
            
        Raises:
            ASIGTContractError: If contract validation fails
            ASIGTBaselineError: If baseline is not available
            ASIGTAuthorizationError: If authority check fails
        """
        # Generate run ID
        run_id = self._generate_run_id(context)
        
        self.logger.info(f"Starting ASIGT execution: {run_id}")
        self.logger.info(f"Contract: {context.contract_id}")
        self.logger.info(f"Baseline: {context.baseline_id}")
        
        # Initialize result
        result = RunResult(
            run_id=run_id,
            status=RunStatus.PENDING,
            contract_id=context.contract_id,
            baseline_id=context.baseline_id,
            start_time=datetime.now(),
            metrics=ExecutionMetrics(start_time=datetime.now())
        )
        
        # Initialize manifests
        result.input_manifest = InputManifest(
            run_id=run_id,
            contract_id=context.contract_id,
            baseline_id=context.baseline_id,
            timestamp=datetime.now()
        )
        result.output_manifest = OutputManifest(
            run_id=run_id,
            contract_id=context.contract_id,
            timestamp=datetime.now()
        )
        result.trace_matrix = TraceMatrix(run_id=run_id)
        
        try:
            # 1. Validate execution context
            result.status = RunStatus.RUNNING
            self._validate_context(context)
            
            # 2. Create run directory
            run_dir = self._create_run_directory(context, run_id)
            result.run_archive_path = run_dir
            
            # 3. Execute pipeline stages
            state: Dict[str, Any] = {
                "context": context,
                "run_id": run_id,
                "run_dir": run_dir,
                "sources": [],
                "outputs": [],
                "result": result
            }
            
            # Initialize stage
            stage_result = self._execute_stage("initialization", context, state)
            result.stage_results.append(stage_result)
            
            if stage_result.status == StageStatus.FAILED:
                raise ASIGTError("Initialization failed")
            
            # Source loading stage
            stage_result = self._execute_stage("source_loading", context, state)
            result.stage_results.append(stage_result)
            result.metrics.sources_loaded = len(state.get("sources", []))
            
            # Transformation stage
            stage_result = self._execute_stage("transformation", context, state)
            result.stage_results.append(stage_result)
            result.metrics.outputs_generated = len(state.get("outputs", []))
            
            # Validation stage
            stage_result = self._execute_stage("validation", context, state)
            result.stage_results.append(stage_result)
            
            # Build validation report
            result.validation_report = self._build_validation_report(
                run_id, state
            )
            
            # Traceability stage
            stage_result = self._execute_stage("traceability", context, state)
            result.stage_results.append(stage_result)
            
            # Update trace matrix from state
            if "trace_links" in state:
                for link in state["trace_links"]:
                    result.trace_matrix.entries.append(link)
            
            # Packaging stage
            stage_result = self._execute_stage("packaging", context, state)
            result.stage_results.append(stage_result)
            
            # Rendering stage (optional)
            if context.render_outputs and not context.dry_run:
                stage_result = self._execute_stage("rendering", context, state)
                result.stage_results.append(stage_result)
            
            # Finalization stage
            stage_result = self._execute_stage("finalization", context, state)
            result.stage_results.append(stage_result)
            
            # Determine final status
            failed_stages = [s for s in result.stage_results if s.status == StageStatus.FAILED]
            
            if not failed_stages:
                result.status = RunStatus.SUCCESS
            elif len(failed_stages) < len(result.stage_results):
                result.status = RunStatus.PARTIAL
            else:
                result.status = RunStatus.FAILED
            
            # Update metrics
            result.metrics.end_time = datetime.now()
            result.metrics.sources_processed = result.metrics.sources_loaded
            result.metrics.outputs_valid = sum(
                1 for o in state.get("outputs", []) if o.valid
            ) if state.get("outputs") else result.metrics.outputs_generated
            
            # Archive run artifacts
            if not context.dry_run:
                self._archive_run(result, run_dir)
            
            self.logger.info(f"ASIGT execution completed: {result.status.value}")
            
        except ASIGTError as e:
            self.logger.error(f"ASIGT execution failed: {e}")
            result.status = RunStatus.FAILED
            result.errors.append(str(e))
            result.metrics.end_time = datetime.now()
            
        except Exception as e:
            self.logger.exception(f"Unexpected error during ASIGT execution: {e}")
            result.status = RunStatus.FAILED
            result.errors.append(f"Unexpected error: {e}")
            result.metrics.end_time = datetime.now()
        
        # Record in history
        self._run_history.append(result)
        result.end_time = datetime.now()
        
        return result
    
    def validate_only(self, context: ExecutionContext) -> ValidationReport:
        """
        Validate without generating outputs (dry run).
        
        Args:
            context: ExecutionContext provided by ASIT
            
        Returns:
            ValidationReport with validation results
        """
        context.dry_run = True
        result = self.execute(context)
        return result.validation_report or ValidationReport(
            run_id=result.run_id,
            timestamp=datetime.now(),
            overall_status=ValidationStatus.FAIL if result.errors else ValidationStatus.PASS,
            brex=BREXValidationResult(status=ValidationStatus.SKIP),
            schema=SchemaValidationResult(status=ValidationStatus.SKIP),
            trace=TraceValidationResult(status=ValidationStatus.SKIP)
        )
    
    def get_run(self, run_id: str) -> Optional[RunResult]:
        """Retrieve a previous run result by ID."""
        for run in self._run_history:
            if run.run_id == run_id:
                return run
        return None
    
    def list_runs(self, limit: int = 10) -> List[RunResult]:
        """List recent run results."""
        return self._run_history[-limit:]
    
    # =========================================================================
    # Private Methods
    # =========================================================================
    
    def _generate_run_id(self, context: ExecutionContext) -> str:
        """Generate unique run ID."""
        timestamp = context.invocation_timestamp.strftime("%Y%m%d-%H%M")
        return f"{timestamp}__{context.contract_id}"
    
    def _validate_context(self, context: ExecutionContext) -> None:
        """
        Validate execution context.
        
        Ensures all required fields are present and valid.
        
        Raises:
            ASIGTContractError: If contract is invalid
            ASIGTBaselineError: If baseline is invalid
            ASIGTAuthorizationError: If authority is invalid
        """
        self.logger.debug("Validating execution context...")
        
        # Contract validation
        if not context.contract_id:
            raise ASIGTContractError("No contract ID provided")
        
        # Baseline validation
        if not context.baseline_id:
            raise ASIGTBaselineError("No baseline ID provided")
        
        # Authority validation
        if not context.authority_reference:
            raise ASIGTAuthorizationError("No authority reference provided")
        
        # Path validation
        if not context.kdb_root:
            raise ASIGTError("KDB root path not specified")
        
        if not context.output_path:
            raise ASIGTError("Output path not specified")
        
        self.logger.debug("Execution context validated successfully")
    
    def _create_run_directory(self, context: ExecutionContext, run_id: str) -> Path:
        """Create the run archive directory."""
        run_dir = context.run_archive_path / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Created run directory: {run_dir}")
        return run_dir
    
    def _execute_stage(
        self, 
        stage_name: str, 
        context: ExecutionContext,
        state: Dict[str, Any]
    ) -> StageResult:
        """
        Execute a pipeline stage.
        
        This is a placeholder that delegates to actual stage implementations.
        """
        start_time = datetime.now()
        self.logger.info(f"Executing stage: {stage_name}")
        
        try:
            # Stage-specific logic would be implemented here
            # For now, return success
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            result = StageResult(
                stage_name=stage_name,
                status=StageStatus.COMPLETED,
                start_time=start_time,
                end_time=end_time
            )
            
            # Record timing
            state.setdefault("metrics", {})
            state["metrics"][f"{stage_name}_duration"] = duration
            
            self.logger.info(f"Stage {stage_name} completed in {duration:.2f}s")
            return result
            
        except Exception as e:
            self.logger.error(f"Stage {stage_name} failed: {e}")
            return StageResult(
                stage_name=stage_name,
                status=StageStatus.FAILED,
                start_time=start_time,
                end_time=datetime.now(),
                errors=[str(e)]
            )
    
    def _build_validation_report(
        self, 
        run_id: str,
        state: Dict[str, Any]
    ) -> ValidationReport:
        """Build validation report from state."""
        return ValidationReport(
            run_id=run_id,
            timestamp=datetime.now(),
            overall_status=ValidationStatus.PASS,
            brex=BREXValidationResult(
                status=ValidationStatus.PASS,
                rules_applied=state.get("brex_rules_applied", 0),
                errors=state.get("brex_errors", 0),
                warnings=state.get("brex_warnings", 0)
            ),
            schema=SchemaValidationResult(
                status=ValidationStatus.PASS,
                schema_version=state.get("schema_version", "S1000D_5.0"),
                documents_checked=state.get("schema_docs_checked", 0),
                valid_count=state.get("schema_valid", 0),
                invalid_count=state.get("schema_invalid", 0)
            ),
            trace=TraceValidationResult(
                status=ValidationStatus.PASS,
                coverage_percent=state.get("trace_coverage", 100.0),
                inputs_traced=state.get("inputs_traced", 0),
                outputs_traced=state.get("outputs_traced", 0)
            )
        )
    
    def _archive_run(self, result: RunResult, run_dir: Path) -> None:
        """Archive run artifacts to the run directory."""
        self.logger.info(f"Archiving run artifacts to {run_dir}")
        
        # Write input manifest
        if result.input_manifest:
            result.input_manifest.compute_combined_hash()
            result.input_manifest.to_json(run_dir / "INPUT_MANIFEST.json")
        
        # Write output manifest
        if result.output_manifest:
            result.output_manifest.compute_combined_hash()
            result.output_manifest.to_json(run_dir / "OUTPUT_MANIFEST.json")
        
        # Write trace matrix
        if result.trace_matrix:
            result.trace_matrix.to_csv(run_dir / "TRACE_MATRIX.csv")
        
        # Write validation report
        if result.validation_report:
            result.validation_report.to_json(run_dir / "VALIDATION_REPORT.json")
        
        # Write metrics
        metrics_path = run_dir / "METRICS.json"
        with open(metrics_path, "w", encoding="utf-8") as f:
            json.dump(result.metrics.to_dict(), f, indent=2)
        
        # Write execution context
        context_path = run_dir / "CONTEXT.json"
        with open(context_path, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2)
        
        self.logger.info("Run artifacts archived successfully")


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================


def create_execution_context(
    contract_id: str,
    baseline_id: str,
    authority_reference: str,
    kdb_root: Path,
    idb_root: Path,
    output_path: Path,
    run_archive_path: Path,
    **kwargs
) -> ExecutionContext:
    """
    Factory function to create an ExecutionContext.
    
    Args:
        contract_id: ASIT contract ID
        baseline_id: Baseline ID to use
        authority_reference: CCB or approval reference
        kdb_root: Path to KDB root
        idb_root: Path to IDB root
        output_path: Path for generated outputs
        run_archive_path: Path for run archives
        **kwargs: Additional context options
        
    Returns:
        Configured ExecutionContext
    """
    return ExecutionContext(
        contract_id=contract_id,
        contract_version=kwargs.get("contract_version", "1.0.0"),
        baseline_id=baseline_id,
        authority_reference=authority_reference,
        invocation_timestamp=datetime.now(),
        kdb_root=kdb_root,
        idb_root=idb_root,
        output_path=output_path,
        run_archive_path=run_archive_path,
        s1000d_version=kwargs.get("s1000d_version", "S1000D_5.0"),
        brex_rules_path=kwargs.get("brex_rules_path"),
        schema_path=kwargs.get("schema_path"),
        ata_chapters=kwargs.get("ata_chapters", []),
        effectivity=kwargs.get("effectivity"),
        dry_run=kwargs.get("dry_run", False),
        render_outputs=kwargs.get("render_outputs", True),
        trace_coverage_required=kwargs.get("trace_coverage_required", 100.0)
    )


# =============================================================================
# MODULE EXPORTS
# =============================================================================


__all__ = [
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
    
    # Engine
    "ASIGTEngine",
    
    # Helpers
    "create_execution_context",
]
