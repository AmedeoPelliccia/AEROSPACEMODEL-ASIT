"""
Distributed Cognitive Intelligence Module

Implements the cognitive/distributed intelligence layer for AEROSPACEMODEL —
the "field of models" representing emergent intelligence from data flows
in the governed 3D mesh topology.

This module defines:
- Model tiers (micro, in-network, foundation)
- Physics-informed constraints on model behaviour
- Federated learning sessions across constellation nodes
- The DistributedModelField that manages all models
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
    Union,
)

logger = logging.getLogger(__name__)


# =============================================================================
# EXCEPTIONS
# =============================================================================


class CognitiveError(Exception):
    """Base exception for cognitive/distributed intelligence errors."""
    pass


class ModelRegistrationError(CognitiveError):
    """Error related to model registration issues."""
    pass


class FederationError(CognitiveError):
    """Error related to federated learning issues."""
    pass


class PhysicsConstraintError(CognitiveError):
    """Error related to physics constraint violations."""
    pass


# =============================================================================
# ENUMERATIONS
# =============================================================================


class ModelTier(Enum):
    """Model deployment tier within the constellation architecture."""
    MICRO = "MICRO"                # On-board satellite
    IN_NETWORK = "IN_NETWORK"      # Aggregation/consensus in constellation
    FOUNDATION = "FOUNDATION"      # Ground-based, retrained with global data


class ModelCapability(Enum):
    """Capabilities a model may provide."""
    ANOMALY_DETECTION = "ANOMALY_DETECTION"
    SEMANTIC_COMPRESSION = "SEMANTIC_COMPRESSION"
    LOCAL_CONTROL = "LOCAL_CONTROL"
    EDGE_INFERENCE = "EDGE_INFERENCE"
    COLLABORATIVE_INFERENCE = "COLLABORATIVE_INFERENCE"
    FEDERATED_AGGREGATION = "FEDERATED_AGGREGATION"
    INTELLIGENT_CACHING = "INTELLIGENT_CACHING"
    DEEP_ANALYSIS = "DEEP_ANALYSIS"
    RETRAINING = "RETRAINING"
    ARCHIVE_ANALYTICS = "ARCHIVE_ANALYTICS"


class GovernanceRole(Enum):
    """Governance role a model may hold in the distributed field."""
    CONTRIBUTOR = "CONTRIBUTOR"    # Can contribute to training
    INFERRER = "INFERRER"          # Can only use for inference
    AGGREGATOR = "AGGREGATOR"      # Can aggregate federated updates
    VALIDATOR = "VALIDATOR"        # Can validate model outputs


_DEFAULT_FOUNDATION_CAPABILITIES: List[ModelCapability] = [
    ModelCapability.DEEP_ANALYSIS,
    ModelCapability.RETRAINING,
    ModelCapability.ARCHIVE_ANALYTICS,
]


class PhysicsConstraintType(Enum):
    """Types of physics constraints applicable to distributed models."""
    ORBITAL_DYNAMICS = "ORBITAL_DYNAMICS"
    SIGNAL_PROPAGATION = "SIGNAL_PROPAGATION"
    POWER_BUDGET = "POWER_BUDGET"
    LINK_BUDGET = "LINK_BUDGET"
    THERMAL = "THERMAL"
    RADIATION = "RADIATION"


# =============================================================================
# DATA CLASSES
# =============================================================================


@dataclass
class PhysicsConstraint:
    """
    A physics constraint governing model behaviour.

    Parameters hold numeric limits (e.g. {"max_power_w": 50.0}).
    Hard constraints block operation; soft constraints apply penalties.
    """
    constraint_type: PhysicsConstraintType
    description: str
    parameters: Dict[str, float] = field(default_factory=dict)
    is_hard_constraint: bool = True

    def check(self, value: float, parameter_key: str) -> bool:
        """Return True if *value* does NOT exceed the specified parameter.

        Raises:
            PhysicsConstraintError: If *parameter_key* is not found.
        """
        if parameter_key not in self.parameters:
            raise PhysicsConstraintError(
                f"Parameter key '{parameter_key}' not found in constraint "
                f"'{self.constraint_type.value}'"
            )
        return value <= self.parameters[parameter_key]


@dataclass
class MicroModel:
    """An on-board micro model deployed on a constellation node."""
    model_id: str
    node_id: str
    tier: ModelTier = ModelTier.MICRO
    capabilities: List[ModelCapability] = field(default_factory=list)
    governance_role: GovernanceRole = GovernanceRole.INFERRER
    physics_constraints: List[PhysicsConstraint] = field(default_factory=list)
    version: str = "1.0.0"
    is_active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    def can_contribute(self) -> bool:
        """Return True if this model's role allows training contributions."""
        return self.governance_role in (
            GovernanceRole.CONTRIBUTOR,
            GovernanceRole.AGGREGATOR,
        )

    def has_capability(self, cap: ModelCapability) -> bool:
        """Return True if this model possesses the given capability."""
        return cap in self.capabilities

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the micro model to a dictionary."""
        return {
            "model_id": self.model_id,
            "node_id": self.node_id,
            "tier": self.tier.value,
            "capabilities": [c.value for c in self.capabilities],
            "governance_role": self.governance_role.value,
            "physics_constraints": [
                {
                    "constraint_type": pc.constraint_type.value,
                    "description": pc.description,
                    "parameters": pc.parameters,
                    "is_hard_constraint": pc.is_hard_constraint,
                }
                for pc in self.physics_constraints
            ],
            "version": self.version,
            "is_active": self.is_active,
            "metadata": self.metadata,
        }


@dataclass
class FederatedSession:
    """A federated learning session across constellation nodes."""
    session_id: str
    round_number: int = 0
    participant_model_ids: List[str] = field(default_factory=list)
    aggregator_model_id: Optional[str] = None
    is_active: bool = True
    contributions_received: int = 0
    consensus_reached: bool = False

    def add_participant(self, model_id: str) -> None:
        """Add a participant model to this session."""
        if model_id not in self.participant_model_ids:
            self.participant_model_ids.append(model_id)
            logger.debug(
                "Added participant '%s' to session '%s'",
                model_id,
                self.session_id,
            )

    def record_contribution(self) -> None:
        """Record a single federated contribution."""
        self.contributions_received += 1
        logger.debug(
            "Session '%s' contributions: %d",
            self.session_id,
            self.contributions_received,
        )

    def check_consensus(self, min_contributions: int) -> bool:
        """Set and return consensus status if enough contributions received."""
        if self.contributions_received >= min_contributions:
            self.consensus_reached = True
        return self.consensus_reached

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the federated session to a dictionary."""
        return {
            "session_id": self.session_id,
            "round_number": self.round_number,
            "participant_model_ids": list(self.participant_model_ids),
            "aggregator_model_id": self.aggregator_model_id,
            "is_active": self.is_active,
            "contributions_received": self.contributions_received,
            "consensus_reached": self.consensus_reached,
        }


@dataclass
class FoundationModel:
    """A ground-based foundation model retrained with global data."""
    model_id: str
    tier: ModelTier = ModelTier.FOUNDATION
    capabilities: List[ModelCapability] = field(
        default_factory=lambda: list(_DEFAULT_FOUNDATION_CAPABILITIES)
    )
    ground_node_id: Optional[str] = None
    version: str = "1.0.0"
    retrain_sources: List[str] = field(default_factory=list)
    physics_informed: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_retrain_source(self, source_id: str) -> None:
        """Register a data source for retraining."""
        if source_id not in self.retrain_sources:
            self.retrain_sources.append(source_id)
            logger.debug(
                "Added retrain source '%s' to foundation model '%s'",
                source_id,
                self.model_id,
            )

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the foundation model to a dictionary."""
        return {
            "model_id": self.model_id,
            "tier": self.tier.value,
            "capabilities": [c.value for c in self.capabilities],
            "ground_node_id": self.ground_node_id,
            "version": self.version,
            "retrain_sources": list(self.retrain_sources),
            "physics_informed": self.physics_informed,
            "metadata": self.metadata,
        }


# =============================================================================
# DISTRIBUTED MODEL FIELD
# =============================================================================


@dataclass
class DistributedModelField:
    """
    The 'field of models' — manages all distributed models across the
    constellation topology.

    Provides registration, querying, federated session management, and
    physics constraint enforcement.
    """
    field_id: str
    micro_models: Dict[str, MicroModel] = field(default_factory=dict)
    foundation_models: Dict[str, FoundationModel] = field(default_factory=dict)
    federated_sessions: Dict[str, FederatedSession] = field(default_factory=dict)
    physics_constraints: List[PhysicsConstraint] = field(default_factory=list)

    # ── Registration ────────────────────────────────────────────────────

    def register_micro_model(self, model: MicroModel) -> None:
        """Register a micro model.

        Raises:
            ModelRegistrationError: If a model with the same ID already exists.
        """
        if model.model_id in self.micro_models:
            raise ModelRegistrationError(
                f"Micro model '{model.model_id}' is already registered"
            )
        self.micro_models[model.model_id] = model
        logger.info(
            "Registered micro model '%s' on node '%s'",
            model.model_id,
            model.node_id,
        )

    def register_foundation_model(self, model: FoundationModel) -> None:
        """Register a foundation model.

        Raises:
            ModelRegistrationError: If a model with the same ID already exists.
        """
        if model.model_id in self.foundation_models:
            raise ModelRegistrationError(
                f"Foundation model '{model.model_id}' is already registered"
            )
        self.foundation_models[model.model_id] = model
        logger.info(
            "Registered foundation model '%s'",
            model.model_id,
        )

    # ── Queries ─────────────────────────────────────────────────────────

    def get_models_on_node(self, node_id: str) -> List[MicroModel]:
        """Return all micro models deployed on a specific node."""
        return [
            m for m in self.micro_models.values()
            if m.node_id == node_id
        ]

    def get_models_by_capability(
        self, capability: ModelCapability
    ) -> List[Union[MicroModel, FoundationModel]]:
        """Return all models (micro and foundation) with a given capability."""
        results: List[Union[MicroModel, FoundationModel]] = []
        for m in self.micro_models.values():
            if m.has_capability(capability):
                results.append(m)
        for fm in self.foundation_models.values():
            if capability in fm.capabilities:
                results.append(fm)
        return results

    def get_contributors(self) -> List[MicroModel]:
        """Return all micro models that can contribute to training."""
        return [
            m for m in self.micro_models.values()
            if m.can_contribute()
        ]

    # ── Federated Sessions ──────────────────────────────────────────────

    def create_federated_session(
        self,
        session_id: str,
        participant_ids: List[str],
        aggregator_id: str,
    ) -> FederatedSession:
        """Create a federated learning session.

        Validates that all participant and aggregator models exist.

        Raises:
            FederationError: If any referenced model is not registered.
        """
        # Validate aggregator
        if (
            aggregator_id not in self.micro_models
            and aggregator_id not in self.foundation_models
        ):
            raise FederationError(
                f"Aggregator model '{aggregator_id}' not found"
            )

        # Validate participants
        for pid in participant_ids:
            if (
                pid not in self.micro_models
                and pid not in self.foundation_models
            ):
                raise FederationError(
                    f"Participant model '{pid}' not found"
                )

        session = FederatedSession(
            session_id=session_id,
            participant_model_ids=list(participant_ids),
            aggregator_model_id=aggregator_id,
        )
        self.federated_sessions[session_id] = session
        logger.info(
            "Created federated session '%s' with %d participants",
            session_id,
            len(participant_ids),
        )
        return session

    # ── Physics Constraints ─────────────────────────────────────────────

    def apply_physics_constraint(self, constraint: PhysicsConstraint) -> None:
        """Add a global physics constraint to the field."""
        self.physics_constraints.append(constraint)
        logger.info(
            "Applied global physics constraint: %s",
            constraint.constraint_type.value,
        )

    # ── Summaries / Serialisation ───────────────────────────────────────

    def get_field_summary(self) -> Dict[str, Any]:
        """Return a summary of the distributed model field."""
        active_sessions = [
            s for s in self.federated_sessions.values() if s.is_active
        ]
        return {
            "field_id": self.field_id,
            "micro_model_count": len(self.micro_models),
            "foundation_model_count": len(self.foundation_models),
            "federated_session_count": len(self.federated_sessions),
            "active_session_count": len(active_sessions),
            "global_constraint_count": len(self.physics_constraints),
        }

    def to_dict(self) -> Dict[str, Any]:
        """Serialise the entire distributed model field to a dictionary."""
        return {
            "field_id": self.field_id,
            "micro_models": {
                mid: m.to_dict() for mid, m in self.micro_models.items()
            },
            "foundation_models": {
                fid: fm.to_dict() for fid, fm in self.foundation_models.items()
            },
            "federated_sessions": {
                sid: s.to_dict() for sid, s in self.federated_sessions.items()
            },
            "physics_constraints": [
                {
                    "constraint_type": pc.constraint_type.value,
                    "description": pc.description,
                    "parameters": pc.parameters,
                    "is_hard_constraint": pc.is_hard_constraint,
                }
                for pc in self.physics_constraints
            ],
        }
