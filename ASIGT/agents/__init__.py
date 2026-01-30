# =============================================================================
# ASIGT Agents Module
# Multi-Agent MDO Swarm for Aerospace Design Optimization
# =============================================================================
"""
Agents Module for ASIGT (Aerospace System Information Generation Tool)

Provides multi-agent MDO (Multidisciplinary Design Optimization) capabilities:
    - MDOSwarmOrchestrator: Coordinates multi-agent swarm
    - Specialized agents: Aerodynamics, Structures, Propulsion, etc.
    - Pareto front construction and optimization

Example:
    >>> from ASIGT.agents import create_aircraft_mdo_swarm
    >>> swarm = create_aircraft_mdo_swarm(
    ...     swarm_id="MDO-SWARM-001",
    ...     contract_id="KITDM-CTR-MDO-001"
    ... )
    >>> result = swarm.run_optimization(
    ...     objectives=[OptimizationObjective.MAXIMIZE_L_D],
    ...     constraints=[],
    ...     generations=100
    ... )
"""

from .mdo_agent_swarm import (
    # Enumerations
    AgentType,
    OptimizationObjective,
    DesignDomain,
    ConstraintType,

    # Data classes
    DesignVariable,
    DesignConstraint,
    DesignConfiguration,
    AgentDecision,

    # Base class
    MDOAgent,

    # Specialized agents
    AerodynamicsAgent,
    StructuresAgent,
    PropulsionAgent,

    # Orchestrator
    MDOSwarmOrchestrator,

    # Factory functions
    create_aircraft_mdo_swarm,
    create_standard_design_variables,
)

__all__ = [
    # Enumerations
    "AgentType",
    "OptimizationObjective",
    "DesignDomain",
    "ConstraintType",

    # Data classes
    "DesignVariable",
    "DesignConstraint",
    "DesignConfiguration",
    "AgentDecision",

    # Base class
    "MDOAgent",

    # Specialized agents
    "AerodynamicsAgent",
    "StructuresAgent",
    "PropulsionAgent",

    # Orchestrator
    "MDOSwarmOrchestrator",

    # Factory functions
    "create_aircraft_mdo_swarm",
    "create_standard_design_variables",
]
