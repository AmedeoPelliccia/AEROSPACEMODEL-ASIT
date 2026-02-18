"""
AMPEL360 Q100 Identifier Grammar Module

This module implements the canonical identifier grammar for AMPEL360 Q100
artifacts per CV-003 specification.

Grammar:
    AMPEL360-Q100-MSN{nnn}-ATA{cc}-{ss}-{ss}-LC{nn}-{Type}-{Seq}

Formats:
    - Compact: AMPEL360_Q100_MSN001_ATA25-10-00_LC02_REQ_001
    - URN:     urn:ampel360:q100:msn001:ata25-10-00:lc02:req:001

Author: ASIT (Aircraft Systems Information Transponder)
Document: AMPEL360-CV-003 v3.0
Date: 2026-02-18
"""

import re
from dataclasses import dataclass
from typing import Optional, Tuple
from enum import Enum


class IDFormat(Enum):
    """Identifier format options."""
    COMPACT = "compact"  # AMPEL360_Q100_MSN001_ATA25-10-00_LC02_REQ_001
    HYPHENATED = "hyphenated"  # AMPEL360-Q100-MSN001-ATA25-10-00-LC02-REQ-001
    URN = "urn"  # urn:ampel360:q100:msn001:ata25-10-00:lc02:req:001


class PhaseType(Enum):
    """Lifecycle phase type."""
    PLM = "PLM"  # Product Lifecycle Management (LC01-LC10)
    OPS = "OPS"  # Operations (LC11-LC14)


@dataclass
class ArtifactID:
    """
    AMPEL360 Q100 Artifact Identifier.
    
    Represents a canonical artifact identifier with all components
    per CV-003 specification.
    """
    aircraft_id: str = "AMPEL360"
    model_id: str = "Q100"
    msn: str = ""  # MSN001, MSN042, etc.
    ata_chapter: str = ""  # 00-98 or IN
    section: str = "00"  # 00-99
    subject: str = "00"  # 00-99
    lc_phase: str = ""  # LC01-LC14
    artifact_type: str = ""  # REQ, DES, SAF, etc.
    sequence: str = "001"  # 001-999
    
    def __post_init__(self):
        """Validate identifier components after initialization."""
        self._validate()
    
    def _validate(self):
        """Validate all identifier components."""
        # Aircraft and model are constants
        if self.aircraft_id != "AMPEL360":
            raise ValueError(f"Invalid aircraft_id: {self.aircraft_id}. Must be 'AMPEL360'")
        if self.model_id != "Q100":
            raise ValueError(f"Invalid model_id: {self.model_id}. Must be 'Q100'")
        
        # MSN validation
        if not re.match(r'^MSN\d{3}$', self.msn):
            raise ValueError(f"Invalid MSN: {self.msn}. Must be MSNnnn (e.g., MSN001)")
        
        # ATA chapter validation
        if not re.match(r'^(\d{2}|IN)$', self.ata_chapter):
            raise ValueError(f"Invalid ATA chapter: {self.ata_chapter}. Must be 00-98 or IN")
        
        # Section and subject validation
        if not re.match(r'^\d{2}$', self.section):
            raise ValueError(f"Invalid section: {self.section}. Must be 00-99")
        if not re.match(r'^\d{2}$', self.subject):
            raise ValueError(f"Invalid subject: {self.subject}. Must be 00-99")
        
        # LC phase validation
        if not re.match(r'^LC(0[1-9]|1[0-4])$', self.lc_phase):
            raise ValueError(f"Invalid LC phase: {self.lc_phase}. Must be LC01-LC14")
        
        # Artifact type validation (alphanumeric with hyphens)
        if not re.match(r'^[A-Z0-9\-]+$', self.artifact_type):
            raise ValueError(f"Invalid artifact type: {self.artifact_type}")
        
        # Sequence validation (001-999)
        if not re.match(r'^\d{3}$', self.sequence):
            raise ValueError(f"Invalid sequence: {self.sequence}. Must be 001-999")
        seq_int = int(self.sequence)
        if not 1 <= seq_int <= 999:
            raise ValueError(f"Invalid sequence: {self.sequence}. Must be 001-999")
    
    def to_compact(self) -> str:
        """
        Generate compact form identifier.
        
        Returns:
            AMPEL360_Q100_MSN001_ATA25-10-00_LC02_REQ_001
        """
        return (f"{self.aircraft_id}_{self.model_id}_{self.msn}_"
                f"ATA{self.ata_chapter}-{self.section}-{self.subject}_"
                f"{self.lc_phase}_{self.artifact_type}_{self.sequence}")
    
    def to_hyphenated(self) -> str:
        """
        Generate hyphenated form identifier.
        
        Returns:
            AMPEL360-Q100-MSN001-ATA25-10-00-LC02-REQ-001
        """
        return (f"{self.aircraft_id}-{self.model_id}-{self.msn}-"
                f"ATA{self.ata_chapter}-{self.section}-{self.subject}-"
                f"{self.lc_phase}-{self.artifact_type}-{self.sequence}")
    
    def to_urn(self) -> str:
        """
        Generate URN form identifier.
        
        Returns:
            urn:ampel360:q100:msn001:ata25-10-00:lc02:req:001
        """
        return (f"urn:ampel360:q100:{self.msn.lower()}:"
                f"ata{self.ata_chapter.lower()}-{self.section}-{self.subject}:"
                f"{self.lc_phase.lower()}:{self.artifact_type.lower()}:{self.sequence}")
    
    def to_string(self, format: IDFormat = IDFormat.COMPACT) -> str:
        """
        Generate identifier in specified format.
        
        Args:
            format: Desired output format
            
        Returns:
            Formatted identifier string
        """
        if format == IDFormat.COMPACT:
            return self.to_compact()
        elif format == IDFormat.HYPHENATED:
            return self.to_hyphenated()
        elif format == IDFormat.URN:
            return self.to_urn()
        else:
            raise ValueError(f"Unknown format: {format}")
    
    def __str__(self) -> str:
        """Default string representation (compact form)."""
        return self.to_compact()
    
    def get_phase_type(self) -> PhaseType:
        """
        Determine if this is a PLM or OPS phase artifact.
        
        Returns:
            PhaseType.PLM for LC01-LC10, PhaseType.OPS for LC11-LC14
        """
        phase_num = int(self.lc_phase[2:])
        return PhaseType.PLM if phase_num <= 10 else PhaseType.OPS
    
    def get_ssot_root(self) -> str:
        """
        Get SSOT root directory based on phase type.
        
        Returns:
            'KDB/LM/SSOT/PLM' for PLM phases, 'IDB/OPS/LM' for OPS phases
        """
        return "KDB/LM/SSOT/PLM" if self.get_phase_type() == PhaseType.PLM else "IDB/OPS/LM"
    
    def get_ata_path_component(self) -> str:
        """
        Get ATA path component for directory structure.
        
        Returns:
            'ATA{cc}-{ss}-{ss}' format for path building
        """
        return f"ATA{self.ata_chapter}-{self.section}-{self.subject}"


class IDParser:
    """Parse AMPEL360 Q100 identifiers from various formats."""
    
    # Regex patterns for different formats
    COMPACT_PATTERN = re.compile(
        r'^AMPEL360_Q100_(MSN\d{3})_ATA(\d{2}|IN)-(\d{2})-(\d{2})_'
        r'(LC(?:0[1-9]|1[0-4]))_([A-Z0-9\-]+)_(\d{3})$'
    )
    
    HYPHENATED_PATTERN = re.compile(
        r'^AMPEL360-Q100-(MSN\d{3})-ATA(\d{2}|IN)-(\d{2})-(\d{2})-'
        r'(LC(?:0[1-9]|1[0-4]))-([A-Z0-9\-]+)-(\d{3})$'
    )
    
    URN_PATTERN = re.compile(
        r'^urn:ampel360:q100:(msn\d{3}):ata(\d{2}|in)-(\d{2})-(\d{2}):'
        r'(lc(?:0[1-9]|1[0-4])):([a-z0-9\-]+):(\d{3})$'
    )
    
    @classmethod
    def parse(cls, identifier: str) -> Optional[ArtifactID]:
        """
        Parse an identifier string into an ArtifactID object.
        
        Args:
            identifier: Identifier string in any supported format
            
        Returns:
            ArtifactID object if parsing successful, None otherwise
        """
        # Try compact format
        match = cls.COMPACT_PATTERN.match(identifier)
        if match:
            msn, ata, section, subject, lc, atype, seq = match.groups()
            return ArtifactID(
                msn=msn,
                ata_chapter=ata,
                section=section,
                subject=subject,
                lc_phase=lc,
                artifact_type=atype,
                sequence=seq
            )
        
        # Try hyphenated format
        match = cls.HYPHENATED_PATTERN.match(identifier)
        if match:
            msn, ata, section, subject, lc, atype, seq = match.groups()
            return ArtifactID(
                msn=msn,
                ata_chapter=ata,
                section=section,
                subject=subject,
                lc_phase=lc,
                artifact_type=atype,
                sequence=seq
            )
        
        # Try URN format
        match = cls.URN_PATTERN.match(identifier)
        if match:
            msn, ata, section, subject, lc, atype, seq = match.groups()
            return ArtifactID(
                msn=msn.upper(),
                ata_chapter=ata.upper() if ata != "in" else "IN",
                section=section,
                subject=subject,
                lc_phase=lc.upper(),
                artifact_type=atype.upper(),
                sequence=seq
            )
        
        return None
    
    @classmethod
    def validate(cls, identifier: str) -> Tuple[bool, Optional[str]]:
        """
        Validate an identifier string.
        
        Args:
            identifier: Identifier string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            parsed = cls.parse(identifier)
            if parsed is None:
                return False, "Identifier does not match any supported format"
            return True, None
        except ValueError as e:
            return False, str(e)


class IDGenerator:
    """Generate AMPEL360 Q100 identifiers with auto-sequencing."""
    
    def __init__(self):
        """Initialize the ID generator."""
        self._sequence_counters = {}
    
    def _get_base_key(self, msn: str, ata_chapter: str, section: str, 
                      subject: str, lc_phase: str, artifact_type: str) -> str:
        """Generate a key for sequence tracking."""
        return f"{msn}:{ata_chapter}-{section}-{subject}:{lc_phase}:{artifact_type}"
    
    def generate(self, msn: str, ata_chapter: str, section: str, subject: str,
                 lc_phase: str, artifact_type: str, 
                 sequence: Optional[int] = None) -> ArtifactID:
        """
        Generate a new artifact ID with optional auto-sequencing.
        
        Args:
            msn: Manufacturer Serial Number (MSN001, MSN042, etc.)
            ata_chapter: ATA chapter (00-98 or IN)
            section: Section code (00-99)
            subject: Subject code (00-99)
            lc_phase: Lifecycle phase (LC01-LC14)
            artifact_type: Artifact type code (REQ, DES, etc.)
            sequence: Optional explicit sequence number (1-999)
            
        Returns:
            New ArtifactID object
        """
        if sequence is None:
            # Auto-sequence
            base_key = self._get_base_key(msn, ata_chapter, section, subject, 
                                          lc_phase, artifact_type)
            if base_key not in self._sequence_counters:
                self._sequence_counters[base_key] = 0
            self._sequence_counters[base_key] += 1
            sequence = self._sequence_counters[base_key]
        
        if not (1 <= sequence <= 999):
            raise ValueError(f"Sequence must be 1-999, got {sequence}")
        
        return ArtifactID(
            msn=msn,
            ata_chapter=ata_chapter,
            section=section,
            subject=subject,
            lc_phase=lc_phase,
            artifact_type=artifact_type,
            sequence=f"{sequence:03d}"
        )
    
    def reset_sequence(self, msn: str, ata_chapter: str, section: str, 
                       subject: str, lc_phase: str, artifact_type: str):
        """Reset sequence counter for a specific artifact series."""
        base_key = self._get_base_key(msn, ata_chapter, section, subject, 
                                      lc_phase, artifact_type)
        if base_key in self._sequence_counters:
            del self._sequence_counters[base_key]


# Convenience functions

def parse_identifier(identifier: str) -> Optional[ArtifactID]:
    """
    Parse an identifier string.
    
    Args:
        identifier: Identifier in any supported format
        
    Returns:
        ArtifactID object or None if parsing fails
    """
    return IDParser.parse(identifier)


def validate_identifier(identifier: str) -> Tuple[bool, Optional[str]]:
    """
    Validate an identifier string.
    
    Args:
        identifier: Identifier to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    return IDParser.validate(identifier)


def create_identifier(msn: str, ata_chapter: str, section: str, subject: str,
                      lc_phase: str, artifact_type: str, sequence: int = 1,
                      format: IDFormat = IDFormat.COMPACT) -> str:
    """
    Create a new identifier in the specified format.
    
    Args:
        msn: Manufacturer Serial Number
        ata_chapter: ATA chapter code
        section: Section code
        subject: Subject code
        lc_phase: Lifecycle phase
        artifact_type: Artifact type code
        sequence: Sequence number (default: 1)
        format: Output format (default: COMPACT)
        
    Returns:
        Formatted identifier string
    """
    artifact_id = ArtifactID(
        msn=msn,
        ata_chapter=ata_chapter,
        section=section,
        subject=subject,
        lc_phase=lc_phase,
        artifact_type=artifact_type,
        sequence=f"{sequence:03d}"
    )
    return artifact_id.to_string(format)
