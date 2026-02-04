#!/usr/bin/env python3
"""
Marketplace Agents Demo

Demonstrates the CNOT-agent orchestration system with GitHub Marketplace
action integration for aerospace lifecycle management.

This demo shows:
1. Marketplace action catalog and categorization
2. Lifecycle agent configuration and execution
3. Agent registry management
4. CNOT gate validation and provenance tracking
"""

from pathlib import Path

from aerospacemodel.agents import (
    MarketplaceAgent,
    MarketplaceActionCategory,
    LifecycleAgent,
    AgentConfiguration,
    AgentAction,
    LifecycleTransition,
    AgentRegistry,
    create_agent_from_yaml,
)


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def demo_marketplace_catalog():
    """Demo 1: Marketplace action catalog exploration."""
    print_section("DEMO 1: Marketplace Action Catalog")
    
    agent = MarketplaceAgent()
    
    print("📦 GitHub Marketplace Actions Catalog")
    print(f"Total actions: {len(agent.ACTION_CATALOG)}\n")
    
    # Show actions by category
    categories = [
        MarketplaceActionCategory.AI_REASONING,
        MarketplaceActionCategory.SBOM_GENERATION,
        MarketplaceActionCategory.SECURITY_SCANNING,
        MarketplaceActionCategory.POLICY_ENFORCEMENT,
    ]
    
    for category in categories:
        actions = agent.list_actions_by_category(category)
        print(f"\n{category.value.upper().replace('_', ' ')} ({len(actions)} actions):")
        for action_key in actions:
            info = agent.get_action_info(action_key)
            print(f"  ✓ {action_key}")
            print(f"    Source: {info['source']}")
            print(f"    License: {info['license']}")
            print(f"    Verified: {'Yes' if info['verified'] else 'No'}")
    
    print("\n✓ For complete catalog, see: docs/GITHUB_MARKETPLACE_ACTIONS_CATALOG.md")


def demo_action_execution():
    """Demo 2: Marketplace action execution."""
    print_section("DEMO 2: Marketplace Action Execution")
    
    agent = MarketplaceAgent(execution_mode="python")
    
    print("🚀 Executing marketplace actions...\n")
    
    # Execute SBOM generation
    print("Action 1: SBOM Generation")
    result1 = agent.execute_action(
        "anchore-sbom",
        {"format": "spdx-json", "artifact-name": "demo-sbom"},
        {"component": "aerospacemodel"}
    )
    print(f"  Status: {result1.status}")
    print(f"  Action: {result1.action_source}")
    print(f"  Queued: {result1.metadata.get('queued_for')}")
    
    # Execute AI code review
    print("\nAction 2: AI Code Review")
    result2 = agent.execute_action(
        "ai-code-reviewer",
        {"exclude_patterns": "tests/**"},
        {"pr_number": 42}
    )
    print(f"  Status: {result2.status}")
    print(f"  Action: {result2.action_source}")
    
    # Execute policy check
    print("\nAction 3: Policy Check (GHAS)")
    result3 = agent.execute_action(
        "ghas-policy",
        {"policy": "compliance_policy.yaml"},
        {"repository": "AmedeoPelliccia/AEROSPACEMODEL"}
    )
    print(f"  Status: {result3.status}")
    print(f"  Action: {result3.action_source}")
    
    print("\n✓ All actions queued for GitHub Actions execution")


def demo_lifecycle_agent():
    """Demo 3: Lifecycle agent execution."""
    print_section("DEMO 3: Lifecycle Agent Execution")
    
    print("🔄 Creating Design-to-Verification Agent\n")
    
    # Create agent configuration
    config = AgentConfiguration(
        agent_id="DEMO-AGENT-001",
        agent_name="Demo Design Verification Agent",
        description="Demonstrates lifecycle transition validation",
        lifecycle_transition=LifecycleTransition.DESIGN_TO_VERIFICATION,
        gates=[
            {
                "type": "ContractGate",
                "contract_id": "KITDM-CTR-LM-CSDB_ATA27"
            },
            {
                "type": "BaselineGate",
                "baseline_id": "FBL-2026-Q1-003"
            },
            {
                "type": "AuthorityGate",
                "required_authority": "STK_CM"
            },
        ],
        actions=[
            AgentAction(
                name="SBOM Generation",
                action_type="marketplace",
                action_source="anchore/sbom-action",
                params={"format": "spdx-json"},
                outputs={"sbom": "sbom.json"}
            ),
            AgentAction(
                name="AI Code Review",
                action_type="marketplace",
                action_source="gaurav-nelson/github-actions-ai-code-reviewer",
                params={},
                outputs={"review": "review.json"}
            ),
        ],
        outputs={
            "state_update": {
                "component_state": "verification_ready",
                "lifecycle_state": "verification"
            }
        },
        governance={
            "policy_engine": "OPA"
        }
    )
    
    print(f"Agent: {config.agent_name}")
    print(f"ID: {config.agent_id}")
    print(f"Transition: {config.lifecycle_transition.value}")
    print(f"Gates: {len(config.gates)}")
    print(f"Actions: {len(config.actions)}\n")
    
    # Create agent
    agent = LifecycleAgent(config)
    
    # Prepare execution context
    context = {
        "component_id": "ATA27-AILERON",
        "contract": {
            "contract_id": "KITDM-CTR-LM-CSDB_ATA27",
            "status": "ACTIVE"
        },
        "baseline": {
            "baseline_id": "FBL-2026-Q1-003",
            "state": "APPROVED"
        },
        "execution_authority": "STK_CM",
        "brex_result": {
            "success": True,
            "final_action": "ALLOW"
        },
        "trace_data": {
            "total_required": 100,
            "total_linked": 100
        },
        "safety_impact": {
            "is_safety_critical": False
        }
    }
    
    print("Executing agent with context:")
    print(f"  Component: {context['component_id']}")
    print(f"  Contract: {context['contract']['contract_id']}")
    print(f"  Baseline: {context['baseline']['baseline_id']}")
    print(f"  Authority: {context['execution_authority']}\n")
    
    # Execute agent
    result = agent.execute(context)
    
    print("Execution Result:")
    print(f"  Success: {'✓' if result['success'] else '✗'}")
    print(f"  Execution ID: {result['execution_id']}")
    
    print("\n  Gate Results:")
    for gate_result in result['gate_results']:
        status = "✓" if gate_result['passed'] else "✗"
        print(f"    {status} {gate_result['gate']}: {gate_result['message']}")
    
    print("\n  Action Results:")
    for action_result in result['action_results']:
        print(f"    • {action_result['action_name']} ({action_result['action_type']})")
        print(f"      Status: {action_result.get('status', 'unknown')}")
    
    print("\n  Provenance:")
    provenance = result['provenance']
    print(f"    Vector ID: {provenance['vector_id']}")
    print(f"    Transition: {provenance['lifecycle_transition']}")
    print(f"    Gates: {len(provenance['gate_decisions'])}")
    print(f"    Actions: {len(provenance['actions_executed'])}")
    
    print("\n✓ Agent execution completed successfully")


def demo_agent_registry():
    """Demo 4: Agent registry management."""
    print_section("DEMO 4: Agent Registry Management")
    
    print("📋 Agent Registry Demo\n")
    
    # Create registry
    registry = AgentRegistry()
    
    # Register multiple agents
    agents_to_register = [
        ("AGENT-DESIGN-VERIFY", "Design to Verification", LifecycleTransition.DESIGN_TO_VERIFICATION),
        ("AGENT-VERIFY-CERT", "Verification to Certification", LifecycleTransition.VERIFICATION_TO_CERTIFICATION),
        ("AGENT-CERT-PROD", "Certification to Production", LifecycleTransition.CERTIFICATION_TO_PRODUCTION),
    ]
    
    for agent_id, agent_name, transition in agents_to_register:
        config = AgentConfiguration(
            agent_id=agent_id,
            agent_name=agent_name,
            description=f"Agent for {transition.value}",
            lifecycle_transition=transition,
            gates=[],
            actions=[],
            outputs={},
            governance={}
        )
        registry.register(agent_id, config)
        print(f"✓ Registered: {agent_id} ({agent_name})")
    
    print(f"\nTotal agents registered: {len(registry.list())}")
    
    # List agents by transition
    print("\nAgents by Lifecycle Transition:")
    transitions = [
        LifecycleTransition.DESIGN_TO_VERIFICATION,
        LifecycleTransition.VERIFICATION_TO_CERTIFICATION,
        LifecycleTransition.CERTIFICATION_TO_PRODUCTION,
    ]
    
    for transition in transitions:
        agents = registry.list_by_transition(transition.value)
        print(f"  {transition.value}: {len(agents)} agent(s)")
        for agent_id in agents:
            info = registry.get_info(agent_id)
            print(f"    - {info['agent_name']}")
    
    # Retrieve and display agent info
    print("\nAgent Details:")
    for agent_id in registry.list():
        info = registry.get_info(agent_id)
        print(f"\n  {info['agent_id']}")
        print(f"    Name: {info['agent_name']}")
        print(f"    Description: {info['description']}")
        print(f"    Transition: {info['lifecycle_transition']}")
    
    print("\n✓ Registry management demonstration complete")


def demo_yaml_agent_loading():
    """Demo 5: Loading agents from YAML configuration."""
    print_section("DEMO 5: YAML Agent Configuration")
    
    print("📄 Loading agents from YAML configuration files\n")
    
    # Check for agent templates
    templates_dir = Path("templates/agents")
    
    if not templates_dir.exists():
        print("⚠️  Agent templates directory not found")
        print("   Expected: templates/agents/")
        return
    
    # Find YAML files
    yaml_files = list(templates_dir.glob("*.yaml"))
    
    if not yaml_files:
        print("⚠️  No agent YAML files found in templates/agents/")
        return
    
    print(f"Found {len(yaml_files)} agent configuration(s):\n")
    
    for yaml_file in yaml_files:
        print(f"  • {yaml_file.name}")
        
        try:
            # Load agent from YAML
            agent = create_agent_from_yaml(str(yaml_file))
            
            print(f"    Agent ID: {agent.config.agent_id}")
            print(f"    Agent Name: {agent.config.agent_name}")
            print(f"    Transition: {agent.config.lifecycle_transition.value}")
            print(f"    Gates: {len(agent.config.gates)}")
            print(f"    Actions: {len(agent.config.actions)}")
            print(f"    ✓ Successfully loaded\n")
            
        except Exception as e:
            print(f"    ✗ Error loading: {e}\n")
    
    print("✓ YAML agent loading demonstration complete")


def demo_complete_workflow():
    """Demo 6: Complete workflow simulation."""
    print_section("DEMO 6: Complete Workflow Simulation")
    
    print("🔄 Simulating complete lifecycle transition workflow\n")
    
    print("Scenario: ATA 27 Flight Controls - Design to Verification")
    print("="*60)
    
    # Step 1: Setup
    print("\nStep 1: Initialize Marketplace Agent")
    MarketplaceAgent(execution_mode="python")
    print("  ✓ Marketplace agent ready")
    
    # Step 2: Create lifecycle agent
    print("\nStep 2: Create Lifecycle Agent")
    config = AgentConfiguration(
        agent_id="WORKFLOW-AGENT-001",
        agent_name="ATA27 Design Verification Workflow",
        description="Complete workflow for ATA 27 flight controls",
        lifecycle_transition=LifecycleTransition.DESIGN_TO_VERIFICATION,
        gates=[
            {"type": "ContractGate", "contract_id": "KITDM-CTR-LM-CSDB_ATA27"},
            {"type": "BaselineGate", "baseline_id": "FBL-2026-Q1-003"},
            {"type": "AuthorityGate", "required_authority": "STK_CM"},
        ],
        actions=[
            AgentAction(
                name="SBOM Generation",
                action_type="marketplace",
                action_source="anchore/sbom-action",
                params={"format": "spdx-json"},
                outputs={"sbom": "sbom.json"}
            ),
            AgentAction(
                name="Security Scan",
                action_type="marketplace",
                action_source="scottman625/security-scanner-action",
                params={},
                outputs={"sarif": "security.sarif"}
            ),
        ],
        outputs={
            "state_update": {
                "component_state": "verification_ready",
                "lifecycle_state": "verification"
            }
        },
        governance={"policy_engine": "OPA"}
    )
    lifecycle_agent = LifecycleAgent(config)
    print(f"  ✓ Lifecycle agent created: {config.agent_name}")
    
    # Step 3: Prepare context
    print("\nStep 3: Prepare Execution Context")
    context = {
        "component_id": "ATA27-AILERON-CONTROL",
        "contract": {"contract_id": "KITDM-CTR-LM-CSDB_ATA27", "status": "ACTIVE"},
        "baseline": {"baseline_id": "FBL-2026-Q1-003", "state": "APPROVED"},
        "execution_authority": "STK_CM",
        "brex_result": {"success": True, "final_action": "ALLOW"},
        "trace_data": {"total_required": 100, "total_linked": 100},
        "safety_impact": {"is_safety_critical": False}
    }
    print("  ✓ Context prepared")
    
    # Step 4: Execute gates
    print("\nStep 4: Execute CNOT Gates")
    result = lifecycle_agent.execute(context)
    
    if result['success']:
        print("  ✓ All gates passed")
        for gate_result in result['gate_results']:
            print(f"    - {gate_result['gate']}: {gate_result['message']}")
    else:
        print(f"  ✗ Blocked by: {result.get('blocked_by')}")
        return
    
    # Step 5: Execute marketplace actions
    print("\nStep 5: Execute Marketplace Actions")
    for action_result in result['action_results']:
        print(f"  • {action_result['action_name']}")
        print(f"    Status: {action_result.get('status')}")
        if 'action' in action_result:
            print(f"    Action: {action_result['action']}")
    
    # Step 6: Generate provenance
    print("\nStep 6: Generate Provenance Vector")
    provenance = result['provenance']
    print(f"  ✓ Vector ID: {provenance['vector_id']}")
    print(f"  ✓ Transition: {provenance['lifecycle_transition']}")
    print(f"  ✓ Gates validated: {len(provenance['gate_decisions'])}")
    print(f"  ✓ Actions executed: {len(provenance['actions_executed'])}")
    
    # Step 7: Update state
    print("\nStep 7: Update Lifecycle State")
    state_update = result['state_update']
    print(f"  ✓ Component state: {state_update['component_state']}")
    print(f"  ✓ Lifecycle state: {state_update['lifecycle_state']}")
    
    print("\n" + "="*60)
    print("✓ Complete workflow simulation successful")
    print("="*60)


def main():
    """Run all demonstrations."""
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║       MARKETPLACE AGENTS DEMONSTRATION                     ║")
    print("║   CNOT-Gate Lifecycle Orchestration with GitHub Actions   ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    # Run demonstrations
    demo_marketplace_catalog()
    demo_action_execution()
    demo_lifecycle_agent()
    demo_agent_registry()
    demo_yaml_agent_loading()
    demo_complete_workflow()
    
    # Final summary
    print_section("DEMONSTRATION COMPLETE")
    
    print("Key Takeaways:")
    print("  ✓ 18 GitHub Marketplace actions cataloged and categorized")
    print("  ✓ Lifecycle agents orchestrate CNOT gates and marketplace actions")
    print("  ✓ Agent registry enables discovery and management")
    print("  ✓ YAML configuration supports declarative agent definition")
    print("  ✓ Full provenance tracking for audit and certification")
    print("  ✓ Integration with existing AEROSPACEMODEL BREX and contracts")
    
    print("\nFor More Information:")
    print("  • Documentation: docs/CNOT_AGENT_LIFECYCLE_ARCHITECTURE.md")
    print("  • Actions Catalog: docs/GITHUB_MARKETPLACE_ACTIONS_CATALOG.md")
    print("  • Workflows: .github/workflows/cnot-agent-orchestration.yml")
    print("  • Templates: templates/agents/")
    print("")


if __name__ == "__main__":
    main()
