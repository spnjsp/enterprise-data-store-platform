"""
Base pipeline class for ETL operations.
Provides framework for defining, executing, and monitoring ETL jobs.
"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd

logger = logging.getLogger(__name__)


class ETLPipeline(ABC):
    """
    Abstract base class for ETL pipelines.
    
    Defines standard ETL workflow: Extract -> Transform -> Load
    """
    
    def __init__(self, name: str, version: str = "1.0.0"):
        """
        Initialize ETL pipeline.
        
        Args:
            name: Pipeline name
            version: Pipeline version
        """
        self.name = name
        self.version = version
        self.logger = logger
        self.start_time: datetime = None
        self.end_time: datetime = None
        self.status = "INITIALIZED"
        self.metrics: Dict[str, Any] = {}
    
    @abstractmethod
    def extract(self) -> pd.DataFrame:
        """Extract data from source."""
        pass
    
    @abstractmethod
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Transform extracted data."""
        pass
    
    @abstractmethod
    def load(self, data: pd.DataFrame) -> bool:
        """Load transformed data to destination."""
        pass
    
    def execute(self) -> bool:
        """
        Execute complete ETL pipeline.
        
        Returns:
            bool: Success status
        """
        try:
            self.start_time = datetime.utcnow()
            self.status = "RUNNING"
            
            self.logger.info(f"Starting ETL pipeline: {self.name} v{self.version}")
            
            # Extract
            data = self.extract()
            self.metrics["extracted_rows"] = len(data)
            
            # Transform
            data = self.transform(data)
            self.metrics["transformed_rows"] = len(data)
            
            # Load
            success = self.load(data)
            self.metrics["loaded_rows"] = len(data) if success else 0
            
            self.end_time = datetime.utcnow()
            self.status = "COMPLETED" if success else "FAILED"
            
            return success
            
        except Exception as e:
            self.logger.error(f"Pipeline execution failed: {str(e)}")
            self.status = "ERROR"
            raise
