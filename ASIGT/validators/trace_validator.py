# =============================================================================
# ASIGT Trace Validator
# Traceability completeness validation
# Version: 2.0.0
# =============================================================================
"""
Trace Validator

Validates traceability completeness for ASIT-ASIGT transformations.
Ensures that all generated outputs are properly traced to their
source artifacts, supporting certification and audit requirements.

Validates:
- Source-to-target completeness (forward trace)
- Target-to-source completeness (backward trace)
- Trace chain integrity
- Hash verification
- Contract compliance

Operates exclusively under ASIT contract authority.
"""

from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


class TraceType(Enum):
    """Types of traceability relationships."""
    DERIVED = "derived"           # Target derived from source
    TRANSFORMED = "transformed"   # Source transformed to target
    REFERENCES = "references"     # Target references source
    IMPLEMENTS = "implements"     # Target implements source requirement
    VERIFIES = "verifies"        # Target verifies source
    ALLOCATES = "allocates"      # Source allocates to target


class TraceSeverity(Enum):
    """Trace validation issue severity."""
    ERROR = "error"       # Critical - missing required trace
    WARNING = "warning"   # Should be addressed
    INFO = "info"        # Informational


class TraceDirection(Enum):
    """Trace direction for validation."""
    FORWARD = "forward"     # Source → Target
    BACKWARD = "backward"   # Target → Source
    BIDIRECTIONAL = "bidirectional"


@dataclass
class TraceLink:
    """
    A single traceability link.
    
    Connects a source artifact to a target artifact with metadata.
    """
    source_id: str                  # Source artifact ID
    target_id: str                  # Target artifact ID
    trace_type: TraceType          # Relationship type
    contract_id: str               # ASIT contract that created this link
    baseline_ref: str              # Source baseline reference
    source_hash: Optional[str] = None
    target_hash: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "trace_type": self.trace_type.value,
            "contract_id": self.contract_id,
            "baseline_ref": self.baseline_ref,
            "source_hash": self.source_hash,
            "target_hash": self.target_hash,
            "created_at": self.created_at,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TraceLink":
        """Create from dictionary."""
        return cls(
            source_id=data["source_id"],
            target_id=data["target_id"],
            trace_type=TraceType(data["trace_type"]),
            contract_id=data["contract_id"],
            baseline_ref=data["baseline_ref"],
            source_hash=data.get("source_hash"),
            target_hash=data.get("target_hash"),
            created_at=data.get("created_at", datetime.now().isoformat()),
            metadata=data.get("metadata", {}),
        )


@dataclass
class TraceIssue:
    """A traceability validation issue."""
    severity: TraceSeverity
    issue_type: str
    message: str
    source_id: Optional[str] = None
    target_id: Optional[str] = None
    contract_id: Optional[str] = None
    suggestion: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "severity": self.severity.value,
            "issue_type": self.issue_type,
            "message": self.message,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "contract_id": self.contract_id,
            "suggestion": self.suggestion,
        }


@dataclass
class TraceValidationResult:
    """Result of trace validation."""
    valid: bool
    contract_id: str
    total_links: int = 0
    forward_coverage: float = 0.0      # % of sources with targets
    backward_coverage: float = 0.0     # % of targets with sources
    issues: List[TraceIssue] = field(default_factory=list)
    errors: int = 0
    warnings: int = 0
    validated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def add_issue(self, issue: TraceIssue) -> None:
        """Add an issue and update counts."""
        self.issues.append(issue)
        if issue.severity == TraceSeverity.ERROR:
            self.errors += 1
            self.valid = False
        elif issue.severity == TraceSeverity.WARNING:
            self.warnings += 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "valid": self.valid,
            "contract_id": self.contract_id,
            "total_links": self.total_links,
            "forward_coverage": self.forward_coverage,
            "backward_coverage": self.backward_coverage,
            "errors": self.errors,
            "warnings": self.warnings,
            "issues": [i.to_dict() for i in self.issues],
            "validated_at": self.validated_at,
        }


class TraceMatrix:
    """
    Traceability matrix for managing trace links.
    
    Maintains source-target relationships and supports
    validation queries.
    """
    
    def __init__(self):
        """Initialize empty trace matrix."""
        self._links: List[TraceLink] = []
        self._source_index: Dict[str, List[int]] = {}  # source_id -> link indices
        self._target_index: Dict[str, List[int]] = {}  # target_id -> link indices
    
    def add_link(self, link: TraceLink) -> None:
        """Add a trace link."""
        index = len(self._links)
        self._links.append(link)
        
        # Update source index
        if link.source_id not in self._source_index:
            self._source_index[link.source_id] = []
        self._source_index[link.source_id].append(index)
        
        # Update target index
        if link.target_id not in self._target_index:
            self._target_index[link.target_id] = []
        self._target_index[link.target_id].append(index)
    
    def get_links_from_source(self, source_id: str) -> List[TraceLink]:
        """Get all links from a source."""
        indices = self._source_index.get(source_id, [])
        return [self._links[i] for i in indices]
    
    def get_links_to_target(self, target_id: str) -> List[TraceLink]:
        """Get all links to a target."""
        indices = self._target_index.get(target_id, [])
        return [self._links[i] for i in indices]
    
    def get_all_sources(self) -> Set[str]:
        """Get all source IDs."""
        return set(self._source_index.keys())
    
    def get_all_targets(self) -> Set[str]:
        """Get all target IDs."""
        return set(self._target_index.keys())
    
    def get_all_links(self) -> List[TraceLink]:
        """Get all links."""
        return self._links.copy()
    
    def has_forward_trace(self, source_id: str) -> bool:
        """Check if source has at least one target."""
        return source_id in self._source_index and len(self._source_index[source_id]) > 0
    
    def has_backward_trace(self, target_id: str) -> bool:
        """Check if target has at least one source."""
        return target_id in self._target_index and len(self._target_index[target_id]) > 0
    
    def get_trace_chain(
        self,
        start_id: str,
        direction: TraceDirection = TraceDirection.FORWARD,
        max_depth: int = 10,
    ) -> List[List[str]]:
        """
        Get trace chain from start ID.
        
        Args:
            start_id: Starting artifact ID
            direction: Trace direction
            max_depth: Maximum chain depth
            
        Returns:
            List of paths (each path is a list of IDs)
        """
        paths = []
        
        def traverse(current_id: str, path: List[str], depth: int):
            if depth > max_depth:
                return
            
            new_path = path + [current_id]
            
            if direction == TraceDirection.FORWARD:
                links = self.get_links_from_source(current_id)
                next_ids = [link.target_id for link in links]
            else:
                links = self.get_links_to_target(current_id)
                next_ids = [link.source_id for link in links]
            
            if not next_ids:
                paths.append(new_path)
            else:
                for next_id in next_ids:
                    if next_id not in path:  # Avoid cycles
                        traverse(next_id, new_path, depth + 1)
        
        traverse(start_id, [], 0)
        return paths
    
    def to_csv(self) -> str:
        """Export matrix to CSV format."""
        lines = [
            "source_id,target_id,trace_type,contract_id,baseline_ref,source_hash,target_hash,created_at"
        ]
        
        for link in self._links:
            lines.append(
                f"{link.source_id},{link.target_id},{link.trace_type.value},"
                f"{link.contract_id},{link.baseline_ref},"
                f"{link.source_hash or ''},{link.target_hash or ''},"
                f"{link.created_at}"
            )
        
        return "\n".join(lines)
    
    def __len__(self) -> int:
        return len(self._links)


class TraceValidator:
    """
    Traceability Validator.
    
    Validates traceability completeness and integrity for
    ASIT-ASIGT transformations. Supports certification
    requirements for full traceability.
    
    Attributes:
        contract: ASIT transformation contract
        config: Validator configuration
        
    Example:
        >>> validator = TraceValidator(contract=contract, config=config)
        >>> validator.add_trace(source_id="REQ-001", target_id="DM-001-040A")
        >>> result = validator.validate(required_sources=source_list)
    """
    
    def __init__(
        self,
        contract: Dict[str, Any],
        config: Dict[str, Any],
    ):
        """
        Initialize Trace Validator.
        
        Args:
            contract: ASIT transformation contract (required)
            config: Validator configuration
            
        Raises:
            ValueError: If contract is missing
        """
        if not contract:
            raise ValueError("ASIT contract is required for trace validation")
        
        self.contract = contract
        self.config = config
        
        # Contract parameters
        self.contract_id = contract.get("id", "UNKNOWN")
        self.baseline_ref = contract.get("source", {}).get("baseline", "UNKNOWN")
        
        # Configuration
        self.require_complete = config.get("require_complete", True)
        self.require_bidirectional = config.get("require_bidirectional", False)
        self.require_hash = config.get("require_hash", True)
        
        # Trace matrix
        self.matrix = TraceMatrix()
        
        # Validation tracking
        self._validation_count = 0
        
        logger.info(
            f"TraceValidator initialized: contract={self.contract_id}, "
            f"baseline={self.baseline_ref}"
        )
    
    def add_trace(
        self,
        source_id: str,
        target_id: str,
        trace_type: TraceType = TraceType.DERIVED,
        source_hash: Optional[str] = None,
        target_hash: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> TraceLink:
        """
        Add a trace link.
        
        Args:
            source_id: Source artifact ID
            target_id: Target artifact ID
            trace_type: Type of relationship
            source_hash: SHA-256 hash of source content
            target_hash: SHA-256 hash of target content
            metadata: Additional metadata
            
        Returns:
            Created TraceLink
        """
        link = TraceLink(
            source_id=source_id,
            target_id=target_id,
            trace_type=trace_type,
            contract_id=self.contract_id,
            baseline_ref=self.baseline_ref,
            source_hash=source_hash,
            target_hash=target_hash,
            metadata=metadata or {},
        )
        
        self.matrix.add_link(link)
        logger.debug(f"Added trace: {source_id} -> {target_id}")
        return link
    
    def add_traces_batch(
        self,
        traces: List[Dict[str, Any]],
    ) -> List[TraceLink]:
        """
        Add multiple trace links.
        
        Args:
            traces: List of trace specifications
            
        Returns:
            List of created TraceLinks
        """
        links = []
        for trace in traces:
            link = self.add_trace(
                source_id=trace["source_id"],
                target_id=trace["target_id"],
                trace_type=TraceType(trace.get("trace_type", "derived")),
                source_hash=trace.get("source_hash"),
                target_hash=trace.get("target_hash"),
                metadata=trace.get("metadata"),
            )
            links.append(link)
        return links
    
    def validate(
        self,
        required_sources: Optional[List[str]] = None,
        required_targets: Optional[List[str]] = None,
    ) -> TraceValidationResult:
        """
        Validate traceability completeness.
        
        Args:
            required_sources: List of source IDs that must have traces
            required_targets: List of target IDs that must have traces
            
        Returns:
            TraceValidationResult
        """
        self._validation_count += 1
        result = TraceValidationResult(
            valid=True,
            contract_id=self.contract_id,
            total_links=len(self.matrix),
        )
        
        # Get all traced items
        traced_sources = self.matrix.get_all_sources()
        traced_targets = self.matrix.get_all_targets()
        
        # Validate forward traceability (sources → targets)
        if required_sources:
            sources_with_trace = 0
            for source_id in required_sources:
                if self.matrix.has_forward_trace(source_id):
                    sources_with_trace += 1
                else:
                    result.add_issue(TraceIssue(
                        severity=TraceSeverity.ERROR if self.require_complete else TraceSeverity.WARNING,
                        issue_type="missing_forward_trace",
                        message=f"Source '{source_id}' has no forward trace to any target",
                        source_id=source_id,
                        contract_id=self.contract_id,
                        suggestion="Add trace link from source to generated target",
                    ))
            
            result.forward_coverage = (
                sources_with_trace / len(required_sources) * 100
                if required_sources else 100.0
            )
        else:
            result.forward_coverage = 100.0
        
        # Validate backward traceability (targets → sources)
        if required_targets:
            targets_with_trace = 0
            for target_id in required_targets:
                if self.matrix.has_backward_trace(target_id):
                    targets_with_trace += 1
                else:
                    severity = TraceSeverity.ERROR if self.require_bidirectional else TraceSeverity.WARNING
                    result.add_issue(TraceIssue(
                        severity=severity,
                        issue_type="missing_backward_trace",
                        message=f"Target '{target_id}' has no backward trace to any source",
                        target_id=target_id,
                        contract_id=self.contract_id,
                        suggestion="Add trace link to source artifact",
                    ))
            
            result.backward_coverage = (
                targets_with_trace / len(required_targets) * 100
                if required_targets else 100.0
            )
        else:
            result.backward_coverage = 100.0
        
        # Validate hash integrity
        if self.require_hash:
            for link in self.matrix.get_all_links():
                if not link.source_hash:
                    result.add_issue(TraceIssue(
                        severity=TraceSeverity.WARNING,
                        issue_type="missing_source_hash",
                        message=f"Trace link missing source hash",
                        source_id=link.source_id,
                        target_id=link.target_id,
                        suggestion="Include content hash for verification",
                    ))
                if not link.target_hash:
                    result.add_issue(TraceIssue(
                        severity=TraceSeverity.WARNING,
                        issue_type="missing_target_hash",
                        message=f"Trace link missing target hash",
                        source_id=link.source_id,
                        target_id=link.target_id,
                        suggestion="Include content hash for verification",
                    ))
        
        # Check for orphaned targets (targets with no source)
        all_targets = traced_targets
        if required_targets:
            all_targets = set(required_targets) | traced_targets
        
        for target_id in all_targets:
            if not self.matrix.has_backward_trace(target_id):
                if target_id in (required_targets or []):
                    # Already reported above
                    continue
                result.add_issue(TraceIssue(
                    severity=TraceSeverity.INFO,
                    issue_type="orphaned_target",
                    message=f"Target '{target_id}' is in matrix but has no source trace",
                    target_id=target_id,
                ))
        
        return result
    
    def verify_hash(
        self,
        artifact_id: str,
        content: str,
        is_source: bool = True,
    ) -> Tuple[bool, Optional[str]]:
        """
        Verify content hash against stored trace hash.
        
        Args:
            artifact_id: Artifact ID to verify
            content: Current content
            is_source: True if source, False if target
            
        Returns:
            Tuple of (matches, expected_hash)
        """
        current_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        
        if is_source:
            links = self.matrix.get_links_from_source(artifact_id)
            for link in links:
                if link.source_hash:
                    return (link.source_hash == current_hash, link.source_hash)
        else:
            links = self.matrix.get_links_to_target(artifact_id)
            for link in links:
                if link.target_hash:
                    return (link.target_hash == current_hash, link.target_hash)
        
        return (True, None)  # No hash to verify against
    
    def get_trace_chain(
        self,
        artifact_id: str,
        direction: TraceDirection = TraceDirection.FORWARD,
    ) -> List[List[str]]:
        """Get trace chain from artifact."""
        return self.matrix.get_trace_chain(artifact_id, direction)
    
    def get_impact_analysis(
        self,
        source_id: str,
    ) -> Dict[str, Any]:
        """
        Analyze impact of changes to a source artifact.
        
        Args:
            source_id: Source artifact ID
            
        Returns:
            Impact analysis with affected targets
        """
        direct_targets = [
            link.target_id
            for link in self.matrix.get_links_from_source(source_id)
        ]
        
        # Get full impact chain
        all_affected = set()
        chains = self.get_trace_chain(source_id, TraceDirection.FORWARD)
        for chain in chains:
            all_affected.update(chain[1:])  # Exclude source itself
        
        return {
            "source_id": source_id,
            "direct_impacts": direct_targets,
            "total_affected": list(all_affected),
            "impact_count": len(all_affected),
            "trace_chains": chains,
        }
    
    def export_matrix(self, format: str = "csv") -> str:
        """
        Export trace matrix.
        
        Args:
            format: Export format ("csv", "json")
            
        Returns:
            Exported matrix as string
        """
        if format == "csv":
            return self.matrix.to_csv()
        elif format == "json":
            import json
            return json.dumps(
                [link.to_dict() for link in self.matrix.get_all_links()],
                indent=2,
            )
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get trace statistics."""
        links = self.matrix.get_all_links()
        
        # Count by type
        type_counts = {}
        for link in links:
            t = link.trace_type.value
            type_counts[t] = type_counts.get(t, 0) + 1
        
        return {
            "contract_id": self.contract_id,
            "baseline_ref": self.baseline_ref,
            "total_links": len(links),
            "unique_sources": len(self.matrix.get_all_sources()),
            "unique_targets": len(self.matrix.get_all_targets()),
            "by_type": type_counts,
            "validation_count": self._validation_count,
        }
    
    def generate_report(
        self,
        result: TraceValidationResult,
    ) -> str:
        """Generate a validation report."""
        lines = [
            "=" * 70,
            "TRACEABILITY VALIDATION REPORT",
            f"Contract: {self.contract_id}",
            f"Baseline: {self.baseline_ref}",
            f"Generated: {datetime.now().isoformat()}",
            "=" * 70,
            "",
            f"Total Trace Links: {result.total_links}",
            f"Forward Coverage: {result.forward_coverage:.1f}%",
            f"Backward Coverage: {result.backward_coverage:.1f}%",
            "",
            f"Status: {'VALID' if result.valid else 'INVALID'}",
            f"Errors: {result.errors}",
            f"Warnings: {result.warnings}",
            "",
            "-" * 70,
        ]
        
        if result.issues:
            lines.append("")
            lines.append("ISSUES:")
            lines.append("")
            
            for issue in result.issues:
                severity = issue.severity.value.upper()
                lines.append(f"  [{severity}] {issue.issue_type}")
                lines.append(f"    {issue.message}")
                if issue.source_id:
                    lines.append(f"    Source: {issue.source_id}")
                if issue.target_id:
                    lines.append(f"    Target: {issue.target_id}")
                if issue.suggestion:
                    lines.append(f"    Suggestion: {issue.suggestion}")
                lines.append("")
        
        lines.extend(["", "=" * 70])
        return "\n".join(lines)
