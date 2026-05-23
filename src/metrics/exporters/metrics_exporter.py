"""
Metrics exporters.
Export collected metrics to external systems.
"""

import logging
import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class MetricsExporter(ABC):
    """Abstract base class for metrics exporters."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize exporter.
        
        Args:
            config: Export configuration
        """
        self.config = config
        self.logger = logger
    
    @abstractmethod
    def export(self, metrics: List[Dict[str, Any]]) -> bool:
        """Export metrics to destination."""
        pass


class JSONExporter(MetricsExporter):
    """Export metrics to JSON file."""
    
    def export(self, metrics: List[Dict[str, Any]]) -> bool:
        """
        Export metrics to JSON.
        
        Args:
            metrics: List of metrics to export
            
        Returns:
            bool: Success status
        """
        try:
            output_file = self.config.get("output_file", "metrics.json")
            
            with open(output_file, "w") as f:
                json.dump({
                    "metrics": metrics,
                    "count": len(metrics)
                }, f, indent=2, default=str)
            
            self.logger.info(f"Exported {len(metrics)} metrics to {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Export failed: {str(e)}")
            return False
