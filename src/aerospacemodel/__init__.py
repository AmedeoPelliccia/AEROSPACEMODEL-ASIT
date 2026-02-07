"""
AEROSPACEMODEL
==============

ASIT + ASIGT: Aircraft Systems Information Transponders

Transform governed aerospace engineering knowledge into
industry-standard technical publications.

Architecture:
    - ASIT: Aircraft Systems Information Transponder
            Governance, structure, lifecycle authority
    - ASIGT: Aircraft Systems Information Generative Transponder
             Content generation under ASIT control
    - Topology: 3D mesh topology for governed satellite constellations
    - Data Lifecycle: End-to-end data flow management
    - Layers: Functional layers (ATM/CNS, Military, Ground, Core Mission)
    - Cognitive: Distributed model field (emergent intelligence)
    - Framework: Unified 3-axis cube (lifecycle × topology × domains)

Quick Start:
    >>> from aerospacemodel import ASIT, ASIGT, Contract
    >>>
    >>> # ASIT governs
    >>> asit = ASIT(config_path="ASIT/config/asit_config.yaml")
    >>> contract = Contract.load("ASIT/CONTRACTS/active/KITDM-CTR-LM-CSDB_ATA28.yaml")
    >>>
    >>> # ASIGT executes under ASIT control
    >>> asigt = ASIGT(asit_instance=asit)
    >>> result = asigt.execute(contract, baseline="FBL-2026-Q1-003")
    >>>
    >>> if result.success:
    ...     print(f"Generated {result.output_count} artifacts")
    ...     print(f"Trace coverage: {result.trace_coverage}%")

CLI Usage:
    $ aerospacemodel init --program "MyAircraft" --model-code "MA"
    $ aerospacemodel run --contract KITDM-CTR-LM-CSDB_ATA28
    $ aerospacemodel validate --contract KITDM-CTR-LM-CSDB_ATA28

Constraint:
    ASIGT cannot operate standalone. It executes ONLY through
    ASIT contracts, baselines, and governance rules.

Documentation:
    https://docs.aerospacemodel.io

License:
    Apache License 2.0

Copyright:
    2024-2026 AEROSPACEMODEL Contributors
"""

__version__ = "2.0.0"
__author__ = "AEROSPACEMODEL Contributors"
__license__ = "Apache-2.0"

# ═══════════════════════════════════════════════════════════════════════════
# ASIT — Governance Authority Layer
# ═══════════════════════════════════════════════════════════════════════════

from aerospacemodel.asit import (
    ASIT,
    Contract,
    ContractStatus,
    Baseline,
    BaselineType,
    Governance,
    ChangeRequest,
    ChangeOrder,
)

# ═══════════════════════════════════════════════════════════════════════════
# ASIGT — Content Generation Layer (ASIT-controlled)
# ═══════════════════════════════════════════════════════════════════════════

from aerospacemodel.asigt import (
    ASIGT,
    RunResult,
    RunStatus,
    ValidationReport,
    TraceMatrix,
)

# ═══════════════════════════════════════════════════════════════════════════
# TOPOLOGY — 3D Mesh Constellation Layer
# ═══════════════════════════════════════════════════════════════════════════

from aerospacemodel.topology import (
    Mesh3DTopology,
    MeshNode,
    MeshLink,
    TopologicalServiceUnit,
    FunctionalLayerType,
    OrbitalLayer,
    LinkType,
    NodeRole,
    QoSClass,
    QoSProfile,
)

# ═══════════════════════════════════════════════════════════════════════════
# DATA LIFECYCLE — End-to-end Data Flow Management
# ═══════════════════════════════════════════════════════════════════════════

from aerospacemodel.data_lifecycle import (
    DataLifecycleManager,
    DataRecord,
    DataClassification,
    LifecycleStage,
    DataClass,
    SecurityDomain,
    DataOriginType,
    ConsumptionAction,
    ProcessingLocation,
)

# ═══════════════════════════════════════════════════════════════════════════
# FUNCTIONAL LAYERS — ATM/CNS, Military, Ground, Core Mission
# ═══════════════════════════════════════════════════════════════════════════

from aerospacemodel.layers import (
    FunctionalLayerStack,
    ATMLayer,
    MilitarySecurityLayer,
    GroundBasedLayer,
    CoreMissionLayer,
)

# ═══════════════════════════════════════════════════════════════════════════
# COGNITIVE — Distributed Model Field
# ═══════════════════════════════════════════════════════════════════════════

from aerospacemodel.cognitive import (
    DistributedModelField,
    MicroModel,
    FoundationModel,
    FederatedSession,
    ModelCapability,
    ModelTier,
    GovernanceRole,
)

# ═══════════════════════════════════════════════════════════════════════════
# FRAMEWORK — Unified 3-Axis Cube
# ═══════════════════════════════════════════════════════════════════════════

from aerospacemodel.framework import (
    UnifiedFramework,
    CubeCell,
    ServiceProfile,
    SecurityProfile,
    ModelRole,
)

# ═══════════════════════════════════════════════════════════════════════════
# EXCEPTIONS
# ═══════════════════════════════════════════════════════════════════════════

from aerospacemodel.exceptions import (
    AerospaceModelError,
    ASITError,
    ASIGTError,
    ContractError,
    BaselineError,
    ValidationError,
    TraceError,
)

# ═══════════════════════════════════════════════════════════════════════════
# PUBLIC API
# ═══════════════════════════════════════════════════════════════════════════

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__license__",

    # ASIT (Governance)
    "ASIT",
    "Contract",
    "ContractStatus",
    "Baseline",
    "BaselineType",
    "Governance",
    "ChangeRequest",
    "ChangeOrder",

    # ASIGT (Generation)
    "ASIGT",
    "RunResult",
    "RunStatus",
    "ValidationReport",
    "TraceMatrix",

    # Topology (3D Mesh)
    "Mesh3DTopology",
    "MeshNode",
    "MeshLink",
    "TopologicalServiceUnit",
    "FunctionalLayerType",
    "OrbitalLayer",
    "LinkType",
    "NodeRole",
    "QoSClass",
    "QoSProfile",

    # Data Lifecycle
    "DataLifecycleManager",
    "DataRecord",
    "DataClassification",
    "LifecycleStage",
    "DataClass",
    "SecurityDomain",
    "DataOriginType",
    "ConsumptionAction",
    "ProcessingLocation",

    # Functional Layers
    "FunctionalLayerStack",
    "ATMLayer",
    "MilitarySecurityLayer",
    "GroundBasedLayer",
    "CoreMissionLayer",

    # Cognitive (Distributed Models)
    "DistributedModelField",
    "MicroModel",
    "FoundationModel",
    "FederatedSession",
    "ModelCapability",
    "ModelTier",
    "GovernanceRole",

    # Framework (Unified Cube)
    "UnifiedFramework",
    "CubeCell",
    "ServiceProfile",
    "SecurityProfile",
    "ModelRole",

    # Exceptions
    "AerospaceModelError",
    "ASITError",
    "ASIGTError",
    "ContractError",
    "BaselineError",
    "ValidationError",
    "TraceError",
]


def get_version() -> str:
    """Return the AEROSPACEMODEL version string."""
    return __version__
