"""
AEROSPACEMODEL Agents Module

Implements CNOT-gate agents for lifecycle simulation and orchestration.
Integrates GitHub Marketplace actions with internal AEROSPACEMODEL components.

Components:
    - lifecycle_agent: Core lifecycle transition agent implementation
    - marketplace_agent: GitHub Marketplace action integration
    - agent_registry: Agent registration and factory pattern
"""

from .lifecycle_agent import (
    LifecycleAgent,
    AgentConfiguration,
    AgentAction,
    LifecycleTransition,
    create_agent_from_yaml,
)

from .marketplace_agent import (
    MarketplaceAgent,
    MarketplaceActionResult,
    MarketplaceActionCategory,
    execute_marketplace_action,
)

from .agent_registry import (
    AgentRegistry,
    register_agent,
    get_agent,
    list_agents,
    get_registry,
)

__all__ = [
    # Lifecycle Agent
    "LifecycleAgent",
    "AgentConfiguration",
    "AgentAction",
    "LifecycleTransition",
    "create_agent_from_yaml",
    
    # Marketplace Agent
    "MarketplaceAgent",
    "MarketplaceActionResult",
    "MarketplaceActionCategory",
    "execute_marketplace_action",
    
    # Agent Registry
    "AgentRegistry",
    "register_agent",
    "get_agent",
    "list_agents",
    "get_registry",
]

__version__ = "2.0.0"
