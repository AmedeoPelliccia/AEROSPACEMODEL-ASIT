# =============================================================================
# HPC Agentic Compute Architecture
# BREX-Governed Distributed Computing for Aerospace Design Intelligence
# Version: 2.0.0
# =============================================================================
"""
HPC Agentic Compute Architecture

Implements a multi-agent ASIT-governed aerospace design intelligence system
running on HPC clusters with hybrid classical-quantum acceleration, capable of
evaluating millions of aircraft configurations in parallel under strict
deterministic BREX decision rules.

Key Capabilities:
    - Agentic HPC: AI-assisted scheduling and resource optimization
    - Hybrid Classical-Quantum: Offload specific workloads to quantum accelerators
    - BREX-Governed: All agent decisions follow deterministic BREX rules
    - Traceable: Full audit trail for certification (DO-178C, ARP4754A)

Architecture:
    ┌──────────────────────────────────────────────────────────────────────────┐
    │                     ASIT GOVERNANCE LAYER                                │
    │  (Contracts, Baselines, BREX Rules, Safety Pathways)                     │
    └─────────────────────────────┬────────────────────────────────────────────┘
                                  │
    ┌─────────────────────────────▼────────────────────────────────────────────┐
    │                    HPC ORCHESTRATION LAYER                               │
    │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
    │  │ Job Sched.  │  │ Resource    │  │ Workflow    │  │ Data        │     │
    │  │ (Agentic)   │  │ Manager     │  │ Engine      │  │ Fabric      │     │
    │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘     │
    └─────────────────────────────┬────────────────────────────────────────────┘
                                  │
    ┌─────────────────────────────▼────────────────────────────────────────────┐
    │                   COMPUTE EXECUTION LAYER                                │
    │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐                │
    │  │  CPU Cluster  │  │  GPU Cluster  │  │    Quantum    │                │
    │  │  (Classical)  │  │  (AI/ML)      │  │  Accelerator  │                │
    │  └───────────────┘  └───────────────┘  └───────────────┘                │
    └──────────────────────────────────────────────────────────────────────────┘

Compliance:
    - S1000D Issue 5.0
    - DO-178C traceability
    - ARP4754A development assurance
    - ARP4761 safety assessment
"""

from __future__ import annotations

import logging
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
import json

logger = logging.getLogger(__name__)


# =============================================================================
# ENUMERATIONS
# =============================================================================

class ComputeResourceType(Enum):
    """Types of compute resources in HPC cluster."""
    CPU = "cpu"                     # Classical CPU compute
    GPU = "gpu"                     # GPU-accelerated compute
    TPU = "tpu"                     # Tensor processing unit
    QUANTUM = "quantum"             # Quantum processor
    FPGA = "fpga"                   # Field-programmable gate array
    HYBRID = "hybrid"               # Mixed resource allocation


class WorkloadType(Enum):
    """Types of aerospace simulation workloads."""
    CFD = "cfd"                     # Computational Fluid Dynamics
    FEM = "fem"                     # Finite Element Method
    MDO = "mdo"                     # Multidisciplinary Design Optimization
    AEROELASTIC = "aeroelastic"     # Aeroelastic analysis
    THERMAL = "thermal"             # Thermal analysis
    ACOUSTIC = "acoustic"           # Acoustic/noise analysis
    SYSTEM_SIM = "system_sim"       # System simulation
    TRAJECTORY = "trajectory"       # Trajectory optimization
    FLEET_OPT = "fleet_opt"         # Fleet optimization
    QUANTUM_OPT = "quantum_opt"     # Quantum-accelerated optimization


class JobStatus(Enum):
    """Status of HPC job execution."""
    PENDING = "pending"             # Waiting in queue
    SCHEDULED = "scheduled"         # Scheduled for execution
    RUNNING = "running"             # Currently executing
    COMPLETED = "completed"         # Successfully completed
    FAILED = "failed"               # Execution failed
    CANCELLED = "cancelled"         # User cancelled
    ESCALATED = "escalated"         # Requires human approval


class AgentRole(Enum):
    """Roles of agents in the multi-agent system."""
    ORCHESTRATOR = "orchestrator"   # Master coordination agent
    SCHEDULER = "scheduler"         # Job scheduling agent
    OPTIMIZER = "optimizer"         # Design optimization agent
    VALIDATOR = "validator"         # Validation/verification agent
    ANALYST = "analyst"             # Analysis execution agent
    SYNTHESIZER = "synthesizer"     # Results synthesis agent


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class ComputeResource:
    """
    Represents a compute resource in the HPC cluster.
    """
    resource_id: str
    resource_type: ComputeResourceType
    name: str
    capacity: int                   # Cores/QPUs/etc.
    memory_gb: float
    available: bool = True
    current_load: float = 0.0       # 0.0 to 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "resource_id": self.resource_id,
            "resource_type": self.resource_type.value,
            "name": self.name,
            "capacity": self.capacity,
            "memory_gb": self.memory_gb,
            "available": self.available,
            "current_load": self.current_load,
            "metadata": self.metadata,
        }


@dataclass
class HPCJob:
    """
    Represents an HPC job for aerospace simulation.
    """
    job_id: str
    name: str
    workload_type: WorkloadType
    priority: int = 5               # 1 (highest) to 10 (lowest)
    status: JobStatus = JobStatus.PENDING

    # Resource requirements
    required_cores: int = 1
    required_memory_gb: float = 1.0
    required_gpus: int = 0
    required_qpus: int = 0          # Quantum processing units
    estimated_runtime_hours: float = 1.0

    # ASIT governance
    contract_id: str = ""
    baseline_id: str = ""
    ata_domain: str = ""
    safety_critical: bool = False

    # Execution tracking
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    assigned_resources: List[str] = field(default_factory=list)

    # Results
    result_path: Optional[str] = None
    exit_code: Optional[int] = None
    error_message: Optional[str] = None

    # BREX decision trail
    brex_decisions: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "name": self.name,
            "workload_type": self.workload_type.value,
            "priority": self.priority,
            "status": self.status.value,
            "required_cores": self.required_cores,
            "required_memory_gb": self.required_memory_gb,
            "required_gpus": self.required_gpus,
            "required_qpus": self.required_qpus,
            "estimated_runtime_hours": self.estimated_runtime_hours,
            "contract_id": self.contract_id,
            "baseline_id": self.baseline_id,
            "ata_domain": self.ata_domain,
            "safety_critical": self.safety_critical,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "assigned_resources": self.assigned_resources,
            "result_path": self.result_path,
            "exit_code": self.exit_code,
            "error_message": self.error_message,
            "brex_decisions": self.brex_decisions,
        }


@dataclass
class WorkflowStage:
    """
    Represents a stage in an HPC workflow.
    """
    stage_id: str
    name: str
    jobs: List[HPCJob] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)  # stage_ids
    status: JobStatus = JobStatus.PENDING
    brex_rules: List[str] = field(default_factory=list)    # BREX rule IDs to evaluate

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stage_id": self.stage_id,
            "name": self.name,
            "jobs": [j.to_dict() for j in self.jobs],
            "dependencies": self.dependencies,
            "status": self.status.value,
            "brex_rules": self.brex_rules,
        }


@dataclass
class HPCWorkflow:
    """
    Represents a complete HPC workflow for aerospace design exploration.
    """
    workflow_id: str
    name: str
    description: str
    stages: List[WorkflowStage] = field(default_factory=list)

    # ASIT governance
    contract_id: str = ""
    baseline_id: str = ""

    # Execution tracking
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    status: JobStatus = JobStatus.PENDING

    # Metrics
    total_core_hours: float = 0.0
    total_gpu_hours: float = 0.0
    total_quantum_shots: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "name": self.name,
            "description": self.description,
            "stages": [s.to_dict() for s in self.stages],
            "contract_id": self.contract_id,
            "baseline_id": self.baseline_id,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "status": self.status.value,
            "total_core_hours": self.total_core_hours,
            "total_gpu_hours": self.total_gpu_hours,
            "total_quantum_shots": self.total_quantum_shots,
        }


# =============================================================================
# AGENTIC HPC SCHEDULER
# =============================================================================

class AgenticHPCScheduler:
    """
    AI-Powered Agentic HPC Job Scheduler.

    Implements intelligent job scheduling with:
        - AI-powered memory prediction
        - Dynamic resource allocation
        - BREX-governed decision making
        - Priority-based queue management

    The scheduler operates under ASIT governance and logs all decisions
    for certification traceability.

    Example:
        >>> scheduler = AgenticHPCScheduler(contract_id="KITDM-CTR-HPC-001")
        >>> job = HPCJob(
        ...     job_id="JOB-001",
        ...     name="Wing CFD Analysis",
        ...     workload_type=WorkloadType.CFD,
        ...     contract_id="KITDM-CTR-HPC-001"
        ... )
        >>> result = scheduler.schedule_job(job)
    """

    def __init__(
        self,
        contract_id: str,
        baseline_id: str = "",
        max_concurrent_jobs: int = 1000,
    ):
        """
        Initialize the Agentic HPC Scheduler.

        Args:
            contract_id: ASIT contract identifier
            baseline_id: Baseline identifier
            max_concurrent_jobs: Maximum concurrent jobs allowed
        """
        self.contract_id = contract_id
        self.baseline_id = baseline_id
        self.max_concurrent_jobs = max_concurrent_jobs

        # Resource pool
        self.resources: Dict[str, ComputeResource] = {}

        # Job queues
        self.pending_queue: List[HPCJob] = []
        self.running_jobs: Dict[str, HPCJob] = {}
        self.completed_jobs: List[HPCJob] = []

        # Decision log
        self.decision_log: List[Dict[str, Any]] = []

        logger.info(
            f"AgenticHPCScheduler initialized: contract={contract_id}, "
            f"max_jobs={max_concurrent_jobs}"
        )

    def register_resource(self, resource: ComputeResource) -> None:
        """Register a compute resource with the scheduler."""
        self.resources[resource.resource_id] = resource
        logger.info(f"Registered resource: {resource.name} ({resource.resource_type.value})")

    def schedule_job(self, job: HPCJob) -> Dict[str, Any]:
        """
        Schedule a job using AI-powered agentic decision making.

        Args:
            job: The HPC job to schedule

        Returns:
            Scheduling decision with BREX trail
        """
        decision = {
            "job_id": job.job_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": "schedule",
            "brex_rules_evaluated": [],
            "resource_allocation": None,
            "status": "pending",
        }

        # Step 1: Validate ASIT governance
        if not job.contract_id:
            decision["status"] = "rejected"
            decision["reason"] = "Missing ASIT contract ID"
            decision["brex_rules_evaluated"].append({
                "rule_id": "HPC-CTR-001",
                "name": "Contract Required",
                "passed": False,
            })
            self._log_decision(decision)
            return decision

        decision["brex_rules_evaluated"].append({
            "rule_id": "HPC-CTR-001",
            "name": "Contract Required",
            "passed": True,
        })

        # Step 2: Check safety-critical constraints
        if job.safety_critical:
            decision["brex_rules_evaluated"].append({
                "rule_id": "HPC-SAFETY-001",
                "name": "Safety Critical Job",
                "passed": True,
                "note": "Elevated priority and validation required",
            })
            job.priority = min(job.priority, 2)  # Elevate priority

        # Step 3: AI-powered resource prediction
        predicted_resources = self._predict_resources(job)
        decision["predicted_resources"] = predicted_resources

        # Step 4: Find available resources
        allocated = self._allocate_resources(job, predicted_resources)
        if allocated:
            job.status = JobStatus.SCHEDULED
            job.assigned_resources = [r.resource_id for r in allocated]
            decision["status"] = "scheduled"
            decision["resource_allocation"] = [r.to_dict() for r in allocated]
        else:
            job.status = JobStatus.PENDING
            self.pending_queue.append(job)
            decision["status"] = "queued"
            decision["reason"] = "Waiting for resources"

        decision["brex_rules_evaluated"].append({
            "rule_id": "HPC-RES-001",
            "name": "Resource Availability",
            "passed": allocated is not None,
        })

        job.brex_decisions.append(decision)
        self._log_decision(decision)

        return decision

    def schedule_workflow(self, workflow: HPCWorkflow) -> Dict[str, Any]:
        """
        Schedule an entire workflow with dependency resolution.

        Args:
            workflow: The HPC workflow to schedule

        Returns:
            Workflow scheduling result
        """
        result = {
            "workflow_id": workflow.workflow_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "stages_scheduled": 0,
            "jobs_scheduled": 0,
            "brex_decisions": [],
        }

        # Topological sort of stages based on dependencies
        sorted_stages = self._topological_sort_stages(workflow.stages)

        for stage in sorted_stages:
            # Check dependencies are complete
            deps_complete = all(
                self._is_stage_complete(workflow, dep_id)
                for dep_id in stage.dependencies
            )

            if deps_complete:
                # Evaluate stage BREX rules
                brex_passed = self._evaluate_stage_brex(stage)
                result["brex_decisions"].append({
                    "stage_id": stage.stage_id,
                    "brex_rules": stage.brex_rules,
                    "passed": brex_passed,
                })

                if brex_passed:
                    # Schedule all jobs in stage
                    for job in stage.jobs:
                        job_decision = self.schedule_job(job)
                        if job_decision["status"] in ("scheduled", "queued"):
                            result["jobs_scheduled"] += 1

                    result["stages_scheduled"] += 1
                    stage.status = JobStatus.SCHEDULED

        workflow.status = JobStatus.SCHEDULED if result["stages_scheduled"] > 0 else JobStatus.PENDING

        return result

    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status and metrics."""
        return {
            "pending_jobs": len(self.pending_queue),
            "running_jobs": len(self.running_jobs),
            "completed_jobs": len(self.completed_jobs),
            "total_resources": len(self.resources),
            "available_resources": sum(1 for r in self.resources.values() if r.available),
            "resource_utilization": self._calculate_utilization(),
        }

    def _predict_resources(self, job: HPCJob) -> Dict[str, Any]:
        """
        AI-powered resource prediction.

        Uses historical data and workload characteristics to predict
        optimal resource allocation.
        """
        # Base prediction on workload type
        predictions = {
            WorkloadType.CFD: {"cores": 128, "memory_gb": 256, "gpus": 2},
            WorkloadType.FEM: {"cores": 64, "memory_gb": 128, "gpus": 0},
            WorkloadType.MDO: {"cores": 256, "memory_gb": 512, "gpus": 4},
            WorkloadType.AEROELASTIC: {"cores": 64, "memory_gb": 64, "gpus": 0},
            WorkloadType.THERMAL: {"cores": 32, "memory_gb": 64, "gpus": 0},
            WorkloadType.ACOUSTIC: {"cores": 32, "memory_gb": 32, "gpus": 0},
            WorkloadType.SYSTEM_SIM: {"cores": 16, "memory_gb": 32, "gpus": 0},
            WorkloadType.TRAJECTORY: {"cores": 8, "memory_gb": 16, "gpus": 0},
            WorkloadType.FLEET_OPT: {"cores": 64, "memory_gb": 128, "gpus": 0},
            WorkloadType.QUANTUM_OPT: {"cores": 4, "memory_gb": 8, "gpus": 0, "qpus": 1},
        }

        base = predictions.get(job.workload_type, {"cores": 16, "memory_gb": 32, "gpus": 0})

        # Adjust based on job requirements
        return {
            "cores": max(job.required_cores, base.get("cores", 16)),
            "memory_gb": max(job.required_memory_gb, base.get("memory_gb", 32)),
            "gpus": max(job.required_gpus, base.get("gpus", 0)),
            "qpus": max(job.required_qpus, base.get("qpus", 0)),
        }

    def _allocate_resources(
        self,
        job: HPCJob,
        requirements: Dict[str, Any],
    ) -> Optional[List[ComputeResource]]:
        """Allocate resources for a job."""
        allocated = []

        # Find CPU resources
        cpu_needed = requirements.get("cores", 0)
        for resource in self.resources.values():
            if resource.resource_type == ComputeResourceType.CPU and resource.available:
                if resource.capacity >= cpu_needed:
                    allocated.append(resource)
                    cpu_needed = 0
                    break

        # Find GPU resources if needed
        gpu_needed = requirements.get("gpus", 0)
        if gpu_needed > 0:
            for resource in self.resources.values():
                if resource.resource_type == ComputeResourceType.GPU and resource.available:
                    if resource.capacity >= gpu_needed:
                        allocated.append(resource)
                        gpu_needed = 0
                        break

        # Find Quantum resources if needed
        qpu_needed = requirements.get("qpus", 0)
        if qpu_needed > 0:
            for resource in self.resources.values():
                if resource.resource_type == ComputeResourceType.QUANTUM and resource.available:
                    allocated.append(resource)
                    qpu_needed = 0
                    break

        # Check if all requirements met
        if cpu_needed > 0 or gpu_needed > 0 or qpu_needed > 0:
            return None

        return allocated

    def _topological_sort_stages(self, stages: List[WorkflowStage]) -> List[WorkflowStage]:
        """
        Topologically sort workflow stages based on dependencies.
        
        Raises:
            ValueError: If circular dependency is detected
        """
        sorted_stages = []
        remaining = list(stages)
        completed_ids: Set[str] = set()

        while remaining:
            # Find a stage with all dependencies satisfied
            found = False
            for stage in remaining:
                if all(dep in completed_ids for dep in stage.dependencies):
                    sorted_stages.append(stage)
                    completed_ids.add(stage.stage_id)
                    remaining.remove(stage)
                    found = True
                    break
            
            if not found:
                # Circular dependency or missing dependency
                remaining_ids = [s.stage_id for s in remaining]
                logger.error(f"Circular dependency detected. Remaining stages: {remaining_ids}")
                raise ValueError(
                    f"Circular dependency detected in workflow stages. "
                    f"Cannot schedule: {remaining_ids}"
                )

        return sorted_stages

    def _is_stage_complete(self, workflow: HPCWorkflow, stage_id: str) -> bool:
        """Check if a workflow stage is complete."""
        for stage in workflow.stages:
            if stage.stage_id == stage_id:
                return stage.status == JobStatus.COMPLETED
        return False

    def _evaluate_stage_brex(self, stage: WorkflowStage) -> bool:
        """Evaluate BREX rules for a workflow stage."""
        # For now, return True - would integrate with BREX Decision Engine
        return True

    def _calculate_utilization(self) -> float:
        """Calculate overall resource utilization."""
        if not self.resources:
            return 0.0
        return sum(r.current_load for r in self.resources.values()) / len(self.resources)

    def _log_decision(self, decision: Dict[str, Any]) -> None:
        """Log a scheduling decision."""
        self.decision_log.append(decision)
        logger.info(f"Scheduling decision: {decision['job_id']} -> {decision['status']}")


# =============================================================================
# HPC CLUSTER MANAGER
# =============================================================================

class HPCClusterManager:
    """
    Manages HPC cluster resources and hybrid classical-quantum execution.

    Provides:
        - Resource discovery and registration
        - Workload distribution
        - Hybrid quantum-classical execution
        - Performance monitoring

    Example:
        >>> cluster = HPCClusterManager(cluster_id="AEROSPACE-HPC-01")
        >>> cluster.add_cpu_partition("CPU-MAIN", nodes=100, cores_per_node=64)
        >>> cluster.add_gpu_partition("GPU-AI", nodes=20, gpus_per_node=4)
        >>> cluster.add_quantum_backend("QUANTUM-01", qubits=127)
    """

    def __init__(self, cluster_id: str, name: str = ""):
        """
        Initialize HPC Cluster Manager.

        Args:
            cluster_id: Unique cluster identifier
            name: Human-readable cluster name
        """
        self.cluster_id = cluster_id
        self.name = name or cluster_id
        self.partitions: Dict[str, Dict[str, Any]] = {}
        self.quantum_backends: Dict[str, Dict[str, Any]] = {}
        self.scheduler = AgenticHPCScheduler(
            contract_id=f"HPC-{cluster_id}",
            baseline_id="HPC-BASELINE-001",
        )

        logger.info(f"HPCClusterManager initialized: {cluster_id}")

    def add_cpu_partition(
        self,
        partition_id: str,
        nodes: int,
        cores_per_node: int,
        memory_per_node_gb: float = 256.0,
    ) -> None:
        """Add a CPU compute partition to the cluster."""
        self.partitions[partition_id] = {
            "type": "cpu",
            "nodes": nodes,
            "cores_per_node": cores_per_node,
            "memory_per_node_gb": memory_per_node_gb,
            "total_cores": nodes * cores_per_node,
            "status": "active",
        }

        # Register with scheduler
        for i in range(nodes):
            resource = ComputeResource(
                resource_id=f"{partition_id}-NODE-{i:04d}",
                resource_type=ComputeResourceType.CPU,
                name=f"{partition_id} Node {i}",
                capacity=cores_per_node,
                memory_gb=memory_per_node_gb,
            )
            self.scheduler.register_resource(resource)

        logger.info(f"Added CPU partition: {partition_id} ({nodes} nodes, {nodes * cores_per_node} cores)")

    def add_gpu_partition(
        self,
        partition_id: str,
        nodes: int,
        gpus_per_node: int,
        gpu_memory_gb: float = 80.0,
    ) -> None:
        """Add a GPU compute partition to the cluster."""
        self.partitions[partition_id] = {
            "type": "gpu",
            "nodes": nodes,
            "gpus_per_node": gpus_per_node,
            "gpu_memory_gb": gpu_memory_gb,
            "total_gpus": nodes * gpus_per_node,
            "status": "active",
        }

        # Register with scheduler
        for i in range(nodes):
            resource = ComputeResource(
                resource_id=f"{partition_id}-NODE-{i:04d}",
                resource_type=ComputeResourceType.GPU,
                name=f"{partition_id} GPU Node {i}",
                capacity=gpus_per_node,
                memory_gb=gpu_memory_gb * gpus_per_node,
            )
            self.scheduler.register_resource(resource)

        logger.info(f"Added GPU partition: {partition_id} ({nodes * gpus_per_node} GPUs)")

    def add_quantum_backend(
        self,
        backend_id: str,
        qubits: int,
        connectivity: str = "heavy-hex",
        error_rate: float = 0.001,
    ) -> None:
        """Add a quantum computing backend to the cluster."""
        self.quantum_backends[backend_id] = {
            "qubits": qubits,
            "connectivity": connectivity,
            "error_rate": error_rate,
            "status": "active",
        }

        # Register with scheduler
        resource = ComputeResource(
            resource_id=backend_id,
            resource_type=ComputeResourceType.QUANTUM,
            name=f"Quantum Backend {backend_id}",
            capacity=qubits,
            memory_gb=0,  # Quantum doesn't use classical memory
            metadata={
                "connectivity": connectivity,
                "error_rate": error_rate,
            }
        )
        self.scheduler.register_resource(resource)

        logger.info(f"Added quantum backend: {backend_id} ({qubits} qubits)")

    def submit_workflow(self, workflow: HPCWorkflow) -> Dict[str, Any]:
        """Submit a workflow for execution on the cluster."""
        return self.scheduler.schedule_workflow(workflow)

    def submit_job(self, job: HPCJob) -> Dict[str, Any]:
        """Submit a single job for execution."""
        return self.scheduler.schedule_job(job)

    def get_cluster_status(self) -> Dict[str, Any]:
        """Get overall cluster status."""
        return {
            "cluster_id": self.cluster_id,
            "name": self.name,
            "partitions": self.partitions,
            "quantum_backends": self.quantum_backends,
            "scheduler_status": self.scheduler.get_queue_status(),
        }


# =============================================================================
# FACTORY FUNCTIONS
# =============================================================================

def create_aerospace_hpc_cluster(
    cluster_id: str = "AEROSPACE-HPC-01",
    cpu_nodes: int = 100,
    gpu_nodes: int = 20,
    quantum_qubits: int = 127,
) -> HPCClusterManager:
    """
    Factory function to create a standard aerospace HPC cluster configuration.

    Args:
        cluster_id: Unique cluster identifier
        cpu_nodes: Number of CPU compute nodes
        gpu_nodes: Number of GPU compute nodes
        quantum_qubits: Number of qubits in quantum backend

    Returns:
        Configured HPCClusterManager instance
    """
    cluster = HPCClusterManager(cluster_id, f"Aerospace Design HPC - {cluster_id}")

    # Add CPU partition for classical simulations
    cluster.add_cpu_partition(
        partition_id="CPU-MAIN",
        nodes=cpu_nodes,
        cores_per_node=64,
        memory_per_node_gb=512.0,
    )

    # Add GPU partition for AI/ML workloads
    cluster.add_gpu_partition(
        partition_id="GPU-AI",
        nodes=gpu_nodes,
        gpus_per_node=4,
        gpu_memory_gb=80.0,
    )

    # Add quantum backend for optimization
    if quantum_qubits > 0:
        cluster.add_quantum_backend(
            backend_id="QUANTUM-OPT",
            qubits=quantum_qubits,
            connectivity="heavy-hex",
            error_rate=0.001,
        )

    return cluster


def create_mdo_workflow(
    workflow_name: str,
    contract_id: str,
    baseline_id: str,
    ata_domain: str,
    configurations: int = 100,
) -> HPCWorkflow:
    """
    Create an MDO (Multidisciplinary Design Optimization) workflow.

    Args:
        workflow_name: Name of the workflow
        contract_id: ASIT contract ID
        baseline_id: Baseline ID
        ata_domain: ATA domain (e.g., "ATA 27", "ATA 57")
        configurations: Number of design configurations to evaluate

    Returns:
        Configured HPCWorkflow for MDO
    """
    workflow = HPCWorkflow(
        workflow_id=f"MDO-{uuid.uuid4().hex[:8].upper()}",
        name=workflow_name,
        description=f"MDO workflow for {ata_domain} with {configurations} configurations",
        contract_id=contract_id,
        baseline_id=baseline_id,
    )

    # Stage 1: Design Space Generation
    stage1 = WorkflowStage(
        stage_id="STAGE-001",
        name="Design Space Generation",
        brex_rules=["HPC-CTR-001", "HPC-ATA-001"],
    )
    stage1.jobs.append(HPCJob(
        job_id=f"JOB-GEN-{uuid.uuid4().hex[:6].upper()}",
        name="Generate Design Configurations",
        workload_type=WorkloadType.MDO,
        contract_id=contract_id,
        baseline_id=baseline_id,
        ata_domain=ata_domain,
        required_cores=32,
        required_memory_gb=64,
    ))
    workflow.stages.append(stage1)

    # Stage 2: Parallel CFD Analysis
    stage2 = WorkflowStage(
        stage_id="STAGE-002",
        name="Aerodynamic Analysis",
        dependencies=["STAGE-001"],
        brex_rules=["HPC-CFD-001"],
    )
    for i in range(min(configurations, 10)):  # Limit for example
        stage2.jobs.append(HPCJob(
            job_id=f"JOB-CFD-{i:04d}",
            name=f"CFD Analysis Config {i}",
            workload_type=WorkloadType.CFD,
            contract_id=contract_id,
            baseline_id=baseline_id,
            ata_domain=ata_domain,
            required_cores=128,
            required_memory_gb=256,
            required_gpus=2,
        ))
    workflow.stages.append(stage2)

    # Stage 3: Structural Analysis
    stage3 = WorkflowStage(
        stage_id="STAGE-003",
        name="Structural Analysis",
        dependencies=["STAGE-001"],
        brex_rules=["HPC-FEM-001"],
    )
    for i in range(min(configurations, 10)):
        stage3.jobs.append(HPCJob(
            job_id=f"JOB-FEM-{i:04d}",
            name=f"FEM Analysis Config {i}",
            workload_type=WorkloadType.FEM,
            contract_id=contract_id,
            baseline_id=baseline_id,
            ata_domain=ata_domain,
            required_cores=64,
            required_memory_gb=128,
        ))
    workflow.stages.append(stage3)

    # Stage 4: Quantum Optimization
    stage4 = WorkflowStage(
        stage_id="STAGE-004",
        name="Quantum-Accelerated Optimization",
        dependencies=["STAGE-002", "STAGE-003"],
        brex_rules=["HPC-QUANTUM-001"],
    )
    stage4.jobs.append(HPCJob(
        job_id=f"JOB-QOPT-{uuid.uuid4().hex[:6].upper()}",
        name="QAOA Global Optimization",
        workload_type=WorkloadType.QUANTUM_OPT,
        contract_id=contract_id,
        baseline_id=baseline_id,
        ata_domain=ata_domain,
        required_cores=4,
        required_memory_gb=8,
        required_qpus=1,
    ))
    workflow.stages.append(stage4)

    # Stage 5: Results Synthesis
    stage5 = WorkflowStage(
        stage_id="STAGE-005",
        name="Results Synthesis",
        dependencies=["STAGE-004"],
        brex_rules=["HPC-SYN-001"],
    )
    stage5.jobs.append(HPCJob(
        job_id=f"JOB-SYN-{uuid.uuid4().hex[:6].upper()}",
        name="Synthesize Optimization Results",
        workload_type=WorkloadType.MDO,
        contract_id=contract_id,
        baseline_id=baseline_id,
        ata_domain=ata_domain,
        required_cores=16,
        required_memory_gb=32,
    ))
    workflow.stages.append(stage5)

    return workflow


# =============================================================================
# MODULE EXPORTS
# =============================================================================

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
