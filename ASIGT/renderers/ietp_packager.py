# =============================================================================
# ASIGT IETP Packager
# Interactive Electronic Technical Publication packaging
# Version: 2.0.0
# =============================================================================
"""
IETP Packager

Packages S1000D content into Interactive Electronic Technical Publication (IETP)
format for deployment to interactive viewing systems. Generates:
- Complete IETP container with all referenced DMs
- Viewer configuration files
- Search indexes
- Cross-reference maps
- Applicability filtering
- Multimedia content integration

Operates exclusively under ASIT contract authority.

IETP Structure:
    ietp_package/
    ├── content/          # S1000D XML data modules
    ├── graphics/         # ICN graphics (CGM, PNG, SVG, etc.)
    ├── multimedia/       # Video, audio, 3D models
    ├── css/             # Stylesheets
    ├── js/              # Viewer scripts
    ├── index/           # Search indexes
    ├── config.xml       # IETP configuration
    └── index.html       # Entry point
"""

from __future__ import annotations

import json
import logging
import shutil
import zipfile
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union
from xml.etree import ElementTree as ET

logger = logging.getLogger(__name__)


class IETPFormat(Enum):
    """IETP package formats."""
    DIRECTORY = "directory"     # Unpacked directory structure
    ZIP = "zip"                 # ZIP archive
    CSP = "csp"                 # Common Source Package (S1000D)


class ViewerType(Enum):
    """IETP viewer types."""
    WEB = "web"                 # Web browser-based
    DESKTOP = "desktop"         # Standalone desktop app
    MOBILE = "mobile"           # Mobile app
    EMBEDDED = "embedded"       # Embedded system viewer


@dataclass
class IETPConfig:
    """IETP configuration."""
    title: str = "Technical Publication"
    version: str = "1.0.0"
    language: str = "en-US"
    viewer_type: ViewerType = ViewerType.WEB
    enable_search: bool = True
    enable_bookmarks: bool = True
    enable_annotations: bool = False
    enable_print: bool = True
    enable_offline: bool = True
    applicability_filtering: bool = True
    cross_reference_resolution: bool = True
    multimedia_support: bool = True
    security_level: str = "UNCLASSIFIED"


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
            "total_size_mb": round(self.total_size_bytes / (1024 * 1024), 2),
            "errors": self.errors,
            "warnings": self.warnings,
            "packaged_at": self.packaged_at,
            "package_time_seconds": self.package_time_seconds,
        }


@dataclass
class SearchIndexEntry:
    """Search index entry."""
    dm_code: str
    title: str
    keywords: List[str] = field(default_factory=list)
    content_text: str = ""
    weight: int = 1


class IETPPackager:
    """
    IETP Packager.
    
    Packages validated S1000D content into Interactive Electronic Technical
    Publication format with viewer integration. Operates under ASIT contract authority.
    
    Attributes:
        contract: ASIT transformation contract
        config: Packager configuration
        
    Example:
        >>> packager = IETPPackager(contract=contract, config=config)
        >>> result = packager.package_publication(
        ...     pm_content=pm_xml,
        ...     dm_contents=dm_dict,
        ...     output_path="AMM_v1.0_IETP",
        ... )
    """
    
    def __init__(
        self,
        contract: Dict[str, Any],
        config: Dict[str, Any],
    ):
        """
        Initialize IETP Packager.
        
        Args:
            contract: ASIT transformation contract (required)
            config: Packager configuration
            
        Raises:
            ValueError: If contract is missing
        """
        if not contract:
            raise ValueError("ASIT contract is required for IETP packaging")
        
        self.contract = contract
        self.config = config
        
        # Contract parameters
        self.contract_id = contract.get("id", "UNKNOWN")
        self.baseline_ref = contract.get("source", {}).get("baseline", "UNKNOWN")
        
        # Default IETP config
        self.ietp_config = IETPConfig(
            title=config.get("title", "Technical Publication"),
            version=config.get("version", "1.0.0"),
            language=config.get("language", "en-US"),
            viewer_type=ViewerType(config.get("viewer_type", "web")),
            enable_search=config.get("enable_search", True),
            enable_bookmarks=config.get("enable_bookmarks", True),
        )
        
        # Statistics
        self._package_count = 0
        self._dm_refs: Set[str] = set()
        self._icn_refs: Set[str] = set()
        
        logger.info(
            f"IETPPackager initialized: contract={self.contract_id}, "
            f"viewer={self.ietp_config.viewer_type.value}"
        )
    
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
        
        result = IETPPackageResult(
            success=False,
            package_format=package_format,
        )
        
        # Parse PM XML
        try:
            if isinstance(pm_content, str):
                pm_root = ET.fromstring(pm_content)
            else:
                pm_root = pm_content
        except Exception as e:
            result.errors.append(f"Failed to parse PM XML: {e}")
            return result
        
        # Extract PM metadata
        pm_title = self._extract_pm_title(pm_root)
        dm_refs = self._extract_dm_refs(pm_root)
        
        self.ietp_config.title = pm_title
        result.dm_count = len(dm_refs)
        
        # Create package directory
        output_path = Path(output_path)
        
        try:
            # Use temporary directory for zip/csp formats
            if package_format in [IETPFormat.ZIP, IETPFormat.CSP]:
                import tempfile
                temp_dir = Path(tempfile.mkdtemp())
                package_dir = temp_dir / "ietp_package"
            else:
                package_dir = output_path
            
            package_dir.mkdir(parents=True, exist_ok=True)
            
            # Create directory structure
            self._create_directory_structure(package_dir)
            
            # Package PM
            pm_file = package_dir / "content" / "publication.xml"
            pm_xml_str = ET.tostring(pm_root, encoding='unicode')
            pm_file.write_text(pm_xml_str, encoding='utf-8')
            
            # Package DMs
            for dm_code in dm_refs:
                if dm_code in dm_contents:
                    try:
                        dm_xml = dm_contents[dm_code]
                        if isinstance(dm_xml, str):
                            dm_root = ET.fromstring(dm_xml)
                        else:
                            dm_root = dm_xml
                        
                        # Save DM
                        dm_filename = self._sanitize_filename(dm_code) + ".xml"
                        dm_file = package_dir / "content" / dm_filename
                        dm_xml_str = ET.tostring(dm_root, encoding='unicode')
                        dm_file.write_text(dm_xml_str, encoding='utf-8')
                        
                        # Extract ICN references
                        icn_refs = self._extract_icn_refs(dm_root)
                        self._icn_refs.update(icn_refs)
                        
                    except Exception as e:
                        result.warnings.append(f"Failed to package DM {dm_code}: {e}")
                else:
                    result.warnings.append(f"DM content not found: {dm_code}")
            
            # Copy graphics
            if graphics_dir and graphics_dir.exists():
                result.icn_count = self._copy_graphics(
                    graphics_dir,
                    package_dir / "graphics",
                )
            
            # Copy multimedia
            if multimedia_dir and multimedia_dir.exists():
                result.multimedia_count = self._copy_multimedia(
                    multimedia_dir,
                    package_dir / "multimedia",
                )
            
            # Generate configuration
            self._generate_config(package_dir, pm_root, dm_refs)
            
            # Generate HTML viewer
            self._generate_viewer(package_dir)
            
            # Generate search index
            if self.ietp_config.enable_search:
                self._generate_search_index(
                    package_dir,
                    dm_refs,
                    dm_contents,
                )
            
            # Generate cross-reference map
            if self.ietp_config.cross_reference_resolution:
                self._generate_xref_map(package_dir, dm_contents)
            
            # Calculate total size
            result.total_size_bytes = self._calculate_directory_size(package_dir)
            
            # Create archive if requested
            if package_format == IETPFormat.ZIP:
                zip_path = output_path.with_suffix('.zip')
                self._create_zip(package_dir, zip_path)
                result.output_path = zip_path
                # Clean up temp directory
                shutil.rmtree(temp_dir)
            elif package_format == IETPFormat.CSP:
                csp_path = output_path.with_suffix('.csp')
                self._create_csp(package_dir, csp_path)
                result.output_path = csp_path
                # Clean up temp directory
                shutil.rmtree(temp_dir)
            else:
                result.output_path = package_dir
            
            result.success = True
            
        except Exception as e:
            result.errors.append(f"Failed to create package: {e}")
            return result
        
        # Update statistics
        self._package_count += 1
        self._dm_refs.update(dm_refs)
        
        # Calculate package time
        end_time = datetime.now()
        result.package_time_seconds = (end_time - start_time).total_seconds()
        
        return result
    
    def _create_directory_structure(self, package_dir: Path) -> None:
        """Create IETP directory structure."""
        subdirs = [
            "content",
            "graphics",
            "multimedia",
            "css",
            "js",
            "index",
            "config",
        ]
        
        for subdir in subdirs:
            (package_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    def _generate_config(
        self,
        package_dir: Path,
        pm_root: ET.Element,
        dm_refs: List[str],
    ) -> None:
        """Generate IETP configuration file."""
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
                },
            },
            "content": {
                "publication": "content/publication.xml",
                "data_modules": [
                    f"content/{self._sanitize_filename(dm)}.xml"
                    for dm in dm_refs
                ],
            },
            "applicability": {
                "enabled": self.ietp_config.applicability_filtering,
                "default_profile": "all",
            },
        }
        
        config_file = package_dir / "config" / "ietp_config.json"
        config_file.write_text(json.dumps(config, indent=2), encoding='utf-8')
    
    def _generate_viewer(self, package_dir: Path) -> None:
        """Generate HTML viewer interface."""
        # Main index.html
        index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.ietp_config.title}</title>
    <link rel="stylesheet" href="css/viewer.css">
</head>
<body>
    <div id="ietp-viewer">
        <header id="header">
            <h1>{self.ietp_config.title}</h1>
            <div id="toolbar">
                <button id="btn-home">Home</button>
                <button id="btn-toc">TOC</button>
                <button id="btn-search">Search</button>
                <button id="btn-print">Print</button>
            </div>
        </header>
        
        <div id="container">
            <nav id="sidebar">
                <div id="toc"></div>
            </nav>
            
            <main id="content">
                <div id="viewer-frame"></div>
            </main>
        </div>
        
        <footer id="footer">
            <p>Contract: {self.contract_id} | Baseline: {self.baseline_ref}</p>
        </footer>
    </div>
    
    <script src="js/viewer.js"></script>
</body>
</html>
"""
        
        index_file = package_dir / "index.html"
        index_file.write_text(index_html, encoding='utf-8')
        
        # Viewer CSS
        viewer_css = """
/* IETP Viewer CSS */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    font-size: 14px;
    color: #333;
}

#ietp-viewer {
    display: flex;
    flex-direction: column;
    height: 100vh;
}

#header {
    background-color: #2c3e50;
    color: white;
    padding: 15px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

#header h1 {
    font-size: 20px;
    font-weight: normal;
}

#toolbar button {
    background-color: #34495e;
    color: white;
    border: none;
    padding: 8px 15px;
    margin-left: 10px;
    cursor: pointer;
    border-radius: 4px;
}

#toolbar button:hover {
    background-color: #415b76;
}

#container {
    display: flex;
    flex: 1;
    overflow: hidden;
}

#sidebar {
    width: 300px;
    background-color: #ecf0f1;
    border-right: 1px solid #bdc3c7;
    overflow-y: auto;
    padding: 20px;
}

#toc {
    list-style: none;
}

#toc a {
    display: block;
    padding: 8px 10px;
    color: #2c3e50;
    text-decoration: none;
    border-radius: 4px;
}

#toc a:hover {
    background-color: #d5dbdb;
}

#content {
    flex: 1;
    overflow-y: auto;
    padding: 30px;
}

#viewer-frame {
    max-width: 1200px;
    margin: 0 auto;
}

#footer {
    background-color: #ecf0f1;
    border-top: 1px solid #bdc3c7;
    padding: 10px 20px;
    text-align: center;
    font-size: 12px;
    color: #7f8c8d;
}

/* Responsive design */
@media (max-width: 768px) {
    #container {
        flex-direction: column;
    }
    
    #sidebar {
        width: 100%;
        max-height: 200px;
    }
}
"""
        
        css_file = package_dir / "css" / "viewer.css"
        css_file.write_text(viewer_css, encoding='utf-8')
        
        # Viewer JavaScript
        viewer_js = """
/* IETP Viewer JavaScript */

class IETPViewer {
    constructor() {
        this.config = null;
        this.currentDM = null;
        this.init();
    }
    
    async init() {
        // Load configuration
        this.config = await this.loadConfig();
        
        // Build TOC
        this.buildTOC();
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Load first DM
        if (this.config.content.data_modules.length > 0) {
            this.loadDM(this.config.content.data_modules[0]);
        }
    }
    
    async loadConfig() {
        const response = await fetch('config/ietp_config.json');
        return await response.json();
    }
    
    async buildTOC() {
        const tocElement = document.getElementById('toc');
        const ul = document.createElement('ul');
        
        for (const dmPath of this.config.content.data_modules) {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = '#';
            a.textContent = dmPath.replace('content/', '').replace('.xml', '');
            a.addEventListener('click', (e) => {
                e.preventDefault();
                this.loadDM(dmPath);
            });
            li.appendChild(a);
            ul.appendChild(li);
        }
        
        tocElement.appendChild(ul);
    }
    
    async loadDM(dmPath) {
        try {
            const response = await fetch(dmPath);
            const xmlText = await response.text();
            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(xmlText, 'text/xml');
            
            // Render DM content
            this.renderDM(xmlDoc);
            this.currentDM = dmPath;
            
        } catch (error) {
            console.error('Failed to load DM:', error);
        }
    }
    
    renderDM(xmlDoc) {
        const frame = document.getElementById('viewer-frame');
        
        // Extract title
        const techName = xmlDoc.querySelector('techName');
        const title = techName ? techName.textContent : 'Data Module';
        
        // Simple rendering (in production, use XSLT or more sophisticated rendering)
        let html = `<h1>${title}</h1>`;
        
        // Extract content
        const content = xmlDoc.querySelector('content');
        if (content) {
            html += this.renderElement(content);
        }
        
        frame.innerHTML = html;
    }
    
    renderElement(element) {
        // Simple element rendering
        // In production, implement full S1000D rendering logic
        let html = '';
        
        for (const child of element.children) {
            const tagName = child.tagName.toLowerCase();
            
            if (tagName === 'para') {
                html += `<p>${child.textContent}</p>`;
            } else if (tagName === 'title') {
                html += `<h2>${child.textContent}</h2>`;
            } else {
                html += this.renderElement(child);
            }
        }
        
        return html;
    }
    
    setupEventListeners() {
        document.getElementById('btn-home').addEventListener('click', () => {
            window.location.reload();
        });
        
        document.getElementById('btn-toc').addEventListener('click', () => {
            const sidebar = document.getElementById('sidebar');
            sidebar.style.display = sidebar.style.display === 'none' ? 'block' : 'none';
        });
        
        document.getElementById('btn-search').addEventListener('click', () => {
            this.showSearch();
        });
        
        document.getElementById('btn-print').addEventListener('click', () => {
            window.print();
        });
    }
    
    showSearch() {
        alert('Search functionality - to be implemented');
    }
}

// Initialize viewer on load
document.addEventListener('DOMContentLoaded', () => {
    new IETPViewer();
});
"""
        
        js_file = package_dir / "js" / "viewer.js"
        js_file.write_text(viewer_js, encoding='utf-8')
    
    def _generate_search_index(
        self,
        package_dir: Path,
        dm_refs: List[str],
        dm_contents: Dict[str, Union[str, ET.Element]],
    ) -> None:
        """Generate search index."""
        index_entries = []
        
        for dm_code in dm_refs:
            if dm_code in dm_contents:
                try:
                    dm_xml = dm_contents[dm_code]
                    if isinstance(dm_xml, str):
                        dm_root = ET.fromstring(dm_xml)
                    else:
                        dm_root = dm_xml
                    
                    # Extract title
                    title = self._find_element_text(dm_root, "techName", dm_code)
                    
                    # Extract keywords
                    keywords = []
                    for kw in dm_root.iter():
                        if kw.tag.endswith("keyword"):
                            keywords.append(kw.text or "")
                    
                    # Extract content text
                    content_text = self._extract_text_content(dm_root)
                    
                    entry = {
                        "dm_code": dm_code,
                        "title": title,
                        "keywords": keywords,
                        "content_preview": content_text[:200],
                    }
                    
                    index_entries.append(entry)
                    
                except Exception as e:
                    logger.warning(f"Failed to index DM {dm_code}: {e}")
        
        # Save index
        index_file = package_dir / "index" / "search_index.json"
        index_file.write_text(json.dumps(index_entries, indent=2), encoding='utf-8')
    
    def _generate_xref_map(
        self,
        package_dir: Path,
        dm_contents: Dict[str, Union[str, ET.Element]],
    ) -> None:
        """Generate cross-reference map."""
        xref_map = {}
        
        for dm_code, dm_xml in dm_contents.items():
            try:
                if isinstance(dm_xml, str):
                    dm_root = ET.fromstring(dm_xml)
                else:
                    dm_root = dm_xml
                
                refs = []
                
                # Find internal refs
                for ref in dm_root.iter():
                    local_name = ref.tag.split("}")[-1] if "}" in ref.tag else ref.tag
                    if local_name == "internalRef":
                        ref_id = ref.get("internalRefId", "")
                        if ref_id:
                            refs.append({"type": "internal", "target": ref_id})
                    elif local_name == "dmRef":
                        dm_code_elem = self._find_element(ref, "dmCode")
                        if dm_code_elem is not None:
                            target_dmc = self._build_dmc_string(dm_code_elem)
                            refs.append({"type": "dm", "target": target_dmc})
                
                if refs:
                    xref_map[dm_code] = refs
                    
            except Exception as e:
                logger.warning(f"Failed to map xrefs for {dm_code}: {e}")
        
        # Save map
        xref_file = package_dir / "index" / "xref_map.json"
        xref_file.write_text(json.dumps(xref_map, indent=2), encoding='utf-8')
    
    def _copy_graphics(
        self,
        source_dir: Path,
        target_dir: Path,
    ) -> int:
        """Copy graphics files to package."""
        count = 0
        
        # Common graphic extensions
        extensions = ['.png', '.jpg', '.jpeg', '.svg', '.cgm', '.tif', '.tiff']
        
        for ext in extensions:
            for file_path in source_dir.glob(f"**/*{ext}"):
                try:
                    target_path = target_dir / file_path.name
                    shutil.copy2(file_path, target_path)
                    count += 1
                except Exception as e:
                    logger.warning(f"Failed to copy graphic {file_path}: {e}")
        
        return count
    
    def _copy_multimedia(
        self,
        source_dir: Path,
        target_dir: Path,
    ) -> int:
        """Copy multimedia files to package."""
        count = 0
        
        # Common multimedia extensions
        extensions = ['.mp4', '.webm', '.mp3', '.wav', '.pdf']
        
        for ext in extensions:
            for file_path in source_dir.glob(f"**/*{ext}"):
                try:
                    target_path = target_dir / file_path.name
                    shutil.copy2(file_path, target_path)
                    count += 1
                except Exception as e:
                    logger.warning(f"Failed to copy multimedia {file_path}: {e}")
        
        return count
    
    def _create_zip(self, source_dir: Path, zip_path: Path) -> None:
        """Create ZIP archive of package."""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in source_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(source_dir)
                    zipf.write(file_path, arcname)
    
    def _create_csp(self, source_dir: Path, csp_path: Path) -> None:
        """Create Common Source Package (CSP) archive."""
        # CSP is essentially a ZIP with specific naming and structure
        self._create_zip(source_dir, csp_path)
    
    def _calculate_directory_size(self, directory: Path) -> int:
        """Calculate total size of directory."""
        total_size = 0
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        return total_size
    
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
    
    def _extract_icn_refs(self, root: ET.Element) -> List[str]:
        """Extract ICN references from DM."""
        icn_refs = []
        for graphic in root.iter():
            local_name = graphic.tag.split("}")[-1] if "}" in graphic.tag else graphic.tag
            if local_name == "graphic":
                icn_id = graphic.get("infoEntityIdent", "")
                if icn_id:
                    icn_refs.append(icn_id)
        return icn_refs
    
    def _extract_text_content(self, root: ET.Element) -> str:
        """Extract all text content from XML."""
        text_parts = []
        for elem in root.iter():
            if elem.text:
                text_parts.append(elem.text.strip())
        return " ".join(text_parts)
    
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
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize filename."""
        return "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get packaging statistics."""
        return {
            "contract_id": self.contract_id,
            "package_count": self._package_count,
            "total_dms": len(self._dm_refs),
            "total_icns": len(self._icn_refs),
        }
