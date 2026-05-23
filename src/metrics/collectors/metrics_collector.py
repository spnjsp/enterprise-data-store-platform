"""
Base metrics collector.
Gathers metrics from system and application sources.
"""

import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class Metric:
    """Represents a single metric."""
    
    def __init__(self, name: str, value: float, unit: str, timestamp: Optional[datetime] = None):
        """
        Initialize metric.
        
        Args:
            name: Metric name
            value: Metric value
            unit: Unit of measurement
            timestamp: Timestamp of metric
        """
        self.name = name
        self.value = value
        self.unit = unit
        self.timestamp = timestamp or datetime.utcnow()
        self.tags: Dict[str, str] = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metric to dictionary."""
        return {
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
            "timestamp": self.timestamp.isoformat(),
            "tags": self.tags
        }


class MetricsCollector(ABC):
    """Abstract base class for metrics collectors."""
    
    def __init__(self, name: str):
        """
        Initialize collector.
        
        Args:
            name: Collector name
        """
        self.name = name
        self.logger = logger
        self.metrics: List[Metric] = []
    
    @abstractmethod
    def collect(self) -> List[Metric]:
        """Collect metrics."""
        pass
    
    def add_metric(self, metric: Metric) -> None:
        """Add metric to collection."""
        self.metrics.append(metric)
    
    def get_metrics(self) -> List[Metric]:
        """Get collected metrics."""
        return self.metrics
    
    def clear_metrics(self) -> None:
        """Clear collected metrics."""
        self.metrics.clear()
