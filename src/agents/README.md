# Multi-Agent Architecture

Autonomous agent coordination framework for distributed task execution and data processing.

## Overview

The agent system provides:
- **Agent Orchestrator** - Manages agent lifecycle and workflows
- **Worker Agents** - Specialized autonomous agents
- **Message Broker** - Inter-agent communication
- **Workflow Execution** - Complex multi-agent workflows

## Architecture

```
Orchestrator
    ├── Agent 1 (Data Processor)
    ├── Agent 2 (Analyzer)
    └── Agent 3 (Reporter)
        ↓
    Message Broker (communication)
```

## Agent Orchestrator

### Setup

```python
from src.agents.orchestrator.agent_orchestrator import (
    AgentOrchestrator,
    Agent,
    AgentStatus
)

# Create orchestrator
orchestrator = AgentOrchestrator()

# Register agents
agent1 = Agent("DataProcessor", "data_processor")
agent2 = Agent("DataAnalyzer", "analyzer")

orchestrator.register_agent(agent1)
orchestrator.register_agent(agent2)
```

### Workflow Execution

```python
# Define workflow
workflow = {
    "name": "data_processing_workflow",
    "tasks": [
        {
            "agent": "DataProcessor",
            "pipeline": "etl_pipeline_1",
            "input": "data/raw/input.csv"
        },
        {
            "agent": "DataAnalyzer",
            "analysis_type": "statistical_analysis",
            "input_from": "DataProcessor"
        }
    ]
}

# Execute workflow
success = orchestrator.execute_workflow(workflow)
```

## Worker Agents

### Data Processor Agent

```python
from src.agents.workers.data_processor_agent import DataProcessorAgent

agent = DataProcessorAgent()

task = {
    "pipeline": "etl_pipeline_1",
    "config": {
        "source": "data/raw/input.csv",
        "destination": "data/processed/output.csv"
    }
}

success = agent.execute(task)
```

### Creating Custom Agents

```python
from src.agents.orchestrator.agent_orchestrator import Agent

class AnalysisAgent(Agent):
    def __init__(self, name: str = "AnalysisAgent"):
        super().__init__(name, "analyzer")
    
    def execute(self, task: Dict[str, Any]) -> bool:
        try:
            analysis_type = task.get("analysis_type")
            data_source = task.get("data_source")
            
            # Perform analysis
            results = self.perform_analysis(analysis_type, data_source)
            
            self.result = {
                "analysis_type": analysis_type,
                "results": results
            }
            
            return True
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            return False
    
    def perform_analysis(self, analysis_type: str, data_source: str):
        # Implement analysis logic
        pass
```

## Message Broker

### Setup

```python
from src.agents.communication.message_broker import MessageBroker, Message

broker = MessageBroker()

# Register message handlers
def handle_processor_output(message: Message):
    print(f"Received message: {message.content}")

broker.register_handler("DataAnalyzer", handle_processor_output)
```

### Sending Messages

```python
# Create and send message
message = Message(
    sender="DataProcessor",
    receiver="DataAnalyzer",
    content={
        "type": "pipeline_complete",
        "rows_processed": 10000,
        "output_file": "data/processed/output.csv"
    }
)

broker.send_message(message)
```

## Workflow Examples

### ETL Pipeline Workflow

```python
workflow = {
    "name": "etl_pipeline_workflow",
    "tasks": [
        {
            "agent": "DataProcessor",
            "task_type": "extract_transform_load",
            "pipeline": "customer_data_pipeline",
            "source": "raw_customers.csv",
            "destination": "processed_customers.csv"
        }
    ]
}

orchestrator.execute_workflow(workflow)
```

### Analysis Workflow

```python
workflow = {
    "name": "analysis_workflow",
    "tasks": [
        {
            "agent": "DataProcessor",
            "pipeline": "data_prep"
        },
        {
            "agent": "AnalysisAgent",
            "analysis_type": "statistical_analysis"
        },
        {
            "agent": "ReportAgent",
            "report_type": "executive_summary"
        }
    ]
}

orchestrator.execute_workflow(workflow)
```

## Agent States

```
IDLE → RUNNING → COMPLETED
              ↘ FAILED
              ↘ PAUSED
```

## Error Handling

```python
try:
    success = orchestrator.execute_workflow(workflow)
    if not success:
        logger.error("Workflow execution failed")
except AgentException as e:
    logger.error(f"Agent error: {e.message}")
```

## Monitoring

```python
# Check agent status
for agent_name, agent in orchestrator.agents.items():
    print(f"{agent_name}: {agent.status.value}")
    if agent.result:
        print(f"  Result: {agent.result}")
```

## Scalability

- **Horizontal Scaling** - Add more agent instances
- **Load Balancing** - Distribute tasks across agents
- **Resource Management** - Monitor CPU, memory usage
- **Queue Management** - Task queue for pending work

## Best Practices

1. **Idempotency** - Tasks should be safely re-runnable
2. **Timeouts** - Set execution timeouts
3. **Logging** - Log all agent activities
4. **Error Recovery** - Implement retry logic
5. **Monitoring** - Track agent performance
6. **Documentation** - Document agent responsibilities

## Testing

```bash
pytest tests/integration/test_workflows.py -v
```

## Advanced Topics

### Dynamic Agent Creation

```python
def create_agent_pool(count: int, agent_type: str):
    agents = []
    for i in range(count):
        agent = Agent(f"{agent_type}_{i}", agent_type)
        agents.append(agent)
    return agents
```

### Conditional Workflows

```python
workflow = {
    "name": "conditional_workflow",
    "tasks": [
        {
            "agent": "DataProcessor",
            "pipeline": "etl"
        }
    ],
    "conditions": [
        {
            "if": "rows_processed > 1000",
            "then": {"agent": "AnalysisAgent", "analysis_type": "deep_analysis"}
        }
    ]
}
```

## Documentation

See [docs/architecture/](../../docs/architecture/) for detailed agent architecture patterns.
