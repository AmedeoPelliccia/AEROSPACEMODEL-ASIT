#!/usr/bin/env python3
"""
Constitutional Pylint Plugin

Enforces Article 3 (Technology as Servant) and Article 6 (Human Harm Precedence)
by detecting critical decision paths that lack constitutional safeguards.

This plugin flags functions that:
- Are marked as safety-critical
- Override or bypass human review
- Lack explicit degrade/pause/escalate logic

Usage:
    pylint --load-plugins=constitutional_pylint_plugin <module>
"""

import re
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class ConstitutionalChecker(BaseChecker):
    """
    Pylint checker for constitutional compliance in safety-critical code.
    
    Enforces:
    - Article 3: Technology serves, doesn't replace moral agency
    - Article 6: Human harm has absolute precedence
    """
    
    __implements__ = IAstroidChecker
    
    name = "constitutional"
    priority = -1
    
    msgs = {
        "C9001": (
            "ARTICLE 6 VIOLATION: Critical path requires explicit degrade/pause/escalate logic. "
            "Function '%s' is safety-critical or overrides human authority but lacks "
            "harm-mitigation controls (escalate_to_human, degrade_mode, pause_operation, etc.)",
            "constitution-violation-harm-precedence",
            "Safety-critical functions must implement explicit harm-mitigation logic per Article 6. "
            "Add escalate_to_human(), degrade_mode(), or pause_operation() calls.",
        ),
        "C9002": (
            "ARTICLE 3 VIOLATION: Autonomous override detected without human authorization path. "
            "Function '%s' bypasses human review but lacks accountability mechanism.",
            "constitution-violation-autonomous-override",
            "Functions that override human decisions must maintain accountability per Article 3. "
            "Add human authorization or review mechanisms.",
        ),
    }
    
    def visit_functiondef(self, node):
        """
        Visit function definitions to check for constitutional compliance.
        
        Checks:
        1. Safety-critical functions have harm-mitigation logic
        2. Override/bypass functions maintain human accountability
        3. Critical decision points have traceability
        """
        self._check_safety_critical_safeguards(node)
        self._check_autonomous_override_accountability(node)
    
    def _check_safety_critical_safeguards(self, node):
        """
        Check if safety-critical functions have required safeguards.
        
        A function is considered safety-critical if:
        - Docstring contains "safety" or "critical"
        - Name contains "safety_", "critical_", or "override_"
        - Calls safety-critical APIs
        """
        is_safety_critical = self._is_safety_critical_function(node)
        
        if not is_safety_critical:
            return
        
        # Check for harm-mitigation patterns in function body
        has_mitigation = self._has_harm_mitigation_logic(node)
        
        if not has_mitigation:
            self.add_message(
                "constitution-violation-harm-precedence",
                node=node,
                args=(node.name,)
            )
    
    def _check_autonomous_override_accountability(self, node):
        """
        Check if override/bypass functions maintain accountability.
        
        A function is considered an override if:
        - Name contains "override", "bypass", "autonomous"
        - Docstring mentions overriding human decisions
        """
        is_override = self._is_override_function(node)
        
        if not is_override:
            return
        
        # Check for accountability mechanisms
        has_accountability = self._has_accountability_mechanism(node)
        
        if not has_accountability:
            self.add_message(
                "constitution-violation-autonomous-override",
                node=node,
                args=(node.name,)
            )
    
    def _is_safety_critical_function(self, node):
        """
        Determine if a function is safety-critical.
        """
        # Check docstring
        if node.doc:
            doc_lower = node.doc.lower()
            if any(keyword in doc_lower for keyword in 
                   ["safety", "critical", "safety-critical", "dal a", "dal b"]):
                return True
        
        # Check function name
        name_lower = node.name.lower()
        if any(keyword in name_lower for keyword in 
               ["safety", "critical", "override", "bypass", "emergency"]):
            return True
        
        # Check function body for safety-critical patterns
        body_str = self._get_body_as_string(node)
        if any(re.search(pattern, body_str) for pattern in
               ["override.*human", "bypass.*review", "autonomous.*decision"]):
            return True
        
        return False
    
    def _is_override_function(self, node):
        """
        Determine if a function overrides human authority.
        """
        # Check function name
        name_lower = node.name.lower()
        if any(keyword in name_lower for keyword in 
               ["override", "bypass", "autonomous", "auto_execute"]):
            return True
        
        # Check docstring
        if node.doc:
            doc_lower = node.doc.lower()
            if any(keyword in doc_lower for keyword in 
                   ["override", "bypass", "without human", "autonomous"]):
                return True
        
        return False
    
    def _has_harm_mitigation_logic(self, node):
        """
        Check if function contains harm-mitigation patterns.
        
        Required patterns (at least one):
        - escalate_to_human()
        - degrade_mode()
        - pause_operation()
        - emergency_stop()
        - human_review_required()
        """
        body_str = self._get_body_as_string(node)
        
        mitigation_patterns = [
            r"escalate_to_human\s*\(",
            r"degrade_mode\s*\(",
            r"pause_operation\s*\(",
            r"emergency_stop\s*\(",
            r"human_review_required\s*\(",
            r"request_human_override\s*\(",
            r"safety_fallback\s*\(",
        ]
        
        for pattern in mitigation_patterns:
            if re.search(pattern, body_str):
                return True
        
        return False
    
    def _has_accountability_mechanism(self, node):
        """
        Check if function has accountability mechanisms.
        
        Required patterns (at least one):
        - logging.log()
        - audit_log()
        - record_decision()
        - human_authorization_required()
        """
        body_str = self._get_body_as_string(node)
        
        accountability_patterns = [
            r"logging\.",
            r"audit_log\s*\(",
            r"record_decision\s*\(",
            r"log_override\s*\(",
            r"human_authorization_required\s*\(",
            r"trace_decision\s*\(",
        ]
        
        for pattern in accountability_patterns:
            if re.search(pattern, body_str):
                return True
        
        return False
    
    def _get_body_as_string(self, node):
        """
        Get function body as a string for pattern matching.
        """
        try:
            return node.as_string()
        except Exception:
            return ""


def register(linter):
    """
    Required function for Pylint plugin registration.
    """
    linter.register_checker(ConstitutionalChecker(linter))
