"""
ASIT Baselines Module

Manages baseline creation, registration, lifecycle, and integrity verification.

Baselines are immutable, versioned snapshots of configuration items that
serve as the authoritative reference for all downstream transformations.

ASIGT operates exclusively against approved baselines.
"""

from __future__ import annotations

import csv
import hashlib
import json
import logging
import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple, Union

import yaml

logger = logging.getLogger(__name__)


# =============================================================================
# ENUMERATIONS
# =============================================================================


class BaselineType(Enum):
    """
    Baseline categories per ARP4754A configuration management.
    
    Each type represents a different stage in the product lifecycle.
    """
    FBL = "FBL"  # Functional Baseline - Requirements freeze (after SRR)
    ABL = "ABL"  # Allocated Baseline - Design allocation (after PDR)
    DBL = "DBL"  # Design Baseline - Legacy alias for ABL
    PBL = "PBL"  # Product Baseline - As-built config (after CDR)
    OBL = "OBL"  # Operational Baseline - In-service config (after TC)


class BaselineState(Enum):
    """
    Baseline lifecycle states.
    
    Baselines progress through these states and become immutable once released.
    """
    DRAFT = "DRAFT"           # Under development, editable
    REVIEW = "REVIEW"         # Submitted to CCB, pending approval
    APPROVED = "APPROVED"     # CCB approved, locked
    RELEASED = "RELEASED"     # Published for use, immutable
    SUPERSEDED = "SUPERSEDED" # Replaced by newer baseline


class ArtifactStatus(Enum):
    """Status of an artifact within a baseline."""
    VALID = "VALID"           # Hash verified, content intact
    MODIFIED = "MODIFIED"     # Content changed since baseline
    MISSING = "MISSING"       # File not found
    UNCHECKED = "UNCHECKED"   # Not yet verified


# =============================================================================
# DATA CLASSES
# =============================================================================


@dataclass
class BaselineArtifact:
    """
    An artifact included in a baseline.
    
    Each artifact is tracked with its path, hash, and version
    for integrity verification.
    """
    artifact_id: str
    path: str
    hash: str  # Format: "sha256:hexdigest"
    version: str
    artifact_type: str
    lifecycle_phase: Optional[str] = None
    ata_chapter: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def hash_algorithm(self) -> str:
        """Extract hash algorithm from hash string."""
        if ":" in self.hash:
            return self.hash.split(":")[0]
        return "unknown"
    
    @property
    def hash_value(self) -> str:
        """Extract hash value from hash string."""
        if ":" in self.hash:
            return self.hash.split(":", 1)[1]
        return self.hash
    
    def verify(self, root_path: Path) -> ArtifactStatus:
        """
        Verify artifact integrity against stored hash.
        
        Args:
            root_path: Root directory for resolving artifact path
            
        Returns:
            ArtifactStatus indicating verification result
        """
        file_path = root_path / self.path
        
        if not file_path.exists():
            return ArtifactStatus.MISSING
        
        try:
            content = file_path.read_bytes()
            computed_hash = f"sha256:{hashlib.sha256(content).hexdigest()}"
            
            if computed_hash == self.hash:
                return ArtifactStatus.VALID
            else:
                return ArtifactStatus.MODIFIED
        except Exception as e:
            logger.warning(f"Failed to verify artifact {self.artifact_id}: {e}")
            return ArtifactStatus.UNCHECKED
    
    @classmethod
    def from_file(
        cls,
        artifact_id: str,
        file_path: Path,
        root_path: Path,
        version: str = "1.0.0",
        artifact_type: str = "unknown",
        **kwargs
    ) -> "BaselineArtifact":
        """
        Create artifact entry from an existing file.
        
        Args:
            artifact_id: Unique artifact identifier
            file_path: Absolute path to the file
            root_path: Root directory for relative path calculation
            version: Artifact version
            artifact_type: Type classification
            **kwargs: Additional metadata
            
        Returns:
            BaselineArtifact with computed hash
        """
        content = file_path.read_bytes()
        hash_value = f"sha256:{hashlib.sha256(content).hexdigest()}"
        relative_path = str(file_path.relative_to(root_path))
        
        return cls(
            artifact_id=artifact_id,
            path=relative_path,
            hash=hash_value,
            version=version,
            artifact_type=artifact_type,
            **kwargs
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = {
            "artifact_id": self.artifact_id,
            "path": self.path,
            "hash": self.hash,
            "version": self.version,
            "type": self.artifact_type,
        }
        if self.lifecycle_phase:
            result["lifecycle_phase"] = self.lifecycle_phase
        if self.ata_chapter:
            result["ata_chapter"] = self.ata_chapter
        if self.metadata:
            result["metadata"] = self.metadata
        return result


@dataclass
class BaselineScope:
    """Defines the scope of a baseline."""
    ata_chapters: List[str] = field(default_factory=list)
    lifecycle_phases: List[str] = field(default_factory=list)
    artifact_types: List[str] = field(default_factory=list)
    paths: List[str] = field(default_factory=list)  # KDB paths included


@dataclass
class BaselineEffectivity:
    """
    Effectivity constraints for a baseline.
    
    Defines when and to what the baseline applies.
    """
    established_date: Optional[datetime] = None
    superseded_date: Optional[datetime] = None
    msn_range: Optional[Tuple[str, str]] = None  # (start, end) serial numbers
    tail_numbers: List[str] = field(default_factory=list)
    mod_status: Dict[str, str] = field(default_factory=dict)
    
    def is_effective_for_msn(self, msn: str) -> bool:
        """Check if baseline is effective for a given MSN."""
        if not self.msn_range:
            return True  # No restriction
        start, end = self.msn_range
        return start <= msn <= end
    
    def is_superseded(self) -> bool:
        """Check if baseline has been superseded."""
        return self.superseded_date is not None


@dataclass
class BaselineAuthority:
    """Authority and approval information for a baseline."""
    ccb_reference: Optional[str] = None
    eco_reference: Optional[str] = None
    approved_by: Optional[str] = None  # Stakeholder role
    approver_name: Optional[str] = None
    approval_date: Optional[datetime] = None
    signature_ref: Optional[str] = None
    
    def is_approved(self) -> bool:
        """Check if baseline has been formally approved."""
        return self.approval_date is not None and self.approved_by is not None


@dataclass
class BaselineDelta:
    """
    Changes between two baselines.
    
    Documents what was added, modified, or removed.
    """
    from_baseline: str
    to_baseline: str
    added: List[str] = field(default_factory=list)      # Artifact IDs
    modified: List[str] = field(default_factory=list)   # Artifact IDs
    removed: List[str] = field(default_factory=list)    # Artifact IDs
    computed_at: Optional[datetime] = None
    
    @property
    def total_changes(self) -> int:
        """Total number of changed artifacts."""
        return len(self.added) + len(self.modified) + len(self.removed)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "from_baseline": self.from_baseline,
            "to_baseline": self.to_baseline,
            "added": self.added,
            "modified": self.modified,
            "removed": self.removed,
            "total_changes": self.total_changes,
            "computed_at": self.computed_at.isoformat() if self.computed_at else None,
        }


# =============================================================================
# MAIN BASELINE CLASS
# =============================================================================


@dataclass
class Baseline:
    """
    ASIT Baseline — Immutable, versioned configuration snapshot.
    
    A baseline identifies a specific set of artifacts at a point in time,
    serving as the authoritative reference for transformations.
    
    Attributes:
        id: Unique baseline identifier (e.g., "FBL-2026-Q1-003")
        type: Baseline category (FBL, ABL, PBL, OBL)
        state: Current lifecycle state
        version: Semantic version
        description: Human-readable description
        scope: What the baseline covers
        artifacts: List of included artifacts
        effectivity: When/where the baseline applies
        authority: Approval information
        parent_baseline: Previous baseline this derives from
        created_date: When the baseline was created
        released_date: When the baseline was released
    
    Example:
        >>> baseline = Baseline.load(Path("baselines/FBL-2026-Q1-003.yaml"))
        >>> if baseline.is_usable():
        ...     integrity = baseline.verify_integrity(kdb_root)
        ...     if integrity["valid"]:
        ...         # Use baseline for transformation
        ...         pass
    """
    id: str
    type: BaselineType
    state: BaselineState
    version: str = "1.0.0"
    description: str = ""
    scope: BaselineScope = field(default_factory=BaselineScope)
    artifacts: List[BaselineArtifact] = field(default_factory=list)
    effectivity: Optional[BaselineEffectivity] = None
    authority: Optional[BaselineAuthority] = None
    parent_baseline: Optional[str] = None
    created_date: Optional[datetime] = None
    released_date: Optional[datetime] = None
    
    # Internal tracking
    _file_path: Optional[Path] = field(default=None, repr=False)
    
    # ==========================================================================
    # State Checks
    # ==========================================================================
    
    def is_draft(self) -> bool:
        """Check if baseline is in draft state."""
        return self.state == BaselineState.DRAFT
    
    def is_released(self) -> bool:
        """Check if baseline is released (immutable)."""
        return self.state == BaselineState.RELEASED
    
    def is_usable(self) -> bool:
        """
        Check if baseline can be used for transformations.
        
        Only APPROVED and RELEASED baselines are usable.
        """
        return self.state in (BaselineState.APPROVED, BaselineState.RELEASED)
    
    def is_superseded(self) -> bool:
        """Check if baseline has been superseded."""
        if self.state == BaselineState.SUPERSEDED:
            return True
        if self.effectivity and self.effectivity.is_superseded():
            return True
        return False
    
    def is_editable(self) -> bool:
        """Check if baseline can be modified."""
        return self.state == BaselineState.DRAFT
    
    # ==========================================================================
    # Artifact Management
    # ==========================================================================
    
    def get_artifact(self, artifact_id: str) -> Optional[BaselineArtifact]:
        """Retrieve artifact by ID."""
        for artifact in self.artifacts:
            if artifact.artifact_id == artifact_id:
                return artifact
        return None
    
    def get_artifacts_by_type(self, artifact_type: str) -> List[BaselineArtifact]:
        """Get all artifacts of a specific type."""
        return [a for a in self.artifacts if a.artifact_type == artifact_type]
    
    def get_artifacts_by_ata(self, ata_chapter: str) -> List[BaselineArtifact]:
        """Get all artifacts for a specific ATA chapter."""
        return [
            a for a in self.artifacts 
            if a.ata_chapter and a.ata_chapter.startswith(ata_chapter)
        ]
    
    def get_artifacts_by_phase(self, lifecycle_phase: str) -> List[BaselineArtifact]:
        """Get all artifacts for a specific lifecycle phase."""
        return [a for a in self.artifacts if a.lifecycle_phase == lifecycle_phase]
    
    def add_artifact(self, artifact: BaselineArtifact) -> None:
        """
        Add artifact to baseline.
        
        Raises:
            ValueError: If baseline is not editable
        """
        if not self.is_editable():
            raise ValueError(f"Cannot modify baseline in {self.state.value} state")
        
        # Check for duplicate
        if self.get_artifact(artifact.artifact_id):
            raise ValueError(f"Artifact already exists: {artifact.artifact_id}")
        
        self.artifacts.append(artifact)
    
    def remove_artifact(self, artifact_id: str) -> bool:
        """
        Remove artifact from baseline.
        
        Returns:
            True if artifact was removed, False if not found
            
        Raises:
            ValueError: If baseline is not editable
        """
        if not self.is_editable():
            raise ValueError(f"Cannot modify baseline in {self.state.value} state")
        
        for i, artifact in enumerate(self.artifacts):
            if artifact.artifact_id == artifact_id:
                self.artifacts.pop(i)
                return True
        return False
    
    @property
    def artifact_count(self) -> int:
        """Number of artifacts in baseline."""
        return len(self.artifacts)
    
    @property
    def artifact_ids(self) -> Set[str]:
        """Set of all artifact IDs."""
        return {a.artifact_id for a in self.artifacts}
    
    # ==========================================================================
    # Integrity Verification
    # ==========================================================================
    
    def verify_integrity(self, root_path: Path) -> Dict[str, Any]:
        """
        Verify integrity of all baseline artifacts.
        
        Args:
            root_path: Root directory for artifact resolution
            
        Returns:
            Dictionary with verification results:
            - valid: True if all artifacts are valid
            - total: Total artifact count
            - valid_count: Number of valid artifacts
            - modified_count: Number of modified artifacts
            - missing_count: Number of missing artifacts
            - details: Per-artifact status
        """
        results = {
            "baseline_id": self.id,
            "verified_at": datetime.utcnow().isoformat(),
            "total": len(self.artifacts),
            "valid_count": 0,
            "modified_count": 0,
            "missing_count": 0,
            "unchecked_count": 0,
            "details": {},
        }
        
        for artifact in self.artifacts:
            status = artifact.verify(root_path)
            results["details"][artifact.artifact_id] = status.value
            
            if status == ArtifactStatus.VALID:
                results["valid_count"] += 1
            elif status == ArtifactStatus.MODIFIED:
                results["modified_count"] += 1
            elif status == ArtifactStatus.MISSING:
                results["missing_count"] += 1
            else:
                results["unchecked_count"] += 1
        
        results["valid"] = (
            results["valid_count"] == results["total"] and results["total"] > 0
        )
        
        return results
    
    def compute_manifest_hash(self) -> str:
        """
        Compute hash of the entire baseline manifest.
        
        This provides a single hash representing the entire baseline state.
        """
        # Sort artifacts by ID for deterministic hashing
        sorted_artifacts = sorted(self.artifacts, key=lambda a: a.artifact_id)
        
        manifest_data = {
            "baseline_id": self.id,
            "version": self.version,
            "artifacts": [
                {"id": a.artifact_id, "hash": a.hash, "version": a.version}
                for a in sorted_artifacts
            ]
        }
        
        manifest_json = json.dumps(manifest_data, sort_keys=True)
        return f"sha256:{hashlib.sha256(manifest_json.encode()).hexdigest()}"
    
    # ==========================================================================
    # Delta Computation
    # ==========================================================================
    
    def compute_delta(self, other: "Baseline") -> BaselineDelta:
        """
        Compute changes between this baseline and another.
        
        Args:
            other: Baseline to compare against (typically newer)
            
        Returns:
            BaselineDelta describing the changes
        """
        self_ids = self.artifact_ids
        other_ids = other.artifact_ids
        
        added = list(other_ids - self_ids)
        removed = list(self_ids - other_ids)
        
        # Check for modifications (same ID, different hash)
        common_ids = self_ids & other_ids
        modified = []
        for artifact_id in common_ids:
            self_artifact = self.get_artifact(artifact_id)
            other_artifact = other.get_artifact(artifact_id)
            if self_artifact and other_artifact:
                if self_artifact.hash != other_artifact.hash:
                    modified.append(artifact_id)
        
        return BaselineDelta(
            from_baseline=self.id,
            to_baseline=other.id,
            added=sorted(added),
            modified=sorted(modified),
            removed=sorted(removed),
            computed_at=datetime.utcnow(),
        )
    
    # ==========================================================================
    # Serialization
    # ==========================================================================
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert baseline to dictionary representation."""
        result = {
            "baseline": {
                "id": self.id,
                "type": self.type.value,
                "status": self.state.value,
                "version": self.version,
                "description": self.description,
            }
        }
        
        if self.scope.ata_chapters or self.scope.lifecycle_phases:
            result["baseline"]["scope"] = {
                "ata_chapters": self.scope.ata_chapters,
                "lifecycle_phases": self.scope.lifecycle_phases,
            }
        
        if self.artifacts:
            result["baseline"]["contents"] = [a.to_dict() for a in self.artifacts]
        
        if self.effectivity:
            eff = {}
            if self.effectivity.established_date:
                eff["established_date"] = self.effectivity.established_date.isoformat()
            if self.effectivity.superseded_date:
                eff["superseded_date"] = self.effectivity.superseded_date.isoformat()
            if self.effectivity.msn_range:
                eff["msn_range"] = list(self.effectivity.msn_range)
            if eff:
                result["baseline"]["effectivity"] = eff
        
        if self.authority:
            auth = {}
            if self.authority.ccb_reference:
                auth["ccb_reference"] = self.authority.ccb_reference
            if self.authority.approved_by:
                auth["approved_by"] = self.authority.approved_by
            if self.authority.approval_date:
                auth["approval_date"] = self.authority.approval_date.isoformat()
            if auth:
                result["baseline"]["authority"] = auth
        
        if self.parent_baseline:
            result["baseline"]["parent_baseline"] = self.parent_baseline
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], file_path: Optional[Path] = None) -> "Baseline":
        """Create Baseline from dictionary."""
        baseline_data = data.get("baseline", data)
        
        # Parse scope
        scope_data = baseline_data.get("scope", {})
        scope = BaselineScope(
            ata_chapters=scope_data.get("ata_chapters", []),
            lifecycle_phases=scope_data.get("lifecycle_phases", []),
            artifact_types=scope_data.get("artifact_types", []),
            paths=scope_data.get("paths", []),
        )
        
        # Parse artifacts
        artifacts = []
        for item in baseline_data.get("contents", []):
            artifacts.append(BaselineArtifact(
                artifact_id=item["artifact_id"],
                path=item["path"],
                hash=item["hash"],
                version=item["version"],
                artifact_type=item.get("type", "unknown"),
                lifecycle_phase=item.get("lifecycle_phase"),
                ata_chapter=item.get("ata_chapter"),
                metadata=item.get("metadata", {}),
            ))
        
        # Parse effectivity
        effectivity = None
        if "effectivity" in baseline_data:
            eff = baseline_data["effectivity"]
            effectivity = BaselineEffectivity(
                established_date=_parse_datetime(eff.get("established_date")),
                superseded_date=_parse_datetime(eff.get("superseded_date")),
                msn_range=tuple(eff["msn_range"]) if eff.get("msn_range") else None,
                tail_numbers=eff.get("tail_numbers", []),
                mod_status=eff.get("mod_status", {}),
            )
        
        # Parse authority
        authority = None
        if "authority" in baseline_data:
            auth = baseline_data["authority"]
            authority = BaselineAuthority(
                ccb_reference=auth.get("ccb_reference"),
                eco_reference=auth.get("eco_reference"),
                approved_by=auth.get("approved_by"),
                approver_name=auth.get("approver_name"),
                approval_date=_parse_datetime(auth.get("approval_date")),
                signature_ref=auth.get("signature_ref"),
            )
        
        baseline = cls(
            id=baseline_data["id"],
            type=BaselineType(baseline_data["type"]),
            state=BaselineState(baseline_data.get("status", "DRAFT")),
            version=baseline_data.get("version", "1.0.0"),
            description=baseline_data.get("description", ""),
            scope=scope,
            artifacts=artifacts,
            effectivity=effectivity,
            authority=authority,
            parent_baseline=baseline_data.get("parent_baseline"),
            created_date=_parse_datetime(baseline_data.get("created_date")),
            released_date=_parse_datetime(baseline_data.get("released_date")),
        )
        
        baseline._file_path = file_path
        return baseline
    
    @classmethod
    def load(cls, path: Path) -> "Baseline":
        """
        Load baseline from YAML file.
        
        Args:
            path: Path to baseline YAML file
            
        Returns:
            Baseline instance
        """
        if not path.exists():
            raise FileNotFoundError(f"Baseline file not found: {path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        return cls.from_dict(data, file_path=path)
    
    def save(self, path: Path) -> None:
        """
        Save baseline to YAML file.
        
        Args:
            path: Destination path
        """
        data = self.to_dict()
        
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        
        self._file_path = path


# =============================================================================
# BASELINE MANAGER
# =============================================================================


class BaselineError(Exception):
    """Base exception for baseline errors."""
    pass


class BaselineNotFoundError(BaselineError):
    """Raised when a baseline cannot be found."""
    pass


class BaselineIntegrityError(BaselineError):
    """Raised when baseline integrity verification fails."""
    pass


class BaselineStateError(BaselineError):
    """Raised for invalid state transitions."""
    pass


class BaselineManager:
    """
    Manages ASIT baselines.
    
    Provides baseline registration, lookup, lifecycle management,
    and integrity verification.
    
    Usage:
        >>> manager = BaselineManager(Path("ASIT/GOVERNANCE"))
        >>> baseline = manager.get_baseline("FBL-2026-Q1-003")
        >>> if baseline.is_usable():
        ...     integrity = manager.verify_baseline(baseline.id, kdb_root)
    """
    
    # Baseline ID pattern: TYPE-YEAR-QUARTER-SEQUENCE
    BASELINE_ID_PATTERN = re.compile(
        r"^(FBL|ABL|DBL|PBL|OBL)-\d{4}-Q[1-4]-\d{3}$"
    )
    
    def __init__(self, governance_root: Path):
        """
        Initialize baseline manager.
        
        Args:
            governance_root: Path to ASIT/GOVERNANCE directory
        """
        self.governance_root = Path(governance_root)
        self.register_path = self.governance_root / "BASELINE_REGISTER.csv"
        self.baselines_dir = self.governance_root / "baselines"
        
        self._baselines: Dict[str, Baseline] = {}
        self._register: List[Dict[str, str]] = []
        
        self._load_register()
    
    def _load_register(self) -> None:
        """Load baseline register from CSV."""
        if not self.register_path.exists():
            logger.warning(f"Baseline register not found: {self.register_path}")
            return
        
        self._register.clear()
        self._baselines.clear()
        
        with open(self.register_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Skip comment rows
                if row.get("baseline_id", "").startswith("#"):
                    continue
                if not row.get("baseline_id"):
                    continue
                
                self._register.append(dict(row))
                
                # Create baseline from register entry
                try:
                    baseline = Baseline(
                        id=row["baseline_id"],
                        type=BaselineType(row["type"]),
                        state=BaselineState(row["state"]),
                        version=row.get("version", "1.0.0"),
                        description=row.get("description", ""),
                        created_date=_parse_datetime(row.get("created_date")),
                        released_date=_parse_datetime(row.get("released_date")),
                    )
                    
                    if row.get("authority") or row.get("eco_ref"):
                        baseline.authority = BaselineAuthority(
                            approved_by=row.get("authority"),
                            eco_reference=row.get("eco_ref"),
                        )
                    
                    self._baselines[baseline.id] = baseline
                except Exception as e:
                    logger.warning(f"Failed to parse baseline {row.get('baseline_id')}: {e}")
    
    def _save_register(self) -> None:
        """Save baseline register to CSV."""
        fieldnames = [
            "baseline_id", "type", "version", "state",
            "created_date", "released_date", "authority", "eco_ref", "description"
        ]
        
        with open(self.register_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for baseline in sorted(self._baselines.values(), key=lambda b: b.id):
                row = {
                    "baseline_id": baseline.id,
                    "type": baseline.type.value,
                    "version": baseline.version,
                    "state": baseline.state.value,
                    "created_date": baseline.created_date.strftime("%Y-%m-%d") 
                        if baseline.created_date else "",
                    "released_date": baseline.released_date.strftime("%Y-%m-%d") 
                        if baseline.released_date else "",
                    "authority": baseline.authority.approved_by 
                        if baseline.authority else "",
                    "eco_ref": baseline.authority.eco_reference 
                        if baseline.authority else "",
                    "description": baseline.description,
                }
                writer.writerow(row)
    
    # =========================================================================
    # Baseline Lookup
    # =========================================================================
    
    def get_baseline(self, baseline_id: str) -> Baseline:
        """
        Retrieve baseline by ID.
        
        Args:
            baseline_id: Baseline identifier
            
        Returns:
            Baseline instance
            
        Raises:
            BaselineNotFoundError: If baseline doesn't exist
        """
        if baseline_id not in self._baselines:
            raise BaselineNotFoundError(f"Baseline not found: {baseline_id}")
        return self._baselines[baseline_id]
    
    def get_latest(
        self, 
        baseline_type: BaselineType,
        state: Optional[BaselineState] = None
    ) -> Optional[Baseline]:
        """
        Get the latest baseline of a given type.
        
        Args:
            baseline_type: Type to filter by
            state: Optional state filter (default: RELEASED)
            
        Returns:
            Latest matching baseline, or None if none found
        """
        if state is None:
            state = BaselineState.RELEASED
        
        candidates = [
            b for b in self._baselines.values()
            if b.type == baseline_type and b.state == state
        ]
        
        if not candidates:
            return None
        
        # Sort by ID (assumes chronological naming convention)
        return max(candidates, key=lambda b: b.id)
    
    def list_baselines(
        self,
        baseline_type: Optional[BaselineType] = None,
        state: Optional[BaselineState] = None,
    ) -> List[Baseline]:
        """
        List baselines with optional filtering.
        
        Args:
            baseline_type: Filter by type
            state: Filter by state
            
        Returns:
            List of matching baselines, sorted by ID
        """
        result = list(self._baselines.values())
        
        if baseline_type:
            result = [b for b in result if b.type == baseline_type]
        if state:
            result = [b for b in result if b.state == state]
        
        return sorted(result, key=lambda b: b.id)
    
    def list_usable_baselines(self) -> List[Baseline]:
        """List all baselines that can be used for transformations."""
        return [b for b in self._baselines.values() if b.is_usable()]
    
    def exists(self, baseline_id: str) -> bool:
        """Check if a baseline exists."""
        return baseline_id in self._baselines
    
    # =========================================================================
    # Baseline Lifecycle
    # =========================================================================
    
    def create_baseline(
        self,
        baseline_type: BaselineType,
        description: str = "",
        parent_baseline: Optional[str] = None,
        scope: Optional[BaselineScope] = None,
    ) -> Baseline:
        """
        Create a new baseline in DRAFT state.
        
        Args:
            baseline_type: Type of baseline to create
            description: Human-readable description
            parent_baseline: ID of parent baseline (if derived)
            scope: Optional scope specification
            
        Returns:
            New Baseline in DRAFT state
        """
        # Generate ID
        baseline_id = self._generate_baseline_id(baseline_type)
        
        baseline = Baseline(
            id=baseline_id,
            type=baseline_type,
            state=BaselineState.DRAFT,
            version="1.0.0",
            description=description,
            scope=scope or BaselineScope(),
            parent_baseline=parent_baseline,
            created_date=datetime.utcnow(),
        )
        
        self._baselines[baseline_id] = baseline
        self._save_register()
        
        logger.info(f"Created baseline: {baseline_id}")
        return baseline
    
    def _generate_baseline_id(self, baseline_type: BaselineType) -> str:
        """Generate a new baseline ID."""
        now = datetime.utcnow()
        year = now.year
        quarter = f"Q{(now.month - 1) // 3 + 1}"
        prefix = f"{baseline_type.value}-{year}-{quarter}"
        
        # Find highest sequence number for this prefix
        existing = [
            b.id for b in self._baselines.values()
            if b.id.startswith(prefix)
        ]
        
        if existing:
            max_seq = max(int(bid.split("-")[-1]) for bid in existing)
            sequence = max_seq + 1
        else:
            sequence = 1
        
        return f"{prefix}-{sequence:03d}"
    
    def submit_for_review(self, baseline_id: str) -> None:
        """
        Submit baseline for CCB review.
        
        Transitions from DRAFT to REVIEW state.
        """
        baseline = self.get_baseline(baseline_id)
        
        if baseline.state != BaselineState.DRAFT:
            raise BaselineStateError(
                f"Cannot submit baseline in {baseline.state.value} state"
            )
        
        baseline.state = BaselineState.REVIEW
        self._save_register()
        logger.info(f"Baseline {baseline_id} submitted for review")
    
    def approve(
        self,
        baseline_id: str,
        approved_by: str,
        ccb_reference: Optional[str] = None,
    ) -> None:
        """
        Approve a baseline.
        
        Transitions from REVIEW to APPROVED state.
        """
        baseline = self.get_baseline(baseline_id)
        
        if baseline.state != BaselineState.REVIEW:
            raise BaselineStateError(
                f"Cannot approve baseline in {baseline.state.value} state"
            )
        
        baseline.state = BaselineState.APPROVED
        baseline.authority = BaselineAuthority(
            approved_by=approved_by,
            ccb_reference=ccb_reference,
            approval_date=datetime.utcnow(),
        )
        
        self._save_register()
        logger.info(f"Baseline {baseline_id} approved by {approved_by}")
    
    def release(self, baseline_id: str) -> None:
        """
        Release a baseline for use.
        
        Transitions from APPROVED to RELEASED state.
        Baseline becomes immutable.
        """
        baseline = self.get_baseline(baseline_id)
        
        if baseline.state != BaselineState.APPROVED:
            raise BaselineStateError(
                f"Cannot release baseline in {baseline.state.value} state"
            )
        
        baseline.state = BaselineState.RELEASED
        baseline.released_date = datetime.utcnow()
        
        self._save_register()
        logger.info(f"Baseline {baseline_id} released")
    
    def supersede(self, baseline_id: str, successor_id: str) -> None:
        """
        Mark a baseline as superseded.
        
        Args:
            baseline_id: Baseline to supersede
            successor_id: Baseline that replaces it
        """
        baseline = self.get_baseline(baseline_id)
        successor = self.get_baseline(successor_id)
        
        if not baseline.is_released():
            raise BaselineStateError("Only released baselines can be superseded")
        
        baseline.state = BaselineState.SUPERSEDED
        if baseline.effectivity:
            baseline.effectivity.superseded_date = datetime.utcnow()
        else:
            baseline.effectivity = BaselineEffectivity(
                superseded_date=datetime.utcnow()
            )
        
        self._save_register()
        logger.info(f"Baseline {baseline_id} superseded by {successor_id}")
    
    # =========================================================================
    # Integrity Verification
    # =========================================================================
    
    def verify_baseline(
        self,
        baseline_id: str,
        root_path: Path
    ) -> Dict[str, Any]:
        """
        Verify baseline integrity.
        
        Args:
            baseline_id: Baseline to verify
            root_path: Root path for artifact resolution
            
        Returns:
            Verification results
        """
        baseline = self.get_baseline(baseline_id)
        return baseline.verify_integrity(root_path)
    
    # =========================================================================
    # ID Validation
    # =========================================================================
    
    def validate_baseline_id(self, baseline_id: str) -> bool:
        """Check if baseline ID follows naming convention."""
        return bool(self.BASELINE_ID_PATTERN.match(baseline_id))
    
    # =========================================================================
    # Reload
    # =========================================================================
    
    def reload(self) -> None:
        """Reload baseline register from disk."""
        self._load_register()


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def _parse_datetime(value: Optional[str]) -> Optional[datetime]:
    """Parse datetime string to datetime object."""
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        pass
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return None


# =============================================================================
# MODULE EXPORTS
# =============================================================================


__all__ = [
    # Enums
    "BaselineType",
    "BaselineState",
    "ArtifactStatus",
    
    # Data classes
    "BaselineArtifact",
    "BaselineScope",
    "BaselineEffectivity",
    "BaselineAuthority",
    "BaselineDelta",
    
    # Main classes
    "Baseline",
    "BaselineManager",
    
    # Exceptions
    "BaselineError",
    "BaselineNotFoundError",
    "BaselineIntegrityError",
    "BaselineStateError",
]
