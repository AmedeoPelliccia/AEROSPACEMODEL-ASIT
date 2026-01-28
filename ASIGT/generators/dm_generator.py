# =============================================================================
# ASIGT Data Module Generator
# S1000D Data Module generation under ASIT contract authority
# Version: 2.0.0
# =============================================================================
"""
Data Module Generator

Generates S1000D-compliant Data Modules (DM) from KDB source artifacts.
Operates exclusively under ASIT contract authority.

Supported DM Types:
    - Descriptive (descript)
    - Procedural (proced)
    - Fault Isolation (fault)
    - Illustrated Parts Data (ipd)
    - Crew/Operator (crew)
    - Process (process)
    - Wiring Data (wrngdata)
    - Front Matter (frontmatter)
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


class DMType(Enum):
    """S1000D Data Module information types."""
    DESCRIPTIVE = "descript"
    PROCEDURAL = "proced"
    FAULT = "fault"
    IPD = "ipd"
    CREW = "crew"
    PROCESS = "process"
    WIRING = "wrngdata"
    FRONT_MATTER = "frontmatter"


@dataclass
class DMCode:
    """
    S1000D Data Module Code (DMC) structure.
    
    Format: MODEL-SYSTEM-SUBSYSTEM-SUBSUBSYSTEM-ASSY-DISASSY-DISASSYV-INFOCODE-INFOCODEVAR-ITEMLOC
    Example: HJ1-28-10-00-00A-040A-A
    """
    model_ident_code: str           # 2-14 chars, aircraft model
    system_diff_code: str = "A"     # 1-4 chars, system difference
    system_code: str = "00"         # 2-3 chars, ATA chapter
    sub_system_code: str = "0"      # 1 char
    sub_sub_system_code: str = "0"  # 1 char
    assy_code: str = "00"           # 2-4 chars
    disassy_code: str = "00"        # 2 chars
    disassy_code_variant: str = "A" # 1-3 chars
    info_code: str = "040"          # 3 chars, information code
    info_code_variant: str = "A"    # 1 char
    item_location_code: str = "A"   # 1 char
    learn_code: Optional[str] = None
    learn_event_code: Optional[str] = None
    
    def __str__(self) -> str:
        """Generate DMC string representation."""
        parts = [
            self.model_ident_code,
            self.system_diff_code,
            self.system_code,
            self.sub_system_code,
            self.sub_sub_system_code,
            self.assy_code,
            self.disassy_code,
            self.disassy_code_variant,
            self.info_code,
            self.info_code_variant,
            self.item_location_code,
        ]
        return "-".join(parts)
    
    @classmethod
    def from_string(cls, dmc_string: str) -> "DMCode":
        """Parse DMC from string representation."""
        parts = dmc_string.split("-")
        if len(parts) < 11:
            raise ValueError(f"Invalid DMC format: {dmc_string}")
        return cls(
            model_ident_code=parts[0],
            system_diff_code=parts[1],
            system_code=parts[2],
            sub_system_code=parts[3],
            sub_sub_system_code=parts[4],
            assy_code=parts[5],
            disassy_code=parts[6],
            disassy_code_variant=parts[7],
            info_code=parts[8],
            info_code_variant=parts[9],
            item_location_code=parts[10],
        )


@dataclass
class DMIdentification:
    """Data Module identification metadata."""
    dmc: DMCode
    language: str = "en-US"
    issue_number: str = "001"
    in_work: str = "00"
    issue_date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    security_classification: str = "01"  # 01 = Unclassified
    responsible_partner_company: Optional[str] = None
    originator: Optional[str] = None


@dataclass
class DMStatus:
    """Data Module status information."""
    issue_type: str = "new"  # new, changed, deleted, rinstatement
    brex_dm_ref: Optional[str] = None
    quality_assurance: str = "unverified"
    applicable_to: List[str] = field(default_factory=list)


@dataclass
class GenerationResult:
    """Result of DM generation operation."""
    success: bool
    dm_code: str
    output_path: Optional[Path] = None
    xml_content: Optional[str] = None
    source_refs: List[str] = field(default_factory=list)
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    input_hash: Optional[str] = None
    output_hash: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())


class DMGenerator:
    """
    S1000D Data Module Generator.
    
    Generates Data Modules from KDB sources under ASIT contract authority.
    All generation is traced and auditable.
    
    Attributes:
        contract: ASIT transformation contract
        config: Generator configuration
        template_path: Path to S1000D XML templates
        
    Example:
        >>> contract = load_contract("KITDM-CTR-LM-CSDB_ATA28")
        >>> generator = DMGenerator(contract=contract, config=config)
        >>> result = generator.generate_descriptive(
        ...     source=requirement_data,
        ...     dmc=DMCode(model_ident_code="HJ1", system_code="28"),
        ... )
    """
    
    # S1000D Issue 5.0 namespace
    S1000D_NS = "http://www.s1000d.org/S1000D_5-0"
    
    # Information code mappings (common codes)
    INFO_CODES = {
        "description": "040",       # Description and operation
        "procedure": "520",         # Removal procedure
        "fault_isolation": "300",   # Fault isolation
        "ipd": "941",              # Illustrated parts data
        "servicing": "200",        # Servicing
        "inspection": "100",       # Inspection/check
        "cleaning": "250",         # Cleaning
        "testing": "400",          # Testing and fault isolation
        "repair": "600",           # Repair
        "removal": "520",          # Removal
        "installation": "540",     # Installation
    }
    
    def __init__(
        self,
        contract: Dict[str, Any],
        config: Dict[str, Any],
        template_path: Optional[Path] = None,
    ):
        """
        Initialize DM Generator.
        
        Args:
            contract: ASIT transformation contract (required)
            config: Generator configuration
            template_path: Path to S1000D XML templates
            
        Raises:
            ValueError: If contract is missing or invalid
        """
        if not contract:
            raise ValueError("ASIT contract is required for DM generation")
        
        self.contract = contract
        self.config = config
        self.template_path = template_path or Path("ASIGT/s1000d_templates")
        
        # Extract contract parameters
        self.contract_id = contract.get("id", "UNKNOWN")
        self.baseline_ref = contract.get("source", {}).get("baseline", "UNKNOWN")
        self.model_code = config.get("model_ident_code", "XXX")
        
        # Generation tracking
        self._generation_log: List[GenerationResult] = []
        
        logger.info(
            f"DMGenerator initialized: contract={self.contract_id}, "
            f"baseline={self.baseline_ref}"
        )
    
    def generate(
        self,
        sources: List[Dict[str, Any]],
        dm_type: DMType = DMType.DESCRIPTIVE,
    ) -> List[GenerationResult]:
        """
        Generate Data Modules from source artifacts.
        
        Args:
            sources: List of KDB source artifacts
            dm_type: Type of DM to generate
            
        Returns:
            List of generation results with trace information
        """
        results = []
        
        for source in sources:
            try:
                if dm_type == DMType.DESCRIPTIVE:
                    result = self.generate_descriptive(source)
                elif dm_type == DMType.PROCEDURAL:
                    result = self.generate_procedural(source)
                elif dm_type == DMType.FAULT:
                    result = self.generate_fault_isolation(source)
                elif dm_type == DMType.IPD:
                    result = self.generate_ipd(source)
                else:
                    result = self.generate_descriptive(source)
                
                results.append(result)
                self._generation_log.append(result)
                
            except Exception as e:
                logger.error(f"Generation failed for source {source.get('id')}: {e}")
                results.append(GenerationResult(
                    success=False,
                    dm_code="FAILED",
                    errors=[str(e)],
                    source_refs=[source.get("id", "unknown")],
                ))
        
        return results
    
    def generate_descriptive(
        self,
        source: Dict[str, Any],
        dmc: Optional[DMCode] = None,
    ) -> GenerationResult:
        """
        Generate a descriptive Data Module.
        
        Args:
            source: KDB source data (requirement, design doc, etc.)
            dmc: Optional pre-defined DMC, otherwise auto-generated
            
        Returns:
            GenerationResult with XML content and trace info
        """
        # Build DMC if not provided
        if dmc is None:
            dmc = self._build_dmc(source, info_code="040")
        
        # Calculate input hash for traceability
        input_hash = self._compute_hash(str(source))
        
        # Build identification
        ident = DMIdentification(
            dmc=dmc,
            language=self.config.get("default_language", "en-US"),
            security_classification=self.config.get("security_classification", "01"),
            responsible_partner_company=self.config.get("organization"),
            originator=self.config.get("organization"),
        )
        
        # Generate XML structure
        root = self._create_dmodule_root()
        
        # Add identification section
        ident_section = self._build_ident_section(ident)
        root.append(ident_section)
        
        # Add status section
        status = DMStatus(
            brex_dm_ref=self.config.get("brex_dm_ref"),
            applicable_to=source.get("applicability", []),
        )
        status_section = self._build_status_section(status)
        root.append(status_section)
        
        # Add content section
        content = self._build_descriptive_content(source)
        root.append(content)
        
        # Serialize to XML
        xml_content = self._serialize_xml(root)
        output_hash = self._compute_hash(xml_content)
        
        return GenerationResult(
            success=True,
            dm_code=str(dmc),
            xml_content=xml_content,
            source_refs=[source.get("id", "unknown")],
            input_hash=input_hash,
            output_hash=output_hash,
        )
    
    def generate_procedural(
        self,
        source: Dict[str, Any],
        dmc: Optional[DMCode] = None,
    ) -> GenerationResult:
        """
        Generate a procedural Data Module.
        
        Args:
            source: KDB task/procedure data
            dmc: Optional pre-defined DMC
            
        Returns:
            GenerationResult with procedural DM
        """
        if dmc is None:
            dmc = self._build_dmc(source, info_code="520")
        
        input_hash = self._compute_hash(str(source))
        
        ident = DMIdentification(
            dmc=dmc,
            language=self.config.get("default_language", "en-US"),
            security_classification=self.config.get("security_classification", "01"),
        )
        
        root = self._create_dmodule_root()
        root.append(self._build_ident_section(ident))
        root.append(self._build_status_section(DMStatus()))
        
        # Build procedural content
        content = self._build_procedural_content(source)
        root.append(content)
        
        xml_content = self._serialize_xml(root)
        output_hash = self._compute_hash(xml_content)
        
        return GenerationResult(
            success=True,
            dm_code=str(dmc),
            xml_content=xml_content,
            source_refs=[source.get("id", "unknown")],
            input_hash=input_hash,
            output_hash=output_hash,
        )
    
    def generate_fault_isolation(
        self,
        source: Dict[str, Any],
        dmc: Optional[DMCode] = None,
    ) -> GenerationResult:
        """
        Generate a fault isolation Data Module.
        
        Args:
            source: KDB fault/troubleshooting data
            dmc: Optional pre-defined DMC
            
        Returns:
            GenerationResult with fault isolation DM
        """
        if dmc is None:
            dmc = self._build_dmc(source, info_code="300")
        
        input_hash = self._compute_hash(str(source))
        
        ident = DMIdentification(
            dmc=dmc,
            language=self.config.get("default_language", "en-US"),
        )
        
        root = self._create_dmodule_root()
        root.append(self._build_ident_section(ident))
        root.append(self._build_status_section(DMStatus()))
        
        # Build fault isolation content
        content = self._build_fault_content(source)
        root.append(content)
        
        xml_content = self._serialize_xml(root)
        output_hash = self._compute_hash(xml_content)
        
        return GenerationResult(
            success=True,
            dm_code=str(dmc),
            xml_content=xml_content,
            source_refs=[source.get("id", "unknown")],
            input_hash=input_hash,
            output_hash=output_hash,
        )
    
    def generate_ipd(
        self,
        source: Dict[str, Any],
        dmc: Optional[DMCode] = None,
    ) -> GenerationResult:
        """
        Generate an Illustrated Parts Data (IPD) Data Module.
        
        Args:
            source: KDB parts data
            dmc: Optional pre-defined DMC
            
        Returns:
            GenerationResult with IPD DM
        """
        if dmc is None:
            dmc = self._build_dmc(source, info_code="941")
        
        input_hash = self._compute_hash(str(source))
        
        ident = DMIdentification(
            dmc=dmc,
            language=self.config.get("default_language", "en-US"),
        )
        
        root = self._create_dmodule_root()
        root.append(self._build_ident_section(ident))
        root.append(self._build_status_section(DMStatus()))
        
        # Build IPD content
        content = self._build_ipd_content(source)
        root.append(content)
        
        xml_content = self._serialize_xml(root)
        output_hash = self._compute_hash(xml_content)
        
        return GenerationResult(
            success=True,
            dm_code=str(dmc),
            xml_content=xml_content,
            source_refs=[source.get("id", "unknown")],
            input_hash=input_hash,
            output_hash=output_hash,
        )
    
    def _build_dmc(self, source: Dict[str, Any], info_code: str) -> DMCode:
        """Build DMC from source artifact."""
        ata_chapter = source.get("ata_chapter", "00")
        ata_section = source.get("ata_section", "0")
        ata_subject = source.get("ata_subject", "0")
        
        return DMCode(
            model_ident_code=self.model_code,
            system_code=str(ata_chapter).zfill(2),
            sub_system_code=str(ata_section)[0] if ata_section else "0",
            sub_sub_system_code=str(ata_subject)[0] if ata_subject else "0",
            info_code=info_code,
        )
    
    def _create_dmodule_root(self) -> ET.Element:
        """Create S1000D dmodule root element."""
        root = ET.Element("dmodule")
        root.set("xmlns", self.S1000D_NS)
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        return root
    
    def _build_ident_section(self, ident: DMIdentification) -> ET.Element:
        """Build identAndStatusSection."""
        section = ET.Element("identAndStatusSection")
        
        # dmAddress
        dm_address = ET.SubElement(section, "dmAddress")
        
        # dmIdent
        dm_ident = ET.SubElement(dm_address, "dmIdent")
        
        # dmCode
        dm_code = ET.SubElement(dm_ident, "dmCode")
        dm_code.set("modelIdentCode", ident.dmc.model_ident_code)
        dm_code.set("systemDiffCode", ident.dmc.system_diff_code)
        dm_code.set("systemCode", ident.dmc.system_code)
        dm_code.set("subSystemCode", ident.dmc.sub_system_code)
        dm_code.set("subSubSystemCode", ident.dmc.sub_sub_system_code)
        dm_code.set("assyCode", ident.dmc.assy_code)
        dm_code.set("disassyCode", ident.dmc.disassy_code)
        dm_code.set("disassyCodeVariant", ident.dmc.disassy_code_variant)
        dm_code.set("infoCode", ident.dmc.info_code)
        dm_code.set("infoCodeVariant", ident.dmc.info_code_variant)
        dm_code.set("itemLocationCode", ident.dmc.item_location_code)
        
        # language
        language = ET.SubElement(dm_ident, "language")
        lang_parts = ident.language.split("-")
        language.set("languageIsoCode", lang_parts[0])
        if len(lang_parts) > 1:
            language.set("countryIsoCode", lang_parts[1])
        
        # issueInfo
        issue_info = ET.SubElement(dm_ident, "issueInfo")
        issue_info.set("issueNumber", ident.issue_number)
        issue_info.set("inWork", ident.in_work)
        
        # dmAddressItems
        dm_address_items = ET.SubElement(dm_address, "dmAddressItems")
        issue_date = ET.SubElement(dm_address_items, "issueDate")
        date_parts = ident.issue_date.split("-")
        issue_date.set("year", date_parts[0])
        issue_date.set("month", date_parts[1])
        issue_date.set("day", date_parts[2])
        
        # dmTitle
        dm_title = ET.SubElement(dm_address_items, "dmTitle")
        tech_name = ET.SubElement(dm_title, "techName")
        tech_name.text = "Generated Data Module"  # To be filled from source
        
        return section
    
    def _build_status_section(self, status: DMStatus) -> ET.Element:
        """Build dmStatus section."""
        dm_status = ET.Element("dmStatus")
        dm_status.set("issueType", status.issue_type)
        
        # Security
        security = ET.SubElement(dm_status, "security")
        security.set("securityClassification", "01")
        
        # Responsible partner company
        rpc = ET.SubElement(dm_status, "responsiblePartnerCompany")
        enterprise = ET.SubElement(rpc, "enterpriseName")
        enterprise.text = self.config.get("organization", "AEROSPACEMODEL")
        
        # Originator
        originator = ET.SubElement(dm_status, "originator")
        orig_enterprise = ET.SubElement(originator, "enterpriseName")
        orig_enterprise.text = self.config.get("organization", "AEROSPACEMODEL")
        
        # Quality assurance
        qa = ET.SubElement(dm_status, "qualityAssurance")
        qa.set("status", status.quality_assurance)
        
        return dm_status
    
    def _build_descriptive_content(self, source: Dict[str, Any]) -> ET.Element:
        """Build content section for descriptive DM."""
        content = ET.Element("content")
        descript = ET.SubElement(content, "descript")
        
        # Description paragraphs
        description = source.get("description", source.get("content", ""))
        if isinstance(description, str):
            description = [description]
        
        for para_text in description:
            para = ET.SubElement(descript, "para")
            para.text = para_text
        
        return content
    
    def _build_procedural_content(self, source: Dict[str, Any]) -> ET.Element:
        """Build content section for procedural DM."""
        content = ET.Element("content")
        procedure = ET.SubElement(content, "procedure")
        
        # Preliminary requirements
        prelim_reqs = ET.SubElement(procedure, "preliminaryRqmts")
        req_conditions = ET.SubElement(prelim_reqs, "reqCondGroup")
        no_conds = ET.SubElement(req_conditions, "noConds")
        no_conds.text = "None"
        
        # Main procedure
        main_proc = ET.SubElement(procedure, "mainProcedure")
        
        steps = source.get("steps", source.get("tasks", []))
        for i, step_data in enumerate(steps, 1):
            proc_step = ET.SubElement(main_proc, "proceduralStep")
            proc_step.set("id", f"step-{i:03d}")
            
            para = ET.SubElement(proc_step, "para")
            if isinstance(step_data, dict):
                para.text = step_data.get("instruction", str(step_data))
            else:
                para.text = str(step_data)
        
        # Close requirements
        close_reqs = ET.SubElement(procedure, "closeRqmts")
        no_close = ET.SubElement(close_reqs, "noCloseReqs")
        
        return content
    
    def _build_fault_content(self, source: Dict[str, Any]) -> ET.Element:
        """Build content section for fault isolation DM."""
        content = ET.Element("content")
        fault_iso = ET.SubElement(content, "faultIsolation")
        
        # Fault info
        faults = source.get("faults", [source])
        for fault_data in faults:
            fault = ET.SubElement(fault_iso, "fault")
            
            # Fault description
            fault_descr = ET.SubElement(fault, "faultDescr")
            descr_para = ET.SubElement(fault_descr, "para")
            descr_para.text = fault_data.get("description", "Fault description")
            
            # Isolation procedure
            iso_proc = ET.SubElement(fault, "isolationProcedure")
            iso_step = ET.SubElement(iso_proc, "isolationStep")
            iso_para = ET.SubElement(iso_step, "para")
            iso_para.text = fault_data.get("isolation_procedure", "Isolation step")
        
        return content
    
    def _build_ipd_content(self, source: Dict[str, Any]) -> ET.Element:
        """Build content section for IPD DM."""
        content = ET.Element("content")
        ipd = ET.SubElement(content, "illustratedPartsCatalog")
        
        # Figure section (placeholder)
        figure = ET.SubElement(ipd, "figure")
        figure.set("id", "fig-001")
        
        title = ET.SubElement(figure, "title")
        title.text = source.get("figure_title", "Parts Breakdown")
        
        # Parts list
        catalog_seq = ET.SubElement(ipd, "catalogSeqNumber")
        
        parts = source.get("parts", [])
        for part in parts:
            item = ET.SubElement(catalog_seq, "itemSeqNumber")
            item.set("itemSeqNumberValue", part.get("sequence", "001"))
            
            part_ref = ET.SubElement(item, "partRef")
            part_ref.set("manufacturerCodeValue", part.get("mfr_code", "00000"))
            part_ref.set("partNumberValue", part.get("part_number", "UNKNOWN"))
            
            qty = ET.SubElement(item, "quantityPerNextHigherAssy")
            qty.text = str(part.get("quantity", 1))
        
        return content
    
    def _serialize_xml(self, root: ET.Element) -> str:
        """Serialize XML element to string."""
        ET.indent(root, space="  ")
        return ET.tostring(root, encoding="unicode", xml_declaration=True)
    
    def _compute_hash(self, content: str) -> str:
        """Compute SHA-256 hash of content."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()
    
    def get_generation_log(self) -> List[GenerationResult]:
        """Get log of all generation operations."""
        return self._generation_log.copy()
    
    def get_trace_matrix(self) -> List[Dict[str, Any]]:
        """
        Generate traceability matrix for all generated DMs.
        
        Returns:
            List of trace records linking sources to outputs
        """
        trace_records = []
        for result in self._generation_log:
            trace_records.append({
                "contract_id": self.contract_id,
                "baseline_ref": self.baseline_ref,
                "source_refs": result.source_refs,
                "output_dm": result.dm_code,
                "trace_id": result.trace_id,
                "input_hash": result.input_hash,
                "output_hash": result.output_hash,
                "generated_at": result.generated_at,
                "success": result.success,
            })
        return trace_records
