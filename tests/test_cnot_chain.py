"""
Tests for CNOT Chain

Tests complete chain execution, state collapse mechanics, and integration.
"""

from aerospacemodel.cnot.chain import CNOTChain
from aerospacemodel.cnot.gates import (
    AuthorityGate,
    BaselineGate,
    BREXGate,
    ContractGate,
    GateStatus,
    SafetyGate,
    TraceGate,
)
from aerospacemodel.cnot.state import CollapsedState, QuantumState, StateType


class TestCNOTChain:
    """Tests for CNOTChain."""
    
    def test_chain_creation(self):
        """Test creating a CNOT chain."""
        chain = CNOTChain(chain_id="TEST-CHAIN-001")
        
        assert chain.chain_id == "TEST-CHAIN-001"
        assert chain.get_gate_count() == 0
        assert chain.provenance_enabled is True
    
    def test_chain_add_gate(self):
        """Test adding gates to a chain."""
        chain = CNOTChain()
        gate1 = ContractGate(contract_id="TEST-CTR-001")
        gate2 = BaselineGate(baseline_id="TEST-BL-001")
        
        chain.add_gate(gate1)
        chain.add_gate(gate2)
        
        assert chain.get_gate_count() == 2
        assert len(chain.get_gate_ids()) == 2
    
    def test_chain_method_chaining(self):
        """Test method chaining for adding gates."""
        chain = CNOTChain()
        
        chain.add_gate(ContractGate("TEST-CTR-001")) \
             .add_gate(BaselineGate("TEST-BL-001")) \
             .add_gate(BREXGate())
        
        assert chain.get_gate_count() == 3
    
    def test_chain_validate(self):
        """Test chain validation."""
        chain = CNOTChain()
        chain.add_gate(ContractGate("TEST-CTR-001"))
        chain.add_gate(BaselineGate("TEST-BL-001"))
        
        assert chain.validate_chain() is True
    
    def test_chain_validate_empty(self):
        """Test validation fails for empty chain."""
        chain = CNOTChain()
        
        assert chain.validate_chain() is False
    
    def test_chain_clear_gates(self):
        """Test clearing gates from chain."""
        chain = CNOTChain()
        chain.add_gate(ContractGate("TEST-CTR-001"))
        chain.add_gate(BaselineGate("TEST-BL-001"))
        
        assert chain.get_gate_count() == 2
        
        chain.clear_gates()
        
        assert chain.get_gate_count() == 0


class TestChainExecution:
    """Tests for chain execution."""
    
    def test_chain_execute_all_gates_pass(self):
        """Test chain execution when all gates pass."""
        chain = CNOTChain(chain_id="TEST-SUCCESS-CHAIN")
        chain.add_gate(ContractGate("KITDM-CTR-LM-CSDB_ATA28"))
        chain.add_gate(BaselineGate("FBL-2026-Q1-003"))
        
        context = {
            "contract": {
                "contract_id": "KITDM-CTR-LM-CSDB_ATA28",
                "status": "APPROVED"
            },
            "baseline": {
                "baseline_id": "FBL-2026-Q1-003",
                "state": "APPROVED"
            }
        }
        
        result = chain.execute(context)
        
        assert result.success is True
        assert result.collapsed is True
        assert result.blocked_by is None
        assert len(result.gate_results) == 2
        assert all(gr.passed for gr in result.gate_results)
        assert result.collapsed_state is not None
        assert result.collapsed_state.state_type == StateType.COLLAPSED
    
    def test_chain_execute_stops_at_first_failure(self):
        """Test chain execution stops at first failing gate."""
        chain = CNOTChain()
        chain.add_gate(ContractGate("KITDM-CTR-LM-CSDB_ATA28"))
        chain.add_gate(BaselineGate("FBL-2026-Q1-003"))
        chain.add_gate(BREXGate())
        
        context = {
            "contract": {
                "contract_id": "KITDM-CTR-LM-CSDB_ATA28",
                "status": "DRAFT"  # Will fail ContractGate
            },
            "baseline": {
                "baseline_id": "FBL-2026-Q1-003",
                "state": "APPROVED"
            }
        }
        
        result = chain.execute(context)
        
        assert result.success is False
        assert result.collapsed is False
        assert result.blocked_by is not None
        assert len(result.gate_results) == 1  # Only first gate executed
        assert result.collapsed_state is not None
        assert result.collapsed_state.state_type == StateType.BLOCKED
    
    def test_chain_execute_with_escalation(self):
        """Test chain execution with gate requiring escalation."""
        chain = CNOTChain()
        chain.add_gate(ContractGate("KITDM-CTR-LM-CSDB_ATA28"))
        chain.add_gate(SafetyGate())
        
        context = {
            "contract": {
                "contract_id": "KITDM-CTR-LM-CSDB_ATA28",
                "status": "APPROVED"
            },
            "safety_impact": {
                "is_safety_critical": True,
                "safety_level": "CATASTROPHIC"
            }
        }
        
        result = chain.execute(context)
        
        assert result.success is False
        assert result.collapsed is False
        assert result.collapsed_state.state_type == StateType.PENDING_HITL
        # Find the safety gate result
        safety_result = next((gr for gr in result.gate_results if "SAFETY" in gr.gate_id), None)
        assert safety_result is not None
        assert safety_result.status == GateStatus.ESCALATE
    
    def test_chain_execute_with_provenance(self):
        """Test chain execution generates provenance vector."""
        chain = CNOTChain(provenance_enabled=True)
        chain.add_gate(ContractGate("KITDM-CTR-LM-CSDB_ATA28"))
        chain.add_gate(BaselineGate("FBL-2026-Q1-003"))
        
        context = {
            "contract": {
                "contract_id": "KITDM-CTR-LM-CSDB_ATA28",
                "status": "APPROVED"
            },
            "baseline": {
                "baseline_id": "FBL-2026-Q1-003",
                "state": "APPROVED"
            },
            "source_artifacts": ["DM-001", "DM-002"]
        }
        
        result = chain.execute(context)
        
        assert result.provenance is not None
        assert len(result.provenance.gate_decisions) == 2
        assert result.provenance.transformation_contract == "KITDM-CTR-LM-CSDB_ATA28"
        assert result.provenance.source_artifacts == ["DM-001", "DM-002"]
        assert result.provenance.collapsed_artifact is not None
    
    def test_chain_execute_without_provenance(self):
        """Test chain execution with provenance tracking disabled."""
        chain = CNOTChain(provenance_enabled=False)
        chain.add_gate(ContractGate("KITDM-CTR-LM-CSDB_ATA28"))
        chain.add_gate(BaselineGate("FBL-2026-Q1-003"))
        
        context = {
            "contract": {
                "contract_id": "KITDM-CTR-LM-CSDB_ATA28",
                "status": "APPROVED"
            },
            "baseline": {
                "baseline_id": "FBL-2026-Q1-003",
                "state": "APPROVED"
            },
            "source_artifacts": ["DM-001", "DM-002"]
        }
        
        result = chain.execute(context)
        
        # Should still succeed but with no provenance
        assert result.success is True
        assert result.collapsed is True
        assert result.provenance is None
        assert result.collapsed_state is not None
        assert result.collapsed_state.provenance is None
    
    def test_chain_execute_with_custom_quantum_state(self):
        """Test chain execution with custom quantum state."""
        chain = CNOTChain()
        chain.add_gate(ContractGate("KITDM-CTR-LM-CSDB_ATA28"))
        
        quantum_state = QuantumState(
            state_id="CUSTOM-QS-001",
            context={"custom": "data"}
        )
        
        context = {
            "contract": {
                "contract_id": "KITDM-CTR-LM-CSDB_ATA28",
                "status": "APPROVED"
            }
        }
        
        result = chain.execute(context, quantum_state=quantum_state)
        
        assert result.quantum_state.state_id == "CUSTOM-QS-001"
        assert result.quantum_state.context["custom"] == "data"


class TestComplexChainScenarios:
    """Tests for complex chain scenarios."""
    
    def test_full_standard_transformation_chain(self):
        """Test a complete standard transformation chain."""
        chain = CNOTChain(chain_id="STANDARD-TRANS")
        
        # Build standard chain
        chain.add_gate(ContractGate("KITDM-CTR-LM-CSDB_ATA28"))
        chain.add_gate(BaselineGate("FBL-2026-Q1-003"))
        chain.add_gate(AuthorityGate(required_authority="STK_CM"))
        chain.add_gate(BREXGate())
        chain.add_gate(TraceGate(config={"coverage_threshold": 100}))
        chain.add_gate(SafetyGate())
        
        # Full valid context
        context = {
            "contract": {
                "contract_id": "KITDM-CTR-LM-CSDB_ATA28",
                "status": "ACTIVE"
            },
            "baseline": {
                "baseline_id": "FBL-2026-Q1-003",
                "state": "RELEASED"
            },
            "execution_authority": "STK_PM",
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
            }
        }
        
        result = chain.execute(context)
        
        assert result.success is True
        assert result.collapsed is True
        assert len(result.gate_results) == 6
        assert all(gr.passed for gr in result.gate_results)
    
    def test_chain_with_insufficient_trace_coverage(self):
        """Test chain blocks when trace coverage is insufficient."""
        chain = CNOTChain()
        chain.add_gate(ContractGate("KITDM-CTR-LM-CSDB_ATA28"))
        chain.add_gate(TraceGate(config={"coverage_threshold": 100}))
        
        context = {
            "contract": {
                "contract_id": "KITDM-CTR-LM-CSDB_ATA28",
                "status": "APPROVED"
            },
            "trace_data": {
                "total_required": 100,
                "total_linked": 95  # Only 95% coverage
            }
        }
        
        result = chain.execute(context)
        
        assert result.success is False
        assert result.collapsed is False
        assert "TRACE" in result.blocked_by


class TestStateCollapse:
    """Tests for state collapse mechanics."""
    
    def test_state_collapse_creates_collapsed_state(self):
        """Test that successful chain creates CollapsedState."""
        chain = CNOTChain()
        chain.add_gate(ContractGate("KITDM-CTR-LM-CSDB_ATA28"))
        
        context = {
            "contract": {
                "contract_id": "KITDM-CTR-LM-CSDB_ATA28",
                "status": "APPROVED"
            },
            "artifact": {"type": "DataModule", "id": "DM-001"}
        }
        
        result = chain.execute(context)
        
        assert isinstance(result.collapsed_state, CollapsedState)
        assert result.collapsed_state.state_type == StateType.COLLAPSED
        assert result.collapsed_state.artifact is not None
    
    def test_blocked_chain_creates_blocked_state(self):
        """Test that blocked chain creates BlockedState."""
        chain = CNOTChain()
        chain.add_gate(ContractGate("KITDM-CTR-LM-CSDB_ATA28"))
        
        context = {
            "contract": {
                "contract_id": "KITDM-CTR-LM-CSDB_ATA28",
                "status": "DRAFT"
            }
        }
        
        result = chain.execute(context)
        
        assert isinstance(result.collapsed_state, CollapsedState)
        assert result.collapsed_state.state_type == StateType.BLOCKED
        assert result.collapsed_state.artifact is None


class TestDeterminism:
    """Tests for deterministic execution."""
    
    def test_same_input_produces_same_output(self):
        """Test that same inputs produce same outputs (determinism)."""
        def create_chain_and_execute():
            chain = CNOTChain(chain_id="DETERMINISM-TEST")
            chain.add_gate(ContractGate("KITDM-CTR-LM-CSDB_ATA28"))
            chain.add_gate(BaselineGate("FBL-2026-Q1-003"))
            
            context = {
                "contract": {
                    "contract_id": "KITDM-CTR-LM-CSDB_ATA28",
                    "status": "APPROVED"
                },
                "baseline": {
                    "baseline_id": "FBL-2026-Q1-003",
                    "state": "APPROVED"
                }
            }
            
            return chain.execute(context)
        
        result1 = create_chain_and_execute()
        result2 = create_chain_and_execute()
        
        # Both should succeed
        assert result1.success == result2.success
        assert result1.collapsed == result2.collapsed
        assert len(result1.gate_results) == len(result2.gate_results)
        
        # All gate results should match
        for i in range(len(result1.gate_results)):
            assert result1.gate_results[i].passed == result2.gate_results[i].passed
            assert result1.gate_results[i].status == result2.gate_results[i].status


class TestChainResult:
    """Tests for ChainResult."""
    
    def test_chain_result_to_dict(self):
        """Test ChainResult serialization."""
        chain = CNOTChain()
        chain.add_gate(ContractGate("KITDM-CTR-LM-CSDB_ATA28"))
        
        context = {
            "contract": {
                "contract_id": "KITDM-CTR-LM-CSDB_ATA28",
                "status": "APPROVED"
            }
        }
        
        result = chain.execute(context)
        result_dict = result.to_dict()
        
        assert "chain_id" in result_dict
        assert "success" in result_dict
        assert "collapsed" in result_dict
        assert "gate_results" in result_dict
        assert "provenance" in result_dict
        assert isinstance(result_dict["gate_results"], list)
