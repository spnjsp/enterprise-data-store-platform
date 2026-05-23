"""
Base service class for all business logic services.
Provides common patterns for data validation, error handling, and logging.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict

logger = logging.getLogger(__name__)


class BaseService(ABC):
    """
    Abstract base service class.
    All business logic services should inherit from this class.
    """
    
    def __init__(self):
        """Initialize base service with logging."""
        self.logger = logger
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize service resources."""
        pass
    
    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown service resources."""
        pass
    
    def validate_input(self, data: Dict[str, Any]) -> bool:
        """
        Validate input data.
        
        Args:
            data: Input data to validate
            
        Returns:
            bool: True if valid
            
        Raises:
            ValueError: If validation fails
        """
        if not isinstance(data, dict):
            raise ValueError("Input data must be a dictionary")
        return True
