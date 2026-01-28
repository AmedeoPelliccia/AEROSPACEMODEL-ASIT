"""
ASIT Governance Module

Manages baselines, approvals, change control, and authority for
aerospace information transformation.

GOVERNANCE controls:
    - Who controls what (authority matrix)
    - Change authorization (ECR/ECO)
    - Baseline management (FBL, ABL, PBL, OBL)
    - Approval workflows
"""

from __future__ import annotations

import csv
import hashlib
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import yaml

logger = logging.getLogger(__name__)


# =============================================================================
# ENUMERATIONS
# =============================================================================


class BaselineType(Enum):
    """Baseline categories per ARP4754A."""
    FBL = "FBL"  # Functional Baseline
    ABL = "ABL"  # Allocated Baseline
    DBL = "DBL"  # Design Baseline (legacy alias for ABL)
    PBL = "PBL"  # Product Baseline
    OBL = "OBL"  # Operational Baseline


class BaselineState(Enum):
    """Baseline lifecycle states."""
    DRAFT = "DRAFT"           # Under development, editable
    REVIEW = "REVIEW"         # Submitted to CCB, pending
    APPROVED = "APPROVED"     # CCB approved, locked
    RELEASED = "RELEASED"     # Published, immutable
    SUPERSEDED = "SUPERSEDED" # Replaced by newer baseline


class ChangeRequestStatus(Enum):
    """ECR lifecycle states."""
    OPEN = "OPEN"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"


class ChangeOrderStatus(Enum):
    """ECO lifecycle states."""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    CANCELLED = "CANCELLED"


class ChangeClassification(Enum):
    """Change impact classification."""
    MAJOR = "MAJOR"           # Requires full CCB review
    MINOR = "MINOR"           # Delegated authority
    ADMINISTRATIVE = "ADMINISTRATIVE"  # Editorial only


class ApprovalState(Enum):
    """Approval workflow states."""
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    DEFERRED = "DEFERRED"


# =============================================================================
# STAKEHOLDER / AUTHORITY DEFINITIONS
# =============================================================================


class StakeholderRole(Enum):
    """Standard ASIT stakeholder roles."""
    STK_PM = "STK_PM"       # Program Management
    STK_SE = "STK_SE"       # Systems Engineering
    STK_CM = "STK_CM"       # Configuration Management
    STK_ENG = "STK_ENG"     # Engineering
    STK_SAF = "STK_SAF"     # Safety
    STK_QA = "STK_QA"       # Quality Assurance
    STK_OPS = "STK_OPS"     # Operations
    STK_CERT = "STK_CERT"   # Certification
    STK_TEST = "STK_TEST"   # Test & Verification
    STK_MRO = "STK_MRO"     # Maintenance, Repair, Overhaul


@dataclass
class Stakeholder:
    """A governance stakeholder with authority."""
    role: StakeholderRole
    name: str
    email: Optional[str] = None
    organization: Optional[str] = None
    delegate: Optional[str] = None  # Backup authority


# =============================================================================
# BASELINE MANAGEMENT
# =============================================================================


@dataclass
class BaselineContent:
    """A single artifact within a baseline."""
    artifact_id: str
    path: str
    hash: str
    version: str
    artifact_type: str
    
    def verify_hash(self, file_path: Path) -> bool:
        """Verify artifact integrity against stored hash."""
        if not file_path.exists():
            return False
        content = file_path.read_bytes()
        computed = f"sha256:{hashlib.sha256(content).hexdigest()}"
        return computed == self.hash


@dataclass
class BaselineEffectivity:
    """Effectivity constraints for a baseline."""
    established_date: Optional[datetime] = None
    superseded_date: Optional[datetime] = None
    msn_range: Optional[List[str]] = None  # Aircraft serial numbers
    tail_numbers: Optional[List[str]] = None
    mod_status: Optional[Dict[str, str]] = None  # Modification applicability


@dataclass
class BaselineAuthority:
    """Authority record for baseline approval."""
    ccb_reference: str
    approved_by: StakeholderRole
    approval_date: datetime
    approver_name: Optional[str] = None
    signature_ref: Optional[str] = None


@dataclass
class Baseline:
    """
    ASIT Baseline — Frozen configuration snapshot.
    
    A baseline identifies a specific, immutable set of artifacts
    that serves as the authoritative reference for transformations.
    
    Attributes:
        id: Unique baseline identifier (e.g., "FBL-2026-Q1-003")
        type: Baseline category (FBL, ABL, PBL, OBL)
        state: Current lifecycle state
        description: Human-readable description
        scope_ata_chapters: ATA chapters included
        scope_lifecycle_phases: Lifecycle phases included
        contents: Artifacts in this baseline
        effectivity: Applicability constraints
        authority: Approval information
        parent_baseline: Previous baseline this derives from
    """
    id: str
    type: BaselineType
    state: BaselineState
    description: str = ""
    scope_ata_chapters: List[str] = field(default_factory=list)
    scope_lifecycle_phases: List[str] = field(default_factory=list)
    contents: List[BaselineContent] = field(default_factory=list)
    effectivity: Optional[BaselineEffectivity] = None
    authority: Optional[BaselineAuthority] = None
    parent_baseline: Optional[str] = None
    created_date: Optional[datetime] = None
    version: str = "1.0.0"
    
    def is_released(self) -> bool:
        """Check if baseline is in released (immutable) state."""
        return self.state == BaselineState.RELEASED
    
    def is_usable(self) -> bool:
        """Check if baseline can be used for transformations."""
        return self.state in (BaselineState.APPROVED, BaselineState.RELEASED)
    
    def get_artifact(self, artifact_id: str) -> Optional[BaselineContent]:
        """Retrieve a specific artifact from the baseline."""
        for content in self.contents:
            if content.artifact_id == artifact_id:
                return content
        return None
    
    def verify_integrity(self, root_path: Path) -> Dict[str, bool]:
        """Verify all artifacts against stored hashes."""
        results = {}
        for content in self.contents:
            file_path = root_path / content.path
            results[content.artifact_id] = content.verify_hash(file_path)
        return results
    
    @classmethod
    def from_yaml(cls, data: Dict[str, Any]) -> "Baseline":
        """Create Baseline from YAML dictionary."""
        baseline_data = data.get("baseline", data)
        
        # Parse contents
        contents = []
        for item in baseline_data.get("contents", []):
            contents.append(BaselineContent(
                artifact_id=item["artifact_id"],
                path=item["path"],
                hash=item["hash"],
                version=item["version"],
                artifact_type=item.get("type", "unknown")
            ))
        
        # Parse effectivity
        effectivity = None
        if "effectivity" in baseline_data:
            eff = baseline_data["effectivity"]
            effectivity = BaselineEffectivity(
                established_date=datetime.fromisoformat(eff["established_date"]) 
                    if eff.get("established_date") else None,
                superseded_date=datetime.fromisoformat(eff["superseded_date"]) 
                    if eff.get("superseded_date") else None,
                msn_range=eff.get("msn_range"),
                tail_numbers=eff.get("tail_numbers"),
                mod_status=eff.get("mod_status")
            )
        
        # Parse authority
        authority = None
        if "authority" in baseline_data:
            auth = baseline_data["authority"]
            authority = BaselineAuthority(
                ccb_reference=auth["ccb_reference"],
                approved_by=StakeholderRole(auth["approved_by"]),
                approval_date=datetime.fromisoformat(auth["approval_date"]),
                approver_name=auth.get("approver_name"),
                signature_ref=auth.get("signature_ref")
            )
        
        scope = baseline_data.get("scope", {})
        
        return cls(
            id=baseline_data["id"],
            type=BaselineType(baseline_data["type"]),
            state=BaselineState(baseline_data["status"]),
            description=baseline_data.get("description", ""),
            scope_ata_chapters=scope.get("ata_chapters", []),
            scope_lifecycle_phases=scope.get("lifecycle_phases", []),
            contents=contents,
            effectivity=effectivity,
            authority=authority,
            parent_baseline=baseline_data.get("parent_baseline"),
            version=baseline_data.get("version", "1.0.0")
        )
    
    @classmethod
    def load(cls, path: Path) -> "Baseline":
        """Load baseline from YAML file."""
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return cls.from_yaml(data)


# =============================================================================
# CHANGE CONTROL
# =============================================================================


@dataclass
class AffectedItem:
    """An item affected by a change request."""
    artifact_id: str
    change_type: str  # ADD, MODIFY, DELETE
    description: str = ""
    current_version: Optional[str] = None
    target_version: Optional[str] = None


@dataclass
class ChangeAnalysis:
    """Impact analysis for a change request."""
    safety_impact: str
    certification_impact: str
    schedule_impact: Optional[str] = None
    cost_impact: Optional[str] = None
    affected_baselines: List[str] = field(default_factory=list)
    affected_publications: List[str] = field(default_factory=list)


@dataclass
class ChangeRequest:
    """
    Engineering Change Request (ECR).
    
    Documents a proposed change and its impact analysis
    before CCB disposition.
    """
    id: str
    title: str
    status: ChangeRequestStatus
    classification: ChangeClassification
    description: str = ""
    requestor: Optional[str] = None
    created_date: Optional[datetime] = None
    affected_items: List[AffectedItem] = field(default_factory=list)
    analysis: Optional[ChangeAnalysis] = None
    ccb_disposition: Optional[str] = None
    disposition_date: Optional[datetime] = None
    eco_reference: Optional[str] = None  # Linked ECO if approved
    
    def is_approved(self) -> bool:
        """Check if ECR has been approved."""
        return self.status == ChangeRequestStatus.APPROVED
    
    def can_implement(self) -> bool:
        """Check if change can be implemented."""
        return self.is_approved() and self.eco_reference is not None
    
    @classmethod
    def from_yaml(cls, data: Dict[str, Any]) -> "ChangeRequest":
        """Create ChangeRequest from YAML dictionary."""
        ecr_data = data.get("ecr", data)
        
        # Parse affected items
        affected_items = []
        for item in ecr_data.get("affected_items", []):
            affected_items.append(AffectedItem(
                artifact_id=item["artifact"],
                change_type=item["change_type"],
                description=item.get("description", ""),
                current_version=item.get("current_version"),
                target_version=item.get("target_version")
            ))
        
        # Parse analysis
        analysis = None
        if "analysis" in ecr_data:
            ana = ecr_data["analysis"]
            analysis = ChangeAnalysis(
                safety_impact=ana.get("safety_impact", "Not assessed"),
                certification_impact=ana.get("certification_impact", "Not assessed"),
                schedule_impact=ana.get("schedule_impact"),
                cost_impact=ana.get("cost_impact"),
                affected_baselines=ana.get("affected_baselines", []),
                affected_publications=ana.get("affected_publications", [])
            )
        
        classification = ecr_data.get("classification", {})
        
        return cls(
            id=ecr_data["id"],
            title=ecr_data["title"],
            status=ChangeRequestStatus(ecr_data["status"]),
            classification=ChangeClassification(
                classification.get("type", "MAJOR") 
                if isinstance(classification, dict) 
                else classification
            ),
            description=ecr_data.get("description", ""),
            requestor=ecr_data.get("requestor"),
            affected_items=affected_items,
            analysis=analysis,
            ccb_disposition=ecr_data.get("disposition"),
            eco_reference=ecr_data.get("eco_reference")
        )


@dataclass
class ImplementationStep:
    """A single step in ECO implementation."""
    sequence: int
    description: str
    responsible: StakeholderRole
    status: str = "PENDING"  # PENDING, IN_PROGRESS, COMPLETE
    completed_date: Optional[datetime] = None
    evidence: Optional[str] = None


@dataclass 
class ChangeOrder:
    """
    Engineering Change Order (ECO).
    
    Authorizes and tracks implementation of an approved change.
    """
    id: str
    ecr_reference: str
    status: ChangeOrderStatus
    description: str = ""
    affected_baselines: List[str] = field(default_factory=list)
    target_baseline: Optional[str] = None
    implementation_steps: List[ImplementationStep] = field(default_factory=list)
    verification_criteria: List[str] = field(default_factory=list)
    verification_evidence: List[str] = field(default_factory=list)
    approved_by: Optional[str] = None
    approval_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    
    def is_complete(self) -> bool:
        """Check if ECO implementation is complete."""
        return self.status == ChangeOrderStatus.COMPLETE
    
    def get_progress(self) -> float:
        """Get implementation progress as percentage."""
        if not self.implementation_steps:
            return 0.0
        completed = sum(1 for s in self.implementation_steps if s.status == "COMPLETE")
        return (completed / len(self.implementation_steps)) * 100
    
    @classmethod
    def from_yaml(cls, data: Dict[str, Any]) -> "ChangeOrder":
        """Create ChangeOrder from YAML dictionary."""
        eco_data = data.get("eco", data)
        
        # Parse implementation steps
        steps = []
        for i, step in enumerate(eco_data.get("implementation", {}).get("steps", []), 1):
            steps.append(ImplementationStep(
                sequence=step.get("sequence", i),
                description=step["description"],
                responsible=StakeholderRole(step["responsible"]),
                status=step.get("status", "PENDING"),
                evidence=step.get("evidence")
            ))
        
        impl = eco_data.get("implementation", {})
        verif = eco_data.get("verification", {})
        
        return cls(
            id=eco_data["id"],
            ecr_reference=eco_data["ecr_reference"],
            status=ChangeOrderStatus(eco_data["status"]),
            description=eco_data.get("description", ""),
            affected_baselines=impl.get("affected_baselines", []),
            target_baseline=impl.get("target_baseline"),
            implementation_steps=steps,
            verification_criteria=verif.get("criteria", []),
            verification_evidence=verif.get("evidence", []),
            approved_by=eco_data.get("approved_by"),
            approval_date=datetime.fromisoformat(eco_data["approval_date"]) 
                if eco_data.get("approval_date") else None,
            completion_date=datetime.fromisoformat(eco_data["completion_date"]) 
                if eco_data.get("completion_date") else None
        )


# =============================================================================
# APPROVAL MATRIX
# =============================================================================


@dataclass
class ApprovalRequirement:
    """A single approval requirement from the matrix."""
    artifact_type: str
    lifecycle_phase: str
    approver_role: StakeholderRole
    required: bool = True
    backup_role: Optional[StakeholderRole] = None


@dataclass
class ApprovalRecord:
    """Record of an actual approval."""
    requirement: ApprovalRequirement
    state: ApprovalState
    approver_name: str
    approval_date: Optional[datetime] = None
    signature_ref: Optional[str] = None
    comments: Optional[str] = None


class ApprovalMatrix:
    """
    Manages approval requirements and records.
    
    The approval matrix defines who must approve what,
    based on artifact type and lifecycle phase.
    """
    
    def __init__(self):
        self._requirements: List[ApprovalRequirement] = []
        
    def load_from_csv(self, path: Path) -> None:
        """Load approval matrix from CSV file."""
        self._requirements.clear()
        
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                backup = None
                if row.get("backup_role"):
                    backup = StakeholderRole(row["backup_role"])
                    
                self._requirements.append(ApprovalRequirement(
                    artifact_type=row["artifact_type"],
                    lifecycle_phase=row["lifecycle_phase"],
                    approver_role=StakeholderRole(row["approver_role"]),
                    required=row.get("required", "true").lower() == "true",
                    backup_role=backup
                ))
    
    def get_requirements(
        self, 
        artifact_type: str, 
        lifecycle_phase: str
    ) -> List[ApprovalRequirement]:
        """Get approval requirements for an artifact."""
        return [
            req for req in self._requirements
            if req.artifact_type == artifact_type 
            and req.lifecycle_phase == lifecycle_phase
        ]
    
    def get_required_approvers(
        self, 
        artifact_type: str, 
        lifecycle_phase: str
    ) -> Set[StakeholderRole]:
        """Get set of required approver roles."""
        reqs = self.get_requirements(artifact_type, lifecycle_phase)
        return {req.approver_role for req in reqs if req.required}
    
    def validate_approvals(
        self,
        artifact_type: str,
        lifecycle_phase: str,
        approvals: List[ApprovalRecord]
    ) -> Dict[str, Any]:
        """
        Validate that all required approvals are present.
        
        Returns:
            Dictionary with 'valid', 'missing', and 'extra' keys.
        """
        required = self.get_required_approvers(artifact_type, lifecycle_phase)
        approved = {
            a.requirement.approver_role 
            for a in approvals 
            if a.state == ApprovalState.APPROVED
        }
        
        missing = required - approved
        extra = approved - required
        
        return {
            "valid": len(missing) == 0,
            "missing": list(missing),
            "extra": list(extra),
            "required_count": len(required),
            "approved_count": len(approved)
        }


# =============================================================================
# GOVERNANCE CONTROLLER
# =============================================================================


class GovernanceError(Exception):
    """Exception raised for governance violations."""
    pass


class BaselineNotFoundError(GovernanceError):
    """Raised when a baseline cannot be found."""
    pass


class AuthorizationError(GovernanceError):
    """Raised when an operation is not authorized."""
    pass


class GovernanceController:
    """
    ASIT Governance Controller.
    
    Central authority for baseline management, change control,
    and approval workflows.
    
    Usage:
        >>> governance = GovernanceController(Path("ASIT"))
        >>> baseline = governance.get_baseline("FBL-2026-Q1-003")
        >>> if governance.can_execute_transformation(contract, baseline):
        ...     # Proceed with ASIGT execution
        ...     pass
    """
    
    def __init__(self, asit_root: Path):
        """
        Initialize governance controller.
        
        Args:
            asit_root: Path to ASIT directory containing GOVERNANCE,
                       STRUCTURE, CONTRACTS, etc.
        """
        self.asit_root = Path(asit_root)
        self.governance_root = self.asit_root / "GOVERNANCE"
        self.contracts_root = self.asit_root / "CONTRACTS"
        
        self._baselines: Dict[str, Baseline] = {}
        self._ecrs: Dict[str, ChangeRequest] = {}
        self._ecos: Dict[str, ChangeOrder] = {}
        self._approval_matrix = ApprovalMatrix()
        
        self._load_governance_data()
    
    def _load_governance_data(self) -> None:
        """Load governance data from files."""
        # Load baseline register
        register_path = self.governance_root / "BASELINE_REGISTER.csv"
        if register_path.exists():
            self._load_baseline_register(register_path)
        
        # Load approval matrix
        matrix_path = self.governance_root / "APPROVALS" / "APPROVAL_MATRIX.csv"
        if matrix_path.exists():
            self._approval_matrix.load_from_csv(matrix_path)
        
        # Load ECRs
        ecr_dir = self.governance_root / "CHANGE_CONTROL" / "ECR"
        if ecr_dir.exists():
            for ecr_file in ecr_dir.glob("*.yaml"):
                try:
                    with open(ecr_file, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                    ecr = ChangeRequest.from_yaml(data)
                    self._ecrs[ecr.id] = ecr
                except Exception as e:
                    logger.warning(f"Failed to load ECR {ecr_file}: {e}")
        
        # Load ECOs
        eco_dir = self.governance_root / "CHANGE_CONTROL" / "ECO"
        if eco_dir.exists():
            for eco_file in eco_dir.glob("*.yaml"):
                try:
                    with open(eco_file, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                    eco = ChangeOrder.from_yaml(data)
                    self._ecos[eco.id] = eco
                except Exception as e:
                    logger.warning(f"Failed to load ECO {eco_file}: {e}")
    
    def _load_baseline_register(self, path: Path) -> None:
        """Load baseline register from CSV."""
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    baseline = Baseline(
                        id=row["baseline_id"],
                        type=BaselineType(row["type"]),
                        state=BaselineState(row["state"]),
                        description=row.get("description", ""),
                        version=row.get("version", "1.0.0")
                    )
                    self._baselines[baseline.id] = baseline
                except Exception as e:
                    logger.warning(f"Failed to load baseline {row.get('baseline_id')}: {e}")
    
    # -------------------------------------------------------------------------
    # Baseline Management
    # -------------------------------------------------------------------------
    
    def get_baseline(self, baseline_id: str) -> Baseline:
        """
        Retrieve baseline by ID.
        
        Args:
            baseline_id: Baseline identifier (e.g., "FBL-2026-Q1-003")
            
        Returns:
            Baseline object
            
        Raises:
            BaselineNotFoundError: If baseline doesn't exist
        """
        if baseline_id not in self._baselines:
            raise BaselineNotFoundError(f"Baseline not found: {baseline_id}")
        return self._baselines[baseline_id]
    
    def get_latest_baseline(self, baseline_type: BaselineType) -> Optional[Baseline]:
        """Get the latest released baseline of a given type."""
        candidates = [
            b for b in self._baselines.values()
            if b.type == baseline_type and b.is_released()
        ]
        if not candidates:
            return None
        # Sort by ID (assumes chronological naming convention)
        return max(candidates, key=lambda b: b.id)
    
    def list_baselines(
        self, 
        baseline_type: Optional[BaselineType] = None,
        state: Optional[BaselineState] = None
    ) -> List[Baseline]:
        """List baselines with optional filtering."""
        result = list(self._baselines.values())
        
        if baseline_type:
            result = [b for b in result if b.type == baseline_type]
        if state:
            result = [b for b in result if b.state == state]
            
        return sorted(result, key=lambda b: b.id)
    
    def validate_baseline_integrity(
        self, 
        baseline_id: str, 
        root_path: Path
    ) -> Dict[str, Any]:
        """
        Validate baseline artifact integrity.
        
        Args:
            baseline_id: Baseline to validate
            root_path: Root path for artifact resolution
            
        Returns:
            Validation results with per-artifact status
        """
        baseline = self.get_baseline(baseline_id)
        
        if not baseline.contents:
            return {
                "valid": True,
                "baseline_id": baseline_id,
                "artifacts_checked": 0,
                "artifacts_valid": 0,
                "details": {}
            }
        
        results = baseline.verify_integrity(root_path)
        valid_count = sum(1 for v in results.values() if v)
        
        return {
            "valid": all(results.values()),
            "baseline_id": baseline_id,
            "artifacts_checked": len(results),
            "artifacts_valid": valid_count,
            "details": results
        }
    
    # -------------------------------------------------------------------------
    # Change Control
    # -------------------------------------------------------------------------
    
    def get_change_request(self, ecr_id: str) -> Optional[ChangeRequest]:
        """Retrieve ECR by ID."""
        return self._ecrs.get(ecr_id)
    
    def get_change_order(self, eco_id: str) -> Optional[ChangeOrder]:
        """Retrieve ECO by ID."""
        return self._ecos.get(eco_id)
    
    def list_open_change_requests(self) -> List[ChangeRequest]:
        """List all open ECRs."""
        return [
            ecr for ecr in self._ecrs.values()
            if ecr.status in (ChangeRequestStatus.OPEN, ChangeRequestStatus.UNDER_REVIEW)
        ]
    
    def list_active_change_orders(self) -> List[ChangeOrder]:
        """List all in-progress ECOs."""
        return [
            eco for eco in self._ecos.values()
            if eco.status in (ChangeOrderStatus.PENDING, ChangeOrderStatus.IN_PROGRESS)
        ]
    
    # -------------------------------------------------------------------------
    # Authorization
    # -------------------------------------------------------------------------
    
    def can_execute_transformation(
        self,
        contract_id: str,
        contract_status: str,
        baseline_id: str
    ) -> bool:
        """
        Check if a transformation can be executed.
        
        This is called by ASIGT before any content generation.
        
        Args:
            contract_id: Contract to execute
            contract_status: Current contract status
            baseline_id: Source baseline
            
        Returns:
            True if execution is authorized
        """
        # Contract must be approved
        if contract_status != "APPROVED":
            logger.warning(
                f"Contract {contract_id} not approved (status: {contract_status})"
            )
            return False
        
        # Baseline must exist and be usable
        try:
            baseline = self.get_baseline(baseline_id)
        except BaselineNotFoundError:
            logger.warning(f"Baseline not found: {baseline_id}")
            return False
        
        if not baseline.is_usable():
            logger.warning(
                f"Baseline {baseline_id} not usable (state: {baseline.state})"
            )
            return False
        
        return True
    
    def validate_approval_authority(
        self,
        artifact_type: str,
        lifecycle_phase: str,
        approver_role: StakeholderRole
    ) -> bool:
        """Check if a role can approve a given artifact type."""
        required_roles = self._approval_matrix.get_required_approvers(
            artifact_type, lifecycle_phase
        )
        return approver_role in required_roles
    
    def get_required_approvals(
        self,
        artifact_type: str,
        lifecycle_phase: str
    ) -> List[ApprovalRequirement]:
        """Get list of required approvals for an artifact."""
        return self._approval_matrix.get_requirements(artifact_type, lifecycle_phase)
    
    # -------------------------------------------------------------------------
    # Execution Context
    # -------------------------------------------------------------------------
    
    def create_execution_context(
        self,
        contract_id: str,
        contract_version: str,
        baseline_id: str,
        invoker: str,
        authority_reference: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create an execution context for ASIGT.
        
        This packages all governance information needed for
        a controlled transformation.
        
        Args:
            contract_id: Contract to execute
            contract_version: Contract version
            baseline_id: Source baseline
            invoker: Identity of invoking user/system
            authority_reference: CCB or approval reference
            
        Returns:
            Execution context dictionary for ASIGT
        """
        baseline = self.get_baseline(baseline_id)
        timestamp = datetime.utcnow()
        run_id = timestamp.strftime("%Y%m%d-%H%M")
        
        return {
            "execution_context": {
                # Contract identification
                "contract_id": contract_id,
                "contract_version": contract_version,
                
                # Source baseline
                "baseline_id": baseline_id,
                "baseline_effective": baseline.effectivity.established_date.isoformat()
                    if baseline.effectivity and baseline.effectivity.established_date
                    else None,
                
                # Authority
                "invoker": invoker,
                "invocation_time": timestamp.isoformat() + "Z",
                "authority_reference": authority_reference 
                    or (baseline.authority.ccb_reference if baseline.authority else None),
                
                # Run identification
                "run_id": f"{run_id}__{contract_id}",
                
                # Governance version
                "asit_version": "2.0.0"
            }
        }


# =============================================================================
# MODULE EXPORTS
# =============================================================================


__all__ = [
    # Enums
    "BaselineType",
    "BaselineState",
    "ChangeRequestStatus",
    "ChangeOrderStatus",
    "ChangeClassification",
    "ApprovalState",
    "StakeholderRole",
    
    # Data classes
    "Stakeholder",
    "BaselineContent",
    "BaselineEffectivity",
    "BaselineAuthority",
    "Baseline",
    "AffectedItem",
    "ChangeAnalysis",
    "ChangeRequest",
    "ImplementationStep",
    "ChangeOrder",
    "ApprovalRequirement",
    "ApprovalRecord",
    
    # Controllers
    "ApprovalMatrix",
    "GovernanceController",
    
    # Exceptions
    "GovernanceError",
    "BaselineNotFoundError",
    "AuthorizationError",
]
