# Metrics Engine

Observability and monitoring system for collecting, aggregating, and exporting system and application metrics.

## Overview

The metrics engine provides:
- **Metrics Collection** - Gather system and application metrics
- **Metric Storage** - Store metrics with timestamps
- **Metrics Export** - Export metrics to various destinations
- **Performance Tracking** - Monitor system performance

## Architecture

```
Application
    ↓
Metrics Collector
    ↓
Metrics Storage
    ↓
Metrics Exporter
    ↓
External Systems
```

## Collectors

### Built-in Collectors

```python
from src.metrics.collectors.metrics_collector import MetricsCollector, Metric

class ApplicationMetricsCollector(MetricsCollector):
    def __init__(self):
        super().__init__("ApplicationMetrics")
    
    def collect(self):
        # Collect metrics
        metrics = [
            Metric("request_count", 1000, "requests"),
            Metric("average_response_time", 45, "ms"),
            Metric("error_rate", 0.5, "%")
        ]
        return metrics
```

### Metric Creation

```python
from src.metrics.collectors.metrics_collector import Metric
from datetime import datetime

metric = Metric(
    name="pipeline_execution_time",
    value=120.5,
    unit="seconds",
    timestamp=datetime.utcnow()
)

metric.tags = {
    "pipeline": "etl_pipeline_1",
    "status": "success"
}

print(metric.to_dict())
```

## Exporters

### JSON Exporter

```python
from src.metrics.exporters.metrics_exporter import JSONExporter

exporter = JSONExporter({
    "output_file": "metrics/output.json"
})

metrics_data = [
    {"name": "request_count", "value": 1000},
    {"name": "response_time", "value": 45}
]

success = exporter.export(metrics_data)
```

### Custom Exporter

```python
from src.metrics.exporters.metrics_exporter import MetricsExporter
from typing import List, Dict, Any

class PrometheusExporter(MetricsExporter):
    def export(self, metrics: List[Dict[str, Any]]) -> bool:
        try:
            # Format metrics for Prometheus
            prometheus_format = self._format_prometheus(metrics)
            
            # Send to Prometheus
            response = requests.post(
                self.config.get("prometheus_url"),
                data=prometheus_format
            )
            
            return response.status_code == 200
            
        except Exception as e:
            self.logger.error(f"Export failed: {str(e)}")
            return False
    
    def _format_prometheus(self, metrics: List[Dict[str, Any]]) -> str:
        # Convert to Prometheus format
        pass
```

## Integration with ETL

Track ETL metrics:

```python
from src.etl.pipelines.pipeline_base import ETLPipeline
from src.metrics.collectors.metrics_collector import MetricsCollector, Metric
import time

class MonitoredPipeline(ETLPipeline):
    def __init__(self):
        super().__init__("MonitoredPipeline", "1.0.0")
        self.metrics_collector = MetricsCollector("PipelineMetrics")
    
    def execute(self) -> bool:
        start_time = time.time()
        
        try:
            # Execute pipeline
            data = self.extract()
            data = self.transform(data)
            success = self.load(data)
            
            # Collect metrics
            duration = time.time() - start_time
            metric = Metric(
                "pipeline_execution_time",
                duration,
                "seconds"
            )
            metric.tags = {"status": "success"}
            
            self.metrics_collector.add_metric(metric)
            
            return success
            
        except Exception as e:
            duration = time.time() - start_time
            metric = Metric(
                "pipeline_execution_time",
                duration,
                "seconds"
            )
            metric.tags = {"status": "failed", "error": str(e)}
            
            self.metrics_collector.add_metric(metric)
            return False
```

## Monitoring Patterns

### Request/Response Tracking

```python
def track_request(operation_name: str):
    start_time = time.time()
    
    try:
        # Perform operation
        result = perform_operation()
        
        # Track success
        duration = time.time() - start_time
        return result
        
    except Exception as e:
        # Track error
        duration = time.time() - start_time
        raise
```

### Resource Monitoring

```python
import psutil

def collect_system_metrics():
    metrics = [
        Metric("cpu_percent", psutil.cpu_percent(), "%"),
        Metric("memory_percent", psutil.virtual_memory().percent, "%"),
        Metric("disk_percent", psutil.disk_usage('/').percent, "%")
    ]
    return metrics
```

## Metric Types

- **Counter** - Incrementing value (total requests)
- **Gauge** - Point-in-time value (CPU usage)
- **Histogram** - Distribution of values (response times)
- **Summary** - Aggregated statistics (percentiles)

## Time Series Metrics

Export time-series data:

```python
from datetime import datetime, timedelta

def collect_timeseries():
    metrics = []
    current_time = datetime.utcnow()
    
    for i in range(10):
        metric = Metric(
            "temperature",
            20 + i,
            "celsius",
            current_time - timedelta(hours=i)
        )
        metrics.append(metric)
    
    return metrics
```

## Performance Baselines

Track performance over time:

```python
baselines = {
    "etl_pipeline_1": {
        "average_execution_time": 120,
        "p95_execution_time": 150,
        "p99_execution_time": 180
    }
}

def check_performance(actual_time, baseline):
    if actual_time > baseline["p99_execution_time"]:
        alert("Pipeline performance degraded")
```

## Alerting

Create alerts based on metrics:

```python
def create_alert_rule(metric_name, threshold, condition):
    return {
        "metric": metric_name,
        "threshold": threshold,
        "condition": condition,  # >, <, ==, !=
        "action": "send_notification"
    }

# Usage
alert = create_alert_rule("error_rate", 5, ">")
```

## Best Practices

1. **Metric Naming** - Use descriptive, hierarchical names
2. **Tags** - Add context with tags/labels
3. **Aggregation** - Pre-aggregate high-volume metrics
4. **Retention** - Define retention policies
5. **Sampling** - Use sampling for high-frequency metrics
6. **Documentation** - Document all metrics collected

## Testing

```bash
pytest tests/unit/ -k metrics -v
```

## Documentation

See [docs/](../../docs/) for detailed metrics documentation.
