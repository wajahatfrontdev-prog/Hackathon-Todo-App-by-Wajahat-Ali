"""
MCP Server for Phase III AI Chatbot.

This module provides the MCP server that exposes task CRUD tools
using the Official MCP SDK. The server is initialized once and
used by the OpenAI Agents SDK.

The MCP server exposes the following tools:
- add_task: Create a new task
- list_tasks: List user's tasks (optionally filtered by status)
- complete_task: Mark a task as complete
- update_task: Update task title or due date
- delete_task: Delete a task
"""

import json
import logging
from datetime import datetime, date
from typing import Any, Dict

from mcp.server import Server
from mcp.types import Tool, TextContent

from .tools import add_task, complete_task, delete_task, list_tasks, update_task
from ..db import get_db_context
from ..dependencies.auth import verify_token

logger = logging.getLogger(__name__)

# Initialize MCP server with name
app = Server(name="todo-chat")


def _get_user_id_from_token(token: str) -> str:
    """
    Extract user_id from JWT token.

    Args:
        token: JWT token string

    Returns:
        User ID as string

    Raises:
        ValueError: If token is invalid
    """
    is_valid, user_id, error = verify_token(token)
    if not is_valid:
        raise ValueError(f"Invalid token: {error}")
    return str(user_id)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List available MCP tools.

    Returns:
        List of Tool definitions for the task CRUD operations
    """
    return [
        Tool(
            name="add_task",
            description="Create a new task for the user. "
                        "Use this when the user wants to add a new todo item. "
                        "Title is required. Due date is optional.",
            inputSchema={
                "type": "object",
                "properties": {
                    "token": {
                        "type": "string",
                        "description": "JWT authentication token",
                    },
                    "title": {
                        "type": "string",
                        "description": "Task title (required)",
                        "minLength": 1,
                    },
                    "due_date": {
                        "type": "string",
                        "description": "Optional due date in YYYY-MM-DD or ISO format",
                    },
                },
                "required": ["token", "title"],
            },
        ),
        Tool(
            name="list_tasks",
            description="List the user's tasks. "
                        "Can filter by status (pending or complete). "
                        "Use this when the user wants to see their todo list.",
            inputSchema={
                "type": "object",
                "properties": {
                    "token": {
                        "type": "string",
                        "description": "JWT authentication token",
                    },
                    "status": {
                        "type": "string",
                        "description": "Optional filter: 'pending' or 'complete'",
                        "enum": ["pending", "complete"],
                    },
                },
                "required": ["token"],
            },
        ),
        Tool(
            name="complete_task",
            description="Mark a task as complete. "
                        "Use this when the user indicates they finished a task.",
            inputSchema={
                "type": "object",
                "properties": {
                    "token": {
                        "type": "string",
                        "description": "JWT authentication token",
                    },
                    "task_id": {
                        "type": "string",
                        "description": "UUID of the task to complete",
                    },
                },
                "required": ["token", "task_id"],
            },
        ),
        Tool(
            name="update_task",
            description="Update a task's title or due date. "
                        "Use this when the user wants to modify an existing task.",
            inputSchema={
                "type": "object",
                "properties": {
                    "token": {
                        "type": "string",
                        "description": "JWT authentication token",
                    },
                    "task_id": {
                        "type": "string",
                        "description": "UUID of the task to update",
                    },
                    "title": {
                        "type": "string",
                        "description": "New task title (optional)",
                    },
                    "due_date": {
                        "type": "string",
                        "description": "New due date in YYYY-MM-DD or ISO format (optional)",
                    },
                },
                "required": ["token", "task_id"],
            },
        ),
        Tool(
            name="delete_task",
            description="Delete a task. "
                        "Use this when the user wants to remove a task.",
            inputSchema={
                "type": "object",
                "properties": {
                    "token": {
                        "type": "string",
                        "description": "JWT authentication token",
                    },
                    "task_id": {
                        "type": "string",
                        "description": "UUID of the task to delete",
                    },
                },
                "required": ["token", "task_id"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> list[TextContent]:
    """
    Handle MCP tool calls.

    Args:
        name: Tool name
        arguments: Tool arguments from the request

    Returns:
        List of TextContent with the tool result

    Raises:
        ValueError: For invalid arguments or tool errors
    """
    # Extract token and get user_id
    token = arguments.get("token")
    if not token:
        raise ValueError("Authentication token is required")

    try:
        user_id = _get_user_id_from_token(token)
    except ValueError as e:
        raise ValueError(str(e))

    # Remove token from arguments for tool functions
    tool_args = {k: v for k, v in arguments.items() if k != "token"}

    try:
        # Execute tool with database session
        async with get_db_context() as db:
            if name == "add_task":
                result = await add_task(
                    db=db,
                    user_id=user_id,  # type: ignore
                    title=tool_args["title"],
                    due_date=tool_args.get("due_date"),
                )
            elif name == "list_tasks":
                result = await list_tasks(
                    db=db,
                    user_id=user_id,  # type: ignore
                    status=tool_args.get("status"),
                )
            elif name == "complete_task":
                result = await complete_task(
                    db=db,
                    user_id=user_id,  # type: ignore
                    task_id=tool_args["task_id"],
                )
            elif name == "update_task":
                result = await update_task(
                    db=db,
                    user_id=user_id,  # type: ignore
                    task_id=tool_args["task_id"],
                    title=tool_args.get("title"),
                    due_date=tool_args.get("due_date"),
                )
            elif name == "delete_task":
                result = await delete_task(
                    db=db,
                    user_id=user_id,  # type: ignore
                    task_id=tool_args["task_id"],
                )
            else:
                raise ValueError(f"Unknown tool: {name}")

        # Return result as text content
        return [TextContent(type="text", text=json_dumps(result))]

    except ValueError as e:
        # Re-raise validation errors
        raise
    except Exception as e:
        logger.error(f"Tool {name} failed: {e}")
        raise ValueError(f"Tool execution failed: {str(e)}")


def json_dumps(obj: Any) -> str:
    """Serialize object to JSON string with proper datetime handling."""

    class JSONEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, (datetime, date)):
                return o.isoformat()
            if hasattr(o, "__dict__"):
                return o.__dict__
            return str(o)

    return json.dumps(obj, cls=JSONEncoder, indent=2)


# Export the MCP server instance for use with OpenAI Agents SDK
__all__ = ["app"]
