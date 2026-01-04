#!/usr/bin/env python3

import asyncio
import sys
import os
sys.path.append('/workspaces/simple/backend/src')

from backend.src.agents.task_agent import task_agent
from backend.src.mcp.task_server import mcp_server

async def test_full_chatbot():
    user_id = "9a6a3993-91a6-41fe-9644-6e7089c0928c"
    
    print("=== Testing Full Chatbot Functionality ===\n")
    
    # Test 1: Add task
    print("1. Adding task...")
    response, _ = await task_agent.process_message(
        user_id=user_id,
        message="Add buy groceries to my tasks",
        conversation_history=[],
        mcp_server=mcp_server
    )
    print(f"Response: {response}\n")
    
    # Test 2: List tasks
    print("2. Listing tasks...")
    response, _ = await task_agent.process_message(
        user_id=user_id,
        message="Show me all my tasks",
        conversation_history=[],
        mcp_server=mcp_server
    )
    print(f"Response: {response}\n")
    
    # Test 3: Complete task
    print("3. Completing task...")
    response, _ = await task_agent.process_message(
        user_id=user_id,
        message="Mark buy milk as completed",
        conversation_history=[],
        mcp_server=mcp_server
    )
    print(f"Response: {response}\n")
    
    # Test 4: Delete task
    print("4. Deleting task...")
    response, _ = await task_agent.process_message(
        user_id=user_id,
        message="Delete buy groceries task",
        conversation_history=[],
        mcp_server=mcp_server
    )
    print(f"Response: {response}\n")

if __name__ == "__main__":
    asyncio.run(test_full_chatbot())