"""
Message broker for agent communication.
Enables asynchronous communication between agents.
"""

import logging
import uuid
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class Message:
    """Represents an agent message."""
    
    def __init__(self, sender: str, receiver: str, content: Dict[str, Any]):
        """
        Initialize message.
        
        Args:
            sender: Sender agent name
            receiver: Receiver agent name
            content: Message content
        """
        self.id = str(uuid.uuid4())
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.timestamp = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "id": self.id,
            "sender": self.sender,
            "receiver": self.receiver,
            "content": self.content,
            "timestamp": self.timestamp.isoformat()
        }


class MessageBroker:
    """Broker for agent message passing."""
    
    def __init__(self):
        """Initialize message broker."""
        self.logger = logger
        self.message_queue: List[Message] = []
        self.handlers: Dict[str, List[Callable]] = {}
    
    def send_message(self, message: Message) -> None:
        """
        Send message.
        
        Args:
            message: Message to send
        """
        self.message_queue.append(message)
        self.logger.info(
            f"Message queued: {message.sender} -> {message.receiver}"
        )
        
        # Trigger handlers
        if message.receiver in self.handlers:
            for handler in self.handlers[message.receiver]:
                handler(message)
    
    def register_handler(self, agent_name: str, handler: Callable) -> None:
        """
        Register message handler.
        
        Args:
            agent_name: Agent name
            handler: Handler function
        """
        if agent_name not in self.handlers:
            self.handlers[agent_name] = []
        self.handlers[agent_name].append(handler)
