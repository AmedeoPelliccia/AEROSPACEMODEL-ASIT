"""
TDMS Planes Module
==================

Defines the dual-plane representation for document management:

1. Human Plane (HumanPlane):
   - Authoritative, editable representation
   - Uses YAML/JSON/XML formats
   - Source of truth for all content
   - Designed for human review and audit

2. Machine Plane (MachinePlane):
   - Runtime, token-efficient representation
   - Uses TSV/CSV/Line Protocol formats
   - Derived view for AI agents and loops
   - Optimized for context window efficiency

The planes are complementary, not competing:
    Human Plane = Source of Truth
    Machine Plane = Derived View for Agents
"""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Union

import yaml

from aerospacemodel.tdms.exceptions import TDMSError
from aerospacemodel.tdms.formats import (
    TSVFormat,
    CSVFormat,
    LineProtocolFormat,
)
from aerospacemodel.tdms.dictionary import (
    DictionaryRegistry,
    DictionaryType,
)

logger = logging.getLogger(__name__)


class PlaneType(Enum):
    """Types of TDMS representation planes."""
    HUMAN = "human"       # Human-readable, authoritative
    MACHINE = "machine"   # Token-efficient, derived


@dataclass
class PlaneMetadata:
    """
    Metadata for a TDMS plane instance.
    
    Tracks provenance and validity of plane data.
    """
    plane_type: PlaneType
    source_hash: str = ""           # Hash of source content
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
    derived_from: Optional[str] = None  # Path/ID of source
    version: str = "1.0.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "plane_type": self.plane_type.value,
            "source_hash": self.source_hash,
            "created": self.created.isoformat() if self.created else None,
            "modified": self.modified.isoformat() if self.modified else None,
            "derived_from": self.derived_from,
            "version": self.version,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PlaneMetadata:
        """Create from dictionary."""
        return cls(
            plane_type=PlaneType(data["plane_type"]),
            source_hash=data.get("source_hash", ""),
            created=datetime.fromisoformat(data["created"]) if data.get("created") else None,
            modified=datetime.fromisoformat(data["modified"]) if data.get("modified") else None,
            derived_from=data.get("derived_from"),
            version=data.get("version", "1.0.0"),
        )


@dataclass
class HumanPlane:
    """
    Human Plane representation.
    
    The authoritative, editable representation of document data.
    Uses YAML/JSON/XML formats for human readability.
    
    This is the SOURCE OF TRUTH in the TDMS architecture.
    
    Attributes:
        data: The document data as nested dictionaries
        metadata: Plane metadata for tracking
        schema: Optional schema reference for validation
        
    Example:
        >>> human = HumanPlane.load("contract.yaml")
        >>> print(human.data["header"]["title"])
        'Fuel System CSDB Generation'
        >>> human.data["header"]["status"] = "APPROVED"
        >>> human.save("contract_updated.yaml")
    """
    data: Dict[str, Any]
    metadata: PlaneMetadata = field(default_factory=lambda: PlaneMetadata(PlaneType.HUMAN))
    schema: Optional[str] = None
    
    def __post_init__(self) -> None:
        """Initialize metadata timestamps."""
        now = datetime.now()
        if self.metadata.created is None:
            self.metadata.created = now
        self.metadata.modified = now
        self._compute_hash()
    
    def _compute_hash(self) -> None:
        """Compute content hash for integrity tracking."""
        content = json.dumps(self.data, sort_keys=True, default=str)
        self.metadata.source_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def get(self, path: str, default: Any = None) -> Any:
        """
        Get value by dot-notation path.
        
        Args:
            path: Dot-separated path (e.g., "header.title")
            default: Default value if path not found
            
        Returns:
            Value at path or default
        """
        keys = path.split(".")
        value = self.data
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    return default
            else:
                return default
        return value
    
    def set(self, path: str, value: Any) -> None:
        """
        Set value by dot-notation path.
        
        Args:
            path: Dot-separated path
            value: Value to set
        """
        keys = path.split(".")
        data = self.data
        for key in keys[:-1]:
            if key not in data:
                data[key] = {}
            data = data[key]
        data[keys[-1]] = value
        self.metadata.modified = datetime.now()
        self._compute_hash()
    
    def to_dict(self) -> Dict[str, Any]:
        """Export complete plane with metadata."""
        return {
            "_metadata": self.metadata.to_dict(),
            "_schema": self.schema,
            **self.data,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> HumanPlane:
        """Create from dictionary including metadata."""
        metadata_data = data.pop("_metadata", None)
        schema = data.pop("_schema", None)
        
        metadata = PlaneMetadata.from_dict(metadata_data) if metadata_data else PlaneMetadata(PlaneType.HUMAN)
        
        return cls(data=data, metadata=metadata, schema=schema)
    
    def save(self, path: Union[str, Path], format: str = "yaml") -> None:
        """
        Save to file.
        
        Args:
            path: Output path
            format: Format ('yaml' or 'json')
        """
        path = Path(path)
        self.metadata.modified = datetime.now()
        self._compute_hash()
        
        with open(path, "w", encoding="utf-8") as f:
            if format == "yaml":
                yaml.safe_dump(self.data, f, default_flow_style=False, sort_keys=False)
            elif format == "json":
                json.dump(self.data, f, indent=2, default=str)
            else:
                raise TDMSError(f"Unsupported format: {format}")
        
        logger.info(f"HumanPlane saved to {path}")
    
    @classmethod
    def load(cls, path: Union[str, Path]) -> HumanPlane:
        """
        Load from file.
        
        Args:
            path: Input path (YAML or JSON)
            
        Returns:
            Loaded HumanPlane instance
            
        Raises:
            TDMSError: If file format is unsupported or content is not a mapping
        """
        path = Path(path)
        
        with open(path, "r", encoding="utf-8") as f:
            if path.suffix in [".yaml", ".yml"]:
                data = yaml.safe_load(f)
            elif path.suffix == ".json":
                data = json.load(f)
            else:
                raise TDMSError(f"Unsupported file format: {path.suffix}")
        
        # Ensure the loaded document has a mapping/object at the root level.
        if not isinstance(data, dict):
            raise TDMSError(
                f"Invalid TDMS document structure in {path}: "
                f"root element must be a mapping/object, got {type(data).__name__}."
            )
        
        instance = cls(data=data)
        instance.metadata.derived_from = str(path)
        return instance
    
    def flatten(self, prefix: str = "") -> Dict[str, Any]:
        """
        Flatten nested structure to dot-notation keys.
        
        Args:
            prefix: Key prefix for recursion
            
        Returns:
            Flattened dictionary
        """
        result = {}
        
        def _flatten(obj: Any, current_prefix: str) -> None:
            if isinstance(obj, dict):
                for key, value in obj.items():
                    new_key = f"{current_prefix}.{key}" if current_prefix else key
                    _flatten(value, new_key)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    _flatten(item, f"{current_prefix}[{i}]")
            else:
                result[current_prefix] = obj
        
        _flatten(self.data, prefix)
        return result
    
    def validate(self) -> List[str]:
        """
        Validate plane data.
        
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        # Basic structure validation
        if not self.data:
            errors.append("Empty data structure")
        
        # Check for required top-level keys (configurable per schema)
        # This is a basic check; full schema validation would use jsonschema
        
        return errors


@dataclass  
class MachinePlane:
    """
    Machine Plane representation.
    
    The token-efficient, runtime representation for AI agents.
    Uses TSV/CSV/Line Protocol formats for compactness.
    
    This is a DERIVED VIEW in the TDMS architecture.
    The Human Plane remains the source of truth.
    
    Attributes:
        records: List of flat record dictionaries
        columns: Column order for serialization
        metadata: Plane metadata
        dictionary_registry: Registry for ID disambiguation
        
    Example:
        >>> machine = MachinePlane.from_tsv("contracts.tsv")
        >>> for record in machine.records:
        ...     print(f"{record['id']}: {record['status']}")
        CTR001: APV
        CTR002: DFT
    """
    records: List[Dict[str, Any]] = field(default_factory=list)
    columns: List[str] = field(default_factory=list)
    metadata: PlaneMetadata = field(default_factory=lambda: PlaneMetadata(PlaneType.MACHINE))
    dictionary_registry: Optional[DictionaryRegistry] = None
    
    def __post_init__(self) -> None:
        """Initialize metadata and columns."""
        now = datetime.now()
        if self.metadata.created is None:
            self.metadata.created = now
        self.metadata.modified = now
        
        # Infer columns from records if not specified
        if not self.columns and self.records:
            self.columns = list(self.records[0].keys())
        
        self._compute_hash()
    
    def _compute_hash(self) -> None:
        """Compute content hash."""
        content = json.dumps(self.records, sort_keys=True, default=str)
        self.metadata.source_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def __len__(self) -> int:
        """Return number of records."""
        return len(self.records)
    
    def __iter__(self) -> Iterator[Dict[str, Any]]:
        """Iterate over records."""
        return iter(self.records)
    
    def __getitem__(self, index: int) -> Dict[str, Any]:
        """Get record by index."""
        return self.records[index]
    
    def add_record(self, record: Dict[str, Any]) -> None:
        """Add a record to the plane."""
        self.records.append(record)
        self.metadata.modified = datetime.now()
        
        # Update columns if needed
        for key in record.keys():
            if key not in self.columns:
                self.columns.append(key)
        
        self._compute_hash()
    
    def filter(self, **criteria: Any) -> List[Dict[str, Any]]:
        """
        Filter records by criteria.
        
        Args:
            **criteria: Key-value pairs to match
            
        Returns:
            List of matching records
        """
        results = []
        for record in self.records:
            match = all(record.get(k) == v for k, v in criteria.items())
            if match:
                results.append(record)
        return results
    
    def get_column_values(self, column: str) -> List[Any]:
        """Get all values for a column."""
        return [r.get(column) for r in self.records]
    
    def to_tsv(self, path: Optional[Union[str, Path]] = None) -> str:
        """
        Export to TSV format.
        
        Args:
            path: Optional output file path
            
        Returns:
            TSV string
        """
        handler = TSVFormat()
        content = handler.serialize(self.records, self.columns)
        
        if path:
            path = Path(path)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info(f"MachinePlane exported to TSV: {path}")
        
        return content
    
    def to_csv(self, path: Optional[Union[str, Path]] = None) -> str:
        """
        Export to CSV format.
        
        Args:
            path: Optional output file path
            
        Returns:
            CSV string
        """
        handler = CSVFormat()
        content = handler.serialize(self.records, self.columns)
        
        if path:
            path = Path(path)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info(f"MachinePlane exported to CSV: {path}")
        
        return content
    
    def to_line_protocol(self, path: Optional[Union[str, Path]] = None) -> str:
        """
        Export to line protocol format.
        
        Args:
            path: Optional output file path
            
        Returns:
            Line protocol string
        """
        handler = LineProtocolFormat()
        content = handler.serialize(self.records)
        
        if path:
            path = Path(path)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info(f"MachinePlane exported to line protocol: {path}")
        
        return content
    
    @classmethod
    def from_tsv(
        cls,
        source: Union[str, Path],
        dictionary_registry: Optional[DictionaryRegistry] = None,
    ) -> MachinePlane:
        """
        Load from TSV file or string.
        
        Args:
            source: File path or TSV string
            dictionary_registry: Optional dictionary registry
            
        Returns:
            MachinePlane instance
        """
        handler = TSVFormat()
        
        # Check if source is a Path object or a path string that exists
        source_path = None
        if isinstance(source, Path):
            source_path = source
        elif isinstance(source, str):
            try:
                potential_path = Path(source)
                if potential_path.exists():
                    source_path = potential_path
            except (OSError, ValueError):
                pass  # Not a valid path
        
        if source_path and source_path.exists():
            records = handler.read(source_path)
            derived_from = str(source_path)
        else:
            records = handler.deserialize(str(source))
            derived_from = None
        
        instance = cls(records=records, dictionary_registry=dictionary_registry)
        if derived_from:
            instance.metadata.derived_from = derived_from
        return instance
    
    @classmethod
    def from_csv(
        cls,
        source: Union[str, Path],
        dictionary_registry: Optional[DictionaryRegistry] = None,
    ) -> MachinePlane:
        """Load from CSV file or string."""
        handler = CSVFormat()
        
        # Check if source is a Path object or a path string that exists
        source_path = None
        if isinstance(source, Path):
            source_path = source
        elif isinstance(source, str):
            try:
                potential_path = Path(source)
                if potential_path.exists():
                    source_path = potential_path
            except (OSError, ValueError):
                pass  # Not a valid path
        
        if source_path and source_path.exists():
            records = handler.read(source_path)
            derived_from = str(source_path)
        else:
            records = handler.deserialize(str(source))
            derived_from = None
        
        instance = cls(records=records, dictionary_registry=dictionary_registry)
        if derived_from:
            instance.metadata.derived_from = derived_from
        return instance
    
    @classmethod
    def from_line_protocol(
        cls,
        source: Union[str, Path],
        dictionary_registry: Optional[DictionaryRegistry] = None,
    ) -> MachinePlane:
        """Load from line protocol file or string."""
        handler = LineProtocolFormat()
        
        # Check if source is a Path object or a path string that exists
        source_path = None
        if isinstance(source, Path):
            source_path = source
        elif isinstance(source, str):
            try:
                potential_path = Path(source)
                if potential_path.exists():
                    source_path = potential_path
            except (OSError, ValueError):
                pass  # Not a valid path
        
        if source_path and source_path.exists():
            records = handler.read(source_path)
            derived_from = str(source_path)
        else:
            records = handler.deserialize(str(source))
            derived_from = None
        
        instance = cls(records=records, dictionary_registry=dictionary_registry)
        if derived_from:
            instance.metadata.derived_from = derived_from
        return instance
    
    def resolve_ids(self) -> MachinePlane:
        """
        Create new plane with IDs resolved to full values.
        
        Uses the dictionary registry to expand compact IDs.
        
        Returns:
            New MachinePlane with resolved values
        """
        if not self.dictionary_registry:
            return self
        
        resolved_records = []
        for record in self.records:
            resolved = dict(record)
            # Attempt to resolve known ID fields
            for field_name, dict_type in [
                ("status", DictionaryType.STATUS),
                ("ata", DictionaryType.ATA),
                ("publication", DictionaryType.PUBLICATION),
                ("baseline_type", DictionaryType.BASELINE),
                ("stakeholder", DictionaryType.STAKEHOLDER),
            ]:
                if field_name in resolved and resolved[field_name]:
                    try:
                        dictionary = self.dictionary_registry.get(dict_type)
                        if dictionary and dictionary.has_id(str(resolved[field_name])):
                            resolved[field_name] = dictionary.get_value(str(resolved[field_name]))
                    except Exception as e:
                        # Log at debug level to aid troubleshooting without crashing
                        logger.debug(f"Could not resolve ID '{resolved[field_name]}' for field '{field_name}': {e}")
            resolved_records.append(resolved)
        
        return MachinePlane(
            records=resolved_records,
            columns=self.columns.copy(),
            dictionary_registry=self.dictionary_registry,
        )
    
    def token_count_estimate(self) -> int:
        """
        Estimate token count for LLM context.
        
        This is a rough approximation using ~4 characters per token,
        which works reasonably well for technical English content.
        Actual token counts may vary based on tokenizer and content.
        
        Returns:
            Estimated token count
        """
        content = self.to_tsv()
        # Rough estimate: 4 chars per token for technical content
        return len(content) // 4
    
    def matches_source_hash(self, source_hash: str) -> bool:
        """
        Check if this derived plane's hash matches a source hash.
        
        Use this to verify that a MachinePlane was derived from
        a specific HumanPlane without modification.
        
        Args:
            source_hash: Hash of the source HumanPlane
            
        Returns:
            True if hashes match
        """
        return self.metadata.source_hash == source_hash


__all__ = [
    "PlaneType",
    "PlaneMetadata",
    "HumanPlane",
    "MachinePlane",
]
