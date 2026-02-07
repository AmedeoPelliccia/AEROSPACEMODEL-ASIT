"""
Mesh 3D Topology Module

Implements a three-dimensional mesh topology for satellite constellations
governed by the AEROSPACEMODEL framework. Provides:
- Multi-layer orbital mesh modelling (LEO, MEO, GEO, Ground)
- Topological Service Unit (TSU) abstraction
- Functional layer isolation (Core Mission, ATM/CNS, Military, Ground)
- QoS-aware path finding and k-connectivity analysis
- Single-point-of-failure detection (articulation points)

The topology is designed around the concept of a 3D mesh where:
- X/Y dimensions represent orbital planes and positions within a plane
- Z dimension represents orbital altitude layers and ground segments
- Functional layers provide logical isolation across the physical mesh
"""

from __future__ import annotations

import logging
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
)

logger = logging.getLogger(__name__)

# Limits for graph algorithms to prevent combinatorial explosion
_MAX_BFS_QUEUE_SIZE = 10000
_MAX_PATHS = 5
_MAX_CONNECTIVITY_SAMPLE_PAIRS = 20


# =============================================================================
# EXCEPTIONS
# =============================================================================


class TopologyError(Exception):
    """Base exception for topology-related errors."""
    pass


class ConnectivityError(TopologyError):
    """Error related to mesh connectivity issues."""
    pass


class RoutingError(TopologyError):
    """Error related to path routing failures."""
    pass


class TSUConfigurationError(TopologyError):
    """Error related to Topological Service Unit configuration."""
    pass


# =============================================================================
# ENUMERATIONS
# =============================================================================


class OrbitalLayer(Enum):
    """Orbital altitude layer classification."""
    LEO = "LEO"        # Low Earth Orbit
    MEO = "MEO"        # Medium Earth Orbit
    GEO = "GEO"        # Geostationary Orbit
    GROUND = "GROUND"  # Ground segment


class LinkType(Enum):
    """Inter-node link type classification."""
    INTRA_ORBIT = "INTRA_ORBIT"          # Same orbital ring
    INTER_ORBIT = "INTER_ORBIT"          # Diagonal between orbits
    CROSS_LAYER = "CROSS_LAYER"          # GEO/MEO hubs
    GROUND_UPLINK = "GROUND_UPLINK"      # Ground to space
    GROUND_DOWNLINK = "GROUND_DOWNLINK"  # Space to ground


class FunctionalLayerType(Enum):
    """Logical functional layer classification."""
    CORE_MISSION = "CORE_MISSION"
    ATM_CNS = "ATM_CNS"
    MILITARY_SECURITY = "MILITARY_SECURITY"
    GROUND_BASED = "GROUND_BASED"


class NodeRole(Enum):
    """Role of a mesh node within the constellation."""
    SATELLITE = "SATELLITE"
    GATEWAY = "GATEWAY"
    HUB = "HUB"
    GROUND_STATION = "GROUND_STATION"
    DATA_CENTER = "DATA_CENTER"
    MOC_SOC = "MOC_SOC"  # Mission/Satellite Operations Center


class QoSClass(Enum):
    """Quality of Service classification."""
    CRITICAL_REALTIME = "CRITICAL_REALTIME"
    NEAR_REALTIME = "NEAR_REALTIME"
    BULK_DEFERRABLE = "BULK_DEFERRABLE"
    SECURITY = "SECURITY"
    ATM = "ATM"
    MILITARY = "MILITARY"


# =============================================================================
# DATA STRUCTURES
# =============================================================================


@dataclass
class QoSProfile:
    """Quality of Service profile for a functional layer or TSU.

    Defines performance and availability constraints that must be
    satisfied when routing traffic through the mesh.
    """
    qos_class: QoSClass
    max_latency_ms: float
    max_jitter_ms: float
    min_availability: float  # 0.0 – 1.0
    min_redundant_paths: int
    priority: int  # 1 = highest


@dataclass
class TopologicalServiceUnit:
    """Topological Service Unit (TSU).

    Groups mesh nodes into a resilient service cluster with
    defined redundancy and QoS guarantees.
    """
    tsu_id: str
    redundancy_level: int = 2
    qos_profiles: List[QoSProfile] = field(default_factory=list)
    node_ids: List[str] = field(default_factory=list)
    is_active: bool = True

    def meets_redundancy(self, min_level: int) -> bool:
        """Check whether this TSU meets the required redundancy level.

        Args:
            min_level: Minimum required redundancy level.

        Returns:
            True if the TSU redundancy level is at least *min_level*.
        """
        return self.redundancy_level >= min_level


@dataclass
class MeshNode:
    """A single node in the 3D mesh topology.

    Represents a satellite, ground station, or other network element
    with its orbital parameters, functional layer membership, and
    capacity characteristics.
    """
    node_id: str
    role: NodeRole
    orbital_layer: OrbitalLayer
    position: Dict[str, float] = field(default_factory=dict)
    functional_layers: List[FunctionalLayerType] = field(default_factory=list)
    tsu_id: Optional[str] = None
    is_operational: bool = True
    capacity_gbps: float = 1.0


@dataclass
class MeshLink:
    """A link between two mesh nodes, treated as bidirectional.

    Carries traffic between nodes with defined capacity, latency,
    and functional layer assignments.  The topology builds an
    undirected adjacency list so every link is traversable in both
    directions regardless of *source_id* / *target_id* ordering.
    """
    link_id: str
    source_id: str
    target_id: str
    link_type: LinkType
    capacity_gbps: float = 1.0
    latency_ms: float = 10.0
    is_active: bool = True
    functional_layers: List[FunctionalLayerType] = field(default_factory=list)


@dataclass
class FunctionalLayer:
    """Logical overlay that isolates a subset of nodes and links.

    Provides traffic separation for mission-specific or
    security-sensitive communication.
    """
    layer_type: FunctionalLayerType
    description: str
    node_ids: Set[str] = field(default_factory=set)
    link_ids: Set[str] = field(default_factory=set)
    qos_profile: Optional[QoSProfile] = None
    encryption_required: bool = False


# =============================================================================
# MESH 3D TOPOLOGY MANAGER
# =============================================================================


@dataclass
class Mesh3DTopology:
    """Three-dimensional mesh topology manager.

    Maintains the full constellation graph (nodes, links, TSUs,
    functional layers) and exposes analysis primitives such as
    path finding, k-connectivity checking, and single-point-of-failure
    detection.
    """
    topology_id: str
    nodes: Dict[str, MeshNode] = field(default_factory=dict)
    links: Dict[str, MeshLink] = field(default_factory=dict)
    tsus: Dict[str, TopologicalServiceUnit] = field(default_factory=dict)
    functional_layers: Dict[FunctionalLayerType, FunctionalLayer] = field(
        default_factory=dict
    )

    # ------------------------------------------------------------------
    # Node / Link / TSU management
    # ------------------------------------------------------------------

    def add_node(self, node: MeshNode) -> None:
        """Add a node to the topology.

        The node is also registered in every functional layer it
        declares membership in.

        Args:
            node: The mesh node to add.

        Raises:
            TopologyError: If a node with the same ID already exists.
        """
        if node.node_id in self.nodes:
            raise TopologyError(
                f"Node '{node.node_id}' already exists in topology "
                f"'{self.topology_id}'"
            )
        self.nodes[node.node_id] = node
        for layer_type in node.functional_layers:
            if layer_type in self.functional_layers:
                self.functional_layers[layer_type].node_ids.add(node.node_id)
        logger.debug("Added node '%s' to topology '%s'",
                      node.node_id, self.topology_id)

    def add_link(self, link: MeshLink) -> None:
        """Add a link to the topology.

        Both the source and target nodes must already exist.

        Args:
            link: The mesh link to add.

        Raises:
            TopologyError: If the link ID is duplicate or referenced
                nodes do not exist.
        """
        if link.link_id in self.links:
            raise TopologyError(
                f"Link '{link.link_id}' already exists in topology "
                f"'{self.topology_id}'"
            )
        if link.source_id not in self.nodes:
            raise TopologyError(
                f"Source node '{link.source_id}' not found in topology "
                f"'{self.topology_id}'"
            )
        if link.target_id not in self.nodes:
            raise TopologyError(
                f"Target node '{link.target_id}' not found in topology "
                f"'{self.topology_id}'"
            )
        self.links[link.link_id] = link
        for layer_type in link.functional_layers:
            if layer_type in self.functional_layers:
                self.functional_layers[layer_type].link_ids.add(link.link_id)
        logger.debug("Added link '%s' (%s -> %s) to topology '%s'",
                      link.link_id, link.source_id, link.target_id,
                      self.topology_id)

    def add_tsu(self, tsu: TopologicalServiceUnit) -> None:
        """Register a Topological Service Unit.

        Args:
            tsu: The TSU to register.

        Raises:
            TSUConfigurationError: If a TSU with the same ID exists.
        """
        if tsu.tsu_id in self.tsus:
            raise TSUConfigurationError(
                f"TSU '{tsu.tsu_id}' already exists in topology "
                f"'{self.topology_id}'"
            )
        self.tsus[tsu.tsu_id] = tsu
        logger.debug("Registered TSU '%s' in topology '%s'",
                      tsu.tsu_id, self.topology_id)

    def register_functional_layer(self, layer: FunctionalLayer) -> None:
        """Register a functional layer.

        Args:
            layer: The functional layer to register.
        """
        self.functional_layers[layer.layer_type] = layer
        logger.debug("Registered functional layer '%s' in topology '%s'",
                      layer.layer_type.value, self.topology_id)

    # ------------------------------------------------------------------
    # Graph queries
    # ------------------------------------------------------------------

    def _build_adjacency(
        self, *, active_only: bool = True
    ) -> Dict[str, List[str]]:
        """Build an undirected adjacency list from active links.

        Args:
            active_only: When True, skip inactive links and
                non-operational nodes.

        Returns:
            Mapping of node ID to list of neighbour node IDs.
        """
        adj: Dict[str, List[str]] = {
            nid: [] for nid, n in self.nodes.items()
            if not active_only or n.is_operational
        }
        for link in self.links.values():
            if active_only and not link.is_active:
                continue
            if link.source_id in adj and link.target_id in adj:
                adj[link.source_id].append(link.target_id)
                adj[link.target_id].append(link.source_id)
        return adj

    def get_neighbors(self, node_id: str) -> List[str]:
        """Return IDs of all nodes connected to the given node.

        Only active links and operational nodes are considered.

        Args:
            node_id: The node whose neighbours to retrieve.

        Returns:
            List of neighbour node IDs.

        Raises:
            TopologyError: If *node_id* is not in the topology.
        """
        if node_id not in self.nodes:
            raise TopologyError(
                f"Node '{node_id}' not found in topology "
                f"'{self.topology_id}'"
            )
        adj = self._build_adjacency()
        return list(adj.get(node_id, []))

    # ------------------------------------------------------------------
    # Path finding
    # ------------------------------------------------------------------

    def find_paths(
        self,
        source_id: str,
        target_id: str,
        max_hops: int = 10,
    ) -> List[List[str]]:
        """Find up to ``_MAX_PATHS`` paths between two nodes using BFS.

        Args:
            source_id: Origin node ID.
            target_id: Destination node ID.
            max_hops: Maximum number of hops per path.

        Returns:
            List of paths (capped at ``_MAX_PATHS``), each path being
            a list of node IDs from *source_id* to *target_id*.

        Raises:
            TopologyError: If source or target node is missing.
            RoutingError: If no path exists.
        """
        for nid in (source_id, target_id):
            if nid not in self.nodes:
                raise TopologyError(
                    f"Node '{nid}' not found in topology "
                    f"'{self.topology_id}'"
                )

        adj = self._build_adjacency()
        paths: List[List[str]] = []
        queue: deque[List[str]] = deque([[source_id]])

        while queue and len(paths) < _MAX_PATHS:
            path = queue.popleft()
            if len(path) - 1 >= max_hops:
                continue
            current = path[-1]
            visited = set(path)
            for neighbor in adj.get(current, []):
                if neighbor in visited:
                    continue
                new_path = path + [neighbor]
                if neighbor == target_id:
                    paths.append(new_path)
                    if len(paths) >= _MAX_PATHS:
                        break
                elif len(queue) < _MAX_BFS_QUEUE_SIZE:
                    queue.append(new_path)

        if not paths:
            raise RoutingError(
                f"No path from '{source_id}' to '{target_id}' in "
                f"topology '{self.topology_id}'"
            )
        return paths

    @staticmethod
    def _bfs_shortest(
        adj: Dict[str, List[str]],
        source: str,
        target: str,
        excluded: Set[str],
    ) -> Optional[List[str]]:
        """BFS shortest path on *adj* skipping *excluded* nodes.

        Returns:
            Path as list of node IDs, or None if unreachable.
        """
        if source == target:
            return [source]
        parent: Dict[str, Optional[str]] = {source: None}
        queue: deque[str] = deque([source])
        while queue:
            current = queue.popleft()
            for neighbor in adj.get(current, []):
                if neighbor in parent or neighbor in excluded:
                    continue
                parent[neighbor] = current
                if neighbor == target:
                    path: List[str] = []
                    node: Optional[str] = target
                    while node is not None:
                        path.append(node)
                        node = parent[node]
                    path.reverse()
                    return path
                queue.append(neighbor)
        return None

    def find_disjoint_paths(
        self,
        source_id: str,
        target_id: str,
    ) -> List[List[str]]:
        """Find node-disjoint paths between two nodes.

        Uses iterative BFS: after finding a path, intermediate nodes
        (excluding source and target) are removed before searching for
        the next path.

        Args:
            source_id: Origin node ID.
            target_id: Destination node ID.

        Returns:
            List of node-disjoint paths (node ID lists).
        """
        for nid in (source_id, target_id):
            if nid not in self.nodes:
                raise TopologyError(
                    f"Node '{nid}' not found in topology "
                    f"'{self.topology_id}'"
                )

        adj = self._build_adjacency()
        excluded: Set[str] = set()
        disjoint: List[List[str]] = []

        while True:
            found = self._bfs_shortest(adj, source_id, target_id, excluded)
            if found is None:
                break
            disjoint.append(found)
            # Exclude intermediate nodes for next iteration
            new_excluded = {nid for nid in found[1:-1] if nid not in excluded}
            if not new_excluded:
                # Direct edge with no intermediates — remove the edge
                # from the adjacency so we can look for longer
                # node-disjoint alternatives.
                if len(found) == 2:
                    src, tgt = found[0], found[1]
                    if tgt in adj.get(src, []):
                        adj[src] = [n for n in adj[src] if n != tgt]
                    if src in adj.get(tgt, []):
                        adj[tgt] = [n for n in adj[tgt] if n != src]
                    continue
                # Path reuses only already-excluded intermediates
                break
            excluded.update(new_excluded)

        return disjoint

    # ------------------------------------------------------------------
    # Connectivity analysis
    # ------------------------------------------------------------------

    def check_k_connectivity(self, k: int) -> bool:
        """Check if the topology is at least *k*-connected.

        Samples up to ``_MAX_CONNECTIVITY_SAMPLE_PAIRS`` operational
        node pairs and verifies that at least *k* node-disjoint paths
        exist for each pair.

        Args:
            k: Minimum connectivity level.

        Returns:
            True if every sampled pair has at least *k* disjoint paths.
        """
        operational = [
            nid for nid, n in self.nodes.items() if n.is_operational
        ]
        if len(operational) < 2:
            return k <= 0

        pairs: List[Tuple[str, str]] = []
        for i, a in enumerate(operational):
            for b in operational[i + 1:]:
                pairs.append((a, b))
                if len(pairs) >= _MAX_CONNECTIVITY_SAMPLE_PAIRS:
                    break
            if len(pairs) >= _MAX_CONNECTIVITY_SAMPLE_PAIRS:
                break

        for src, tgt in pairs:
            paths = self.find_disjoint_paths(src, tgt)
            if len(paths) < k:
                logger.debug(
                    "k-connectivity check failed for pair (%s, %s): "
                    "%d paths < k=%d", src, tgt, len(paths), k,
                )
                return False
        return True

    def get_single_points_of_failure(self) -> List[str]:
        """Identify articulation points in the operational topology.

        Uses a DFS-based algorithm to find nodes whose removal would
        disconnect the graph.

        Returns:
            List of node IDs that are single points of failure.
        """
        adj = self._build_adjacency()
        node_list = list(adj.keys())
        if not node_list:
            return []

        disc: Dict[str, int] = {}
        low: Dict[str, int] = {}
        parent: Dict[str, Optional[str]] = {}
        ap_set: Set[str] = set()
        timer = [0]

        def _dfs(u: str) -> None:
            children = 0
            disc[u] = low[u] = timer[0]
            timer[0] += 1

            for v in adj.get(u, []):
                if v not in disc:
                    children += 1
                    parent[v] = u
                    _dfs(v)
                    low[u] = min(low[u], low[v])

                    # u is an AP if it is root with 2+ children
                    if parent[u] is None and children > 1:
                        ap_set.add(u)
                    # u is an AP if not root and low[v] >= disc[u]
                    if parent[u] is not None and low[v] >= disc[u]:
                        ap_set.add(u)
                elif v != parent.get(u):
                    low[u] = min(low[u], disc[v])

        for node in node_list:
            if node not in disc:
                parent[node] = None
                _dfs(node)

        return list(ap_set)

    # ------------------------------------------------------------------
    # Functional layer queries
    # ------------------------------------------------------------------

    def get_layer_subgraph(
        self, layer_type: FunctionalLayerType
    ) -> Tuple[Set[str], Set[str]]:
        """Return the node and link IDs belonging to a functional layer.

        Args:
            layer_type: The functional layer to query.

        Returns:
            Tuple of (node_ids, link_ids) for the layer.
        """
        layer = self.functional_layers.get(layer_type)
        if layer is None:
            return set(), set()
        return set(layer.node_ids), set(layer.link_ids)

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the topology to a plain dictionary.

        Returns:
            Dictionary representation suitable for YAML/JSON export.
        """
        return {
            "topology_id": self.topology_id,
            "nodes": {
                nid: {
                    "node_id": n.node_id,
                    "role": n.role.value,
                    "orbital_layer": n.orbital_layer.value,
                    "position": n.position,
                    "functional_layers": [
                        fl.value for fl in n.functional_layers
                    ],
                    "tsu_id": n.tsu_id,
                    "is_operational": n.is_operational,
                    "capacity_gbps": n.capacity_gbps,
                }
                for nid, n in self.nodes.items()
            },
            "links": {
                lid: {
                    "link_id": lk.link_id,
                    "source_id": lk.source_id,
                    "target_id": lk.target_id,
                    "link_type": lk.link_type.value,
                    "capacity_gbps": lk.capacity_gbps,
                    "latency_ms": lk.latency_ms,
                    "is_active": lk.is_active,
                    "functional_layers": [
                        fl.value for fl in lk.functional_layers
                    ],
                }
                for lid, lk in self.links.items()
            },
            "tsus": {
                tid: {
                    "tsu_id": t.tsu_id,
                    "redundancy_level": t.redundancy_level,
                    "qos_profiles": [
                        {
                            "qos_class": qp.qos_class.value,
                            "max_latency_ms": qp.max_latency_ms,
                            "max_jitter_ms": qp.max_jitter_ms,
                            "min_availability": qp.min_availability,
                            "min_redundant_paths": qp.min_redundant_paths,
                            "priority": qp.priority,
                        }
                        for qp in t.qos_profiles
                    ],
                    "node_ids": t.node_ids,
                    "is_active": t.is_active,
                }
                for tid, t in self.tsus.items()
            },
            "functional_layers": {
                fl_type.value: {
                    "layer_type": fl.layer_type.value,
                    "description": fl.description,
                    "node_ids": sorted(fl.node_ids),
                    "link_ids": sorted(fl.link_ids),
                    "qos_profile": (
                        {
                            "qos_class": fl.qos_profile.qos_class.value,
                            "max_latency_ms": fl.qos_profile.max_latency_ms,
                            "max_jitter_ms": fl.qos_profile.max_jitter_ms,
                            "min_availability": (
                                fl.qos_profile.min_availability
                            ),
                            "min_redundant_paths": (
                                fl.qos_profile.min_redundant_paths
                            ),
                            "priority": fl.qos_profile.priority,
                        }
                        if fl.qos_profile is not None
                        else None
                    ),
                    "encryption_required": fl.encryption_required,
                }
                for fl_type, fl in self.functional_layers.items()
            },
        }
