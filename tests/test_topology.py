"""
Tests for Mesh 3D Topology Module

Tests mesh nodes, links, TSUs, QoS profiles, and the full topology manager
including path finding, connectivity analysis, and serialization.
"""

import pytest

from aerospacemodel.topology.mesh import (
    FunctionalLayer,
    FunctionalLayerType,
    LinkType,
    Mesh3DTopology,
    MeshLink,
    MeshNode,
    NodeRole,
    OrbitalLayer,
    QoSClass,
    QoSProfile,
    RoutingError,
    TopologicalServiceUnit,
    TopologyError,
)


class TestMeshNode:
    """Tests for MeshNode dataclass."""

    def test_node_creation_with_defaults(self):
        """Test creating a MeshNode with default values."""
        node = MeshNode(
            node_id="SAT-001",
            role=NodeRole.SATELLITE,
            orbital_layer=OrbitalLayer.LEO,
        )

        assert node.node_id == "SAT-001"
        assert node.role == NodeRole.SATELLITE
        assert node.orbital_layer == OrbitalLayer.LEO
        assert node.position == {}
        assert node.functional_layers == []
        assert node.tsu_id is None
        assert node.is_operational is True
        assert node.capacity_gbps == 1.0

    def test_node_with_functional_layers(self):
        """Test creating a MeshNode with functional layer membership."""
        node = MeshNode(
            node_id="SAT-002",
            role=NodeRole.SATELLITE,
            orbital_layer=OrbitalLayer.MEO,
            functional_layers=[
                FunctionalLayerType.CORE_MISSION,
                FunctionalLayerType.ATM_CNS,
            ],
        )

        assert len(node.functional_layers) == 2
        assert FunctionalLayerType.CORE_MISSION in node.functional_layers
        assert FunctionalLayerType.ATM_CNS in node.functional_layers

    def test_node_custom_position(self):
        """Test creating a MeshNode with a custom position dict."""
        position = {"x": 1.0, "y": 2.0, "z": 500.0}
        node = MeshNode(
            node_id="SAT-003",
            role=NodeRole.GATEWAY,
            orbital_layer=OrbitalLayer.GEO,
            position=position,
            capacity_gbps=10.0,
        )

        assert node.position == {"x": 1.0, "y": 2.0, "z": 500.0}
        assert node.capacity_gbps == 10.0
        assert node.role == NodeRole.GATEWAY


class TestMeshLink:
    """Tests for MeshLink dataclass."""

    def test_link_creation(self):
        """Test creating a MeshLink with explicit values."""
        link = MeshLink(
            link_id="L-001",
            source_id="SAT-001",
            target_id="SAT-002",
            link_type=LinkType.INTRA_ORBIT,
            capacity_gbps=5.0,
            latency_ms=2.5,
        )

        assert link.link_id == "L-001"
        assert link.source_id == "SAT-001"
        assert link.target_id == "SAT-002"
        assert link.link_type == LinkType.INTRA_ORBIT
        assert link.capacity_gbps == 5.0
        assert link.latency_ms == 2.5

    def test_link_defaults(self):
        """Test MeshLink default field values."""
        link = MeshLink(
            link_id="L-002",
            source_id="SAT-A",
            target_id="SAT-B",
            link_type=LinkType.CROSS_LAYER,
        )

        assert link.capacity_gbps == 1.0
        assert link.latency_ms == 10.0
        assert link.is_active is True
        assert link.functional_layers == []


class TestTopologicalServiceUnit:
    """Tests for TopologicalServiceUnit."""

    def test_tsu_meets_redundancy(self):
        """Test TSU meets minimum redundancy level."""
        tsu = TopologicalServiceUnit(
            tsu_id="TSU-001",
            redundancy_level=3,
        )

        assert tsu.meets_redundancy(2) is True
        assert tsu.meets_redundancy(3) is True

    def test_tsu_insufficient_redundancy(self):
        """Test TSU fails redundancy check when level is too low."""
        tsu = TopologicalServiceUnit(
            tsu_id="TSU-002",
            redundancy_level=1,
        )

        assert tsu.meets_redundancy(2) is False

    def test_tsu_defaults(self):
        """Test TSU default field values."""
        tsu = TopologicalServiceUnit(tsu_id="TSU-003")

        assert tsu.redundancy_level == 2
        assert tsu.qos_profiles == []
        assert tsu.node_ids == []
        assert tsu.is_active is True


class TestQoSProfile:
    """Tests for QoSProfile."""

    def test_qos_profile_creation(self):
        """Test creating a QoSProfile with all fields."""
        profile = QoSProfile(
            qos_class=QoSClass.CRITICAL_REALTIME,
            max_latency_ms=10.0,
            max_jitter_ms=1.0,
            min_availability=0.9999,
            min_redundant_paths=3,
            priority=1,
        )

        assert profile.qos_class == QoSClass.CRITICAL_REALTIME
        assert profile.max_latency_ms == 10.0
        assert profile.min_availability == 0.9999
        assert profile.min_redundant_paths == 3

    def test_qos_priority(self):
        """Test that QoS priority values are stored correctly."""
        high = QoSProfile(
            qos_class=QoSClass.CRITICAL_REALTIME,
            max_latency_ms=5.0,
            max_jitter_ms=0.5,
            min_availability=0.999,
            min_redundant_paths=2,
            priority=1,
        )
        low = QoSProfile(
            qos_class=QoSClass.BULK_DEFERRABLE,
            max_latency_ms=5000.0,
            max_jitter_ms=100.0,
            min_availability=0.95,
            min_redundant_paths=1,
            priority=10,
        )

        assert high.priority < low.priority


# ─── Helper to build a small topology ────────────────────────────────────────

def _make_node(node_id: str, layer: OrbitalLayer = OrbitalLayer.LEO) -> MeshNode:
    return MeshNode(node_id=node_id, role=NodeRole.SATELLITE, orbital_layer=layer)


def _make_link(link_id: str, src: str, tgt: str) -> MeshLink:
    return MeshLink(
        link_id=link_id, source_id=src, target_id=tgt,
        link_type=LinkType.INTRA_ORBIT,
    )


class TestMesh3DTopology:
    """Tests for Mesh3DTopology manager."""

    def test_add_node(self):
        """Test adding a node to the topology."""
        topo = Mesh3DTopology(topology_id="T1")
        node = _make_node("A")

        topo.add_node(node)

        assert "A" in topo.nodes

    def test_add_duplicate_node_raises_error(self):
        """Test that adding a duplicate node raises TopologyError."""
        topo = Mesh3DTopology(topology_id="T1")
        topo.add_node(_make_node("A"))

        with pytest.raises(TopologyError, match="already exists"):
            topo.add_node(_make_node("A"))

    def test_add_link(self):
        """Test adding a link between two existing nodes."""
        topo = Mesh3DTopology(topology_id="T1")
        topo.add_node(_make_node("A"))
        topo.add_node(_make_node("B"))

        topo.add_link(_make_link("L1", "A", "B"))

        assert "L1" in topo.links

    def test_add_link_missing_node_raises_error(self):
        """Test that adding a link with a missing node raises TopologyError."""
        topo = Mesh3DTopology(topology_id="T1")
        topo.add_node(_make_node("A"))

        with pytest.raises(TopologyError, match="not found"):
            topo.add_link(_make_link("L1", "A", "MISSING"))

    def test_get_neighbors(self):
        """Test retrieving neighbours of a node."""
        topo = Mesh3DTopology(topology_id="T1")
        topo.add_node(_make_node("A"))
        topo.add_node(_make_node("B"))
        topo.add_node(_make_node("C"))
        topo.add_link(_make_link("L1", "A", "B"))
        topo.add_link(_make_link("L2", "A", "C"))

        neighbors = topo.get_neighbors("A")

        assert set(neighbors) == {"B", "C"}

    def test_find_paths_simple(self):
        """Test finding a path in a small linear graph A-B-C."""
        topo = Mesh3DTopology(topology_id="T1")
        for nid in ("A", "B", "C"):
            topo.add_node(_make_node(nid))
        topo.add_link(_make_link("L1", "A", "B"))
        topo.add_link(_make_link("L2", "B", "C"))

        paths = topo.find_paths("A", "C")

        assert len(paths) >= 1
        assert paths[0] == ["A", "B", "C"]

    def test_find_paths_no_path_raises_error(self):
        """Test that RoutingError is raised for disconnected nodes."""
        topo = Mesh3DTopology(topology_id="T1")
        topo.add_node(_make_node("A"))
        topo.add_node(_make_node("Z"))

        with pytest.raises(RoutingError, match="No path"):
            topo.find_paths("A", "Z")

    def test_find_disjoint_paths(self):
        """Test finding node-disjoint paths in a graph with two routes."""
        # Graph: A-B-D and A-C-D (two disjoint paths)
        topo = Mesh3DTopology(topology_id="T1")
        for nid in ("A", "B", "C", "D"):
            topo.add_node(_make_node(nid))
        topo.add_link(_make_link("L1", "A", "B"))
        topo.add_link(_make_link("L2", "B", "D"))
        topo.add_link(_make_link("L3", "A", "C"))
        topo.add_link(_make_link("L4", "C", "D"))

        disjoint = topo.find_disjoint_paths("A", "D")

        assert len(disjoint) >= 2

    def test_check_k_connectivity_passes(self):
        """Test k-connectivity passes on a well-connected graph."""
        # Fully connected 4-node graph (each connected to every other)
        topo = Mesh3DTopology(topology_id="T1")
        nodes = ["A", "B", "C", "D"]
        for nid in nodes:
            topo.add_node(_make_node(nid))
        link_idx = 0
        for i, a in enumerate(nodes):
            for b in nodes[i + 1:]:
                topo.add_link(_make_link(f"L{link_idx}", a, b))
                link_idx += 1

        assert topo.check_k_connectivity(2) is True

    def test_check_k_connectivity_fails(self):
        """Test k-connectivity fails on a chain topology for k=2."""
        # Chain: A-B-C (B is a single point of failure)
        topo = Mesh3DTopology(topology_id="T1")
        for nid in ("A", "B", "C"):
            topo.add_node(_make_node(nid))
        topo.add_link(_make_link("L1", "A", "B"))
        topo.add_link(_make_link("L2", "B", "C"))

        assert topo.check_k_connectivity(2) is False

    def test_get_single_points_of_failure(self):
        """Test detection of articulation points."""
        # Chain: A-B-C  -> B is an articulation point
        topo = Mesh3DTopology(topology_id="T1")
        for nid in ("A", "B", "C"):
            topo.add_node(_make_node(nid))
        topo.add_link(_make_link("L1", "A", "B"))
        topo.add_link(_make_link("L2", "B", "C"))

        spofs = topo.get_single_points_of_failure()

        assert "B" in spofs

    def test_get_layer_subgraph(self):
        """Test retrieving node/link sets for a functional layer."""
        topo = Mesh3DTopology(topology_id="T1")
        layer = FunctionalLayer(
            layer_type=FunctionalLayerType.CORE_MISSION,
            description="Core mission layer",
        )
        topo.register_functional_layer(layer)

        node = MeshNode(
            node_id="SAT-1",
            role=NodeRole.SATELLITE,
            orbital_layer=OrbitalLayer.LEO,
            functional_layers=[FunctionalLayerType.CORE_MISSION],
        )
        topo.add_node(node)

        node_ids, link_ids = topo.get_layer_subgraph(
            FunctionalLayerType.CORE_MISSION
        )

        assert "SAT-1" in node_ids

    def test_to_dict(self):
        """Test serialization of topology to dict."""
        topo = Mesh3DTopology(topology_id="T1")
        topo.add_node(_make_node("A"))

        result = topo.to_dict()

        assert result["topology_id"] == "T1"
        assert "A" in result["nodes"]
        assert isinstance(result["links"], dict)
        assert isinstance(result["tsus"], dict)
        assert isinstance(result["functional_layers"], dict)
