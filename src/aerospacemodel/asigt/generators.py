"""
ASIGT Generators Module

S1000D content generators operating EXCLUSIVELY under ASIT contract authority.

This module provides generators for:
    - Data Modules (DM): Descriptive, Procedural, Fault Isolation, IPD
    - Publication Modules (PM): AMM, SRM, CMM, IPC structure
    - Data Module Lists (DML): CSDB inventory and delivery lists
    - Information Control Numbers (ICN): Graphics and multimedia
    - Applicability: ACT/PCT/CCT processing

CRITICAL CONSTRAINT:
    ASIGT cannot operate standalone.
    All generators require a valid ASIT contract to execute.
    Generation scope is governed by ASIT baselines and contracts.

Generation Process:
    1. Receive sources from KDB (under ASIT baseline)
    2. Load appropriate mapping rules
    3. Apply transformation rules
    4. Generate S1000D XML artifacts
    5. Return artifacts for validation and packaging
"""

from __future__ import annotations

import hashlib
import logging
import re
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Protocol,
    Set,
    Tuple,
    Type,
    Union,
)
from xml.etree import ElementTree as ET
from xml.dom import minidom

import yaml

from .engine import (
    ArtifactType,
    SourceArtifact,
    OutputArtifact,
    TraceLink,
    ExecutionContext,
    ASIGTError,
    ASIGTTransformationError,
)


logger = logging.getLogger(__name__)


# =============================================================================
# ENUMERATIONS
# =============================================================================


class DMType(Enum):
    """Data Module types per S1000D."""
    DESCRIPTIVE = "descriptive"
    PROCEDURAL = "procedural"
    FAULT_ISOLATION = "fault_isolation"
    IPD = "ipd"
    SCHEMATIC = "schematic"
    CREW = "crew"
    BREX = "brex"
    SCORMCONTENTPACKAGE = "scormcontentpackage"


class InfoCodeCategory(Enum):
    """S1000D Information Code categories."""
    GENERAL = "000"                    # General information
    DESCRIPTION = "040"                 # Description/operation
    PROCEDURE = "100"                   # Operations
    SERVICING = "200"                   # Servicing
    INSPECTION = "300"                  # Examine/inspect
    FAULT_ISOLATION = "400"             # Fault isolation
    DISCONNECT_CONNECT = "500"          # Disconnect/connect
    REMOVAL = "510"                     # Removal
    INSTALLATION = "520"                # Installation
    TESTING = "700"                     # Testing/checking
    STORAGE = "800"                     # Storage
    CLEANING = "900"                    # Cleaning/painting
    IPD = "941"                         # Illustrated parts data


class PublicationType(Enum):
    """Publication Module types."""
    AMM = "amm"                         # Aircraft Maintenance Manual
    SRM = "srm"                         # Structural Repair Manual
    CMM = "cmm"                         # Component Maintenance Manual
    IPC = "ipc"                         # Illustrated Parts Catalog
    FCOM = "fcom"                       # Flight Crew Operating Manual
    TSM = "tsm"                         # Troubleshooting Manual
    WDM = "wdm"                         # Wiring Diagram Manual
    SB = "sb"                           # Service Bulletin
    IETP = "ietp"                       # Interactive Electronic Technical Publication


class DMLType(Enum):
    """Data Module List types."""
    CSDB = "C"                          # CSDB content inventory
    DELIVERY = "S"                      # Delivery (shipment)
    CHANGE = "E"                        # Change/amendment
    COMMENT = "T"                       # Comment
    PRODUCTION = "P"                    # Production


class ApplicabilityType(Enum):
    """Applicability cross-reference table types."""
    ACT = "act"                         # Applicability Cross-reference Table
    PCT = "pct"                         # Product Cross-reference Table
    CCT = "cct"                         # Conditions Cross-reference Table


class SecurityClassification(Enum):
    """Security classification codes."""
    UNCLASSIFIED = "01"
    RESTRICTED = "02"
    CONFIDENTIAL = "03"
    SECRET = "04"
    TOP_SECRET = "05"


class MaintenanceLevel(Enum):
    """Maintenance level codes."""
    ORGANIZATIONAL = "O"                # O-level / Line maintenance
    INTERMEDIATE = "I"                  # I-level / Base maintenance
    DEPOT = "D"                         # D-level / Heavy maintenance
    SPECIALIZED = "S"                   # Specialized repair


class QualityAssuranceStatus(Enum):
    """QA verification status."""
    UNVERIFIED = "unverified"
    FIRST_VERIFICATION = "firstVerification"
    SECOND_VERIFICATION = "secondVerification"
    VERIFIED = "verified"


# =============================================================================
# DATA CLASSES - DATA MODULE CODE (DMC)
# =============================================================================


@dataclass
class DMCode:
    """
    S1000D Data Module Code structure.
    
    Format: MODEL-SYSDIFF-SYSTEM-SUBSYS-SUBSUBSYS-ASSY-DISASSY-DISASSYVAR-INFO-INFOVAR-ITEMLOC
    Example: HJONE-A-28-10-00-00A-510A-D
    """
    model_ident_code: str               # 2-14 alphanumeric
    system_diff_code: str = "A"         # 1-4 alphanumeric
    system_code: str = "00"             # 2-3 alphanumeric (ATA chapter)
    subsystem_code: str = "0"           # 1 alphanumeric
    sub_subsystem_code: str = "0"       # 1 alphanumeric
    assy_code: str = "00"               # 2-4 alphanumeric
    disassy_code: str = "00"            # 2 alphanumeric
    disassy_code_variant: str = "A"     # 1-3 alphanumeric
    info_code: str = "040"              # 3 alphanumeric
    info_code_variant: str = "A"        # 1 alphanumeric
    item_location_code: str = "D"       # 1 alphanumeric (A=wing, B=fuselage, etc.)
    
    def __str__(self) -> str:
        """Return full DMC string."""
        return (
            f"{self.model_ident_code}-{self.system_diff_code}-"
            f"{self.system_code}-{self.subsystem_code}{self.sub_subsystem_code}-"
            f"{self.assy_code}-{self.disassy_code}{self.disassy_code_variant}-"
            f"{self.info_code}{self.info_code_variant}-{self.item_location_code}"
        )
    
    @classmethod
    def from_string(cls, dmc_str: str) -> "DMCode":
        """Parse DMC from string."""
        # Pattern: MODEL-SYSDIFF-SYSTEM-SUBSYS-ASSY-DISASSY-INFO-LOC
        pattern = r"^([A-Z0-9]+)-([A-Z0-9]+)-(\d{2,3})-(\d)(\d)-([A-Z0-9]{2,4})-([A-Z0-9]{2})([A-Z0-9])-(\d{3})([A-Z0-9])-([A-Z])$"
        match = re.match(pattern, dmc_str.upper())
        
        if not match:
            raise ValueError(f"Invalid DMC format: {dmc_str}")
        
        return cls(
            model_ident_code=match.group(1),
            system_diff_code=match.group(2),
            system_code=match.group(3),
            subsystem_code=match.group(4),
            sub_subsystem_code=match.group(5),
            assy_code=match.group(6),
            disassy_code=match.group(7),
            disassy_code_variant=match.group(8),
            info_code=match.group(9),
            info_code_variant=match.group(10),
            item_location_code=match.group(11)
        )
    
    def to_xml_attributes(self) -> Dict[str, str]:
        """Return attributes for dmCode XML element."""
        return {
            "modelIdentCode": self.model_ident_code,
            "systemDiffCode": self.system_diff_code,
            "systemCode": self.system_code,
            "subSystemCode": self.subsystem_code,
            "subSubSystemCode": self.sub_subsystem_code,
            "assyCode": self.assy_code,
            "disassyCode": self.disassy_code,
            "disassyCodeVariant": self.disassy_code_variant,
            "infoCode": self.info_code,
            "infoCodeVariant": self.info_code_variant,
            "itemLocationCode": self.item_location_code
        }


@dataclass
class PMCode:
    """
    S1000D Publication Module Code structure.
    
    Format: MODEL-ISSUER-NUMBER-VOLUME
    """
    model_ident_code: str
    pm_issuer: str                      # Organization issuing the PM
    pm_number: str                      # Publication number
    pm_volume: str = "00"               # Volume number
    
    def __str__(self) -> str:
        return f"{self.model_ident_code}-{self.pm_issuer}-{self.pm_number}-{self.pm_volume}"
    
    def to_xml_attributes(self) -> Dict[str, str]:
        """Return attributes for pmCode XML element."""
        return {
            "modelIdentCode": self.model_ident_code,
            "pmIssuer": self.pm_issuer,
            "pmNumber": self.pm_number,
            "pmVolume": self.pm_volume
        }


@dataclass
class DMLCode:
    """
    S1000D Data Module List Code structure.
    
    Format: MODEL-SENDER-TYPE-YEAR-SEQ
    """
    model_ident_code: str
    sender_ident: str                   # Sending organization
    dml_type: str = "C"                 # DML type code
    year_of_data_issue: str = ""        # YYYY
    seq_number: str = "00001"           # 5-digit sequence
    
    def __post_init__(self):
        if not self.year_of_data_issue:
            self.year_of_data_issue = str(datetime.now().year)
    
    def __str__(self) -> str:
        return f"{self.model_ident_code}-{self.sender_ident}-{self.dml_type}-{self.year_of_data_issue}-{self.seq_number}"
    
    def to_xml_attributes(self) -> Dict[str, str]:
        """Return attributes for dmlCode XML element."""
        return {
            "modelIdentCode": self.model_ident_code,
            "senderIdent": self.sender_ident,
            "dmlType": self.dml_type,
            "yearOfDataIssue": self.year_of_data_issue,
            "seqNumber": self.seq_number
        }


@dataclass
class ICNCode:
    """
    Information Control Number for graphics.
    
    Format: ICN-MODEL-SYSTEM-FIGURE-SHEET-VARIANT
    """
    model_ident_code: str
    system_code: str
    figure_number: str
    sheet_number: str = "00001"
    variant: str = "00"
    language_code: str = "SX"           # SX = no language
    
    def __str__(self) -> str:
        return f"ICN-{self.model_ident_code}-{self.system_code}-{self.figure_number}-{self.sheet_number}-{self.variant}"
    
    @property
    def full_code(self) -> str:
        """Full ICN with language."""
        return f"ICN-{self.model_ident_code}-{self.system_code}-{self.figure_number}-{self.sheet_number}-{self.language_code}-{self.variant}"


# =============================================================================
# DATA CLASSES - GENERATION CONTEXT
# =============================================================================


@dataclass
class GeneratorConfig:
    """Configuration for generators."""
    model_ident_code: str
    organization_name: str
    organization_cage: str
    s1000d_version: str = "5.0"
    language_code: str = "en"
    country_code: str = "US"
    security_classification: SecurityClassification = SecurityClassification.UNCLASSIFIED
    brex_dm_ref: Optional[DMCode] = None
    
    # Template paths
    templates_path: Optional[Path] = None
    mapping_path: Optional[Path] = None
    
    # Output options
    pretty_print: bool = True
    include_comments: bool = False


@dataclass
class GenerationResult:
    """Result of a generation operation."""
    success: bool
    artifact: Optional[OutputArtifact] = None
    xml_content: str = ""
    dmc: str = ""
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    trace_links: List[TraceLink] = field(default_factory=list)
    generation_time: Optional[datetime] = None
    
    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0


@dataclass
class DMMetadata:
    """Metadata for a Data Module."""
    dmc: DMCode
    tech_name: str
    info_name: str
    issue_number: str = "001"
    in_work: str = "00"
    issue_type: str = "new"
    issue_date: Optional[date] = None
    security: SecurityClassification = SecurityClassification.UNCLASSIFIED
    responsible_company: str = ""
    originator: str = ""
    originator_cage: str = ""
    applicability_text: str = "All"
    
    def __post_init__(self):
        if self.issue_date is None:
            self.issue_date = date.today()


@dataclass
class ProceduralStep:
    """Represents a procedural step."""
    step_id: str
    instruction: str
    warnings: List[str] = field(default_factory=list)
    cautions: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    figure_refs: List[str] = field(default_factory=list)
    sub_steps: List["ProceduralStep"] = field(default_factory=list)


@dataclass
class PreliminaryRequirements:
    """Preliminary requirements for a procedure."""
    conditions: List[str] = field(default_factory=list)
    support_equipment: List[Dict[str, Any]] = field(default_factory=list)
    supplies: List[Dict[str, Any]] = field(default_factory=list)
    spares: List[Dict[str, Any]] = field(default_factory=list)
    safety_warnings: List[str] = field(default_factory=list)
    safety_cautions: List[str] = field(default_factory=list)
    maint_level: MaintenanceLevel = MaintenanceLevel.ORGANIZATIONAL
    task_duration: str = ""
    crew_size: int = 1


@dataclass
class PartItem:
    """Represents a part in an IPD."""
    part_number: str
    description: str
    manufacturer_cage: str = "00000"
    quantity: int = 1
    unit_of_measure: str = "EA"
    find_number: str = ""
    hotspot_ref: str = ""
    applicability: str = "All"
    nsn: str = ""
    alternate_parts: List[str] = field(default_factory=list)


@dataclass
class CatalogSeqNumber:
    """IPD Catalog Sequence Number entry."""
    csn_value: str
    indenture: str = "1"
    items: List[PartItem] = field(default_factory=list)


# =============================================================================
# BASE GENERATOR CLASS
# =============================================================================


class BaseGenerator(ABC):
    """
    Abstract base class for all ASIGT generators.
    
    All generators operate under ASIT contract authority.
    """
    
    S1000D_NS = "http://www.s1000d.org/S1000D_5-0"
    XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"
    
    def __init__(self, config: GeneratorConfig, context: Optional[ExecutionContext] = None):
        """
        Initialize generator.
        
        Args:
            config: Generator configuration
            context: Execution context from ASIT
        """
        self.config = config
        self.context = context
        self.logger = logging.getLogger(f"asigt.generator.{self.__class__.__name__}")
        
        # Register namespaces
        ET.register_namespace("", self.S1000D_NS)
        ET.register_namespace("xsi", self.XSI_NS)
    
    @abstractmethod
    def generate(self, source: SourceArtifact, **kwargs) -> GenerationResult:
        """
        Generate output from source artifact.
        
        Args:
            source: Source artifact from KDB
            **kwargs: Additional generation parameters
            
        Returns:
            GenerationResult with generated content
        """
        raise NotImplementedError
    
    def validate_source(self, source: SourceArtifact) -> bool:
        """Validate source artifact before generation."""
        if not source:
            return False
        if not source.content:
            source.load_content()
        return source.content is not None
    
    def create_xml_element(self, tag: str, attrib: Optional[Dict[str, str]] = None) -> ET.Element:
        """Create XML element with S1000D namespace."""
        return ET.Element(f"{{{self.S1000D_NS}}}{tag}", attrib or {})
    
    def create_sub_element(
        self, 
        parent: ET.Element, 
        tag: str, 
        text: Optional[str] = None,
        attrib: Optional[Dict[str, str]] = None
    ) -> ET.Element:
        """Create and append child element."""
        elem = ET.SubElement(parent, f"{{{self.S1000D_NS}}}{tag}", attrib or {})
        if text:
            elem.text = text
        return elem
    
    def prettify_xml(self, element: ET.Element) -> str:
        """Return pretty-printed XML string."""
        rough_string = ET.tostring(element, encoding="unicode")
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    
    def create_dm_address(
        self, 
        parent: ET.Element, 
        metadata: DMMetadata
    ) -> ET.Element:
        """Create dmAddress element."""
        dm_address = self.create_sub_element(parent, "dmAddress")
        
        # dmIdent
        dm_ident = self.create_sub_element(dm_address, "dmIdent")
        
        # dmCode
        dm_code = self.create_sub_element(dm_ident, "dmCode", attrib=metadata.dmc.to_xml_attributes())
        
        # language
        self.create_sub_element(dm_ident, "language", attrib={
            "languageIsoCode": self.config.language_code,
            "countryIsoCode": self.config.country_code
        })
        
        # issueInfo
        self.create_sub_element(dm_ident, "issueInfo", attrib={
            "issueNumber": metadata.issue_number,
            "inWork": metadata.in_work
        })
        
        # dmAddressItems
        dm_address_items = self.create_sub_element(dm_address, "dmAddressItems")
        
        # issueDate
        self.create_sub_element(dm_address_items, "issueDate", attrib={
            "year": str(metadata.issue_date.year),
            "month": f"{metadata.issue_date.month:02d}",
            "day": f"{metadata.issue_date.day:02d}"
        })
        
        # dmTitle
        dm_title = self.create_sub_element(dm_address_items, "dmTitle")
        self.create_sub_element(dm_title, "techName", text=metadata.tech_name)
        self.create_sub_element(dm_title, "infoName", text=metadata.info_name)
        
        return dm_address
    
    @staticmethod
    def _parse_ref_entry(entry: Any) -> Tuple[str, str]:
        """Parse a ref entry into a (code, title) tuple.

        Accepts either a plain string (returned as the code with an empty
        title) or a dict whose code is read from the first *present and
        non-empty* key among ``standard``, ``code``, and ``name``, and whose
        title comes from the first *present and non-empty* key among ``title``
        and ``description``.  Returns ``('', '')`` for any other type.

        Key lookup uses explicit ``None`` and empty-string checks so that a
        key whose value is ``None`` or ``""`` is treated as absent rather than
        masking a later key that carries a real value.

        .. note::
            ElementTree automatically escapes special characters (``&``, ``<``,
            ``>``, etc.) when serialising text content, so callers need not
            pre-escape the returned strings before passing them to
            :meth:`create_sub_element`.
        """
        if isinstance(entry, str):
            return entry, ""
        if isinstance(entry, dict):
            code = ""
            for key in ("standard", "code", "name"):
                val = entry.get(key)
                if val is not None and val != "":
                    code = str(val)
                    break
            title = ""
            for key in ("title", "description"):
                val = entry.get(key)
                if val is not None and val != "":
                    title = str(val)
                    break
            return code, title
        return "", ""

    def create_dm_status(
        self,
        parent: ET.Element,
        metadata: DMMetadata,
        regulatory_refs: Optional[List[Any]] = None,
        best_practices: Optional[List[Any]] = None,
    ) -> ET.Element:
        """Create dmStatus element.

        Args:
            parent: Parent element to append ``dmStatus`` to.
            metadata: Data module metadata.
            regulatory_refs: Regulatory reference entries to emit as
                ``<refs>/<externalPubRef>`` elements, positioned before
                ``brexDmRef`` per S1000D Issue 5.0 schema ordering.
            best_practices: Additional best-practice entries appended to
                *regulatory_refs* in the same ``<refs>`` block.
        """
        dm_status = self.create_sub_element(parent, "dmStatus", attrib={
            "issueType": metadata.issue_type
        })
        
        # security
        self.create_sub_element(dm_status, "security", attrib={
            "securityClassification": metadata.security.value
        })
        
        # responsiblePartnerCompany
        rpc = self.create_sub_element(dm_status, "responsiblePartnerCompany")
        self.create_sub_element(rpc, "enterpriseName", 
                                text=metadata.responsible_company or self.config.organization_name)
        
        # originator
        orig = self.create_sub_element(dm_status, "originator")
        self.create_sub_element(orig, "enterpriseName", 
                                text=metadata.originator or self.config.organization_name)
        self.create_sub_element(orig, "enterpriseIdent",
                                text=metadata.originator_cage or self.config.organization_cage)
        
        # applic
        applic = self.create_sub_element(dm_status, "applic")
        display_text = self.create_sub_element(applic, "displayText")
        self.create_sub_element(display_text, "simplePara", text=metadata.applicability_text)
        
        # refs – positioned here, before brexDmRef, per S1000D Issue 5.0 schema ordering
        self.create_regulatory_refs(dm_status, regulatory_refs or [], best_practices)

        # brexDmRef
        if self.config.brex_dm_ref:
            brex_ref = self.create_sub_element(dm_status, "brexDmRef")
            dm_ref = self.create_sub_element(brex_ref, "dmRef")
            dm_ref_ident = self.create_sub_element(dm_ref, "dmRefIdent")
            self.create_sub_element(dm_ref_ident, "dmCode", 
                                    attrib=self.config.brex_dm_ref.to_xml_attributes())
        
        # qualityAssurance
        qa = self.create_sub_element(dm_status, "qualityAssurance")
        self.create_sub_element(qa, "unverified")
        
        return dm_status
    
    def create_regulatory_refs(
        self,
        dm_status: ET.Element,
        regulatory_refs: List[Any],
        best_practices: Optional[List[Any]] = None,
    ) -> Optional[ET.Element]:
        """
        Create a ``refs`` element inside *dm_status* for regulatory references
        and industry best-practice citations.

        Each entry in *regulatory_refs* may be either a plain string
        (treated as the publication code) or a dict with optional keys
        ``standard`` / ``code`` and ``title``.

        Args:
            dm_status: The ``dmStatus`` parent element.
            regulatory_refs: Regulatory references to emit.
            best_practices: Optional additional best-practice references.

        Returns:
            The created ``refs`` element, or ``None`` if no refs were added.
        """
        all_refs: List[Any] = list(regulatory_refs or [])
        all_refs.extend(best_practices or [])

        if not all_refs:
            return None

        refs_elem = self.create_sub_element(dm_status, "refs")

        for ref in all_refs:
            code, title = self._parse_ref_entry(ref)
            if not code:
                continue
            ext_pub_ref = self.create_sub_element(refs_elem, "externalPubRef")
            ext_pub_ref_ident = self.create_sub_element(ext_pub_ref, "externalPubRefIdent")
            # ElementTree automatically escapes XML special characters in text content.
            self.create_sub_element(ext_pub_ref_ident, "externalPubCode", text=code)
            if title:
                self.create_sub_element(ext_pub_ref_ident, "externalPubTitle", text=title)

        return refs_elem

    def create_trace_link(
        self,
        source: SourceArtifact,
        output: OutputArtifact,
        transform_rule: str = ""
    ) -> TraceLink:
        """Create traceability link from source to output."""
        return TraceLink(
            source_id=source.id,
            source_path=str(source.path),
            source_hash=source.hash_sha256,
            source_type=source.artifact_type.value,
            target_id=output.id,
            target_path=str(output.path),
            target_hash=output.hash_sha256,
            target_type=output.artifact_type.value,
            link_type="transforms",
            transform_rule=transform_rule,
            timestamp=datetime.now()
        )


# =============================================================================
# DATA MODULE GENERATOR - DESCRIPTIVE
# =============================================================================


class DescriptiveDMGenerator(BaseGenerator):
    """
    Generator for S1000D Descriptive Data Modules.
    
    Generates description, theory of operation, and overview content.
    Info codes: 000, 001, 010, 018, 020, 040, 041, 042
    """
    
    SUPPORTED_INFO_CODES = ["000", "001", "010", "018", "020", "040", "041", "042"]
    
    def generate(
        self, 
        source: SourceArtifact, 
        metadata: Optional[DMMetadata] = None,
        **kwargs
    ) -> GenerationResult:
        """
        Generate descriptive DM from source.
        
        Args:
            source: Source artifact (requirement, description data)
            metadata: DM metadata (or derive from source)
            **kwargs: Additional options
            
        Returns:
            GenerationResult with XML content
        """
        result = GenerationResult(
            success=False,
            generation_time=datetime.now()
        )
        
        try:
            # Validate source
            if not self.validate_source(source):
                result.errors.append("Invalid source artifact")
                return result
            
            content = source.content
            
            # Build metadata if not provided
            if metadata is None:
                metadata = self._build_metadata_from_source(content)
            
            # Create DM root
            dmodule = self.create_xml_element("dmodule")
            
            # Ident and status section
            ident_status = self.create_sub_element(dmodule, "identAndStatusSection")
            self.create_dm_address(ident_status, metadata)
            # Collect regulatory references; both 'regulatory_refs' and 'standards' are
            # merged so neither is silently ignored when both fields are present.
            reg_refs_raw = content.get("regulatory_refs")
            standards_raw = content.get("standards")
            if reg_refs_raw is not None:
                regulatory_refs: List[Any] = list(reg_refs_raw) + list(standards_raw or [])
            else:
                regulatory_refs = list(standards_raw or [])
            best_practices: List[Any] = list(content.get("best_practices") or [])

            # Pass refs into create_dm_status so <refs> is emitted at the correct
            # S1000D schema position (before <brexDmRef>).
            dm_status = self.create_dm_status(ident_status, metadata, regulatory_refs, best_practices)

            # Content section
            content_elem = self.create_sub_element(dmodule, "content")
            description = self.create_sub_element(content_elem, "description")
            
            # Generate content structure
            self._generate_description_content(description, content)
            
            # Serialize
            xml_string = self.prettify_xml(dmodule)
            
            # Create output artifact
            output = OutputArtifact(
                id=f"DM-{metadata.dmc}",
                path=Path(f"{metadata.dmc}.xml"),
                artifact_type=ArtifactType.DM_DESCRIPTIVE,
                dmc=str(metadata.dmc),
                source_refs=[source.id],
                generated_at=datetime.now(),
                valid=True
            )
            
            # Create trace link
            trace = self.create_trace_link(source, output, "requirement_to_dm:descriptive")
            
            result.success = True
            result.artifact = output
            result.xml_content = xml_string
            result.dmc = str(metadata.dmc)
            result.trace_links = [trace]
            
            self.logger.info(f"Generated descriptive DM: {metadata.dmc}")
            
        except Exception as e:
            self.logger.error(f"Error generating descriptive DM: {e}")
            result.errors.append(str(e))
        
        return result
    
    def _build_metadata_from_source(self, content: Dict[str, Any]) -> DMMetadata:
        """Build DMMetadata from source content."""
        # Extract ATA chapter
        ata_chapter = content.get("ata_chapter", content.get("system_code", "00"))
        ata_section = content.get("ata_section", content.get("subsystem", "0"))
        
        # Determine info code based on content type
        content_type = content.get("type", "description")
        info_code = self._get_info_code_for_type(content_type)
        
        dmc = DMCode(
            model_ident_code=self.config.model_ident_code,
            system_code=str(ata_chapter).zfill(2),
            subsystem_code=str(ata_section)[0] if ata_section else "0",
            sub_subsystem_code=str(ata_section)[1] if len(str(ata_section)) > 1 else "0",
            info_code=info_code,
            info_code_variant="A",
            item_location_code="D"
        )
        
        return DMMetadata(
            dmc=dmc,
            tech_name=content.get("title", content.get("tech_name", "Unknown")),
            info_name=content.get("info_name", "Description"),
            responsible_company=self.config.organization_name,
            originator=self.config.organization_name,
            originator_cage=self.config.organization_cage
        )
    
    def _get_info_code_for_type(self, content_type: str) -> str:
        """Map content type to info code."""
        type_mapping = {
            "description": "040",
            "theory_of_operation": "041",
            "overview": "042",
            "general": "000",
            "identification": "001",
            "title_page": "010",
            "revisions": "018",
            "functional": "020"
        }
        return type_mapping.get(content_type.lower(), "040")
    
    def _generate_description_content(
        self, 
        description: ET.Element, 
        content: Dict[str, Any]
    ) -> None:
        """Generate description content structure."""
        # General section
        if content.get("general_description") or content.get("description"):
            general = self.create_sub_element(description, "levelledPara")
            self.create_sub_element(general, "title", text="General")
            self.create_sub_element(
                general, "para", 
                text=content.get("general_description") or content.get("description", "")
            )
        
        # System overview
        if content.get("system_overview"):
            overview = self.create_sub_element(description, "levelledPara")
            self.create_sub_element(overview, "title", text="System Overview")
            self.create_sub_element(overview, "para", text=content["system_overview"])
        
        # Functional description
        if content.get("functional_description"):
            functional = self.create_sub_element(description, "levelledPara")
            self.create_sub_element(functional, "title", text="Functional Description")
            self.create_sub_element(functional, "para", text=content["functional_description"])
        
        # Theory of operation
        if content.get("theory_of_operation"):
            theory = self.create_sub_element(description, "levelledPara")
            self.create_sub_element(theory, "title", text="Theory of Operation")
            self.create_sub_element(theory, "para", text=content["theory_of_operation"])
        
        # System interfaces
        if content.get("system_interfaces"):
            interfaces = self.create_sub_element(description, "levelledPara")
            self.create_sub_element(interfaces, "title", text="System Interfaces")
            for interface in content["system_interfaces"]:
                if isinstance(interface, str):
                    self.create_sub_element(interfaces, "para", text=interface)
                elif isinstance(interface, dict):
                    self.create_sub_element(
                        interfaces, "para", 
                        text=f"{interface.get('name', 'Interface')}: {interface.get('description', '')}"
                    )
        
        # Location and access
        if content.get("location_access"):
            location = self.create_sub_element(description, "levelledPara")
            self.create_sub_element(location, "title", text="Location and Access")
            self.create_sub_element(location, "para", text=content["location_access"])

        # Regulatory references and industry best practices – inline citations.
        # Both 'regulatory_refs' and 'standards' are merged so neither is silently ignored.
        reg_refs_raw = content.get("regulatory_refs")
        standards_raw = content.get("standards")
        if reg_refs_raw is not None:
            _reg_refs: List[Any] = list(reg_refs_raw) + list(standards_raw or [])
        else:
            _reg_refs = list(standards_raw or [])
        _best_practices: List[Any] = list(content.get("best_practices") or [])
        all_citations = _reg_refs + _best_practices
        if all_citations:
            citations_para = self.create_sub_element(description, "levelledPara")
            self.create_sub_element(citations_para, "title",
                                    text="Regulatory References and Industry Best Practices")
            for entry in all_citations:
                code, title = self._parse_ref_entry(entry)
                if not code:
                    continue
                citation_text = f"[{code}]" if not title else f"[{code}] {title}"
                self.create_sub_element(citations_para, "para", text=citation_text)


# =============================================================================
# DATA MODULE GENERATOR - PROCEDURAL
# =============================================================================


class ProceduralDMGenerator(BaseGenerator):
    """
    Generator for S1000D Procedural Data Modules.
    
    Generates maintenance tasks, operational procedures, servicing, etc.
    Info codes: 100, 200, 300, 500, 510, 520, 600, 700, 720, 800, 900
    """
    
    SUPPORTED_INFO_CODES = ["100", "200", "300", "500", "510", "520", "600", "700", "720", "800", "900"]
    
    def generate(
        self, 
        source: SourceArtifact, 
        metadata: Optional[DMMetadata] = None,
        preliminary_req: Optional[PreliminaryRequirements] = None,
        steps: Optional[List[ProceduralStep]] = None,
        **kwargs
    ) -> GenerationResult:
        """
        Generate procedural DM from source.
        
        Args:
            source: Source artifact (task definition)
            metadata: DM metadata
            preliminary_req: Preliminary requirements
            steps: Procedural steps
            **kwargs: Additional options
            
        Returns:
            GenerationResult with XML content
        """
        result = GenerationResult(
            success=False,
            generation_time=datetime.now()
        )
        
        try:
            # Validate source
            if not self.validate_source(source):
                result.errors.append("Invalid source artifact")
                return result
            
            content = source.content
            
            # Build metadata if not provided
            if metadata is None:
                metadata = self._build_metadata_from_source(content)
            
            # Build preliminary requirements if not provided
            if preliminary_req is None:
                preliminary_req = self._build_preliminary_from_source(content)
            
            # Build steps if not provided
            if steps is None:
                steps = self._build_steps_from_source(content)
            
            # Create DM root
            dmodule = self.create_xml_element("dmodule")
            
            # Ident and status section
            ident_status = self.create_sub_element(dmodule, "identAndStatusSection")
            self.create_dm_address(ident_status, metadata)
            # Collect regulatory references; both 'regulatory_refs' and 'standards' are
            # merged so neither is silently ignored when both fields are present.
            reg_refs_raw = content.get("regulatory_refs")
            standards_raw = content.get("standards")
            if reg_refs_raw is not None:
                regulatory_refs: List[Any] = list(reg_refs_raw) + list(standards_raw or [])
            else:
                regulatory_refs = list(standards_raw or [])
            best_practices: List[Any] = list(content.get("best_practices") or [])

            # Pass refs into create_dm_status so <refs> is emitted at the correct
            # S1000D schema position (before <brexDmRef>).
            dm_status = self.create_dm_status(ident_status, metadata, regulatory_refs, best_practices)

            # Content section
            content_elem = self.create_sub_element(dmodule, "content")
            procedure = self.create_sub_element(content_elem, "procedure")
            
            # Preliminary requirements
            self._generate_preliminary_rqmts(procedure, preliminary_req)
            
            # Main procedure
            self._generate_main_procedure(procedure, steps)
            
            # Close-up requirements
            close_rqmts = self.create_sub_element(procedure, "closeRqmts")
            req_cond_group = self.create_sub_element(close_rqmts, "reqCondGroup")
            req_cond_dm = self.create_sub_element(req_cond_group, "reqCondDm")
            close_text = content.get("close_requirements", "Task complete. Return aircraft to service.")
            self.create_sub_element(req_cond_dm, "reqCond", text=close_text)
            
            # Serialize
            xml_string = self.prettify_xml(dmodule)
            
            # Create output artifact
            output = OutputArtifact(
                id=f"DM-{metadata.dmc}",
                path=Path(f"{metadata.dmc}.xml"),
                artifact_type=ArtifactType.DM_PROCEDURAL,
                dmc=str(metadata.dmc),
                source_refs=[source.id],
                generated_at=datetime.now(),
                valid=True
            )
            
            # Create trace link
            trace = self.create_trace_link(source, output, "task_to_dm:procedural")
            
            result.success = True
            result.artifact = output
            result.xml_content = xml_string
            result.dmc = str(metadata.dmc)
            result.trace_links = [trace]
            
            self.logger.info(f"Generated procedural DM: {metadata.dmc}")
            
        except Exception as e:
            self.logger.error(f"Error generating procedural DM: {e}")
            result.errors.append(str(e))
        
        return result
    
    def _build_metadata_from_source(self, content: Dict[str, Any]) -> DMMetadata:
        """Build DMMetadata from source content."""
        ata_chapter = content.get("ata_chapter", "00")
        ata_section = content.get("ata_section", "0")
        
        # Determine info code based on task type
        task_type = content.get("task_type", content.get("type", "procedure"))
        info_code = self._get_info_code_for_task_type(task_type)
        
        dmc = DMCode(
            model_ident_code=self.config.model_ident_code,
            system_code=str(ata_chapter).zfill(2),
            subsystem_code=str(ata_section)[0] if ata_section else "0",
            sub_subsystem_code=str(ata_section)[1] if len(str(ata_section)) > 1 else "0",
            assy_code=content.get("assy_code", "00"),
            disassy_code=content.get("disassy_code", "00"),
            info_code=info_code,
            info_code_variant="A",
            item_location_code="D"
        )
        
        # Determine info name
        info_name = content.get("info_name", self._get_info_name_for_code(info_code))
        
        return DMMetadata(
            dmc=dmc,
            tech_name=content.get("task_title", content.get("title", "Unknown")),
            info_name=info_name,
            responsible_company=self.config.organization_name,
            originator=self.config.organization_name,
            originator_cage=self.config.organization_cage
        )
    
    def _get_info_code_for_task_type(self, task_type: str) -> str:
        """Map task type to info code."""
        type_mapping = {
            "removal": "510",
            "remove": "510",
            "installation": "520",
            "install": "520",
            "servicing": "200",
            "service": "200",
            "lubrication": "210",
            "inspection": "300",
            "inspect": "300",
            "visual_check": "310",
            "detailed_inspection": "320",
            "operational_check": "700",
            "functional_test": "720",
            "cleaning": "900",
            "painting": "920",
            "storage": "800",
            "disconnect": "500",
            "connect": "500"
        }
        return type_mapping.get(task_type.lower(), "100")
    
    def _get_info_name_for_code(self, info_code: str) -> str:
        """Get default info name for info code."""
        code_names = {
            "100": "Operation",
            "200": "Servicing",
            "210": "Lubrication",
            "300": "Inspection",
            "310": "Visual Check",
            "320": "Detailed Inspection",
            "500": "Disconnect/Connect",
            "510": "Removal",
            "520": "Installation",
            "700": "Operational Check",
            "720": "Functional Test",
            "800": "Storage",
            "900": "Cleaning",
            "920": "Painting/Finishing"
        }
        return code_names.get(info_code, "Procedure")
    
    def _build_preliminary_from_source(self, content: Dict[str, Any]) -> PreliminaryRequirements:
        """Build preliminary requirements from source content."""
        prelim = PreliminaryRequirements()
        
        # Conditions
        if "preconditions" in content:
            prelim.conditions = content["preconditions"] if isinstance(content["preconditions"], list) else [content["preconditions"]]
        
        # Tools/equipment
        if "tools_required" in content:
            for tool in content["tools_required"]:
                if isinstance(tool, dict):
                    prelim.support_equipment.append(tool)
                else:
                    prelim.support_equipment.append({"name": str(tool)})
        
        # Supplies/consumables
        if "materials_required" in content or "consumables" in content:
            materials = content.get("materials_required", []) + content.get("consumables", [])
            for material in materials:
                if isinstance(material, dict):
                    prelim.supplies.append(material)
                else:
                    prelim.supplies.append({"name": str(material)})
        
        # Spares
        if "spares_required" in content:
            for spare in content["spares_required"]:
                if isinstance(spare, dict):
                    prelim.spares.append(spare)
                else:
                    prelim.spares.append({"name": str(spare)})
        
        # Safety
        if "safety_warnings" in content:
            prelim.safety_warnings = content["safety_warnings"] if isinstance(content["safety_warnings"], list) else [content["safety_warnings"]]
        if "safety_cautions" in content:
            prelim.safety_cautions = content["safety_cautions"] if isinstance(content["safety_cautions"], list) else [content["safety_cautions"]]
        
        # Maintenance info
        maint_level = content.get("maint_level", "organizational")
        prelim.maint_level = MaintenanceLevel(maint_level[0].upper()) if maint_level else MaintenanceLevel.ORGANIZATIONAL
        prelim.task_duration = str(content.get("man_hours", content.get("task_duration", "")))
        prelim.crew_size = content.get("crew_size", 1)
        
        return prelim
    
    def _build_steps_from_source(self, content: Dict[str, Any]) -> List[ProceduralStep]:
        """Build procedural steps from source content."""
        steps = []
        raw_steps = content.get("procedure_steps", content.get("steps", []))
        
        for i, step_data in enumerate(raw_steps, 1):
            step_id = f"step-{i:03d}"
            
            if isinstance(step_data, str):
                step = ProceduralStep(step_id=step_id, instruction=step_data)
            elif isinstance(step_data, dict):
                step = ProceduralStep(
                    step_id=step_data.get("id", step_id),
                    instruction=step_data.get("instruction", step_data.get("text", "")),
                    warnings=step_data.get("warnings", []),
                    cautions=step_data.get("cautions", []),
                    notes=step_data.get("notes", []),
                    figure_refs=step_data.get("figure_refs", [])
                )
                # Handle sub-steps recursively
                if "sub_steps" in step_data:
                    for j, sub_step in enumerate(step_data["sub_steps"], 1):
                        sub_id = f"{step_id}-{j:02d}"
                        if isinstance(sub_step, str):
                            step.sub_steps.append(ProceduralStep(step_id=sub_id, instruction=sub_step))
                        elif isinstance(sub_step, dict):
                            step.sub_steps.append(ProceduralStep(
                                step_id=sub_step.get("id", sub_id),
                                instruction=sub_step.get("instruction", sub_step.get("text", ""))
                            ))
            else:
                continue
            
            steps.append(step)
        
        return steps
    
    def _generate_preliminary_rqmts(
        self, 
        procedure: ET.Element, 
        prelim: PreliminaryRequirements
    ) -> None:
        """Generate preliminaryRqmts element."""
        prelim_elem = self.create_sub_element(procedure, "preliminaryRqmts")
        
        # Production/Maintainability data
        prod_data = self.create_sub_element(prelim_elem, "productionMaintData")
        self.create_sub_element(prod_data, "maintLevel", text=prelim.maint_level.value)
        if prelim.task_duration:
            self.create_sub_element(prod_data, "taskDuration", text=prelim.task_duration)
        
        # Required conditions
        req_cond_group = self.create_sub_element(prelim_elem, "reqCondGroup")
        if prelim.conditions:
            for condition in prelim.conditions:
                req_cond_dm = self.create_sub_element(req_cond_group, "reqCondDm")
                self.create_sub_element(req_cond_dm, "reqCond", text=condition)
        else:
            req_cond_dm = self.create_sub_element(req_cond_group, "reqCondDm")
            self.create_sub_element(req_cond_dm, "reqCond", text="None")
        
        # Support equipment
        req_support = self.create_sub_element(prelim_elem, "reqSupportEquips")
        equip_group = self.create_sub_element(req_support, "supportEquipDescrGroup")
        if prelim.support_equipment:
            for i, equip in enumerate(prelim.support_equipment, 1):
                se_descr = self.create_sub_element(equip_group, "supportEquipDescr", attrib={"id": f"seq-{i:03d}"})
                self.create_sub_element(se_descr, "name", text=equip.get("name", "Unknown"))
                if equip.get("part_number"):
                    ident_num = self.create_sub_element(se_descr, "identNumber")
                    pn = self.create_sub_element(ident_num, "partAndSerialNumber")
                    self.create_sub_element(pn, "partNumber", text=equip["part_number"])
                if equip.get("quantity"):
                    self.create_sub_element(se_descr, "reqQuantity", text=str(equip["quantity"]))
        else:
            self.create_sub_element(equip_group, "noSupportEquips")
        
        # Supplies
        req_supplies = self.create_sub_element(prelim_elem, "reqSupplies")
        supply_group = self.create_sub_element(req_supplies, "supplyDescrGroup")
        if prelim.supplies:
            for i, supply in enumerate(prelim.supplies, 1):
                sup_descr = self.create_sub_element(supply_group, "supplyDescr", attrib={"id": f"sup-{i:03d}"})
                self.create_sub_element(sup_descr, "name", text=supply.get("name", "Unknown"))
                if supply.get("quantity"):
                    self.create_sub_element(sup_descr, "reqQuantity", text=str(supply["quantity"]))
        else:
            self.create_sub_element(supply_group, "noSupplies")
        
        # Spares
        req_spares = self.create_sub_element(prelim_elem, "reqSpares")
        spare_group = self.create_sub_element(req_spares, "spareDescrGroup")
        if prelim.spares:
            for i, spare in enumerate(prelim.spares, 1):
                spr_descr = self.create_sub_element(spare_group, "spareDescr", attrib={"id": f"spr-{i:03d}"})
                self.create_sub_element(spr_descr, "name", text=spare.get("name", "Unknown"))
                if spare.get("part_number"):
                    ident_num = self.create_sub_element(spr_descr, "identNumber")
                    pn = self.create_sub_element(ident_num, "partAndSerialNumber")
                    self.create_sub_element(pn, "partNumber", text=spare["part_number"])
                if spare.get("quantity"):
                    self.create_sub_element(spr_descr, "reqQuantity", text=str(spare["quantity"]))
        else:
            self.create_sub_element(spare_group, "noSpares")
        
        # Safety requirements
        req_safety = self.create_sub_element(prelim_elem, "reqSafety")
        if prelim.safety_warnings or prelim.safety_cautions:
            safety_rqmts = self.create_sub_element(req_safety, "safetyRqmts")
            for i, warning in enumerate(prelim.safety_warnings, 1):
                wrn = self.create_sub_element(safety_rqmts, "warning", attrib={"id": f"wrn-prelim-{i:03d}"})
                self.create_sub_element(wrn, "warningAndCautionPara", text=warning)
            for i, caution in enumerate(prelim.safety_cautions, 1):
                ctn = self.create_sub_element(safety_rqmts, "caution", attrib={"id": f"ctn-prelim-{i:03d}"})
                self.create_sub_element(ctn, "warningAndCautionPara", text=caution)
        else:
            self.create_sub_element(req_safety, "noSafety")
    
    def _generate_main_procedure(
        self, 
        procedure: ET.Element, 
        steps: List[ProceduralStep]
    ) -> None:
        """Generate mainProcedure element."""
        main_proc = self.create_sub_element(procedure, "mainProcedure")
        
        for step in steps:
            self._generate_procedural_step(main_proc, step)
    
    def _generate_procedural_step(
        self, 
        parent: ET.Element, 
        step: ProceduralStep
    ) -> None:
        """Generate a single procedural step (recursive for sub-steps)."""
        step_elem = self.create_sub_element(parent, "proceduralStep", attrib={"id": step.step_id})
        
        # Warnings (must come first - W-C-N-P order)
        for i, warning in enumerate(step.warnings, 1):
            wrn = self.create_sub_element(step_elem, "warning", attrib={"id": f"wrn-{step.step_id}-{i:03d}"})
            self.create_sub_element(wrn, "warningAndCautionPara", text=warning)
        
        # Cautions
        for i, caution in enumerate(step.cautions, 1):
            ctn = self.create_sub_element(step_elem, "caution", attrib={"id": f"ctn-{step.step_id}-{i:03d}"})
            self.create_sub_element(ctn, "warningAndCautionPara", text=caution)
        
        # Notes
        for i, note in enumerate(step.notes, 1):
            note_elem = self.create_sub_element(step_elem, "note", attrib={"id": f"note-{step.step_id}-{i:03d}"})
            self.create_sub_element(note_elem, "notePara", text=note)
        
        # Para (instruction)
        self.create_sub_element(step_elem, "para", text=step.instruction)
        
        # Sub-steps
        for sub_step in step.sub_steps:
            self._generate_procedural_step(step_elem, sub_step)


# =============================================================================
# DATA MODULE GENERATOR - IPD
# =============================================================================


class IPDGenerator(BaseGenerator):
    """
    Generator for S1000D Illustrated Parts Data Modules.
    
    Generates illustrated parts catalogs with figures and parts lists.
    Info codes: 941, 942, 944
    """
    
    SUPPORTED_INFO_CODES = ["941", "942", "944"]
    
    def generate(
        self, 
        source: SourceArtifact, 
        metadata: Optional[DMMetadata] = None,
        csn_entries: Optional[List[CatalogSeqNumber]] = None,
        figure_icn: Optional[str] = None,
        figure_title: Optional[str] = None,
        **kwargs
    ) -> GenerationResult:
        """
        Generate IPD DM from source.
        
        Args:
            source: Source artifact (parts data)
            metadata: DM metadata
            csn_entries: Catalog sequence number entries
            figure_icn: ICN reference for illustration
            figure_title: Title for illustration
            **kwargs: Additional options
            
        Returns:
            GenerationResult with XML content
        """
        result = GenerationResult(
            success=False,
            generation_time=datetime.now()
        )
        
        try:
            # Validate source
            if not self.validate_source(source):
                result.errors.append("Invalid source artifact")
                return result
            
            content = source.content
            
            # Build metadata if not provided
            if metadata is None:
                metadata = self._build_metadata_from_source(content)
            
            # Build CSN entries if not provided
            if csn_entries is None:
                csn_entries = self._build_csn_from_source(content)
            
            # Create DM root
            dmodule = self.create_xml_element("dmodule")
            
            # Ident and status section
            ident_status = self.create_sub_element(dmodule, "identAndStatusSection")
            self.create_dm_address(ident_status, metadata)
            self.create_dm_status(ident_status, metadata)
            
            # Content section
            content_elem = self.create_sub_element(dmodule, "content")
            ipd = self.create_sub_element(content_elem, "illustratedPartsCatalog")
            
            # Figure
            fig_icn = figure_icn or content.get("figure", {}).get("icn", "")
            fig_title = figure_title or content.get("figure", {}).get("title", "Assembly Breakdown")
            if fig_icn:
                self._generate_figure(ipd, fig_icn, fig_title)
            
            # Catalog sequence numbers
            for csn in csn_entries:
                self._generate_csn(ipd, csn)
            
            # Serialize
            xml_string = self.prettify_xml(dmodule)
            
            # Create output artifact
            output = OutputArtifact(
                id=f"DM-{metadata.dmc}",
                path=Path(f"{metadata.dmc}.xml"),
                artifact_type=ArtifactType.DM_IPD,
                dmc=str(metadata.dmc),
                source_refs=[source.id],
                generated_at=datetime.now(),
                valid=True
            )
            
            # Create trace link
            trace = self.create_trace_link(source, output, "parts_to_ipd")
            
            result.success = True
            result.artifact = output
            result.xml_content = xml_string
            result.dmc = str(metadata.dmc)
            result.trace_links = [trace]
            
            self.logger.info(f"Generated IPD DM: {metadata.dmc}")
            
        except Exception as e:
            self.logger.error(f"Error generating IPD DM: {e}")
            result.errors.append(str(e))
        
        return result
    
    def _build_metadata_from_source(self, content: Dict[str, Any]) -> DMMetadata:
        """Build DMMetadata from source content."""
        assembly = content.get("assembly", content)
        ata_chapter = assembly.get("ata_chapter", "00")
        ata_section = assembly.get("ata_section", "0")
        
        dmc = DMCode(
            model_ident_code=self.config.model_ident_code,
            system_code=str(ata_chapter).zfill(2),
            subsystem_code=str(ata_section)[0] if ata_section else "0",
            sub_subsystem_code=str(ata_section)[1] if len(str(ata_section)) > 1 else "0",
            assy_code=assembly.get("assy_code", "01"),
            info_code="941",
            info_code_variant="A",
            item_location_code="D"
        )
        
        return DMMetadata(
            dmc=dmc,
            tech_name=assembly.get("part_name", assembly.get("title", "Assembly")),
            info_name="Illustrated Parts Data",
            responsible_company=self.config.organization_name,
            originator=self.config.organization_name,
            originator_cage=self.config.organization_cage
        )
    
    def _build_csn_from_source(self, content: Dict[str, Any]) -> List[CatalogSeqNumber]:
        """Build CSN entries from source content."""
        csn_list = []
        parts = content.get("parts", [])
        
        # Group by find number or create single CSN
        if parts:
            csn = CatalogSeqNumber(csn_value="001", indenture="1")
            
            for i, part_data in enumerate(parts, 1):
                if isinstance(part_data, dict):
                    part = PartItem(
                        part_number=part_data.get("part_number", ""),
                        description=part_data.get("part_name", part_data.get("description", "")),
                        manufacturer_cage=part_data.get("cage_code", "00000"),
                        quantity=part_data.get("quantity", 1),
                        find_number=part_data.get("find_number", str(i).zfill(3)),
                        hotspot_ref=f"hs-001-{i:03d}"
                    )
                    csn.items.append(part)
            
            csn_list.append(csn)
        
        return csn_list
    
    def _generate_figure(
        self, 
        ipd: ET.Element, 
        icn: str, 
        title: str
    ) -> None:
        """Generate figure element."""
        figure = self.create_sub_element(ipd, "figure", attrib={"id": "fig-ipd-001"})
        self.create_sub_element(figure, "title", text=title)
        self.create_sub_element(figure, "graphic", attrib={"infoEntityIdent": icn})
    
    def _generate_csn(
        self, 
        ipd: ET.Element, 
        csn: CatalogSeqNumber
    ) -> None:
        """Generate catalogSeqNumber element."""
        csn_elem = self.create_sub_element(ipd, "catalogSeqNumber", attrib={
            "id": f"csn-{csn.csn_value}",
            "catalogSeqNumberValue": csn.csn_value,
            "indenture": csn.indenture
        })
        
        for item in csn.items:
            self._generate_item_seq_number(csn_elem, item)
    
    def _generate_item_seq_number(
        self, 
        csn_elem: ET.Element, 
        item: PartItem
    ) -> None:
        """Generate itemSeqNumber element."""
        isn = self.create_sub_element(csn_elem, "itemSeqNumber", attrib={
            "itemSeqNumberValue": item.find_number
        })
        
        # Quantity
        self.create_sub_element(isn, "quantityPerNextHigherAssy", text=str(item.quantity))
        
        # Part reference
        part_ref = self.create_sub_element(isn, "partRef")
        part_ident = self.create_sub_element(part_ref, "partIdent", attrib={
            "manufacturerCodeValue": item.manufacturer_cage
        })
        self.create_sub_element(part_ident, "partNumber", text=item.part_number)
        
        # Part identification segment
        part_seg = self.create_sub_element(isn, "partIdentSegment")
        self.create_sub_element(part_seg, "descrForPart", text=item.description.upper())
        
        # References (hotspot)
        if item.hotspot_ref:
            refs = self.create_sub_element(isn, "refs")
            self.create_sub_element(refs, "internalRef", attrib={
                "internalRefId": item.hotspot_ref,
                "internalRefTargetType": "irtt03"
            })


# =============================================================================
# DATA MODULE GENERATOR - FAULT ISOLATION
# =============================================================================


class FaultIsolationDMGenerator(BaseGenerator):
    """
    Generator for S1000D Fault Isolation Data Modules.
    
    Generates troubleshooting and fault isolation procedures.
    Info codes: 400, 410, 420
    """
    
    SUPPORTED_INFO_CODES = ["400", "410", "420"]
    
    def generate(
        self, 
        source: SourceArtifact, 
        metadata: Optional[DMMetadata] = None,
        **kwargs
    ) -> GenerationResult:
        """
        Generate fault isolation DM from source.
        
        Args:
            source: Source artifact (fault data)
            metadata: DM metadata
            **kwargs: Additional options
            
        Returns:
            GenerationResult with XML content
        """
        result = GenerationResult(
            success=False,
            generation_time=datetime.now()
        )
        
        try:
            if not self.validate_source(source):
                result.errors.append("Invalid source artifact")
                return result
            
            content = source.content
            
            if metadata is None:
                metadata = self._build_metadata_from_source(content)
            
            # Create DM root
            dmodule = self.create_xml_element("dmodule")
            
            # Ident and status section
            ident_status = self.create_sub_element(dmodule, "identAndStatusSection")
            self.create_dm_address(ident_status, metadata)
            self.create_dm_status(ident_status, metadata)
            
            # Content section with fault isolation
            content_elem = self.create_sub_element(dmodule, "content")
            fault_iso = self.create_sub_element(content_elem, "faultIsolation")
            
            # Generate fault isolation content
            self._generate_fault_content(fault_iso, content)
            
            xml_string = self.prettify_xml(dmodule)
            
            output = OutputArtifact(
                id=f"DM-{metadata.dmc}",
                path=Path(f"{metadata.dmc}.xml"),
                artifact_type=ArtifactType.DM_FAULT_ISOLATION,
                dmc=str(metadata.dmc),
                source_refs=[source.id],
                generated_at=datetime.now(),
                valid=True
            )
            
            trace = self.create_trace_link(source, output, "fault_to_dm")
            
            result.success = True
            result.artifact = output
            result.xml_content = xml_string
            result.dmc = str(metadata.dmc)
            result.trace_links = [trace]
            
            self.logger.info(f"Generated fault isolation DM: {metadata.dmc}")
            
        except Exception as e:
            self.logger.error(f"Error generating fault isolation DM: {e}")
            result.errors.append(str(e))
        
        return result
    
    def _build_metadata_from_source(self, content: Dict[str, Any]) -> DMMetadata:
        """Build DMMetadata from source content."""
        ata_chapter = content.get("ata_chapter", "00")
        ata_section = content.get("ata_section", "0")
        
        dmc = DMCode(
            model_ident_code=self.config.model_ident_code,
            system_code=str(ata_chapter).zfill(2),
            subsystem_code=str(ata_section)[0] if ata_section else "0",
            sub_subsystem_code=str(ata_section)[1] if len(str(ata_section)) > 1 else "0",
            info_code="400",
            info_code_variant="A",
            item_location_code="D"
        )
        
        return DMMetadata(
            dmc=dmc,
            tech_name=content.get("title", content.get("system_name", "System")),
            info_name="Fault Isolation",
            responsible_company=self.config.organization_name,
            originator=self.config.organization_name,
            originator_cage=self.config.organization_cage
        )
    
    def _generate_fault_content(self, fault_iso: ET.Element, content: Dict[str, Any]) -> None:
        """Generate fault isolation content."""
        # Isolation procedure
        isolation_proc = self.create_sub_element(fault_iso, "isolationProcedure")
        
        # Fault
        fault = self.create_sub_element(isolation_proc, "fault", attrib={
            "faultCode": content.get("fault_code", "FC001")
        })
        
        fault_descr = self.create_sub_element(fault, "faultDescr")
        self.create_sub_element(fault_descr, "descr", text=content.get("fault_description", "Fault condition"))
        
        # Isolation steps
        isolation_steps = content.get("isolation_steps", [])
        if isolation_steps:
            iso_step = self.create_sub_element(fault, "isolationStep", attrib={"id": "iso-step-001"})
            action = self.create_sub_element(iso_step, "action")
            
            for i, step in enumerate(isolation_steps, 1):
                self.create_sub_element(action, "para", text=f"{i}. {step}")


# =============================================================================
# PUBLICATION MODULE GENERATOR
# =============================================================================


class PMGenerator(BaseGenerator):
    """
    Generator for S1000D Publication Modules.
    
    Generates publication structure (AMM, SRM, CMM, IPC, etc.).
    """
    
    def __init__(
        self, 
        config: GeneratorConfig, 
        context: Optional[ExecutionContext] = None,
        publication_type: PublicationType = PublicationType.AMM
    ):
        super().__init__(config, context)
        self.publication_type = publication_type
    
    def generate(
        self, 
        source: SourceArtifact,
        pm_code: Optional[PMCode] = None,
        title: Optional[str] = None,
        dm_refs: Optional[List[DMCode]] = None,
        **kwargs
    ) -> GenerationResult:
        """
        Generate Publication Module from source.
        
        Args:
            source: Source artifact (publication definition)
            pm_code: Publication module code
            title: Publication title
            dm_refs: Data module references to include
            **kwargs: Additional options
            
        Returns:
            GenerationResult with XML content
        """
        result = GenerationResult(
            success=False,
            generation_time=datetime.now()
        )
        
        try:
            content = source.content if source else {}
            
            # Build PM code if not provided
            if pm_code is None:
                pm_code = PMCode(
                    model_ident_code=self.config.model_ident_code,
                    pm_issuer=self.config.organization_cage,
                    pm_number=self._get_pm_number_for_type(),
                    pm_volume="00"
                )
            
            # Build title
            if title is None:
                title = content.get("title", self._get_title_for_type())
            
            # Create PM root
            pm = self.create_xml_element("pm")
            
            # Ident and status section
            ident_status = self.create_sub_element(pm, "identAndStatusSection")
            self._create_pm_address(ident_status, pm_code, title)
            self._create_pm_status(ident_status, pm_code)
            
            # Content section
            content_elem = self.create_sub_element(pm, "content")
            root_entry = self.create_sub_element(content_elem, "pmEntry")
            
            # Generate PM structure based on type
            self._generate_pm_structure(root_entry, content, dm_refs or [])
            
            xml_string = self.prettify_xml(pm)
            
            output = OutputArtifact(
                id=f"PM-{pm_code}",
                path=Path(f"{pm_code}.xml"),
                artifact_type=ArtifactType.PM,
                dmc=str(pm_code),
                source_refs=[source.id] if source else [],
                generated_at=datetime.now(),
                valid=True
            )
            
            result.success = True
            result.artifact = output
            result.xml_content = xml_string
            result.dmc = str(pm_code)
            
            self.logger.info(f"Generated PM: {pm_code}")
            
        except Exception as e:
            self.logger.error(f"Error generating PM: {e}")
            result.errors.append(str(e))
        
        return result
    
    def _get_pm_number_for_type(self) -> str:
        """Get PM number based on publication type."""
        pm_numbers = {
            PublicationType.AMM: "00001",
            PublicationType.SRM: "00002",
            PublicationType.CMM: "00003",
            PublicationType.IPC: "00004",
            PublicationType.FCOM: "00005",
            PublicationType.TSM: "00006",
            PublicationType.WDM: "00007",
            PublicationType.SB: "00008"
        }
        return pm_numbers.get(self.publication_type, "00001")
    
    def _get_title_for_type(self) -> str:
        """Get default title based on publication type."""
        titles = {
            PublicationType.AMM: "Aircraft Maintenance Manual",
            PublicationType.SRM: "Structural Repair Manual",
            PublicationType.CMM: "Component Maintenance Manual",
            PublicationType.IPC: "Illustrated Parts Catalog",
            PublicationType.FCOM: "Flight Crew Operating Manual",
            PublicationType.TSM: "Troubleshooting Manual",
            PublicationType.WDM: "Wiring Diagram Manual",
            PublicationType.SB: "Service Bulletin"
        }
        return titles.get(self.publication_type, "Technical Publication")
    
    def _create_pm_address(
        self, 
        ident_status: ET.Element, 
        pm_code: PMCode,
        title: str
    ) -> None:
        """Create pmAddress element."""
        pm_address = self.create_sub_element(ident_status, "pmAddress")
        
        # pmIdent
        pm_ident = self.create_sub_element(pm_address, "pmIdent")
        self.create_sub_element(pm_ident, "pmCode", attrib=pm_code.to_xml_attributes())
        self.create_sub_element(pm_ident, "language", attrib={
            "languageIsoCode": self.config.language_code,
            "countryIsoCode": self.config.country_code
        })
        self.create_sub_element(pm_ident, "issueInfo", attrib={
            "issueNumber": "001",
            "inWork": "00"
        })
        
        # pmAddressItems
        pm_address_items = self.create_sub_element(pm_address, "pmAddressItems")
        today = date.today()
        self.create_sub_element(pm_address_items, "issueDate", attrib={
            "year": str(today.year),
            "month": f"{today.month:02d}",
            "day": f"{today.day:02d}"
        })
        self.create_sub_element(pm_address_items, "pmTitle", text=title)
        self.create_sub_element(pm_address_items, "shortPmTitle", text=self.publication_type.value.upper())
    
    def _create_pm_status(self, ident_status: ET.Element, pm_code: PMCode) -> None:
        """Create pmStatus element."""
        pm_status = self.create_sub_element(ident_status, "pmStatus", attrib={"issueType": "new"})
        
        self.create_sub_element(pm_status, "security", attrib={
            "securityClassification": self.config.security_classification.value
        })
        
        rpc = self.create_sub_element(pm_status, "responsiblePartnerCompany")
        self.create_sub_element(rpc, "enterpriseName", text=self.config.organization_name)
        
        orig = self.create_sub_element(pm_status, "originator")
        self.create_sub_element(orig, "enterpriseName", text=self.config.organization_name)
        self.create_sub_element(orig, "enterpriseIdent", text=self.config.organization_cage)
        
        applic = self.create_sub_element(pm_status, "applic")
        display_text = self.create_sub_element(applic, "displayText")
        self.create_sub_element(display_text, "simplePara", text="All")
        
        qa = self.create_sub_element(pm_status, "qualityAssurance")
        self.create_sub_element(qa, "unverified")
    
    def _generate_pm_structure(
        self, 
        root_entry: ET.Element, 
        content: Dict[str, Any],
        dm_refs: List[DMCode]
    ) -> None:
        """Generate PM entry structure based on publication type."""
        # Front matter
        front_matter = self.create_sub_element(root_entry, "pmEntry", attrib={"pmEntryType": "pmt51"})
        self.create_sub_element(front_matter, "pmEntryTitle", text="Front Matter")
        
        # Chapter entries from content
        chapters = content.get("chapters", [])
        for chapter in chapters:
            if isinstance(chapter, dict):
                chapter_entry = self.create_sub_element(root_entry, "pmEntry", attrib={"pmEntryType": "pmt52"})
                self.create_sub_element(chapter_entry, "pmEntryTitle", 
                                        text=f"ATA {chapter.get('ata_chapter', '00')} - {chapter.get('title', 'Chapter')}")
        
        # Add DM references
        for dmc in dm_refs:
            self._add_dm_reference(root_entry, dmc)
    
    def _add_dm_reference(self, parent: ET.Element, dmc: DMCode) -> None:
        """Add DM reference to PM entry."""
        dm_ref = self.create_sub_element(parent, "dmRef")
        dm_ref_ident = self.create_sub_element(dm_ref, "dmRefIdent")
        self.create_sub_element(dm_ref_ident, "dmCode", attrib=dmc.to_xml_attributes())


# =============================================================================
# DATA MODULE LIST GENERATOR
# =============================================================================


class DMLGenerator(BaseGenerator):
    """
    Generator for S1000D Data Module Lists.
    
    Generates CSDB content inventories and delivery lists.
    """
    
    def __init__(
        self, 
        config: GeneratorConfig, 
        context: Optional[ExecutionContext] = None,
        dml_type: DMLType = DMLType.CSDB
    ):
        super().__init__(config, context)
        self.dml_type = dml_type
    
    def generate(
        self, 
        source: Optional[SourceArtifact] = None,
        dml_code: Optional[DMLCode] = None,
        title: Optional[str] = None,
        dm_list: Optional[List[DMCode]] = None,
        **kwargs
    ) -> GenerationResult:
        """
        Generate Data Module List.
        
        Args:
            source: Optional source artifact
            dml_code: DML code
            title: DML title
            dm_list: List of DMCs to include
            **kwargs: Additional options
            
        Returns:
            GenerationResult with XML content
        """
        result = GenerationResult(
            success=False,
            generation_time=datetime.now()
        )
        
        try:
            # Build DML code if not provided
            if dml_code is None:
                dml_code = DMLCode(
                    model_ident_code=self.config.model_ident_code,
                    sender_ident=self.config.organization_cage,
                    dml_type=self.dml_type.value
                )
            
            if title is None:
                title = f"Data Module List - {self.dml_type.name}"
            
            # Create DML root
            dml = self.create_xml_element("dml")
            
            # Ident and status section
            ident_status = self.create_sub_element(dml, "identAndStatusSection")
            self._create_dml_address(ident_status, dml_code, title)
            self._create_dml_status(ident_status, dml_code)
            
            # Content section
            dml_content = self.create_sub_element(dml, "dmlContent")
            
            # Add DM entries
            for dmc in (dm_list or []):
                self._add_dml_entry(dml_content, dmc)
            
            xml_string = self.prettify_xml(dml)
            
            output = OutputArtifact(
                id=f"DML-{dml_code}",
                path=Path(f"{dml_code}.xml"),
                artifact_type=ArtifactType.DML,
                dmc=str(dml_code),
                source_refs=[source.id] if source else [],
                generated_at=datetime.now(),
                valid=True
            )
            
            result.success = True
            result.artifact = output
            result.xml_content = xml_string
            result.dmc = str(dml_code)
            
            self.logger.info(f"Generated DML: {dml_code}")
            
        except Exception as e:
            self.logger.error(f"Error generating DML: {e}")
            result.errors.append(str(e))
        
        return result
    
    def _create_dml_address(
        self, 
        ident_status: ET.Element, 
        dml_code: DMLCode,
        title: str
    ) -> None:
        """Create dmlAddress element."""
        dml_address = self.create_sub_element(ident_status, "dmlAddress")
        
        # dmlIdent
        dml_ident = self.create_sub_element(dml_address, "dmlIdent")
        self.create_sub_element(dml_ident, "dmlCode", attrib=dml_code.to_xml_attributes())
        self.create_sub_element(dml_ident, "issueInfo", attrib={
            "issueNumber": "001",
            "inWork": "00"
        })
        
        # dmlAddressItems
        dml_address_items = self.create_sub_element(dml_address, "dmlAddressItems")
        today = date.today()
        self.create_sub_element(dml_address_items, "issueDate", attrib={
            "year": str(today.year),
            "month": f"{today.month:02d}",
            "day": f"{today.day:02d}"
        })
        self.create_sub_element(dml_address_items, "dmlTitle", text=title)
    
    def _create_dml_status(self, ident_status: ET.Element, dml_code: DMLCode) -> None:
        """Create dmlStatus element."""
        dml_status = self.create_sub_element(ident_status, "dmlStatus", attrib={"issueType": "new"})
        
        self.create_sub_element(dml_status, "security", attrib={
            "securityClassification": self.config.security_classification.value
        })
        
        rpc = self.create_sub_element(dml_status, "responsiblePartnerCompany")
        self.create_sub_element(rpc, "enterpriseName", text=self.config.organization_name)
        
        orig = self.create_sub_element(dml_status, "originator")
        self.create_sub_element(orig, "enterpriseName", text=self.config.organization_name)
        self.create_sub_element(orig, "enterpriseIdent", text=self.config.organization_cage)
        
        qa = self.create_sub_element(dml_status, "qualityAssurance")
        self.create_sub_element(qa, "unverified")
    
    def _add_dml_entry(self, dml_content: ET.Element, dmc: DMCode) -> None:
        """Add DML entry for a DM."""
        dml_entry = self.create_sub_element(dml_content, "dmlEntry")
        
        # DM reference
        dm_ref = self.create_sub_element(dml_entry, "dmRef")
        dm_ref_ident = self.create_sub_element(dm_ref, "dmRefIdent")
        self.create_sub_element(dm_ref_ident, "dmCode", attrib=dmc.to_xml_attributes())
        self.create_sub_element(dm_ref_ident, "language", attrib={
            "languageIsoCode": self.config.language_code,
            "countryIsoCode": self.config.country_code
        })
        self.create_sub_element(dm_ref_ident, "issueInfo", attrib={
            "issueNumber": "001",
            "inWork": "00"
        })
        
        # Entry status
        entry_status = self.create_sub_element(dml_entry, "dmlEntryStatus")
        self.create_sub_element(entry_status, "answer", attrib={"answerStatusCode": "0"})
        
        rpc = self.create_sub_element(entry_status, "responsiblePartnerCompany")
        self.create_sub_element(rpc, "enterpriseName", text=self.config.organization_name)
        
        self.create_sub_element(entry_status, "security", attrib={
            "securityClassification": self.config.security_classification.value
        })


# =============================================================================
# ICN HANDLER
# =============================================================================


class ICNHandler(BaseGenerator):
    """
    Handler for Information Control Numbers (graphics/multimedia).
    
    Processes and generates ICN references and metadata.
    """
    
    SUPPORTED_FORMATS = [".png", ".jpg", ".jpeg", ".tif", ".tiff", ".svg", ".cgm", ".gif", ".pdf"]
    
    def generate(
        self, 
        source: SourceArtifact,
        icn_code: Optional[ICNCode] = None,
        **kwargs
    ) -> GenerationResult:
        """
        Process graphic and generate ICN.
        
        Args:
            source: Source graphic artifact
            icn_code: Optional ICN code
            **kwargs: Additional options
            
        Returns:
            GenerationResult with ICN info
        """
        result = GenerationResult(
            success=False,
            generation_time=datetime.now()
        )
        
        try:
            # Validate graphic format
            if source.path.suffix.lower() not in self.SUPPORTED_FORMATS:
                result.errors.append(f"Unsupported graphic format: {source.path.suffix}")
                return result
            
            content = source.content or {}
            
            # Build ICN code if not provided
            if icn_code is None:
                icn_code = ICNCode(
                    model_ident_code=self.config.model_ident_code,
                    system_code=content.get("ata_chapter", "00"),
                    figure_number=content.get("figure_number", "00001")
                )
            
            # Create output artifact
            output = OutputArtifact(
                id=icn_code.full_code,
                path=source.path,
                artifact_type=ArtifactType.ICN,
                dmc=icn_code.full_code,
                source_refs=[source.id],
                generated_at=datetime.now(),
                valid=True
            )
            
            trace = self.create_trace_link(source, output, "graphic_to_icn")
            
            result.success = True
            result.artifact = output
            result.dmc = icn_code.full_code
            result.trace_links = [trace]
            
            self.logger.info(f"Processed ICN: {icn_code.full_code}")
            
        except Exception as e:
            self.logger.error(f"Error processing ICN: {e}")
            result.errors.append(str(e))
        
        return result


# =============================================================================
# APPLICABILITY PROCESSOR
# =============================================================================


@dataclass
class ApplicabilityCondition:
    """Represents an applicability condition."""
    property_ident: str
    property_type: str
    property_values: List[str] = field(default_factory=list)
    operator: str = "="


@dataclass
class ApplicabilityAssertion:
    """Represents an applicability assertion."""
    conditions: List[ApplicabilityCondition] = field(default_factory=list)
    display_text: str = "All"


class ApplicabilityProcessor:
    """
    Processor for S1000D applicability (ACT/PCT/CCT).
    
    Handles applicability cross-reference tables and assertions.
    """
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
        self.logger = logging.getLogger("asigt.applicability")
        
        # ACT (Applicability Cross-reference Table)
        self.act_properties: Dict[str, Dict[str, Any]] = {}
        
        # PCT (Product Cross-reference Table)
        self.pct_products: Dict[str, Dict[str, Any]] = {}
        
        # CCT (Conditions Cross-reference Table)
        self.cct_conditions: Dict[str, Dict[str, Any]] = {}
    
    def register_product(
        self, 
        product_id: str,
        product_name: str,
        serial_range: Optional[Tuple[str, str]] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> None:
        """Register a product in the PCT."""
        self.pct_products[product_id] = {
            "name": product_name,
            "serial_from": serial_range[0] if serial_range else None,
            "serial_to": serial_range[1] if serial_range else None,
            "properties": properties or {}
        }
        self.logger.debug(f"Registered product: {product_id}")
    
    def register_condition(
        self, 
        condition_id: str,
        condition_type: str,
        description: str
    ) -> None:
        """Register a condition in the CCT."""
        self.cct_conditions[condition_id] = {
            "type": condition_type,
            "description": description
        }
        self.logger.debug(f"Registered condition: {condition_id}")
    
    def create_assertion(
        self,
        model: Optional[str] = None,
        serial_from: Optional[str] = None,
        serial_to: Optional[str] = None,
        conditions: Optional[List[str]] = None
    ) -> ApplicabilityAssertion:
        """Create an applicability assertion."""
        assertion = ApplicabilityAssertion()
        
        # Model assertion
        if model:
            assertion.conditions.append(ApplicabilityCondition(
                property_ident="model",
                property_type="prodattr",
                property_values=[model]
            ))
        
        # Serial range
        if serial_from:
            assertion.conditions.append(ApplicabilityCondition(
                property_ident="serialNumber",
                property_type="prodattr",
                property_values=[serial_from] if not serial_to else [serial_from, serial_to],
                operator=">=" if serial_to else "="
            ))
        
        # Build display text
        parts = []
        if model:
            parts.append(model)
        if serial_from and serial_to:
            parts.append(f"S/N {serial_from} thru {serial_to}")
        elif serial_from:
            parts.append(f"S/N {serial_from} and subsequent")
        
        assertion.display_text = ", ".join(parts) if parts else "All"
        
        return assertion
    
    def format_display_text(self, assertion: ApplicabilityAssertion) -> str:
        """Format assertion as display text."""
        return assertion.display_text
    
    def generate_applic_element(
        self, 
        parent: ET.Element, 
        assertion: ApplicabilityAssertion,
        ns: str = ""
    ) -> ET.Element:
        """Generate applic XML element from assertion."""
        ns_prefix = f"{{{ns}}}" if ns else ""
        
        applic = ET.SubElement(parent, f"{ns_prefix}applic")
        
        # Display text
        display_text = ET.SubElement(applic, f"{ns_prefix}displayText")
        simple_para = ET.SubElement(display_text, f"{ns_prefix}simplePara")
        simple_para.text = assertion.display_text
        
        # Assertions
        for condition in assertion.conditions:
            assert_elem = ET.SubElement(applic, f"{ns_prefix}assert", attrib={
                "applicPropertyIdent": condition.property_ident,
                "applicPropertyType": condition.property_type,
                "applicPropertyValues": " ".join(condition.property_values)
            })
        
        return applic


# =============================================================================
# UNIFIED GENERATOR FACADE
# =============================================================================


class DMGenerator:
    """
    Unified Data Module generator facade.
    
    Provides a single entry point for generating all DM types.
    Delegates to specific generators based on content type.
    """
    
    def __init__(self, config: GeneratorConfig, context: Optional[ExecutionContext] = None):
        self.config = config
        self.context = context
        self.logger = logging.getLogger("asigt.generator.dm")
        
        # Initialize specialized generators
        self._descriptive = DescriptiveDMGenerator(config, context)
        self._procedural = ProceduralDMGenerator(config, context)
        self._ipd = IPDGenerator(config, context)
        self._fault_isolation = FaultIsolationDMGenerator(config, context)
    
    def generate(self, source: SourceArtifact, **kwargs) -> GenerationResult:
        """
        Generate DM based on source artifact type.
        
        Automatically detects the appropriate generator.
        
        Args:
            source: Source artifact
            **kwargs: Additional parameters
            
        Returns:
            GenerationResult
        """
        # Determine DM type from source
        dm_type = self._determine_dm_type(source)
        
        self.logger.info(f"Generating {dm_type.value} DM from source: {source.id}")
        
        # Delegate to appropriate generator
        if dm_type == DMType.DESCRIPTIVE:
            return self._descriptive.generate(source, **kwargs)
        elif dm_type == DMType.PROCEDURAL:
            return self._procedural.generate(source, **kwargs)
        elif dm_type == DMType.IPD:
            return self._ipd.generate(source, **kwargs)
        elif dm_type == DMType.FAULT_ISOLATION:
            return self._fault_isolation.generate(source, **kwargs)
        else:
            result = GenerationResult(success=False)
            result.errors.append(f"Unsupported DM type: {dm_type}")
            return result
    
    def generate_descriptive(self, source: SourceArtifact, **kwargs) -> GenerationResult:
        """Generate descriptive DM."""
        return self._descriptive.generate(source, **kwargs)
    
    def generate_procedural(self, source: SourceArtifact, **kwargs) -> GenerationResult:
        """Generate procedural DM."""
        return self._procedural.generate(source, **kwargs)
    
    def generate_ipd(self, source: SourceArtifact, **kwargs) -> GenerationResult:
        """Generate IPD DM."""
        return self._ipd.generate(source, **kwargs)
    
    def generate_fault_isolation(self, source: SourceArtifact, **kwargs) -> GenerationResult:
        """Generate fault isolation DM."""
        return self._fault_isolation.generate(source, **kwargs)
    
    def _determine_dm_type(self, source: SourceArtifact) -> DMType:
        """Determine DM type from source artifact."""
        # Check artifact type first
        type_mapping = {
            ArtifactType.REQUIREMENT: DMType.DESCRIPTIVE,
            ArtifactType.TASK: DMType.PROCEDURAL,
            ArtifactType.FAULT_DATA: DMType.FAULT_ISOLATION,
            ArtifactType.PART: DMType.IPD
        }
        
        if source.artifact_type in type_mapping:
            return type_mapping[source.artifact_type]
        
        # Check content
        content = source.content or {}
        content_type = content.get("type", content.get("dm_type", ""))
        
        if content_type in ["description", "theory", "overview", "functional", "requirement"]:
            return DMType.DESCRIPTIVE
        elif content_type in ["procedure", "task", "removal", "installation", "servicing", "inspection"]:
            return DMType.PROCEDURAL
        elif content_type in ["parts", "ipd", "bom", "catalog"]:
            return DMType.IPD
        elif content_type in ["fault", "troubleshooting", "isolation"]:
            return DMType.FAULT_ISOLATION
        
        # Default to descriptive
        return DMType.DESCRIPTIVE


# =============================================================================
# MODULE EXPORTS
# =============================================================================


__all__ = [
    # Enumerations
    "DMType",
    "InfoCodeCategory",
    "PublicationType",
    "DMLType",
    "ApplicabilityType",
    "SecurityClassification",
    "MaintenanceLevel",
    "QualityAssuranceStatus",
    
    # Code structures
    "DMCode",
    "PMCode",
    "DMLCode",
    "ICNCode",
    
    # Configuration
    "GeneratorConfig",
    "GenerationResult",
    
    # Metadata and content structures
    "DMMetadata",
    "ProceduralStep",
    "PreliminaryRequirements",
    "PartItem",
    "CatalogSeqNumber",
    
    # Generators
    "BaseGenerator",
    "DescriptiveDMGenerator",
    "ProceduralDMGenerator",
    "IPDGenerator",
    "FaultIsolationDMGenerator",
    "PMGenerator",
    "DMLGenerator",
    "ICNHandler",
    
    # Unified facade
    "DMGenerator",
    
    # Applicability
    "ApplicabilityCondition",
    "ApplicabilityAssertion",
    "ApplicabilityProcessor",
]
