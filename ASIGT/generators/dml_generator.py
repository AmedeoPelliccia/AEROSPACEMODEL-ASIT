# =============================================================================
# ASIGT Data Module List Generator
# S1000D Data Module List generation under ASIT contract authority
# Version: 2.0.0
# =============================================================================
"""
Data Module List Generator

Generates S1000D-compliant Data Module Lists (DML) for tracking and
managing collections of Data Modules. Operates exclusively under
ASIT contract authority.

DML Types:
    - CSDB DML: Complete listing of all DMs in the Common Source Database
    - Delivery DML: DMs included in a specific delivery/release
    - Change DML: DMs affected by a specific change (ECO/ECR)
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


class DMLType(Enum):
    """Types of Data Module Lists."""
    CSDB = "csdb"           # Complete CSDB listing
    DELIVERY = "delivery"   # Delivery package
    CHANGE = "change"       # Change-specific DML
    SUBSET = "subset"       # Filtered subset


@dataclass
class DMLCode:
    """
    S1000D Data Module List Code (DMLC) structure.
    
    Format: MODEL-SENDER-DMLTYPE-YEAR-SEQUENCE
    Example: HJ1-GAVIN-C-2026-00001
    """
    model_ident_code: str           # 2-14 chars, aircraft model
    sender_ident: str = "00001"     # Sender identification
    dml_type: str = "C"             # C=CSDB, S=subset, P=package
    year_of_data_issue: str = field(
        default_factory=lambda: datetime.now().strftime("%Y")
    )
    seq_number: str = "00001"       # Sequence number
    
    def __str__(self) -> str:
        """Generate DMLC string representation."""
        return f"DML-{self.model_ident_code}-{self.sender_ident}-{self.dml_type}-{self.year_of_data_issue}-{self.seq_number}"
    
    @classmethod
    def from_string(cls, dmlc_string: str) -> "DMLCode":
        """Parse DMLC from string representation."""
        if dmlc_string.startswith("DML-"):
            dmlc_string = dmlc_string[4:]
        
        parts = dmlc_string.split("-")
        if len(parts) < 5:
            raise ValueError(f"Invalid DMLC format: {dmlc_string}")
        
        return cls(
            model_ident_code=parts[0],
            sender_ident=parts[1],
            dml_type=parts[2],
            year_of_data_issue=parts[3],
            seq_number=parts[4],
        )


@dataclass
class DMLEntry:
    """Entry in a Data Module List."""
    dm_code: str
    issue_number: str = "001"
    in_work: str = "00"
    issue_type: str = "new"  # new, changed, deleted, status
    security_classification: str = "01"
    responsible_partner_company: Optional[str] = None
    title: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "dm_code": self.dm_code,
            "issue_number": self.issue_number,
            "in_work": self.in_work,
            "issue_type": self.issue_type,
            "security_classification": self.security_classification,
            "responsible_partner_company": self.responsible_partner_company,
            "title": self.title,
        }


@dataclass
class DMLGenerationResult:
    """Result of DML generation operation."""
    success: bool
    dml_code: str
    dml_type: str
    dm_count: int = 0
    output_path: Optional[Path] = None
    xml_content: Optional[str] = None
    dm_entries: List[str] = field(default_factory=list)
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    input_hash: Optional[str] = None
    output_hash: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())


class DMLGenerator:
    """
    S1000D Data Module List Generator.
    
    Generates Data Module Lists for tracking and managing collections
    of Data Modules. All generation is traced and auditable under
    ASIT contract authority.
    
    Attributes:
        contract: ASIT transformation contract
        config: Generator configuration
        
    Example:
        >>> contract = load_contract("KITDM-CTR-LM-CSDB_ATA28")
        >>> generator = DMLGenerator(contract=contract, config=config)
        >>> result = generator.generate_csdb_dml(dm_list=data_modules)
    """
    
    # S1000D Issue 5.0 namespace
    S1000D_NS = "http://www.s1000d.org/S1000D_5-0"
    
    def __init__(
        self,
        contract: Dict[str, Any],
        config: Dict[str, Any],
    ):
        """
        Initialize DML Generator.
        
        Args:
            contract: ASIT transformation contract (required)
            config: Generator configuration
            
        Raises:
            ValueError: If contract is missing or invalid
        """
        if not contract:
            raise ValueError("ASIT contract is required for DML generation")
        
        self.contract = contract
        self.config = config
        
        # Extract contract parameters
        self.contract_id = contract.get("id", "UNKNOWN")
        self.baseline_ref = contract.get("source", {}).get("baseline", "UNKNOWN")
        self.model_code = config.get("model_ident_code", "XXX")
        
        # Generation tracking
        self._generation_log: List[DMLGenerationResult] = []
        self._dml_counter = 0
        
        logger.info(
            f"DMLGenerator initialized: contract={self.contract_id}, "
            f"baseline={self.baseline_ref}"
        )
    
    def generate(
        self,
        dm_list: List[Dict[str, Any]],
        dml_type: DMLType = DMLType.CSDB,
        dmlc: Optional[DMLCode] = None,
        remarks: Optional[str] = None,
    ) -> DMLGenerationResult:
        """
        Generate a Data Module List.
        
        Args:
            dm_list: List of Data Modules to include
            dml_type: Type of DML to generate
            dmlc: Optional pre-defined DMLC
            remarks: Optional remarks for the DML
            
        Returns:
            DMLGenerationResult with XML content and trace info
        """
        # Build DMLC if not provided
        if dmlc is None:
            self._dml_counter += 1
            dml_type_code = {
                DMLType.CSDB: "C",
                DMLType.DELIVERY: "P",
                DMLType.CHANGE: "S",
                DMLType.SUBSET: "S",
            }.get(dml_type, "C")
            
            dmlc = DMLCode(
                model_ident_code=self.model_code,
                dml_type=dml_type_code,
                seq_number=f"{self._dml_counter:05d}",
            )
        
        # Calculate input hash
        input_hash = self._compute_hash(str(dm_list))
        
        # Convert to DML entries
        entries = self._convert_to_entries(dm_list)
        
        # Generate XML structure
        root = self._create_dml_root()
        
        # Add identification section
        ident_section = self._build_dml_ident_section(dmlc, dml_type, remarks)
        root.append(ident_section)
        
        # Add content section with DM entries
        content_section = self._build_dml_content(entries)
        root.append(content_section)
        
        # Serialize to XML
        xml_content = self._serialize_xml(root)
        output_hash = self._compute_hash(xml_content)
        
        # Build result
        dm_codes = [entry.dm_code for entry in entries]
        
        result = DMLGenerationResult(
            success=True,
            dml_code=str(dmlc),
            dml_type=dml_type.value,
            dm_count=len(entries),
            xml_content=xml_content,
            dm_entries=dm_codes,
            input_hash=input_hash,
            output_hash=output_hash,
        )
        
        self._generation_log.append(result)
        return result
    
    def generate_csdb_dml(
        self,
        dm_list: List[Dict[str, Any]],
        remarks: Optional[str] = None,
    ) -> DMLGenerationResult:
        """
        Generate a CSDB Data Module List.
        
        Complete listing of all Data Modules in the Common Source Database.
        
        Args:
            dm_list: All Data Modules in CSDB
            remarks: Optional remarks
            
        Returns:
            DMLGenerationResult
        """
        return self.generate(
            dm_list=dm_list,
            dml_type=DMLType.CSDB,
            remarks=remarks or "Complete CSDB listing",
        )
    
    def generate_delivery_dml(
        self,
        dm_list: List[Dict[str, Any]],
        delivery_id: str,
        remarks: Optional[str] = None,
    ) -> DMLGenerationResult:
        """
        Generate a Delivery Data Module List.
        
        DMs included in a specific delivery/release package.
        
        Args:
            dm_list: Data Modules in delivery
            delivery_id: Delivery identifier
            remarks: Optional remarks
            
        Returns:
            DMLGenerationResult
        """
        return self.generate(
            dm_list=dm_list,
            dml_type=DMLType.DELIVERY,
            remarks=remarks or f"Delivery package: {delivery_id}",
        )
    
    def generate_change_dml(
        self,
        dm_list: List[Dict[str, Any]],
        change_id: str,
        change_type: str = "ECO",
        remarks: Optional[str] = None,
    ) -> DMLGenerationResult:
        """
        Generate a Change Data Module List.
        
        DMs affected by a specific change (ECO/ECR).
        
        Args:
            dm_list: Data Modules affected by change
            change_id: Change identifier (ECO/ECR number)
            change_type: Type of change (ECO, ECR)
            remarks: Optional remarks
            
        Returns:
            DMLGenerationResult
        """
        return self.generate(
            dm_list=dm_list,
            dml_type=DMLType.CHANGE,
            remarks=remarks or f"{change_type}: {change_id}",
        )
    
    def generate_subset_dml(
        self,
        dm_list: List[Dict[str, Any]],
        filter_criteria: Dict[str, Any],
        remarks: Optional[str] = None,
    ) -> DMLGenerationResult:
        """
        Generate a Subset Data Module List.
        
        Filtered subset based on criteria (ATA chapter, effectivity, etc.).
        
        Args:
            dm_list: Data Modules matching filter
            filter_criteria: Filter criteria used
            remarks: Optional remarks
            
        Returns:
            DMLGenerationResult
        """
        criteria_str = ", ".join(f"{k}={v}" for k, v in filter_criteria.items())
        return self.generate(
            dm_list=dm_list,
            dml_type=DMLType.SUBSET,
            remarks=remarks or f"Subset: {criteria_str}",
        )
    
    def _convert_to_entries(
        self,
        dm_list: List[Dict[str, Any]],
    ) -> List[DMLEntry]:
        """Convert DM dictionaries to DMLEntry objects."""
        entries = []
        
        for dm in dm_list:
            entry = DMLEntry(
                dm_code=dm.get("dm_code", dm.get("id", "unknown")),
                issue_number=dm.get("issue_number", "001"),
                in_work=dm.get("in_work", "00"),
                issue_type=dm.get("issue_type", "new"),
                security_classification=dm.get("security_classification", "01"),
                responsible_partner_company=dm.get(
                    "responsible_partner_company",
                    self.config.get("organization"),
                ),
                title=dm.get("title", dm.get("tech_name")),
            )
            entries.append(entry)
        
        return entries
    
    def _create_dml_root(self) -> ET.Element:
        """Create S1000D dml root element."""
        root = ET.Element("dml")
        root.set("xmlns", self.S1000D_NS)
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        return root
    
    def _build_dml_ident_section(
        self,
        dmlc: DMLCode,
        dml_type: DMLType,
        remarks: Optional[str],
    ) -> ET.Element:
        """Build DML identification section."""
        section = ET.Element("identAndStatusSection")
        
        # dmlAddress
        dml_address = ET.SubElement(section, "dmlAddress")
        
        # dmlIdent
        dml_ident = ET.SubElement(dml_address, "dmlIdent")
        
        # dmlCode
        dml_code = ET.SubElement(dml_ident, "dmlCode")
        dml_code.set("modelIdentCode", dmlc.model_ident_code)
        dml_code.set("senderIdent", dmlc.sender_ident)
        dml_code.set("dmlType", dmlc.dml_type)
        dml_code.set("yearOfDataIssue", dmlc.year_of_data_issue)
        dml_code.set("seqNumber", dmlc.seq_number)
        
        # issueInfo
        issue_info = ET.SubElement(dml_ident, "issueInfo")
        issue_info.set("issueNumber", "001")
        issue_info.set("inWork", "00")
        
        # dmlAddressItems
        dml_address_items = ET.SubElement(dml_address, "dmlAddressItems")
        
        # issueDate
        issue_date = ET.SubElement(dml_address_items, "issueDate")
        now = datetime.now()
        issue_date.set("year", str(now.year))
        issue_date.set("month", f"{now.month:02d}")
        issue_date.set("day", f"{now.day:02d}")
        
        # dmlStatus
        dml_status = ET.SubElement(section, "dmlStatus")
        dml_status.set("issueType", "new")
        
        # security
        security = ET.SubElement(dml_status, "security")
        security.set("securityClassification", "01")
        
        # responsiblePartnerCompany
        rpc = ET.SubElement(dml_status, "responsiblePartnerCompany")
        enterprise = ET.SubElement(rpc, "enterpriseName")
        enterprise.text = self.config.get("organization", "AEROSPACEMODEL")
        
        # remarks
        if remarks:
            remarks_elem = ET.SubElement(dml_status, "remarks")
            simple_para = ET.SubElement(remarks_elem, "simplePara")
            simple_para.text = remarks
        
        return section
    
    def _build_dml_content(self, entries: List[DMLEntry]) -> ET.Element:
        """Build DML content section with DM entries."""
        content = ET.Element("dmlContent")
        
        for entry in entries:
            dml_entry = ET.SubElement(content, "dmlEntry")
            
            # dmRef
            dm_ref = ET.SubElement(dml_entry, "dmRef")
            dm_ref_ident = ET.SubElement(dm_ref, "dmRefIdent")
            
            # dmCode
            dm_code = ET.SubElement(dm_ref_ident, "dmCode")
            
            # Parse DMC from string
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
                dm_code.set("modelIdentCode", entry.dm_code)
            
            # issueInfo
            issue_info = ET.SubElement(dm_ref_ident, "issueInfo")
            issue_info.set("issueNumber", entry.issue_number)
            issue_info.set("inWork", entry.in_work)
            
            # dmRefAddressItems
            if entry.title:
                dm_ref_address = ET.SubElement(dm_ref, "dmRefAddressItems")
                dm_title = ET.SubElement(dm_ref_address, "dmTitle")
                tech_name = ET.SubElement(dm_title, "techName")
                tech_name.text = entry.title
            
            # security
            security = ET.SubElement(dml_entry, "security")
            security.set("securityClassification", entry.security_classification)
            
            # responsiblePartnerCompany
            if entry.responsible_partner_company:
                rpc = ET.SubElement(dml_entry, "responsiblePartnerCompany")
                enterprise = ET.SubElement(rpc, "enterpriseName")
                enterprise.text = entry.responsible_partner_company
        
        return content
    
    def _serialize_xml(self, root: ET.Element) -> str:
        """Serialize XML element to string."""
        ET.indent(root, space="  ")
        return ET.tostring(root, encoding="unicode", xml_declaration=True)
    
    def _compute_hash(self, content: str) -> str:
        """Compute SHA-256 hash of content."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()
    
    def get_generation_log(self) -> List[DMLGenerationResult]:
        """Get log of all generation operations."""
        return self._generation_log.copy()
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary of all generated DMLs.
        
        Returns:
            Summary statistics
        """
        total_dms = sum(result.dm_count for result in self._generation_log)
        
        return {
            "contract_id": self.contract_id,
            "baseline_ref": self.baseline_ref,
            "dml_count": len(self._generation_log),
            "total_dm_entries": total_dms,
            "dml_types": [result.dml_type for result in self._generation_log],
            "successful": sum(1 for r in self._generation_log if r.success),
            "failed": sum(1 for r in self._generation_log if not r.success),
        }
