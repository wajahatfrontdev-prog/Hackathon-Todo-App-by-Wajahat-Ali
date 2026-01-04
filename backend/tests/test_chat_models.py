"""
Unit tests for Phase III Chat models.

Tests for Conversation and Message SQLModel entities.
"""

import pytest
from datetime import datetime
from uuid import uuid4, UUID

from sqlmodel import SQLModel


class TestConversationModel:
    """Tests for Conversation SQLModel."""

    def test_conversation_fields(self):
        """Test Conversation model has all required fields."""
        from ..src.models.conversation import Conversation

        # Check required attributes exist
        assert hasattr(Conversation, "id")
        assert hasattr(Conversation, "user_id")
        assert hasattr(Conversation, "created_at")
        assert hasattr(Conversation, "updated_at")
        assert hasattr(Conversation, "messages")

    def test_conversation_default_factory(self):
        """Test Conversation uses uuid4 for id."""
        from ..src.models.conversation import Conversation

        conv = Conversation(user_id=uuid4())
        assert conv.id is not None
        assert isinstance(conv.id, UUID)

    def test_conversation_timestamps(self):
        """Test Conversation has timestamp defaults."""
        from ..src.models.conversation import Conversation

        user_id = uuid4()
        conv = Conversation(user_id=user_id)

        assert conv.created_at is not None
        assert isinstance(conv.created_at, datetime)
        assert conv.updated_at is not None
        assert isinstance(conv.updated_at, datetime)

    def test_conversation_user_id_required(self):
        """Test Conversation requires user_id."""
        from ..src.models.conversation import Conversation

        # user_id is a required field (no default)
        assert Conversation.__table__.columns["user_id"].nullable is False


class TestMessageModel:
    """Tests for Message SQLModel."""

    def test_message_fields(self):
        """Test Message model has all required fields."""
        from ..src.models.message import Message, MessageRole

        # Check required attributes exist
        assert hasattr(Message, "id")
        assert hasattr(Message, "conversation_id")
        assert hasattr(Message, "role")
        assert hasattr(Message, "content")
        assert hasattr(Message, "created_at")
        assert hasattr(Message, "tool_calls")
        assert hasattr(Message, "conversation")

    def test_message_role_enum(self):
        """Test MessageRole enum values."""
        from ..src.models.message import MessageRole

        assert MessageRole.USER.value == "user"
        assert MessageRole.ASSISTANT.value == "assistant"

    def test_message_default_factory(self):
        """Test Message uses uuid4 for id."""
        from ..src.models.message import Message

        msg = Message(
            conversation_id=uuid4(),
            role=MessageRole.USER,
            content="Test message"
        )
        assert msg.id is not None
        assert isinstance(msg.id, UUID)

    def test_message_timestamps(self):
        """Test Message has timestamp defaults."""
        from ..src.models.message import Message, MessageRole

        msg = Message(
            conversation_id=uuid4(),
            role=MessageRole.USER,
            content="Test message"
        )
        assert msg.created_at is not None
        assert isinstance(msg.created_at, datetime)

    def test_message_tool_calls_optional(self):
        """Test Message tool_calls is optional."""
        from ..src.models.message import Message, MessageRole

        # Can create message without tool_calls
        msg = Message(
            conversation_id=uuid4(),
            role=MessageRole.USER,
            content="Test message"
        )
        assert msg.tool_calls is None

    def test_message_tool_calls_json(self):
        """Test Message tool_calls can store JSON."""
        from ..src.models.message import Message, MessageRole
        import json

        tool_calls_data = [
            {
                "tool": "add_task",
                "arguments": {"title": "buy milk"},
                "result": {"success": True, "task_id": "123"}
            }
        ]

        msg = Message(
            conversation_id=uuid4(),
            role=MessageRole.ASSISTANT,
            content="I've added 'buy milk' to your tasks.",
            tool_calls=json.dumps(tool_calls_data)
        )
        assert msg.tool_calls is not None

        # Verify it's valid JSON
        parsed = json.loads(msg.tool_calls)
        assert len(parsed) == 1
        assert parsed[0]["tool"] == "add_task"


class TestModelRelationships:
    """Tests for model relationships."""

    def test_conversation_messages_relationship(self):
        """Test Conversation has messages relationship."""
        from ..src.models.conversation import Conversation

        # Check relationship attribute exists
        assert hasattr(Conversation, "messages")

    def test_message_conversation_relationship(self):
        """Test Message has conversation relationship."""
        from ..src.models.message import Message

        # Check relationship attribute exists
        assert hasattr(Message, "conversation")


class TestModelExports:
    """Tests for model package exports."""

    def test_package_exports_conversation(self):
        """Test models package exports Conversation."""
        from ..src.models import Conversation
        assert Conversation is not None

    def test_package_exports_message(self):
        """Test models package exports Message."""
        from ..src.models import Message
        assert Message is not None

    def test_package_exports_message_role(self):
        """Test models package exports MessageRole."""
        from ..src.models import MessageRole
        assert MessageRole is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
