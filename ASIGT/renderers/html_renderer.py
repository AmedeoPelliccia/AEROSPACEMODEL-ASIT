# =============================================================================
# ASIGT HTML Renderer
# S1000D to HTML conversion
# Version: 2.0.0
# =============================================================================
"""
HTML Renderer

Renders S1000D Data Modules and Publication Modules to HTML format.
Generates responsive HTML with CSS styling for:
- Web viewing
- IETP (Interactive Electronic Technical Publication) integration
- Offline viewer packages
- Preview/review workflows

Operates exclusively under ASIT contract authority.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union
from xml.etree import ElementTree as ET

logger = logging.getLogger(__name__)


class HTMLVersion(Enum):
    """HTML version standards."""
    HTML5 = "html5"
    XHTML = "xhtml"


class CSSFramework(Enum):
    """CSS frameworks."""
    CUSTOM = "custom"
    BOOTSTRAP = "bootstrap"
    TAILWIND = "tailwind"


@dataclass
class HTMLRenderOptions:
    """HTML rendering options."""
    html_version: HTMLVersion = HTMLVersion.HTML5
    css_framework: CSSFramework = CSSFramework.CUSTOM
    include_navigation: bool = True
    include_toc: bool = True
    include_breadcrumbs: bool = True
    include_search: bool = True
    responsive_design: bool = True
    dark_mode_support: bool = True
    inline_css: bool = False              # Inline vs external CSS
    include_javascript: bool = True       # Interactive features
    graphics_inline: bool = False         # Inline images as base64
    syntax_highlighting: bool = True      # For code examples
    print_friendly: bool = True          # Print stylesheet
    
    # Styling
    primary_color: str = "#0066cc"
    secondary_color: str = "#666666"
    warning_color: str = "#ff6600"
    font_family: str = "Arial, sans-serif"
    base_font_size: str = "16px"


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
            "file_size_kb": round(self.file_size_bytes / 1024, 2),
        }


class HTMLRenderer:
    """
    S1000D HTML Renderer.
    
    Converts validated S1000D XML to responsive HTML with CSS styling.
    Operates under ASIT contract authority.
    
    Attributes:
        contract: ASIT transformation contract
        config: Renderer configuration
        
    Example:
        >>> renderer = HTMLRenderer(contract=contract, config=config)
        >>> result = renderer.render_dm(
        ...     dm_content=dm_xml,
        ...     output_path="AMM_28-10-00.html",
        ... )
    """
    
    def __init__(
        self,
        contract: Dict[str, Any],
        config: Dict[str, Any],
    ):
        """
        Initialize HTML Renderer.
        
        Args:
            contract: ASIT transformation contract (required)
            config: Renderer configuration
            
        Raises:
            ValueError: If contract is missing
        """
        if not contract:
            raise ValueError("ASIT contract is required for HTML rendering")
        
        self.contract = contract
        self.config = config
        
        # Contract parameters
        self.contract_id = contract.get("id", "UNKNOWN")
        self.baseline_ref = contract.get("source", {}).get("baseline", "UNKNOWN")
        
        # Default options
        self.default_options = HTMLRenderOptions(
            html_version=HTMLVersion(config.get("html_version", "html5")),
            css_framework=CSSFramework(config.get("css_framework", "custom")),
            include_navigation=config.get("include_navigation", True),
            include_toc=config.get("include_toc", True),
            primary_color=config.get("primary_color", "#0066cc"),
        )
        
        # Statistics
        self._render_count = 0
        self._cross_refs: Set[str] = set()
        
        logger.info(
            f"HTMLRenderer initialized: contract={self.contract_id}, "
            f"version={self.default_options.html_version.value}"
        )
    
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
        options = options or self.default_options
        
        result = HTMLRenderResult(success=False)
        
        # Parse XML
        try:
            if isinstance(dm_content, str):
                root = ET.fromstring(dm_content)
            else:
                root = dm_content
        except Exception as e:
            result.errors.append(f"Failed to parse XML: {e}")
            return result
        
        # Extract DM code and metadata
        dm_code = self._extract_dm_code(root)
        result.dm_codes = [dm_code]
        
        dm_title = self._find_element_text(root, "techName", "Data Module")
        
        # Build HTML
        try:
            html_body = self._dm_to_html(root, options)
            full_html = self._build_html_document(
                title=dm_title,
                body_content=html_body,
                options=options,
            )
            result.html_data = full_html
            result.file_size_bytes = len(full_html.encode('utf-8'))
            result.success = True
            
        except Exception as e:
            result.errors.append(f"Failed to generate HTML: {e}")
            return result
        
        # Write to file if path provided
        if output_path and result.success:
            try:
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(full_html, encoding='utf-8')
                result.output_path = output_path
                
                # Generate CSS file if external
                if not options.inline_css:
                    css_path = output_path.with_suffix('.css')
                    css_content = self._generate_css(options)
                    css_path.write_text(css_content, encoding='utf-8')
                    result.asset_files.append(css_path)
                
                # Generate JS file if enabled
                if options.include_javascript:
                    js_path = output_path.with_suffix('.js')
                    js_content = self._generate_javascript(options)
                    js_path.write_text(js_content, encoding='utf-8')
                    result.asset_files.append(js_path)
                    
            except Exception as e:
                result.warnings.append(f"Failed to write to file: {e}")
        
        # Update statistics
        self._render_count += 1
        
        # Calculate render time
        end_time = datetime.now()
        result.render_time_seconds = (end_time - start_time).total_seconds()
        
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
        
        Generates:
        - Index page with TOC
        - Individual HTML pages for each DM
        - Navigation structure
        
        Args:
            pm_content: Publication Module XML
            dm_contents: Dictionary of DM codes to DM XML content
            output_dir: Output directory for HTML files
            options: Rendering options
            
        Returns:
            HTMLRenderResult
        """
        start_time = datetime.now()
        options = options or self.default_options
        
        result = HTMLRenderResult(success=False)
        
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
        dm_refs = self._extract_dm_refs(pm_root)
        result.dm_codes = dm_refs
        
        # Create output directory
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
        
        # Render index page
        try:
            index_html = self._generate_index_page(pm_title, dm_refs, options)
            if output_dir:
                index_path = output_dir / "index.html"
                index_path.write_text(index_html, encoding='utf-8')
                result.output_path = index_path
            result.html_data = index_html
            
        except Exception as e:
            result.errors.append(f"Failed to generate index page: {e}")
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
                    
                    dm_html_body = self._dm_to_html(dm_root, options)
                    dm_title = self._find_element_text(dm_root, "techName", dm_ref)
                    
                    # Add navigation to other DMs
                    nav_html = self._generate_dm_navigation(dm_ref, dm_refs)
                    full_dm_html = self._build_html_document(
                        title=dm_title,
                        body_content=nav_html + dm_html_body,
                        options=options,
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
        
        # Generate shared CSS
        if output_dir and not options.inline_css:
            css_path = output_dir / "styles.css"
            css_content = self._generate_css(options)
            css_path.write_text(css_content, encoding='utf-8')
            result.asset_files.append(css_path)
        
        # Generate shared JavaScript
        if output_dir and options.include_javascript:
            js_path = output_dir / "scripts.js"
            js_content = self._generate_javascript(options)
            js_path.write_text(js_content, encoding='utf-8')
            result.asset_files.append(js_path)
        
        result.success = True
        result.file_size_bytes = len(index_html.encode('utf-8'))
        
        # Update statistics
        self._render_count += 1
        
        # Calculate render time
        end_time = datetime.now()
        result.render_time_seconds = (end_time - start_time).total_seconds()
        
        return result
    
    def _dm_to_html(
        self,
        dm_root: ET.Element,
        options: HTMLRenderOptions,
    ) -> str:
        """Convert Data Module XML to HTML body content."""
        html_parts = ['<article class="data-module">']
        
        # Extract title
        tech_name = self._find_element_text(dm_root, "techName", "Data Module")
        html_parts.append(f'<h1 class="dm-title">{self._escape_html(tech_name)}</h1>')
        
        # Info name
        info_name = self._find_element_text(dm_root, "infoName", "")
        if info_name:
            html_parts.append(f'<p class="dm-subtitle">{self._escape_html(info_name)}</p>')
        
        # Process content
        content = self._find_element(dm_root, "content")
        if content is not None:
            content_html = self._element_to_html(content, options)
            html_parts.append(content_html)
        
        html_parts.append('</article>')
        return "\n".join(html_parts)
    
    def _element_to_html(
        self,
        element: ET.Element,
        options: HTMLRenderOptions,
        level: int = 0,
    ) -> str:
        """Convert XML element to HTML recursively."""
        local_name = element.tag.split("}")[-1] if "}" in element.tag else element.tag
        
        # Element mapping
        html_converters = {
            "para": self._convert_para,
            "title": self._convert_title,
            "proceduralStep": self._convert_step,
            "warning": self._convert_warning,
            "caution": self._convert_caution,
            "note": self._convert_note,
            "table": self._convert_table,
            "figure": self._convert_figure,
            "internalRef": self._convert_internal_ref,
            "externalPubRef": self._convert_external_ref,
        }
        
        # Use custom converter if available
        if local_name in html_converters:
            return html_converters[local_name](element, options)
        
        # Default conversion
        return self._convert_default(element, options, level)
    
    def _convert_para(self, element: ET.Element, options: HTMLRenderOptions) -> str:
        """Convert paragraph."""
        text = self._get_element_text_with_children(element, options)
        return f'<p class="para">{text}</p>'
    
    def _convert_title(self, element: ET.Element, options: HTMLRenderOptions) -> str:
        """Convert title."""
        text = self._get_element_text_with_children(element, options)
        return f'<h2 class="title">{text}</h2>'
    
    def _convert_step(self, element: ET.Element, options: HTMLRenderOptions) -> str:
        """Convert procedural step."""
        text = self._get_element_text_with_children(element, options)
        return f'<li class="step">{text}</li>'
    
    def _convert_warning(self, element: ET.Element, options: HTMLRenderOptions) -> str:
        """Convert warning."""
        text = self._get_element_text_with_children(element, options)
        return f'''
        <div class="alert alert-warning">
            <div class="alert-icon">⚠️</div>
            <div class="alert-content">
                <strong>WARNING</strong>
                {text}
            </div>
        </div>
        '''
    
    def _convert_caution(self, element: ET.Element, options: HTMLRenderOptions) -> str:
        """Convert caution."""
        text = self._get_element_text_with_children(element, options)
        return f'''
        <div class="alert alert-caution">
            <div class="alert-icon">⚡</div>
            <div class="alert-content">
                <strong>CAUTION</strong>
                {text}
            </div>
        </div>
        '''
    
    def _convert_note(self, element: ET.Element, options: HTMLRenderOptions) -> str:
        """Convert note."""
        text = self._get_element_text_with_children(element, options)
        return f'''
        <div class="alert alert-note">
            <div class="alert-icon">ℹ️</div>
            <div class="alert-content">
                <strong>NOTE</strong>
                {text}
            </div>
        </div>
        '''
    
    def _convert_table(self, element: ET.Element, options: HTMLRenderOptions) -> str:
        """Convert table."""
        html = ['<table class="table">']
        
        # Title
        title = self._find_element(element, "title")
        if title is not None:
            title_text = self._get_element_text_with_children(title, options)
            html.append(f'<caption>{title_text}</caption>')
        
        # Rows
        html.append('<tbody>')
        for row in element.iter():
            local_name = row.tag.split("}")[-1] if "}" in row.tag else row.tag
            if local_name == "row":
                html.append('<tr>')
                for entry in row:
                    entry_local = entry.tag.split("}")[-1] if "}" in entry.tag else entry.tag
                    if entry_local == "entry":
                        entry_text = self._get_element_text_with_children(entry, options)
                        html.append(f'<td>{entry_text}</td>')
                html.append('</tr>')
        html.append('</tbody>')
        html.append('</table>')
        
        return "\n".join(html)
    
    def _convert_figure(self, element: ET.Element, options: HTMLRenderOptions) -> str:
        """Convert figure."""
        html = ['<figure class="figure">']
        
        # Graphic reference
        graphic = self._find_element(element, "graphic")
        if graphic is not None:
            icn_ref = graphic.get("infoEntityIdent", "")
            if icn_ref:
                html.append(f'<img src="{icn_ref}.png" alt="{icn_ref}" class="figure-img">')
        
        # Title/Caption
        title = self._find_element(element, "title")
        if title is not None:
            title_text = self._get_element_text_with_children(title, options)
            html.append(f'<figcaption>{title_text}</figcaption>')
        
        html.append('</figure>')
        return "\n".join(html)
    
    def _convert_internal_ref(self, element: ET.Element, options: HTMLRenderOptions) -> str:
        """Convert internal reference."""
        ref_id = element.get("internalRefId", "")
        text = element.text or ref_id
        self._cross_refs.add(ref_id)
        return f'<a href="#{ref_id}" class="internal-ref">{self._escape_html(text)}</a>'
    
    def _convert_external_ref(self, element: ET.Element, options: HTMLRenderOptions) -> str:
        """Convert external reference."""
        text = self._get_element_text_with_children(element, options)
        return f'<a href="#" class="external-ref">{text}</a>'
    
    def _convert_default(
        self,
        element: ET.Element,
        options: HTMLRenderOptions,
        level: int,
    ) -> str:
        """Default element conversion."""
        local_name = element.tag.split("}")[-1] if "}" in element.tag else element.tag
        text = element.text or ""
        children_html = "".join(
            self._element_to_html(child, options, level + 1) for child in element
        )
        tail = element.tail or ""
        
        return f"<div class='{local_name}'>{text}{children_html}</div>{tail}"
    
    def _get_element_text_with_children(
        self,
        element: ET.Element,
        options: HTMLRenderOptions,
    ) -> str:
        """Get element text including children recursively."""
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
        options: HTMLRenderOptions,
    ) -> str:
        """Build complete HTML document."""
        doctype = "<!DOCTYPE html>" if options.html_version == HTMLVersion.HTML5 else ""
        
        # CSS link or inline
        css_block = ""
        if options.inline_css:
            css_content = self._generate_css(options)
            css_block = f"<style>{css_content}</style>"
        else:
            css_filename = "styles.css"
            css_block = f'<link rel="stylesheet" href="{css_filename}">'
        
        # JavaScript
        js_block = ""
        if options.include_javascript:
            if options.inline_css:  # Use same logic for JS
                js_content = self._generate_javascript(options)
                js_block = f"<script>{js_content}</script>"
            else:
                js_filename = "scripts.js"
                js_block = f'<script src="{js_filename}"></script>'
        
        # Metadata
        metadata = f"""
        <meta name="contract" content="{self.contract_id}">
        <meta name="baseline" content="{self.baseline_ref}">
        <meta name="generated" content="{datetime.now().isoformat()}">
        """
        
        return f"""{doctype}
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self._escape_html(title)}</title>
    {metadata}
    {css_block}
</head>
<body>
    {body_content}
    {js_block}
</body>
</html>
"""
    
    def _generate_css(self, options: HTMLRenderOptions) -> str:
        """Generate CSS stylesheet."""
        return f"""
/* S1000D HTML Renderer CSS */
/* Contract: {self.contract_id} */

:root {{
    --primary-color: {options.primary_color};
    --secondary-color: {options.secondary_color};
    --warning-color: {options.warning_color};
    --font-family: {options.font_family};
    --base-font-size: {options.base_font_size};
}}

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

.data-module {{
    margin: 20px 0;
}}

.dm-title {{
    font-size: 2em;
    font-weight: bold;
    color: var(--primary-color);
    margin-bottom: 0.5em;
    border-bottom: 3px solid var(--primary-color);
    padding-bottom: 0.3em;
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
    color: #222;
}}

.para {{
    margin: 1em 0;
    text-align: justify;
}}

.step {{
    margin: 0.5em 0;
    line-height: 1.8;
}}

.alert {{
    display: flex;
    padding: 15px;
    margin: 20px 0;
    border-left: 5px solid;
    border-radius: 4px;
}}

.alert-warning {{
    background-color: #fff3cd;
    border-color: #ff6600;
}}

.alert-caution {{
    background-color: #fff8dc;
    border-color: #ffa500;
}}

.alert-note {{
    background-color: #e7f3ff;
    border-color: var(--primary-color);
}}

.alert-icon {{
    font-size: 24px;
    margin-right: 15px;
}}

.alert-content {{
    flex: 1;
}}

.alert-content strong {{
    display: block;
    margin-bottom: 8px;
    font-size: 1.1em;
}}

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

.table td, .table th {{
    border: 1px solid #ddd;
    padding: 10px;
    text-align: left;
}}

.table tr:nth-child(even) {{
    background-color: #f9f9f9;
}}

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

.internal-ref, .external-ref {{
    color: var(--primary-color);
    text-decoration: none;
    border-bottom: 1px dotted var(--primary-color);
}}

.internal-ref:hover, .external-ref:hover {{
    text-decoration: underline;
}}

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
    flex-wrap: wrap;
    gap: 15px;
}}

.navigation li {{
    margin: 0;
}}

.navigation a {{
    color: var(--primary-color);
    text-decoration: none;
}}

.navigation a:hover {{
    text-decoration: underline;
}}

/* Responsive design */
@media (max-width: 768px) {{
    body {{
        padding: 10px;
        font-size: 14px;
    }}
    
    .dm-title {{
        font-size: 1.5em;
    }}
    
    .table {{
        font-size: 0.9em;
    }}
}}

/* Print styles */
@media print {{
    body {{
        max-width: 100%;
        font-size: 12pt;
    }}
    
    .navigation {{
        display: none;
    }}
    
    .alert {{
        page-break-inside: avoid;
    }}
    
    .figure {{
        page-break-inside: avoid;
    }}
}}

/* Dark mode support */
@media (prefers-color-scheme: dark) {{
    body {{
        background-color: #1e1e1e;
        color: #e0e0e0;
    }}
    
    .dm-title {{
        color: #6ba3ff;
        border-color: #6ba3ff;
    }}
    
    .table td, .table th {{
        border-color: #444;
    }}
    
    .table tr:nth-child(even) {{
        background-color: #2a2a2a;
    }}
}}
"""
    
    def _generate_javascript(self, options: HTMLRenderOptions) -> str:
        """Generate JavaScript for interactive features."""
        return """
/* S1000D HTML Renderer JavaScript */

// Search functionality
function initSearch() {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const query = e.target.value.toLowerCase();
            // Implement search logic
            console.log('Searching for:', query);
        });
    }
}

// Collapsible sections
function initCollapsible() {
    document.querySelectorAll('.collapsible-header').forEach(header => {
        header.addEventListener('click', function() {
            this.classList.toggle('active');
            const content = this.nextElementSibling;
            if (content.style.maxHeight) {
                content.style.maxHeight = null;
            } else {
                content.style.maxHeight = content.scrollHeight + 'px';
            }
        });
    });
}

// Highlight current section in navigation
function highlightCurrentSection() {
    const sections = document.querySelectorAll('article[id]');
    const navLinks = document.querySelectorAll('.navigation a');
    
    window.addEventListener('scroll', function() {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (pageYOffset >= sectionTop - 60) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('active');
            }
        });
    });
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    initSearch();
    initCollapsible();
    highlightCurrentSection();
});
"""
    
    def _generate_index_page(
        self,
        pm_title: str,
        dm_refs: List[str],
        options: HTMLRenderOptions,
    ) -> str:
        """Generate index page for publication module."""
        body = ['<div class="index-page">']
        body.append(f'<h1>{self._escape_html(pm_title)}</h1>')
        body.append('<nav class="toc">')
        body.append('<h2>Table of Contents</h2>')
        body.append('<ul>')
        
        for dm_ref in dm_refs:
            filename = self._sanitize_filename(dm_ref) + ".html"
            body.append(f'<li><a href="{filename}">{self._escape_html(dm_ref)}</a></li>')
        
        body.append('</ul>')
        body.append('</nav>')
        body.append('</div>')
        
        body_content = "\n".join(body)
        return self._build_html_document(pm_title, body_content, options)
    
    def _generate_dm_navigation(
        self,
        current_dm: str,
        all_dms: List[str],
    ) -> str:
        """Generate navigation for DM page."""
        html = ['<nav class="navigation">']
        html.append('<ul>')
        html.append('<li><a href="index.html">← Index</a></li>')
        
        # Find previous and next
        try:
            current_idx = all_dms.index(current_dm)
            if current_idx > 0:
                prev_dm = all_dms[current_idx - 1]
                prev_file = self._sanitize_filename(prev_dm) + ".html"
                html.append(f'<li><a href="{prev_file}">← Previous</a></li>')
            
            if current_idx < len(all_dms) - 1:
                next_dm = all_dms[current_idx + 1]
                next_file = self._sanitize_filename(next_dm) + ".html"
                html.append(f'<li><a href="{next_file}">Next →</a></li>')
        except ValueError:
            pass
        
        html.append('</ul>')
        html.append('</nav>')
        return "\n".join(html)
    
    def _extract_dm_code(self, root: ET.Element) -> str:
        """Extract DM code from XML."""
        dm_code = self._find_element(root, "dmCode")
        if dm_code is not None:
            parts = [
                dm_code.get("modelIdentCode", ""),
                dm_code.get("systemCode", ""),
                dm_code.get("infoCode", ""),
            ]
            return "-".join(p for p in parts if p) or "UNKNOWN"
        return "UNKNOWN"
    
    def _extract_pm_title(self, root: ET.Element) -> str:
        """Extract PM title."""
        return self._find_element_text(root, "pmTitle", "Publication")
    
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
        """Sanitize filename."""
        # Replace invalid characters
        return "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get rendering statistics."""
        return {
            "contract_id": self.contract_id,
            "render_count": self._render_count,
            "cross_refs_count": len(self._cross_refs),
        }
