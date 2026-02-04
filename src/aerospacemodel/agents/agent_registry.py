"""
Agent Registry - Registration and factory pattern for agents

Provides a registry for discovering and instantiating lifecycle agents.
"""

from typing import Dict, List, Any, Optional, Type
import logging
from pathlib import Path

from .lifecycle_agent import LifecycleAgent, AgentConfiguration, create_agent_from_yaml

logger = logging.getLogger(__name__)


class AgentRegistry:
    """
    Registry for CNOT-gate lifecycle agents.
    
    Allows registration, discovery, and instantiation of agents.
    """
    
    def __init__(self):
        self._agents: Dict[str, AgentConfiguration] = {}
        self._agent_instances: Dict[str, LifecycleAgent] = {}
    
    def register(
        self,
        agent_id: str,
        config: AgentConfiguration
    ) -> None:
        """
        Register an agent configuration.
        
        Args:
            agent_id: Unique agent identifier
            config: Agent configuration
        """
        if agent_id in self._agents:
            logger.warning(f"Agent {agent_id} already registered, overwriting")
        
        self._agents[agent_id] = config
        logger.info(f"Registered agent: {agent_id} ({config.agent_name})")
    
    def register_from_yaml(self, yaml_path: str) -> str:
        """
        Register an agent from YAML configuration file.
        
        Args:
            yaml_path: Path to YAML configuration
        
        Returns:
            Agent ID
        """
        agent = create_agent_from_yaml(yaml_path)
        agent_id = agent.config.agent_id
        
        self.register(agent_id, agent.config)
        self._agent_instances[agent_id] = agent
        
        return agent_id
    
    def register_directory(self, directory: str) -> List[str]:
        """
        Register all agents in a directory.
        
        Args:
            directory: Directory path containing agent YAML files
        
        Returns:
            List of registered agent IDs
        """
        dir_path = Path(directory)
        
        if not dir_path.exists():
            logger.error(f"Directory not found: {directory}")
            return []
        
        agent_ids = []
        
        for yaml_file in dir_path.glob("*.yaml"):
            try:
                agent_id = self.register_from_yaml(str(yaml_file))
                agent_ids.append(agent_id)
            except Exception as e:
                logger.error(f"Failed to register agent from {yaml_file}: {e}")
        
        logger.info(f"Registered {len(agent_ids)} agents from {directory}")
        return agent_ids
    
    def get(self, agent_id: str) -> Optional[LifecycleAgent]:
        """
        Get an agent instance.
        
        Args:
            agent_id: Agent identifier
        
        Returns:
            LifecycleAgent instance or None
        """
        if agent_id in self._agent_instances:
            return self._agent_instances[agent_id]
        
        if agent_id in self._agents:
            # Create instance from configuration
            config = self._agents[agent_id]
            agent = LifecycleAgent(config)
            self._agent_instances[agent_id] = agent
            return agent
        
        logger.error(f"Agent not found: {agent_id}")
        return None
    
    def list(self) -> List[str]:
        """List all registered agent IDs."""
        return list(self._agents.keys())
    
    def list_by_transition(self, transition: str) -> List[str]:
        """
        List agents for a specific lifecycle transition.
        
        Args:
            transition: Lifecycle transition name
        
        Returns:
            List of agent IDs
        """
        return [
            agent_id
            for agent_id, config in self._agents.items()
            if config.lifecycle_transition.value == transition
        ]
    
    def get_info(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Get agent information.
        
        Args:
            agent_id: Agent identifier
        
        Returns:
            Agent information dict or None
        """
        if agent_id not in self._agents:
            return None
        
        config = self._agents[agent_id]
        
        return {
            "agent_id": config.agent_id,
            "agent_name": config.agent_name,
            "description": config.description,
            "lifecycle_transition": config.lifecycle_transition.value,
            "num_gates": len(config.gates),
            "num_actions": len(config.actions)
        }


# Global registry instance
_global_registry = AgentRegistry()


def register_agent(agent_id: str, config: AgentConfiguration) -> None:
    """Register an agent in the global registry."""
    _global_registry.register(agent_id, config)


def get_agent(agent_id: str) -> Optional[LifecycleAgent]:
    """Get an agent from the global registry."""
    return _global_registry.get(agent_id)


def list_agents() -> List[str]:
    """List all agents in the global registry."""
    return _global_registry.list()


def get_registry() -> AgentRegistry:
    """Get the global registry instance."""
    return _global_registry
