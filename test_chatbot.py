#!/usr/bin/env python3

import asyncio
import sys
import os
sys.path.append('/workspaces/simple/backend/src')

from backend.src.agents.task_agent import task_agent
from backend.src.mcp.task_server import mcp_server

async def test_chatbot():
    print("Testing Groq chatbot...")
    
    # Test if agent is configured
    print(f"Agent configured: {task_agent.is_configured()}")
    
    # Test simple message
    try:
        response, tool_calls = await task_agent.process_message(
            user_id="9a6a3993-91a6-41fe-9644-6e7089c0928c",
            message="Add buy milk to my tasks",
            conversation_history=[],
            mcp_server=mcp_server
        )
        
        print(f"Response: {response}")
        print(f"Tool calls: {tool_calls}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_chatbot())