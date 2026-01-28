"""
ASIT Contracts Module

Defines and manages transformation contracts that govern how ASIGT
transforms KDB knowledge into IDB publications.

Every ASIGT execution requires an approved contract.
No transformation without a contract. No contract without authority.
"""

from __future__ import annotations

import hashlib
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

import yaml

logger = logging.getLogger(__name__)


# =============================================================================
# ENUMERATIONS
# =============================================================================


class ContractStatus(Enum):
    """Contract lifecycle states."""
    DRAFT = "DRAFT"           # Under development, editable
    REVIEW = "REVIEW"         # Submitted for approval
    APPROVED = "APPROVED"     # CCB approved, executable
    ACTIVE = "ACTIVE"         # Currently in use, executable
    SUPERSEDED = "SUPERSEDED" # Replaced by newer version
    WITHDRAWN = "WITHDRAWN"   # Cancelled


class ContractCategory(Enum):
    """Contract categories."""
    LM = "LM"       # Lifecycle Management
    OPS = "OPS"     # Operations
    MRO = "MRO"     # Maintenance, Repair, Overhaul
    TRN = "TRN"     # Training
    CERT = "CERT"   # Certification


class ExecutionMode(Enum):
    """Contract execution modes."""
    FULL = "FULL"             # Full regeneration
    INCREMENTAL = "INCREMENTAL"  # Only changed sources
    DELTA = "DELTA"           # Generate delta publication


class ErrorHandling(Enum):
    """Error handling behavior during execution."""
    STOP = "STOP"         # Stop on first error
    CONTINUE = "CONTINUE" # Continue processing, collect errors
    ROLLBACK = "ROLLBACK" # Rollback all changes on error


class SeverityThreshold(Enum):
    """Validation severity thresholds."""
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class PublicationType(Enum):
    """Target publication types."""
    AMM = "AMM"     # Aircraft Maintenance Manual
    SRM = "SRM"     # Structural Repair Manual
    CMM = "CMM"     # Component Maintenance Manual
    IPC = "IPC"     # Illustrated Parts Catalog
    FCOM = "FCOM"   # Flight Crew Operating Manual
    TSM = "TSM"     # Troubleshooting Manual
    WDM = "WDM"     # Wiring Diagram Manual
    SB = "SB"       # Service Bulletins
    IETP = "IETP"   # Interactive Electronic Technical Publication
    CSDB = "CSDB"   # Common Source Database


class OutputType(Enum):
    """Output artifact types."""
    DM = "DM"       # Data Module
    PM = "PM"       # Publication Module
    DML = "DML"     # Data Module List
    ICN = "ICN"     # Information Control Number (graphics)
    PDF = "PDF"     # PDF export
    HTML = "HTML"   # HTML export
    IETP = "IETP"   # IETP package


class S1000DVersion(Enum):
    """Supported S1000D versions."""
    V5_0 = "S1000D_5.0"
    V4_2 = "S1000D_4.2"
    V4_1 = "S1000D_4.1"


# =============================================================================
# DATA CLASSES - CONTRACT COMPONENTS
# =============================================================================


@dataclass
class ContractHeader:
    """Contract identification and metadata."""
    contract_id: str
    version: str
    title: str
    category: ContractCategory
    status: ContractStatus
    created_date: datetime
    description: str = ""
    effective_date: Optional[datetime] = None
    supersedes: Optional[str] = None
    
    @property
    def versioned_id(self) -> str:
        """Get contract ID with version suffix."""
        return f"{self.contract_id}-{self.version}"


@dataclass
class ContractAuthority:
    """Governance and approval information."""
    owner: str  # Stakeholder role
    approver: str
    approval_date: Optional[datetime] = None
    approval_reference: Optional[str] = None  # CCB or ECO reference


@dataclass
class BaselineReference:
    """Reference to source baseline."""
    type: str  # FBL, ABL, PBL, OBL
    id: str    # Baseline ID or "LATEST"
    locked: bool = True


@dataclass
class ScopeFilters:
    """Additional scope filtering criteria."""
    effectivity: Optional[str] = None
    lifecycle_phases: List[str] = field(default_factory=list)
    custom_filters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SourceScope:
    """Source specification scope."""
    ata_chapters: List[str]
    artifact_types: List[str]
    ata_exclude: List[str] = field(default_factory=list)
    filters: Optional[ScopeFilters] = None


@dataclass
class SourceSpecification:
    """Complete source specification."""
    baseline: BaselineReference
    scope: SourceScope
    paths: List[str] = field(default_factory=list)


@dataclass
class OutputFormat:
    """Output format specification."""
    standard: S1000DVersion
    output_types: List[OutputType]


@dataclass
class NamingConfiguration:
    """S1000D naming configuration."""
    model_ident_code: str
    system_diff_code: str = "A"
    originator_code: Optional[str] = None


@dataclass
class TargetSpecification:
    """Target output specification."""
    publication: PublicationType
    format: OutputFormat
    destination: str
    naming: Optional[NamingConfiguration] = None


@dataclass
class MappingRule:
    """Source to target mapping rule."""
    source_type: str
    target_type: str
    mapping_file: str
    options: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DMGenerationOptions:
    """Data Module generation options."""
    include_applicability: bool = True
    include_references: bool = True
    include_warnings: bool = True
    language: str = "en-US"


@dataclass
class SecurityConfiguration:
    """Security classification configuration."""
    classification: str = "01"  # 01 = Unclassified
    caveats: List[str] = field(default_factory=list)


@dataclass
class TransformationOptions:
    """Generator options."""
    include_graphics: bool = True
    generate_toc: bool = True
    applicability_filtering: bool = True
    dm_options: Optional[DMGenerationOptions] = None
    security: Optional[SecurityConfiguration] = None


@dataclass
class TransformationSpecification:
    """Complete transformation specification."""
    mapping_rules: List[MappingRule]
    generators: List[str]
    options: Optional[TransformationOptions] = None


@dataclass
class BREXValidation:
    """BREX validation configuration."""
    enabled: bool = True
    rules_file: str = "ASIGT/brex/project_brex.yaml"
    severity_threshold: SeverityThreshold = SeverityThreshold.ERROR


@dataclass
class SchemaValidation:
    """Schema validation configuration."""
    enabled: bool = True
    schema_version: str = "5.0"
    strict_mode: bool = True


@dataclass
class TraceValidation:
    """Traceability validation configuration."""
    enabled: bool = True
    require_complete: bool = True
    require_bidirectional: bool = False


@dataclass
class CustomValidationRule:
    """Custom validation rule definition."""
    rule_id: str
    description: str
    validator: str  # Path to validator


@dataclass
class ValidationSpecification:
    """Complete validation specification."""
    brex: BREXValidation
    schema: SchemaValidation
    trace: TraceValidation
    custom_rules: List[CustomValidationRule] = field(default_factory=list)


@dataclass
class NotificationConfig:
    """Notification configuration."""
    on_success: List[str] = field(default_factory=list)
    on_failure: List[str] = field(default_factory=list)


@dataclass
class ExecutionSpecification:
    """Execution configuration."""
    mode: ExecutionMode = ExecutionMode.FULL
    parallel: bool = True
    max_workers: int = 4
    timeout_minutes: int = 60
    on_error: ErrorHandling = ErrorHandling.STOP
    pre_checks: List[str] = field(default_factory=list)
    post_actions: List[str] = field(default_factory=list)
    notifications: Optional[NotificationConfig] = None


@dataclass
class ArchiveConfiguration:
    """Run archive configuration."""
    enabled: bool = True
    retention_days: int = 365
    location: str = "ASIGT/runs/"


@dataclass
class MetadataConfiguration:
    """Output metadata configuration."""
    include_provenance: bool = True
    include_hashes: bool = True
    include_metrics: bool = True
    include_contract_copy: bool = True


@dataclass
class OutputSpecification:
    """Output artifacts specification."""
    artifacts: List[str]
    archive: ArchiveConfiguration
    metadata: MetadataConfiguration


@dataclass
class RevisionEntry:
    """Contract revision history entry."""
    version: str
    date: datetime
    author: str
    description: str


# =============================================================================
# MAIN CONTRACT CLASS
# =============================================================================


@dataclass
class Contract:
    """
    ASIT Transformation Contract.
    
    A contract defines a governed transformation from KDB sources
    to IDB outputs. ASIGT can only execute approved contracts.
    
    Attributes:
        header: Contract identification and metadata
        authority: Governance and approval information
        source: Source specification (what to transform)
        target: Target specification (what to produce)
        transformation: Transformation rules (how to transform)
        validation: Validation requirements (what to check)
        execution: Execution configuration (how to run)
        outputs: Output specification (what to deliver)
        notes: Additional notes
        revision_history: Version history
    
    Example:
        >>> contract = Contract.load(Path("contracts/active/my-contract.yaml"))
        >>> if contract.is_executable():
        ...     # Pass to ASIGT
        ...     pass
    """
    header: ContractHeader
    authority: ContractAuthority
    source: SourceSpecification
    target: TargetSpecification
    transformation: TransformationSpecification
    validation: ValidationSpecification
    execution: ExecutionSpecification
    outputs: OutputSpecification
    notes: str = ""
    revision_history: List[RevisionEntry] = field(default_factory=list)
    
    # Internal tracking
    _file_path: Optional[Path] = field(default=None, repr=False)
    _file_hash: Optional[str] = field(default=None, repr=False)
    
    @property
    def id(self) -> str:
        """Contract ID."""
        return self.header.contract_id
    
    @property
    def version(self) -> str:
        """Contract version."""
        return self.header.version
    
    @property
    def status(self) -> ContractStatus:
        """Contract status."""
        return self.header.status
    
    @property
    def versioned_id(self) -> str:
        """Contract ID with version."""
        return self.header.versioned_id
    
    def is_executable(self) -> bool:
        """
        Check if contract can be executed by ASIGT.
        
        Only APPROVED and ACTIVE contracts are executable.
        """
        return self.header.status in (ContractStatus.APPROVED, ContractStatus.ACTIVE)
    
    def is_editable(self) -> bool:
        """Check if contract can be edited."""
        return self.header.status == ContractStatus.DRAFT
    
    def get_baseline_id(self) -> str:
        """Get the source baseline ID."""
        return self.source.baseline.id
    
    def get_ata_scope(self) -> Set[str]:
        """Get set of ATA chapters in scope."""
        included = set(self.source.scope.ata_chapters)
        excluded = set(self.source.scope.ata_exclude)
        return included - excluded
    
    def get_generators(self) -> List[str]:
        """Get list of ASIGT generators to invoke."""
        return self.transformation.generators
    
    def get_mapping_rules(self) -> List[MappingRule]:
        """Get transformation mapping rules."""
        return self.transformation.mapping_rules
    
    def requires_brex_validation(self) -> bool:
        """Check if BREX validation is required."""
        return self.validation.brex.enabled
    
    def requires_schema_validation(self) -> bool:
        """Check if schema validation is required."""
        return self.validation.schema.enabled
    
    def requires_trace_validation(self) -> bool:
        """Check if trace validation is required."""
        return self.validation.trace.enabled
    
    def get_output_artifacts(self) -> List[str]:
        """Get required output artifacts."""
        return self.outputs.artifacts
    
    def get_archive_path(self, run_id: str) -> str:
        """Get archive path for a run."""
        return f"{self.outputs.archive.location}{run_id}__{self.id}"
    
    def compute_hash(self) -> str:
        """Compute SHA-256 hash of contract content."""
        if self._file_path and self._file_path.exists():
            content = self._file_path.read_bytes()
            return f"sha256:{hashlib.sha256(content).hexdigest()}"
        return ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert contract to dictionary representation."""
        return {
            "header": {
                "contract_id": self.header.contract_id,
                "version": self.header.version,
                "title": self.header.title,
                "description": self.header.description,
                "category": self.header.category.value,
                "status": self.header.status.value,
                "created_date": self.header.created_date.isoformat(),
                "effective_date": self.header.effective_date.isoformat() 
                    if self.header.effective_date else None,
                "supersedes": self.header.supersedes,
            },
            "authority": {
                "owner": self.authority.owner,
                "approver": self.authority.approver,
                "approval_date": self.authority.approval_date.isoformat() 
                    if self.authority.approval_date else None,
                "approval_reference": self.authority.approval_reference,
            },
            "source": {
                "baseline": {
                    "type": self.source.baseline.type,
                    "id": self.source.baseline.id,
                    "locked": self.source.baseline.locked,
                },
                "scope": {
                    "ata_chapters": self.source.scope.ata_chapters,
                    "ata_exclude": self.source.scope.ata_exclude,
                    "artifact_types": self.source.scope.artifact_types,
                },
                "paths": self.source.paths,
            },
            "target": {
                "publication": self.target.publication.value,
                "format": {
                    "standard": self.target.format.standard.value,
                    "output_types": [t.value for t in self.target.format.output_types],
                },
                "destination": self.target.destination,
            },
            "transformation": {
                "mapping_rules": [
                    {
                        "source_type": r.source_type,
                        "target_type": r.target_type,
                        "mapping_file": r.mapping_file,
                    }
                    for r in self.transformation.mapping_rules
                ],
                "generators": self.transformation.generators,
            },
            "validation": {
                "brex": {"enabled": self.validation.brex.enabled},
                "schema": {"enabled": self.validation.schema.enabled},
                "trace": {"enabled": self.validation.trace.enabled},
            },
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], file_path: Optional[Path] = None) -> "Contract":
        """Create Contract from dictionary."""
        header_data = data.get("header", data)
        
        # Parse header
        header = ContractHeader(
            contract_id=header_data["contract_id"],
            version=header_data.get("version", "v1.0.0"),
            title=header_data.get("title", ""),
            description=header_data.get("description", ""),
            category=ContractCategory(header_data.get("category", "LM")),
            status=ContractStatus(header_data.get("status", "DRAFT")),
            created_date=_parse_date(header_data.get("created_date")),
            effective_date=_parse_date(header_data.get("effective_date")),
            supersedes=header_data.get("supersedes"),
        )
        
        # Parse authority
        auth_data = data.get("authority", {})
        authority = ContractAuthority(
            owner=auth_data.get("owner", "STK_CM"),
            approver=auth_data.get("approver", "STK_CM"),
            approval_date=_parse_date(auth_data.get("approval_date")),
            approval_reference=auth_data.get("approval_reference"),
        )
        
        # Parse source
        source_data = data.get("source", {})
        baseline_data = source_data.get("baseline", {})
        scope_data = source_data.get("scope", {})
        filters_data = scope_data.get("filters", {})
        
        source = SourceSpecification(
            baseline=BaselineReference(
                type=baseline_data.get("type", "FBL"),
                id=baseline_data.get("id", "LATEST"),
                locked=baseline_data.get("locked", True),
            ),
            scope=SourceScope(
                ata_chapters=scope_data.get("ata_chapters", []),
                artifact_types=scope_data.get("artifact_types", []),
                ata_exclude=scope_data.get("ata_exclude", []),
                filters=ScopeFilters(
                    effectivity=filters_data.get("effectivity"),
                    lifecycle_phases=filters_data.get("lifecycle_phase", []),
                ) if filters_data else None,
            ),
            paths=source_data.get("paths", []),
        )
        
        # Parse target
        target_data = data.get("target", {})
        format_data = target_data.get("format", {})
        naming_data = target_data.get("naming", {})
        
        target = TargetSpecification(
            publication=PublicationType(target_data.get("publication", "CSDB")),
            format=OutputFormat(
                standard=S1000DVersion(format_data.get("standard", "S1000D_5.0")),
                output_types=[
                    OutputType(t) for t in format_data.get("output_types", ["DM"])
                ],
            ),
            destination=target_data.get("destination", "IDB/CSDB/"),
            naming=NamingConfiguration(
                model_ident_code=naming_data.get("model_ident_code", ""),
                system_diff_code=naming_data.get("system_diff_code", "A"),
            ) if naming_data.get("model_ident_code") else None,
        )
        
        # Parse transformation
        trans_data = data.get("transformation", {})
        options_data = trans_data.get("options", {})
        dm_options_data = options_data.get("dm_options", {})
        security_data = options_data.get("security", {})
        
        mapping_rules = [
            MappingRule(
                source_type=r["source_type"],
                target_type=r["target_type"],
                mapping_file=r["mapping_file"],
                options=r.get("options", {}),
            )
            for r in trans_data.get("mapping_rules", [])
        ]
        
        transformation = TransformationSpecification(
            mapping_rules=mapping_rules,
            generators=trans_data.get("generators", []),
            options=TransformationOptions(
                include_graphics=options_data.get("include_graphics", True),
                generate_toc=options_data.get("generate_toc", True),
                applicability_filtering=options_data.get("applicability_filtering", True),
                dm_options=DMGenerationOptions(
                    include_applicability=dm_options_data.get("include_applicability", True),
                    include_references=dm_options_data.get("include_references", True),
                    include_warnings=dm_options_data.get("include_warnings", True),
                    language=dm_options_data.get("language", "en-US"),
                ) if dm_options_data else None,
                security=SecurityConfiguration(
                    classification=security_data.get("classification", "01"),
                    caveats=security_data.get("caveats", []),
                ) if security_data else None,
            ) if options_data else None,
        )
        
        # Parse validation
        val_data = data.get("validation", {})
        brex_data = val_data.get("brex", {})
        schema_data = val_data.get("schema", {})
        trace_data = val_data.get("trace", {})
        
        validation = ValidationSpecification(
            brex=BREXValidation(
                enabled=brex_data.get("enabled", True),
                rules_file=brex_data.get("rules_file", "ASIGT/brex/project_brex.yaml"),
                severity_threshold=SeverityThreshold(
                    brex_data.get("severity_threshold", "ERROR")
                ),
            ),
            schema=SchemaValidation(
                enabled=schema_data.get("enabled", True),
                schema_version=schema_data.get("schema_version", "5.0"),
                strict_mode=schema_data.get("strict_mode", True),
            ),
            trace=TraceValidation(
                enabled=trace_data.get("enabled", True),
                require_complete=trace_data.get("require_complete", True),
                require_bidirectional=trace_data.get("require_bidirectional", False),
            ),
            custom_rules=[
                CustomValidationRule(
                    rule_id=r["rule_id"],
                    description=r["description"],
                    validator=r["validator"],
                )
                for r in val_data.get("custom_rules", [])
            ],
        )
        
        # Parse execution
        exec_data = data.get("execution", {})
        notif_data = exec_data.get("notifications", {})
        
        execution = ExecutionSpecification(
            mode=ExecutionMode(exec_data.get("mode", "FULL")),
            parallel=exec_data.get("parallel", True),
            max_workers=exec_data.get("max_workers", 4),
            timeout_minutes=exec_data.get("timeout_minutes", 60),
            on_error=ErrorHandling(exec_data.get("on_error", "STOP")),
            pre_checks=exec_data.get("pre_checks", []),
            post_actions=exec_data.get("post_actions", []),
            notifications=NotificationConfig(
                on_success=notif_data.get("on_success", []),
                on_failure=notif_data.get("on_failure", []),
            ) if notif_data else None,
        )
        
        # Parse outputs
        out_data = data.get("outputs", {})
        archive_data = out_data.get("archive", {})
        meta_data = out_data.get("metadata", {})
        
        outputs = OutputSpecification(
            artifacts=out_data.get("artifacts", ["DATA_MODULES", "TRACE_MATRIX"]),
            archive=ArchiveConfiguration(
                enabled=archive_data.get("enabled", True),
                retention_days=archive_data.get("retention_days", 365),
                location=archive_data.get("location", "ASIGT/runs/"),
            ),
            metadata=MetadataConfiguration(
                include_provenance=meta_data.get("include_provenance", True),
                include_hashes=meta_data.get("include_hashes", True),
                include_metrics=meta_data.get("include_metrics", True),
                include_contract_copy=meta_data.get("include_contract_copy", True),
            ),
        )
        
        # Parse revision history
        revision_history = [
            RevisionEntry(
                version=r["version"],
                date=_parse_date(r["date"]),
                author=r["author"],
                description=r["description"],
            )
            for r in data.get("revision_history", [])
        ]
        
        contract = cls(
            header=header,
            authority=authority,
            source=source,
            target=target,
            transformation=transformation,
            validation=validation,
            execution=execution,
            outputs=outputs,
            notes=data.get("notes", ""),
            revision_history=revision_history,
        )
        
        contract._file_path = file_path
        if file_path and file_path.exists():
            contract._file_hash = contract.compute_hash()
        
        return contract
    
    @classmethod
    def load(cls, path: Path) -> "Contract":
        """
        Load contract from YAML file.
        
        Args:
            path: Path to contract YAML file
            
        Returns:
            Contract instance
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If contract is invalid
        """
        if not path.exists():
            raise FileNotFoundError(f"Contract file not found: {path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        return cls.from_dict(data, file_path=path)
    
    def save(self, path: Path) -> None:
        """
        Save contract to YAML file.
        
        Args:
            path: Destination path
            
        Note:
            Only DRAFT contracts can be saved/modified.
        """
        if not self.is_editable():
            raise ValueError(
                f"Cannot save contract in {self.status.value} state. "
                "Only DRAFT contracts can be modified."
            )
        
        data = self.to_dict()
        data["notes"] = self.notes
        
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        
        self._file_path = path
        self._file_hash = self.compute_hash()


# =============================================================================
# CONTRACT MANAGER
# =============================================================================


class ContractError(Exception):
    """Exception raised for contract errors."""
    pass


class ContractNotFoundError(ContractError):
    """Raised when a contract cannot be found."""
    pass


class ContractValidationError(ContractError):
    """Raised when contract validation fails."""
    pass


class ContractManager:
    """
    Manages ASIT transformation contracts.
    
    Provides contract loading, validation, and lifecycle management.
    
    Usage:
        >>> manager = ContractManager(Path("ASIT/CONTRACTS"))
        >>> contract = manager.get_contract("KITDM-CTR-LM-CSDB_ATA28")
        >>> if contract.is_executable():
        ...     # Execute with ASIGT
        ...     pass
    """
    
    # Contract ID pattern: PREFIX-CTR-CATEGORY-TARGET[-SCOPE]
    CONTRACT_ID_PATTERN = re.compile(
        r"^[A-Z0-9]+-CTR-[A-Z]+-[A-Z0-9]+(?:_[A-Za-z0-9_]+)?$"
    )
    
    def __init__(self, contracts_root: Path):
        """
        Initialize contract manager.
        
        Args:
            contracts_root: Path to ASIT/CONTRACTS directory
        """
        self.contracts_root = Path(contracts_root)
        self.templates_dir = self.contracts_root / "templates"
        self.active_dir = self.contracts_root / "active"
        
        self._contracts: Dict[str, Contract] = {}
        self._load_contracts()
    
    def _load_contracts(self) -> None:
        """Load all contracts from active directory."""
        if not self.active_dir.exists():
            logger.warning(f"Active contracts directory not found: {self.active_dir}")
            return
        
        for contract_file in self.active_dir.glob("*.yaml"):
            try:
                contract = Contract.load(contract_file)
                self._contracts[contract.id] = contract
                logger.debug(f"Loaded contract: {contract.id}")
            except Exception as e:
                logger.warning(f"Failed to load contract {contract_file}: {e}")
    
    def get_contract(self, contract_id: str) -> Contract:
        """
        Retrieve contract by ID.
        
        Args:
            contract_id: Contract identifier
            
        Returns:
            Contract instance
            
        Raises:
            ContractNotFoundError: If contract doesn't exist
        """
        if contract_id not in self._contracts:
            raise ContractNotFoundError(f"Contract not found: {contract_id}")
        return self._contracts[contract_id]
    
    def get_contract_by_path(self, path: Path) -> Contract:
        """Load contract from specific path."""
        return Contract.load(path)
    
    def list_contracts(
        self,
        status: Optional[ContractStatus] = None,
        category: Optional[ContractCategory] = None,
        publication: Optional[PublicationType] = None,
    ) -> List[Contract]:
        """
        List contracts with optional filtering.
        
        Args:
            status: Filter by status
            category: Filter by category
            publication: Filter by target publication
            
        Returns:
            List of matching contracts
        """
        result = list(self._contracts.values())
        
        if status:
            result = [c for c in result if c.status == status]
        if category:
            result = [c for c in result if c.header.category == category]
        if publication:
            result = [c for c in result if c.target.publication == publication]
        
        return sorted(result, key=lambda c: c.id)
    
    def list_executable_contracts(self) -> List[Contract]:
        """List all contracts that can be executed."""
        return [c for c in self._contracts.values() if c.is_executable()]
    
    def list_templates(self) -> List[Path]:
        """List available contract templates."""
        if not self.templates_dir.exists():
            return []
        return list(self.templates_dir.glob("*.template.yaml"))
    
    def validate_contract_id(self, contract_id: str) -> bool:
        """Validate contract ID format."""
        return bool(self.CONTRACT_ID_PATTERN.match(contract_id))
    
    def validate_contract(self, contract: Contract) -> Dict[str, Any]:
        """
        Validate a contract for completeness and correctness.
        
        Args:
            contract: Contract to validate
            
        Returns:
            Validation results dictionary
        """
        errors = []
        warnings = []
        
        # Validate ID format
        if not self.validate_contract_id(contract.id):
            errors.append(f"Invalid contract ID format: {contract.id}")
        
        # Validate required fields
        if not contract.header.title:
            errors.append("Contract title is required")
        
        if not contract.source.scope.ata_chapters:
            warnings.append("No ATA chapters specified in scope")
        
        if not contract.source.scope.artifact_types:
            warnings.append("No artifact types specified in scope")
        
        if not contract.transformation.generators:
            errors.append("At least one generator must be specified")
        
        if not contract.transformation.mapping_rules:
            warnings.append("No mapping rules defined")
        
        # Validate baseline reference
        if contract.source.baseline.id == "LATEST" and contract.is_executable():
            warnings.append(
                "Using 'LATEST' baseline reference. "
                "Consider pinning to specific baseline for reproducibility."
            )
        
        # Validate approval for executable contracts
        if contract.is_executable():
            if not contract.authority.approval_date:
                warnings.append("Executable contract missing approval date")
            if not contract.authority.approval_reference:
                warnings.append("Executable contract missing approval reference")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "error_count": len(errors),
            "warning_count": len(warnings),
        }
    
    def create_from_template(
        self,
        template_name: str,
        contract_id: str,
        **kwargs,
    ) -> Contract:
        """
        Create a new contract from a template.
        
        Args:
            template_name: Template name (without extension)
            contract_id: New contract ID
            **kwargs: Template variable substitutions
            
        Returns:
            New Contract instance (in DRAFT status)
        """
        template_path = self.templates_dir / f"{template_name}.template.yaml"
        if not template_path.exists():
            raise ContractNotFoundError(f"Template not found: {template_name}")
        
        # Load template
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Substitute placeholders
        for key, value in kwargs.items():
            content = content.replace(f"<{key.upper()}>", str(value))
        
        # Parse as contract
        data = yaml.safe_load(content)
        data["header"]["contract_id"] = contract_id
        data["header"]["status"] = "DRAFT"
        data["header"]["created_date"] = datetime.utcnow().strftime("%Y-%m-%d")
        
        return Contract.from_dict(data)
    
    def reload(self) -> None:
        """Reload all contracts from disk."""
        self._contracts.clear()
        self._load_contracts()


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def _parse_date(value: Optional[str]) -> Optional[datetime]:
    """Parse date string to datetime."""
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    try:
        # Try ISO format first
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        pass
    try:
        # Try date-only format
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return None


# =============================================================================
# MODULE EXPORTS
# =============================================================================


__all__ = [
    # Enums
    "ContractStatus",
    "ContractCategory",
    "ExecutionMode",
    "ErrorHandling",
    "SeverityThreshold",
    "PublicationType",
    "OutputType",
    "S1000DVersion",
    
    # Data classes - Header
    "ContractHeader",
    "ContractAuthority",
    
    # Data classes - Source
    "BaselineReference",
    "ScopeFilters",
    "SourceScope",
    "SourceSpecification",
    
    # Data classes - Target
    "OutputFormat",
    "NamingConfiguration",
    "TargetSpecification",
    
    # Data classes - Transformation
    "MappingRule",
    "DMGenerationOptions",
    "SecurityConfiguration",
    "TransformationOptions",
    "TransformationSpecification",
    
    # Data classes - Validation
    "BREXValidation",
    "SchemaValidation",
    "TraceValidation",
    "CustomValidationRule",
    "ValidationSpecification",
    
    # Data classes - Execution
    "NotificationConfig",
    "ExecutionSpecification",
    
    # Data classes - Output
    "ArchiveConfiguration",
    "MetadataConfiguration",
    "OutputSpecification",
    "RevisionEntry",
    
    # Main classes
    "Contract",
    "ContractManager",
    
    # Exceptions
    "ContractError",
    "ContractNotFoundError",
    "ContractValidationError",
]
