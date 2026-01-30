"""
TDMS Format Handlers
====================

Token-efficient format handlers for the machine plane:
    - TSV: Tab-separated values (recommended for most use cases)
    - CSV: Comma-separated values
    - LineProtocol: Compact line-based protocol (TSON/TOON-style)

Design Principles:
    - Minimize token count for LLM context efficiency
    - Preserve semantic clarity through ID references
    - Deterministic serialization for reproducibility
    - Human-readable headers for debugging

Example TSV output:
    id\\ttype\\tata\\tstatus\\ttitle
    CTR001\\tLM\\t28\\tAPV\\tFuel System CSDB Generation
    CTR002\\tOPS\\t32\\tDFT\\tLanding Gear SB Generation
"""

from __future__ import annotations

import csv
import io
import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from aerospacemodel.tdms.exceptions import FormatError

logger = logging.getLogger(__name__)


class FormatType(Enum):
    """Supported machine plane format types."""
    TSV = "tsv"             # Tab-separated values
    CSV = "csv"             # Comma-separated values
    LINE_PROTOCOL = "lp"    # Line protocol format


@dataclass
class FormatOptions:
    """Options for format serialization."""
    include_header: bool = True
    include_metadata: bool = False
    quote_strings: bool = False
    null_value: str = "∅"
    preserve_leading_zeros: bool = True
    date_format: str = "%Y-%m-%d"
    datetime_format: str = "%Y-%m-%dT%H:%M:%S"
    encoding: str = "utf-8"
    line_ending: str = "\n"


class BaseFormat(ABC):
    """
    Abstract base class for machine plane formats.
    
    All format handlers must implement:
        - serialize: Convert records to string
        - deserialize: Parse string to records
    """
    
    format_type: FormatType
    
    def __init__(self, options: Optional[FormatOptions] = None) -> None:
        """Initialize format handler with options."""
        self.options = options or FormatOptions()
    
    @abstractmethod
    def serialize(
        self,
        records: List[Dict[str, Any]],
        columns: Optional[List[str]] = None,
    ) -> str:
        """
        Serialize records to format string.
        
        Args:
            records: List of record dictionaries
            columns: Optional column order (inferred if not provided)
            
        Returns:
            Serialized string representation
        """
        pass
    
    @abstractmethod
    def deserialize(
        self,
        content: str,
        columns: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Deserialize format string to records.
        
        Args:
            content: Format string
            columns: Optional column names (parsed from header if not provided)
            
        Returns:
            List of record dictionaries
        """
        pass
    
    def write(
        self,
        records: List[Dict[str, Any]],
        path: Union[str, Path],
        columns: Optional[List[str]] = None,
    ) -> None:
        """Write records to file."""
        path = Path(path)
        content = self.serialize(records, columns)
        with open(path, "w", encoding=self.options.encoding) as f:
            f.write(content)
        logger.info(f"Wrote {len(records)} records to {path}")
    
    def read(
        self,
        path: Union[str, Path],
        columns: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Read records from file."""
        path = Path(path)
        with open(path, "r", encoding=self.options.encoding) as f:
            content = f.read()
        return self.deserialize(content, columns)
    
    def _format_value(self, value: Any) -> str:
        """Format a value for serialization."""
        if value is None:
            return self.options.null_value
        elif isinstance(value, bool):
            return "1" if value else "0"
        elif isinstance(value, datetime):
            return value.strftime(self.options.datetime_format)
        elif isinstance(value, (list, dict)):
            return json.dumps(value, separators=(",", ":"))
        else:
            return str(value)
    
    def _parse_value(self, value: str) -> Any:
        """Parse a serialized value."""
        if value == self.options.null_value:
            return None
        # Try to parse as JSON for complex types
        if value.startswith("[") or value.startswith("{"):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass
        # Try numeric conversion only if preserve_leading_zeros is False
        # or the value doesn't have leading zeros
        if not self.options.preserve_leading_zeros or not (value.startswith("0") and len(value) > 1 and value[1:].isdigit()):
            try:
                if "." in value:
                    return float(value)
                return int(value)
            except ValueError:
                pass
        return value


class TSVFormat(BaseFormat):
    """
    Tab-Separated Values format handler.
    
    TSV is the recommended format for machine plane due to:
        - Excellent token efficiency (tabs are single tokens)
        - Simple parsing without quoting edge cases
        - Human-readable in editors and terminals
    
    Example:
        >>> tsv = TSVFormat()
        >>> records = [{"id": "CTR001", "type": "LM", "status": "APV"}]
        >>> print(tsv.serialize(records))
        id\\ttype\\tstatus
        CTR001\\tLM\\tAPV
    """
    
    format_type = FormatType.TSV
    
    def __init__(self, options: Optional[FormatOptions] = None) -> None:
        super().__init__(options)
        self.delimiter = "\t"
    
    def serialize(
        self,
        records: List[Dict[str, Any]],
        columns: Optional[List[str]] = None,
    ) -> str:
        """Serialize records to TSV string."""
        if not records:
            return ""
        
        # Determine columns
        if columns is None:
            # Use keys from first record
            columns = list(records[0].keys())
        
        lines = []
        
        # Header
        if self.options.include_header:
            lines.append(self.delimiter.join(columns))
        
        # Data rows
        for record in records:
            row = []
            for col in columns:
                value = record.get(col)
                row.append(self._format_value(value))
            lines.append(self.delimiter.join(row))
        
        return self.options.line_ending.join(lines)
    
    def deserialize(
        self,
        content: str,
        columns: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Deserialize TSV string to records."""
        if not content.strip():
            return []
        
        lines = content.strip().split(self.options.line_ending)
        records = []
        
        # Parse header or use provided columns
        if self.options.include_header and columns is None:
            header = lines[0].split(self.delimiter)
            data_lines = lines[1:]
        else:
            header = columns or []
            data_lines = lines
        
        if not header:
            raise FormatError("No column names available for TSV parsing")
        
        # Parse data rows
        for line in data_lines:
            if not line.strip():
                continue
            values = line.split(self.delimiter)
            record = {}
            for i, col in enumerate(header):
                if i < len(values):
                    record[col] = self._parse_value(values[i])
                else:
                    record[col] = None
            records.append(record)
        
        return records


class CSVFormat(BaseFormat):
    """
    Comma-Separated Values format handler.
    
    Uses Python's csv module for proper quoting and escaping.
    Slightly less token-efficient than TSV but more compatible.
    
    Example:
        >>> csv_fmt = CSVFormat()
        >>> records = [{"id": "CTR001", "title": "Fuel System, Generation"}]
        >>> print(csv_fmt.serialize(records))
        id,title
        CTR001,"Fuel System, Generation"
    """
    
    format_type = FormatType.CSV
    
    def __init__(self, options: Optional[FormatOptions] = None) -> None:
        super().__init__(options)
        self.delimiter = ","
    
    def serialize(
        self,
        records: List[Dict[str, Any]],
        columns: Optional[List[str]] = None,
    ) -> str:
        """Serialize records to CSV string."""
        if not records:
            return ""
        
        # Determine columns
        if columns is None:
            columns = list(records[0].keys())
        
        output = io.StringIO()
        writer = csv.writer(
            output,
            delimiter=self.delimiter,
            quoting=csv.QUOTE_MINIMAL if not self.options.quote_strings else csv.QUOTE_ALL,
        )
        
        # Header
        if self.options.include_header:
            writer.writerow(columns)
        
        # Data rows
        for record in records:
            row = [self._format_value(record.get(col)) for col in columns]
            writer.writerow(row)
        
        return output.getvalue().strip()
    
    def deserialize(
        self,
        content: str,
        columns: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Deserialize CSV string to records."""
        if not content.strip():
            return []
        
        reader = csv.reader(
            io.StringIO(content),
            delimiter=self.delimiter,
        )
        
        rows = list(reader)
        if not rows:
            return []
        
        # Parse header or use provided columns
        if self.options.include_header and columns is None:
            header = rows[0]
            data_rows = rows[1:]
        else:
            header = columns or []
            data_rows = rows
        
        if not header:
            raise FormatError("No column names available for CSV parsing")
        
        # Parse data rows
        records = []
        for row in data_rows:
            record = {}
            for i, col in enumerate(header):
                if i < len(row):
                    record[col] = self._parse_value(row[i])
                else:
                    record[col] = None
            records.append(record)
        
        return records


class LineProtocolFormat(BaseFormat):
    """
    Line Protocol format handler.
    
    A compact line-based format inspired by InfluxDB line protocol
    and TSON/TOON concepts. Optimized for sequential processing
    by AI agents.
    
    Format:
        <type>/<id> <key1>=<val1>,<key2>=<val2> <timestamp>
    
    Example:
        >>> lp = LineProtocolFormat()
        >>> records = [{"_type": "contract", "id": "CTR001", "status": "APV"}]
        >>> print(lp.serialize(records))
        contract/CTR001 status=APV
    """
    
    format_type = FormatType.LINE_PROTOCOL
    
    def __init__(self, options: Optional[FormatOptions] = None) -> None:
        super().__init__(options)
        self.type_field = "_type"
        self.id_field = "id"
        self.timestamp_field = "_ts"
    
    def serialize(
        self,
        records: List[Dict[str, Any]],
        columns: Optional[List[str]] = None,
    ) -> str:
        """Serialize records to line protocol format."""
        lines = []
        
        for record in records:
            record_type = record.get(self.type_field, "record")
            record_id = record.get(self.id_field, "")
            timestamp = record.get(self.timestamp_field)
            
            # Build key=value pairs
            pairs = []
            for key, value in record.items():
                if key in (self.type_field, self.id_field, self.timestamp_field):
                    continue
                if value is not None:
                    # Handle strings specially to ensure safe line protocol encoding
                    if isinstance(value, str):
                        # Escape backslashes and double quotes
                        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
                        formatted = escaped
                        # Quote strings containing spaces, commas, quotes, or backslashes
                        if any(ch in value for ch in (" ", ",", '"', "\\")):
                            formatted = f'"{escaped}"'
                    else:
                        formatted = self._format_value(value)
                    pairs.append(f"{key}={formatted}")
            
            # Build line
            line = f"{record_type}/{record_id}"
            if pairs:
                line += " " + ",".join(pairs)
            if timestamp:
                line += f" {self._format_value(timestamp)}"
            
            lines.append(line)
        
        return self.options.line_ending.join(lines)
    
    def deserialize(
        self,
        content: str,
        columns: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Deserialize line protocol format to records."""
        if not content.strip():
            return []
        
        records = []
        
        for line in content.strip().split(self.options.line_ending):
            line = line.strip()
            if not line:
                continue
            
            record = {}
            
            # Parse type/id prefix
            parts = line.split(" ", 2)
            type_id = parts[0]
            
            if "/" in type_id:
                record_type, record_id = type_id.split("/", 1)
                record[self.type_field] = record_type
                record[self.id_field] = record_id
            else:
                record[self.id_field] = type_id
            
            # Parse key=value pairs
            if len(parts) > 1:
                pairs_str = parts[1]
                # Handle quoted values
                pairs = self._parse_pairs(pairs_str)
                record.update(pairs)
            
            # Parse timestamp
            if len(parts) > 2:
                record[self.timestamp_field] = self._parse_value(parts[2])
            
            records.append(record)
        
        return records
    
    def _parse_pairs(self, pairs_str: str) -> Dict[str, Any]:
        """Parse key=value pairs handling quoted strings and escaped characters."""
        pairs: Dict[str, Any] = {}
        current = []
        in_quotes = False
        escape_next = False

        # Append a sentinel comma to flush the last pair
        for char in pairs_str + ",":
            if escape_next:
                # Current character is escaped; add as-is
                current.append(char)
                escape_next = False
                continue

            if char == "\\":
                # Next character (including quote or comma) should be treated literally
                escape_next = True
                continue

            if char == '"':
                # Toggle quote state only for unescaped quotes
                in_quotes = not in_quotes
                current.append(char)
            elif char == "," and not in_quotes:
                segment = "".join(current).strip()
                if segment and "=" in segment:
                    key, value = segment.split("=", 1)
                    key = key.strip()
                    value_str = value.strip()

                    # If value is a quoted string, use JSON decoding to handle escapes
                    if len(value_str) >= 2 and value_str[0] == '"' and value_str[-1] == '"':
                        try:
                            decoded_value = json.loads(value_str)
                        except json.JSONDecodeError:
                            # Fallback: strip outer quotes only
                            decoded_value = value_str[1:-1]
                        pairs[key] = self._parse_value(decoded_value) if not isinstance(decoded_value, str) else decoded_value
                    else:
                        pairs[key] = self._parse_value(value_str)
                current = []
            else:
                current.append(char)
        
        return pairs


def get_format_handler(format_type: FormatType, options: Optional[FormatOptions] = None) -> BaseFormat:
    """
    Get appropriate format handler for type.
    
    Args:
        format_type: The format type
        options: Optional format options
        
    Returns:
        Format handler instance
    """
    handlers = {
        FormatType.TSV: TSVFormat,
        FormatType.CSV: CSVFormat,
        FormatType.LINE_PROTOCOL: LineProtocolFormat,
    }
    
    handler_class = handlers.get(format_type)
    if handler_class is None:
        raise FormatError(f"Unsupported format type: {format_type}")
    
    return handler_class(options)


__all__ = [
    "FormatType",
    "FormatOptions",
    "BaseFormat",
    "TSVFormat",
    "CSVFormat",
    "LineProtocolFormat",
    "get_format_handler",
]
