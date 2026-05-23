"""
Validation rule engine.
Executes validation rules against data.
"""

import logging
from typing import Any, Dict, List, Callable

import pandas as pd

logger = logging.getLogger(__name__)


class ValidationRule:
    """Represents a single validation rule."""
    
    def __init__(self, name: str, condition: Callable, error_message: str):
        """
        Initialize validation rule.
        
        Args:
            name: Rule name
            condition: Validation function
            error_message: Message on validation failure
        """
        self.name = name
        self.condition = condition
        self.error_message = error_message
    
    def validate(self, data: pd.DataFrame) -> tuple[bool, str]:
        """Execute validation rule."""
        try:
            result = self.condition(data)
            return result, self.error_message if not result else ""
        except Exception as e:
            return False, f"Rule execution error: {str(e)}"


class RuleEngine:
    """Execute validation rules against data."""
    
    def __init__(self):
        """Initialize rule engine."""
        self.logger = logger
        self.rules: List[ValidationRule] = []
    
    def add_rule(self, rule: ValidationRule) -> None:
        """Add validation rule."""
        self.rules.append(rule)
    
    def validate_all(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Execute all validation rules.
        
        Args:
            data: Data to validate
            
        Returns:
            dict: Validation results
        """
        results = {
            "valid": True,
            "passed_rules": [],
            "failed_rules": [],
            "errors": []
        }
        
        for rule in self.rules:
            passed, error_msg = rule.validate(data)
            
            if passed:
                results["passed_rules"].append(rule.name)
            else:
                results["valid"] = False
                results["failed_rules"].append(rule.name)
                results["errors"].append({
                    "rule": rule.name,
                    "message": error_msg
                })
        
        return results
