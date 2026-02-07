"""
Tests for Unified 3-Axis Cube Framework

Tests service profiles, security profiles, model roles, cube cells,
and the unified framework manager including cell management, axis
queries, configuration queries, and serialization.
"""

import pytest

from aerospacemodel.framework.cube import (
    CubeCell,
    FrameworkError,
    ModelRole,
    SecurityProfile,
    ServiceProfile,
    UnifiedFramework,
)


class TestServiceProfile:
    """Tests for ServiceProfile dataclass."""

    def test_service_profile_high_availability(self):
        """Test that min_availability >= 0.999 is high availability."""
        profile = ServiceProfile(
            qos_class="CRITICAL_REALTIME",
            min_availability=0.9999,
            max_latency_ms=10.0,
            redundant_paths=3,
        )

        assert profile.is_high_availability() is True

    def test_service_profile_not_high_availability(self):
        """Test that min_availability below 0.999 is not high availability."""
        profile = ServiceProfile(
            qos_class="BULK_DEFERRABLE",
            min_availability=0.95,
        )

        assert profile.is_high_availability() is False


class TestSecurityProfile:
    """Tests for SecurityProfile dataclass."""

    def test_security_profile_creation(self):
        """Test creating a SecurityProfile with explicit values."""
        profile = SecurityProfile(
            security_domain="MILITARY",
            encryption_layers=["AES-256", "QUANTUM"],
            compartmentalized=True,
            key_rotation_hours=4,
            audit_required=True,
        )

        assert profile.security_domain == "MILITARY"
        assert len(profile.encryption_layers) == 2
        assert profile.compartmentalized is True
        assert profile.key_rotation_hours == 4

    def test_security_profile_defaults(self):
        """Test SecurityProfile default values."""
        profile = SecurityProfile(security_domain="CIVIL")

        assert profile.encryption_layers == []
        assert profile.compartmentalized is False
        assert profile.key_rotation_hours == 24
        assert profile.audit_required is True


class TestModelRole:
    """Tests for ModelRole dataclass."""

    def test_model_role_defaults(self):
        """Test ModelRole default field values."""
        role = ModelRole(model_tier="EDGE")

        assert role.capabilities == []
        assert role.governance_role == "INFERRER"
        assert role.learns is False
        assert role.infers is True

    def test_model_role_learning(self):
        """Test ModelRole configured for learning."""
        role = ModelRole(
            model_tier="GROUND",
            capabilities=["anomaly_detection", "retraining"],
            governance_role="TRAINER",
            learns=True,
            infers=True,
        )

        assert role.learns is True
        assert role.governance_role == "TRAINER"
        assert "retraining" in role.capabilities


class TestCubeCell:
    """Tests for CubeCell dataclass."""

    def test_cell_creation(self):
        """Test creating a CubeCell with required fields."""
        cell = CubeCell(
            cell_id="GEN::LEO::CORE",
            lifecycle_stage="GENERATION",
            topology_position="LEO",
            domain_layer="CORE_MISSION",
        )

        assert cell.cell_id == "GEN::LEO::CORE"
        assert cell.lifecycle_stage == "GENERATION"
        assert cell.service_profile is None

    def test_cell_fully_configured(self):
        """Test that a cell with all three profiles is fully configured."""
        cell = CubeCell(
            cell_id="FULL",
            lifecycle_stage="PROCESSING",
            topology_position="MEO",
            domain_layer="ATM_CNS",
            service_profile=ServiceProfile(qos_class="ATM"),
            security_profile=SecurityProfile(security_domain="CIVIL"),
            model_role=ModelRole(model_tier="EDGE"),
        )

        assert cell.is_fully_configured() is True

    def test_cell_not_fully_configured(self):
        """Test that a cell missing a profile is not fully configured."""
        cell = CubeCell(
            cell_id="PARTIAL",
            lifecycle_stage="TRANSMISSION",
            topology_position="GEO",
            domain_layer="CORE_MISSION",
            service_profile=ServiceProfile(qos_class="NEAR_REALTIME"),
        )

        assert cell.is_fully_configured() is False

    def test_cell_to_dict(self):
        """Test CubeCell serialization to dict."""
        cell = CubeCell(
            cell_id="SER",
            lifecycle_stage="CONSUMPTION",
            topology_position="GROUND",
            domain_layer="GROUND_BASED",
            service_profile=ServiceProfile(qos_class="BULK"),
            security_profile=SecurityProfile(security_domain="CIVIL"),
            model_role=ModelRole(model_tier="GROUND"),
        )

        result = cell.to_dict()

        assert result["cell_id"] == "SER"
        assert result["service_profile"]["qos_class"] == "BULK"
        assert result["security_profile"]["security_domain"] == "CIVIL"
        assert result["model_role"]["model_tier"] == "GROUND"


# ─── Helper to build profiles ────────────────────────────────────────────────

def _full_profiles():
    return dict(
        service_profile=ServiceProfile(qos_class="ATM"),
        security_profile=SecurityProfile(security_domain="CIVIL"),
        model_role=ModelRole(model_tier="EDGE"),
    )


class TestUnifiedFramework:
    """Tests for UnifiedFramework manager."""

    def test_add_cell(self):
        """Test adding a cell to the framework."""
        fw = UnifiedFramework(framework_id="FW-1")
        cell = CubeCell(
            cell_id="C1",
            lifecycle_stage="GENERATION",
            topology_position="LEO",
            domain_layer="CORE_MISSION",
        )

        fw.add_cell(cell)

        assert "C1" in fw.cells

    def test_add_duplicate_cell_raises_error(self):
        """Test that adding a duplicate cell raises FrameworkError."""
        fw = UnifiedFramework(framework_id="FW-1")
        cell = CubeCell(
            cell_id="DUP",
            lifecycle_stage="GENERATION",
            topology_position="LEO",
            domain_layer="CORE_MISSION",
        )
        fw.add_cell(cell)

        with pytest.raises(FrameworkError, match="already exists"):
            fw.add_cell(cell)

    def test_create_cell(self):
        """Test creating a cell via create_cell helper."""
        fw = UnifiedFramework(framework_id="FW-1")

        cell = fw.create_cell(
            lifecycle_stage="PROCESSING",
            topology_position="MEO",
            domain_layer="ATM_CNS",
        )

        assert cell.cell_id == "PROCESSING::MEO::ATM_CNS"
        assert cell.cell_id in fw.cells

    def test_get_cell(self):
        """Test retrieving a cell by ID."""
        fw = UnifiedFramework(framework_id="FW-1")
        fw.create_cell("GENERATION", "LEO", "CORE_MISSION")

        result = fw.get_cell("GENERATION::LEO::CORE_MISSION")

        assert result is not None
        assert result.lifecycle_stage == "GENERATION"

    def test_get_cells_by_stage(self):
        """Test filtering cells by lifecycle stage."""
        fw = UnifiedFramework(framework_id="FW-1")
        fw.create_cell("GENERATION", "LEO", "CORE_MISSION")
        fw.create_cell("GENERATION", "MEO", "ATM_CNS")
        fw.create_cell("PROCESSING", "LEO", "CORE_MISSION")

        result = fw.get_cells_by_stage("GENERATION")

        assert len(result) == 2

    def test_get_cells_by_layer(self):
        """Test filtering cells by domain layer."""
        fw = UnifiedFramework(framework_id="FW-1")
        fw.create_cell("GENERATION", "LEO", "CORE_MISSION")
        fw.create_cell("PROCESSING", "MEO", "CORE_MISSION")
        fw.create_cell("PROCESSING", "GEO", "ATM_CNS")

        result = fw.get_cells_by_layer("CORE_MISSION")

        assert len(result) == 2

    def test_get_configured_cells(self):
        """Test retrieving fully configured cells."""
        fw = UnifiedFramework(framework_id="FW-1")
        fw.create_cell("GENERATION", "LEO", "CORE_MISSION", **_full_profiles())
        fw.create_cell("PROCESSING", "MEO", "ATM_CNS")  # incomplete

        configured = fw.get_configured_cells()

        assert len(configured) == 1
        assert configured[0].lifecycle_stage == "GENERATION"

    def test_get_unconfigured_cells(self):
        """Test retrieving unconfigured cells."""
        fw = UnifiedFramework(framework_id="FW-1")
        fw.create_cell("GENERATION", "LEO", "CORE_MISSION", **_full_profiles())
        fw.create_cell("PROCESSING", "MEO", "ATM_CNS")

        unconfigured = fw.get_unconfigured_cells()

        assert len(unconfigured) == 1
        assert unconfigured[0].lifecycle_stage == "PROCESSING"

    def test_get_framework_summary(self):
        """Test framework summary generation."""
        fw = UnifiedFramework(framework_id="FW-SUM")
        fw.create_cell("GENERATION", "LEO", "CORE_MISSION", **_full_profiles())
        fw.create_cell("PROCESSING", "MEO", "ATM_CNS")

        summary = fw.get_framework_summary()

        assert summary["framework_id"] == "FW-SUM"
        assert summary["total_cells"] == 2
        assert summary["configured_cells"] == 1
        assert summary["unconfigured_cells"] == 1

    def test_to_dict(self):
        """Test UnifiedFramework serialization to dict."""
        fw = UnifiedFramework(framework_id="FW-SER")
        fw.create_cell("GENERATION", "LEO", "CORE_MISSION")

        result = fw.to_dict()

        assert result["framework_id"] == "FW-SER"
        assert "GENERATION::LEO::CORE_MISSION" in result["cells"]
        assert isinstance(result["axis_lifecycle_stages"], list)
        assert isinstance(result["axis_topology_positions"], list)
        assert isinstance(result["axis_domain_layers"], list)
