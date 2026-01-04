"""
MCP Server package for Phase III AI Chatbot.

This package provides:
- server: MCP server with task CRUD tools
- tools: Individual tool implementations

Exports:
- app: MCP Server instance for integration with OpenAI Agents SDK
"""

from .server import app

__all__ = ["app"]
