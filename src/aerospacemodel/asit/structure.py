"""
ASIT Structure Module

Defines the structural framework for aerospace information management:
- ATA iSpec 2200 chapter mapping and system breakdown
- KDB/IDB partitioning rules
- Lifecycle phases (LC01-LC14)
- Naming conventions and ID grammar

This module provides the structural authority that governs how
information is organized, identified, and partitioned.
"""

from __future__ import annotations

import re
import yaml
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Pattern,
    Union,
)

logger = logging.getLogger(__name__)


# =============================================================================
# EXCEPTIONS
# =============================================================================


class StructureError(Exception):
    """Base exception for structure-related errors."""
    pass


class ATAMappingError(StructureError):
    """Error related to ATA chapter mapping."""
    pass


class LifecyclePhaseError(StructureError):
    """Error related to lifecycle phase operations."""
    pass


class NamingConventionError(StructureError):
    """Error related to naming conventions."""
    pass


class IDValidationError(NamingConventionError):
    """Error when an ID fails validation."""
    pass


class PartitionError(StructureError):
    """Error related to KDB/IDB partitioning."""
    pass


# =============================================================================
# ENUMERATIONS
# =============================================================================


class DatabaseType(Enum):
    """Database type enumeration (KDB vs IDB)."""
    KDB = "KDB"  # Knowledge Database
    IDB = "IDB"  # Information Database


class KDBCategory(Enum):
    """KDB content categories."""
    REQUIREMENTS = "REQUIREMENTS"
    DESIGN = "DESIGN"
    ANALYSIS = "ANALYSIS"
    TEST = "TEST"
    CERTIFICATION = "CERTIFICATION"


class IDBCategory(Enum):
    """IDB content categories (publication types)."""
    MAINTENANCE = "MAINTENANCE"
    OPERATIONS = "OPERATIONS"
    PARTS = "PARTS"
    SERVICE = "SERVICE"
    TRAINING = "TRAINING"


class LifecyclePhase(Enum):
    """Aircraft program lifecycle phases LC01-LC14."""
    LC01 = "LC01"  # Concept
    LC02 = "LC02"  # Requirements
    LC03 = "LC03"  # Design
    LC04 = "LC04"  # Development
    LC05 = "LC05"  # Verification
    LC06 = "LC06"  # Certification
    LC07 = "LC07"  # Production
    LC08 = "LC08"  # Delivery
    LC09 = "LC09"  # Operations
    LC10 = "LC10"  # Maintenance
    LC11 = "LC11"  # Modification
    LC12 = "LC12"  # Storage
    LC13 = "LC13"  # Retirement
    LC14 = "LC14"  # Disposal


class StakeholderCode(Enum):
    """Stakeholder codes."""
    STK_ENG = "STK_ENG"      # Engineering
    STK_CERT = "STK_CERT"    # Certification
    STK_CM = "STK_CM"        # Configuration Management
    STK_QA = "STK_QA"        # Quality Assurance
    STK_MFG = "STK_MFG"      # Manufacturing
    STK_OPS = "STK_OPS"      # Operations
    STK_MRO = "STK_MRO"      # Maintenance/Repair/Overhaul
    STK_BUS = "STK_BUS"      # Business/Program


class BaselineTypeCode(Enum):
    """Baseline type codes used in naming."""
    FBL = "FBL"  # Functional Baseline
    ABL = "ABL"  # Allocated Baseline
    PBL = "PBL"  # Product Baseline
    OBL = "OBL"  # Operational Baseline


class ContractCategoryCode(Enum):
    """Contract category codes."""
    LM = "LM"      # Lifecycle Management
    OPS = "OPS"    # Operations
    MRO = "MRO"    # Maintenance/Repair/Overhaul
    TRN = "TRN"    # Training
    CERT = "CERT"  # Certification


class GraphicType(Enum):
    """ICN graphic type codes."""
    SH = "SH"  # Sheet (drawing)
    IL = "IL"  # Illustration
    PH = "PH"  # Photograph
    SC = "SC"  # Schematic
    WD = "WD"  # Wiring diagram
    MM = "MM"  # Multimedia


class InformationCode(Enum):
    """Common S1000D information codes."""
    FUNCTIONAL = "000"       # Function description
    DESCRIPTION = "040"      # Descriptive information
    OPERATION = "100"        # Operating procedures
    SERVICING = "200"        # Servicing procedures
    INSPECTION = "300"       # Inspection procedures
    REMOVAL = "400"          # Removal procedures
    INSTALLATION = "500"     # Installation procedures
    REPAIR = "600"           # Repair procedures
    SETTING_TEST = "700"     # Adjustment and test
    STORAGE = "800"          # Storage procedures
    PARTS = "900"            # Parts data
    IPD = "941"              # Illustrated Parts Data


# =============================================================================
# ATA CHAPTER DATA STRUCTURES
# =============================================================================


@dataclass
class ATASection:
    """Represents an ATA section within a chapter."""
    code: str
    title: str
    
    @property
    def chapter(self) -> str:
        """Extract chapter from section code."""
        return self.code.split("-")[0]
    
    @property
    def section_number(self) -> str:
        """Extract section number from code."""
        parts = self.code.split("-")
        return parts[1] if len(parts) > 1 else "00"


@dataclass
class ATAChapter:
    """Represents an ATA chapter per iSpec 2200."""
    code: str
    title: str
    description: str
    sections: Dict[str, ATASection] = field(default_factory=dict)
    
    @property
    def chapter_number(self) -> int:
        """Get chapter as integer."""
        return int(self.code)
    
    def get_section(self, section_code: str) -> Optional[ATASection]:
        """Get section by code."""
        return self.sections.get(section_code)
    
    def list_sections(self) -> List[ATASection]:
        """List all sections in order."""
        return sorted(self.sections.values(), key=lambda s: s.code)


@dataclass
class ATAMapping:
    """
    ATA iSpec 2200 chapter mapping.
    
    Provides system breakdown structure for aircraft information.
    """
    metadata: Dict[str, Any]
    chapters: Dict[str, ATAChapter] = field(default_factory=dict)
    mapping_rules: Dict[str, str] = field(default_factory=dict)
    
    @classmethod
    def from_yaml(cls, yaml_path: Path) -> "ATAMapping":
        """Load ATA mapping from YAML file."""
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        metadata = data.get("metadata", {})
        mapping_rules = data.get("mapping_rules", {})
        
        chapters = {}
        for code, chapter_data in data.get("chapters", {}).items():
            sections = {}
            for section_code, section_title in chapter_data.get("sections", {}).items():
                sections[section_code] = ATASection(
                    code=section_code,
                    title=section_title
                )
            
            chapters[code] = ATAChapter(
                code=code,
                title=chapter_data.get("title", ""),
                description=chapter_data.get("description", ""),
                sections=sections
            )
        
        return cls(
            metadata=metadata,
            chapters=chapters,
            mapping_rules=mapping_rules
        )
    
    def get_chapter(self, code: str) -> Optional[ATAChapter]:
        """Get chapter by code (e.g., '28' for Fuel)."""
        return self.chapters.get(code)
    
    def get_section(self, section_code: str) -> Optional[ATASection]:
        """Get section by full code (e.g., '28-10')."""
        chapter_code = section_code.split("-")[0]
        chapter = self.get_chapter(chapter_code)
        if chapter:
            return chapter.get_section(section_code)
        return None
    
    def get_system_code(self, ata_chapter: str, subsystem: str = "00", 
                        sub_subsystem: str = "00") -> str:
        """
        Convert ATA chapter to S1000D system code.
        
        Args:
            ata_chapter: ATA chapter (e.g., '28')
            subsystem: Subsystem code (e.g., '10')
            sub_subsystem: Sub-subsystem code (e.g., '00')
            
        Returns:
            System code for DMC (e.g., '28-10-00')
        """
        return f"{ata_chapter}-{subsystem}-{sub_subsystem}"
    
    def list_chapters(self) -> List[ATAChapter]:
        """List all chapters in order."""
        return sorted(self.chapters.values(), key=lambda c: c.code)
    
    def search_chapters(self, query: str) -> List[ATAChapter]:
        """Search chapters by title or description."""
        query_lower = query.lower()
        results = []
        for chapter in self.chapters.values():
            if (query_lower in chapter.title.lower() or 
                query_lower in chapter.description.lower()):
                results.append(chapter)
        return results


# =============================================================================
# LIFECYCLE PHASE DATA STRUCTURES
# =============================================================================


@dataclass
class PhaseGate:
    """Gate criteria for phase transitions."""
    entry: str
    exit: str


@dataclass
class PhaseBaselines:
    """Baselines associated with a phase."""
    established: List[str] = field(default_factory=list)
    consumed: List[str] = field(default_factory=list)


@dataclass
class PhaseStakeholders:
    """Stakeholders for a lifecycle phase."""
    primary: List[str] = field(default_factory=list)
    informed: List[str] = field(default_factory=list)


@dataclass
class PhaseArtifacts:
    """Artifacts produced in KDB and IDB."""
    kdb: List[str] = field(default_factory=list)
    idb: List[str] = field(default_factory=list)


@dataclass
class LifecyclePhaseDefinition:
    """
    Full definition of a lifecycle phase.
    
    Based on ARP4754A, ARP4761, and AS9100.
    """
    code: str
    name: str
    description: str
    objectives: List[str] = field(default_factory=list)
    artifacts: PhaseArtifacts = field(default_factory=PhaseArtifacts)
    gates: PhaseGate = field(default_factory=lambda: PhaseGate("", ""))
    baselines: PhaseBaselines = field(default_factory=PhaseBaselines)
    stakeholders: PhaseStakeholders = field(default_factory=PhaseStakeholders)
    duration_typical: str = ""
    
    @property
    def phase_enum(self) -> LifecyclePhase:
        """Get the enum value for this phase."""
        return LifecyclePhase(self.code)
    
    def is_development_phase(self) -> bool:
        """Check if this is a development phase (LC01-LC06)."""
        phase_num = int(self.code[2:])
        return 1 <= phase_num <= 6
    
    def is_operational_phase(self) -> bool:
        """Check if this is an operational phase (LC07-LC11)."""
        phase_num = int(self.code[2:])
        return 7 <= phase_num <= 11
    
    def is_end_of_life_phase(self) -> bool:
        """Check if this is an end-of-life phase (LC12-LC14)."""
        phase_num = int(self.code[2:])
        return 12 <= phase_num <= 14


@dataclass
class PhaseTransition:
    """Transition between lifecycle phases."""
    from_phase: str
    to_phase: str
    gate: str
    criteria: List[str] = field(default_factory=list)


@dataclass
class StakeholderDefinition:
    """Stakeholder definition."""
    code: str
    name: str
    description: str
    responsibilities: List[str] = field(default_factory=list)


@dataclass
class LifecycleModel:
    """
    Complete lifecycle model LC01-LC14.
    
    Provides phase definitions, transitions, and stakeholder information.
    """
    metadata: Dict[str, Any]
    phases: Dict[str, LifecyclePhaseDefinition] = field(default_factory=dict)
    transitions: List[PhaseTransition] = field(default_factory=list)
    stakeholders: Dict[str, StakeholderDefinition] = field(default_factory=dict)
    
    @classmethod
    def from_yaml(cls, yaml_path: Path) -> "LifecycleModel":
        """Load lifecycle model from YAML file."""
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        metadata = data.get("metadata", {})
        
        # Parse phases
        phases = {}
        for code, phase_data in data.get("phases", {}).items():
            artifacts_data = phase_data.get("artifacts", {})
            artifacts = PhaseArtifacts(
                kdb=artifacts_data.get("kdb", []),
                idb=artifacts_data.get("idb", [])
            )
            
            gates_data = phase_data.get("gates", {})
            gates = PhaseGate(
                entry=gates_data.get("entry", ""),
                exit=gates_data.get("exit", "")
            )
            
            baselines_data = phase_data.get("baselines", {})
            baselines = PhaseBaselines(
                established=baselines_data.get("established", []),
                consumed=baselines_data.get("consumed", [])
            )
            
            stakeholders_data = phase_data.get("stakeholders", {})
            stakeholders = PhaseStakeholders(
                primary=stakeholders_data.get("primary", []),
                informed=stakeholders_data.get("informed", [])
            )
            
            phases[code] = LifecyclePhaseDefinition(
                code=code,
                name=phase_data.get("name", ""),
                description=phase_data.get("description", ""),
                objectives=phase_data.get("objectives", []),
                artifacts=artifacts,
                gates=gates,
                baselines=baselines,
                stakeholders=stakeholders,
                duration_typical=phase_data.get("duration_typical", "")
            )
        
        # Parse transitions
        transitions = []
        for trans_data in data.get("transitions", []):
            transitions.append(PhaseTransition(
                from_phase=trans_data.get("from", ""),
                to_phase=trans_data.get("to", ""),
                gate=trans_data.get("gate", ""),
                criteria=trans_data.get("criteria", [])
            ))
        
        # Parse stakeholders
        stakeholders = {}
        for code, stk_data in data.get("stakeholders", {}).items():
            stakeholders[code] = StakeholderDefinition(
                code=code,
                name=stk_data.get("name", ""),
                description=stk_data.get("description", ""),
                responsibilities=stk_data.get("responsibilities", [])
            )
        
        return cls(
            metadata=metadata,
            phases=phases,
            transitions=transitions,
            stakeholders=stakeholders
        )
    
    def get_phase(self, code: str) -> Optional[LifecyclePhaseDefinition]:
        """Get phase by code (e.g., 'LC03')."""
        return self.phases.get(code)
    
    def get_phase_by_name(self, name: str) -> Optional[LifecyclePhaseDefinition]:
        """Get phase by name (e.g., 'Design')."""
        for phase in self.phases.values():
            if phase.name.lower() == name.lower():
                return phase
        return None
    
    def get_next_phase(self, current_code: str) -> Optional[LifecyclePhaseDefinition]:
        """Get the next phase in sequence."""
        for transition in self.transitions:
            if transition.from_phase == current_code:
                return self.get_phase(transition.to_phase)
        return None
    
    def get_transition(self, from_code: str, to_code: str) -> Optional[PhaseTransition]:
        """Get transition between two phases."""
        for transition in self.transitions:
            if transition.from_phase == from_code and transition.to_phase == to_code:
                return transition
        return None
    
    def get_stakeholder(self, code: str) -> Optional[StakeholderDefinition]:
        """Get stakeholder definition by code."""
        return self.stakeholders.get(code)
    
    def get_phases_for_baseline(self, baseline_type: str) -> List[LifecyclePhaseDefinition]:
        """Get phases that establish a given baseline type."""
        results = []
        for phase in self.phases.values():
            if baseline_type in phase.baselines.established:
                results.append(phase)
        return results
    
    def list_phases_in_order(self) -> List[LifecyclePhaseDefinition]:
        """List all phases in order (LC01-LC14)."""
        return [
            self.phases[f"LC{str(i).zfill(2)}"]
            for i in range(1, 15)
            if f"LC{str(i).zfill(2)}" in self.phases
        ]


# =============================================================================
# NAMING CONVENTIONS AND ID VALIDATION
# =============================================================================


@dataclass
class IDPattern:
    """ID pattern definition for validation."""
    name: str
    pattern: str
    description: str
    examples: List[str] = field(default_factory=list)
    
    @property
    def compiled_pattern(self) -> Pattern:
        """Get compiled regex pattern."""
        return re.compile(self.pattern)
    
    def validate(self, value: str) -> bool:
        """Validate a value against this pattern."""
        return bool(self.compiled_pattern.match(value))


class NamingConventions:
    """
    Naming conventions and ID grammar for ASIT-ASIGT.
    
    Provides validation and generation of standardized identifiers.
    """
    
    # Pre-defined patterns
    PATTERNS = {
        "baseline_id": IDPattern(
            name="Baseline ID",
            pattern=r"^(FBL|ABL|PBL|OBL)-\d{4}-Q[1-4]-\d{3}$",
            description="Baseline identifier: <TYPE>-<YEAR>-<QUARTER>-<SEQUENCE>",
            examples=["FBL-2026-Q1-001", "ABL-2026-Q2-003"]
        ),
        "ecr_id": IDPattern(
            name="ECR ID",
            pattern=r"^ECR-\d{4}-\d{4}$",
            description="Engineering Change Request: ECR-<YEAR>-<SEQUENCE>",
            examples=["ECR-2026-0042"]
        ),
        "eco_id": IDPattern(
            name="ECO ID",
            pattern=r"^ECO-\d{4}-\d{4}$",
            description="Engineering Change Order: ECO-<YEAR>-<SEQUENCE>",
            examples=["ECO-2026-0035"]
        ),
        "ccb_id": IDPattern(
            name="CCB ID",
            pattern=r"^CCB-\d{4}-\d{4}$",
            description="Configuration Control Board: CCB-<YEAR>-<SEQUENCE>",
            examples=["CCB-2026-0012"]
        ),
        "contract_id": IDPattern(
            name="Contract ID",
            pattern=r"^[A-Z0-9]+-CTR-[A-Z]+-[A-Z0-9]+(-[A-Za-z0-9_]+)?(-v\d+\.\d+\.\d+)?$",
            description="Contract: <PREFIX>-CTR-<CATEGORY>-<TARGET>[-<SCOPE>][-<VERSION>]",
            examples=["KITDM-CTR-LM-CSDB", "KITDM-CTR-LM-CSDB_ATA28-v1.2.0"]
        ),
        "version": IDPattern(
            name="Version",
            pattern=r"^v\d+\.\d+\.\d+$",
            description="Semantic version: v<MAJOR>.<MINOR>.<PATCH>",
            examples=["v1.0.0", "v2.1.3"]
        ),
        "dmc": IDPattern(
            name="Data Module Code",
            pattern=r"^[A-Z0-9]{2,14}-[A-Z0-9]{1,4}-\d{2,3}-\d{1,2}-\d{1,2}-\d{2}[A-Z]?-\d{3}[A-Z]-[A-Z]$",
            description="S1000D Data Module Code per Issue 5.0",
            examples=["HJ1-A-28-10-00-00A-040A-A"]
        ),
        "pmc": IDPattern(
            name="Publication Module Code",
            pattern=r"^[A-Z0-9]+-\d{5}-\d{3}-[A-Z]{2}$",
            description="Publication Module Code: <MODEL>-<PMIC>-<ISSUE>-<LANGUAGE>",
            examples=["HJ1-00001-001-EN"]
        ),
        "icn": IDPattern(
            name="Information Control Number",
            pattern=r"^ICN-[A-Z0-9]+-[A-Z]{2}-\d{5}-[A-Z]-\d{3}$",
            description="ICN: ICN-<MODEL>-<TYPE>-<SEQUENCE>-<VARIANT>-<ISSUE>",
            examples=["ICN-HJ1-SH-00001-A-001"]
        ),
        "run_id": IDPattern(
            name="Run ID",
            pattern=r"^\d{8}-\d{4}__[A-Z0-9]+-CTR-[A-Z]+-[A-Z0-9]+.*$",
            description="Run ID: <YYYYMMDD>-<HHMM>__<CONTRACT-ID>",
            examples=["20260122-1430__KITDM-CTR-LM-CSDB_ATA28"]
        ),
        "kdb_artifact": IDPattern(
            name="KDB Artifact ID",
            pattern=r"^KDB-(REQ|DSN|ANA|TST|CERT)-[A-Z]{2,4}-\d{4}$",
            description="KDB Artifact: KDB-<CATEGORY>-<TYPE>-<SEQUENCE>",
            examples=["KDB-REQ-SYS-0001", "KDB-DSN-SCH-0042"]
        ),
        "stakeholder": IDPattern(
            name="Stakeholder Code",
            pattern=r"^STK_(ENG|CERT|CM|QA|MFG|OPS|MRO|BUS)$",
            description="Stakeholder code: STK_<ROLE>",
            examples=["STK_ENG", "STK_CERT"]
        ),
        "lifecycle_phase": IDPattern(
            name="Lifecycle Phase",
            pattern=r"^LC(0[1-9]|1[0-4])$",
            description="Lifecycle phase: LC01-LC14",
            examples=["LC01", "LC06", "LC14"]
        ),
        "ata_chapter": IDPattern(
            name="ATA Chapter",
            pattern=r"^\d{2}$",
            description="ATA chapter: 2-digit code",
            examples=["28", "32", "72"]
        ),
        "ata_section": IDPattern(
            name="ATA Section",
            pattern=r"^\d{2}-\d{2}$",
            description="ATA section: <CHAPTER>-<SECTION>",
            examples=["28-10", "32-40"]
        ),
    }
    
    def __init__(self, custom_patterns: Optional[Dict[str, IDPattern]] = None):
        """
        Initialize naming conventions.
        
        Args:
            custom_patterns: Additional custom patterns to register
        """
        self.patterns = dict(self.PATTERNS)
        if custom_patterns:
            self.patterns.update(custom_patterns)
    
    def validate(self, pattern_name: str, value: str) -> bool:
        """
        Validate a value against a named pattern.
        
        Args:
            pattern_name: Name of the pattern to use
            value: Value to validate
            
        Returns:
            True if valid, False otherwise
            
        Raises:
            NamingConventionError: If pattern name is unknown
        """
        if pattern_name not in self.patterns:
            raise NamingConventionError(f"Unknown pattern: {pattern_name}")
        return self.patterns[pattern_name].validate(value)
    
    def validate_strict(self, pattern_name: str, value: str) -> None:
        """
        Validate a value, raising exception on failure.
        
        Args:
            pattern_name: Name of the pattern to use
            value: Value to validate
            
        Raises:
            IDValidationError: If validation fails
        """
        if not self.validate(pattern_name, value):
            pattern = self.patterns.get(pattern_name)
            raise IDValidationError(
                f"Invalid {pattern.name if pattern else pattern_name}: '{value}'. "
                f"Expected format: {pattern.description if pattern else 'unknown'}"
            )
    
    def get_pattern(self, pattern_name: str) -> Optional[IDPattern]:
        """Get pattern by name."""
        return self.patterns.get(pattern_name)
    
    def list_patterns(self) -> List[str]:
        """List all available pattern names."""
        return list(self.patterns.keys())
    
    # =========================================================================
    # ID Generation Methods
    # =========================================================================
    
    def generate_baseline_id(
        self,
        baseline_type: BaselineTypeCode,
        year: int,
        quarter: int,
        sequence: int
    ) -> str:
        """
        Generate a baseline ID.
        
        Args:
            baseline_type: Type of baseline (FBL, ABL, PBL, OBL)
            year: 4-digit year
            quarter: Quarter (1-4)
            sequence: Sequence number (1-999)
            
        Returns:
            Formatted baseline ID
        """
        if not 1 <= quarter <= 4:
            raise NamingConventionError(f"Invalid quarter: {quarter}")
        if not 1 <= sequence <= 999:
            raise NamingConventionError(f"Invalid sequence: {sequence}")
        
        return f"{baseline_type.value}-{year}-Q{quarter}-{sequence:03d}"
    
    def generate_ecr_id(self, year: int, sequence: int) -> str:
        """Generate an ECR ID."""
        if not 1 <= sequence <= 9999:
            raise NamingConventionError(f"Invalid sequence: {sequence}")
        return f"ECR-{year}-{sequence:04d}"
    
    def generate_eco_id(self, year: int, sequence: int) -> str:
        """Generate an ECO ID."""
        if not 1 <= sequence <= 9999:
            raise NamingConventionError(f"Invalid sequence: {sequence}")
        return f"ECO-{year}-{sequence:04d}"
    
    def generate_ccb_id(self, year: int, sequence: int) -> str:
        """Generate a CCB decision ID."""
        if not 1 <= sequence <= 9999:
            raise NamingConventionError(f"Invalid sequence: {sequence}")
        return f"CCB-{year}-{sequence:04d}"
    
    def generate_contract_id(
        self,
        prefix: str,
        category: ContractCategoryCode,
        target: str,
        scope: Optional[str] = None,
        version: Optional[str] = None
    ) -> str:
        """
        Generate a contract ID.
        
        Args:
            prefix: Program/project prefix (e.g., 'KITDM')
            category: Contract category
            target: Target publication/output (e.g., 'CSDB')
            scope: Optional scope qualifier (e.g., 'ATA28')
            version: Optional version string (e.g., 'v1.2.0')
            
        Returns:
            Formatted contract ID
        """
        contract_id = f"{prefix}-CTR-{category.value}-{target}"
        if scope:
            contract_id += f"_{scope}"
        if version:
            if not version.startswith("v"):
                version = f"v{version}"
            contract_id += f"-{version}"
        return contract_id
    
    def generate_icn(
        self,
        model: str,
        graphic_type: GraphicType,
        sequence: int,
        variant: str = "A",
        issue: int = 1
    ) -> str:
        """
        Generate an Information Control Number.
        
        Args:
            model: Model code (e.g., 'HJ1')
            graphic_type: Type of graphic
            sequence: 5-digit sequence number
            variant: Variant letter (A-Z)
            issue: Issue number (1-999)
            
        Returns:
            Formatted ICN
        """
        if not 1 <= sequence <= 99999:
            raise NamingConventionError(f"Invalid sequence: {sequence}")
        if not 1 <= issue <= 999:
            raise NamingConventionError(f"Invalid issue: {issue}")
        
        return f"ICN-{model}-{graphic_type.value}-{sequence:05d}-{variant}-{issue:03d}"
    
    def generate_run_id(self, contract_id: str, timestamp: Optional[datetime] = None) -> str:
        """
        Generate a run/execution ID.
        
        Args:
            contract_id: Contract ID
            timestamp: Optional timestamp (defaults to now)
            
        Returns:
            Formatted run ID
        """
        if timestamp is None:
            timestamp = datetime.now()
        date_str = timestamp.strftime("%Y%m%d")
        time_str = timestamp.strftime("%H%M")
        return f"{date_str}-{time_str}__{contract_id}"
    
    def generate_kdb_artifact_id(
        self,
        category: KDBCategory,
        artifact_type: str,
        sequence: int
    ) -> str:
        """
        Generate a KDB artifact ID.
        
        Args:
            category: KDB category (REQUIREMENTS, DESIGN, etc.)
            artifact_type: 2-4 character type code (e.g., 'SYS', 'SCH')
            sequence: Sequence number (1-9999)
            
        Returns:
            Formatted KDB artifact ID
        """
        # Map category to short code
        category_codes = {
            KDBCategory.REQUIREMENTS: "REQ",
            KDBCategory.DESIGN: "DSN",
            KDBCategory.ANALYSIS: "ANA",
            KDBCategory.TEST: "TST",
            KDBCategory.CERTIFICATION: "CERT",
        }
        
        cat_code = category_codes.get(category, "UNK")
        return f"KDB-{cat_code}-{artifact_type.upper()}-{sequence:04d}"
    
    def generate_version(self, major: int, minor: int, patch: int) -> str:
        """Generate a semantic version string."""
        return f"v{major}.{minor}.{patch}"
    
    def parse_baseline_id(self, baseline_id: str) -> Dict[str, Any]:
        """
        Parse a baseline ID into components.
        
        Args:
            baseline_id: Baseline ID to parse
            
        Returns:
            Dictionary with type, year, quarter, sequence
            
        Raises:
            IDValidationError: If ID is invalid
        """
        self.validate_strict("baseline_id", baseline_id)
        parts = baseline_id.split("-")
        return {
            "type": parts[0],
            "year": int(parts[1]),
            "quarter": int(parts[2][1]),
            "sequence": int(parts[3])
        }
    
    def parse_contract_id(self, contract_id: str) -> Dict[str, Any]:
        """
        Parse a contract ID into components.
        
        Args:
            contract_id: Contract ID to parse
            
        Returns:
            Dictionary with prefix, category, target, scope, version
        """
        result = {
            "prefix": "",
            "category": "",
            "target": "",
            "scope": None,
            "version": None
        }
        
        # Check for version suffix
        version_match = re.search(r"-v(\d+\.\d+\.\d+)$", contract_id)
        if version_match:
            result["version"] = version_match.group(1)
            contract_id = contract_id[:version_match.start()]
        
        # Split main parts
        parts = contract_id.split("-CTR-")
        if len(parts) != 2:
            raise IDValidationError(f"Invalid contract ID format: {contract_id}")
        
        result["prefix"] = parts[0]
        
        # Parse category and target
        remaining = parts[1]
        if "_" in remaining:
            # Has scope
            cat_target, scope = remaining.rsplit("_", 1)
            result["scope"] = scope
        else:
            cat_target = remaining
        
        cat_parts = cat_target.split("-", 1)
        result["category"] = cat_parts[0]
        result["target"] = cat_parts[1] if len(cat_parts) > 1 else ""
        
        return result
    
    def parse_dmc(self, dmc: str) -> Dict[str, str]:
        """
        Parse a Data Module Code into components.
        
        Note: This is a simplified parser. Full S1000D DMC parsing
        requires additional context for proper component extraction.
        
        Args:
            dmc: Data Module Code
            
        Returns:
            Dictionary with DMC components
        """
        # Basic validation
        parts = dmc.split("-")
        if len(parts) < 8:
            raise IDValidationError(f"Invalid DMC format: {dmc}")
        
        return {
            "model_ident_code": parts[0],
            "system_diff_code": parts[1],
            "system_code": parts[2],
            "sub_system_code": parts[3],
            "sub_sub_system_code": parts[4],
            "assy_code": parts[5],
            "info_code": parts[6],
            "item_location_code": parts[7] if len(parts) > 7 else "A"
        }


# =============================================================================
# KDB/IDB PARTITION
# =============================================================================


@dataclass
class ContentMapping:
    """Mapping from KDB source to IDB target."""
    source_type: str
    source_location: str
    target_type: str
    target_location: str
    mapping_rules: str
    description: str = ""


@dataclass
class PartitionRule:
    """Rule for KDB/IDB partitioning."""
    rule_id: str
    name: str
    description: str
    enforcement: str  # REQUIRED, RECOMMENDED, OPTIONAL


class KDBIDBPartition:
    """
    KDB/IDB partitioning rules and enforcement.
    
    Ensures proper separation between engineering knowledge (KDB)
    and operational information (IDB).
    """
    
    # Standard content mappings
    CONTENT_MAPPINGS = [
        ContentMapping(
            source_type="REQUIREMENT",
            source_location="KDB/REQUIREMENTS/",
            target_type="DM_DESCRIPTIVE",
            target_location="IDB/CSDB/",
            mapping_rules="mapping/requirement_to_dm.yaml",
            description="System requirements to descriptive Data Modules"
        ),
        ContentMapping(
            source_type="TASK",
            source_location="KDB/TASKS/",
            target_type="DM_PROCEDURAL",
            target_location="IDB/CSDB/",
            mapping_rules="mapping/task_to_dm.yaml",
            description="Maintenance tasks to procedural Data Modules"
        ),
        ContentMapping(
            source_type="REPAIR",
            source_location="KDB/REPAIRS/",
            target_type="DM_REPAIR",
            target_location="IDB/CSDB/",
            mapping_rules="mapping/repair_to_dm.yaml",
            description="Repair data to SRM Data Modules"
        ),
        ContentMapping(
            source_type="PART",
            source_location="KDB/PARTS/",
            target_type="DM_IPD",
            target_location="IDB/CSDB/",
            mapping_rules="mapping/parts_to_ipd.yaml",
            description="Parts data to Illustrated Parts Data Modules"
        ),
    ]
    
    # Partition rules
    PARTITION_RULES = [
        PartitionRule(
            rule_id="PR-001",
            name="No Direct IDB Authoring",
            description="All IDB content must be generated via ASIGT from KDB sources",
            enforcement="REQUIRED"
        ),
        PartitionRule(
            rule_id="PR-002",
            name="Mandatory Traceability",
            description="Every IDB artifact must trace to KDB source, contract, and baseline",
            enforcement="REQUIRED"
        ),
        PartitionRule(
            rule_id="PR-003",
            name="KDB Primacy",
            description="When discrepancy exists, KDB is authoritative; IDB must regenerate",
            enforcement="REQUIRED"
        ),
        PartitionRule(
            rule_id="PR-004",
            name="Bidirectional Awareness",
            description="IDB feedback triggers ECR/ECO process, never direct KDB modification",
            enforcement="REQUIRED"
        ),
    ]
    
    def __init__(self, asit_root: Path):
        """
        Initialize KDB/IDB partition manager.
        
        Args:
            asit_root: Path to ASIT root directory
        """
        self.asit_root = asit_root
        self.content_mappings = list(self.CONTENT_MAPPINGS)
        self.partition_rules = list(self.PARTITION_RULES)
    
    def get_mapping_for_source(self, source_type: str) -> Optional[ContentMapping]:
        """Get mapping configuration for a source type."""
        for mapping in self.content_mappings:
            if mapping.source_type == source_type:
                return mapping
        return None
    
    def get_target_location(self, source_type: str) -> Optional[str]:
        """Get IDB target location for a KDB source type."""
        mapping = self.get_mapping_for_source(source_type)
        return mapping.target_location if mapping else None
    
    def get_mapping_rules_path(self, source_type: str) -> Optional[Path]:
        """Get path to mapping rules file for a source type."""
        mapping = self.get_mapping_for_source(source_type)
        if mapping:
            return self.asit_root.parent / "ASIGT" / mapping.mapping_rules
        return None
    
    def validate_kdb_path(self, path: Path) -> bool:
        """Validate that a path is within KDB structure."""
        path_str = str(path)
        return "KDB/" in path_str or "KDB\\" in path_str
    
    def validate_idb_path(self, path: Path) -> bool:
        """Validate that a path is within IDB structure."""
        path_str = str(path)
        return "IDB/" in path_str or "IDB\\" in path_str
    
    def get_database_type(self, path: Path) -> Optional[DatabaseType]:
        """Determine database type from path."""
        if self.validate_kdb_path(path):
            return DatabaseType.KDB
        elif self.validate_idb_path(path):
            return DatabaseType.IDB
        return None
    
    def list_mappings(self) -> List[ContentMapping]:
        """List all content mappings."""
        return self.content_mappings
    
    def list_rules(self) -> List[PartitionRule]:
        """List all partition rules."""
        return self.partition_rules
    
    def get_required_rules(self) -> List[PartitionRule]:
        """Get only required partition rules."""
        return [r for r in self.partition_rules if r.enforcement == "REQUIRED"]


# =============================================================================
# STRUCTURE MANAGER
# =============================================================================


class StructureManager:
    """
    Main structure manager for ASIT.
    
    Provides unified access to:
    - ATA mapping
    - Lifecycle phases
    - Naming conventions
    - KDB/IDB partitioning
    """
    
    def __init__(self, asit_root: Path):
        """
        Initialize the structure manager.
        
        Args:
            asit_root: Path to ASIT root directory
        """
        self.asit_root = asit_root
        self.structure_path = asit_root / "STRUCTURE"
        
        # Lazy-loaded components
        self._ata_mapping: Optional[ATAMapping] = None
        self._lifecycle_model: Optional[LifecycleModel] = None
        self._naming: Optional[NamingConventions] = None
        self._partition: Optional[KDBIDBPartition] = None
    
    @property
    def ata_mapping(self) -> ATAMapping:
        """Lazy-load ATA mapping."""
        if self._ata_mapping is None:
            yaml_path = self.structure_path / "ATA_MAPPING.yaml"
            if yaml_path.exists():
                self._ata_mapping = ATAMapping.from_yaml(yaml_path)
            else:
                logger.warning(f"ATA_MAPPING.yaml not found at {yaml_path}")
                self._ata_mapping = ATAMapping(metadata={}, chapters={})
        return self._ata_mapping
    
    @property
    def lifecycle(self) -> LifecycleModel:
        """Lazy-load lifecycle model."""
        if self._lifecycle_model is None:
            yaml_path = self.structure_path / "LIFECYCLE_PHASES.yaml"
            if yaml_path.exists():
                self._lifecycle_model = LifecycleModel.from_yaml(yaml_path)
            else:
                logger.warning(f"LIFECYCLE_PHASES.yaml not found at {yaml_path}")
                self._lifecycle_model = LifecycleModel(metadata={})
        return self._lifecycle_model
    
    @property
    def naming(self) -> NamingConventions:
        """Get naming conventions."""
        if self._naming is None:
            self._naming = NamingConventions()
        return self._naming
    
    @property
    def partition(self) -> KDBIDBPartition:
        """Get KDB/IDB partition manager."""
        if self._partition is None:
            self._partition = KDBIDBPartition(self.asit_root)
        return self._partition
    
    # =========================================================================
    # Convenience Methods
    # =========================================================================
    
    def get_ata_chapter(self, code: str) -> Optional[ATAChapter]:
        """Get ATA chapter by code."""
        return self.ata_mapping.get_chapter(code)
    
    def get_lifecycle_phase(self, code: str) -> Optional[LifecyclePhaseDefinition]:
        """Get lifecycle phase by code."""
        return self.lifecycle.get_phase(code)
    
    def validate_id(self, pattern_name: str, value: str) -> bool:
        """Validate an ID against a pattern."""
        return self.naming.validate(pattern_name, value)
    
    def get_content_mapping(self, source_type: str) -> Optional[ContentMapping]:
        """Get content mapping for a source type."""
        return self.partition.get_mapping_for_source(source_type)
    
    def get_system_code_for_ata(
        self, 
        chapter: str, 
        subsystem: str = "00", 
        sub_subsystem: str = "00"
    ) -> str:
        """Convert ATA chapter to S1000D system code."""
        return self.ata_mapping.get_system_code(chapter, subsystem, sub_subsystem)
    
    def get_stakeholder(self, code: str) -> Optional[StakeholderDefinition]:
        """Get stakeholder definition."""
        return self.lifecycle.get_stakeholder(code)
    
    def search_ata_chapters(self, query: str) -> List[ATAChapter]:
        """Search ATA chapters by title or description."""
        return self.ata_mapping.search_chapters(query)
    
    def get_phases_by_stage(self, stage: str) -> List[LifecyclePhaseDefinition]:
        """
        Get phases by development stage.
        
        Args:
            stage: One of 'development', 'operational', 'end_of_life'
            
        Returns:
            List of phases in that stage
        """
        all_phases = self.lifecycle.list_phases_in_order()
        
        if stage == "development":
            return [p for p in all_phases if p.is_development_phase()]
        elif stage == "operational":
            return [p for p in all_phases if p.is_operational_phase()]
        elif stage == "end_of_life":
            return [p for p in all_phases if p.is_end_of_life_phase()]
        else:
            return all_phases


# =============================================================================
# MODULE EXPORTS
# =============================================================================


__all__ = [
    # Exceptions
    "StructureError",
    "ATAMappingError",
    "LifecyclePhaseError",
    "NamingConventionError",
    "IDValidationError",
    "PartitionError",
    
    # Enumerations
    "DatabaseType",
    "KDBCategory",
    "IDBCategory",
    "LifecyclePhase",
    "StakeholderCode",
    "BaselineTypeCode",
    "ContractCategoryCode",
    "GraphicType",
    "InformationCode",
    
    # ATA Mapping
    "ATASection",
    "ATAChapter",
    "ATAMapping",
    
    # Lifecycle
    "PhaseGate",
    "PhaseBaselines",
    "PhaseStakeholders",
    "PhaseArtifacts",
    "LifecyclePhaseDefinition",
    "PhaseTransition",
    "StakeholderDefinition",
    "LifecycleModel",
    
    # Naming Conventions
    "IDPattern",
    "NamingConventions",
    
    # KDB/IDB Partition
    "ContentMapping",
    "PartitionRule",
    "KDBIDBPartition",
    
    # Main Manager
    "StructureManager",
]
