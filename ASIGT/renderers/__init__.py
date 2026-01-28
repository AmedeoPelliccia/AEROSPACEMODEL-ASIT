# =============================================================================
# ASIGT Renderers Module
# S1000D output rendering under ASIT contract authority
# Version: 2.0.0
# =============================================================================
"""
ASIGT Renderers Package

This package provides output renderers for S1000D content that operate
exclusively under ASIT contract authority. Renderers transform validated
S1000D XML into deliverable formats:
- PDF exports (publication-ready)
- HTML exports (web/IETP)
- IETP packages (runtime viewer)

Renderers:
    - pdf_renderer: PDF generation from S1000D XML
    - html_renderer: HTML generation with CSS styling
    - ietp_packager: Interactive Electronic Technical Publication packaging

Usage:
    from asigt.renderers import PDFRenderer, HTMLRenderer, IETPPackager
    
    # All renderers require an ASIT contract
    renderer = PDFRenderer(contract=contract, config=config)
    result = renderer.render(dm_content, output_path="output.pdf")
"""

from .pdf_renderer import PDFRenderer, PDFRenderResult
from .html_renderer import HTMLRenderer, HTMLRenderResult
from .ietp_packager import IETPPackager, IETPPackageResult

__all__ = [
    "PDFRenderer",
    "PDFRenderResult",
    "HTMLRenderer",
    "HTMLRenderResult",
    "IETPPackager",
    "IETPPackageResult",
]

__version__ = "2.0.0"
