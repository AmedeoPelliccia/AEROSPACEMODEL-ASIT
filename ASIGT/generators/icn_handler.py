# =============================================================================
# ASIGT ICN Handler
# Information Control Number and graphics management
# Version: 2.0.0
# =============================================================================
"""
ICN Handler

Manages Information Control Numbers (ICN) for graphics and multimedia
content in S1000D publications. Handles graphics registration, format
conversion, and reference management.

Supported Formats:
    - CGM (Computer Graphics Metafile) - S1000D standard
    - PNG (Portable Network Graphics)
    - SVG (Scalable Vector Graphics)
    - JPEG (Joint Photographic Experts Group)
    - TIFF (Tagged Image File Format)
    - PDF (Embedded graphics)
"""

from __future__ import annotations

import hashlib
import logging
import mimetypes
import shutil
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class GraphicFormat(Enum):
    """Supported graphic formats."""
    CGM = "cgm"     # S1000D standard vector format
    PNG = "png"     # Raster format
    SVG = "svg"     # Scalable vector graphics
    JPEG = "jpeg"   # Photographic images
    JPG = "jpg"     # Alias for JPEG
    TIFF = "tiff"   # High-quality images
    TIF = "tif"     # Alias for TIFF
    PDF = "pdf"     # Embedded PDFs
    GIF = "gif"     # Legacy support


class ICNType(Enum):
    """Types of ICN content."""
    FIGURE = "figure"               # Technical illustration
    SHEET = "sheet"                 # Multi-sheet figure
    HOTSPOT = "hotspot"             # Interactive hotspot graphic
    MULTIMEDIA = "multimedia"       # Video/animation
    SYMBOL = "symbol"               # Standard symbol
    LEGEND = "legend"               # Legend/key graphic


@dataclass
class ICNCode:
    """
    S1000D Information Control Number (ICN) structure.
    
    Format: ICN-CAGE-MODEL-SYSTEM-GRAPHIC-VARIANT-ISSUE
    Example: ICN-00000-HJ1-28-G0001-A-001-01
    """
    cage_code: str = "00000"        # CAGE code (5 chars)
    model_ident_code: str = "XXX"   # Model identification
    system_code: str = "00"         # ATA system code
    graphic_number: str = "G0001"   # Graphic number
    variant_code: str = "A"         # Variant
    issue_number: str = "001"       # Issue number
    security_classification: str = "01"  # Security class
    
    def __str__(self) -> str:
        """Generate ICN string representation."""
        return f"ICN-{self.cage_code}-{self.model_ident_code}-{self.system_code}-{self.graphic_number}-{self.variant_code}-{self.issue_number}-{self.security_classification}"
    
    @classmethod
    def from_string(cls, icn_string: str) -> "ICNCode":
        """Parse ICN from string representation."""
        if icn_string.startswith("ICN-"):
            icn_string = icn_string[4:]
        
        parts = icn_string.split("-")
        if len(parts) < 7:
            raise ValueError(f"Invalid ICN format: {icn_string}")
        
        return cls(
            cage_code=parts[0],
            model_ident_code=parts[1],
            system_code=parts[2],
            graphic_number=parts[3],
            variant_code=parts[4],
            issue_number=parts[5],
            security_classification=parts[6] if len(parts) > 6 else "01",
        )
    
    def get_filename(self, extension: str = "cgm") -> str:
        """Get standardized filename for this ICN."""
        return f"{self}.{extension.lower()}"


@dataclass
class ICNEntry:
    """Registered ICN entry in the graphics database."""
    icn: ICNCode
    source_path: Path
    format: GraphicFormat
    icn_type: ICNType = ICNType.FIGURE
    title: str = ""
    description: str = ""
    width_mm: Optional[float] = None
    height_mm: Optional[float] = None
    dpi: Optional[int] = None
    file_hash: str = ""
    file_size_bytes: int = 0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    modified_at: str = field(default_factory=lambda: datetime.now().isoformat())
    referenced_by: List[str] = field(default_factory=list)  # DM codes that reference this ICN
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "icn": str(self.icn),
            "source_path": str(self.source_path),
            "format": self.format.value,
            "icn_type": self.icn_type.value,
            "title": self.title,
            "description": self.description,
            "width_mm": self.width_mm,
            "height_mm": self.height_mm,
            "dpi": self.dpi,
            "file_hash": self.file_hash,
            "file_size_bytes": self.file_size_bytes,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "referenced_by": self.referenced_by,
        }


@dataclass
class ICNRegistrationResult:
    """Result of ICN registration operation."""
    success: bool
    icn: str
    source_path: str
    registered_path: Optional[str] = None
    format: Optional[str] = None
    file_hash: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class ICNHandler:
    """
    S1000D Information Control Number Handler.
    
    Manages graphics and multimedia content for S1000D publications.
    Handles ICN generation, registration, and reference tracking.
    
    Attributes:
        contract: ASIT transformation contract
        config: Handler configuration
        graphics_path: Path to graphics storage
        
    Example:
        >>> handler = ICNHandler(contract=contract, config=config)
        >>> result = handler.register_graphic(
        ...     source_path=Path("diagrams/fuel_system.png"),
        ...     ata_chapter="28",
        ...     title="Fuel System Schematic",
        ... )
    """
    
    # Format to MIME type mapping
    FORMAT_MIME_TYPES = {
        GraphicFormat.CGM: "image/cgm",
        GraphicFormat.PNG: "image/png",
        GraphicFormat.SVG: "image/svg+xml",
        GraphicFormat.JPEG: "image/jpeg",
        GraphicFormat.JPG: "image/jpeg",
        GraphicFormat.TIFF: "image/tiff",
        GraphicFormat.TIF: "image/tiff",
        GraphicFormat.PDF: "application/pdf",
        GraphicFormat.GIF: "image/gif",
    }
    
    # Recommended formats for S1000D
    RECOMMENDED_FORMATS = [GraphicFormat.CGM, GraphicFormat.PNG, GraphicFormat.SVG]
    
    def __init__(
        self,
        contract: Dict[str, Any],
        config: Dict[str, Any],
        graphics_path: Optional[Path] = None,
    ):
        """
        Initialize ICN Handler.
        
        Args:
            contract: ASIT transformation contract (required)
            config: Handler configuration
            graphics_path: Path to graphics storage
            
        Raises:
            ValueError: If contract is missing or invalid
        """
        if not contract:
            raise ValueError("ASIT contract is required for ICN handling")
        
        self.contract = contract
        self.config = config
        self.graphics_path = graphics_path or Path("IDB/CSDB/GRAPHICS")
        
        # Extract contract parameters
        self.contract_id = contract.get("id", "UNKNOWN")
        self.model_code = config.get("model_ident_code", "XXX")
        self.cage_code = config.get("cage_code", "00000")
        
        # ICN registry
        self._icn_registry: Dict[str, ICNEntry] = {}
        self._icn_counter: Dict[str, int] = {}  # Per-system counter
        
        logger.info(
            f"ICNHandler initialized: contract={self.contract_id}, "
            f"model={self.model_code}"
        )
    
    def register_graphic(
        self,
        source_path: Path,
        ata_chapter: str,
        title: str = "",
        description: str = "",
        icn_type: ICNType = ICNType.FIGURE,
        copy_to_repository: bool = True,
    ) -> ICNRegistrationResult:
        """
        Register a graphic and generate its ICN.
        
        Args:
            source_path: Path to source graphic file
            ata_chapter: ATA chapter (system code)
            title: Graphic title
            description: Graphic description
            icn_type: Type of ICN content
            copy_to_repository: Whether to copy to graphics repository
            
        Returns:
            ICNRegistrationResult with generated ICN
        """
        source_path = Path(source_path)
        
        # Validate source file
        if not source_path.exists():
            return ICNRegistrationResult(
                success=False,
                icn="",
                source_path=str(source_path),
                errors=[f"Source file not found: {source_path}"],
            )
        
        # Determine format
        graphic_format = self._detect_format(source_path)
        if graphic_format is None:
            return ICNRegistrationResult(
                success=False,
                icn="",
                source_path=str(source_path),
                errors=[f"Unsupported graphic format: {source_path.suffix}"],
            )
        
        # Generate ICN
        system_code = str(ata_chapter).zfill(2)
        icn = self._generate_icn(system_code)
        
        # Calculate file hash
        file_hash = self._compute_file_hash(source_path)
        file_size = source_path.stat().st_size
        
        # Create registry entry
        entry = ICNEntry(
            icn=icn,
            source_path=source_path,
            format=graphic_format,
            icn_type=icn_type,
            title=title,
            description=description,
            file_hash=file_hash,
            file_size_bytes=file_size,
        )
        
        # Copy to repository if requested
        registered_path = None
        if copy_to_repository:
            registered_path = self._copy_to_repository(source_path, icn, graphic_format)
        
        # Register ICN
        self._icn_registry[str(icn)] = entry
        
        # Check for format warnings
        warnings = []
        if graphic_format not in self.RECOMMENDED_FORMATS:
            warnings.append(
                f"Format {graphic_format.value} is not recommended for S1000D. "
                f"Consider converting to CGM, PNG, or SVG."
            )
        
        return ICNRegistrationResult(
            success=True,
            icn=str(icn),
            source_path=str(source_path),
            registered_path=str(registered_path) if registered_path else None,
            format=graphic_format.value,
            file_hash=file_hash,
            warnings=warnings,
        )
    
    def register_batch(
        self,
        graphics: List[Dict[str, Any]],
    ) -> List[ICNRegistrationResult]:
        """
        Register multiple graphics in batch.
        
        Args:
            graphics: List of graphic specifications with keys:
                - source_path: Path to graphic
                - ata_chapter: ATA chapter
                - title: Optional title
                - description: Optional description
                
        Returns:
            List of ICNRegistrationResult
        """
        results = []
        
        for graphic in graphics:
            result = self.register_graphic(
                source_path=Path(graphic["source_path"]),
                ata_chapter=graphic.get("ata_chapter", "00"),
                title=graphic.get("title", ""),
                description=graphic.get("description", ""),
                icn_type=ICNType(graphic.get("icn_type", "figure")),
            )
            results.append(result)
        
        return results
    
    def get_icn(self, icn_code: str) -> Optional[ICNEntry]:
        """
        Get registered ICN entry.
        
        Args:
            icn_code: ICN code string
            
        Returns:
            ICNEntry if found, None otherwise
        """
        return self._icn_registry.get(icn_code)
    
    def list_icns(
        self,
        ata_chapter: Optional[str] = None,
        format: Optional[GraphicFormat] = None,
    ) -> List[ICNEntry]:
        """
        List registered ICNs with optional filtering.
        
        Args:
            ata_chapter: Filter by ATA chapter
            format: Filter by graphic format
            
        Returns:
            List of matching ICNEntry
        """
        entries = list(self._icn_registry.values())
        
        if ata_chapter:
            system_code = str(ata_chapter).zfill(2)
            entries = [e for e in entries if e.icn.system_code == system_code]
        
        if format:
            entries = [e for e in entries if e.format == format]
        
        return entries
    
    def add_reference(self, icn_code: str, dm_code: str) -> bool:
        """
        Add a DM reference to an ICN.
        
        Args:
            icn_code: ICN code
            dm_code: Data Module code that references this ICN
            
        Returns:
            True if successful
        """
        entry = self._icn_registry.get(icn_code)
        if entry:
            if dm_code not in entry.referenced_by:
                entry.referenced_by.append(dm_code)
            return True
        return False
    
    def generate_icn_reference(
        self,
        icn_code: str,
        reproduction_width: Optional[float] = None,
        reproduction_height: Optional[float] = None,
    ) -> str:
        """
        Generate S1000D XML reference element for an ICN.
        
        Args:
            icn_code: ICN code
            reproduction_width: Optional width in mm
            reproduction_height: Optional height in mm
            
        Returns:
            XML string for graphic reference
        """
        entry = self.get_icn(icn_code)
        if not entry:
            raise ValueError(f"ICN not found: {icn_code}")
        
        # Build XML reference
        lines = [
            f'<graphic infoEntityIdent="{icn_code}">',
        ]
        
        if reproduction_width or reproduction_height:
            lines.append('  <reproductionSize>')
            if reproduction_width:
                lines.append(f'    <reproductionWidth>{reproduction_width}</reproductionWidth>')
            if reproduction_height:
                lines.append(f'    <reproductionHeight>{reproduction_height}</reproductionHeight>')
            lines.append('  </reproductionSize>')
        
        lines.append('</graphic>')
        
        return "\n".join(lines)
    
    def generate_figure_element(
        self,
        icn_code: str,
        figure_id: str,
        title: Optional[str] = None,
    ) -> str:
        """
        Generate S1000D figure element with ICN reference.
        
        Args:
            icn_code: ICN code
            figure_id: Figure ID (e.g., "fig-001")
            title: Optional figure title
            
        Returns:
            XML string for complete figure element
        """
        entry = self.get_icn(icn_code)
        title_text = title or (entry.title if entry else "Figure")
        
        return f'''<figure id="{figure_id}">
  <title>{title_text}</title>
  <graphic infoEntityIdent="{icn_code}"/>
</figure>'''
    
    def export_registry(self) -> Dict[str, Any]:
        """
        Export the ICN registry.
        
        Returns:
            Dictionary of all registered ICNs
        """
        return {
            "contract_id": self.contract_id,
            "model_code": self.model_code,
            "exported_at": datetime.now().isoformat(),
            "icn_count": len(self._icn_registry),
            "entries": {
                icn: entry.to_dict()
                for icn, entry in self._icn_registry.items()
            },
        }
    
    def validate_references(
        self,
        dm_icn_refs: List[Tuple[str, str]],
    ) -> Dict[str, Any]:
        """
        Validate ICN references from Data Modules.
        
        Args:
            dm_icn_refs: List of (dm_code, icn_code) tuples
            
        Returns:
            Validation report
        """
        valid = []
        invalid = []
        missing = []
        
        for dm_code, icn_code in dm_icn_refs:
            if icn_code in self._icn_registry:
                valid.append((dm_code, icn_code))
                self.add_reference(icn_code, dm_code)
            else:
                invalid.append((dm_code, icn_code))
                missing.append(icn_code)
        
        return {
            "total_references": len(dm_icn_refs),
            "valid_count": len(valid),
            "invalid_count": len(invalid),
            "missing_icns": list(set(missing)),
            "valid_references": valid,
            "invalid_references": invalid,
        }
    
    def _generate_icn(self, system_code: str) -> ICNCode:
        """Generate a new ICN for the given system code."""
        # Initialize counter for system if needed
        if system_code not in self._icn_counter:
            self._icn_counter[system_code] = 0
        
        # Increment counter
        self._icn_counter[system_code] += 1
        graphic_number = f"G{self._icn_counter[system_code]:04d}"
        
        return ICNCode(
            cage_code=self.cage_code,
            model_ident_code=self.model_code,
            system_code=system_code,
            graphic_number=graphic_number,
        )
    
    def _detect_format(self, path: Path) -> Optional[GraphicFormat]:
        """Detect graphic format from file extension."""
        suffix = path.suffix.lower().lstrip(".")
        
        try:
            return GraphicFormat(suffix)
        except ValueError:
            # Try common aliases
            if suffix in ("jpg", "jpeg"):
                return GraphicFormat.JPEG
            elif suffix in ("tif", "tiff"):
                return GraphicFormat.TIFF
            return None
    
    def _copy_to_repository(
        self,
        source_path: Path,
        icn: ICNCode,
        format: GraphicFormat,
    ) -> Path:
        """Copy graphic file to repository with standardized name."""
        # Create repository directory if needed
        repo_dir = self.graphics_path / icn.system_code
        repo_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate target filename
        target_filename = icn.get_filename(format.value)
        target_path = repo_dir / target_filename
        
        # Copy file
        shutil.copy2(source_path, target_path)
        
        logger.info(f"Copied {source_path} to {target_path}")
        return target_path
    
    def _compute_file_hash(self, path: Path) -> str:
        """Compute SHA-256 hash of file."""
        sha256_hash = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get ICN registry statistics.
        
        Returns:
            Statistics dictionary
        """
        entries = list(self._icn_registry.values())
        
        # Count by format
        format_counts = {}
        for entry in entries:
            fmt = entry.format.value
            format_counts[fmt] = format_counts.get(fmt, 0) + 1
        
        # Count by type
        type_counts = {}
        for entry in entries:
            t = entry.icn_type.value
            type_counts[t] = type_counts.get(t, 0) + 1
        
        # Count by ATA chapter
        chapter_counts = {}
        for entry in entries:
            ch = entry.icn.system_code
            chapter_counts[ch] = chapter_counts.get(ch, 0) + 1
        
        # Total size
        total_size = sum(entry.file_size_bytes for entry in entries)
        
        return {
            "total_icns": len(entries),
            "by_format": format_counts,
            "by_type": type_counts,
            "by_ata_chapter": chapter_counts,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
        }
