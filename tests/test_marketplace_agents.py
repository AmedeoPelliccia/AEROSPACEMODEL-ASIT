"""
Tests for Marketplace Agents

Tests the MarketplaceAgent, LifecycleAgent, and AgentRegistry modules.
"""

import pytest
from pathlib import Path
import tempfile
import yaml

from aerospacemodel.agents import (
    MarketplaceAgent,
    MarketplaceActionCategory,
    MarketplaceActionResult,
    execute_marketplace_action,
    LifecycleAgent,
    AgentConfiguration,
    AgentAction,
    LifecycleTransition,
    create_agent_from_yaml,
    AgentRegistry,
    register_agent,
    get_agent,
    list_agents,
    get_registry,
)


class TestMarketplaceAgent:
    """Tests for MarketplaceAgent."""
    
    def test_marketplace_agent_initialization(self):
        """Test MarketplaceAgent initialization."""
        agent = MarketplaceAgent(execution_mode="python")
        assert agent.execution_mode == "python"
    
    def test_action_catalog_exists(self):
        """Test that action catalog is populated."""
        agent = MarketplaceAgent()
        assert len(agent.ACTION_CATALOG) > 0
        
        # Check known actions
        assert "ai-inference" in agent.ACTION_CATALOG
        assert "anchore-sbom" in agent.ACTION_CATALOG
        assert "ghas-policy" in agent.ACTION_CATALOG
    
    def test_get_action_info(self):
        """Test getting action information."""
        agent = MarketplaceAgent()
        
        # Get info for known action
        info = agent.get_action_info("ai-inference")
        assert info is not None
        assert "source" in info
        assert "category" in info
        assert "license" in info
        assert info["verified"] == True
        
        # Get info for unknown action
        info = agent.get_action_info("nonexistent-action")
        assert info is None
    
    def test_list_actions_by_category(self):
        """Test listing actions by category."""
        agent = MarketplaceAgent()
        
        # List AI reasoning actions
        ai_actions = agent.list_actions_by_category(MarketplaceActionCategory.AI_REASONING)
        assert len(ai_actions) > 0
        assert "ai-inference" in ai_actions
        
        # List SBOM actions
        sbom_actions = agent.list_actions_by_category(MarketplaceActionCategory.SBOM_GENERATION)
        assert len(sbom_actions) > 0
        assert "anchore-sbom" in sbom_actions
    
    def test_execute_action_python_mode(self):
        """Test executing action in Python mode (queuing)."""
        agent = MarketplaceAgent(execution_mode="python")
        
        result = agent.execute_action(
            "anchore-sbom",
            {"format": "spdx-json"},
            {"component": "test"}
        )
        
        assert isinstance(result, MarketplaceActionResult)
        assert result.status == "queued"
        assert result.action_name == "anchore-sbom"
        assert "workflow_step" in result.outputs
    
    def test_execute_unknown_action(self):
        """Test executing unknown action returns error."""
        agent = MarketplaceAgent()
        
        result = agent.execute_action(
            "unknown-action",
            {},
            {}
        )
        
        assert result.status == "error"
        assert result.error is not None
    
    def test_execute_marketplace_action_function(self):
        """Test convenience function for executing actions."""
        result = execute_marketplace_action(
            "ai-inference",
            {"prompt": "test"},
            {"context": "test"}
        )
        
        assert isinstance(result, MarketplaceActionResult)
        assert result.action_name == "ai-inference"


class TestLifecycleAgent:
    """Tests for LifecycleAgent."""
    
    @pytest.fixture
    def sample_config(self):
        """Create sample agent configuration."""
        return AgentConfiguration(
            agent_id="TEST-AGENT-001",
            agent_name="Test Agent",
            description="Test lifecycle agent",
            lifecycle_transition=LifecycleTransition.DESIGN_TO_VERIFICATION,
            gates=[
                {
                    "type": "ContractGate",
                    "contract_id": "TEST-CONTRACT-001"
                }
            ],
            actions=[
                AgentAction(
                    name="Test Action",
                    action_type="marketplace",
                    action_source="test/action",
                    params={"key": "value"},
                    outputs={"result": "output.json"}
                )
            ],
            outputs={
                "state_update": {
                    "component_state": "verified",
                    "lifecycle_state": "verification"
                }
            },
            governance={
                "policy_engine": "OPA"
            }
        )
    
    def test_lifecycle_agent_initialization(self, sample_config):
        """Test LifecycleAgent initialization."""
        agent = LifecycleAgent(sample_config)
        
        assert agent.config == sample_config
        assert agent.cnot_chain is not None
        assert agent.execution_id is None
    
    def test_lifecycle_agent_execute(self, sample_config):
        """Test agent execution."""
        agent = LifecycleAgent(sample_config)
        
        context = {
            "component_id": "TEST-COMPONENT",
            "contract": {
                "contract_id": "TEST-CONTRACT-001",
                "status": "ACTIVE"
            },
            "baseline": {
                "baseline_id": "TEST-BASELINE",
                "state": "APPROVED"
            },
            "execution_authority": "STK_CM"
        }
        
        result = agent.execute(context)
        
        assert "success" in result
        assert "execution_id" in result
        assert "agent_id" in result
        assert result["agent_id"] == "TEST-AGENT-001"
        assert "gate_results" in result
        assert "action_results" in result
        assert "provenance" in result
    
    def test_create_agent_from_yaml(self, tmp_path):
        """Test creating agent from YAML configuration."""
        # Create temporary YAML file
        yaml_config = {
            "cnot_agent": {
                "id": "YAML-TEST-AGENT",
                "name": "YAML Test Agent",
                "description": "Test agent from YAML",
                "lifecycle_transition": {
                    "from": "design",
                    "to": "verification"
                },
                "gates": [
                    {
                        "type": "ContractGate",
                        "contract_id": "TEST-CONTRACT"
                    }
                ],
                "marketplace_actions": [
                    {
                        "name": "Test Action",
                        "action": "test/action",
                        "params": {},
                        "outputs": {}
                    }
                ],
                "internal_actions": [],
                "outputs": {},
                "governance": {}
            }
        }
        
        yaml_path = tmp_path / "test_agent.yaml"
        with open(yaml_path, 'w') as f:
            yaml.dump(yaml_config, f)
        
        # Create agent from YAML
        agent = create_agent_from_yaml(str(yaml_path))
        
        assert agent.config.agent_id == "YAML-TEST-AGENT"
        assert agent.config.agent_name == "YAML Test Agent"
        assert agent.config.lifecycle_transition == LifecycleTransition.DESIGN_TO_VERIFICATION


class TestAgentRegistry:
    """Tests for AgentRegistry."""
    
    @pytest.fixture
    def sample_config(self):
        """Create sample agent configuration."""
        return AgentConfiguration(
            agent_id="REGISTRY-TEST-001",
            agent_name="Registry Test Agent",
            description="Test agent for registry",
            lifecycle_transition=LifecycleTransition.DESIGN_TO_VERIFICATION,
            gates=[],
            actions=[],
            outputs={},
            governance={}
        )
    
    def test_registry_initialization(self):
        """Test registry initialization."""
        registry = AgentRegistry()
        assert len(registry.list()) == 0
    
    def test_register_agent(self, sample_config):
        """Test registering an agent."""
        registry = AgentRegistry()
        registry.register("TEST-001", sample_config)
        
        assert "TEST-001" in registry.list()
        assert len(registry.list()) == 1
    
    def test_get_agent(self, sample_config):
        """Test getting an agent."""
        registry = AgentRegistry()
        registry.register("TEST-001", sample_config)
        
        agent = registry.get("TEST-001")
        assert agent is not None
        assert isinstance(agent, LifecycleAgent)
        assert agent.config == sample_config
    
    def test_get_nonexistent_agent(self):
        """Test getting nonexistent agent returns None."""
        registry = AgentRegistry()
        agent = registry.get("NONEXISTENT")
        assert agent is None
    
    def test_get_info(self, sample_config):
        """Test getting agent information."""
        registry = AgentRegistry()
        registry.register("TEST-001", sample_config)
        
        info = registry.get_info("TEST-001")
        assert info is not None
        assert info["agent_id"] == "REGISTRY-TEST-001"
        assert info["agent_name"] == "Registry Test Agent"
        assert info["lifecycle_transition"] == "design_to_verification"
    
    def test_list_by_transition(self, sample_config):
        """Test listing agents by transition."""
        registry = AgentRegistry()
        registry.register("TEST-001", sample_config)
        
        # Create another config with different transition
        config2 = AgentConfiguration(
            agent_id="REGISTRY-TEST-002",
            agent_name="Registry Test Agent 2",
            description="Test agent 2",
            lifecycle_transition=LifecycleTransition.VERIFICATION_TO_CERTIFICATION,
            gates=[],
            actions=[],
            outputs={},
            governance={}
        )
        registry.register("TEST-002", config2)
        
        # List by transition
        design_verify_agents = registry.list_by_transition("design_to_verification")
        assert len(design_verify_agents) == 1
        assert "TEST-001" in design_verify_agents
        
        verify_cert_agents = registry.list_by_transition("verification_to_certification")
        assert len(verify_cert_agents) == 1
        assert "TEST-002" in verify_cert_agents
    
    def test_global_registry_functions(self, sample_config):
        """Test global registry convenience functions."""
        # Clear global registry first
        registry = get_registry()
        registry._agents.clear()
        registry._agent_instances.clear()
        
        # Register agent
        register_agent("GLOBAL-TEST", sample_config)
        
        # List agents
        agents = list_agents()
        assert "GLOBAL-TEST" in agents
        
        # Get agent
        agent = get_agent("GLOBAL-TEST")
        assert agent is not None
        assert agent.config == sample_config


class TestLifecycleTransition:
    """Tests for LifecycleTransition enum."""
    
    def test_lifecycle_transitions_exist(self):
        """Test that all expected lifecycle transitions exist."""
        assert LifecycleTransition.DESIGN_TO_VERIFICATION
        assert LifecycleTransition.VERIFICATION_TO_CERTIFICATION
        assert LifecycleTransition.CERTIFICATION_TO_PRODUCTION
        assert LifecycleTransition.PRODUCTION_TO_OPERATION
        assert LifecycleTransition.OPERATION_TO_MAINTENANCE
        assert LifecycleTransition.MAINTENANCE_TO_OPERATION
    
    def test_transition_values(self):
        """Test lifecycle transition values."""
        assert LifecycleTransition.DESIGN_TO_VERIFICATION.value == "design_to_verification"
        assert LifecycleTransition.VERIFICATION_TO_CERTIFICATION.value == "verification_to_certification"


class TestMarketplaceActionCategory:
    """Tests for MarketplaceActionCategory enum."""
    
    def test_action_categories_exist(self):
        """Test that all expected action categories exist."""
        assert MarketplaceActionCategory.AI_REASONING
        assert MarketplaceActionCategory.AI_SUMMARIZATION
        assert MarketplaceActionCategory.POLICY_ENFORCEMENT
        assert MarketplaceActionCategory.SECURITY_SCANNING
        assert MarketplaceActionCategory.SBOM_GENERATION
        assert MarketplaceActionCategory.PROVENANCE
        assert MarketplaceActionCategory.AUDIT_TRACKING


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
