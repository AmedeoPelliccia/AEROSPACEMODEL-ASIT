"""
Functional Layers Module

Implements the functional layers of the AEROSPACEMODEL 3D mesh
architecture:
- ATM/CNS layer (air traffic management, communications, navigation)
- Military/Security layer (crypto domains, access control)
- Ground-based layer (mission ops, satellite ops, gateways)
- Core Mission layer (EO, communications, navigation payloads)

Each layer manages its own set of nodes and links, encryption
policies, and serialization.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
)

logger = logging.getLogger(__name__)


# =============================================================================
# EXCEPTIONS
# =============================================================================


class LayerError(Exception):
    """Base exception for functional-layer errors."""
    pass


class EncryptionError(LayerError):
    """Error related to encryption configuration."""
    pass


class ATMLayerError(LayerError):
    """Error related to ATM/CNS layer failures."""
    pass


class GroundLayerError(LayerError):
    """Error related to ground segment issues."""
    pass


# =============================================================================
# ENUMERATIONS
# =============================================================================


class EncryptionLevel(Enum):
    """Encryption level applied to a link or domain."""
    NONE = "NONE"
    LINK = "LINK"
    NETWORK = "NETWORK"
    APPLICATION = "APPLICATION"
    END_TO_END = "END_TO_END"


class CryptoKeyState(Enum):
    """State of a cryptographic key."""
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"
    PENDING_ROTATION = "PENDING_ROTATION"


class ATMServiceType(Enum):
    """ATM/CNS service categories."""
    ADS_B_SURVEILLANCE = "ADS_B_SURVEILLANCE"
    VHF_COMMUNICATIONS = "VHF_COMMUNICATIONS"
    VDL_DATALINK = "VDL_DATALINK"
    CPDLC = "CPDLC"
    CNS_NAVIGATION = "CNS_NAVIGATION"


class GroundSegmentType(Enum):
    """Ground segment facility types."""
    MOC = "MOC"              # Mission Operations Center
    SOC = "SOC"              # Satellite Operations Center
    GATEWAY = "GATEWAY"
    DATA_CENTER = "DATA_CENTER"
    USER_TERMINAL = "USER_TERMINAL"


class RedundancyMode(Enum):
    """Redundancy configuration for ground segments."""
    ACTIVE_ACTIVE = "ACTIVE_ACTIVE"
    ACTIVE_STANDBY = "ACTIVE_STANDBY"
    N_PLUS_ONE = "N_PLUS_ONE"


# =============================================================================
# DATA CLASSES – ENCRYPTION
# =============================================================================


@dataclass
class EncryptionPolicy:
    """Encryption policy describing layers applied in order."""
    levels: List[EncryptionLevel] = field(default_factory=list)
    key_rotation_hours: int = 24
    compartmentalized: bool = False
    description: str = ""


@dataclass
class CryptoDomain:
    """A cryptographic domain governing access to a set of nodes."""
    domain_id: str
    name: str
    encryption_policy: EncryptionPolicy
    allowed_node_ids: Set[str] = field(default_factory=set)
    key_state: CryptoKeyState = CryptoKeyState.ACTIVE

    def is_accessible(self, node_id: str) -> bool:
        """Return *True* if *node_id* may access this domain.

        Access is granted when the key is ACTIVE **and** either no
        restrictions exist (empty allow-list) or the node is explicitly
        listed.
        """
        if self.key_state != CryptoKeyState.ACTIVE:
            return False
        if not self.allowed_node_ids:
            return True
        return node_id in self.allowed_node_ids


# =============================================================================
# ATM / CNS LAYER
# =============================================================================


@dataclass
class ATMLayer:
    """Air Traffic Management / CNS functional layer."""
    layer_id: str = "ATM-CNS-LAYER"
    services: List[ATMServiceType] = field(
        default_factory=lambda: list(ATMServiceType),
    )
    max_latency_ms: float = 150.0
    max_jitter_ms: float = 20.0
    min_availability: float = 0.9999
    redundant_paths_required: int = 2
    node_ids: Set[str] = field(default_factory=set)
    link_ids: Set[str] = field(default_factory=set)
    description: str = (
        "ATM/UTM/CNS critical tenant layer providing air-traffic, "
        "communications, navigation, and surveillance services."
    )

    def add_node(self, node_id: str) -> None:
        """Register a node in this layer."""
        self.node_ids.add(node_id)
        logger.debug("ATMLayer: added node %s", node_id)

    def add_link(self, link_id: str) -> None:
        """Register a link in this layer."""
        self.link_ids.add(link_id)
        logger.debug("ATMLayer: added link %s", link_id)

    def meets_latency_requirement(self, actual_latency_ms: float) -> bool:
        """Return *True* if *actual_latency_ms* is within tolerance."""
        return actual_latency_ms <= self.max_latency_ms

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "layer_id": self.layer_id,
            "services": [s.value for s in self.services],
            "max_latency_ms": self.max_latency_ms,
            "max_jitter_ms": self.max_jitter_ms,
            "min_availability": self.min_availability,
            "redundant_paths_required": self.redundant_paths_required,
            "node_ids": sorted(self.node_ids),
            "link_ids": sorted(self.link_ids),
            "description": self.description,
        }


# =============================================================================
# MILITARY / SECURITY LAYER
# =============================================================================


@dataclass
class MilitarySecurityLayer:
    """Military and security overlay layer with crypto-domain governance."""
    layer_id: str = "MILITARY-SECURITY-LAYER"
    crypto_domains: Dict[str, CryptoDomain] = field(default_factory=dict)
    node_ids: Set[str] = field(default_factory=set)
    link_ids: Set[str] = field(default_factory=set)
    description: str = (
        "Military/security overlay providing compartmentalized "
        "encryption domains and access control."
    )

    def add_crypto_domain(self, domain: CryptoDomain) -> None:
        """Register a crypto domain."""
        self.crypto_domains[domain.domain_id] = domain
        logger.debug(
            "MilitarySecurityLayer: added crypto domain %s", domain.domain_id,
        )

    def get_domain(self, domain_id: str) -> Optional[CryptoDomain]:
        """Retrieve a crypto domain by ID, or *None*."""
        return self.crypto_domains.get(domain_id)

    def add_node(self, node_id: str) -> None:
        """Register a node in this layer."""
        self.node_ids.add(node_id)
        logger.debug("MilitarySecurityLayer: added node %s", node_id)

    def add_link(self, link_id: str) -> None:
        """Register a link in this layer."""
        self.link_ids.add(link_id)
        logger.debug("MilitarySecurityLayer: added link %s", link_id)

    def check_access(self, node_id: str, domain_id: str) -> bool:
        """Return *True* if *node_id* can access the crypto domain."""
        domain = self.crypto_domains.get(domain_id)
        if domain is None:
            return False
        return domain.is_accessible(node_id)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "layer_id": self.layer_id,
            "crypto_domains": {
                did: {
                    "domain_id": d.domain_id,
                    "name": d.name,
                    "key_state": d.key_state.value,
                    "encryption_policy": {
                        "levels": [lv.value for lv in d.encryption_policy.levels],
                        "key_rotation_hours": d.encryption_policy.key_rotation_hours,
                        "compartmentalized": d.encryption_policy.compartmentalized,
                        "description": d.encryption_policy.description,
                    },
                    "allowed_node_ids": sorted(d.allowed_node_ids),
                }
                for did, d in self.crypto_domains.items()
            },
            "node_ids": sorted(self.node_ids),
            "link_ids": sorted(self.link_ids),
            "description": self.description,
        }


# =============================================================================
# GROUND-BASED LAYER
# =============================================================================


@dataclass
class GroundBasedLayer:
    """Ground segment functional layer."""
    layer_id: str = "GROUND-BASED-LAYER"
    segments: Dict[str, GroundSegmentType] = field(default_factory=dict)
    redundancy_mode: RedundancyMode = RedundancyMode.ACTIVE_ACTIVE
    node_ids: Set[str] = field(default_factory=set)
    link_ids: Set[str] = field(default_factory=set)
    description: str = (
        "Ground segment layer managing mission operations centers, "
        "satellite operations, gateways, and user terminals."
    )

    def add_segment(self, segment_id: str, segment_type: GroundSegmentType) -> None:
        """Register a ground segment."""
        self.segments[segment_id] = segment_type
        logger.debug("GroundBasedLayer: added segment %s (%s)", segment_id, segment_type.value)

    def add_node(self, node_id: str) -> None:
        """Register a node in this layer."""
        self.node_ids.add(node_id)
        logger.debug("GroundBasedLayer: added node %s", node_id)

    def add_link(self, link_id: str) -> None:
        """Register a link in this layer."""
        self.link_ids.add(link_id)
        logger.debug("GroundBasedLayer: added link %s", link_id)

    def get_segments_by_type(self, seg_type: GroundSegmentType) -> List[str]:
        """Return segment IDs matching the given type."""
        return [
            sid for sid, stype in self.segments.items()
            if stype == seg_type
        ]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "layer_id": self.layer_id,
            "segments": {
                sid: stype.value for sid, stype in self.segments.items()
            },
            "redundancy_mode": self.redundancy_mode.value,
            "node_ids": sorted(self.node_ids),
            "link_ids": sorted(self.link_ids),
            "description": self.description,
        }


# =============================================================================
# CORE MISSION LAYER
# =============================================================================


@dataclass
class CoreMissionLayer:
    """Core mission data functional layer."""
    layer_id: str = "CORE-MISSION-LAYER"
    mission_types: List[str] = field(
        default_factory=lambda: ["eo", "communications", "navigation"],
    )
    node_ids: Set[str] = field(default_factory=set)
    link_ids: Set[str] = field(default_factory=set)
    description: str = (
        "Core mission data layer carrying primary payload traffic "
        "for Earth observation, communications, and navigation."
    )

    def add_node(self, node_id: str) -> None:
        """Register a node in this layer."""
        self.node_ids.add(node_id)
        logger.debug("CoreMissionLayer: added node %s", node_id)

    def add_link(self, link_id: str) -> None:
        """Register a link in this layer."""
        self.link_ids.add(link_id)
        logger.debug("CoreMissionLayer: added link %s", link_id)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "layer_id": self.layer_id,
            "mission_types": list(self.mission_types),
            "node_ids": sorted(self.node_ids),
            "link_ids": sorted(self.link_ids),
            "description": self.description,
        }


# =============================================================================
# FUNCTIONAL LAYER STACK
# =============================================================================


@dataclass
class FunctionalLayerStack:
    """Aggregates all functional layers into a single manageable stack."""
    stack_id: str
    core_mission: CoreMissionLayer = field(default_factory=CoreMissionLayer)
    atm: ATMLayer = field(default_factory=ATMLayer)
    military_security: MilitarySecurityLayer = field(default_factory=MilitarySecurityLayer)
    ground: GroundBasedLayer = field(default_factory=GroundBasedLayer)

    def get_all_layers(self) -> Dict[str, Any]:
        """Return all layers as a dictionary of serialized representations."""
        return {
            "core_mission": self.core_mission.to_dict(),
            "atm": self.atm.to_dict(),
            "military_security": self.military_security.to_dict(),
            "ground": self.ground.to_dict(),
        }

    def get_node_layers(self, node_id: str) -> List[str]:
        """Return the layer IDs that contain *node_id*."""
        layers: List[str] = []
        if node_id in self.core_mission.node_ids:
            layers.append(self.core_mission.layer_id)
        if node_id in self.atm.node_ids:
            layers.append(self.atm.layer_id)
        if node_id in self.military_security.node_ids:
            layers.append(self.military_security.layer_id)
        if node_id in self.ground.node_ids:
            layers.append(self.ground.layer_id)
        return layers

    def to_dict(self) -> Dict[str, Any]:
        """Serialize entire stack to dictionary."""
        return {
            "stack_id": self.stack_id,
            "layers": self.get_all_layers(),
        }
