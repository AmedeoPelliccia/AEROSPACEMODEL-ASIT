"""
Data Lifecycle Framework

Defines the end-to-end data lifecycle for aerospace network operations:
- Generation: data origin at sensor / subsystem nodes
- Classification: priority, security domain, QoS class assignment
- Transmission: route selection, multipath, disjoint-path options
- Processing: edge AI, in-network aggregation, ground-based analysis
- Consumption: delivery to mission control, ATM, defence, or model update

All lifecycle transitions are validated to ensure correct sequencing.
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
)

logger = logging.getLogger(__name__)


# =============================================================================
# EXCEPTIONS
# =============================================================================


class DataLifecycleError(Exception):
    """Base exception for data lifecycle errors."""
    pass


class ClassificationError(DataLifecycleError):
    """Error related to data classification problems."""
    pass


class RoutingError(DataLifecycleError):
    """Error related to data routing or transmission issues."""
    pass


class ProcessingError(DataLifecycleError):
    """Error related to data processing failures."""
    pass


# =============================================================================
# ENUMERATIONS
# =============================================================================


class LifecycleStage(Enum):
    """Stages in the data lifecycle pipeline."""
    GENERATION = "GENERATION"
    CLASSIFICATION = "CLASSIFICATION"
    TRANSMISSION = "TRANSMISSION"
    PROCESSING = "PROCESSING"
    CONSUMPTION = "CONSUMPTION"


class DataClass(Enum):
    """QoS data classification tiers."""
    CRITICAL_REALTIME = "CRITICAL_REALTIME"
    NEAR_REALTIME = "NEAR_REALTIME"
    BULK_DEFERRABLE = "BULK_DEFERRABLE"
    SECURITY = "SECURITY"
    ATM = "ATM"
    MILITARY = "MILITARY"


class SecurityDomain(Enum):
    """Security domain classification."""
    CIVIL = "CIVIL"
    DUAL_USE = "DUAL_USE"
    MILITARY = "MILITARY"
    CLASSIFIED = "CLASSIFIED"


class ProcessingLocation(Enum):
    """Where data processing takes place."""
    ON_BOARD = "ON_BOARD"          # Edge AI, compression
    IN_NETWORK = "IN_NETWORK"      # Aggregation, federated learning
    GROUND = "GROUND"              # Retraining, archive, deep analysis


class DataOriginType(Enum):
    """Type of data origination."""
    TELEMETRY = "TELEMETRY"
    HOUSEKEEPING = "HOUSEKEEPING"
    PAYLOAD_EO = "PAYLOAD_EO"
    PAYLOAD_COMMS = "PAYLOAD_COMMS"
    PAYLOAD_NAV = "PAYLOAD_NAV"
    ATM_SURVEILLANCE = "ATM_SURVEILLANCE"
    ATM_COMMUNICATIONS = "ATM_COMMUNICATIONS"
    SECURITY_EVENT = "SECURITY_EVENT"
    ANOMALY_DETECTION = "ANOMALY_DETECTION"


class ConsumptionAction(Enum):
    """Actions performed when data is consumed."""
    CONSTELLATION_CONTROL = "CONSTELLATION_CONTROL"
    MISSION_CONTROL = "MISSION_CONTROL"
    ATM_SERVICE = "ATM_SERVICE"
    DEFENSE_SERVICE = "DEFENSE_SERVICE"
    OBSERVATION_SERVICE = "OBSERVATION_SERVICE"
    SPACE_WEATHER = "SPACE_WEATHER"
    MODEL_UPDATE = "MODEL_UPDATE"
    POLICY_UPDATE = "POLICY_UPDATE"


# =============================================================================
# ORDERED STAGE LIST (for transition validation)
# =============================================================================

_STAGE_ORDER: List[LifecycleStage] = [
    LifecycleStage.GENERATION,
    LifecycleStage.CLASSIFICATION,
    LifecycleStage.TRANSMISSION,
    LifecycleStage.PROCESSING,
    LifecycleStage.CONSUMPTION,
]

_STAGE_INDEX: Dict[LifecycleStage, int] = {
    stage: idx for idx, stage in enumerate(_STAGE_ORDER)
}


# =============================================================================
# DATACLASSES
# =============================================================================


@dataclass
class DataClassification:
    """Classification metadata assigned to a data record."""
    data_class: DataClass
    security_domain: SecurityDomain
    priority: int = 5
    deadline_ms: Optional[float] = None
    origin_type: DataOriginType = DataOriginType.TELEMETRY
    destination_layer: Optional[str] = None

    def is_realtime(self) -> bool:
        """Return True if the data class requires real-time handling."""
        return self.data_class in (
            DataClass.CRITICAL_REALTIME,
            DataClass.NEAR_REALTIME,
        )


@dataclass
class QoSAssignment:
    """Quality-of-Service routing assignment for a data record."""
    classification: DataClassification
    assigned_route_ids: List[str] = field(default_factory=list)
    use_multipath: bool = False
    use_disjoint_paths: bool = False
    opportunistic_bulk: bool = False


@dataclass
class ProcessingDirective:
    """Directive describing where and how data is processed."""
    location: ProcessingLocation
    operations: List[str] = field(default_factory=list)
    model_id: Optional[str] = None
    federated: bool = False
    output_destination: Optional[str] = None


@dataclass
class DataRecord:
    """A single data record tracked through the lifecycle."""
    record_id: str
    timestamp: str
    stage: LifecycleStage = LifecycleStage.GENERATION
    classification: Optional[DataClassification] = None
    qos_assignment: Optional[QoSAssignment] = None
    processing_directives: List[ProcessingDirective] = field(default_factory=list)
    consumption_actions: List[ConsumptionAction] = field(default_factory=list)
    source_node_id: Optional[str] = None
    payload: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def advance_stage(self, new_stage: LifecycleStage) -> None:
        """Advance the record to *new_stage*.

        Stage transitions must be sequential:
        GENERATION -> CLASSIFICATION -> TRANSMISSION -> PROCESSING -> CONSUMPTION.

        Raises:
            DataLifecycleError: If the transition is not a valid forward step.
        """
        current_idx = _STAGE_INDEX[self.stage]
        new_idx = _STAGE_INDEX.get(new_stage)
        if new_idx is None:
            raise DataLifecycleError(
                f"Unknown lifecycle stage: {new_stage}"
            )
        if new_idx != current_idx + 1:
            raise DataLifecycleError(
                f"Invalid stage transition: {self.stage.value} -> "
                f"{new_stage.value} (expected {_STAGE_ORDER[current_idx + 1].value})"
                if current_idx + 1 < len(_STAGE_ORDER)
                else f"Invalid stage transition: {self.stage.value} -> "
                     f"{new_stage.value} (already at final stage)"
            )
        logger.debug(
            "Record %s: %s -> %s",
            self.record_id, self.stage.value, new_stage.value,
        )
        self.stage = new_stage

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "record_id": self.record_id,
            "timestamp": self.timestamp,
            "stage": self.stage.value,
            "classification": {
                "data_class": self.classification.data_class.value,
                "security_domain": self.classification.security_domain.value,
                "priority": self.classification.priority,
                "deadline_ms": self.classification.deadline_ms,
                "origin_type": self.classification.origin_type.value,
                "destination_layer": self.classification.destination_layer,
            } if self.classification else None,
            "qos_assignment": {
                "assigned_route_ids": self.qos_assignment.assigned_route_ids,
                "use_multipath": self.qos_assignment.use_multipath,
                "use_disjoint_paths": self.qos_assignment.use_disjoint_paths,
                "opportunistic_bulk": self.qos_assignment.opportunistic_bulk,
            } if self.qos_assignment else None,
            "processing_directives": [
                {
                    "location": d.location.value,
                    "operations": d.operations,
                    "model_id": d.model_id,
                    "federated": d.federated,
                    "output_destination": d.output_destination,
                }
                for d in self.processing_directives
            ],
            "consumption_actions": [a.value for a in self.consumption_actions],
            "source_node_id": self.source_node_id,
            "payload": self.payload,
            "metadata": self.metadata,
        }


# =============================================================================
# MANAGER
# =============================================================================


class DataLifecycleManager:
    """Manages data records through the full lifecycle pipeline."""

    def __init__(
        self,
        manager_id: str,
        records: Optional[Dict[str, DataRecord]] = None,
        classification_rules: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        self.manager_id = manager_id
        self.records: Dict[str, DataRecord] = records if records is not None else {}
        self.classification_rules: List[Dict[str, Any]] = (
            classification_rules if classification_rules is not None else []
        )

    # ------------------------------------------------------------------
    # Record creation
    # ------------------------------------------------------------------

    def create_record(
        self,
        record_id: str,
        origin_type: DataOriginType,
        source_node_id: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> DataRecord:
        """Create a new data record in the GENERATION stage."""
        from datetime import datetime, timezone

        record = DataRecord(
            record_id=record_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            stage=LifecycleStage.GENERATION,
            classification=None,
            source_node_id=source_node_id,
            payload=payload if payload is not None else {},
            metadata={"origin_type": origin_type.value},
        )
        self.records[record_id] = record
        logger.info("Created record %s (origin=%s)", record_id, origin_type.value)
        return record

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------

    def classify_record(
        self,
        record_id: str,
        data_class: DataClass,
        security_domain: SecurityDomain,
        priority: int = 5,
        deadline_ms: Optional[float] = None,
    ) -> DataRecord:
        """Classify a record and advance it to CLASSIFICATION stage.

        Raises:
            DataLifecycleError: If the record is not found.
        """
        record = self._get_record(record_id)
        origin_type_value = record.metadata.get(
            "origin_type", DataOriginType.TELEMETRY.value
        )
        origin_type = DataOriginType(origin_type_value)

        record.classification = DataClassification(
            data_class=data_class,
            security_domain=security_domain,
            priority=priority,
            deadline_ms=deadline_ms,
            origin_type=origin_type,
        )
        record.advance_stage(LifecycleStage.CLASSIFICATION)
        logger.info(
            "Classified record %s as %s / %s (priority=%d)",
            record_id, data_class.value, security_domain.value, priority,
        )
        return record

    # ------------------------------------------------------------------
    # Routing / QoS
    # ------------------------------------------------------------------

    def assign_routing(
        self,
        record_id: str,
        route_ids: List[str],
        use_multipath: bool = False,
        use_disjoint: bool = False,
    ) -> DataRecord:
        """Assign QoS routing and advance to TRANSMISSION stage."""
        record = self._get_record(record_id)
        if record.classification is None:
            raise RoutingError(
                f"Record {record_id} has no classification; classify first"
            )

        opportunistic = (
            record.classification.data_class == DataClass.BULK_DEFERRABLE
        )
        record.qos_assignment = QoSAssignment(
            classification=record.classification,
            assigned_route_ids=list(route_ids),
            use_multipath=use_multipath,
            use_disjoint_paths=use_disjoint,
            opportunistic_bulk=opportunistic,
        )
        record.advance_stage(LifecycleStage.TRANSMISSION)
        logger.info(
            "Assigned routing for record %s (routes=%s)",
            record_id, route_ids,
        )
        return record

    # ------------------------------------------------------------------
    # Processing
    # ------------------------------------------------------------------

    def add_processing(
        self,
        record_id: str,
        location: ProcessingLocation,
        operations: List[str],
        model_id: Optional[str] = None,
        federated: bool = False,
    ) -> DataRecord:
        """Add a processing directive.

        Advances the record to PROCESSING if it is currently in
        TRANSMISSION.  Raises :class:`DataLifecycleError` if the
        record is in a stage earlier than TRANSMISSION (or already
        past PROCESSING).
        """
        record = self._get_record(record_id)

        if record.stage not in (
            LifecycleStage.TRANSMISSION,
            LifecycleStage.PROCESSING,
        ):
            raise DataLifecycleError(
                f"Cannot add processing to record '{record_id}' "
                f"in stage {record.stage.value}; "
                f"expected TRANSMISSION or PROCESSING"
            )

        directive = ProcessingDirective(
            location=location,
            operations=list(operations),
            model_id=model_id,
            federated=federated,
        )
        record.processing_directives.append(directive)

        if record.stage == LifecycleStage.TRANSMISSION:
            record.advance_stage(LifecycleStage.PROCESSING)

        logger.info(
            "Added processing directive for record %s at %s",
            record_id, location.value,
        )
        return record

    # ------------------------------------------------------------------
    # Consumption
    # ------------------------------------------------------------------

    def mark_consumed(
        self,
        record_id: str,
        actions: List[ConsumptionAction],
    ) -> DataRecord:
        """Mark a record as consumed with the given actions.

        Advances the record to CONSUMPTION if it is currently in
        PROCESSING.  Raises :class:`DataLifecycleError` if the
        record is in a stage earlier than PROCESSING.
        """
        record = self._get_record(record_id)

        if record.stage not in (
            LifecycleStage.PROCESSING,
            LifecycleStage.CONSUMPTION,
        ):
            raise DataLifecycleError(
                f"Cannot mark record '{record_id}' as consumed "
                f"in stage {record.stage.value}; "
                f"expected PROCESSING or CONSUMPTION"
            )

        record.consumption_actions.extend(actions)

        if record.stage == LifecycleStage.PROCESSING:
            record.advance_stage(LifecycleStage.CONSUMPTION)

        logger.info(
            "Record %s consumed (actions=%s)",
            record_id, [a.value for a in actions],
        )
        return record

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_records_by_stage(self, stage: LifecycleStage) -> List[DataRecord]:
        """Return all records currently at *stage*."""
        return [r for r in self.records.values() if r.stage == stage]

    def get_records_by_class(self, data_class: DataClass) -> List[DataRecord]:
        """Return all records classified with *data_class*."""
        return [
            r for r in self.records.values()
            if r.classification is not None
            and r.classification.data_class == data_class
        ]

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "manager_id": self.manager_id,
            "record_count": len(self.records),
            "records": {
                rid: rec.to_dict() for rid, rec in self.records.items()
            },
            "classification_rules": self.classification_rules,
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_record(self, record_id: str) -> DataRecord:
        """Retrieve a record or raise DataLifecycleError."""
        record = self.records.get(record_id)
        if record is None:
            raise DataLifecycleError(f"Record not found: {record_id}")
        return record
