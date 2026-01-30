# =============================================================================
# ASIGT HPC Module
# HPC Agentic Compute Architecture for Aerospace Design
# =============================================================================
"""
HPC Module for ASIGT (Aerospace System Information Generation Tool)

Provides HPC cluster management and agentic scheduling capabilities:
    - AgenticHPCScheduler: AI-powered job scheduling
    - HPCClusterManager: Cluster resource management
    - HPCJob/HPCWorkflow: Job and workflow definitions

Example:
    >>> from ASIGT.hpc import create_aerospace_hpc_cluster
    >>> cluster = create_aerospace_hpc_cluster("AEROSPACE-HPC-01")
    >>> job = HPCJob(
    ...     job_id="JOB-001",
    ...     name="Wing CFD",
    ...     workload_type=WorkloadType.CFD,
    ...     contract_id="KITDM-CTR-HPC-001"
    ... )
    >>> result = cluster.submit_job(job)
"""

from .hpc_compute_architecture import (
    # Enumerations
    ComputeResourceType,
    WorkloadType,
    JobStatus,
    AgentRole,

    # Data classes
    ComputeResource,
    HPCJob,
    WorkflowStage,
    HPCWorkflow,

    # Core classes
    AgenticHPCScheduler,
    HPCClusterManager,

    # Factory functions
    create_aerospace_hpc_cluster,
    create_mdo_workflow,
)

__all__ = [
    # Enumerations
    "ComputeResourceType",
    "WorkloadType",
    "JobStatus",
    "AgentRole",

    # Data classes
    "ComputeResource",
    "HPCJob",
    "WorkflowStage",
    "HPCWorkflow",

    # Core classes
    "AgenticHPCScheduler",
    "HPCClusterManager",

    # Factory functions
    "create_aerospace_hpc_cluster",
    "create_mdo_workflow",
]
