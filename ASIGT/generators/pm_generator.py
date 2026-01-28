# =============================================================================
# ASIGT Publication Module Generator
# S1000D Publication Module generation under ASIT contract authority
# Version: 2.0.0
# =============================================================================
"""
Publication Module Generator

Generates S1000D-compliant Publication Modules (PM) that organize
Data Modules into deliverable publications (AMM, SRM, CMM, etc.).
Operates exclusively under ASIT contract authority.

Publications Supported:
    - AMM (Aircraft Maintenance Manual)
    - SRM (Structural Repair Manual)
    - CMM (Component Maintenance Manual)
    - IPC (Illustrated Parts Catalog)
    - FCOM (Flight Crew Operating Manual)
    - TSM (Troubleshooting Manual)
    - WDM (Wiring Diagram Manual)
    - SB (Service Bulletin)
"""

from __future__ import annotations

import hashlib
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
from xml.etree import ElementTree as ET

logger = logging.getLogger(__name__)


class PublicationType(Enum):
    """S1000D publication types."""
    AMM = "amm"         # Aircraft Maintenance Manual
    SRM = "srm"         # Structural Repair Manual
    CMM = "cmm"         # Component Maintenance Manual
    IPC = "ipc"         # Illustrated Parts Catalog
    FCOM = "fcom"       # Flight Crew Operating Manual
    TSM = "tsm"         # Troubleshooting Manual
    WDM = "wdm"         # Wiring Diagram Manual
    SB = "sb"           # Service Bulletin
    IETP = "ietp"       # Interactive Electronic Technical Publication


@dataclass
class PMCode:
    """
    S1000D Publication Module Code (PMC) structure.
    
    Format: MODEL-PMIC-PMISSUER-PMNUMBER-PMVOLUME
    Example: HJ1-A-GAVIN-00001-00
    """
    model_ident_code: str           # 2-14 chars, aircraft model
    pm_issuer: str = "00001"        # PM issuer code
    pm_number: str = "00001"        # PM number
    pm_volume: str = "00"           # Volume number
    
    def __str__(self) -> str:
        """Generate PMC string representation."""
        return f"PMC-{self.model_ident_code}-{self.pm_issuer}-{self.pm_number}-{self.pm_volume}"
    
    @classmethod
    def from_string(cls, pmc_string: str) -> "PMCode":
        """Parse PMC from string representation."""
        # Remove PMC- prefix if present
        if pmc_string.startswith("PMC-"):
            pmc_string = pmc_string[4:]
        
        parts = pmc_string.split("-")
        if len(parts) < 4:
            raise ValueError(f"Invalid PMC format: {pmc_string}")
        
        return cls(
            model_ident_code=parts[0],
            pm_issuer=parts[1],
            pm_number=parts[2],
            pm_volume=parts[3] if len(parts) > 3 else "00",
        )


@dataclass
class PMEntry:
    """Entry in Publication Module (DM reference)."""
    dm_code: str
    dm_title: str
    entry_type: str = "dmRef"  # dmRef, pmRef, externalPubRef
    applicable_to: List[str] = field(default_factory=list)
    security_classification: str = "01"


@dataclass
class PMContent:
    """Publication Module content structure."""
    front_matter: List[PMEntry] = field(default_factory=list)
    chapters: Dict[str, List[PMEntry]] = field(default_factory=dict)  # ATA chapter -> DMs
    appendices: List[PMEntry] = field(default_factory=list)


@dataclass
class PMGenerationResult:
    """Result of PM generation operation."""
    success: bool
    pm_code: str
    publication_type: str
    output_path: Optional[Path] = None
    xml_content: Optional[str] = None
    dm_refs: List[str] = field(default_factory=list)
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    input_hash: Optional[str] = None
    output_hash: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())


class PMGenerator:
    """
    S1000D Publication Module Generator.
    
    Generates Publication Modules that organize Data Modules into
    deliverable technical publications. All generation is traced
    and auditable under ASIT contract authority.
    
    Attributes:
        contract: ASIT transformation contract
        config: Generator configuration
        
    Example:
        >>> contract = load_contract("KITDM-CTR-LM-CSDB_ATA28")
        >>> generator = PMGenerator(contract=contract, config=config)
        >>> result = generator.generate_publication(
        ...     pub_type=PublicationType.AMM,
        ...     dm_list=data_modules,
        ...     title="Aircraft Maintenance Manual",
        ... )
    """
    
    # S1000D Issue 5.0 namespace
    S1000D_NS = "http://www.s1000d.org/S1000D_5-0"
    
    # Publication type metadata
    PUB_METADATA = {
        PublicationType.AMM: {
            "title": "Aircraft Maintenance Manual",
            "short_title": "AMM",
            "description": "Maintenance procedures and instructions",
        },
        PublicationType.SRM: {
            "title": "Structural Repair Manual",
            "short_title": "SRM",
            "description": "Structural repair procedures",
        },
        PublicationType.CMM: {
            "title": "Component Maintenance Manual",
            "short_title": "CMM",
            "description": "Component-level maintenance",
        },
        PublicationType.IPC: {
            "title": "Illustrated Parts Catalog",
            "short_title": "IPC",
            "description": "Parts identification and ordering",
        },
        PublicationType.FCOM: {
            "title": "Flight Crew Operating Manual",
            "short_title": "FCOM",
            "description": "Flight operations procedures",
        },
        PublicationType.TSM: {
            "title": "Troubleshooting Manual",
            "short_title": "TSM",
            "description": "Fault isolation and troubleshooting",
        },
        PublicationType.WDM: {
            "title": "Wiring Diagram Manual",
            "short_title": "WDM",
            "description": "Electrical wiring diagrams",
        },
        PublicationType.SB: {
            "title": "Service Bulletin",
            "short_title": "SB",
            "description": "Service notifications and modifications",
        },
    }
    
    def __init__(
        self,
        contract: Dict[str, Any],
        config: Dict[str, Any],
    ):
        """
        Initialize PM Generator.
        
        Args:
            contract: ASIT transformation contract (required)
            config: Generator configuration
            
        Raises:
            ValueError: If contract is missing or invalid
        """
        if not contract:
            raise ValueError("ASIT contract is required for PM generation")
        
        self.contract = contract
        self.config = config
        
        # Extract contract parameters
        self.contract_id = contract.get("id", "UNKNOWN")
        self.baseline_ref = contract.get("source", {}).get("baseline", "UNKNOWN")
        self.model_code = config.get("model_ident_code", "XXX")
        
        # Generation tracking
        self._generation_log: List[PMGenerationResult] = []
        self._pm_counter = 0
        
        logger.info(
            f"PMGenerator initialized: contract={self.contract_id}, "
            f"baseline={self.baseline_ref}"
        )
    
    def generate_publication(
        self,
        pub_type: PublicationType,
        dm_list: List[Dict[str, Any]],
        title: Optional[str] = None,
        pmc: Optional[PMCode] = None,
    ) -> PMGenerationResult:
        """
        Generate a Publication Module for a specific publication type.
        
        Args:
            pub_type: Type of publication (AMM, SRM, etc.)
            dm_list: List of Data Modules to include
            title: Optional custom title
            pmc: Optional pre-defined PMC
            
        Returns:
            PMGenerationResult with XML content and trace info
        """
        # Build PMC if not provided
        if pmc is None:
            self._pm_counter += 1
            pmc = PMCode(
                model_ident_code=self.model_code,
                pm_number=f"{self._pm_counter:05d}",
            )
        
        # Get publication metadata
        pub_meta = self.PUB_METADATA.get(pub_type, {})
        pub_title = title or pub_meta.get("title", "Technical Publication")
        
        # Calculate input hash
        input_hash = self._compute_hash(str(dm_list))
        
        # Organize DMs by ATA chapter
        content = self._organize_dm_list(dm_list)
        
        # Generate XML structure
        root = self._create_pm_root()
        
        # Add identification section
        ident_section = self._build_pm_ident_section(pmc, pub_title, pub_type)
        root.append(ident_section)
        
        # Add content section with DM references
        content_section = self._build_pm_content(content, pub_type)
        root.append(content_section)
        
        # Serialize to XML
        xml_content = self._serialize_xml(root)
        output_hash = self._compute_hash(xml_content)
        
        # Build result
        dm_refs = [dm.get("dm_code", dm.get("id", "unknown")) for dm in dm_list]
        
        result = PMGenerationResult(
            success=True,
            pm_code=str(pmc),
            publication_type=pub_type.value,
            xml_content=xml_content,
            dm_refs=dm_refs,
            input_hash=input_hash,
            output_hash=output_hash,
        )
        
        self._generation_log.append(result)
        return result
    
    def generate_amm(
        self,
        dm_list: List[Dict[str, Any]],
        title: str = "Aircraft Maintenance Manual",
    ) -> PMGenerationResult:
        """Generate an Aircraft Maintenance Manual (AMM) Publication Module."""
        return self.generate_publication(PublicationType.AMM, dm_list, title)
    
    def generate_srm(
        self,
        dm_list: List[Dict[str, Any]],
        title: str = "Structural Repair Manual",
    ) -> PMGenerationResult:
        """Generate a Structural Repair Manual (SRM) Publication Module."""
        return self.generate_publication(PublicationType.SRM, dm_list, title)
    
    def generate_cmm(
        self,
        dm_list: List[Dict[str, Any]],
        title: str = "Component Maintenance Manual",
    ) -> PMGenerationResult:
        """Generate a Component Maintenance Manual (CMM) Publication Module."""
        return self.generate_publication(PublicationType.CMM, dm_list, title)
    
    def generate_ipc(
        self,
        dm_list: List[Dict[str, Any]],
        title: str = "Illustrated Parts Catalog",
    ) -> PMGenerationResult:
        """Generate an Illustrated Parts Catalog (IPC) Publication Module."""
        return self.generate_publication(PublicationType.IPC, dm_list, title)
    
    def generate_sb(
        self,
        dm_list: List[Dict[str, Any]],
        sb_number: str,
        title: Optional[str] = None,
    ) -> PMGenerationResult:
        """
        Generate a Service Bulletin (SB) Publication Module.
        
        Args:
            dm_list: Data Modules for the SB
            sb_number: Service Bulletin number
            title: Optional custom title
        """
        sb_title = title or f"Service Bulletin {sb_number}"
        return self.generate_publication(PublicationType.SB, dm_list, sb_title)
    
    def generate_toc(
        self,
        pm_result: PMGenerationResult,
    ) -> str:
        """
        Generate Table of Contents for a Publication Module.
        
        Args:
            pm_result: Previously generated PM result
            
        Returns:
            TOC as formatted string
        """
        toc_lines = [
            "=" * 60,
            f"TABLE OF CONTENTS",
            f"Publication: {pm_result.pm_code}",
            f"Type: {pm_result.publication_type.upper()}",
            "=" * 60,
            "",
        ]
        
        for i, dm_ref in enumerate(pm_result.dm_refs, 1):
            toc_lines.append(f"  {i:03d}. {dm_ref}")
        
        toc_lines.extend([
            "",
            "=" * 60,
            f"Total Data Modules: {len(pm_result.dm_refs)}",
            f"Generated: {pm_result.generated_at}",
            "=" * 60,
        ])
        
        return "\n".join(toc_lines)
    
    def _organize_dm_list(
        self,
        dm_list: List[Dict[str, Any]],
    ) -> PMContent:
        """Organize DM list into publication structure."""
        content = PMContent()
        
        for dm in dm_list:
            dm_code = dm.get("dm_code", dm.get("id", "unknown"))
            dm_title = dm.get("title", dm.get("tech_name", "Data Module"))
            ata_chapter = dm.get("ata_chapter", "00")
            
            entry = PMEntry(
                dm_code=dm_code,
                dm_title=dm_title,
                applicable_to=dm.get("applicability", []),
            )
            
            # Organize by ATA chapter
            chapter_key = str(ata_chapter).zfill(2)
            if chapter_key not in content.chapters:
                content.chapters[chapter_key] = []
            content.chapters[chapter_key].append(entry)
        
        return content
    
    def _create_pm_root(self) -> ET.Element:
        """Create S1000D pm (publication module) root element."""
        root = ET.Element("pm")
        root.set("xmlns", self.S1000D_NS)
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        return root
    
    def _build_pm_ident_section(
        self,
        pmc: PMCode,
        title: str,
        pub_type: PublicationType,
    ) -> ET.Element:
        """Build PM identification section."""
        section = ET.Element("identAndStatusSection")
        
        # pmAddress
        pm_address = ET.SubElement(section, "pmAddress")
        
        # pmIdent
        pm_ident = ET.SubElement(pm_address, "pmIdent")
        
        # pmCode
        pm_code = ET.SubElement(pm_ident, "pmCode")
        pm_code.set("modelIdentCode", pmc.model_ident_code)
        pm_code.set("pmIssuer", pmc.pm_issuer)
        pm_code.set("pmNumber", pmc.pm_number)
        pm_code.set("pmVolume", pmc.pm_volume)
        
        # language
        language = ET.SubElement(pm_ident, "language")
        language.set("languageIsoCode", "en")
        language.set("countryIsoCode", "US")
        
        # issueInfo
        issue_info = ET.SubElement(pm_ident, "issueInfo")
        issue_info.set("issueNumber", "001")
        issue_info.set("inWork", "00")
        
        # pmAddressItems
        pm_address_items = ET.SubElement(pm_address, "pmAddressItems")
        
        # issueDate
        issue_date = ET.SubElement(pm_address_items, "issueDate")
        now = datetime.now()
        issue_date.set("year", str(now.year))
        issue_date.set("month", f"{now.month:02d}")
        issue_date.set("day", f"{now.day:02d}")
        
        # pmTitle
        pm_title = ET.SubElement(pm_address_items, "pmTitle")
        pm_title.text = title
        
        # shortPmTitle
        pub_meta = self.PUB_METADATA.get(pub_type, {})
        short_pm_title = ET.SubElement(pm_address_items, "shortPmTitle")
        short_pm_title.text = pub_meta.get("short_title", pub_type.value.upper())
        
        # pmStatus
        pm_status = ET.SubElement(section, "pmStatus")
        pm_status.set("issueType", "new")
        
        # security
        security = ET.SubElement(pm_status, "security")
        security.set("securityClassification", "01")
        
        # responsiblePartnerCompany
        rpc = ET.SubElement(pm_status, "responsiblePartnerCompany")
        enterprise = ET.SubElement(rpc, "enterpriseName")
        enterprise.text = self.config.get("organization", "AEROSPACEMODEL")
        
        return section
    
    def _build_pm_content(
        self,
        content: PMContent,
        pub_type: PublicationType,
    ) -> ET.Element:
        """Build PM content section with DM references."""
        pm_content = ET.Element("content")
        pm_entry = ET.SubElement(pm_content, "pmEntry")
        
        # Add publication title
        pm_entry_title = ET.SubElement(pm_entry, "pmEntryTitle")
        pub_meta = self.PUB_METADATA.get(pub_type, {})
        pm_entry_title.text = pub_meta.get("title", "Technical Publication")
        
        # Add chapters
        for chapter, entries in sorted(content.chapters.items()):
            chapter_entry = ET.SubElement(pm_entry, "pmEntry")
            
            # Chapter title
            chapter_title = ET.SubElement(chapter_entry, "pmEntryTitle")
            chapter_title.text = f"ATA Chapter {chapter}"
            
            # DM references
            for entry in entries:
                dm_ref_element = self._build_dm_ref(entry)
                chapter_entry.append(dm_ref_element)
        
        return pm_content
    
    def _build_dm_ref(self, entry: PMEntry) -> ET.Element:
        """Build dmRef element."""
        dm_ref = ET.Element("dmRef")
        dm_ref_ident = ET.SubElement(dm_ref, "dmRefIdent")
        
        # Parse DMC from string
        dm_code = ET.SubElement(dm_ref_ident, "dmCode")
        
        # Try to parse the DMC string
        dmc_parts = entry.dm_code.split("-")
        if len(dmc_parts) >= 11:
            dm_code.set("modelIdentCode", dmc_parts[0])
            dm_code.set("systemDiffCode", dmc_parts[1])
            dm_code.set("systemCode", dmc_parts[2])
            dm_code.set("subSystemCode", dmc_parts[3])
            dm_code.set("subSubSystemCode", dmc_parts[4])
            dm_code.set("assyCode", dmc_parts[5])
            dm_code.set("disassyCode", dmc_parts[6])
            dm_code.set("disassyCodeVariant", dmc_parts[7])
            dm_code.set("infoCode", dmc_parts[8])
            dm_code.set("infoCodeVariant", dmc_parts[9])
            dm_code.set("itemLocationCode", dmc_parts[10])
        else:
            # Fallback for non-standard codes
            dm_code.set("modelIdentCode", entry.dm_code)
        
        # dmRefAddressItems
        dm_ref_address = ET.SubElement(dm_ref, "dmRefAddressItems")
        dm_title = ET.SubElement(dm_ref_address, "dmTitle")
        tech_name = ET.SubElement(dm_title, "techName")
        tech_name.text = entry.dm_title
        
        return dm_ref
    
    def _serialize_xml(self, root: ET.Element) -> str:
        """Serialize XML element to string."""
        ET.indent(root, space="  ")
        return ET.tostring(root, encoding="unicode", xml_declaration=True)
    
    def _compute_hash(self, content: str) -> str:
        """Compute SHA-256 hash of content."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()
    
    def get_generation_log(self) -> List[PMGenerationResult]:
        """Get log of all generation operations."""
        return self._generation_log.copy()
    
    def get_trace_matrix(self) -> List[Dict[str, Any]]:
        """
        Generate traceability matrix for all generated PMs.
        
        Returns:
            List of trace records linking DMs to publications
        """
        trace_records = []
        for result in self._generation_log:
            trace_records.append({
                "contract_id": self.contract_id,
                "baseline_ref": self.baseline_ref,
                "publication_type": result.publication_type,
                "pm_code": result.pm_code,
                "dm_refs": result.dm_refs,
                "trace_id": result.trace_id,
                "input_hash": result.input_hash,
                "output_hash": result.output_hash,
                "generated_at": result.generated_at,
                "success": result.success,
            })
        return trace_records
