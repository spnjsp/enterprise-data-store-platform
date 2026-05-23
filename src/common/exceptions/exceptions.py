"""
Custom exception definitions.
"""


class PlatformException(Exception):
    """Base exception for the platform."""
    
    def __init__(self, message: str, error_code: str = "UNKNOWN"):
        """
        Initialize exception.
        
        Args:
            message: Error message
            error_code: Error code
        """
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ValidationException(PlatformException):
    """Raised when data validation fails."""
    
    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR")


class ETLException(PlatformException):
    """Raised when ETL operations fail."""
    
    def __init__(self, message: str):
        super().__init__(message, "ETL_ERROR")


class ConfigException(PlatformException):
    """Raised when configuration is invalid."""
    
    def __init__(self, message: str):
        super().__init__(message, "CONFIG_ERROR")


class AgentException(PlatformException):
    """Raised when agent operations fail."""
    
    def __init__(self, message: str):
        super().__init__(message, "AGENT_ERROR")
