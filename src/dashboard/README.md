# Dashboard

Interactive Plotly-based visualization interface for real-time monitoring and analytics.

## Overview

The dashboard provides:
- **Real-time Metrics** - Live system and application metrics
- **Data Visualization** - Interactive charts and graphs
- **Pipeline Monitoring** - ETL pipeline status and performance
- **Customizable Layouts** - Flexible dashboard configuration

## Architecture

```
Layout Manager
    ├── Pages
    │   ├── Dashboard Main (overview)
    │   └── (additional pages)
    └── Components
        ├── Chart Builder
        └── (additional components)
```

## Chart Builder

### Creating Charts

```python
from src.dashboard.components.chart_builder import ChartBuilder
import pandas as pd

# Sample data
data = pd.DataFrame({
    "date": pd.date_range("2024-01-01", periods=10),
    "sales": [100, 150, 120, 180, 200, 175, 190, 210, 220, 240],
    "revenue": [1000, 1500, 1200, 1800, 2000, 1750, 1900, 2100, 2200, 2400]
})

# Line chart
fig = ChartBuilder.create_line_chart(
    data=data,
    x_column="date",
    y_columns=["sales", "revenue"],
    title="Sales and Revenue Trend"
)
fig.show()

# Bar chart
fig = ChartBuilder.create_bar_chart(
    data=data,
    x_column="date",
    y_column="sales",
    title="Daily Sales"
)
fig.show()
```

## Dashboard Pages

### Main Dashboard

```python
from src.dashboard.pages.dashboard_main import MainDashboard

dashboard = MainDashboard()
layout = dashboard.create_layout()

# Add metrics
dashboard.add_metric_card(layout, "Total Records", 15000)
dashboard.add_metric_card(layout, "Pipeline Status", "Active")

layout.show()
```

## Layout Manager

### Custom Layout

```python
from src.dashboard.layouts.layout_manager import Layout

# Create layout
layout = Layout("Custom Dashboard")

# Add components
layout.add_component("metric_card", {
    "title": "Total Revenue",
    "value": "$1.2M",
    "trend": "+15%"
})

layout.add_component("chart", {
    "type": "line",
    "title": "Revenue Trend",
    "data_source": "metrics_api"
})

layout.add_component("table", {
    "title": "Recent Transactions",
    "data_source": "transactions_api",
    "columns": ["id", "amount", "date", "status"]
})

print(layout.to_dict())
```

## Integration with Flask

### Flask Routes

```python
from flask import Flask, render_template
from src.dashboard.pages.dashboard_main import MainDashboard

app = Flask(__name__)

@app.route("/dashboard")
def dashboard():
    dashboard = MainDashboard()
    fig = dashboard.create_layout()
    return render_template("dashboard.html", figure=fig.to_html())
```

## Data Sources

Connect dashboard to data sources:

```python
# Real-time metrics
metrics_data = metrics_collector.get_metrics()

# ETL pipeline data
pipeline_status = orchestrator.get_pipeline_status()

# Database queries
query_results = database.execute_query(sql)
```

## Interactivity

Plotly provides interactive features:
- Hover for details
- Click to zoom
- Drag to pan
- Double-click to reset
- Download as PNG

## Styling

Customize appearance:

```python
fig.update_layout(
    template="plotly_dark",
    font=dict(family="Arial", size=12),
    colorway=["#FF6692", "#636EFA"],
    hovermode="x unified"
)
```

## Real-time Updates

Use WebSockets for real-time updates:

```python
# TODO: Implement WebSocket integration
```

## Performance

- **Caching** - Cache static data and computed visualizations
- **Aggregation** - Pre-aggregate large datasets
- **Sampling** - Use sampling for very large datasets
- **Lazy Loading** - Load data on-demand

## Best Practices

1. **Responsive Design** - Works on desktop and mobile
2. **Accessibility** - Clear labels and alt text
3. **Performance** - Optimize for large datasets
4. **Clarity** - Use appropriate chart types
5. **Context** - Provide filters and drill-down options
6. **Updates** - Refresh data at reasonable intervals

## Testing

```bash
pytest tests/unit/ -k dashboard -v
```

## Deployment

Run dashboard with Flask development server:

```bash
python scripts/run_app.py
```

Access at: `http://localhost:5000/dashboard`

## Documentation

See [docs/](../../docs/) for detailed dashboard documentation and examples.
