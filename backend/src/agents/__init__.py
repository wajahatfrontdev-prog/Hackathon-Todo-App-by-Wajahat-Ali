"""
Groq API configuration for Phase III AI Chatbot.

This module provides agent initialization with MCP tools for task management.
"""

import logging
from typing import Optional

from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

import os

# Groq API key
GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    logging.warning("GROQ_API_KEY not configured - agent will not function")

# Default model for agent
DEFAULT_MODEL: str = "llama-3.1-70b-versatile"

logger = logging.getLogger(__name__)


class ChatAgent:
    """
    Groq API wrapper for the todo chat agent.

    This class initializes the agent with MCP tools and provides
    methods for running conversations.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
    ):
        """
        Initialize the chat agent.

        Args:
            api_key: Groq API key (uses env var if not provided)
            model: Groq model to use (default: llama-3.1-70b-versatile)
        """
        self.api_key = api_key or GROQ_API_KEY
        self.model = model
        self._client: Optional[Groq] = None
        self._agent_initialized = False

    @property
    def client(self) -> Groq:
        """Get or create Groq client."""
        if self._client is None:
            if not self.api_key:
                raise ValueError("GROQ_API_KEY is required")
            self._client = Groq(api_key=self.api_key)
        return self._client

    def is_configured(self) -> bool:
        """Check if agent is properly configured."""
        return self.api_key is not None

    def get_system_prompt(self) -> str:
        """Get the system prompt for the agent."""
        from .prompt import AGENT_SYSTEM_PROMPT

        return AGENT_SYSTEM_PROMPT


# Global agent instance (lazy initialization)
_agent: Optional[ChatAgent] = None


def get_agent() -> ChatAgent:
    """
    Get the global chat agent instance.

    Returns:
        ChatAgent: Configured chat agent

    Note:
        Returns agent even if not configured - caller should check is_configured()
    """
    global _agent
    if _agent is None:
        _agent = ChatAgent()
    return _agent


def create_agent(api_key: str) -> ChatAgent:
    """
    Create a new chat agent with the given API key.

    Args:
        api_key: Groq API key

    Returns:
        ChatAgent: New chat agent instance
    """
    return ChatAgent(api_key=api_key)


__all__ = ["ChatAgent", "get_agent", "create_agent", "GROQ_API_KEY", "DEFAULT_MODEL"]
