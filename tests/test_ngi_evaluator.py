"""Tests for NGI policy evaluator."""
import os
import tempfile
import yaml
import pytest
from pathlib import Path


# Import the evaluator module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import ngi_evaluator


def test_policy_file_exists():
    """Test that policy file exists and is valid."""
    policy_path = Path(__file__).parent.parent / "policy" / "ngi_policy_v1.yaml"
    assert policy_path.exists(), "Policy file should exist"
    
    with open(policy_path, "r") as f:
        policy = yaml.safe_load(f)
    
    assert "policy" in policy
    assert policy["policy"]["id"] == "NGI_POLICY_V1"
    assert policy["policy"]["version"] == "1.0.0"
    assert policy["policy"]["status"] == "RELEASED"


def test_assessment_template_exists():
    """Test that assessment template exists and is valid."""
    template_path = Path(__file__).parent.parent / "assessments" / "ngi_assessment.template.yaml"
    assert template_path.exists(), "Assessment template should exist"
    
    with open(template_path, "r") as f:
        template = yaml.safe_load(f)
    
    assert "ngi_autoassessment" in template
    assert "domains" in template["ngi_autoassessment"]


def test_clamp_score_valid():
    """Test score clamping with valid inputs."""
    assert ngi_evaluator.clamp_score(0) == 0
    assert ngi_evaluator.clamp_score(3) == 3
    assert ngi_evaluator.clamp_score(5) == 5
    assert ngi_evaluator.clamp_score(2.5) == 2


def test_clamp_score_invalid():
    """Test score clamping with invalid inputs."""
    with pytest.raises(ValueError, match="fuera de rango"):
        ngi_evaluator.clamp_score(6)
    
    with pytest.raises(ValueError, match="fuera de rango"):
        ngi_evaluator.clamp_score(-1)
    
    with pytest.raises(ValueError, match="no numérico"):
        ngi_evaluator.clamp_score("invalid")


def test_maturity_levels():
    """Test maturity level assignment."""
    policy_path = Path(__file__).parent.parent / "policy" / "ngi_policy_v1.yaml"
    with open(policy_path, "r") as f:
        policy = yaml.safe_load(f)
    
    levels = policy["policy"]["maturity_levels"]
    
    assert ngi_evaluator.maturity_from_total(0, levels) == "L1"
    assert ngi_evaluator.maturity_from_total(39, levels) == "L1"
    assert ngi_evaluator.maturity_from_total(40, levels) == "L2"
    assert ngi_evaluator.maturity_from_total(59, levels) == "L2"
    assert ngi_evaluator.maturity_from_total(60, levels) == "L3"
    assert ngi_evaluator.maturity_from_total(74, levels) == "L3"
    assert ngi_evaluator.maturity_from_total(75, levels) == "L4"
    assert ngi_evaluator.maturity_from_total(89, levels) == "L4"
    assert ngi_evaluator.maturity_from_total(90, levels) == "L5"
    assert ngi_evaluator.maturity_from_total(100, levels) == "L5"


def test_evaluate_block_hard_gates():
    """Test evaluation with hard gate failures (BLOCK)."""
    policy_path = Path(__file__).parent.parent / "policy" / "ngi_policy_v1.yaml"
    policy = ngi_evaluator.load_yaml(str(policy_path))
    
    assessment = {
        "ngi_autoassessment": {
            "project_id": "TEST",
            "assessment_date": "2026-02-12",
            "assessor": "test",
            "domains": {
                "D1_verificability": {"score": 2, "evidence": [], "notes": ""},  # Hard gate fail
                "D2_transparency": {"score": 3, "evidence": [], "notes": ""},
                "D3_privacy": {"score": 3, "evidence": [], "notes": ""},
                "D4_security": {"score": 3, "evidence": [], "notes": ""},
                "D5_governance": {"score": 3, "evidence": [], "notes": ""},
                "D6_interop": {"score": 3, "evidence": [], "notes": ""},
                "D7_identity": {"score": 3, "evidence": [], "notes": ""},
                "D8_sustainability": {"score": 3, "evidence": [], "notes": ""},
                "D9_antimisinf": {"score": 3, "evidence": [], "notes": ""},
            }
        }
    }
    
    result = ngi_evaluator.evaluate(policy, assessment)
    
    assert result["ngi_autoassessment"]["computed"]["hard_gates_passed"] == False
    assert result["ngi_autoassessment"]["computed"]["publish_decision"] == "BLOCK"


def test_evaluate_warn_soft_total():
    """Test evaluation with soft total gate failure (WARN)."""
    policy_path = Path(__file__).parent.parent / "policy" / "ngi_policy_v1.yaml"
    policy = ngi_evaluator.load_yaml(str(policy_path))
    
    assessment = {
        "ngi_autoassessment": {
            "project_id": "TEST",
            "assessment_date": "2026-02-12",
            "assessor": "test",
            "domains": {
                "D1_verificability": {"score": 3, "evidence": [], "notes": ""},
                "D2_transparency": {"score": 3, "evidence": [], "notes": ""},
                "D3_privacy": {"score": 3, "evidence": [], "notes": ""},
                "D4_security": {"score": 3, "evidence": [], "notes": ""},
                "D5_governance": {"score": 3, "evidence": [], "notes": ""},
                "D6_interop": {"score": 3, "evidence": [], "notes": ""},
                "D7_identity": {"score": 3, "evidence": [], "notes": ""},
                "D8_sustainability": {"score": 2, "evidence": [], "notes": ""},
                "D9_antimisinf": {"score": 3, "evidence": [], "notes": ""},
            }
        }
    }
    
    result = ngi_evaluator.evaluate(policy, assessment)
    
    assert result["ngi_autoassessment"]["computed"]["hard_gates_passed"] == True
    assert result["ngi_autoassessment"]["computed"]["soft_gates_passed"] == False
    assert result["ngi_autoassessment"]["computed"]["publish_decision"] == "WARN"
    # Score: (3/5)*15 + (3/5)*10 + (3/5)*15 + (3/5)*15 + (3/5)*10 + (3/5)*10 + (3/5)*10 + (2/5)*5 + (3/5)*10
    # = 9 + 6 + 9 + 9 + 6 + 6 + 6 + 2 + 6 = 59 (below 70)
    assert result["ngi_autoassessment"]["computed"]["total_score_0_100"] == 59


def test_evaluate_pass():
    """Test evaluation with all gates passed (PASS)."""
    policy_path = Path(__file__).parent.parent / "policy" / "ngi_policy_v1.yaml"
    policy = ngi_evaluator.load_yaml(str(policy_path))
    
    assessment = {
        "ngi_autoassessment": {
            "project_id": "TEST",
            "assessment_date": "2026-02-12",
            "assessor": "test",
            "domains": {
                "D1_verificability": {"score": 4, "evidence": [], "notes": ""},
                "D2_transparency": {"score": 4, "evidence": [], "notes": ""},
                "D3_privacy": {"score": 4, "evidence": [], "notes": ""},
                "D4_security": {"score": 4, "evidence": [], "notes": ""},
                "D5_governance": {"score": 4, "evidence": [], "notes": ""},
                "D6_interop": {"score": 4, "evidence": [], "notes": ""},
                "D7_identity": {"score": 4, "evidence": [], "notes": ""},
                "D8_sustainability": {"score": 4, "evidence": [], "notes": ""},
                "D9_antimisinf": {"score": 4, "evidence": [], "notes": ""},
            }
        }
    }
    
    result = ngi_evaluator.evaluate(policy, assessment)
    
    assert result["ngi_autoassessment"]["computed"]["hard_gates_passed"] == True
    assert result["ngi_autoassessment"]["computed"]["soft_gates_passed"] == True
    assert result["ngi_autoassessment"]["computed"]["publish_decision"] == "PASS"
    # Score: (4/5)*100 = 80
    assert result["ngi_autoassessment"]["computed"]["total_score_0_100"] == 80


def test_evaluate_example_result():
    """Test evaluation with the example result file."""
    policy_path = Path(__file__).parent.parent / "policy" / "ngi_policy_v1.yaml"
    example_path = Path(__file__).parent.parent / "assessments" / "ngi_assessment.result.example.yaml"
    
    policy = ngi_evaluator.load_yaml(str(policy_path))
    assessment = ngi_evaluator.load_yaml(str(example_path))
    
    result = ngi_evaluator.evaluate(policy, assessment)
    
    # Verify calculation: 4*15 + 3*10 + 3*15 + 4*15 + 3*10 + 4*10 + 3*10 + 2*5 + 3*10
    # = (4/5)*15 + (3/5)*10 + (3/5)*15 + (4/5)*15 + (3/5)*10 + (4/5)*10 + (3/5)*10 + (2/5)*5 + (3/5)*10
    # = 12 + 6 + 9 + 12 + 6 + 8 + 6 + 2 + 6 = 67
    assert result["ngi_autoassessment"]["computed"]["total_score_0_100"] == 67
    assert result["ngi_autoassessment"]["computed"]["maturity_level"] == "L3"
    assert result["ngi_autoassessment"]["computed"]["hard_gates_passed"] == True
    assert result["ngi_autoassessment"]["computed"]["soft_gates_passed"] == False
    assert result["ngi_autoassessment"]["computed"]["publish_decision"] == "WARN"


def test_evaluate_default_assessment():
    """Test evaluation with the default assessment file."""
    policy_path = Path(__file__).parent.parent / "policy" / "ngi_policy_v1.yaml"
    assessment_path = Path(__file__).parent.parent / "assessments" / "ngi_assessment.yaml"
    
    policy = ngi_evaluator.load_yaml(str(policy_path))
    assessment = ngi_evaluator.load_yaml(str(assessment_path))
    
    result = ngi_evaluator.evaluate(policy, assessment)
    
    # Verify it evaluates without error
    assert "computed" in result["ngi_autoassessment"]
    assert result["ngi_autoassessment"]["computed"]["publish_decision"] in ["PASS", "WARN", "BLOCK"]
    assert result["ngi_autoassessment"]["computed"]["hard_gates_passed"] == True
    # Updated score after improvements: D1 (3→4), D4 (3→4), D8 (2→3) = +7 points
    assert result["ngi_autoassessment"]["computed"]["total_score_0_100"] == 70
    assert result["ngi_autoassessment"]["computed"]["publish_decision"] == "PASS"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
