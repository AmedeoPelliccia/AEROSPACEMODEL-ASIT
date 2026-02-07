"""
Tests for Data Lifecycle Framework

Tests data classification, records, stage transitions, and the full
lifecycle manager including creation, classification, routing,
processing, consumption, and serialization.
"""

import pytest

from aerospacemodel.data_lifecycle.lifecycle import (
    ConsumptionAction,
    DataClass,
    DataClassification,
    DataLifecycleError,
    DataLifecycleManager,
    DataOriginType,
    DataRecord,
    LifecycleStage,
    ProcessingLocation,
    SecurityDomain,
)


class TestDataClassification:
    """Tests for DataClassification dataclass."""

    def test_classification_realtime(self):
        """Test that CRITICAL_REALTIME is identified as real-time."""
        cls = DataClassification(
            data_class=DataClass.CRITICAL_REALTIME,
            security_domain=SecurityDomain.CIVIL,
        )

        assert cls.is_realtime() is True

    def test_classification_not_realtime(self):
        """Test that BULK_DEFERRABLE is not real-time."""
        cls = DataClassification(
            data_class=DataClass.BULK_DEFERRABLE,
            security_domain=SecurityDomain.CIVIL,
        )

        assert cls.is_realtime() is False

    def test_classification_defaults(self):
        """Test DataClassification default field values."""
        cls = DataClassification(
            data_class=DataClass.ATM,
            security_domain=SecurityDomain.DUAL_USE,
        )

        assert cls.priority == 5
        assert cls.deadline_ms is None
        assert cls.origin_type == DataOriginType.TELEMETRY
        assert cls.destination_layer is None


class TestDataRecord:
    """Tests for DataRecord dataclass."""

    def test_record_creation_defaults(self):
        """Test DataRecord defaults upon creation."""
        record = DataRecord(record_id="REC-001", timestamp="2025-01-01T00:00:00Z")

        assert record.record_id == "REC-001"
        assert record.stage == LifecycleStage.GENERATION
        assert record.classification is None
        assert record.qos_assignment is None
        assert record.processing_directives == []
        assert record.consumption_actions == []

    def test_advance_stage_valid_sequence(self):
        """Test advancing through a valid stage sequence."""
        record = DataRecord(record_id="REC-002", timestamp="2025-01-01T00:00:00Z")

        record.advance_stage(LifecycleStage.CLASSIFICATION)
        assert record.stage == LifecycleStage.CLASSIFICATION

        record.advance_stage(LifecycleStage.TRANSMISSION)
        assert record.stage == LifecycleStage.TRANSMISSION

    def test_advance_stage_invalid_raises_error(self):
        """Test that skipping a stage raises DataLifecycleError."""
        record = DataRecord(record_id="REC-003", timestamp="2025-01-01T00:00:00Z")

        with pytest.raises(DataLifecycleError, match="Invalid stage transition"):
            record.advance_stage(LifecycleStage.PROCESSING)

    def test_record_to_dict(self):
        """Test DataRecord serialization to dict."""
        record = DataRecord(
            record_id="REC-004",
            timestamp="2025-01-01T00:00:00Z",
            payload={"sensor": "thermal"},
        )

        result = record.to_dict()

        assert result["record_id"] == "REC-004"
        assert result["stage"] == "GENERATION"
        assert result["classification"] is None
        assert result["payload"] == {"sensor": "thermal"}


class TestDataLifecycleManager:
    """Tests for DataLifecycleManager."""

    def test_create_record(self):
        """Test creating a new record through the manager."""
        mgr = DataLifecycleManager(manager_id="MGR-001")

        record = mgr.create_record(
            record_id="REC-100",
            origin_type=DataOriginType.TELEMETRY,
        )

        assert record.record_id == "REC-100"
        assert record.stage == LifecycleStage.GENERATION
        assert "REC-100" in mgr.records

    def test_classify_record(self):
        """Test classifying a record advances it to CLASSIFICATION."""
        mgr = DataLifecycleManager(manager_id="MGR-001")
        mgr.create_record(record_id="REC-101", origin_type=DataOriginType.TELEMETRY)

        record = mgr.classify_record(
            record_id="REC-101",
            data_class=DataClass.CRITICAL_REALTIME,
            security_domain=SecurityDomain.CIVIL,
            priority=1,
        )

        assert record.stage == LifecycleStage.CLASSIFICATION
        assert record.classification is not None
        assert record.classification.data_class == DataClass.CRITICAL_REALTIME

    def test_classify_nonexistent_record_raises_error(self):
        """Test that classifying a missing record raises DataLifecycleError."""
        mgr = DataLifecycleManager(manager_id="MGR-001")

        with pytest.raises(DataLifecycleError, match="Record not found"):
            mgr.classify_record(
                record_id="DOES-NOT-EXIST",
                data_class=DataClass.ATM,
                security_domain=SecurityDomain.CIVIL,
            )

    def test_assign_routing(self):
        """Test assigning routing advances record to TRANSMISSION."""
        mgr = DataLifecycleManager(manager_id="MGR-001")
        mgr.create_record(record_id="REC-102", origin_type=DataOriginType.TELEMETRY)
        mgr.classify_record(
            record_id="REC-102",
            data_class=DataClass.ATM,
            security_domain=SecurityDomain.CIVIL,
        )

        record = mgr.assign_routing(
            record_id="REC-102",
            route_ids=["ROUTE-A", "ROUTE-B"],
            use_multipath=True,
        )

        assert record.stage == LifecycleStage.TRANSMISSION
        assert record.qos_assignment is not None
        assert record.qos_assignment.assigned_route_ids == ["ROUTE-A", "ROUTE-B"]

    def test_add_processing(self):
        """Test adding processing advances record to PROCESSING."""
        mgr = DataLifecycleManager(manager_id="MGR-001")
        mgr.create_record(record_id="REC-103", origin_type=DataOriginType.TELEMETRY)
        mgr.classify_record(
            record_id="REC-103",
            data_class=DataClass.ATM,
            security_domain=SecurityDomain.CIVIL,
        )
        mgr.assign_routing(record_id="REC-103", route_ids=["R1"])

        record = mgr.add_processing(
            record_id="REC-103",
            location=ProcessingLocation.ON_BOARD,
            operations=["compress", "filter"],
        )

        assert record.stage == LifecycleStage.PROCESSING
        assert len(record.processing_directives) == 1
        assert record.processing_directives[0].operations == ["compress", "filter"]

    def test_mark_consumed(self):
        """Test marking record as consumed advances to CONSUMPTION."""
        mgr = DataLifecycleManager(manager_id="MGR-001")
        mgr.create_record(record_id="REC-104", origin_type=DataOriginType.TELEMETRY)
        mgr.classify_record(
            record_id="REC-104",
            data_class=DataClass.ATM,
            security_domain=SecurityDomain.CIVIL,
        )
        mgr.assign_routing(record_id="REC-104", route_ids=["R1"])
        mgr.add_processing(
            record_id="REC-104",
            location=ProcessingLocation.GROUND,
            operations=["analyse"],
        )

        record = mgr.mark_consumed(
            record_id="REC-104",
            actions=[ConsumptionAction.ATM_SERVICE],
        )

        assert record.stage == LifecycleStage.CONSUMPTION
        assert ConsumptionAction.ATM_SERVICE in record.consumption_actions

    def test_get_records_by_stage(self):
        """Test filtering records by lifecycle stage."""
        mgr = DataLifecycleManager(manager_id="MGR-001")
        mgr.create_record(record_id="REC-A", origin_type=DataOriginType.TELEMETRY)
        mgr.create_record(record_id="REC-B", origin_type=DataOriginType.TELEMETRY)
        mgr.classify_record(
            record_id="REC-B",
            data_class=DataClass.ATM,
            security_domain=SecurityDomain.CIVIL,
        )

        gen_records = mgr.get_records_by_stage(LifecycleStage.GENERATION)
        cls_records = mgr.get_records_by_stage(LifecycleStage.CLASSIFICATION)

        assert len(gen_records) == 1
        assert gen_records[0].record_id == "REC-A"
        assert len(cls_records) == 1
        assert cls_records[0].record_id == "REC-B"

    def test_get_records_by_class(self):
        """Test filtering records by data class."""
        mgr = DataLifecycleManager(manager_id="MGR-001")
        mgr.create_record(record_id="REC-X", origin_type=DataOriginType.TELEMETRY)
        mgr.classify_record(
            record_id="REC-X",
            data_class=DataClass.SECURITY,
            security_domain=SecurityDomain.MILITARY,
        )

        results = mgr.get_records_by_class(DataClass.SECURITY)

        assert len(results) == 1
        assert results[0].record_id == "REC-X"

    def test_full_lifecycle_flow(self):
        """Test end-to-end lifecycle: create, classify, route, process, consume."""
        mgr = DataLifecycleManager(manager_id="MGR-E2E")
        mgr.create_record(record_id="E2E-001", origin_type=DataOriginType.PAYLOAD_EO)
        mgr.classify_record(
            record_id="E2E-001",
            data_class=DataClass.NEAR_REALTIME,
            security_domain=SecurityDomain.DUAL_USE,
            priority=2,
        )
        mgr.assign_routing(
            record_id="E2E-001",
            route_ids=["R1", "R2"],
            use_multipath=True,
        )
        mgr.add_processing(
            record_id="E2E-001",
            location=ProcessingLocation.IN_NETWORK,
            operations=["aggregate"],
            federated=True,
        )
        record = mgr.mark_consumed(
            record_id="E2E-001",
            actions=[ConsumptionAction.OBSERVATION_SERVICE],
        )

        assert record.stage == LifecycleStage.CONSUMPTION
        assert record.classification.is_realtime() is True

    def test_to_dict(self):
        """Test DataLifecycleManager serialization to dict."""
        mgr = DataLifecycleManager(manager_id="MGR-SER")
        mgr.create_record(record_id="REC-S", origin_type=DataOriginType.TELEMETRY)

        result = mgr.to_dict()

        assert result["manager_id"] == "MGR-SER"
        assert result["record_count"] == 1
        assert "REC-S" in result["records"]
