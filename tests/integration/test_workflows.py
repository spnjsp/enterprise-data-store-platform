"""
Integration tests for complete workflows.
"""

import unittest
from src.agents.orchestrator.agent_orchestrator import AgentOrchestrator, Agent


class TestAgentOrchestrator(unittest.TestCase):
    """Test cases for agent orchestrator."""
    
    def setUp(self):
        """Setup test fixtures."""
        self.orchestrator = AgentOrchestrator()
    
    def test_agent_registration(self):
        """Test agent registration."""
        agent = Agent("TestAgent", "test")
        self.orchestrator.register_agent(agent)
        self.assertIn("TestAgent", self.orchestrator.agents)
    
    def test_workflow_execution(self):
        """Test workflow execution."""
        workflow = {
            "name": "test_workflow",
            "tasks": []
        }
        result = self.orchestrator.execute_workflow(workflow)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
