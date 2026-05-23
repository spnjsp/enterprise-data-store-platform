"""
Layout manager for dashboard organization.
Manages page layouts and component arrangement.
"""

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class Layout:
    """Dashboard layout definition."""
    
    def __init__(self, name: str):
        """
        Initialize layout.
        
        Args:
            name: Layout name
        """
        self.name = name
        self.components: List[Dict[str, Any]] = []
        self.logger = logger
    
    def add_component(self, component_type: str, props: Dict[str, Any]) -> None:
        """
        Add component to layout.
        
        Args:
            component_type: Type of component (chart, metric, table, etc.)
            props: Component properties
        """
        self.components.append({
            "type": component_type,
            "props": props
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert layout to dictionary."""
        return {
            "name": self.name,
            "components": self.components,
            "component_count": len(self.components)
        }
