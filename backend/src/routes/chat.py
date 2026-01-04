"""
Chat API routes for Phase III AI Chatbot with MCP integration.
"""

import json
import logging
from datetime import datetime
from typing import Annotated, Any, Dict, List, Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_db
from ..dependencies.auth import get_current_user
from ..models.chat import Conversation, Message, MessageRole
from ..mcp.task_server import mcp_server
from ..agents.task_agent import task_agent

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    conversation_id: Optional[UUID] = Field(default=None)
    message: str = Field(..., min_length=1, max_length=10000)


class ToolCallItem(BaseModel):
    """Tool call information for response."""
    tool: str
    arguments: Dict[str, Any] = Field(default_factory=dict)
    result: Optional[Any] = Field(default=None)


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    conversation_id: UUID
    response: str
    tool_calls: Optional[List[ToolCallItem]] = Field(default=None)


async def get_or_create_conversation(
    db: AsyncSession,
    user_id: UUID,
    conversation_id: Optional[UUID] = None,
) -> Conversation:
    """Get existing conversation or create new one."""
    if conversation_id:
        result = await db.execute(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
            )
        )
        conversation = result.scalar_one_or_none()
        if conversation:
            conversation.updated_at = datetime.utcnow()
            await db.commit()
            return conversation
    
    # Create new conversation
    conversation = Conversation(
        id=uuid4(),
        user_id=user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    return conversation


async def save_message(
    db: AsyncSession,
    conversation_id: UUID,
    role: MessageRole,
    content: str,
    tool_calls: Optional[str] = None,
) -> Message:
    """Save message to database."""
    message = Message(
        id=uuid4(),
        conversation_id=conversation_id,
        role=role,
        content=content,
        created_at=datetime.utcnow(),
        tool_calls=tool_calls,
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message


async def get_conversation_history(
    db: AsyncSession,
    conversation_id: UUID,
    user_id: UUID,
) -> List[Dict[str, str]]:
    """Get conversation history for OpenAI."""
    result = await db.execute(
        select(Message)
        .join(Conversation, Message.conversation_id == Conversation.id)
        .where(
            Message.conversation_id == conversation_id,
            Conversation.user_id == user_id,
        )
        .order_by(Message.created_at)
    )
    messages = result.scalars().all()
    
    return [
        {"role": msg.role.value, "content": msg.content}
        for msg in messages
    ]


@router.post("", response_model=ChatResponse)
async def send_chat_message(
    request: ChatRequest,
    current_user_id: Annotated[UUID, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ChatResponse:
    """Send chat message and get AI response with MCP tools."""
    
    if not request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message is required",
        )
    
    if not task_agent.is_configured():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Groq API key not configured",
        )
    
    try:
        # Get or create conversation
        conversation = await get_or_create_conversation(
            db=db,
            user_id=current_user_id,
            conversation_id=request.conversation_id,
        )
        
        # Get conversation history
        history = await get_conversation_history(
            db=db,
            conversation_id=conversation.id,
            user_id=current_user_id,
        )
        
        # Save user message
        await save_message(
            db=db,
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content=request.message.strip(),
        )
        
        # Process with AI agent and MCP tools
        response_text, tool_calls = await task_agent.process_message(
            user_id=str(current_user_id),
            message=request.message,
            conversation_history=history,
            mcp_server=mcp_server
        )
        
        # Save assistant response
        tool_calls_json = None
        if tool_calls:
            tool_calls_json = json.dumps(tool_calls)
        
        await save_message(
            db=db,
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content=response_text,
            tool_calls=tool_calls_json,
        )
        
        # Format response
        tool_calls_list = None
        if tool_calls:
            tool_calls_list = [ToolCallItem(**tc) for tc in tool_calls]
        
        return ChatResponse(
            conversation_id=conversation.id,
            response=response_text,
            tool_calls=tool_calls_list,
        )
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat failed: {str(e)}",
        )


@router.get("/health")
async def chat_health() -> Dict[str, str]:
    """Health check for chat service."""
    return {
        "status": "ok",
        "agent": "configured" if task_agent.is_configured() else "not configured",
        "mcp": "ready"
    }
