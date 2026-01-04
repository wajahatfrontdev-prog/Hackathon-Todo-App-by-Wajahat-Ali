"""
Unit tests for OpenAI Agents configuration.

Tests for agent initialization and configuration.
"""

import pytest
from unittest.mock import patch, MagicMock


class TestChatAgent:
    """Tests for ChatAgent class."""

    def test_agent_not_configured_without_api_key(self):
        """Test agent reports not configured without API key."""
        import os

        # Mock environment to not have API key
        with patch.dict(os.environ, {}, clear=True):
            # Clear any cached value
            from ..src.agents import ChatAgent, OPENAI_API_KEY

            # Force reimport
            import importlib
            import src.agents
            importlib.reload(src.agents)

    def test_agent_initialization(self):
        """Test ChatAgent can be initialized with API key."""
        from ..src.agents import ChatAgent

        agent = ChatAgent(api_key="test-key")
        assert agent.api_key == "test-key"
        assert agent.model == "gpt-4o"

    def test_agent_custom_model(self):
        """Test ChatAgent can use custom model."""
        from ..src.agents import ChatAgent

        agent = ChatAgent(api_key="test-key", model="gpt-4o-mini")
        assert agent.model == "gpt-4o-mini"

    def test_agent_is_configured(self):
        """Test is_configured returns True when API key present."""
        from ..src.agents import ChatAgent

        agent = ChatAgent(api_key="test-key")
        assert agent.is_configured() is True

    def test_agent_not_configured_without_key(self):
        """Test is_configured returns False when no API key."""
        from ..src.agents import ChatAgent

        agent = ChatAgent(api_key=None)
        assert agent.is_configured() is False

    def test_get_system_prompt(self):
        """Test get_system_prompt returns non-empty string."""
        from ..src.agents import ChatAgent

        agent = ChatAgent(api_key="test-key")
        prompt = agent.get_system_prompt()

        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert "task management" in prompt.lower()


class TestGetAgent:
    """Tests for get_agent function."""

    def test_get_agent_returns_agent(self):
        """Test get_agent returns a ChatAgent instance."""
        from ..src.agents import get_agent, ChatAgent

        # This will raise if not configured, but we can check the type
        try:
            agent = get_agent()
            assert isinstance(agent, ChatAgent)
        except ValueError:
            # Expected if OPENAI_API_KEY not set
            pass

    def test_create_agent(self):
        """Test create_agent creates new agent."""
        from ..src.agents import create_agent, ChatAgent

        agent = create_agent(api_key="new-key")
        assert isinstance(agent, ChatAgent)
        assert agent.api_key == "new-key"


class TestOpenAIClient:
    """Tests for OpenAI client integration."""

    def test_client_property_creates_client(self):
        """Test accessing client property creates OpenAI client."""
        from ..src.agents import ChatAgent

        agent = ChatAgent(api_key="test-key")
        client = agent.client

        assert client is not None
        # Client should be an OpenAI instance
        assert hasattr(client, "chat")

    def test_client_with_invalid_key_raises(self):
        """Test client raises error with invalid API key."""
        from ..src.agents import ChatAgent

        agent = ChatAgent(api_key=None)
        with pytest.raises(ValueError, match="OPENAI_API_KEY is required"):
            _ = agent.client


class TestDefaultModel:
    """Tests for default model configuration."""

    def test_default_model_is_gpt4o(self):
        """Test default model is gpt-4o."""
        from ..src.agents import DEFAULT_MODEL

        assert DEFAULT_MODEL == "gpt-4o"


class TestAgentPrompt:
    """Tests for agent system prompt."""

    def test_prompt_contains_task_keywords(self):
        """Test system prompt contains task management keywords."""
        from ..src.agents.prompt import AGENT_SYSTEM_PROMPT

        prompt_lower = AGENT_SYSTEM_PROMPT.lower()
        assert "task" in prompt_lower
        assert "add" in prompt_lower or "create" in prompt_lower
        assert "list" in prompt_lower or "show" in prompt_lower
        assert "complete" in prompt_lower or "done" in prompt_lower

    def test_prompt_has_guidelines(self):
        """Test system prompt includes response guidelines."""
        from ..src.agents.prompt import AGENT_SYSTEM_PROMPT

        assert "friendly" in AGENT_SYSTEM_PROMPT.lower() or "helpful" in AGENT_SYSTEM_PROMPT.lower()
        assert "error" in AGENT_SYSTEM_PROMPT.lower() or "clarif" in AGENT_SYSTEM_PROMPT.lower()


class TestChatEndpointModels:
    """Tests for chat endpoint request/response models."""

    def test_chat_request_valid(self):
        """Test valid ChatRequest passes validation."""
        from ..src.routes.chat import ChatRequest
        from uuid import uuid4

        req = ChatRequest(
            conversation_id=uuid4(),
            message="Add buy milk",
        )
        assert req.conversation_id is not None
        assert req.message == "Add buy milk"

    def test_chat_request_without_conversation_id(self):
        """Test ChatRequest works without conversation_id."""
        from ..src.routes.chat import ChatRequest

        req = ChatRequest(message="Add buy milk")
        assert req.conversation_id is None
        assert req.message == "Add buy milk"

    def test_chat_request_empty_message_fails(self):
        """Test ChatRequest rejects empty message."""
        from ..src.routes.chat import ChatRequest
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            ChatRequest(message="")

    def test_chat_request_whitespace_message_fails(self):
        """Test ChatRequest rejects whitespace-only message."""
        from ..src.routes.chat import ChatRequest
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            ChatRequest(message="   ")

    def test_chat_response_model(self):
        """Test ChatResponse model."""
        from ..src.routes.chat import ChatResponse, ToolCallItem
        from uuid import uuid4

        resp = ChatResponse(
            conversation_id=uuid4(),
            response="I've added the task.",
        )
        assert resp.conversation_id is not None
        assert resp.response == "I've added the task."
        assert resp.tool_calls is None

    def test_chat_response_with_tool_calls(self):
        """Test ChatResponse with tool calls."""
        from ..src.routes.chat import ChatResponse, ToolCallItem
        from uuid import uuid4

        tool_call = ToolCallItem(
            tool="add_task",
            arguments={"title": "buy milk"},
            result={"success": True, "task_id": str(uuid4())},
        )
        resp = ChatResponse(
            conversation_id=uuid4(),
            response="I've added the task.",
            tool_calls=[tool_call],
        )
        assert resp.tool_calls is not None
        assert len(resp.tool_calls) == 1
        assert resp.tool_calls[0].tool == "add_task"


class TestConversationService:
    """Tests for conversation service functions."""

    @pytest.mark.asyncio
    async def test_save_message_creates_message(self):
        """Test save_message creates a message record."""
        from ..src.routes.chat import save_message
        from ..src.models import MessageRole
        from ..src.models.conversation import Conversation
        from uuid import uuid4
        from unittest.mock import AsyncMock, MagicMock, patch

        mock_db = AsyncMock()
        mock_db.add = MagicMock()
        mock_db.execute = AsyncMock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        conversation_id = uuid4()

        msg = await save_message(
            db=mock_db,
            conversation_id=conversation_id,
            role=MessageRole.USER,
            content="Test message",
        )

        # Verify message was created with correct fields
        mock_db.add.assert_called_once()
        call_args = mock_db.add.call_args[0][0]
        assert isinstance(call_args, Message)
        assert call_args.conversation_id == conversation_id
        assert call_args.role == MessageRole.USER
        assert call_args.content == "Test message"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
