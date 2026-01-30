"""
Total Document Management System (TDMS)
=======================================

A hybrid human + machine document management system with dual-plane representation:

1. Human Plane (authoritative/editable):
   - Readable, reviewable, auditable formats
   - YAML/JSON (and XML S1000D where appropriate)
   - Source of truth for all document content

2. Machine Plane (runtime/token-efficient):
   - Compact, deterministic, context-efficient formats
   - CSV/TSV tabular formats with line protocols
   - IDs + dictionaries for disambiguation
   - Derived view for AI loops and agents

Architecture:
    The human plane is the source of truth; the machine plane is a derived view.
    They do not compete - they serve different purposes in the document lifecycle.

    Human Plane ←──[source of truth]
         │
         ▼
    Converter (bidirectional with validation)
         │
         ▼  
    Machine Plane ←──[derived view for agents]

Usage:
    >>> from aerospacemodel.tdms import HumanPlane, MachinePlane, TDMSConverter
    >>> 
    >>> # Load from human-readable YAML
    >>> human = HumanPlane.load("contracts/my_contract.yaml")
    >>> 
    >>> # Convert to token-efficient format for AI agents
    >>> converter = TDMSConverter()
    >>> machine = converter.to_machine_plane(human)
    >>> 
    >>> # Export compact representation
    >>> machine.to_tsv("contract_compact.tsv")
    >>> 
    >>> # After AI processing, convert back (with validation)
    >>> modified = MachinePlane.from_tsv("agent_output.tsv")
    >>> result = converter.to_human_plane(modified, validate=True)
    >>> if result.success:
    ...     result.human_plane.save("contract_updated.yaml")

Copyright:
    2024-2026 AEROSPACEMODEL Contributors

License:
    Apache License 2.0
"""

from aerospacemodel.tdms.planes import (
    HumanPlane,
    MachinePlane,
    PlaneType,
)

from aerospacemodel.tdms.converter import (
    TDMSConverter,
    ConversionResult,
    ConversionStatus,
)

from aerospacemodel.tdms.dictionary import (
    TDMSDictionary,
    DictionaryEntry,
    DictionaryType,
    DictionaryRegistry,
)

from aerospacemodel.tdms.formats import (
    TSVFormat,
    CSVFormat,
    LineProtocolFormat,
    FormatType,
)

from aerospacemodel.tdms.exceptions import (
    TDMSError,
    ConversionError,
    ValidationError,
    DictionaryError,
)

__all__ = [
    # Planes
    "HumanPlane",
    "MachinePlane",
    "PlaneType",
    
    # Converter
    "TDMSConverter",
    "ConversionResult",
    "ConversionStatus",
    
    # Dictionary
    "TDMSDictionary",
    "DictionaryEntry",
    "DictionaryType",
    "DictionaryRegistry",
    
    # Formats
    "TSVFormat",
    "CSVFormat",
    "LineProtocolFormat",
    "FormatType",
    
    # Exceptions
    "TDMSError",
    "ConversionError",
    "ValidationError",
    "DictionaryError",
]
