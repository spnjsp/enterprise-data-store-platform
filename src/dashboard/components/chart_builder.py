"""
Chart builder for creating Plotly visualizations.
Provides factory methods for common chart types.
"""

import logging
from typing import Any, Dict, List, Optional

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

logger = logging.getLogger(__name__)


class ChartBuilder:
    """Build interactive charts with Plotly."""
    
    @staticmethod
    def create_line_chart(
        data: pd.DataFrame,
        x_column: str,
        y_columns: List[str],
        title: str = "Line Chart"
    ) -> go.Figure:
        """
        Create line chart.
        
        Args:
            data: DataFrame with data
            x_column: X-axis column name
            y_columns: Y-axis column names
            title: Chart title
            
        Returns:
            go.Figure: Plotly figure
        """
        fig = go.Figure()
        
        for col in y_columns:
            fig.add_trace(go.Scatter(
                x=data[x_column],
                y=data[col],
                mode="lines+markers",
                name=col
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title=x_column,
            yaxis_title="Value",
            hovermode="x unified"
        )
        
        return fig
    
    @staticmethod
    def create_bar_chart(
        data: pd.DataFrame,
        x_column: str,
        y_column: str,
        title: str = "Bar Chart"
    ) -> go.Figure:
        """
        Create bar chart.
        
        Args:
            data: DataFrame with data
            x_column: X-axis column name
            y_column: Y-axis column name
            title: Chart title
            
        Returns:
            go.Figure: Plotly figure
        """
        fig = go.Figure(data=[
            go.Bar(x=data[x_column], y=data[y_column])
        ])
        
        fig.update_layout(
            title=title,
            xaxis_title=x_column,
            yaxis_title=y_column
        )
        
        return fig
