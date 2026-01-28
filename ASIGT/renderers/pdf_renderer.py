# =============================================================================
# ASIGT PDF Renderer
# S1000D to PDF conversion
# Version: 2.0.0
# =============================================================================
"""
PDF Renderer

Renders S1000D Data Modules and Publication Modules to PDF format.
Generates publication-ready PDF documents with:
- Table of contents
- List of effective pages
- Page numbering
- Headers/footers
- Figures and graphics
- Cross-references

Operates exclusively under ASIT contract authority.
"""

from __future__ import annotations

import io
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from xml.etree import ElementTree as ET

logger = logging.getLogger(__name__)


class PageSize(Enum):
    """Standard page sizes."""
    A4 = "A4"           # 210 × 297 mm
    LETTER = "Letter"   # 8.5 × 11 inches
    LEGAL = "Legal"     # 8.5 × 14 inches
    A5 = "A5"           # 148 × 210 mm


class PDFEngine(Enum):
    """PDF generation engines."""
    WEASYPRINT = "weasyprint"   # HTML/CSS to PDF
    REPORTLAB = "reportlab"     # Direct PDF generation
    XSLT = "xslt"              # XSLT transformation + FOP


@dataclass
class PDFRenderOptions:
    """PDF rendering options."""
    page_size: PageSize = PageSize.A4
    include_toc: bool = True              # Table of contents
    include_lep: bool = True              # List of effective pages
    include_bookmarks: bool = True        # PDF bookmarks
    include_page_numbers: bool = True
    watermark: Optional[str] = None       # Watermark text
    header_text: Optional[str] = None
    footer_text: Optional[str] = None
    font_family: str = "Arial"
    font_size: int = 10
    margin_top_mm: float = 20.0
    margin_bottom_mm: float = 20.0
    margin_left_mm: float = 20.0
    margin_right_mm: float = 20.0
    graphics_dpi: int = 150              # Graphics resolution


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
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "output_path": str(self.output_path) if self.output_path else None,
            "page_count": self.page_count,
            "file_size_bytes": self.file_size_bytes,
            "file_size_mb": round(self.file_size_bytes / (1024 * 1024), 2),
            "dm_codes": self.dm_codes,
            "errors": self.errors,
            "warnings": self.warnings,
            "rendered_at": self.rendered_at,
            "render_time_seconds": self.render_time_seconds,
        }


class PDFRenderer:
    """
    S1000D PDF Renderer.
    
    Converts validated S1000D XML to publication-ready PDF documents.
    Operates under ASIT contract authority.
    
    Attributes:
        contract: ASIT transformation contract
        config: Renderer configuration
        engine: PDF generation engine
        
    Example:
        >>> renderer = PDFRenderer(contract=contract, config=config)
        >>> result = renderer.render_dm(
        ...     dm_content=dm_xml,
        ...     output_path="AMM_28-10-00.pdf",
        ... )
    """
    
    def __init__(
        self,
        contract: Dict[str, Any],
        config: Dict[str, Any],
        engine: PDFEngine = PDFEngine.WEASYPRINT,
    ):
        """
        Initialize PDF Renderer.
        
        Args:
            contract: ASIT transformation contract (required)
            config: Renderer configuration
            engine: PDF generation engine to use
            
        Raises:
            ValueError: If contract is missing
        """
        if not contract:
            raise ValueError("ASIT contract is required for PDF rendering")
        
        self.contract = contract
        self.config = config
        self.engine = engine
        
        # Contract parameters
        self.contract_id = contract.get("id", "UNKNOWN")
        self.baseline_ref = contract.get("source", {}).get("baseline", "UNKNOWN")
        
        # Default options
        self.default_options = PDFRenderOptions(
            page_size=PageSize(config.get("page_size", "A4")),
            include_toc=config.get("include_toc", True),
            include_lep=config.get("include_lep", True),
            header_text=config.get("header_text"),
            footer_text=config.get("footer_text"),
        )
        
        # Statistics
        self._render_count = 0
        self._total_pages = 0
        
        # Load engine
        self._engine_available = False
        self._load_engine()
        
        logger.info(
            f"PDFRenderer initialized: contract={self.contract_id}, "
            f"engine={self.engine.value}, available={self._engine_available}"
        )
    
    def render_dm(
        self,
        dm_content: Union[str, ET.Element],
        output_path: Optional[Path] = None,
        options: Optional[PDFRenderOptions] = None,
    ) -> PDFRenderResult:
        """
        Render a Data Module to PDF.
        
        Args:
            dm_content: S1000D XML content
            output_path: Output PDF path (optional)
            options: Rendering options
            
        Returns:
            PDFRenderResult
        """
        start_time = datetime.now()
        options = options or self.default_options
        
        result = PDFRenderResult(success=False)
        
        # Parse XML
        try:
            if isinstance(dm_content, str):
                root = ET.fromstring(dm_content)
            else:
                root = dm_content
        except Exception as e:
            result.errors.append(f"Failed to parse XML: {e}")
            return result
        
        # Extract DM code
        dm_code = self._extract_dm_code(root)
        result.dm_codes = [dm_code]
        
        # Convert to HTML
        try:
            html = self._dm_to_html(root, options)
        except Exception as e:
            result.errors.append(f"Failed to convert to HTML: {e}")
            return result
        
        # Render to PDF
        try:
            pdf_data = self._html_to_pdf(html, options)
            result.pdf_data = pdf_data
            result.file_size_bytes = len(pdf_data)
            result.success = True
            
            # Estimate page count (rough approximation)
            result.page_count = max(1, len(pdf_data) // 10000)
            
        except Exception as e:
            result.errors.append(f"Failed to generate PDF: {e}")
            return result
        
        # Write to file if path provided
        if output_path and result.success:
            try:
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(pdf_data)
                result.output_path = output_path
            except Exception as e:
                result.warnings.append(f"Failed to write to file: {e}")
        
        # Update statistics
        self._render_count += 1
        self._total_pages += result.page_count
        
        # Calculate render time
        end_time = datetime.now()
        result.render_time_seconds = (end_time - start_time).total_seconds()
        
        return result
    
    def render_pm(
        self,
        pm_content: Union[str, ET.Element],
        dm_contents: Dict[str, Union[str, ET.Element]],
        output_path: Optional[Path] = None,
        options: Optional[PDFRenderOptions] = None,
    ) -> PDFRenderResult:
        """
        Render a Publication Module to PDF.
        
        Args:
            pm_content: Publication Module XML
            dm_contents: Dictionary of DM codes to DM XML content
            output_path: Output PDF path
            options: Rendering options
            
        Returns:
            PDFRenderResult
        """
        start_time = datetime.now()
        options = options or self.default_options
        
        result = PDFRenderResult(success=False)
        
        # Parse PM XML
        try:
            if isinstance(pm_content, str):
                pm_root = ET.fromstring(pm_content)
            else:
                pm_root = pm_content
        except Exception as e:
            result.errors.append(f"Failed to parse PM XML: {e}")
            return result
        
        # Extract PM info
        pm_title = self._extract_pm_title(pm_root)
        
        # Get DM references from PM
        dm_refs = self._extract_dm_refs(pm_root)
        result.dm_codes = dm_refs
        
        # Build combined HTML
        html_parts = [self._generate_cover_page(pm_title, options)]
        
        if options.include_toc:
            html_parts.append(self._generate_toc(pm_root, dm_refs))
        
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
                    
                    dm_html = self._dm_to_html(dm_root, options)
                    html_parts.append(dm_html)
                except Exception as e:
                    result.warnings.append(f"Failed to render DM {dm_ref}: {e}")
            else:
                result.warnings.append(f"DM content not found: {dm_ref}")
        
        # Combine HTML
        full_html = self._combine_html_parts(html_parts, pm_title, options)
        
        # Render to PDF
        try:
            pdf_data = self._html_to_pdf(full_html, options)
            result.pdf_data = pdf_data
            result.file_size_bytes = len(pdf_data)
            result.success = True
            
            # Estimate page count
            result.page_count = max(1, len(pdf_data) // 10000)
            
        except Exception as e:
            result.errors.append(f"Failed to generate PDF: {e}")
            return result
        
        # Write to file
        if output_path and result.success:
            try:
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(pdf_data)
                result.output_path = output_path
            except Exception as e:
                result.warnings.append(f"Failed to write to file: {e}")
        
        # Update statistics
        self._render_count += 1
        self._total_pages += result.page_count
        
        # Calculate render time
        end_time = datetime.now()
        result.render_time_seconds = (end_time - start_time).total_seconds()
        
        return result
    
    def _load_engine(self) -> None:
        """Load the PDF generation engine."""
        if self.engine == PDFEngine.WEASYPRINT:
            try:
                import weasyprint
                self._weasyprint = weasyprint
                self._engine_available = True
            except ImportError:
                logger.warning(
                    "WeasyPrint not available. "
                    "Install with: pip install weasyprint"
                )
        elif self.engine == PDFEngine.REPORTLAB:
            try:
                import reportlab
                self._reportlab = reportlab
                self._engine_available = True
            except ImportError:
                logger.warning(
                    "ReportLab not available. "
                    "Install with: pip install reportlab"
                )
        else:
            logger.warning(f"Engine {self.engine.value} not implemented")
    
    def _dm_to_html(
        self,
        dm_root: ET.Element,
        options: PDFRenderOptions,
    ) -> str:
        """Convert Data Module XML to HTML."""
        html_parts = ['<div class="data-module">']
        
        # Extract title
        tech_name = self._find_element_text(dm_root, "techName", "Data Module")
        html_parts.append(f'<h1>{tech_name}</h1>')
        
        # Process content
        content = self._find_element(dm_root, "content")
        if content is not None:
            content_html = self._element_to_html(content)
            html_parts.append(content_html)
        
        html_parts.append('</div>')
        return "\n".join(html_parts)
    
    def _element_to_html(self, element: ET.Element) -> str:
        """Convert XML element to HTML recursively."""
        local_name = element.tag.split("}")[-1] if "}" in element.tag else element.tag
        
        # Element mapping
        html_map = {
            "para": "p",
            "title": "h2",
            "proceduralStep": "li",
            "warning": "div",
            "caution": "div",
            "note": "div",
            "table": "table",
            "row": "tr",
            "entry": "td",
        }
        
        html_tag = html_map.get(local_name, "div")
        
        # Build HTML
        attrs = ""
        if local_name in ["warning", "caution", "note"]:
            attrs = f' class="{local_name}"'
        
        # Get text and children
        text = element.text or ""
        children_html = "".join(self._element_to_html(child) for child in element)
        tail = element.tail or ""
        
        return f"<{html_tag}{attrs}>{text}{children_html}</{html_tag}>{tail}"
    
    def _html_to_pdf(
        self,
        html: str,
        options: PDFRenderOptions,
    ) -> bytes:
        """Convert HTML to PDF using selected engine."""
        if not self._engine_available:
            raise RuntimeError(
                f"PDF engine {self.engine.value} is not available. "
                "Please install required dependencies."
            )
        
        # Add CSS styling
        styled_html = self._add_css(html, options)
        
        if self.engine == PDFEngine.WEASYPRINT:
            return self._weasyprint_render(styled_html, options)
        elif self.engine == PDFEngine.REPORTLAB:
            return self._reportlab_render(styled_html, options)
        else:
            raise NotImplementedError(f"Engine {self.engine.value} not implemented")
    
    def _weasyprint_render(
        self,
        html: str,
        options: PDFRenderOptions,
    ) -> bytes:
        """Render PDF using WeasyPrint."""
        pdf_bytes = self._weasyprint.HTML(string=html).write_pdf()
        return pdf_bytes
    
    def _reportlab_render(
        self,
        html: str,
        options: PDFRenderOptions,
    ) -> bytes:
        """Render PDF using ReportLab."""
        # This is a simplified placeholder
        # Full implementation would use reportlab's document building API
        raise NotImplementedError("ReportLab renderer not yet implemented")
    
    def _add_css(
        self,
        html: str,
        options: PDFRenderOptions,
    ) -> str:
        """Add CSS styling to HTML."""
        css = f"""
        <style>
        @page {{
            size: {options.page_size.value};
            margin: {options.margin_top_mm}mm {options.margin_right_mm}mm 
                    {options.margin_bottom_mm}mm {options.margin_left_mm}mm;
            
            @top-center {{
                content: "{options.header_text or ''}";
                font-size: 9pt;
                color: #666;
            }}
            
            @bottom-center {{
                content: "{options.footer_text or ''} - Page " counter(page) " of " counter(pages);
                font-size: 9pt;
                color: #666;
            }}
        }}
        
        body {{
            font-family: {options.font_family}, sans-serif;
            font-size: {options.font_size}pt;
            line-height: 1.4;
            color: #000;
        }}
        
        h1 {{
            font-size: 18pt;
            font-weight: bold;
            margin-top: 20pt;
            margin-bottom: 12pt;
            page-break-after: avoid;
        }}
        
        h2 {{
            font-size: 14pt;
            font-weight: bold;
            margin-top: 14pt;
            margin-bottom: 8pt;
            page-break-after: avoid;
        }}
        
        p {{
            margin-top: 6pt;
            margin-bottom: 6pt;
            text-align: justify;
        }}
        
        .warning {{
            border-left: 4px solid #ff0000;
            background-color: #fff0f0;
            padding: 10pt;
            margin: 10pt 0;
            font-weight: bold;
        }}
        
        .caution {{
            border-left: 4px solid #ffa500;
            background-color: #fff8f0;
            padding: 10pt;
            margin: 10pt 0;
        }}
        
        .note {{
            border-left: 4px solid #0066cc;
            background-color: #f0f8ff;
            padding: 10pt;
            margin: 10pt 0;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 10pt 0;
        }}
        
        th, td {{
            border: 1pt solid #000;
            padding: 5pt;
            text-align: left;
        }}
        
        th {{
            background-color: #f0f0f0;
            font-weight: bold;
        }}
        
        .cover-page {{
            text-align: center;
            page-break-after: always;
            padding-top: 100pt;
        }}
        
        .toc {{
            page-break-after: always;
        }}
        
        .toc-entry {{
            margin-bottom: 6pt;
        }}
        </style>
        """
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    {css}
</head>
<body>
    {html}
</body>
</html>"""
    
    def _generate_cover_page(
        self,
        title: str,
        options: PDFRenderOptions,
    ) -> str:
        """Generate cover page HTML."""
        return f"""
        <div class="cover-page">
            <h1 style="font-size: 24pt; margin-bottom: 20pt;">{title}</h1>
            <p>Contract: {self.contract_id}</p>
            <p>Baseline: {self.baseline_ref}</p>
            <p>Generated: {datetime.now().strftime("%Y-%m-%d")}</p>
        </div>
        """
    
    def _generate_toc(
        self,
        pm_root: ET.Element,
        dm_refs: List[str],
    ) -> str:
        """Generate table of contents HTML."""
        html = ['<div class="toc">', '<h1>Table of Contents</h1>']
        
        for i, dm_ref in enumerate(dm_refs, 1):
            html.append(f'<div class="toc-entry">{i}. {dm_ref}</div>')
        
        html.append('</div>')
        return "\n".join(html)
    
    def _generate_lep(self, dm_refs: List[str]) -> str:
        """Generate list of effective pages HTML."""
        html = ['<div class="lep">', '<h1>List of Effective Pages</h1>']
        
        for dm_ref in dm_refs:
            html.append(f'<div>{dm_ref} - Rev 001</div>')
        
        html.append('</div>')
        return "\n".join(html)
    
    def _combine_html_parts(
        self,
        parts: List[str],
        title: str,
        options: PDFRenderOptions,
    ) -> str:
        """Combine HTML parts into single document."""
        return "\n".join(parts)
    
    def _extract_dm_code(self, root: ET.Element) -> str:
        """Extract DM code from XML."""
        dm_code = self._find_element(root, "dmCode")
        if dm_code is not None:
            # Build DMC string from attributes
            mic = dm_code.get("modelIdentCode", "")
            sys = dm_code.get("systemCode", "")
            info = dm_code.get("infoCode", "")
            return f"{mic}-{sys}-{info}" if mic else "UNKNOWN"
        return "UNKNOWN"
    
    def _extract_pm_title(self, root: ET.Element) -> str:
        """Extract PM title."""
        pm_title = self._find_element_text(root, "pmTitle", "Publication")
        return pm_title
    
    def _extract_dm_refs(self, root: ET.Element) -> List[str]:
        """Extract DM references from PM."""
        dm_refs = []
        for dm_ref in root.iter():
            local_name = dm_ref.tag.split("}")[-1] if "}" in dm_ref.tag else dm_ref.tag
            if local_name == "dmRef":
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
    
    def _find_element(
        self,
        root: ET.Element,
        name: str,
    ) -> Optional[ET.Element]:
        """Find element by local name."""
        for elem in root.iter():
            local_name = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
            if local_name == name:
                return elem
        return None
    
    def _find_element_text(
        self,
        root: ET.Element,
        name: str,
        default: str = "",
    ) -> str:
        """Find element text by local name."""
        elem = self._find_element(root, name)
        if elem is not None:
            return elem.text or default
        return default
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get rendering statistics."""
        return {
            "contract_id": self.contract_id,
            "engine": self.engine.value,
            "engine_available": self._engine_available,
            "render_count": self._render_count,
            "total_pages": self._total_pages,
        }
