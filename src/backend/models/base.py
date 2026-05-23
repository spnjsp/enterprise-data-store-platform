"""
Base model classes for ORM entities.
Provides common attributes and methods for all models.
"""

from datetime import datetime
from typing import Optional


class BaseModel:
    """
    Base model class for all ORM entities.
    
    Attributes:
        id: Unique identifier
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
        is_active: Soft delete flag
    """
    
    def __init__(self):
        self.id: Optional[str] = None
        self.created_at: datetime = datetime.utcnow()
        self.updated_at: datetime = datetime.utcnow()
        self.is_active: bool = True
    
    def to_dict(self) -> dict:
        """Convert model to dictionary representation."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_active": self.is_active
        }
