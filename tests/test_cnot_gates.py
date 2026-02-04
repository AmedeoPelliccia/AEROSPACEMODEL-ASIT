"""
Tests for CNOT Gates

Tests each gate type independently and validates their behavior.
"""

from aerospacemodel.cnot.gates import (
    AuthorityGate,
    BaselineGate,
    BREXGate,
    ContractGate,
    GateStatus,
    HITLGate,
    SafetyGate,
    TraceGate,
)


class TestContractGate:
    """Tests for ContractGate."""
    
    def test_contract_gate_passes_with_approved_contract(self):
        """Test that ContractGate passes with APPROVED contract."""
        gate = ContractGate(contract_id="KITDM-CTR-LM-CSDB_ATA28")
        context = {
            "contract": {
                "contract_id": "KITDM-CTR-LM-CSDB_ATA28",
                "status": "APPROVED"
            }
        }
        
        result = gate.execute(context)
        
        assert result.passed is True
        assert result.status == GateStatus.PASSED
        assert "validated" in result.message.lower()
    
    def test_contract_gate_passes_with_active_contract(self):
        """Test that ContractGate passes with ACTIVE contract."""
        gate = ContractGate(contract_id="KITDM-CTR-LM-CSDB_ATA28")
        context = {
            "contract": {
                "contract_id": "KITDM-CTR-LM-CSDB_ATA28",
                "status": "ACTIVE"
            }
        }
        
        result = gate.execute(context)
        
        assert result.passed is True
        assert result.status == GateStatus.PASSED
    
    def test_contract_gate_blocks_with_draft_contract(self):
        """Test that ContractGate blocks with DRAFT contract."""
        gate = ContractGate(contract_id="KITDM-CTR-LM-CSDB_ATA28")
        context = {
            "contract": {
                "contract_id": "KITDM-CTR-LM-CSDB_ATA28",
                "status": "DRAFT"
            }
        }
        
        result = gate.execute(context)
        
        assert result.passed is False
        assert result.status == GateStatus.BLOCKED
    
    def test_contract_gate_blocks_with_missing_contract(self):
        """Test that ContractGate blocks when contract is missing."""
        gate = ContractGate(contract_id="KITDM-CTR-LM-CSDB_ATA28")
        context = {}
        
        result = gate.execute(context)
        
        assert result.passed is False
        assert result.status == GateStatus.BLOCKED
        assert "no contract" in result.message.lower()
    
    def test_contract_gate_blocks_with_id_mismatch(self):
        """Test that ContractGate blocks with contract ID mismatch."""
        gate = ContractGate(contract_id="KITDM-CTR-LM-CSDB_ATA28")
        context = {
            "contract": {
                "contract_id": "KITDM-CTR-LM-CSDB_ATA27",
                "status": "APPROVED"
            }
        }
        
        result = gate.execute(context)
        
        assert result.passed is False
        assert result.status == GateStatus.BLOCKED
        assert "mismatch" in result.message.lower()


class TestBaselineGate:
    """Tests for BaselineGate."""
    
    def test_baseline_gate_passes_with_approved_baseline(self):
        """Test that BaselineGate passes with APPROVED baseline."""
        gate = BaselineGate(baseline_id="FBL-2026-Q1-003")
        context = {
            "baseline": {
                "baseline_id": "FBL-2026-Q1-003",
                "state": "APPROVED"
            }
        }
        
        result = gate.execute(context)
        
        assert result.passed is True
        assert result.status == GateStatus.PASSED
    
    def test_baseline_gate_passes_with_released_baseline(self):
        """Test that BaselineGate passes with RELEASED baseline."""
        gate = BaselineGate(baseline_id="FBL-2026-Q1-003")
        context = {
            "baseline": {
                "baseline_id": "FBL-2026-Q1-003",
                "state": "RELEASED"
            }
        }
        
        result = gate.execute(context)
        
        assert result.passed is True
        assert result.status == GateStatus.PASSED
    
    def test_baseline_gate_blocks_with_draft_baseline(self):
        """Test that BaselineGate blocks with DRAFT baseline."""
        gate = BaselineGate(baseline_id="FBL-2026-Q1-003")
        context = {
            "baseline": {
                "baseline_id": "FBL-2026-Q1-003",
                "state": "DRAFT"
            }
        }
        
        result = gate.execute(context)
        
        assert result.passed is False
        assert result.status == GateStatus.BLOCKED
    
    def test_baseline_gate_blocks_with_missing_baseline(self):
        """Test that BaselineGate blocks when baseline is missing."""
        gate = BaselineGate(baseline_id="FBL-2026-Q1-003")
        context = {}
        
        result = gate.execute(context)
        
        assert result.passed is False
        assert result.status == GateStatus.BLOCKED


class TestAuthorityGate:
    """Tests for AuthorityGate."""
    
    def test_authority_gate_passes_with_exact_authority(self):
        """Test that AuthorityGate passes with exact authority match."""
        gate = AuthorityGate(required_authority="STK_CM")
        context = {
            "execution_authority": "STK_CM"
        }
        
        result = gate.execute(context)
        
        assert result.passed is True
        assert result.status == GateStatus.PASSED
    
    def test_authority_gate_passes_with_higher_authority(self):
        """Test that AuthorityGate passes with higher authority."""
        gate = AuthorityGate(required_authority="STK_ENG")
        context = {
            "execution_authority": "STK_CM"  # CM is higher than ENG
        }
        
        result = gate.execute(context)
        
        assert result.passed is True
        assert result.status == GateStatus.PASSED
    
    def test_authority_gate_blocks_with_lower_authority(self):
        """Test that AuthorityGate blocks with lower authority."""
        gate = AuthorityGate(required_authority="STK_CM")
        context = {
            "execution_authority": "STK_ENG"  # ENG is lower than CM
        }
        
        result = gate.execute(context)
        
        assert result.passed is False
        assert result.status == GateStatus.BLOCKED
    
    def test_authority_gate_blocks_with_missing_authority(self):
        """Test that AuthorityGate blocks when authority is missing."""
        gate = AuthorityGate(required_authority="STK_CM")
        context = {}
        
        result = gate.execute(context)
        
        assert result.passed is False
        assert result.status == GateStatus.BLOCKED


class TestBREXGate:
    """Tests for BREXGate."""
    
    def test_brex_gate_passes_with_successful_result(self):
        """Test that BREXGate passes with successful BREX result."""
        gate = BREXGate()
        context = {
            "brex_result": {
                "success": True,
                "final_action": "ALLOW"
            }
        }
        
        result = gate.execute(context)
        
        assert result.passed is True
        assert result.status == GateStatus.PASSED
    
    def test_brex_gate_blocks_with_failed_result(self):
        """Test that BREXGate blocks with failed BREX result."""
        gate = BREXGate()
        context = {
            "brex_result": {
                "success": False,
                "final_action": "BLOCK",
                "blocked_by": "RULE-001"
            }
        }
        
        result = gate.execute(context)
        
        assert result.passed is False
        assert result.status == GateStatus.BLOCKED
    
    def test_brex_gate_escalates_with_escalation_required(self):
        """Test that BREXGate escalates when escalation is required."""
        gate = BREXGate()
        context = {
            "brex_result": {
                "success": True,
                "final_action": "ALLOW",
                "escalation_required": True,
                "escalation_rules": ["RULE-002"]
            }
        }
        
        result = gate.execute(context)
        
        assert result.passed is False
        assert result.status == GateStatus.ESCALATE
    
    def test_brex_gate_blocks_with_missing_result(self):
        """Test that BREXGate blocks when BREX result is missing."""
        gate = BREXGate()
        context = {}
        
        result = gate.execute(context)
        
        assert result.passed is False
        assert result.status == GateStatus.BLOCKED


class TestTraceGate:
    """Tests for TraceGate."""
    
    def test_trace_gate_passes_with_100_percent_coverage(self):
        """Test that TraceGate passes with 100% coverage."""
        gate = TraceGate(config={"coverage_threshold": 100})
        context = {
            "trace_data": {
                "total_required": 100,
                "total_linked": 100
            }
        }
        
        result = gate.execute(context)
        
        assert result.passed is True
        assert result.status == GateStatus.PASSED
    
    def test_trace_gate_passes_with_coverage_above_threshold(self):
        """Test that TraceGate passes with coverage above threshold."""
        gate = TraceGate(config={"coverage_threshold": 95})
        context = {
            "trace_data": {
                "total_required": 100,
                "total_linked": 98
            }
        }
        
        result = gate.execute(context)
        
        assert result.passed is True
        assert result.status == GateStatus.PASSED
    
    def test_trace_gate_blocks_with_coverage_below_threshold(self):
        """Test that TraceGate blocks with coverage below threshold."""
        gate = TraceGate(config={"coverage_threshold": 100})
        context = {
            "trace_data": {
                "total_required": 100,
                "total_linked": 95
            }
        }
        
        result = gate.execute(context)
        
        assert result.passed is False
        assert result.status == GateStatus.BLOCKED
    
    def test_trace_gate_blocks_with_missing_trace_data(self):
        """Test that TraceGate blocks when trace data is missing."""
        gate = TraceGate()
        context = {}
        
        result = gate.execute(context)
        
        assert result.passed is False
        assert result.status == GateStatus.BLOCKED


class TestSafetyGate:
    """Tests for SafetyGate."""
    
    def test_safety_gate_passes_with_no_safety_impact(self):
        """Test that SafetyGate passes with no safety impact."""
        gate = SafetyGate()
        context = {}
        
        result = gate.execute(context)
        
        assert result.passed is True
        assert result.status == GateStatus.PASSED
    
    def test_safety_gate_passes_with_non_critical_impact(self):
        """Test that SafetyGate passes with non-safety-critical impact."""
        gate = SafetyGate()
        context = {
            "safety_impact": {
                "is_safety_critical": False,
                "safety_level": "MINOR"
            }
        }
        
        result = gate.execute(context)
        
        assert result.passed is True
        assert result.status == GateStatus.PASSED
    
    def test_safety_gate_escalates_with_safety_critical(self):
        """Test that SafetyGate escalates with safety-critical impact."""
        gate = SafetyGate()
        context = {
            "safety_impact": {
                "is_safety_critical": True,
                "safety_level": "CATASTROPHIC"
            }
        }
        
        result = gate.execute(context)
        
        assert result.passed is False
        assert result.status == GateStatus.ESCALATE
    
    def test_safety_gate_escalates_with_hazardous_level(self):
        """Test that SafetyGate escalates with HAZARDOUS level."""
        gate = SafetyGate()
        context = {
            "safety_impact": {
                "is_safety_critical": False,
                "safety_level": "HAZARDOUS"
            }
        }
        
        result = gate.execute(context)
        
        assert result.passed is False
        assert result.status == GateStatus.ESCALATE


class TestHITLGate:
    """Tests for HITLGate (Human-in-the-Loop)."""
    
    def test_hitl_gate_escalates_without_decision(self):
        """Test that HITLGate escalates when no decision has been made."""
        gate = HITLGate(checkpoint_id="CHECKPOINT-001")
        context = {}
        
        result = gate.execute(context)
        
        assert result.passed is False
        assert result.status == GateStatus.ESCALATE
    
    def test_hitl_gate_passes_with_approved_decision(self):
        """Test that HITLGate passes with APPROVED decision."""
        gate = HITLGate(checkpoint_id="CHECKPOINT-001")
        context = {
            "hitl_decision": {
                "decision": "APPROVED",
                "decider": "John Doe",
                "rationale": "All checks passed"
            }
        }
        
        result = gate.execute(context)
        
        assert result.passed is True
        assert result.status == GateStatus.PASSED
    
    def test_hitl_gate_passes_with_proceed_decision(self):
        """Test that HITLGate passes with PROCEED decision."""
        gate = HITLGate(checkpoint_id="CHECKPOINT-001")
        context = {
            "hitl_decision": {
                "decision": "PROCEED",
                "decider": "Jane Smith"
            }
        }
        
        result = gate.execute(context)
        
        assert result.passed is True
        assert result.status == GateStatus.PASSED
    
    def test_hitl_gate_blocks_with_rejected_decision(self):
        """Test that HITLGate blocks with REJECTED decision."""
        gate = HITLGate(checkpoint_id="CHECKPOINT-001")
        context = {
            "hitl_decision": {
                "decision": "REJECTED",
                "decider": "John Doe",
                "rationale": "Safety concerns"
            }
        }
        
        result = gate.execute(context)
        
        assert result.passed is False
        assert result.status == GateStatus.BLOCKED


class TestGateResult:
    """Tests for GateResult."""
    
    def test_gate_result_to_dict(self):
        """Test GateResult serialization to dict."""
        from aerospacemodel.cnot.gates import GateResult
        
        result = GateResult(
            gate_id="TEST-001",
            gate_name="Test Gate",
            status=GateStatus.PASSED,
            passed=True,
            message="Test message",
            context={"key": "value"},
            evidence={"data": "evidence"}
        )
        
        result_dict = result.to_dict()
        
        assert result_dict["gate_id"] == "TEST-001"
        assert result_dict["gate_name"] == "Test Gate"
        assert result_dict["status"] == "passed"
        assert result_dict["passed"] is True
        assert result_dict["message"] == "Test message"
        assert result_dict["context"] == {"key": "value"}
        assert result_dict["evidence"] == {"data": "evidence"}
    
    def test_gate_result_to_log_entry(self):
        """Test GateResult log entry generation."""
        from aerospacemodel.cnot.gates import GateResult
        
        result = GateResult(
            gate_id="TEST-001",
            gate_name="Test Gate",
            status=GateStatus.PASSED,
            passed=True,
            message="Test message"
        )
        
        log_entry = result.to_log_entry()
        
        assert "TEST-001" in log_entry
        assert "Test Gate" in log_entry
        assert "PASSED" in log_entry
        assert "Test message" in log_entry
