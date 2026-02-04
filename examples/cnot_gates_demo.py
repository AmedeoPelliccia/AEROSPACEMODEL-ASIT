#!/usr/bin/env python3
"""
CNOT Gates Demo

Demonstrates the CNOT (Control Neural Origin Transaction) gates
in action with a complete transformation chain.
"""

from aerospacemodel.cnot import (
    CNOTChain,
    ContractGate,
    BaselineGate,
    AuthorityGate,
    BREXGate,
    TraceGate,
    SafetyGate,
)


def demo_successful_transformation():
    """Demo: Successful transformation with all gates passing."""
    print("=" * 60)
    print("DEMO 1: Successful Transformation")
    print("=" * 60)
    
    # Create a standard transformation chain
    chain = CNOTChain(chain_id="DEMO-SUCCESS-CHAIN")
    
    # Add gates in sequence
    chain.add_gate(ContractGate(contract_id="KITDM-CTR-LM-CSDB_ATA28"))
    chain.add_gate(BaselineGate(baseline_id="FBL-2026-Q1-003"))
    chain.add_gate(AuthorityGate(required_authority="STK_CM"))
    chain.add_gate(BREXGate())
    chain.add_gate(TraceGate(config={"coverage_threshold": 100}))
    chain.add_gate(SafetyGate())
    
    print(f"\nChain created with {chain.get_gate_count()} gates:")
    for gate_id in chain.get_gate_ids():
        print(f"  - {gate_id}")
    
    # Prepare context with all valid data
    context = {
        "contract": {
            "contract_id": "KITDM-CTR-LM-CSDB_ATA28",
            "status": "ACTIVE"
        },
        "baseline": {
            "baseline_id": "FBL-2026-Q1-003",
            "state": "APPROVED"
        },
        "execution_authority": "STK_PM",  # Higher than required STK_CM
        "brex_result": {
            "success": True,
            "final_action": "ALLOW",
            "escalation_required": False
        },
        "trace_data": {
            "total_required": 100,
            "total_linked": 100
        },
        "safety_impact": {
            "is_safety_critical": False,
            "safety_level": "NONE"
        },
        "artifact": {"type": "DataModule", "content": "S1000D DM"}
    }
    
    # Execute the chain
    print("\nExecuting chain...")
    result = chain.execute(context)
    
    # Display results
    print(f"\n{'='*60}")
    print(f"Result: {'SUCCESS ✓' if result.success else 'FAILED ✗'}")
    print(f"State Collapsed: {result.collapsed}")
    print(f"{'='*60}")
    
    print(f"\nGate Results:")
    for gate_result in result.gate_results:
        status_icon = "✓" if gate_result.passed else "✗"
        print(f"  {status_icon} {gate_result.gate_name}: {gate_result.message}")
    
    if result.collapsed:
        print(f"\nCollapsed State:")
        print(f"  Artifact ID: {result.collapsed_state.artifact_id}")
        print(f"  State Type: {result.collapsed_state.state_type.value}")
        print(f"  Collapsed By: {result.collapsed_state.collapsed_by}")
    
    if result.provenance:
        print(f"\nProvenance Vector:")
        print(f"  Vector ID: {result.provenance.vector_id}")
        print(f"  Contract: {result.provenance.transformation_contract}")
        print(f"  Gate Decisions: {len(result.provenance.gate_decisions)}")


def demo_blocked_transformation():
    """Demo: Transformation blocked by invalid contract."""
    print("\n\n" + "=" * 60)
    print("DEMO 2: Blocked Transformation (Invalid Contract)")
    print("=" * 60)
    
    # Create chain
    chain = CNOTChain(chain_id="DEMO-BLOCKED-CHAIN")
    chain.add_gate(ContractGate(contract_id="KITDM-CTR-LM-CSDB_ATA28"))
    chain.add_gate(BaselineGate(baseline_id="FBL-2026-Q1-003"))
    chain.add_gate(BREXGate())
    
    # Context with DRAFT contract (will fail)
    context = {
        "contract": {
            "contract_id": "KITDM-CTR-LM-CSDB_ATA28",
            "status": "DRAFT"  # ❌ Not approved
        },
        "baseline": {
            "baseline_id": "FBL-2026-Q1-003",
            "state": "APPROVED"
        }
    }
    
    print("\nExecuting chain with DRAFT contract...")
    result = chain.execute(context)
    
    print(f"\n{'='*60}")
    print(f"Result: {'SUCCESS ✓' if result.success else 'BLOCKED ✗'}")
    print(f"Blocked By: {result.blocked_by}")
    print(f"{'='*60}")
    
    print(f"\nGate Results:")
    for gate_result in result.gate_results:
        status_icon = "✓" if gate_result.passed else "✗"
        print(f"  {status_icon} {gate_result.gate_name}: {gate_result.message}")
    
    print(f"\nState Type: {result.collapsed_state.state_type.value}")
    print("No artifact generated - transformation blocked")


def demo_safety_escalation():
    """Demo: Safety-critical operation requiring escalation."""
    print("\n\n" + "=" * 60)
    print("DEMO 3: Safety Escalation (Human-in-the-Loop Required)")
    print("=" * 60)
    
    # Create chain
    chain = CNOTChain(chain_id="DEMO-SAFETY-CHAIN")
    chain.add_gate(ContractGate(contract_id="KITDM-CTR-LM-CSDB_ATA28"))
    chain.add_gate(SafetyGate())
    
    # Context with safety-critical operation
    context = {
        "contract": {
            "contract_id": "KITDM-CTR-LM-CSDB_ATA28",
            "status": "APPROVED"
        },
        "safety_impact": {
            "is_safety_critical": True,
            "safety_level": "CATASTROPHIC"  # ❌ Requires human approval
        }
    }
    
    print("\nExecuting chain with safety-critical operation...")
    result = chain.execute(context)
    
    print(f"\n{'='*60}")
    print(f"Result: ESCALATION REQUIRED")
    print(f"State Type: {result.collapsed_state.state_type.value}")
    print(f"{'='*60}")
    
    print(f"\nGate Results:")
    for gate_result in result.gate_results:
        status_icon = "⚠" if gate_result.status.value == "escalate" else ("✓" if gate_result.passed else "✗")
        print(f"  {status_icon} {gate_result.gate_name}: {gate_result.message}")
    
    print(f"\nHuman-in-the-Loop Decision Required")
    print(f"Escalation Target: STK_SAF (Safety Authority)")


if __name__ == "__main__":
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║          CNOT GATES DEMONSTRATION                          ║")
    print("║   Control Neural Origin Transaction - Gate-Based Control   ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    # Run demos
    demo_successful_transformation()
    demo_blocked_transformation()
    demo_safety_escalation()
    
    print("\n\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("  ✓ Gates provide explicit control boundaries")
    print("  ✓ Execution stops at first failing gate")
    print("  ✓ Full provenance tracking for audit trails")
    print("  ✓ Safety-critical operations require human approval")
    print("  ✓ Deterministic, replayable transformations")
    print("\nFor more information, see: docs/CNOT_GATES_ARCHITECTURE.md")
    print("")
