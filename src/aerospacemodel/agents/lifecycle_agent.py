"""
Lifecycle Agent - CNOT-gate agent for lifecycle transitions

Orchestrates gates and actions for aerospace component lifecycle management.
Implements the agent pattern described in CNOT_AGENT_LIFECYCLE_ARCHITECTURE.md
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import logging

from aerospacemodel.cnot import CNOTChain, ChainResult
from aerospacemodel.cnot.gates import (
    ContractGate, BaselineGate, AuthorityGate,
    BREXGate, TraceGate, SafetyGate
)

logger = logging.getLogger(__name__)


class LifecycleTransition(Enum):
    """Lifecycle transition types."""
    DESIGN_TO_VERIFICATION = "design_to_verification"
    VERIFICATION_TO_CERTIFICATION = "verification_to_certification"
    CERTIFICATION_TO_PRODUCTION = "certification_to_production"
    PRODUCTION_TO_OPERATION = "production_to_operation"
    OPERATION_TO_MAINTENANCE = "operation_to_maintenance"
    MAINTENANCE_TO_OPERATION = "maintenance_to_operation"


@dataclass
class AgentAction:
    """Represents an action to be executed by an agent."""
    name: str
    action_type: str  # "marketplace" or "internal"
    action_source: str  # GitHub action name or Python module path
    params: Dict[str, Any]
    outputs: Dict[str, str]


@dataclass
class AgentConfiguration:
    """Configuration for a CNOT-gate lifecycle agent."""
    agent_id: str
    agent_name: str
    description: str
    lifecycle_transition: LifecycleTransition
    
    # CNOT gates to execute
    gates: List[Dict[str, Any]]
    
    # Actions to execute after gates pass
    actions: List[AgentAction]
    
    # Output configuration
    outputs: Dict[str, Any]
    
    # Governance configuration
    governance: Dict[str, Any]


class LifecycleAgent:
    """
    CNOT-gate agent for lifecycle transitions.
    
    Orchestrates gates and actions for aerospace component lifecycle management.
    """
    
    def __init__(self, config: AgentConfiguration):
        self.config = config
        self.cnot_chain = self._build_cnot_chain()
        self.execution_id: Optional[str] = None
    
    def _build_cnot_chain(self) -> CNOTChain:
        """Build CNOT chain from agent configuration."""
        chain = CNOTChain(chain_id=self.config.agent_id)
        
        for gate_config in self.config.gates:
            gate = self._create_gate(gate_config)
            if gate:
                chain.add_gate(gate)
        
        return chain
    
    def _create_gate(self, gate_config: Dict[str, Any]):
        """Create gate instance from configuration."""
        gate_type = gate_config.get("type")
        
        if gate_type == "ContractGate":
            return ContractGate(contract_id=gate_config.get("contract_id"))
        
        elif gate_type == "BaselineGate":
            return BaselineGate(baseline_id=gate_config.get("baseline_id"))
        
        elif gate_type == "AuthorityGate":
            return AuthorityGate(
                required_authority=gate_config.get("required_authority")
            )
        
        elif gate_type == "BREXGate":
            return BREXGate(config=gate_config.get("config", {}))
        
        elif gate_type == "TraceGate":
            return TraceGate(config=gate_config.get("config", {}))
        
        elif gate_type == "SafetyGate":
            return SafetyGate(config=gate_config.get("config", {}))
        
        return None
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the lifecycle agent.
        
        Args:
            context: Execution context including component info, environment, etc.
        
        Returns:
            Agent execution result with artifacts and provenance
        """
        self.execution_id = f"EXEC-{self.config.agent_id}-{datetime.utcnow().isoformat()}"
        
        logger.info(f"Starting agent execution: {self.execution_id}")
        logger.info(f"Agent: {self.config.agent_name}")
        logger.info(f"Transition: {self.config.lifecycle_transition.value}")
        
        # Execute CNOT gate chain
        chain_result = self.cnot_chain.execute(context)
        
        if not chain_result.success:
            logger.warning(f"Agent execution blocked by gate: {chain_result.blocked_by}")
            return {
                "success": False,
                "execution_id": self.execution_id,
                "blocked_by": chain_result.blocked_by,
                "gate_results": [
                    {
                        "gate": gr.gate_name,
                        "passed": gr.passed,
                        "message": gr.message
                    }
                    for gr in chain_result.gate_results
                ]
            }
        
        logger.info("All gates passed - executing actions")
        
        # All gates passed - execute actions
        action_results = self._execute_actions(context)
        
        # Generate provenance
        provenance = self._generate_provenance(
            chain_result, action_results, context
        )
        
        logger.info(f"Agent execution completed: {self.execution_id}")
        
        # Package outputs
        return {
            "success": True,
            "execution_id": self.execution_id,
            "agent_id": self.config.agent_id,
            "lifecycle_transition": self.config.lifecycle_transition.value,
            "gate_results": [
                {
                    "gate": gr.gate_name,
                    "passed": gr.passed,
                    "message": gr.message
                }
                for gr in chain_result.gate_results
            ],
            "action_results": action_results,
            "provenance": provenance,
            "artifacts": self._collect_artifacts(action_results),
            "state_update": self.config.outputs.get("state_update", {})
        }
    
    def _execute_actions(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute configured actions."""
        results = []
        
        for action in self.config.actions:
            logger.info(f"Executing action: {action.name} ({action.action_type})")
            
            if action.action_type == "marketplace":
                result = self._execute_marketplace_action(action, context)
            elif action.action_type == "internal":
                result = self._execute_internal_action(action, context)
            else:
                result = {"error": f"Unknown action type: {action.action_type}"}
                logger.error(f"Unknown action type: {action.action_type}")
            
            results.append({
                "action_name": action.name,
                "action_type": action.action_type,
                **result
            })
        
        return results
    
    def _execute_marketplace_action(
        self, action: AgentAction, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a GitHub Marketplace action.
        
        Note: In GitHub Actions environment, this would trigger the action.
        In Python environment, this logs the action to be executed.
        """
        logger.info(f"Marketplace action queued: {action.action_source}")
        
        return {
            "status": "queued",
            "action": action.action_source,
            "params": action.params,
            "message": f"Marketplace action {action.name} queued for execution",
            "outputs": action.outputs
        }
    
    def _execute_internal_action(
        self, action: AgentAction, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute an internal Python action.
        
        Security: Only allows execution of pre-approved internal actions.
        """
        # Allowlist of approved internal action modules
        APPROVED_MODULES = [
            "aerospacemodel.asigt.validators",
            "aerospacemodel.asit",
        ]
        
        try:
            # Dynamic import and execution
            module_path, method_name = action.action_source.rsplit(".", 1)
            
            # Security check: verify module is in allowlist
            is_approved = any(
                module_path.startswith(approved) for approved in APPROVED_MODULES
            )
            if not is_approved:
                raise ValueError(
                    f"Internal action module '{module_path}' is not in the approved list. "
                    f"Approved modules: {APPROVED_MODULES}"
                )
            
            module = __import__(module_path, fromlist=[method_name])
            method = getattr(module, method_name)
            
            logger.info(f"Executing internal action: {module_path}.{method_name}")
            result = method(context=context, **action.params)
            
            return {
                "status": "success",
                "result": result,
                "outputs": action.outputs
            }
        except Exception as e:
            logger.error(f"Internal action failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _generate_provenance(
        self, chain_result: ChainResult, action_results: List[Dict], context: Dict
    ) -> Dict[str, Any]:
        """Generate provenance vector for agent execution."""
        timestamp = datetime.utcnow().isoformat()
        
        return {
            "vector_id": f"PV-{self.config.agent_id}-{timestamp}",
            "execution_id": self.execution_id,
            "agent_id": self.config.agent_id,
            "agent_name": self.config.agent_name,
            "lifecycle_transition": self.config.lifecycle_transition.value,
            "timestamp": timestamp,
            "gate_decisions": [
                {
                    "gate_id": gr.gate_id if hasattr(gr, 'gate_id') else gr.gate_name,
                    "gate_name": gr.gate_name,
                    "passed": gr.passed,
                    "timestamp": timestamp
                }
                for gr in chain_result.gate_results
            ],
            "actions_executed": [
                {
                    "action": ar["action_name"],
                    "action_type": ar["action_type"],
                    "status": ar.get("status", "unknown")
                }
                for ar in action_results
            ],
            "source_artifacts": context.get("source_artifacts", []),
            "transformation_contract": context.get("contract", {}).get("contract_id"),
            "execution_context": {
                "component": context.get("component_id"),
                "baseline": context.get("baseline", {}).get("baseline_id"),
                "authority": context.get("execution_authority")
            }
        }
    
    def _collect_artifacts(self, action_results: List[Dict]) -> List[Dict[str, str]]:
        """Collect artifacts from action results."""
        artifacts = []
        
        for result in action_results:
            if "outputs" in result:
                for output_name, output_path in result["outputs"].items():
                    artifacts.append({
                        "name": output_name,
                        "path": output_path,
                        "action": result["action_name"]
                    })
        
        return artifacts


def create_agent_from_yaml(yaml_path: str) -> LifecycleAgent:
    """
    Create a lifecycle agent from YAML configuration.
    
    Args:
        yaml_path: Path to agent configuration YAML
    
    Returns:
        Configured LifecycleAgent instance
    """
    import yaml
    
    with open(yaml_path, 'r') as f:
        config_dict = yaml.safe_load(f)
    
    # Parse configuration
    agent_config = config_dict["cnot_agent"]
    
    # Parse lifecycle transition
    from_state = agent_config["lifecycle_transition"]["from"]
    to_state = agent_config["lifecycle_transition"]["to"]
    transition_name = f"{from_state}_to_{to_state}"
    
    # Build actions list, preserving the source of each action (marketplace vs internal)
    actions: List[AgentAction] = []
    for action in agent_config.get("marketplace_actions", []):
        actions.append(
            AgentAction(
                name=action.get("name", ""),
                action_type="marketplace",
                action_source=action.get("action", ""),
                params=action.get("params", {}),
                outputs=action.get("outputs", {}),
            )
        )
    for action in agent_config.get("internal_actions", []):
        actions.append(
            AgentAction(
                name=action.get("name", ""),
                action_type="internal",
                action_source=action.get("action", ""),
                params=action.get("params", {}),
                outputs=action.get("outputs", {}),
            )
        )
    
    # Convert to AgentConfiguration
    config = AgentConfiguration(
        agent_id=agent_config["id"],
        agent_name=agent_config["name"],
        description=agent_config["description"],
        lifecycle_transition=LifecycleTransition(transition_name),
        gates=agent_config.get("gates", []),
        actions=actions,
        outputs=agent_config.get("outputs", {}),
        governance=agent_config.get("governance", {})
    )
    
    return LifecycleAgent(config)
