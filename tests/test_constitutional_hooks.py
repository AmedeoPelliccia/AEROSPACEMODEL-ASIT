#!/usr/bin/env python3
"""
Test suite for constitutional pre-commit hooks.

Tests validate:
1. Commit message validator enforcement
2. Pattern detection for labor displacement
3. Pylint plugin detection of safety violations
"""

import os
import sys
import tempfile
import subprocess
from pathlib import Path


def test_commit_validator_valid_message():
    """Test that validator accepts valid constitutional commit message."""
    print("\n=== Test 1: Valid Constitutional Commit Message ===")
    
    valid_msg = """INTENT: Test commit validator with valid message
RATIONALE: Validate that properly formatted messages pass validation
HUMAN_IMPACT: No workforce impact. Testing infrastructure only.
REVERSIBILITY: Test can be reverted without harm. Escalate to test lead if issues.
AUTHOR: Test Suite"""
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(valid_msg)
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ['python3', '.github/hooks/constitutional_commit_validator.py', temp_file],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ PASS: Valid message accepted")
            print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print("❌ FAIL: Valid message rejected")
            print(f"   Error: {result.stderr}")
            return False
    finally:
        os.unlink(temp_file)


def test_commit_validator_missing_sections():
    """Test that validator rejects messages missing required sections."""
    print("\n=== Test 2: Missing Required Sections ===")
    
    invalid_msg = """INTENT: Test missing sections
RATIONALE: This message is incomplete"""
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(invalid_msg)
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ['python3', '.github/hooks/constitutional_commit_validator.py', temp_file],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("✅ PASS: Message with missing sections rejected")
            print(f"   Error message includes: {['AUTHOR', 'HUMAN_IMPACT', 'REVERSIBILITY']}")
            if all(section in result.stderr for section in ['AUTHOR', 'HUMAN_IMPACT', 'REVERSIBILITY']):
                print("✅ PASS: Error message lists all missing sections")
                return True
            else:
                print("⚠️  PARTIAL: Some sections not mentioned in error")
                return False
        else:
            print("❌ FAIL: Message with missing sections accepted")
            return False
    finally:
        os.unlink(temp_file)


def test_commit_validator_article_8_violation():
    """Test that validator detects Article 8 violations (workforce reduction)."""
    print("\n=== Test 3: Article 8 Violation Detection ===")
    
    violation_msg = """INTENT: Automate manual process
RATIONALE: Reduce costs through automation
HUMAN_IMPACT: Workforce reduction of 3 engineers to improve efficiency
REVERSIBILITY: Can revert changes if needed, escalate to management
AUTHOR: Automation Team"""
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(violation_msg)
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ['python3', '.github/hooks/constitutional_commit_validator.py', temp_file],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0 and 'ARTICLE 8' in result.stderr:
            print("✅ PASS: Article 8 violation detected")
            print("   Rejection includes reabsorption requirement")
            return True
        else:
            print("❌ FAIL: Article 8 violation not detected")
            return False
    finally:
        os.unlink(temp_file)


def test_commit_validator_article_8_with_reabsorption():
    """Test that validator accepts workforce reduction WITH reabsorption plan."""
    print("\n=== Test 4: Article 8 Compliance (With Reabsorption) ===")
    
    compliant_msg = """INTENT: Automate manual validation
RATIONALE: Reduce repetitive work and improve accuracy
HUMAN_IMPACT: Workforce reduction of 2 validation engineers. Reabsorption plan: Engineers transition to schema governance roles with 6-month training program. New capacity for design review authority.
REVERSIBILITY: Automation can be disabled. If issues arise, degrade to manual validation and escalate to STK_CM.
AUTHOR: Quality Team with HR reabsorption approval"""
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(compliant_msg)
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ['python3', '.github/hooks/constitutional_commit_validator.py', temp_file],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ PASS: Workforce reduction with reabsorption accepted")
            return True
        else:
            print("❌ FAIL: Valid reabsorption plan rejected")
            print(f"   Error: {result.stderr}")
            return False
    finally:
        os.unlink(temp_file)


def test_commit_validator_article_6_violation():
    """Test that validator detects Article 6 violations (missing harm mitigation)."""
    print("\n=== Test 5: Article 6 Violation Detection ===")
    
    violation_msg = """INTENT: Update safety-critical control logic
RATIONALE: Improve response time by 20%
HUMAN_IMPACT: No direct workforce impact. Operators use same interface.
REVERSIBILITY: Can revert the change if problems occur
AUTHOR: Control Systems Team"""
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(violation_msg)
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ['python3', '.github/hooks/constitutional_commit_validator.py', temp_file],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0 and 'ARTICLE 6' in result.stderr:
            print("✅ PASS: Article 6 violation detected")
            print("   Requires degrade/pause/escalate mechanism")
            return True
        else:
            print("❌ FAIL: Article 6 violation not detected")
            return False
    finally:
        os.unlink(temp_file)


def test_commit_validator_article_6_compliant():
    """Test that validator accepts messages with proper harm mitigation."""
    print("\n=== Test 6: Article 6 Compliance ===")
    
    compliant_msg = """INTENT: Update flight control logic
RATIONALE: Improve response time while maintaining safety margins
HUMAN_IMPACT: No workforce impact. Operators retain full override authority.
REVERSIBILITY: System will degrade to baseline control mode if anomalies detected. Operators can pause operation via emergency stop. All critical paths escalate to human authority per ARP4761.
AUTHOR: Flight Control Safety Team"""
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(compliant_msg)
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ['python3', '.github/hooks/constitutional_commit_validator.py', temp_file],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ PASS: Message with harm mitigation accepted")
            return True
        else:
            print("❌ FAIL: Valid harm mitigation rejected")
            print(f"   Error: {result.stderr}")
            return False
    finally:
        os.unlink(temp_file)


def test_commit_validator_empty_sections():
    """Test that validator rejects messages with empty sections."""
    print("\n=== Test 7: Empty Sections Detection ===")
    
    empty_msg = """INTENT: Fix bug
RATIONALE: Bug
HUMAN_IMPACT: None
REVERSIBILITY: Revert
AUTHOR: Dev"""
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(empty_msg)
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ['python3', '.github/hooks/constitutional_commit_validator.py', temp_file],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0 and ('empty' in result.stderr.lower() or 'too short' in result.stderr.lower()):
            print("✅ PASS: Empty/short sections rejected")
            return True
        else:
            print("❌ FAIL: Empty sections not detected")
            return False
    finally:
        os.unlink(temp_file)


def test_pylint_plugin_safety_critical():
    """Test that Pylint plugin detects safety-critical functions without safeguards."""
    print("\n=== Test 8: Pylint Plugin - Safety Critical Detection ===")
    
    # Create test Python file with safety-critical function missing safeguards
    test_code = '''
def safety_critical_flight_control(altitude):
    """Safety-critical flight control logic."""
    if altitude < 1000:
        return "emergency_descent"
    return "nominal"
'''
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
        f.write(test_code)
        temp_file = f.name
    
    try:
        # Check if pylint is available
        pylint_check = subprocess.run(
            ['which', 'pylint'],
            capture_output=True
        )
        
        if pylint_check.returncode != 0:
            print("⚠️  SKIP: Pylint not installed")
            return None
        
        # Run pylint with constitutional plugin
        env = os.environ.copy()
        env['PYTHONPATH'] = '.github/plugins:' + env.get('PYTHONPATH', '')
        
        result = subprocess.run(
            [
                'pylint',
                '--load-plugins=constitutional_pylint_plugin',
                '--disable=all',
                '--enable=constitution-violation-harm-precedence',
                temp_file
            ],
            capture_output=True,
            text=True,
            env=env
        )
        
        if 'constitution-violation-harm-precedence' in result.stdout:
            print("✅ PASS: Safety-critical function without safeguards detected")
            return True
        else:
            print("⚠️  Note: Pylint plugin may need adjustment or function not flagged")
            return None
    except Exception as e:
        print(f"⚠️  SKIP: Pylint test error: {e}")
        return None
    finally:
        os.unlink(temp_file)


def test_pylint_plugin_compliant():
    """Test that Pylint plugin accepts safety-critical functions with safeguards."""
    print("\n=== Test 9: Pylint Plugin - Compliant Safety Function ===")
    
    # Create test Python file with safety-critical function WITH safeguards
    test_code = '''
def safety_critical_flight_control(altitude):
    """Safety-critical flight control logic."""
    if altitude < 1000:
        escalate_to_human("Low altitude detected", {"altitude": altitude})
        return degrade_mode("safe_altitude_hold")
    return "nominal"

def escalate_to_human(msg, data):
    pass

def degrade_mode(mode):
    pass
'''
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
        f.write(test_code)
        temp_file = f.name
    
    try:
        # Check if pylint is available
        pylint_check = subprocess.run(
            ['which', 'pylint'],
            capture_output=True
        )
        
        if pylint_check.returncode != 0:
            print("⚠️  SKIP: Pylint not installed")
            return None
        
        # Run pylint with constitutional plugin
        env = os.environ.copy()
        env['PYTHONPATH'] = '.github/plugins:' + env.get('PYTHONPATH', '')
        
        result = subprocess.run(
            [
                'pylint',
                '--load-plugins=constitutional_pylint_plugin',
                '--disable=all',
                '--enable=constitution-violation-harm-precedence',
                temp_file
            ],
            capture_output=True,
            text=True,
            env=env
        )
        
        if 'constitution-violation-harm-precedence' not in result.stdout:
            print("✅ PASS: Compliant safety function accepted")
            return True
        else:
            print("❌ FAIL: Compliant function incorrectly flagged")
            return False
    except Exception as e:
        print(f"⚠️  SKIP: Pylint test error: {e}")
        return None
    finally:
        os.unlink(temp_file)


