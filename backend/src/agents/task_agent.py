"""
Groq Agent with MCP Tool Integration - Fixed Version.
"""

import json
import os
from typing import Any, Dict, List, Optional

from groq import Groq


class TaskAgent:
    """AI Agent for task management using Groq."""
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = None
        self.model = "llama-3.1-8b-instant"  # Fast and reliable model for function calling
        self.timeout = 10
        
    def _get_client(self):
        """Lazy initialization of Groq client."""
        if self.client is None and self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                print(f"Failed to initialize Groq client: {e}")
                self.client = None
        return self.client
        
    def get_system_prompt(self) -> str:
        """Get the system prompt for the agent."""
        return """You are a helpful task management assistant.

For greetings (hi, hello), respond warmly and ask how you can help.

IMPORTANT PARSING RULES:
- When user says "rename X to Y" or "update X to Y": 
  * Extract X as current_title (the old name)
  * Extract Y as title (the new name)
  * Use update_task with both parameters
- When user says "show all task" or "list tasks", use list_tasks
- When user says "delete [task]", use delete_task with title=[task]
- When adding NEW tasks, only use description if user explicitly provides one
- Do NOT make up descriptions
- Use exact titles as provided

EXAMPLES:
- "rename buy biryani to buy tikka" → update_task(current_title="buy biryani", title="buy tikka")
- "update buy milk to get milk" → update_task(current_title="buy milk", title="get milk")

Available tools:
- add_task: Create NEW tasks only
- update_task: Modify existing tasks (MUST provide current_title to find task, then new title)
- list_tasks: Show tasks  
- delete_task: Remove tasks (use title to find and delete)
- complete_task: Mark as done

Always be friendly and execute the right tool for each request."""

    def get_tools_schema(self) -> List[Dict[str, Any]]:
        """Get function calling schema for MCP tools."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new task with title and optional description",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Task title - use exactly what user says"},
                            "description": {"type": "string", "description": "Task description - only include if user explicitly provides one"}
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "Show all tasks",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "enum": ["all", "pending", "completed"], "description": "Filter by status"}
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task by title",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Task title to delete"}
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update or rename a task. MUST extract current_title (old name) and title (new name) from user message. Example: 'rename X to Y' means current_title=X, title=Y",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "current_title": {"type": "string", "description": "Current task title to find (the old name before 'to')"},
                            "title": {"type": "string", "description": "New title to set (the new name after 'to')"},
                            "description": {"type": "string", "description": "New description (optional)"}
                        },
                        "required": ["current_title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark task as complete",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Task title to complete"}
                        },
                        "required": ["title"]
                    }
                }
            }
        ]

    async def process_message(
        self,
        user_id: str,
        message: str,
        conversation_history: List[Dict[str, str]],
        mcp_server
    ) -> tuple[str, Optional[List[Dict[str, Any]]]]:
        """Process user message and return response with tool calls."""
        
        # Check for simple greetings first
        msg_lower = message.lower().strip()
        if msg_lower in ['hi', 'hello', 'hey', 'salam', 'assalam']:
            return "Hello! 😊 How can I help you with your tasks today?", None
        
        # Handle rename/update operations directly for better reliability
        if ('rename' in msg_lower or 'update' in msg_lower) and ' to ' in msg_lower:
            return await self._handle_rename_update(user_id, message, mcp_server)
        
        # Fallback if Groq not configured
        if not self.is_configured():
            return await self._fallback_process(user_id, message, mcp_server)
        
        # Build messages
        messages = [{"role": "system", "content": self.get_system_prompt()}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": message})
        
        try:
            client = self._get_client()
            if not client:
                return await self._fallback_process(user_id, message, mcp_server)
                
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.get_tools_schema(),
                tool_choice="auto",
                temperature=0.1,
                max_tokens=200,
                timeout=self.timeout
            )
            
            message_obj = response.choices[0].message
            response_text = message_obj.content or ""
            
            tool_calls = []
            
            # Process tool calls if any
            if message_obj.tool_calls:
                for tool_call in message_obj.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # Add user_id to all tool calls
                    function_args["user_id"] = user_id
                    
                    # Execute MCP tool
                    tool_result = await mcp_server.call_tool(function_name, function_args)
                    
                    # Extract result text
                    result_text = tool_result[0].text if tool_result else "No result"
                    
                    tool_calls.append({
                        "tool": function_name,
                        "arguments": function_args,
                        "result": json.loads(result_text) if result_text.startswith(('{', '[')) else {"message": result_text}
                    })
                
                # Generate response based on tool results
                response_text = self._generate_tool_response(tool_calls)
            
            return response_text, tool_calls if tool_calls else None
            
        except Exception as e:
            return f"I encountered an error: {str(e)}", None
    async def _handle_rename_update(self, user_id: str, message: str, mcp_server):
        """Handle rename/update operations directly for better reliability."""
        try:
            # Parse the rename/update command
            msg_lower = message.lower()
            
            # Split on ' to ' to get old and new titles
            if ' to ' in message:
                parts = message.split(' to ', 1)  # Split only on first occurrence
                if len(parts) == 2:
                    # Extract old title (remove 'rename' or 'update' prefix)
                    old_part = parts[0].strip()
                    for prefix in ['rename', 'update']:
                        if old_part.lower().startswith(prefix):
                            old_part = old_part[len(prefix):].strip()
                            break
                    
                    # Extract new title (remove quotes if present)
                    new_title = parts[1].strip().strip('"').strip("'")
                    
                    if old_part and new_title:
                        # Call the update function directly
                        result = await mcp_server.call_tool("update_task", {
                            "user_id": user_id,
                            "current_title": old_part,
                            "title": new_title
                        })
                        
                        # Parse result
                        if result and result[0].text:
                            result_data = json.loads(result[0].text)
                            if result_data.get("status") == "updated":
                                return f"✏️ I've updated '{old_part}' to '{new_title}' successfully!", [{
                                    "tool": "update_task",
                                    "arguments": {"user_id": user_id, "current_title": old_part, "title": new_title},
                                    "result": result_data
                                }]
                            else:
                                return f"❌ Task '{old_part}' not found. Please check the task name.", None
            
            return "❌ Please use format: 'rename [old name] to [new name]'", None
            
        except Exception as e:
            return f"❌ Error updating task: {str(e)}", None
        """Simple fallback when Groq not available."""
        msg = message.lower()
        
        # Handle rename operations
        if 'rename' in msg and ' to ' in msg:
            parts = message.split(' to ')
            if len(parts) == 2:
                old_title = parts[0].replace('rename', '').strip()
                new_title = parts[1].strip().strip('"').strip("'")
                try:
                    result = await mcp_server._update_task({
                        "user_id": user_id, 
                        "current_title": old_title, 
                        "title": new_title
                    })
                    return f"✏️ I've updated '{old_title}' to '{new_title}' successfully!", None
                except Exception as e:
                    return f"❌ Couldn't rename task: {str(e)}", None
        
        # Handle update operations
        if 'update' in msg and ' to ' in msg:
            parts = message.split(' to ')
            if len(parts) == 2:
                old_title = parts[0].replace('update', '').strip()
                new_title = parts[1].strip().strip('"').strip("'")
                try:
                    result = await mcp_server._update_task({
                        "user_id": user_id, 
                        "current_title": old_title, 
                        "title": new_title
                    })
                    return f"✏️ I've updated '{old_title}' to '{new_title}' successfully!", None
                except Exception as e:
                    return f"❌ Couldn't update task: {str(e)}", None
        
        if 'add' in msg:
            title = message.replace('add', '').strip()
            if title:
                result = await mcp_server._add_task({"user_id": user_id, "title": title})
                return f"✅ Added '{title}' to your tasks!", None
        
        if 'show' in msg or 'list' in msg:
            result = await mcp_server._list_tasks({"user_id": user_id, "status": "all"})
            return "📋 Your tasks are listed above.", None
        
        return "I can help you add, show, delete, or update tasks. Try 'add buy milk' or 'show tasks'.", None
    
    def _generate_tool_response(self, tool_calls: List[Dict[str, Any]]) -> str:
        """Generate friendly response based on tool calls."""
        if not tool_calls:
            return "I'm here to help with your tasks!"
        
        tool_call = tool_calls[0]
        tool_name = tool_call["tool"]
        result = tool_call.get("result", {})
        
        if tool_name == "add_task":
            title = result.get("title", "task")
            return f"✅ I've added '{title}' to your task list!"
        
        elif tool_name == "list_tasks":
            try:
                # Handle different result formats
                if isinstance(result, list):
                    tasks = result
                elif isinstance(result, dict):
                    tasks = result.get("data", result.get("tasks", []))
                else:
                    tasks = []
                
                if not tasks:
                    return "📝 You don't have any tasks yet."
                
                task_list = "📋 **Your Tasks:**\n\n"
                for i, task in enumerate(tasks, 1):
                    if not isinstance(task, dict):
                        continue
                    status = "✅" if task.get("completed") else "⏳"
                    title = task.get('title', 'Untitled')
                    desc = task.get('description', '')
                    task_list += f"{i}. {status} {title}"
                    if desc:
                        task_list += f" - {desc}"
                    task_list += "\n"
                return task_list
            except Exception as e:
                return f"Found tasks but couldn't display them: {str(e)}"
        
        elif tool_name == "delete_task":
            title = result.get("title", "task")
            return f"🗑️ I've removed '{title}' from your task list."
        
        elif tool_name == "update_task":
            if result.get("status") == "updated":
                title = result.get("title", "task")
                args = tool_call.get("arguments", {})
                old_title = args.get("current_title", "task")
                return f"✏️ I've updated '{old_title}' to '{title}' successfully!"
            else:
                return "❌ Task not found or couldn't be updated. Please check the task name."
        
        elif tool_name == "complete_task":
            title = result.get("title", "task")
            return f"🎉 Great! I've marked '{title}' as completed!"
        
        return "Task operation completed!"

    def is_configured(self) -> bool:
        """Check if Groq API key is configured."""
        return bool(self.api_key)


# Global agent instance
task_agent = TaskAgent()