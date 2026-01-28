"""
ASIGT Renderers Module

Output rendering engines operating EXCLUSIVELY under ASIT contract authority.

This module provides renderers for S1000D content:
    - PDF: Publication-ready PDF documents
    - HTML: Web-based and IETP-compatible HTML
    - IETP: Interactive Electronic Technical Publication packages

CRITICAL CONSTRAINT:
    ASIGT cannot operate standalone.
    All renderers require valid ASIT contracts for execution.

Rendering Flow:
    1. Receive validated S1000D content
    2. Apply styling and formatting per contract
    3. Generate output in requested format
    4. Package with metadata and provenance
"""

from __future__ import annotations

import io
import json
import logging
import shutil
import zipfile
from abc import ABC, abstractmethod
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
from xml.etree import ElementTree as ET

from .engine import (
    OutputArtifact,
    ExecutionContext,
    ASIGTError,
)


logger = logging.getLogger(__name__)


# =============================================================================
# ENUMERATIONS
# =============================================================================


class PageSize(Enum):
    """Standard page sizes for PDF output."""
    A4 = "A4"           # 210 × 297 mm (ISO standard)
    LETTER = "Letter"   # 8.5 × 11 inches (US standard)
    LEGAL = "Legal"     # 8.5 × 14 inches
    A5 = "A5"           # 148 × 210 mm
    TABLOID = "Tabloid" # 11 × 17 inches


class PDFEngine(Enum):
    """PDF generation engines."""
    WEASYPRINT = "weasyprint"   # HTML/CSS to PDF (recommended)
    REPORTLAB = "reportlab"     # Direct PDF generation
    XSLT_FOP = "xslt_fop"       # XSLT + Apache FOP
    PRINCE = "prince"           # PrinceXML (commercial)


class HTMLVersion(Enum):
    """HTML version standards."""
    HTML5 = "html5"
    XHTML = "xhtml"


class CSSFramework(Enum):
    """CSS frameworks for HTML output."""
    CUSTOM = "custom"
    BOOTSTRAP = "bootstrap"
    TAILWIND = "tailwind"
    MINIMAL = "minimal"


class IETPFormat(Enum):
    """IETP package formats."""
    DIRECTORY = "directory"     # Unpacked directory structure
    ZIP = "zip"                 # ZIP archive
    CSP = "csp"                 # Common Source Package (S1000D)


class ViewerType(Enum):
    """IETP viewer types."""
    WEB = "web"                 # Web browser-based
    DESKTOP = "desktop"         # Standalone desktop application
    MOBILE = "mobile"           # Mobile application
    EMBEDDED = "embedded"       # Embedded system viewer


# =============================================================================
# DATA CLASSES - CONFIGURATION
# =============================================================================


@dataclass
class PDFRenderOptions:
    """PDF rendering configuration options."""
    page_size: PageSize = PageSize.A4
    engine: PDFEngine = PDFEngine.WEASYPRINT
    
    # Page layout
    margin_top_mm: float = 25.0
    margin_bottom_mm: float = 25.0
    margin_left_mm: float = 20.0
    margin_right_mm: float = 20.0
    
    # Content options
    include_toc: bool = True              # Table of contents
    include_lep: bool = True              # List of effective pages
    include_bookmarks: bool = True        # PDF bookmarks/outline
    include_page_numbers: bool = True
    include_revision_marks: bool = False
    
    # Header/Footer
    header_text: Optional[str] = None
    footer_text: Optional[str] = None
    watermark: Optional[str] = None       # Watermark text (e.g., "DRAFT")
    
    # Typography
    font_family: str = "Arial"
    font_size: int = 10                   # Base font size in points
    title_font_size: int = 18
    heading_font_size: int = 14
    
    # Graphics
    graphics_dpi: int = 150               # Graphics resolution
    embed_fonts: bool = True
    compress_images: bool = True
    
    # Accessibility
    pdf_a_compliance: bool = False        # PDF/A for archival
    tagged_pdf: bool = True               # Tagged PDF for accessibility


@dataclass
class HTMLRenderOptions:
    """HTML rendering configuration options."""
    html_version: HTMLVersion = HTMLVersion.HTML5
    css_framework: CSSFramework = CSSFramework.CUSTOM
    
    # Navigation
    include_navigation: bool = True
    include_toc: bool = True
    include_breadcrumbs: bool = True
    include_search: bool = True
    
    # Design
    responsive_design: bool = True
    dark_mode_support: bool = True
    print_friendly: bool = True
    
    # Assets
    inline_css: bool = False              # Inline vs external CSS
    inline_images: bool = False           # Base64 encode images
    include_javascript: bool = True       # Interactive features
    minify_output: bool = False           # Minify HTML/CSS/JS
    
    # Styling
    primary_color: str = "#0066cc"
    secondary_color: str = "#666666"
    accent_color: str = "#ff6600"
    warning_color: str = "#ff6600"
    caution_color: str = "#ffa500"
    font_family: str = "Arial, Helvetica, sans-serif"
    base_font_size: str = "16px"
    
    # Code/Technical
    syntax_highlighting: bool = True      # For code examples
    show_xml_ids: bool = False            # Show element IDs


@dataclass
class IETPConfig:
    """IETP package configuration."""
    title: str = "Technical Publication"
    version: str = "1.0.0"
    language: str = "en-US"
    security_level: str = "UNCLASSIFIED"
    
    # Viewer
    viewer_type: ViewerType = ViewerType.WEB
    
    # Features
    enable_search: bool = True
    enable_bookmarks: bool = True
    enable_annotations: bool = False
    enable_print: bool = True
    enable_offline: bool = True
    enable_hotspots: bool = True          # Interactive graphics hotspots
    
    # Content processing
    applicability_filtering: bool = True
    cross_reference_resolution: bool = True
    multimedia_support: bool = True
    
    # Branding
    logo_path: Optional[str] = None
    custom_css_path: Optional[str] = None


@dataclass
class RendererConfig:
    """Unified renderer configuration."""
    pdf: PDFRenderOptions = field(default_factory=PDFRenderOptions)
    html: HTMLRenderOptions = field(default_factory=HTMLRenderOptions)
    ietp: IETPConfig = field(default_factory=IETPConfig)
    
    # Common options
    output_dir: Optional[Path] = None
    temp_dir: Optional[Path] = None
    graphics_dir: Optional[Path] = None
    multimedia_dir: Optional[Path] = None
    
    # Metadata
    include_provenance: bool = True
    include_contract_info: bool = True


# =============================================================================
# DATA CLASSES - RESULTS
# =============================================================================


@dataclass
class PDFRenderResult:
    """Result of PDF rendering operation."""
    success: bool
    output_path: Optional[Path] = None
    pdf_data: Optional[bytes] = None
    page_count: int = 0
    file_size_bytes: int = 0
    dm_codes: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    rendered_at: str = field(default_factory=lambda: datetime.now().isoformat())
    render_time_seconds: float = 0.0
    
    @property
    def file_size_mb(self) -> float:
        """File size in megabytes."""
        return round(self.file_size_bytes / (1024 * 1024), 2)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "output_path": str(self.output_path) if self.output_path else None,
            "page_count": self.page_count,
            "file_size_bytes": self.file_size_bytes,
            "file_size_mb": self.file_size_mb,
            "dm_codes": self.dm_codes,
            "errors": self.errors,
            "warnings": self.warnings,
            "rendered_at": self.rendered_at,
            "render_time_seconds": self.render_time_seconds,
        }


@dataclass
class HTMLRenderResult:
    """Result of HTML rendering operation."""
    success: bool
    output_path: Optional[Path] = None
    html_data: Optional[str] = None
    asset_files: List[Path] = field(default_factory=list)  # CSS, JS, images
    dm_codes: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    rendered_at: str = field(default_factory=lambda: datetime.now().isoformat())
    render_time_seconds: float = 0.0
    file_size_bytes: int = 0
    
    @property
    def file_size_kb(self) -> float:
        """File size in kilobytes."""
        return round(self.file_size_bytes / 1024, 2)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "output_path": str(self.output_path) if self.output_path else None,
            "asset_files": [str(p) for p in self.asset_files],
            "dm_codes": self.dm_codes,
            "errors": self.errors,
            "warnings": self.warnings,
            "rendered_at": self.rendered_at,
            "render_time_seconds": self.render_time_seconds,
            "file_size_bytes": self.file_size_bytes,
            "file_size_kb": self.file_size_kb,
        }


@dataclass
class IETPPackageResult:
    """Result of IETP packaging operation."""
    success: bool
    output_path: Optional[Path] = None
    package_format: IETPFormat = IETPFormat.DIRECTORY
    dm_count: int = 0
    icn_count: int = 0
    multimedia_count: int = 0
    total_size_bytes: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    packaged_at: str = field(default_factory=lambda: datetime.now().isoformat())
    package_time_seconds: float = 0.0
    
    @property
    def total_size_mb(self) -> float:
        """Total size in megabytes."""
        return round(self.total_size_bytes / (1024 * 1024), 2)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "output_path": str(self.output_path) if self.output_path else None,
            "package_format": self.package_format.value,
            "dm_count": self.dm_count,
            "icn_count": self.icn_count,
            "multimedia_count": self.multimedia_count,
            "total_size_bytes": self.total_size_bytes,
            "total_size_mb": self.total_size_mb,
            "errors": self.errors,
            "warnings": self.warnings,
            "packaged_at": self.packaged_at,
            "package_time_seconds": self.package_time_seconds,
        }


# =============================================================================
# BASE RENDERER CLASS
# =============================================================================


class BaseRenderer(ABC):
    """
    Abstract base class for all ASIGT renderers.
    
    All renderers operate under ASIT contract authority.
    """
    
    S1000D_NS = "http://www.s1000d.org/S1000D_5-0"
    
    def __init__(
        self, 
        contract: Dict[str, Any], 
        config: Dict[str, Any],
        context: Optional[ExecutionContext] = None
    ):
        """
        Initialize renderer.
        
        Args:
            contract: ASIT transformation contract (required)
            config: Renderer configuration
            context: Execution context from ASIT
            
        Raises:
            ValueError: If contract is missing
        """
        if not contract:
            raise ValueError("ASIT contract is required for rendering")
        
        self.contract = contract
        self.config = config
        self.context = context
        self.logger = logging.getLogger(f"asigt.renderer.{self.__class__.__name__}")
        
        # Extract contract metadata
        self.contract_id = contract.get("id", "UNKNOWN")
        self.baseline_ref = contract.get("source", {}).get("baseline", "UNKNOWN")
        
        # Statistics
        self._render_count = 0
    
    @abstractmethod
    def render(self, content: Any, output_path: Optional[Path] = None) -> Any:
        """
        Render content to output format.
        
        Args:
            content: Content to render
            output_path: Output path (optional)
            
        Returns:
            Render result
        """
        raise NotImplementedError
    
    # =========================================================================
    # Common XML Helpers
    # =========================================================================
    
    def _find_element(
        self, 
        root: ET.Element, 
        name: str
    ) -> Optional[ET.Element]:
        """Find element by local name (ignoring namespace)."""
        for elem in root.iter():
            local_name = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
            if local_name == name:
                return elem
        return None
    
    def _find_element_text(
        self,
        root: ET.Element,
        name: str,
        default: str = ""
    ) -> str:
        """Find element text by local name."""
        elem = self._find_element(root, name)
        if elem is not None:
            return elem.text or default
        return default
    
    def _find_all_elements(
        self,
        root: ET.Element,
        name: str
    ) -> List[ET.Element]:
        """Find all elements by local name."""
        results = []
        for elem in root.iter():
            local_name = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
            if local_name == name:
                results.append(elem)
        return results
    
    def _get_local_name(self, element: ET.Element) -> str:
        """Get local name of element (without namespace)."""
        return element.tag.split("}")[-1] if "}" in element.tag else element.tag
    
    def _extract_dm_code(self, root: ET.Element) -> str:
        """Extract DM code from XML."""
        dm_code = self._find_element(root, "dmCode")
        if dm_code is not None:
            parts = [
                dm_code.get("modelIdentCode", ""),
                dm_code.get("systemDiffCode", ""),
                dm_code.get("systemCode", ""),
                dm_code.get("subSystemCode", ""),
                dm_code.get("subSubSystemCode", ""),
                dm_code.get("assyCode", ""),
                dm_code.get("disassyCode", ""),
                dm_code.get("disassyCodeVariant", ""),
                dm_code.get("infoCode", ""),
                dm_code.get("infoCodeVariant", ""),
                dm_code.get("itemLocationCode", ""),
            ]
            # Build standard DMC format
            return "-".join(p for p in parts[:3] if p) or "UNKNOWN"
        return "UNKNOWN"
    
    def _extract_pm_title(self, root: ET.Element) -> str:
        """Extract PM title from XML."""
        return self._find_element_text(root, "pmTitle", "Publication")
    
    def _extract_dm_refs(self, root: ET.Element) -> List[str]:
        """Extract DM references from PM."""
        dm_refs = []
        for dm_ref in self._find_all_elements(root, "dmRef"):
            dm_code = self._find_element(dm_ref, "dmCode")
            if dm_code is not None:
                code_str = self._build_dmc_string(dm_code)
                dm_refs.append(code_str)
        return dm_refs
    
    def _build_dmc_string(self, dm_code: ET.Element) -> str:
        """Build DMC string from dmCode element."""
        parts = [
            dm_code.get("modelIdentCode", ""),
            dm_code.get("systemCode", ""),
            dm_code.get("infoCode", ""),
        ]
        return "-".join(p for p in parts if p) or "UNKNOWN"
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize filename by removing invalid characters."""
        return "".join(c if c.isalnum() or c in "-_." else "_" for c in name)


# =============================================================================
# PDF RENDERER
# =============================================================================


class PDFRenderer(BaseRenderer):
    """
    S1000D PDF Renderer.
    
    Converts validated S1000D XML to publication-ready PDF documents
    with table of contents, list of effective pages, and professional formatting.
    
    Operates exclusively under ASIT contract authority.
    
    Supported engines:
        - WeasyPrint (recommended): HTML/CSS to PDF
        - ReportLab: Direct PDF generation
        - XSLT+FOP: XSLT transformation with Apache FOP
    
    Example:
        >>> renderer = PDFRenderer(
        ...     contract=contract,
        ...     config={"page_size": "A4", "include_toc": True}
        ... )
        >>> result = renderer.render_dm(dm_xml, Path("output/AMM.pdf"))
    """
    
    def __init__(
        self,
        contract: Dict[str, Any],
        config: Dict[str, Any],
        context: Optional[ExecutionContext] = None
    ):
        super().__init__(contract, config, context)
        
        # Parse options
        self.options = PDFRenderOptions(
            page_size=PageSize(config.get("page_size", "A4")),
            engine=PDFEngine(config.get("engine", "weasyprint")),
            include_toc=config.get("include_toc", True),
            include_lep=config.get("include_lep", True),
            include_bookmarks=config.get("include_bookmarks", True),
            header_text=config.get("header_text"),
            footer_text=config.get("footer_text"),
            watermark=config.get("watermark"),
            font_family=config.get("font_family", "Arial"),
            font_size=config.get("font_size", 10),
            margin_top_mm=config.get("margin_top_mm", 25.0),
            margin_bottom_mm=config.get("margin_bottom_mm", 25.0),
            margin_left_mm=config.get("margin_left_mm", 20.0),
            margin_right_mm=config.get("margin_right_mm", 20.0),
        )
        
        # Statistics
        self._total_pages = 0
        
        # Check engine availability
        self._engine_available = self._check_engine_available()
        
        self.logger.info(
            f"PDFRenderer initialized: contract={self.contract_id}, "
            f"engine={self.options.engine.value}, available={self._engine_available}"
        )
    
    def render(
        self, 
        content: Union[str, ET.Element], 
        output_path: Optional[Path] = None
    ) -> PDFRenderResult:
        """Render content to PDF (alias for render_dm)."""
        return self.render_dm(content, output_path)
    
    def render_dm(
        self,
        dm_content: Union[str, ET.Element],
        output_path: Optional[Path] = None,
        options: Optional[PDFRenderOptions] = None,
    ) -> PDFRenderResult:
        """
        Render a Data Module to PDF.
        
        Args:
            dm_content: S1000D XML content (string or Element)
            output_path: Output PDF path (optional)
            options: Rendering options (uses defaults if None)
            
        Returns:
            PDFRenderResult with PDF data and metadata
        """
        start_time = datetime.now()
        options = options or self.options
        result = PDFRenderResult(success=False)
        
        # Parse XML
        try:
            if isinstance(dm_content, str):
                root = ET.fromstring(dm_content)
            else:
                root = dm_content
        except ET.ParseError as e:
            result.errors.append(f"XML parse error: {e}")
            return result
        
        # Extract metadata
        dm_code = self._extract_dm_code(root)
        dm_title = self._find_element_text(root, "techName", "Data Module")
        result.dm_codes = [dm_code]
        
        # Convert to HTML
        try:
            html_content = self._dm_to_html(root, dm_title, options)
        except Exception as e:
            result.errors.append(f"HTML conversion error: {e}")
            return result
        
        # Render to PDF
        try:
            pdf_data = self._html_to_pdf(html_content, options)
            result.pdf_data = pdf_data
            result.file_size_bytes = len(pdf_data)
            result.page_count = self._estimate_page_count(pdf_data)
            result.success = True
        except Exception as e:
            result.errors.append(f"PDF generation error: {e}")
            return result
        
        # Write to file if path provided
        if output_path and result.success:
            try:
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(pdf_data)
                result.output_path = output_path
            except Exception as e:
                result.warnings.append(f"Failed to write file: {e}")
        
        # Update statistics
        self._render_count += 1
        self._total_pages += result.page_count
        
        # Calculate render time
        result.render_time_seconds = (datetime.now() - start_time).total_seconds()
        
        return result
    
    def render_pm(
        self,
        pm_content: Union[str, ET.Element],
        dm_contents: Dict[str, Union[str, ET.Element]],
        output_path: Optional[Path] = None,
        options: Optional[PDFRenderOptions] = None,
    ) -> PDFRenderResult:
        """
        Render a Publication Module with all DMs to PDF.
        
        Args:
            pm_content: Publication Module XML
            dm_contents: Dictionary mapping DM codes to DM XML content
            output_path: Output PDF path
            options: Rendering options
            
        Returns:
            PDFRenderResult
        """
        start_time = datetime.now()
        options = options or self.options
        result = PDFRenderResult(success=False)
        
        # Parse PM XML
        try:
            if isinstance(pm_content, str):
                pm_root = ET.fromstring(pm_content)
            else:
                pm_root = pm_content
        except ET.ParseError as e:
            result.errors.append(f"PM parse error: {e}")
            return result
        
        # Extract PM metadata
        pm_title = self._extract_pm_title(pm_root)
        dm_refs = self._extract_dm_refs(pm_root)
        result.dm_codes = dm_refs
        
        # Build combined HTML document
        html_parts = []
        
        # Cover page
        html_parts.append(self._generate_cover_page(pm_title, options))
        
        # Table of contents
        if options.include_toc:
            html_parts.append(self._generate_toc(dm_refs, dm_contents, options))
        
        # List of effective pages
        if options.include_lep:
            html_parts.append(self._generate_lep(dm_refs))
        
        # Render each DM
        for dm_ref in dm_refs:
            if dm_ref in dm_contents:
                try:
                    dm_xml = dm_contents[dm_ref]
                    if isinstance(dm_xml, str):
                        dm_root = ET.fromstring(dm_xml)
                    else:
                        dm_root = dm_xml
                    
                    dm_title = self._find_element_text(dm_root, "techName", dm_ref)
                    dm_html = self._dm_content_to_html(dm_root, options)
                    
                    # Page break before each DM
                    html_parts.append('<div class="page-break"></div>')
                    html_parts.append(f'<section class="data-module" id="{self._sanitize_filename(dm_ref)}">')
                    html_parts.append(f'<h1>{self._escape_html(dm_title)}</h1>')
                    html_parts.append(dm_html)
                    html_parts.append('</section>')
                    
                except Exception as e:
                    result.warnings.append(f"Failed to render DM {dm_ref}: {e}")
            else:
                result.warnings.append(f"DM content not found: {dm_ref}")
        
        # Combine HTML
        full_html = self._wrap_html_document(
            "\n".join(html_parts), 
            pm_title, 
            options
        )
        
        # Render to PDF
        try:
            pdf_data = self._html_to_pdf(full_html, options)
            result.pdf_data = pdf_data
            result.file_size_bytes = len(pdf_data)
            result.page_count = self._estimate_page_count(pdf_data)
            result.success = True
        except Exception as e:
            result.errors.append(f"PDF generation error: {e}")
            return result
        
        # Write to file
        if output_path and result.success:
            try:
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(pdf_data)
                result.output_path = output_path
            except Exception as e:
                result.warnings.append(f"Failed to write file: {e}")
        
        # Update statistics
        self._render_count += 1
        self._total_pages += result.page_count
        result.render_time_seconds = (datetime.now() - start_time).total_seconds()
        
        return result
    
    def _check_engine_available(self) -> bool:
        """Check if the selected PDF engine is available."""
        if self.options.engine == PDFEngine.WEASYPRINT:
            try:
                import weasyprint
                return True
            except ImportError:
                self.logger.warning("WeasyPrint not installed. Install with: pip install weasyprint")
                return False
        elif self.options.engine == PDFEngine.REPORTLAB:
            try:
                import reportlab
                return True
            except ImportError:
                self.logger.warning("ReportLab not installed. Install with: pip install reportlab")
                return False
        return False
    
    def _dm_to_html(
        self, 
        root: ET.Element, 
        title: str, 
        options: PDFRenderOptions
    ) -> str:
        """Convert complete DM to HTML document."""
        body_html = self._dm_content_to_html(root, options)
        return self._wrap_html_document(
            f'<h1>{self._escape_html(title)}</h1>\n{body_html}',
            title,
            options
        )
    
    def _dm_content_to_html(
        self, 
        root: ET.Element, 
        options: PDFRenderOptions
    ) -> str:
        """Convert DM content section to HTML."""
        html_parts = []
        
        # Info name / subtitle
        info_name = self._find_element_text(root, "infoName", "")
        if info_name:
            html_parts.append(f'<p class="subtitle">{self._escape_html(info_name)}</p>')
        
        # Process content
        content = self._find_element(root, "content")
        if content is not None:
            for child in content:
                html_parts.append(self._element_to_html(child, options))
        
        return "\n".join(html_parts)
    
    def _element_to_html(
        self, 
        element: ET.Element, 
        options: PDFRenderOptions
    ) -> str:
        """Convert XML element to HTML recursively."""
        local_name = self._get_local_name(element)
        
        # Specialized converters
        converters = {
            "description": self._convert_description,
            "procedure": self._convert_procedure,
            "levelledPara": self._convert_levelled_para,
            "para": self._convert_para,
            "title": self._convert_title,
            "warning": lambda e, o: self._convert_admonition(e, o, "warning"),
            "caution": lambda e, o: self._convert_admonition(e, o, "caution"),
            "note": lambda e, o: self._convert_admonition(e, o, "note"),
            "table": self._convert_table,
            "figure": self._convert_figure,
            "proceduralStep": self._convert_procedural_step,
            "internalRef": self._convert_internal_ref,
            "externalPubRef": self._convert_external_ref,
            "dmRef": self._convert_dm_ref,
            "randomList": self._convert_random_list,
            "sequentialList": self._convert_sequential_list,
            "definitionList": self._convert_definition_list,
        }
        
        if local_name in converters:
            return converters[local_name](element, options)
        
        # Default: process children
        return self._convert_default(element, options)
    
    def _convert_description(self, element: ET.Element, options: PDFRenderOptions) -> str:
        """Convert description content."""
        children_html = "".join(self._element_to_html(child, options) for child in element)
        return f'<div class="description">{children_html}</div>'
    
    def _convert_procedure(self, element: ET.Element, options: PDFRenderOptions) -> str:
        """Convert procedure content."""
        children_html = "".join(self._element_to_html(child, options) for child in element)
        return f'<div class="procedure">{children_html}</div>'
    
    def _convert_levelled_para(self, element: ET.Element, options: PDFRenderOptions) -> str:
        """Convert levelled paragraph."""
        html_parts = []
        
        title = self._find_element(element, "title")
        if title is not None:
            html_parts.append(f'<h2>{self._escape_html(title.text or "")}</h2>')
        
        for child in element:
            child_name = self._get_local_name(child)
            if child_name != "title":
                html_parts.append(self._element_to_html(child, options))
        
        return f'<section class="levelled-para">{chr(10).join(html_parts)}</section>'
    
    def _convert_para(self, element: ET.Element, options: PDFRenderOptions) -> str:
        """Convert paragraph."""
        text = self._get_text_with_children(element, options)
        return f'<p class="para">{text}</p>'
    
    def _convert_title(self, element: ET.Element, options: PDFRenderOptions) -> str:
        """Convert title."""
        text = self._get_text_with_children(element, options)
        return f'<h2 class="title">{text}</h2>'
    
    def _convert_admonition(
        self, 
        element: ET.Element, 
        options: PDFRenderOptions,
        admonition_type: str
    ) -> str:
        """Convert warning/caution/note."""
        icons = {"warning": "⚠️", "caution": "⚡", "note": "ℹ️"}
        labels = {"warning": "WARNING", "caution": "CAUTION", "note": "NOTE"}
        
        text = self._get_text_with_children(element, options)
        icon = icons.get(admonition_type, "")
        label = labels.get(admonition_type, "")
        
        return f'''
        <div class="admonition {admonition_type}">
            <div class="admonition-icon">{icon}</div>
            <div class="admonition-content">
                <strong>{label}</strong>
                <div>{text}</div>
            </div>
        </div>
        '''
    
    def _convert_table(self, element: ET.Element, options: PDFRenderOptions) -> str:
        """Convert table."""
        html = ['<table class="s1000d-table">']
        
        # Caption
        title = self._find_element(element, "title")
        if title is not None:
            html.append(f'<caption>{self._escape_html(title.text or "")}</caption>')
        
        # Process tgroup
        tgroup = self._find_element(element, "tgroup")
        if tgroup is not None:
            # Header
            thead = self._find_element(tgroup, "thead")
            if thead is not None:
                html.append('<thead>')
                for row in self._find_all_elements(thead, "row"):
                    html.append('<tr>')
                    for entry in self._find_all_elements(row, "entry"):
                        text = self._get_text_with_children(entry, options)
                        html.append(f'<th>{text}</th>')
                    html.append('</tr>')
                html.append('</thead>')
            
            # Body
            tbody = self._find_element(tgroup, "tbody")
            if tbody is not None:
                html.append('<tbody>')
                for row in self._find_all_elements(tbody, "row"):
                    html.append('<tr>')
                    for entry in self._find_all_elements(row, "entry"):
                        text = self._get_text_with_children(entry, options)
                        html.append(f'<td>{text}</td>')
                    html.append('</tr>')
                html.append('</tbody>')
        
        html.append('</table>')
        return "\n".join(html)
    
    def _convert_figure(self, element: ET.Element, options: PDFRenderOptions) -> str:
        """Convert figure with graphic."""
        html = ['<figure class="s1000d-figure">']
        
        # Graphic
        graphic = self._find_element(element, "graphic")
        if graphic is not None:
            icn = graphic.get("infoEntityIdent", "")
            if icn:
                html.append(f'<img src="{icn}" alt="{icn}" class="figure-graphic">')
        
        # Caption
        title = self._find_element(element, "title")
        if title is not None:
            html.append(f'<figcaption>{self._escape_html(title.text or "")}</figcaption>')
        
        html.append('</figure>')
        return "\n".join(html)
    
    def _convert_procedural_step(
        self, 
        element: ET.Element, 
        options: PDFRenderOptions
    ) -> str:
        """Convert procedural step."""
        html_parts = ['<li class="procedural-step">']
        
        for child in element:
            html_parts.append(self._element_to_html(child, options))
        
        html_parts.append('</li>')
        return "\n".join(html_parts)
    
    def _convert_internal_ref(
        self, 
        element: ET.Element, 
        options: PDFRenderOptions
    ) -> str:
        """Convert internal reference."""
        ref_id = element.get("internalRefId", "")
        text = element.text or ref_id
        return f'<a href="#{ref_id}" class="internal-ref">{self._escape_html(text)}</a>'
    
    def _convert_external_ref(
        self, 
        element: ET.Element, 
        options: PDFRenderOptions
    ) -> str:
        """Convert external publication reference."""
        text = self._get_text_with_children(element, options)
        return f'<span class="external-ref">{text}</span>'
    
    def _convert_dm_ref(self, element: ET.Element, options: PDFRenderOptions) -> str:
        """Convert DM reference."""
        dm_code = self._find_element(element, "dmCode")
        if dm_code is not None:
            dmc = self._build_dmc_string(dm_code)
            return f'<a href="#{self._sanitize_filename(dmc)}" class="dm-ref">{dmc}</a>'
        return ""
    
    def _convert_random_list(
        self, 
        element: ET.Element, 
        options: PDFRenderOptions
    ) -> str:
        """Convert random (unordered) list."""
        items = []
        for item in self._find_all_elements(element, "listItem"):
            text = self._get_text_with_children(item, options)
            items.append(f'<li>{text}</li>')
        return f'<ul class="random-list">{"".join(items)}</ul>'
    
    def _convert_sequential_list(
        self, 
        element: ET.Element, 
        options: PDFRenderOptions
    ) -> str:
        """Convert sequential (ordered) list."""
        items = []
        for item in self._find_all_elements(element, "listItem"):
            text = self._get_text_with_children(item, options)
            items.append(f'<li>{text}</li>')
        return f'<ol class="sequential-list">{"".join(items)}</ol>'
    
    def _convert_definition_list(
        self, 
        element: ET.Element, 
        options: PDFRenderOptions
    ) -> str:
        """Convert definition list."""
        html = ['<dl class="definition-list">']
        for item in self._find_all_elements(element, "definitionListItem"):
            term = self._find_element(item, "listItemTerm")
            defn = self._find_element(item, "listItemDefinition")
            if term is not None:
                html.append(f'<dt>{self._escape_html(term.text or "")}</dt>')
            if defn is not None:
                html.append(f'<dd>{self._get_text_with_children(defn, options)}</dd>')
        html.append('</dl>')
        return "\n".join(html)
    
    def _convert_default(
        self, 
        element: ET.Element, 
        options: PDFRenderOptions
    ) -> str:
        """Default element conversion."""
        children_html = "".join(self._element_to_html(child, options) for child in element)
        text = element.text or ""
        tail = element.tail or ""
        return f"{text}{children_html}{tail}"
    
    def _get_text_with_children(
        self, 
        element: ET.Element, 
        options: PDFRenderOptions
    ) -> str:
        """Get element text including inline children."""
        parts = []
        if element.text:
            parts.append(self._escape_html(element.text))
        for child in element:
            parts.append(self._element_to_html(child, options))
            if child.tail:
                parts.append(self._escape_html(child.tail))
        return "".join(parts)
    
    def _generate_cover_page(self, title: str, options: PDFRenderOptions) -> str:
        """Generate cover page HTML."""
        watermark = ""
        if options.watermark:
            watermark = f'<div class="watermark">{self._escape_html(options.watermark)}</div>'
        
        return f'''
        <div class="cover-page">
            {watermark}
            <h1 class="cover-title">{self._escape_html(title)}</h1>
            <div class="cover-metadata">
                <p><strong>Contract:</strong> {self.contract_id}</p>
                <p><strong>Baseline:</strong> {self.baseline_ref}</p>
                <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d")}</p>
            </div>
        </div>
        '''
    
    def _generate_toc(
        self, 
        dm_refs: List[str],
        dm_contents: Dict[str, Union[str, ET.Element]],
        options: PDFRenderOptions
    ) -> str:
        """Generate table of contents HTML."""
        html = ['<div class="toc">', '<h1>Table of Contents</h1>', '<nav class="toc-list">']
        
        for i, dm_ref in enumerate(dm_refs, 1):
            title = dm_ref
            if dm_ref in dm_contents:
                dm_xml = dm_contents[dm_ref]
                if isinstance(dm_xml, str):
                    try:
                        root = ET.fromstring(dm_xml)
                        title = self._find_element_text(root, "techName", dm_ref)
                    except:
                        pass
                else:
                    title = self._find_element_text(dm_xml, "techName", dm_ref)
            
            anchor = self._sanitize_filename(dm_ref)
            html.append(f'<div class="toc-entry"><a href="#{anchor}">{i}. {self._escape_html(title)}</a></div>')
        
        html.extend(['</nav>', '</div>'])
        return "\n".join(html)
    
    def _generate_lep(self, dm_refs: List[str]) -> str:
        """Generate list of effective pages HTML."""
        html = ['<div class="lep">', '<h1>List of Effective Pages</h1>', '<table class="lep-table">']
        html.append('<tr><th>Data Module</th><th>Revision</th><th>Date</th></tr>')
        
        for dm_ref in dm_refs:
            html.append(f'<tr><td>{self._escape_html(dm_ref)}</td><td>001</td><td>{datetime.now().strftime("%Y-%m-%d")}</td></tr>')
        
        html.extend(['</table>', '</div>'])
        return "\n".join(html)
    
    def _wrap_html_document(
        self, 
        body_content: str, 
        title: str, 
        options: PDFRenderOptions
    ) -> str:
        """Wrap content in complete HTML document with CSS."""
        css = self._generate_pdf_css(options)
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{self._escape_html(title)}</title>
    <style>{css}</style>
</head>
<body>
    {body_content}
</body>
</html>'''
    
    def _generate_pdf_css(self, options: PDFRenderOptions) -> str:
        """Generate CSS for PDF rendering."""
        return f'''
/* S1000D PDF Stylesheet */
/* Contract: {self.contract_id} */

@page {{
    size: {options.page_size.value};
    margin: {options.margin_top_mm}mm {options.margin_right_mm}mm 
            {options.margin_bottom_mm}mm {options.margin_left_mm}mm;
    
    @top-center {{
        content: "{options.header_text or self.contract_id}";
        font-size: 9pt;
        color: #666;
    }}
    
    @bottom-center {{
        content: "{options.footer_text or ''} Page " counter(page) " of " counter(pages);
        font-size: 9pt;
        color: #666;
    }}
}}

body {{
    font-family: {options.font_family}, sans-serif;
    font-size: {options.font_size}pt;
    line-height: 1.5;
    color: #000;
}}

h1 {{
    font-size: {options.title_font_size}pt;
    font-weight: bold;
    margin-top: 24pt;
    margin-bottom: 12pt;
    page-break-after: avoid;
}}

h2 {{
    font-size: {options.heading_font_size}pt;
    font-weight: bold;
    margin-top: 18pt;
    margin-bottom: 9pt;
    page-break-after: avoid;
}}

.para {{
    margin: 8pt 0;
    text-align: justify;
}}

.subtitle {{
    font-size: 12pt;
    font-style: italic;
    color: #444;
    margin-bottom: 18pt;
}}

/* Cover page */
.cover-page {{
    text-align: center;
    page-break-after: always;
    padding-top: 120pt;
}}

.cover-title {{
    font-size: 28pt;
    margin-bottom: 48pt;
}}

.cover-metadata {{
    margin-top: 72pt;
    font-size: 11pt;
}}

.watermark {{
    position: fixed;
    top: 40%;
    left: 50%;
    transform: translate(-50%, -50%) rotate(-45deg);
    font-size: 72pt;
    color: rgba(0, 0, 0, 0.1);
    z-index: -1;
}}

/* TOC */
.toc {{
    page-break-after: always;
}}

.toc-entry {{
    margin: 6pt 0;
}}

.toc-entry a {{
    color: #000;
    text-decoration: none;
}}

/* LEP */
.lep {{
    page-break-after: always;
}}

.lep-table {{
    width: 100%;
    border-collapse: collapse;
}}

.lep-table th, .lep-table td {{
    border: 1pt solid #000;
    padding: 6pt;
    text-align: left;
}}

.lep-table th {{
    background-color: #f0f0f0;
}}

/* Admonitions */
.admonition {{
    display: flex;
    padding: 12pt;
    margin: 12pt 0;
    border-left: 4pt solid;
    page-break-inside: avoid;
}}

.warning {{
    background-color: #fff0f0;
    border-color: #cc0000;
}}

.caution {{
    background-color: #fff8f0;
    border-color: #ff8800;
}}

.note {{
    background-color: #f0f8ff;
    border-color: #0066cc;
}}

.admonition-icon {{
    font-size: 18pt;
    margin-right: 12pt;
}}

.admonition-content strong {{
    display: block;
    margin-bottom: 6pt;
}}

/* Tables */
.s1000d-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12pt 0;
    page-break-inside: avoid;
}}

.s1000d-table caption {{
    font-weight: bold;
    text-align: left;
    padding: 6pt;
    background-color: #f5f5f5;
}}

.s1000d-table th, .s1000d-table td {{
    border: 1pt solid #000;
    padding: 6pt;
    text-align: left;
    vertical-align: top;
}}

.s1000d-table th {{
    background-color: #f0f0f0;
    font-weight: bold;
}}

/* Figures */
.s1000d-figure {{
    text-align: center;
    margin: 18pt 0;
    page-break-inside: avoid;
}}

.figure-graphic {{
    max-width: 100%;
    height: auto;
}}

figcaption {{
    font-style: italic;
    margin-top: 6pt;
}}

/* Lists */
.random-list, .sequential-list {{
    margin: 12pt 0;
    padding-left: 24pt;
}}

.definition-list {{
    margin: 12pt 0;
}}

.definition-list dt {{
    font-weight: bold;
    margin-top: 6pt;
}}

.definition-list dd {{
    margin-left: 24pt;
}}

/* Procedural steps */
.procedure ol {{
    counter-reset: step;
    list-style-type: none;
    padding-left: 0;
}}

.procedural-step {{
    counter-increment: step;
    margin: 12pt 0;
    padding-left: 36pt;
    position: relative;
}}

.procedural-step::before {{
    content: counter(step) ".";
    position: absolute;
    left: 0;
    font-weight: bold;
}}

/* References */
.internal-ref, .dm-ref {{
    color: #0066cc;
    text-decoration: none;
}}

.external-ref {{
    font-style: italic;
}}

/* Page breaks */
.page-break {{
    page-break-before: always;
}}

.data-module {{
    page-break-before: always;
}}
'''
    
    def _html_to_pdf(self, html: str, options: PDFRenderOptions) -> bytes:
        """Convert HTML to PDF using selected engine."""
        if not self._engine_available:
            # Fallback: return placeholder
            self.logger.warning("PDF engine not available, returning placeholder")
            return b"%PDF-1.4 placeholder"
        
        if options.engine == PDFEngine.WEASYPRINT:
            import weasyprint
            return weasyprint.HTML(string=html).write_pdf()
        
        raise NotImplementedError(f"Engine {options.engine.value} not implemented")
    
    def _estimate_page_count(self, pdf_data: bytes) -> int:
        """Estimate page count from PDF data size."""
        # Rough approximation: ~10KB per page
        return max(1, len(pdf_data) // 10000)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get rendering statistics."""
        return {
            "contract_id": self.contract_id,
            "engine": self.options.engine.value,
            "engine_available": self._engine_available,
            "render_count": self._render_count,
            "total_pages": self._total_pages,
        }


# =============================================================================
# HTML RENDERER
# =============================================================================


class HTMLRenderer(BaseRenderer):
    """
    S1000D HTML Renderer.
    
    Converts validated S1000D XML to responsive HTML with CSS styling
    for web viewing, IETP integration, and preview workflows.
    
    Operates exclusively under ASIT contract authority.
    
    Example:
        >>> renderer = HTMLRenderer(
        ...     contract=contract,
        ...     config={"primary_color": "#0066cc", "include_toc": True}
        ... )
        >>> result = renderer.render_dm(dm_xml, Path("output/AMM.html"))
    """
    
    def __init__(
        self,
        contract: Dict[str, Any],
        config: Dict[str, Any],
        context: Optional[ExecutionContext] = None
    ):
        super().__init__(contract, config, context)
        
        # Parse options
        self.options = HTMLRenderOptions(
            html_version=HTMLVersion(config.get("html_version", "html5")),
            css_framework=CSSFramework(config.get("css_framework", "custom")),
            include_navigation=config.get("include_navigation", True),
            include_toc=config.get("include_toc", True),
            include_search=config.get("include_search", True),
            responsive_design=config.get("responsive_design", True),
            dark_mode_support=config.get("dark_mode_support", True),
            inline_css=config.get("inline_css", False),
            include_javascript=config.get("include_javascript", True),
            primary_color=config.get("primary_color", "#0066cc"),
            secondary_color=config.get("secondary_color", "#666666"),
            font_family=config.get("font_family", "Arial, Helvetica, sans-serif"),
        )
        
        # Cross-reference tracking
        self._cross_refs: Set[str] = set()
        
        self.logger.info(
            f"HTMLRenderer initialized: contract={self.contract_id}, "
            f"version={self.options.html_version.value}"
        )
    
    def render(
        self, 
        content: Union[str, ET.Element], 
        output_path: Optional[Path] = None
    ) -> HTMLRenderResult:
        """Render content to HTML (alias for render_dm)."""
        return self.render_dm(content, output_path)
    
    def render_dm(
        self,
        dm_content: Union[str, ET.Element],
        output_path: Optional[Path] = None,
        options: Optional[HTMLRenderOptions] = None,
    ) -> HTMLRenderResult:
        """
        Render a Data Module to HTML.
        
        Args:
            dm_content: S1000D XML content
            output_path: Output HTML path (optional)
            options: Rendering options
            
        Returns:
            HTMLRenderResult
        """
        start_time = datetime.now()
        options = options or self.options
        result = HTMLRenderResult(success=False)
        
        # Parse XML
        try:
            if isinstance(dm_content, str):
                root = ET.fromstring(dm_content)
            else:
                root = dm_content
        except ET.ParseError as e:
            result.errors.append(f"XML parse error: {e}")
            return result
        
        # Extract metadata
        dm_code = self._extract_dm_code(root)
        dm_title = self._find_element_text(root, "techName", "Data Module")
        result.dm_codes = [dm_code]
        
        # Build HTML
        try:
            body_html = self._dm_to_html(root, options)
            full_html = self._build_html_document(dm_title, body_html, options)
            result.html_data = full_html
            result.file_size_bytes = len(full_html.encode('utf-8'))
            result.success = True
        except Exception as e:
            result.errors.append(f"HTML generation error: {e}")
            return result
        
        # Write to file if path provided
        if output_path and result.success:
            try:
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(full_html, encoding='utf-8')
                result.output_path = output_path
                
                # Generate external CSS if not inline
                if not options.inline_css:
                    css_path = output_path.with_suffix('.css')
                    css_content = self._generate_css(options)
                    css_path.write_text(css_content, encoding='utf-8')
                    result.asset_files.append(css_path)
                
                # Generate JavaScript if enabled
                if options.include_javascript:
                    js_path = output_path.with_suffix('.js')
                    js_content = self._generate_javascript(options)
                    js_path.write_text(js_content, encoding='utf-8')
                    result.asset_files.append(js_path)
                    
            except Exception as e:
                result.warnings.append(f"Failed to write files: {e}")
        
        # Update statistics
        self._render_count += 1
        result.render_time_seconds = (datetime.now() - start_time).total_seconds()
        
        return result
    
    def render_pm(
        self,
        pm_content: Union[str, ET.Element],
        dm_contents: Dict[str, Union[str, ET.Element]],
        output_dir: Optional[Path] = None,
        options: Optional[HTMLRenderOptions] = None,
    ) -> HTMLRenderResult:
        """
        Render a Publication Module to HTML.
        
        Generates index page and individual HTML pages for each DM.
        
        Args:
            pm_content: Publication Module XML
            dm_contents: Dictionary of DM codes to DM XML content
            output_dir: Output directory for HTML files
            options: Rendering options
            
        Returns:
            HTMLRenderResult
        """
        start_time = datetime.now()
        options = options or self.options
        result = HTMLRenderResult(success=False)
        
        # Parse PM XML
        try:
            if isinstance(pm_content, str):
                pm_root = ET.fromstring(pm_content)
            else:
                pm_root = pm_content
        except ET.ParseError as e:
            result.errors.append(f"PM parse error: {e}")
            return result
        
        # Extract PM metadata
        pm_title = self._extract_pm_title(pm_root)
        dm_refs = self._extract_dm_refs(pm_root)
        result.dm_codes = dm_refs
        
        # Create output directory
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate index page
        try:
            index_html = self._generate_index_page(pm_title, dm_refs, dm_contents, options)
            if output_dir:
                index_path = output_dir / "index.html"
                index_path.write_text(index_html, encoding='utf-8')
                result.output_path = index_path
            result.html_data = index_html
        except Exception as e:
            result.errors.append(f"Index page error: {e}")
            return result
        
        # Render each DM
        for dm_ref in dm_refs:
            if dm_ref in dm_contents:
                try:
                    dm_xml = dm_contents[dm_ref]
                    if isinstance(dm_xml, str):
                        dm_root = ET.fromstring(dm_xml)
                    else:
                        dm_root = dm_xml
                    
                    dm_title = self._find_element_text(dm_root, "techName", dm_ref)
                    dm_html_body = self._dm_to_html(dm_root, options)
                    
                    # Add navigation
                    nav_html = self._generate_dm_navigation(dm_ref, dm_refs)
                    full_dm_html = self._build_html_document(
                        dm_title,
                        nav_html + dm_html_body,
                        options
                    )
                    
                    if output_dir:
                        dm_filename = self._sanitize_filename(dm_ref) + ".html"
                        dm_path = output_dir / dm_filename
                        dm_path.write_text(full_dm_html, encoding='utf-8')
                        result.asset_files.append(dm_path)
                        
                except Exception as e:
                    result.warnings.append(f"Failed to render DM {dm_ref}: {e}")
            else:
                result.warnings.append(f"DM content not found: {dm_ref}")
        
        # Generate shared assets
        if output_dir:
            # CSS
            if not options.inline_css:
                css_path = output_dir / "styles.css"
                css_path.write_text(self._generate_css(options), encoding='utf-8')
                result.asset_files.append(css_path)
            
            # JavaScript
            if options.include_javascript:
                js_path = output_dir / "scripts.js"
                js_path.write_text(self._generate_javascript(options), encoding='utf-8')
                result.asset_files.append(js_path)
        
        result.success = True
        result.file_size_bytes = len(index_html.encode('utf-8'))
        self._render_count += 1
        result.render_time_seconds = (datetime.now() - start_time).total_seconds()
        
        return result
    
    def _dm_to_html(self, root: ET.Element, options: HTMLRenderOptions) -> str:
        """Convert Data Module to HTML body content."""
        html_parts = ['<article class="data-module">']
        
        # Title
        tech_name = self._find_element_text(root, "techName", "Data Module")
        html_parts.append(f'<h1 class="dm-title">{self._escape_html(tech_name)}</h1>')
        
        # Info name
        info_name = self._find_element_text(root, "infoName", "")
        if info_name:
            html_parts.append(f'<p class="dm-subtitle">{self._escape_html(info_name)}</p>')
        
        # Content
        content = self._find_element(root, "content")
        if content is not None:
            for child in content:
                html_parts.append(self._element_to_html(child, options))
        
        html_parts.append('</article>')
        return "\n".join(html_parts)
    
    def _element_to_html(self, element: ET.Element, options: HTMLRenderOptions) -> str:
        """Convert XML element to HTML recursively."""
        local_name = self._get_local_name(element)
        
        converters = {
            "description": self._convert_section,
            "procedure": self._convert_section,
            "levelledPara": self._convert_levelled_para,
            "para": self._convert_para,
            "title": self._convert_title,
            "warning": lambda e, o: self._convert_alert(e, o, "warning"),
            "caution": lambda e, o: self._convert_alert(e, o, "caution"),
            "note": lambda e, o: self._convert_alert(e, o, "note"),
            "table": self._convert_table,
            "figure": self._convert_figure,
            "proceduralStep": self._convert_step,
            "internalRef": self._convert_internal_ref,
            "externalPubRef": self._convert_external_ref,
            "randomList": self._convert_ul,
            "sequentialList": self._convert_ol,
        }
        
        if local_name in converters:
            return converters[local_name](element, options)
        
        return self._convert_default(element, options)
    
    def _convert_section(self, element: ET.Element, options: HTMLRenderOptions) -> str:
        """Convert section element."""
        local_name = self._get_local_name(element)
        children = "".join(self._element_to_html(c, options) for c in element)
        return f'<section class="{local_name}">{children}</section>'
    
    def _convert_levelled_para(self, element: ET.Element, options: HTMLRenderOptions) -> str:
        """Convert levelled paragraph."""
        html_parts = ['<div class="levelled-para">']
        title = self._find_element(element, "title")
        if title is not None:
            html_parts.append(f'<h2>{self._escape_html(title.text or "")}</h2>')
        for child in element:
            if self._get_local_name(child) != "title":
                html_parts.append(self._element_to_html(child, options))
        html_parts.append('</div>')
        return "\n".join(html_parts)
    
    def _convert_para(self, element: ET.Element, options: HTMLRenderOptions) -> str:
        """Convert paragraph."""
        text = self._get_text_with_children(element, options)
        return f'<p class="para">{text}</p>'
    
    def _convert_title(self, element: ET.Element, options: HTMLRenderOptions) -> str:
        """Convert title."""
        text = self._get_text_with_children(element, options)
        return f'<h2 class="title">{text}</h2>'
    
    def _convert_alert(
        self, 
        element: ET.Element, 
        options: HTMLRenderOptions,
        alert_type: str
    ) -> str:
        """Convert warning/caution/note to alert box."""
        icons = {"warning": "⚠️", "caution": "⚡", "note": "ℹ️"}
        text = self._get_text_with_children(element, options)
        
        return f'''
        <div class="alert alert-{alert_type}">
            <div class="alert-icon">{icons.get(alert_type, "")}</div>
            <div class="alert-content">
                <strong>{alert_type.upper()}</strong>
                {text}
            </div>
        </div>
        '''
    
    def _convert_table(self, element: ET.Element, options: HTMLRenderOptions) -> str:
        """Convert table."""
        html = ['<table class="table">']
        
        title = self._find_element(element, "title")
        if title is not None:
            html.append(f'<caption>{self._escape_html(title.text or "")}</caption>')
        
        tgroup = self._find_element(element, "tgroup")
        if tgroup is not None:
            thead = self._find_element(tgroup, "thead")
            if thead:
                html.append('<thead>')
                for row in self._find_all_elements(thead, "row"):
                    html.append('<tr>')
                    for entry in self._find_all_elements(row, "entry"):
                        html.append(f'<th>{self._get_text_with_children(entry, options)}</th>')
                    html.append('</tr>')
                html.append('</thead>')
            
            tbody = self._find_element(tgroup, "tbody")
            if tbody:
                html.append('<tbody>')
                for row in self._find_all_elements(tbody, "row"):
                    html.append('<tr>')
                    for entry in self._find_all_elements(row, "entry"):
                        html.append(f'<td>{self._get_text_with_children(entry, options)}</td>')
                    html.append('</tr>')
                html.append('</tbody>')
        
        html.append('</table>')
        return "\n".join(html)
    
    def _convert_figure(self, element: ET.Element, options: HTMLRenderOptions) -> str:
        """Convert figure."""
        html = ['<figure class="figure">']
        
        graphic = self._find_element(element, "graphic")
        if graphic is not None:
            icn = graphic.get("infoEntityIdent", "")
            if icn:
                html.append(f'<img src="{icn}.png" alt="{icn}" class="figure-img">')
        
        title = self._find_element(element, "title")
        if title is not None:
            html.append(f'<figcaption>{self._escape_html(title.text or "")}</figcaption>')
        
        html.append('</figure>')
        return "\n".join(html)
    
    def _convert_step(self, element: ET.Element, options: HTMLRenderOptions) -> str:
        """Convert procedural step."""
        children = "".join(self._element_to_html(c, options) for c in element)
        return f'<li class="step">{children}</li>'
    
    def _convert_internal_ref(self, element: ET.Element, options: HTMLRenderOptions) -> str:
        """Convert internal reference."""
        ref_id = element.get("internalRefId", "")
        text = element.text or ref_id
        self._cross_refs.add(ref_id)
        return f'<a href="#{ref_id}" class="internal-ref">{self._escape_html(text)}</a>'
    
    def _convert_external_ref(self, element: ET.Element, options: HTMLRenderOptions) -> str:
        """Convert external reference."""
        text = self._get_text_with_children(element, options)
        return f'<span class="external-ref">{text}</span>'
    
    def _convert_ul(self, element: ET.Element, options: HTMLRenderOptions) -> str:
        """Convert unordered list."""
        items = []
        for item in self._find_all_elements(element, "listItem"):
            items.append(f'<li>{self._get_text_with_children(item, options)}</li>')
        return f'<ul class="list">{"".join(items)}</ul>'
    
    def _convert_ol(self, element: ET.Element, options: HTMLRenderOptions) -> str:
        """Convert ordered list."""
        items = []
        for item in self._find_all_elements(element, "listItem"):
            items.append(f'<li>{self._get_text_with_children(item, options)}</li>')
        return f'<ol class="list">{"".join(items)}</ol>'
    
    def _convert_default(self, element: ET.Element, options: HTMLRenderOptions) -> str:
        """Default element conversion."""
        local_name = self._get_local_name(element)
        children = "".join(self._element_to_html(c, options) for c in element)
        text = element.text or ""
        tail = element.tail or ""
        return f'<div class="{local_name}">{text}{children}</div>{tail}'
    
    def _get_text_with_children(self, element: ET.Element, options: HTMLRenderOptions) -> str:
        """Get element text including inline children."""
        parts = []
        if element.text:
            parts.append(self._escape_html(element.text))
        for child in element:
            parts.append(self._element_to_html(child, options))
            if child.tail:
                parts.append(self._escape_html(child.tail))
        return "".join(parts)
    
    def _build_html_document(
        self, 
        title: str, 
        body_content: str, 
        options: HTMLRenderOptions
    ) -> str:
        """Build complete HTML document."""
        # CSS
        if options.inline_css:
            css_block = f"<style>{self._generate_css(options)}</style>"
        else:
            css_block = '<link rel="stylesheet" href="styles.css">'
        
        # JavaScript
        js_block = ""
        if options.include_javascript:
            if options.inline_css:
                js_block = f"<script>{self._generate_javascript(options)}</script>"
            else:
                js_block = '<script src="scripts.js"></script>'
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="contract" content="{self.contract_id}">
    <meta name="baseline" content="{self.baseline_ref}">
    <meta name="generated" content="{datetime.now().isoformat()}">
    <title>{self._escape_html(title)}</title>
    {css_block}
</head>
<body>
    {body_content}
    {js_block}
</body>
</html>'''
    
    def _generate_index_page(
        self,
        pm_title: str,
        dm_refs: List[str],
        dm_contents: Dict[str, Union[str, ET.Element]],
        options: HTMLRenderOptions
    ) -> str:
        """Generate index page for publication module."""
        toc_items = []
        for dm_ref in dm_refs:
            title = dm_ref
            if dm_ref in dm_contents:
                dm_xml = dm_contents[dm_ref]
                if isinstance(dm_xml, str):
                    try:
                        root = ET.fromstring(dm_xml)
                        title = self._find_element_text(root, "techName", dm_ref)
                    except:
                        pass
                else:
                    title = self._find_element_text(dm_xml, "techName", dm_ref)
            
            filename = self._sanitize_filename(dm_ref) + ".html"
            toc_items.append(f'<li><a href="{filename}">{self._escape_html(title)}</a></li>')
        
        body = f'''
        <div class="index-page">
            <h1>{self._escape_html(pm_title)}</h1>
            <nav class="toc">
                <h2>Table of Contents</h2>
                <ul>{"".join(toc_items)}</ul>
            </nav>
            <footer>
                <p>Contract: {self.contract_id} | Baseline: {self.baseline_ref}</p>
            </footer>
        </div>
        '''
        
        return self._build_html_document(pm_title, body, options)
    
    def _generate_dm_navigation(self, current_dm: str, all_dms: List[str]) -> str:
        """Generate navigation bar for DM page."""
        nav_items = ['<li><a href="index.html">← Index</a></li>']
        
        try:
            idx = all_dms.index(current_dm)
            if idx > 0:
                prev_file = self._sanitize_filename(all_dms[idx - 1]) + ".html"
                nav_items.append(f'<li><a href="{prev_file}">← Previous</a></li>')
            if idx < len(all_dms) - 1:
                next_file = self._sanitize_filename(all_dms[idx + 1]) + ".html"
                nav_items.append(f'<li><a href="{next_file}">Next →</a></li>')
        except ValueError:
            pass
        
        return f'<nav class="navigation"><ul>{"".join(nav_items)}</ul></nav>'
    
    def _generate_css(self, options: HTMLRenderOptions) -> str:
        """Generate CSS stylesheet."""
        return f'''
/* S1000D HTML Renderer CSS */
/* Contract: {self.contract_id} */

:root {{
    --primary-color: {options.primary_color};
    --secondary-color: {options.secondary_color};
    --accent-color: {options.accent_color};
    --warning-color: {options.warning_color};
    --font-family: {options.font_family};
    --base-font-size: {options.base_font_size};
}}

* {{ box-sizing: border-box; }}

body {{
    font-family: var(--font-family);
    font-size: var(--base-font-size);
    line-height: 1.6;
    color: #333;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    background-color: #fff;
}}

.data-module {{ margin: 20px 0; }}

.dm-title {{
    font-size: 2em;
    font-weight: bold;
    color: var(--primary-color);
    border-bottom: 3px solid var(--primary-color);
    padding-bottom: 0.3em;
    margin-bottom: 0.5em;
}}

.dm-subtitle {{
    font-size: 1.2em;
    color: var(--secondary-color);
    margin-bottom: 1.5em;
}}

.title {{
    font-size: 1.5em;
    font-weight: bold;
    margin-top: 1.5em;
    margin-bottom: 0.8em;
}}

.para {{
    margin: 1em 0;
    text-align: justify;
}}

/* Alerts */
.alert {{
    display: flex;
    padding: 15px;
    margin: 20px 0;
    border-left: 5px solid;
    border-radius: 4px;
}}

.alert-warning {{ background-color: #fff3cd; border-color: #ff6600; }}
.alert-caution {{ background-color: #fff8dc; border-color: #ffa500; }}
.alert-note {{ background-color: #e7f3ff; border-color: var(--primary-color); }}

.alert-icon {{ font-size: 24px; margin-right: 15px; }}
.alert-content {{ flex: 1; }}
.alert-content strong {{ display: block; margin-bottom: 8px; }}

/* Tables */
.table {{
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}}

.table caption {{
    font-weight: bold;
    text-align: left;
    padding: 10px;
    background-color: #f5f5f5;
}}

.table th, .table td {{
    border: 1px solid #ddd;
    padding: 10px;
    text-align: left;
}}

.table th {{ background-color: #f0f0f0; font-weight: bold; }}
.table tr:nth-child(even) {{ background-color: #f9f9f9; }}

/* Figures */
.figure {{
    margin: 20px 0;
    text-align: center;
}}

.figure-img {{
    max-width: 100%;
    height: auto;
    border: 1px solid #ddd;
}}

figcaption {{
    margin-top: 10px;
    font-style: italic;
    color: var(--secondary-color);
}}

/* Lists */
.list {{ margin: 12px 0; padding-left: 24px; }}
.step {{ margin: 0.5em 0; line-height: 1.8; }}

/* Navigation */
.navigation {{
    background-color: #f5f5f5;
    padding: 15px;
    margin-bottom: 20px;
    border-radius: 4px;
}}

.navigation ul {{
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    gap: 15px;
}}

.navigation a {{
    color: var(--primary-color);
    text-decoration: none;
}}

.navigation a:hover {{ text-decoration: underline; }}

/* Links */
.internal-ref, .external-ref {{
    color: var(--primary-color);
    text-decoration: none;
    border-bottom: 1px dotted var(--primary-color);
}}

.internal-ref:hover {{ text-decoration: underline; }}

/* Index page */
.index-page {{ padding: 20px; }}
.toc ul {{ list-style: none; padding: 0; }}
.toc li {{ margin: 10px 0; }}
.toc a {{ font-size: 1.1em; }}

/* Responsive */
@media (max-width: 768px) {{
    body {{ padding: 10px; font-size: 14px; }}
    .dm-title {{ font-size: 1.5em; }}
    .navigation ul {{ flex-direction: column; gap: 10px; }}
}}

/* Print */
@media print {{
    body {{ max-width: 100%; }}
    .navigation {{ display: none; }}
    .alert {{ page-break-inside: avoid; }}
}}

/* Dark mode */
@media (prefers-color-scheme: dark) {{
    body {{ background-color: #1e1e1e; color: #e0e0e0; }}
    .dm-title {{ color: #6ba3ff; border-color: #6ba3ff; }}
    .table td, .table th {{ border-color: #444; }}
    .table tr:nth-child(even) {{ background-color: #2a2a2a; }}
}}
'''
    
    def _generate_javascript(self, options: HTMLRenderOptions) -> str:
        """Generate JavaScript for interactive features."""
        return '''
/* S1000D HTML Renderer JavaScript */

document.addEventListener('DOMContentLoaded', function() {
    // Search functionality
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const query = e.target.value.toLowerCase();
            document.querySelectorAll('.para, .step').forEach(el => {
                el.style.display = el.textContent.toLowerCase().includes(query) ? '' : 'none';
            });
        });
    }
    
    // Smooth scroll for internal refs
    document.querySelectorAll('.internal-ref').forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href').substring(1);
            const target = document.getElementById(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // Print button
    const printBtn = document.getElementById('btn-print');
    if (printBtn) {
        printBtn.addEventListener('click', () => window.print());
    }
});
'''
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get rendering statistics."""
        return {
            "contract_id": self.contract_id,
            "render_count": self._render_count,
            "cross_refs_count": len(self._cross_refs),
        }


# =============================================================================
# IETP PACKAGER
# =============================================================================


class IETPPackager(BaseRenderer):
    """
    IETP Packager.
    
    Packages validated S1000D content into Interactive Electronic Technical
    Publication (IETP) format for deployment to viewing systems.
    
    Generates:
        - Complete IETP container with all DMs
        - Viewer configuration
        - Search indexes
        - Cross-reference maps
        - Graphics and multimedia integration
    
    Operates exclusively under ASIT contract authority.
    
    Example:
        >>> packager = IETPPackager(
        ...     contract=contract,
        ...     config={"title": "AMM", "enable_search": True}
        ... )
        >>> result = packager.package_publication(
        ...     pm_xml, dm_contents, Path("output/AMM_IETP")
        ... )
    """
    
    def __init__(
        self,
        contract: Dict[str, Any],
        config: Dict[str, Any],
        context: Optional[ExecutionContext] = None
    ):
        super().__init__(contract, config, context)
        
        # Parse IETP config
        self.ietp_config = IETPConfig(
            title=config.get("title", "Technical Publication"),
            version=config.get("version", "1.0.0"),
            language=config.get("language", "en-US"),
            viewer_type=ViewerType(config.get("viewer_type", "web")),
            enable_search=config.get("enable_search", True),
            enable_bookmarks=config.get("enable_bookmarks", True),
            enable_annotations=config.get("enable_annotations", False),
            enable_print=config.get("enable_print", True),
            enable_offline=config.get("enable_offline", True),
            applicability_filtering=config.get("applicability_filtering", True),
            cross_reference_resolution=config.get("cross_reference_resolution", True),
        )
        
        # Tracking
        self._dm_refs: Set[str] = set()
        self._icn_refs: Set[str] = set()
        
        self.logger.info(
            f"IETPPackager initialized: contract={self.contract_id}, "
            f"viewer={self.ietp_config.viewer_type.value}"
        )
    
    def render(
        self, 
        content: Any, 
        output_path: Optional[Path] = None
    ) -> IETPPackageResult:
        """Render/package content (not typically used directly)."""
        raise NotImplementedError("Use package_publication() for IETP packaging")
    
    def package_publication(
        self,
        pm_content: Union[str, ET.Element],
        dm_contents: Dict[str, Union[str, ET.Element]],
        output_path: Path,
        package_format: IETPFormat = IETPFormat.DIRECTORY,
        graphics_dir: Optional[Path] = None,
        multimedia_dir: Optional[Path] = None,
    ) -> IETPPackageResult:
        """
        Package a publication module into IETP format.
        
        Args:
            pm_content: Publication Module XML
            dm_contents: Dictionary of DM codes to DM XML content
            output_path: Output path for IETP package
            package_format: Package format (directory, zip, csp)
            graphics_dir: Directory containing graphics files
            multimedia_dir: Directory containing multimedia files
            
        Returns:
            IETPPackageResult
        """
        start_time = datetime.now()
        result = IETPPackageResult(success=False, package_format=package_format)
        
        # Parse PM
        try:
            if isinstance(pm_content, str):
                pm_root = ET.fromstring(pm_content)
            else:
                pm_root = pm_content
        except ET.ParseError as e:
            result.errors.append(f"PM parse error: {e}")
            return result
        
        # Extract metadata
        pm_title = self._extract_pm_title(pm_root)
        dm_refs = self._extract_dm_refs(pm_root)
        self.ietp_config.title = pm_title
        result.dm_count = len(dm_refs)
        
        # Setup package directory
        output_path = Path(output_path)
        
        try:
            # Create temporary directory for archive formats
            if package_format in [IETPFormat.ZIP, IETPFormat.CSP]:
                import tempfile
                temp_dir = Path(tempfile.mkdtemp())
                package_dir = temp_dir / "ietp_package"
            else:
                package_dir = output_path
                temp_dir = None
            
            package_dir.mkdir(parents=True, exist_ok=True)
            
            # Create directory structure
            self._create_structure(package_dir)
            
            # Package PM
            pm_xml_str = ET.tostring(pm_root, encoding='unicode')
            (package_dir / "content" / "publication.xml").write_text(pm_xml_str, encoding='utf-8')
            
            # Package DMs
            for dm_ref in dm_refs:
                if dm_ref in dm_contents:
                    try:
                        dm_xml = dm_contents[dm_ref]
                        if isinstance(dm_xml, str):
                            dm_root = ET.fromstring(dm_xml)
                        else:
                            dm_root = dm_xml
                        
                        # Save DM
                        filename = self._sanitize_filename(dm_ref) + ".xml"
                        dm_xml_str = ET.tostring(dm_root, encoding='unicode')
                        (package_dir / "content" / filename).write_text(dm_xml_str, encoding='utf-8')
                        
                        # Extract ICN refs
                        for graphic in self._find_all_elements(dm_root, "graphic"):
                            icn = graphic.get("infoEntityIdent", "")
                            if icn:
                                self._icn_refs.add(icn)
                                
                    except Exception as e:
                        result.warnings.append(f"Failed to package DM {dm_ref}: {e}")
                else:
                    result.warnings.append(f"DM not found: {dm_ref}")
            
            # Copy graphics
            if graphics_dir and graphics_dir.exists():
                result.icn_count = self._copy_files(
                    graphics_dir,
                    package_dir / "graphics",
                    ['.png', '.jpg', '.jpeg', '.svg', '.cgm', '.tif', '.tiff']
                )
            
            # Copy multimedia
            if multimedia_dir and multimedia_dir.exists():
                result.multimedia_count = self._copy_files(
                    multimedia_dir,
                    package_dir / "multimedia",
                    ['.mp4', '.webm', '.mp3', '.wav', '.pdf']
                )
            
            # Generate configuration
            self._generate_config(package_dir, dm_refs)
            
            # Generate viewer
            self._generate_viewer(package_dir)
            
            # Generate search index
            if self.ietp_config.enable_search:
                self._generate_search_index(package_dir, dm_refs, dm_contents)
            
            # Generate cross-reference map
            if self.ietp_config.cross_reference_resolution:
                self._generate_xref_map(package_dir, dm_contents)
            
            # Calculate size
            result.total_size_bytes = sum(
                f.stat().st_size for f in package_dir.rglob('*') if f.is_file()
            )
            
            # Create archive if needed
            if package_format == IETPFormat.ZIP:
                zip_path = output_path.with_suffix('.zip')
                self._create_archive(package_dir, zip_path)
                result.output_path = zip_path
                if temp_dir:
                    shutil.rmtree(temp_dir)
            elif package_format == IETPFormat.CSP:
                csp_path = output_path.with_suffix('.csp')
                self._create_archive(package_dir, csp_path)
                result.output_path = csp_path
                if temp_dir:
                    shutil.rmtree(temp_dir)
            else:
                result.output_path = package_dir
            
            result.success = True
            
        except Exception as e:
            result.errors.append(f"Package error: {e}")
            return result
        
        # Update stats
        self._render_count += 1
        self._dm_refs.update(dm_refs)
        result.package_time_seconds = (datetime.now() - start_time).total_seconds()
        
        return result
    
    def _create_structure(self, package_dir: Path) -> None:
        """Create IETP directory structure."""
        for subdir in ["content", "graphics", "multimedia", "css", "js", "index", "config"]:
            (package_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    def _copy_files(
        self, 
        source_dir: Path, 
        target_dir: Path, 
        extensions: List[str]
    ) -> int:
        """Copy files with specified extensions."""
        count = 0
        for ext in extensions:
            for file_path in source_dir.glob(f"**/*{ext}"):
                try:
                    shutil.copy2(file_path, target_dir / file_path.name)
                    count += 1
                except Exception as e:
                    self.logger.warning(f"Failed to copy {file_path}: {e}")
        return count
    
    def _generate_config(self, package_dir: Path, dm_refs: List[str]) -> None:
        """Generate IETP configuration."""
        config = {
            "ietp": {
                "version": "1.0",
                "title": self.ietp_config.title,
                "publication_version": self.ietp_config.version,
                "language": self.ietp_config.language,
                "security": self.ietp_config.security_level,
                "contract_id": self.contract_id,
                "baseline": self.baseline_ref,
                "generated": datetime.now().isoformat(),
            },
            "viewer": {
                "type": self.ietp_config.viewer_type.value,
                "features": {
                    "search": self.ietp_config.enable_search,
                    "bookmarks": self.ietp_config.enable_bookmarks,
                    "annotations": self.ietp_config.enable_annotations,
                    "print": self.ietp_config.enable_print,
                    "offline": self.ietp_config.enable_offline,
                }
            },
            "content": {
                "publication": "content/publication.xml",
                "data_modules": [
                    f"content/{self._sanitize_filename(dm)}.xml" for dm in dm_refs
                ]
            }
        }
        
        (package_dir / "config" / "ietp_config.json").write_text(
            json.dumps(config, indent=2), encoding='utf-8'
        )
    
    def _generate_viewer(self, package_dir: Path) -> None:
        """Generate IETP viewer files."""
        # Index HTML
        index_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self._escape_html(self.ietp_config.title)}</title>
    <link rel="stylesheet" href="css/viewer.css">
</head>
<body>
    <div id="ietp-viewer">
        <header>
            <h1>{self._escape_html(self.ietp_config.title)}</h1>
            <nav id="toolbar">
                <button id="btn-home">Home</button>
                <button id="btn-toc">TOC</button>
                <button id="btn-search">Search</button>
                <button id="btn-print">Print</button>
            </nav>
        </header>
        <div id="container">
            <aside id="sidebar"><div id="toc"></div></aside>
            <main id="content"><div id="viewer-frame"></div></main>
        </div>
        <footer>
            <p>Contract: {self.contract_id} | Baseline: {self.baseline_ref}</p>
        </footer>
    </div>
    <script src="js/viewer.js"></script>
</body>
</html>'''
        
        (package_dir / "index.html").write_text(index_html, encoding='utf-8')
        
        # CSS
        viewer_css = '''
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: Arial, sans-serif; }
#ietp-viewer { display: flex; flex-direction: column; height: 100vh; }
header { background: #2c3e50; color: white; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; }
header h1 { font-size: 20px; }
#toolbar button { background: #34495e; color: white; border: none; padding: 8px 15px; margin-left: 10px; cursor: pointer; border-radius: 4px; }
#toolbar button:hover { background: #415b76; }
#container { display: flex; flex: 1; overflow: hidden; }
#sidebar { width: 300px; background: #ecf0f1; border-right: 1px solid #bdc3c7; overflow-y: auto; padding: 20px; }
#content { flex: 1; overflow-y: auto; padding: 30px; }
#viewer-frame { max-width: 1200px; margin: 0 auto; }
footer { background: #ecf0f1; border-top: 1px solid #bdc3c7; padding: 10px; text-align: center; font-size: 12px; }
@media (max-width: 768px) { #container { flex-direction: column; } #sidebar { width: 100%; max-height: 200px; } }
'''
        (package_dir / "css" / "viewer.css").write_text(viewer_css, encoding='utf-8')
        
        # JavaScript
        viewer_js = '''
class IETPViewer {
    constructor() { this.config = null; this.init(); }
    async init() {
        this.config = await fetch('config/ietp_config.json').then(r => r.json());
        this.buildTOC();
        this.setupEvents();
        if (this.config.content.data_modules.length > 0) this.loadDM(this.config.content.data_modules[0]);
    }
    buildTOC() {
        const toc = document.getElementById('toc');
        const ul = document.createElement('ul');
        this.config.content.data_modules.forEach(dm => {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = '#';
            a.textContent = dm.replace('content/', '').replace('.xml', '');
            a.onclick = e => { e.preventDefault(); this.loadDM(dm); };
            li.appendChild(a);
            ul.appendChild(li);
        });
        toc.appendChild(ul);
    }
    async loadDM(path) {
        try {
            const xml = await fetch(path).then(r => r.text());
            const doc = new DOMParser().parseFromString(xml, 'text/xml');
            this.renderDM(doc);
        } catch(e) { console.error('Load error:', e); }
    }
    renderDM(doc) {
        const frame = document.getElementById('viewer-frame');
        const title = doc.querySelector('techName')?.textContent || 'Data Module';
        let html = '<h1>' + title + '</h1>';
        const content = doc.querySelector('content');
        if (content) html += this.renderElement(content);
        frame.innerHTML = html;
    }
    renderElement(el) {
        let html = '';
        for (const child of el.children) {
            const tag = child.tagName.toLowerCase();
            if (tag === 'para') html += '<p>' + child.textContent + '</p>';
            else if (tag === 'title') html += '<h2>' + child.textContent + '</h2>';
            else html += this.renderElement(child);
        }
        return html;
    }
    setupEvents() {
        document.getElementById('btn-home').onclick = () => location.reload();
        document.getElementById('btn-toc').onclick = () => {
            const s = document.getElementById('sidebar');
            s.style.display = s.style.display === 'none' ? 'block' : 'none';
        };
        document.getElementById('btn-print').onclick = () => window.print();
        document.getElementById('btn-search').onclick = () => alert('Search - TBD');
    }
}
document.addEventListener('DOMContentLoaded', () => new IETPViewer());
'''
        (package_dir / "js" / "viewer.js").write_text(viewer_js, encoding='utf-8')
    
    def _generate_search_index(
        self,
        package_dir: Path,
        dm_refs: List[str],
        dm_contents: Dict[str, Union[str, ET.Element]]
    ) -> None:
        """Generate search index."""
        entries = []
        for dm_ref in dm_refs:
            if dm_ref in dm_contents:
                try:
                    dm_xml = dm_contents[dm_ref]
                    if isinstance(dm_xml, str):
                        root = ET.fromstring(dm_xml)
                    else:
                        root = dm_xml
                    
                    title = self._find_element_text(root, "techName", dm_ref)
                    text = " ".join(el.text.strip() for el in root.iter() if el.text)
                    
                    entries.append({
                        "dm_code": dm_ref,
                        "title": title,
                        "content_preview": text[:200]
                    })
                except:
                    pass
        
        (package_dir / "index" / "search_index.json").write_text(
            json.dumps(entries, indent=2), encoding='utf-8'
        )
    
    def _generate_xref_map(
        self,
        package_dir: Path,
        dm_contents: Dict[str, Union[str, ET.Element]]
    ) -> None:
        """Generate cross-reference map."""
        xref_map = {}
        for dm_code, dm_xml in dm_contents.items():
            try:
                if isinstance(dm_xml, str):
                    root = ET.fromstring(dm_xml)
                else:
                    root = dm_xml
                
                refs = []
                for ref in self._find_all_elements(root, "internalRef"):
                    ref_id = ref.get("internalRefId", "")
                    if ref_id:
                        refs.append({"type": "internal", "target": ref_id})
                
                for ref in self._find_all_elements(root, "dmRef"):
                    dm_code_el = self._find_element(ref, "dmCode")
                    if dm_code_el:
                        refs.append({"type": "dm", "target": self._build_dmc_string(dm_code_el)})
                
                if refs:
                    xref_map[dm_code] = refs
            except:
                pass
        
        (package_dir / "index" / "xref_map.json").write_text(
            json.dumps(xref_map, indent=2), encoding='utf-8'
        )
    
    def _create_archive(self, source_dir: Path, archive_path: Path) -> None:
        """Create ZIP archive."""
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in source_dir.rglob('*'):
                if file_path.is_file():
                    zipf.write(file_path, file_path.relative_to(source_dir))
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get packaging statistics."""
        return {
            "contract_id": self.contract_id,
            "package_count": self._render_count,
            "total_dms": len(self._dm_refs),
            "total_icns": len(self._icn_refs),
        }


# =============================================================================
# COMBINED RENDERER
# =============================================================================


class CombinedRenderer:
    """
    Combined renderer providing unified interface for all output formats.
    
    Provides a single entry point for PDF, HTML, and IETP rendering
    under ASIT contract authority.
    
    Example:
        >>> renderer = CombinedRenderer(contract, config)
        >>> pdf_result = renderer.render_to_pdf(dm_xml, Path("output.pdf"))
        >>> html_result = renderer.render_to_html(dm_xml, Path("output.html"))
        >>> ietp_result = renderer.package_ietp(pm_xml, dm_dict, Path("output_ietp"))
    """
    
    def __init__(
        self,
        contract: Dict[str, Any],
        config: RendererConfig,
        context: Optional[ExecutionContext] = None
    ):
        self.contract = contract
        self.config = config
        self.context = context
        
        self.pdf_renderer = PDFRenderer(contract, config.pdf.__dict__, context)
        self.html_renderer = HTMLRenderer(contract, config.html.__dict__, context)
        self.ietp_packager = IETPPackager(contract, config.ietp.__dict__, context)
    
    def render_to_pdf(
        self,
        content: Union[str, ET.Element],
        output_path: Optional[Path] = None
    ) -> PDFRenderResult:
        """Render content to PDF."""
        return self.pdf_renderer.render_dm(content, output_path)
    
    def render_to_html(
        self,
        content: Union[str, ET.Element],
        output_path: Optional[Path] = None
    ) -> HTMLRenderResult:
        """Render content to HTML."""
        return self.html_renderer.render_dm(content, output_path)
    
    def package_ietp(
        self,
        pm_content: Union[str, ET.Element],
        dm_contents: Dict[str, Union[str, ET.Element]],
        output_path: Path,
        package_format: IETPFormat = IETPFormat.DIRECTORY
    ) -> IETPPackageResult:
        """Package content as IETP."""
        return self.ietp_packager.package_publication(
            pm_content, dm_contents, output_path, package_format
        )


# =============================================================================
# MODULE EXPORTS
# =============================================================================


__all__ = [
    # Enumerations
    "PageSize",
    "PDFEngine",
    "HTMLVersion",
    "CSSFramework",
    "IETPFormat",
    "ViewerType",
    
    # Configuration
    "PDFRenderOptions",
    "HTMLRenderOptions",
    "IETPConfig",
    "RendererConfig",
    
    # Results
    "PDFRenderResult",
    "HTMLRenderResult",
    "IETPPackageResult",
    
    # Renderers
    "BaseRenderer",
    "PDFRenderer",
    "HTMLRenderer",
    "IETPPackager",
    "CombinedRenderer",
]
