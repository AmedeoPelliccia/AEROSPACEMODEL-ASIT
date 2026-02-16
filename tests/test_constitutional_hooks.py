"""
Test suite for constitutional pre-commit hooks.

Tests validate:
1. Commit message validator enforcement
2. Pattern detection for labor displacement
3. Pylint plugin detection of safety violations
"""

import os
import tempfile
import subprocess
from pathlib import Path

try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False

# Change to repo root
repo_root = Path(__file__).parent.parent
os.chdir(repo_root)


def test_commit_validator_valid_message():
    """Test that validator accepts valid constitutional commit message."""
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
        
        assert result.returncode == 0, f"Valid message rejected: {result.stderr}"
        assert "Constitutional commit validated" in result.stdout
    finally:
        os.unlink(temp_file)


def test_commit_validator_missing_sections():
    """Test that validator rejects messages missing required sections."""
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
        
        assert result.returncode != 0, "Message with missing sections should be rejected"
        assert 'AUTHOR' in result.stderr, "Error should mention AUTHOR"
        assert 'HUMAN_IMPACT' in result.stderr, "Error should mention HUMAN_IMPACT"
        assert 'REVERSIBILITY' in result.stderr, "Error should mention REVERSIBILITY"
    finally:
        os.unlink(temp_file)


def test_commit_validator_article_8_violation():
    """Test that validator detects Article 8 violations (workforce reduction)."""
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
        
        assert result.returncode != 0, "Article 8 violation should be detected"
        assert 'ARTICLE 8' in result.stderr, "Error should mention Article 8"
        assert 'reabsorption' in result.stderr.lower(), "Error should mention reabsorption"
    finally:
        os.unlink(temp_file)


def test_commit_validator_article_8_with_reabsorption():
    """Test that validator accepts workforce reduction WITH reabsorption plan."""
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
        
        assert result.returncode == 0, f"Valid reabsorption plan should be accepted: {result.stderr}"
    finally:
        os.unlink(temp_file)


def test_commit_validator_article_6_violation():
    """Test that validator detects Article 6 violations (missing harm mitigation)."""
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
        
        assert result.returncode != 0, "Article 6 violation should be detected"
        assert 'ARTICLE 6' in result.stderr, "Error should mention Article 6"
        assert any(word in result.stderr.lower() for word in ['degrade', 'pause', 'escalate']), \
            "Error should mention harm mitigation paths"
    finally:
        os.unlink(temp_file)


def test_commit_validator_article_6_compliant():
    """Test that validator accepts messages with proper harm mitigation."""
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
        
        assert result.returncode == 0, f"Message with harm mitigation should be accepted: {result.stderr}"
    finally:
        os.unlink(temp_file)


def test_commit_validator_empty_sections():
    """Test that validator rejects messages with empty sections."""
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
        
        assert result.returncode != 0, "Empty/short sections should be rejected"
        assert any(word in result.stderr.lower() for word in ['empty', 'short', 'meaningful']), \
            "Error should mention section content requirements"
    finally:
        os.unlink(temp_file)


def test_commit_validator_multiline_sections():
    """Test that validator correctly parses multi-line sections."""
    multiline_msg = """INTENT: Test multi-line parsing
This is line 2 of the intent
This is line 3 of the intent

RATIONALE: This rationale spans
multiple lines and includes
blank lines in between

HUMAN_IMPACT: Multi-line impact description
with additional context
on multiple lines

REVERSIBILITY: Can degrade to previous state
or escalate to human review
with multiple mitigation paths

AUTHOR: Test Author Team"""
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(multiline_msg)
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ['python3', '.github/hooks/constitutional_commit_validator.py', temp_file],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Multi-line message should be accepted: {result.stderr}"
    finally:
        os.unlink(temp_file)


def test_labor_scanner_detects_patterns():
    """Test that labor scanner detects workforce reduction patterns."""
    content_with_pattern = """This document discusses workforce reduction
and how we will eliminate positions to improve efficiency."""
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(content_with_pattern)
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ['python3', '.github/hooks/labor_reabsorption_scanner.py', temp_file],
            capture_output=True,
            text=True
        )
        
        # Scanner warns but doesn't block (returns 0)
        assert result.returncode == 0
        assert 'LABOR PATTERN DETECTED' in result.stdout
        assert 'reabsorption' in result.stdout.lower()
    finally:
        os.unlink(temp_file)


def test_labor_scanner_clean_file():
    """Test that labor scanner passes clean files."""
    clean_content = """This document discusses improving our processes
without affecting staffing levels."""
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(clean_content)
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ['python3', '.github/hooks/labor_reabsorption_scanner.py', temp_file],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert 'LABOR PATTERN DETECTED' not in result.stdout
    finally:
        os.unlink(temp_file)


# Standalone test runner (when pytest is not available)
if __name__ == "__main__":
    if PYTEST_AVAILABLE:
        import pytest
        pytest.main([__file__, '-v'])
    else:
        import sys
        
        print("=" * 70)
        print("Constitutional Pre-Commit Hooks Test Suite")
        print("Note: Install pytest for better output (pip install pytest)")
        print("=" * 70)
        
        tests = [
            ("Valid message", test_commit_validator_valid_message),
            ("Missing sections", test_commit_validator_missing_sections),
            ("Article 8 violation", test_commit_validator_article_8_violation),
            ("Article 8 compliant", test_commit_validator_article_8_with_reabsorption),
            ("Article 6 violation", test_commit_validator_article_6_violation),
            ("Article 6 compliant", test_commit_validator_article_6_compliant),
            ("Empty sections", test_commit_validator_empty_sections),
            ("Multi-line sections", test_commit_validator_multiline_sections),
            ("Labor scanner detects", test_labor_scanner_detects_patterns),
            ("Labor scanner clean", test_labor_scanner_clean_file),
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            try:
                print(f"\nTest: {test_name}...", end=" ")
                test_func()
                print("✅ PASS")
                passed += 1
            except AssertionError as e:
                print(f"❌ FAIL")
                print(f"   {e}")
                failed += 1
            except Exception as e:
                print(f"❌ ERROR")
                print(f"   {e}")
                failed += 1
        
        print("\n" + "=" * 70)
        print(f"Results: {passed} passed, {failed} failed, {len(tests)} total")
        print("=" * 70)
        
        sys.exit(1 if failed > 0 else 0)
