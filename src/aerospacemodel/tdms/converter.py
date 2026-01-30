"""
TDMS Converter Module
=====================

Bidirectional converter between Human Plane and Machine Plane representations.

The converter ensures:
    - Lossless conversion from human to machine plane
    - Validated conversion from machine to human plane
    - Provenance tracking for audit trails
    - Dictionary-based ID compaction/expansion

Conversion Flow:
    Human Plane (YAML/JSON) ──[flatten + compact]──> Machine Plane (TSV/CSV)
    Machine Plane (TSV/CSV) ──[expand + validate]──> Human Plane (YAML/JSON)

Example:
    >>> converter = TDMSConverter()
    >>> 
    >>> # Convert human-readable contract to token-efficient format
    >>> human = HumanPlane.load("contract.yaml")
    >>> machine = converter.to_machine_plane(human)
    >>> machine.to_tsv("contract_compact.tsv")
    >>> 
    >>> # After AI agent processing, convert back
    >>> modified = MachinePlane.from_tsv("agent_output.tsv")
    >>> result = converter.to_human_plane(modified, validate=True)
    >>> if result.success:
    ...     result.human_plane.save("contract_updated.yaml")
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Union

from aerospacemodel.tdms.planes import HumanPlane, MachinePlane, PlaneMetadata, PlaneType
from aerospacemodel.tdms.dictionary import (
    DictionaryRegistry,
    DictionaryType,
)
from aerospacemodel.tdms.formats import FormatType

logger = logging.getLogger(__name__)


class ConversionStatus(Enum):
    """Status of conversion operation."""
    SUCCESS = "success"
    PARTIAL = "partial"     # Converted with warnings
    FAILED = "failed"


@dataclass
class ConversionWarning:
    """A warning encountered during conversion."""
    field: str
    message: str
    original_value: Any = None
    converted_value: Any = None


@dataclass
class ConversionResult:
    """
    Result of a conversion operation.
    
    Attributes:
        status: Conversion status
        human_plane: Resulting HumanPlane (if converting to human)
        machine_plane: Resulting MachinePlane (if converting to machine)
        warnings: List of conversion warnings
        errors: List of error messages
        source_hash: Hash of source content
        target_hash: Hash of converted content
    """
    status: ConversionStatus
    human_plane: Optional[HumanPlane] = None
    machine_plane: Optional[MachinePlane] = None
    warnings: List[ConversionWarning] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    source_hash: str = ""
    target_hash: str = ""
    conversion_time: Optional[datetime] = None
    
    @property
    def success(self) -> bool:
        """Check if conversion was successful."""
        return self.status in (ConversionStatus.SUCCESS, ConversionStatus.PARTIAL)
    
    def add_warning(
        self,
        field: str,
        message: str,
        original_value: Any = None,
        converted_value: Any = None,
    ) -> None:
        """Add a conversion warning."""
        self.warnings.append(ConversionWarning(
            field=field,
            message=message,
            original_value=original_value,
            converted_value=converted_value,
        ))
    
    def add_error(self, message: str) -> None:
        """Add a conversion error."""
        self.errors.append(message)
        self.status = ConversionStatus.FAILED


@dataclass
class ConversionConfig:
    """
    Configuration for conversion operations.
    
    Attributes:
        compact_ids: Use dictionary IDs instead of full values
        flatten_arrays: Flatten arrays to indexed keys
        max_array_items: Maximum array items to include
        include_metadata: Include TDMS metadata in output
        preserve_order: Preserve key order in conversion
        strict_validation: Fail on validation errors
    """
    compact_ids: bool = True
    flatten_arrays: bool = True
    max_array_items: int = 100
    include_metadata: bool = True
    preserve_order: bool = True
    strict_validation: bool = True
    excluded_fields: Set[str] = field(default_factory=lambda: {"_metadata", "_schema"})
    
    # Field mappings for compaction
    id_fields: Dict[str, DictionaryType] = field(default_factory=lambda: {
        "status": DictionaryType.STATUS,
        "category": DictionaryType.PUBLICATION,
        "publication": DictionaryType.PUBLICATION,
        "baseline_type": DictionaryType.BASELINE,
        "owner": DictionaryType.STAKEHOLDER,
        "approver": DictionaryType.STAKEHOLDER,
    })


class TDMSConverter:
    """
    Bidirectional converter between Human and Machine planes.
    
    Handles:
        - Flattening nested structures for machine plane
        - Compacting values to IDs using dictionaries
        - Expanding IDs back to values
        - Validating conversions
        - Tracking provenance
    
    Example:
        >>> converter = TDMSConverter()
        >>> 
        >>> # Human to Machine (flatten and compact)
        >>> human = HumanPlane(data={"header": {"title": "Test", "status": "DRAFT"}})
        >>> machine = converter.to_machine_plane(human)
        >>> print(machine.to_tsv())
        header.title\\theader.status
        Test\\tDFT
        
        >>> # Machine to Human (expand and validate)
        >>> result = converter.to_human_plane(machine, validate=True)
        >>> print(result.human_plane.data)
        {'header': {'title': 'Test', 'status': 'Draft'}}
    """
    
    def __init__(
        self,
        config: Optional[ConversionConfig] = None,
        dictionary_registry: Optional[DictionaryRegistry] = None,
    ) -> None:
        """
        Initialize converter.
        
        Args:
            config: Conversion configuration
            dictionary_registry: Dictionary registry for ID disambiguation
        """
        self.config = config or ConversionConfig()
        self.dictionary_registry = dictionary_registry or DictionaryRegistry.create_with_defaults()
    
    def to_machine_plane(
        self,
        human: HumanPlane,
        record_type: Optional[str] = None,
    ) -> MachinePlane:
        """
        Convert HumanPlane to MachinePlane.
        
        Flattens nested structure and compacts values using dictionaries.
        
        Args:
            human: Source HumanPlane
            record_type: Optional record type identifier
            
        Returns:
            Converted MachinePlane
        """
        # Flatten the nested structure
        flat = self._flatten_dict(human.data)
        
        # Compact values using dictionaries
        if self.config.compact_ids:
            flat = self._compact_values(flat)
        
        # Add record type if specified
        if record_type:
            flat["_type"] = record_type
        
        # Create machine plane record
        records = [flat]
        columns = list(flat.keys())
        
        machine = MachinePlane(
            records=records,
            columns=columns,
            dictionary_registry=self.dictionary_registry,
        )
        
        # Track provenance: keep MachinePlane's own source_hash as its content hash
        # and store the human hash in derived_from
        machine.metadata.derived_from = human.metadata.source_hash
        
        logger.info(f"Converted HumanPlane to MachinePlane: {len(flat)} fields")
        return machine
    
    def to_human_plane(
        self,
        machine: MachinePlane,
        validate: bool = True,
        record_index: int = 0,
    ) -> ConversionResult:
        """
        Convert MachinePlane to HumanPlane.
        
        Expands IDs and reconstructs nested structure.
        
        Args:
            machine: Source MachinePlane
            validate: Whether to validate the result
            record_index: Which record to convert (for multi-record planes)
            
        Returns:
            ConversionResult with HumanPlane or errors
        """
        result = ConversionResult(
            status=ConversionStatus.SUCCESS,
            conversion_time=datetime.now(),
            source_hash=machine.metadata.source_hash,
        )
        
        try:
            if not machine.records:
                result.add_error("No records in MachinePlane")
                return result
            
            if record_index >= len(machine.records):
                result.add_error(f"Record index {record_index} out of range")
                return result
            
            # Get flat record
            flat = machine.records[record_index].copy()
            
            # Remove internal fields
            for field in ["_type", "_ts"]:
                flat.pop(field, None)
            
            # Expand compact IDs
            if self.config.compact_ids:
                flat = self._expand_values(flat, result)
            
            # Reconstruct nested structure
            nested = self._unflatten_dict(flat)
            
            # Create human plane
            human = HumanPlane(data=nested)
            human.metadata.derived_from = machine.metadata.source_hash
            
            # Validate if requested
            if validate:
                errors = human.validate()
                if errors:
                    if self.config.strict_validation:
                        for error in errors:
                            result.add_error(f"Validation failed: {error}")
                        result.status = ConversionStatus.FAILED
                    else:
                        for error in errors:
                            result.add_warning("validation", error)
            
            result.human_plane = human
            result.target_hash = human.metadata.source_hash
            
            if result.warnings and result.status == ConversionStatus.SUCCESS:
                result.status = ConversionStatus.PARTIAL
            
            logger.info(f"Converted MachinePlane to HumanPlane: {len(nested)} top-level keys")
            
        except Exception as e:
            result.add_error(f"Conversion failed: {str(e)}")
            logger.error(f"Conversion error: {e}")
        
        return result
    
    def convert_multiple(
        self,
        humans: List[HumanPlane],
        format_type: FormatType = FormatType.TSV,
    ) -> MachinePlane:
        """
        Convert multiple HumanPlanes to a single MachinePlane.
        
        Useful for batch processing of related documents.
        
        Args:
            humans: List of HumanPlane instances
            format_type: Target format type
            
        Returns:
            MachinePlane with multiple records
        """
        all_records = []
        all_columns: Set[str] = set()
        
        for i, human in enumerate(humans):
            flat = self._flatten_dict(human.data)
            if self.config.compact_ids:
                flat = self._compact_values(flat)
            flat["_idx"] = i
            all_records.append(flat)
            all_columns.update(flat.keys())
        
        # Ensure consistent column order
        columns = sorted(all_columns)
        
        machine = MachinePlane(
            records=all_records,
            columns=columns,
            dictionary_registry=self.dictionary_registry,
        )
        
        logger.info(f"Converted {len(humans)} HumanPlanes to MachinePlane")
        return machine
    
    def _flatten_dict(
        self,
        data: Dict[str, Any],
        prefix: str = "",
        result: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Flatten nested dictionary to dot-notation keys.
        
        Args:
            data: Nested dictionary
            prefix: Current key prefix
            result: Accumulator dictionary
            
        Returns:
            Flattened dictionary
        """
        if result is None:
            result = {}
        
        for key, value in data.items():
            # Skip excluded fields
            if key in self.config.excluded_fields:
                continue
            
            new_key = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                self._flatten_dict(value, new_key, result)
            elif isinstance(value, list):
                if self.config.flatten_arrays:
                    for i, item in enumerate(value[:self.config.max_array_items]):
                        if isinstance(item, dict):
                            self._flatten_dict(item, f"{new_key}[{i}]", result)
                        else:
                            result[f"{new_key}[{i}]"] = item
                else:
                    # Store as JSON string
                    result[new_key] = json.dumps(value, separators=(",", ":"))
            else:
                result[new_key] = value
        
        return result
    
    def _unflatten_dict(self, flat: Dict[str, Any]) -> Dict[str, Any]:
        """
        Reconstruct nested dictionary from dot-notation keys.
        
        Args:
            flat: Flattened dictionary
            
        Returns:
            Nested dictionary
        """
        result: Dict[str, Any] = {}
        
        for key, value in flat.items():
            parts = self._parse_key(key)
            current = result
            
            for i, part in enumerate(parts[:-1]):
                if isinstance(part, int):
                    # Array index
                    while len(current) <= part:
                        current.append({})
                    current = current[part]
                else:
                    # Dictionary key
                    next_part = parts[i + 1]
                    if part not in current:
                        current[part] = [] if isinstance(next_part, int) else {}
                    current = current[part]
            
            # Set final value
            last_part = parts[-1]
            if isinstance(last_part, int):
                while len(current) <= last_part:
                    current.append(None)
                current[last_part] = value
            else:
                current[last_part] = value
        
        return result
    
    def _parse_key(self, key: str) -> List[Union[str, int]]:
        """
        Parse dot-notation key to parts.
        
        Args:
            key: Key like "header.items[0].name"
            
        Returns:
            List of parts (strings and ints)
        """
        parts: List[Union[str, int]] = []
        
        # Split by dots, handling array indices
        for segment in key.split("."):
            # Check for array index
            match = re.match(r"^(.+?)\[(\d+)\]$", segment)
            if match:
                parts.append(match.group(1))
                parts.append(int(match.group(2)))
            else:
                parts.append(segment)
        
        return parts
    
    def _compact_values(self, flat: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compact values using dictionary IDs.
        
        Args:
            flat: Flattened dictionary with full values
            
        Returns:
            Dictionary with compacted IDs
        """
        result = {}
        
        for key, value in flat.items():
            # Check if this field should be compacted
            field_name = key.split(".")[-1].split("[")[0]
            
            if field_name in self.config.id_fields and value:
                dict_type = self.config.id_fields[field_name]
                try:
                    dictionary = self.dictionary_registry.get(dict_type)
                    if dictionary and dictionary.has_value(str(value)):
                        value = dictionary.get_id(str(value))
                except Exception:
                    pass  # Keep original value
            
            result[key] = value
        
        return result
    
    def _expand_values(
        self,
        flat: Dict[str, Any],
        result: ConversionResult,
    ) -> Dict[str, Any]:
        """
        Expand compact IDs to full values.
        
        Args:
            flat: Flattened dictionary with compact IDs
            result: ConversionResult to track warnings
            
        Returns:
            Dictionary with expanded values
        """
        expanded = {}
        
        for key, value in flat.items():
            field_name = key.split(".")[-1].split("[")[0]
            
            if field_name in self.config.id_fields and value:
                dict_type = self.config.id_fields[field_name]
                try:
                    dictionary = self.dictionary_registry.get(dict_type)
                    if dictionary and dictionary.has_id(str(value)):
                        expanded[key] = dictionary.get_value(str(value))
                    else:
                        expanded[key] = value
                        result.add_warning(
                            field=key,
                            message=f"Could not expand ID '{value}'",
                            original_value=value,
                        )
                except Exception as e:
                    expanded[key] = value
                    result.add_warning(
                        field=key,
                        message=f"Expansion error: {str(e)}",
                        original_value=value,
                    )
            else:
                expanded[key] = value
        
        return expanded
    
    def validate_round_trip(self, human: HumanPlane) -> ConversionResult:
        """
        Validate lossless round-trip conversion.
        
        Converts human → machine → human and compares.
        
        Args:
            human: Original HumanPlane
            
        Returns:
            ConversionResult with validation status
        """
        result = ConversionResult(
            status=ConversionStatus.SUCCESS,
            conversion_time=datetime.now(),
            source_hash=human.metadata.source_hash,
        )
        
        try:
            # Convert to machine
            machine = self.to_machine_plane(human)
            
            # Convert back to human
            back_result = self.to_human_plane(machine, validate=False)
            
            if not back_result.success:
                result.errors = back_result.errors
                result.status = ConversionStatus.FAILED
                return result
            
            # Compare hashes
            original_flat = self._flatten_dict(human.data)
            converted_flat = self._flatten_dict(back_result.human_plane.data)
            
            # Check for differences
            all_keys = set(original_flat.keys()) | set(converted_flat.keys())
            for key in all_keys:
                orig = original_flat.get(key)
                conv = converted_flat.get(key)
                if orig != conv:
                    result.add_warning(
                        field=key,
                        message="Value changed in round-trip",
                        original_value=orig,
                        converted_value=conv,
                    )
            
            if result.warnings:
                result.status = ConversionStatus.PARTIAL
            
            result.human_plane = back_result.human_plane
            result.target_hash = back_result.human_plane.metadata.source_hash
            
        except Exception as e:
            result.add_error(f"Round-trip validation failed: {str(e)}")
        
        return result


__all__ = [
    "ConversionStatus",
    "ConversionWarning",
    "ConversionResult",
    "ConversionConfig",
    "TDMSConverter",
]
