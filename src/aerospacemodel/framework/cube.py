"""
Unified 3-Axis Cube Framework

Implements the unified cube framework for AEROSPACEMODEL — the intersection
of data lifecycle, topology, and domains/layers.  Each point in the cube
represents a :class:`CubeCell` where a lifecycle stage, topology position,
and functional domain layer meet.

The three axes are:

1. **Data Lifecycle** — stages from generation through consumption.
2. **Topology** — orbital layers and link types in the mesh.
3. **Domain / Layer** — functional layer classification (core mission, ATM/CNS,
   military, ground).

Cells may be annotated with service, security, and model-role profiles to
capture QoS, encryption, and cognitive-layer requirements at each point.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from aerospacemodel.topology.mesh import (
    FunctionalLayerType,
    OrbitalLayer,
)
from aerospacemodel.data_lifecycle.lifecycle import (
    LifecycleStage,
)

logger = logging.getLogger(__name__)


# =============================================================================
# EXCEPTIONS
# =============================================================================


class FrameworkError(Exception):
    """Base exception for unified framework errors."""
    pass


class CellConfigurationError(FrameworkError):
    """Error related to cube cell configuration issues."""
    pass


class ProfileValidationError(FrameworkError):
    """Error related to profile validation failures."""
    pass


# =============================================================================
# DATA STRUCTURES
# =============================================================================


@dataclass
class ServiceProfile:
    """Quality-of-service profile attached to a cube cell.

    Captures availability, latency, and redundancy requirements for
    the intersection of lifecycle stage, topology position, and domain
    layer represented by the cell.
    """
    qos_class: str
    min_availability: float = 0.99
    max_latency_ms: float = 1000.0
    redundant_paths: int = 1
    resilience_level: str = "standard"

    def is_high_availability(self) -> bool:
        """Return True if *min_availability* is at least 0.999."""
        return self.min_availability >= 0.999


@dataclass
class SecurityProfile:
    """Security profile attached to a cube cell.

    Defines encryption, compartmentalisation, and auditing requirements
    for data traversing this point in the cube.
    """
    security_domain: str
    encryption_layers: List[str] = field(default_factory=list)
    compartmentalized: bool = False
    key_rotation_hours: int = 24
    audit_required: bool = True


@dataclass
class ModelRole:
    """Cognitive model role attached to a cube cell.

    Describes which model tier operates at this cube point, what it
    can do, and whether it trains or only infers.
    """
    model_tier: str
    capabilities: List[str] = field(default_factory=list)
    governance_role: str = "INFERRER"
    learns: bool = False
    infers: bool = True


@dataclass
class CubeCell:
    """A single point in the unified 3-axis framework cube.

    Each cell sits at the intersection of a lifecycle stage, a
    topology position, and a functional domain layer.  Optional
    profiles annotate the cell with service, security, and model
    requirements.
    """
    cell_id: str
    lifecycle_stage: str
    topology_position: str
    domain_layer: str
    service_profile: Optional[ServiceProfile] = None
    security_profile: Optional[SecurityProfile] = None
    model_role: Optional[ModelRole] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_fully_configured(self) -> bool:
        """Return True if all three profiles are set."""
        return (
            self.service_profile is not None
            and self.security_profile is not None
            and self.model_role is not None
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the cube cell to a plain dictionary."""
        return {
            "cell_id": self.cell_id,
            "lifecycle_stage": self.lifecycle_stage,
            "topology_position": self.topology_position,
            "domain_layer": self.domain_layer,
            "service_profile": {
                "qos_class": self.service_profile.qos_class,
                "min_availability": self.service_profile.min_availability,
                "max_latency_ms": self.service_profile.max_latency_ms,
                "redundant_paths": self.service_profile.redundant_paths,
                "resilience_level": self.service_profile.resilience_level,
            } if self.service_profile is not None else None,
            "security_profile": {
                "security_domain": self.security_profile.security_domain,
                "encryption_layers": list(
                    self.security_profile.encryption_layers
                ),
                "compartmentalized": self.security_profile.compartmentalized,
                "key_rotation_hours": (
                    self.security_profile.key_rotation_hours
                ),
                "audit_required": self.security_profile.audit_required,
            } if self.security_profile is not None else None,
            "model_role": {
                "model_tier": self.model_role.model_tier,
                "capabilities": list(self.model_role.capabilities),
                "governance_role": self.model_role.governance_role,
                "learns": self.model_role.learns,
                "infers": self.model_role.infers,
            } if self.model_role is not None else None,
            "metadata": self.metadata,
        }


# =============================================================================
# AXIS DEFAULTS
# =============================================================================


def _default_lifecycle_stages() -> List[str]:
    """Return all :class:`LifecycleStage` values as strings."""
    return [stage.value for stage in LifecycleStage]


def _default_topology_positions() -> List[str]:
    """Return all :class:`OrbitalLayer` values as strings."""
    return [layer.value for layer in OrbitalLayer]


def _default_domain_layers() -> List[str]:
    """Return all :class:`FunctionalLayerType` values as strings."""
    return [layer.value for layer in FunctionalLayerType]


# =============================================================================
# UNIFIED FRAMEWORK
# =============================================================================


@dataclass
class UnifiedFramework:
    """The unified 3-axis cube framework.

    Manages :class:`CubeCell` instances positioned across three axes:

    * **Lifecycle** — data lifecycle stages.
    * **Topology** — orbital layers and link types.
    * **Domain** — functional layer classifications.

    Cells are keyed by their *cell_id* and may be queried along any
    single axis or filtered by configuration completeness.
    """
    framework_id: str
    cells: Dict[str, CubeCell] = field(default_factory=dict)
    axis_lifecycle_stages: List[str] = field(
        default_factory=_default_lifecycle_stages
    )
    axis_topology_positions: List[str] = field(
        default_factory=_default_topology_positions
    )
    axis_domain_layers: List[str] = field(
        default_factory=_default_domain_layers
    )

    # ------------------------------------------------------------------
    # Cell management
    # ------------------------------------------------------------------

    def add_cell(self, cell: CubeCell) -> None:
        """Add a cell to the framework.

        Args:
            cell: The cube cell to add.

        Raises:
            FrameworkError: If a cell with the same ID already exists.
        """
        if cell.cell_id in self.cells:
            raise FrameworkError(
                f"Cell '{cell.cell_id}' already exists in framework "
                f"'{self.framework_id}'"
            )
        self.cells[cell.cell_id] = cell
        logger.debug(
            "Added cell '%s' to framework '%s'",
            cell.cell_id, self.framework_id,
        )

    def get_cell(self, cell_id: str) -> Optional[CubeCell]:
        """Retrieve a cell by its ID.

        Args:
            cell_id: Unique cell identifier.

        Returns:
            The :class:`CubeCell` if found, otherwise ``None``.
        """
        return self.cells.get(cell_id)

    def create_cell(
        self,
        lifecycle_stage: str,
        topology_position: str,
        domain_layer: str,
        service_profile: Optional[ServiceProfile] = None,
        security_profile: Optional[SecurityProfile] = None,
        model_role: Optional[ModelRole] = None,
    ) -> CubeCell:
        """Create a new cell from the three axis coordinates.

        The *cell_id* is auto-generated from the axis values.

        Args:
            lifecycle_stage: Lifecycle stage value.
            topology_position: Topology position value.
            domain_layer: Domain layer value.
            service_profile: Optional service QoS profile.
            security_profile: Optional security profile.
            model_role: Optional cognitive model role.

        Returns:
            The newly created and stored :class:`CubeCell`.
        """
        cell_id = f"{lifecycle_stage}::{topology_position}::{domain_layer}"
        cell = CubeCell(
            cell_id=cell_id,
            lifecycle_stage=lifecycle_stage,
            topology_position=topology_position,
            domain_layer=domain_layer,
            service_profile=service_profile,
            security_profile=security_profile,
            model_role=model_role,
        )
        self.add_cell(cell)
        return cell

    # ------------------------------------------------------------------
    # Axis queries
    # ------------------------------------------------------------------

    def get_cells_by_stage(self, stage: str) -> List[CubeCell]:
        """Return all cells matching a lifecycle stage.

        Args:
            stage: Lifecycle stage value to filter by.

        Returns:
            List of matching :class:`CubeCell` instances.
        """
        return [
            c for c in self.cells.values()
            if c.lifecycle_stage == stage
        ]

    def get_cells_by_layer(self, layer: str) -> List[CubeCell]:
        """Return all cells matching a domain layer.

        Args:
            layer: Domain layer value to filter by.

        Returns:
            List of matching :class:`CubeCell` instances.
        """
        return [
            c for c in self.cells.values()
            if c.domain_layer == layer
        ]

    def get_cells_by_position(self, position: str) -> List[CubeCell]:
        """Return all cells matching a topology position.

        Args:
            position: Topology position value to filter by.

        Returns:
            List of matching :class:`CubeCell` instances.
        """
        return [
            c for c in self.cells.values()
            if c.topology_position == position
        ]

    # ------------------------------------------------------------------
    # Configuration queries
    # ------------------------------------------------------------------

    def get_configured_cells(self) -> List[CubeCell]:
        """Return cells where all three profiles are set."""
        return [
            c for c in self.cells.values()
            if c.is_fully_configured()
        ]

    def get_unconfigured_cells(self) -> List[CubeCell]:
        """Return cells that are missing one or more profiles."""
        return [
            c for c in self.cells.values()
            if not c.is_fully_configured()
        ]

    # ------------------------------------------------------------------
    # Summaries / Serialisation
    # ------------------------------------------------------------------

    def get_framework_summary(self) -> Dict[str, Any]:
        """Return a high-level summary of the framework.

        Returns:
            Dictionary with total cell count, configured count,
            and per-axis breakdowns.
        """
        configured = self.get_configured_cells()
        stages: Dict[str, int] = {}
        positions: Dict[str, int] = {}
        layers: Dict[str, int] = {}
        for cell in self.cells.values():
            stages[cell.lifecycle_stage] = (
                stages.get(cell.lifecycle_stage, 0) + 1
            )
            positions[cell.topology_position] = (
                positions.get(cell.topology_position, 0) + 1
            )
            layers[cell.domain_layer] = (
                layers.get(cell.domain_layer, 0) + 1
            )

        return {
            "framework_id": self.framework_id,
            "total_cells": len(self.cells),
            "configured_cells": len(configured),
            "unconfigured_cells": len(self.cells) - len(configured),
            "cells_per_lifecycle_stage": stages,
            "cells_per_topology_position": positions,
            "cells_per_domain_layer": layers,
        }

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the full framework to a plain dictionary.

        Returns:
            Dictionary representation suitable for YAML/JSON export.
        """
        return {
            "framework_id": self.framework_id,
            "axis_lifecycle_stages": list(self.axis_lifecycle_stages),
            "axis_topology_positions": list(self.axis_topology_positions),
            "axis_domain_layers": list(self.axis_domain_layers),
            "cells": {
                cid: cell.to_dict()
                for cid, cell in self.cells.items()
            },
        }
