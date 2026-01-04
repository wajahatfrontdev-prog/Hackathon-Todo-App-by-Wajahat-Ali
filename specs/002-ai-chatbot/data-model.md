# Data Model: Phase III AI Chatbot

**Date**: 2025-12-31 | **Feature**: 002-ai-chatbot

## Entity Definitions

### Conversation

Represents a chat session belonging to a user.

```python
from datetime import datetime
from typing import List
from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

class Conversation(SQLModel, table=True):
    """Chat conversation entity."""
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")
```

**Fields**:
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| id | UUID | Yes | auto-generated | Primary key, unique identifier |
| user_id | UUID | Yes | - | Foreign key to User (Phase II) |
| created_at | datetime | Yes | utcnow | Timestamp of conversation creation |
| updated_at | datetime | Yes | utcnow | Timestamp of last message (auto-updated) |

**Constraints**:
- `user_id` references Phase II User.id
- Index on `user_id` for fast user conversation lookup
- Index on `(user_id, updated_at DESC)` for "most recent conversation" query

### Message

Represents a single exchange within a conversation.

```python
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
import json

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class Message(SQLModel, table=True):
    """Chat message entity."""
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversation.id", nullable=False, index=True)
    role: MessageRole = Field(nullable=False)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    tool_calls: Optional[str] = Field(default=None, nullable=True)  # JSON array

    # Relationship to conversation
    conversation: Conversation = Relationship(back_populates="messages")
```

**Fields**:
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| id | UUID | Yes | auto-generated | Primary key, unique identifier |
| conversation_id | UUID | Yes | - | Foreign key to Conversation |
| role | MessageRole | Yes | - | Either "user" or "assistant" |
| content | str | Yes | - | The message text |
| created_at | datetime | Yes | utcnow | Timestamp when message was created |
| tool_calls | JSON | No | null | Array of tool invocations made by assistant |

**Constraints**:
- `conversation_id` references Conversation.id
- Index on `conversation_id` for fast message retrieval
- Index on `created_at` for chronological ordering

**tool_calls Format** (JSON):
```json
[
  {
    "tool": "add_task",
    "arguments": {"title": "buy milk", "due_date": null},
    "result": {"success": true, "task_id": "..."}
  }
]
```

## Relationships

```
User (Phase II)
  │
  └── Conversation (1:N)
        │
        └── Message (1:N)
```

- One User has many Conversations
- One Conversation belongs to one User
- One Conversation has many Messages
- One Message belongs to one Conversation

## Database Migration

Add to existing Phase II schema via Alembic migration:

```python
# alembic/versions/xxx_add_chat_tables.py

def upgrade():
    # Create conversations table
    op.create_table(
        "conversation",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("user.id"), nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(), nullable=False),
        sa.Column("updated_at", postgresql.TIMESTAMP(), nullable=False),
    )
    op.create_index("ix_conversation_user_id", "conversation", ["user_id"])

    # Create messages table
    op.create_table(
        "message",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("conversation_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("conversation.id"), nullable=False),
        sa.Column("role", sa.Enum("user", "assistant", name="message_role"), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(), nullable=False),
        sa.Column("tool_calls", postgresql.JSON(), nullable=True),
    )
    op.create_index("ix_message_conversation_id", "message", ["conversation_id"])

def downgrade():
    op.drop_table("message")
    op.drop_table("conversation")
    op.execute("DROP TYPE message_role")
```

## User Isolation

All queries MUST include user_id filtering:

```python
# Get user's conversation
def get_user_conversation(conversation_id: UUID, user_id: UUID):
    return db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    ).first()

# Get user's messages in conversation
def get_conversation_messages(conversation_id: UUID, user_id: UUID):
    return db.query(Message).join(Conversation).filter(
        Message.conversation_id == conversation_id,
        Conversation.user_id == user_id
    ).order_by(Message.created_at).all()
```

## Phase II Integration

The new tables reference the existing User table from Phase II:

```python
# conversation.user_id references user.id (Phase II User model)
# No changes to existing Phase II tables required
```

## Sample Data

```python
# Create conversation
conversation = Conversation(
    user_id=user_id,
    created_at=datetime.utcnow(),
    updated_at=datetime.utcnow()
)

# Create user message
user_message = Message(
    conversation_id=conversation.id,
    role=MessageRole.USER,
    content="Add buy milk",
    created_at=datetime.utcnow()
)

# Create assistant message with tool call
assistant_message = Message(
    conversation_id=conversation.id,
    role=MessageRole.ASSISTANT,
    content="I've added 'buy milk' to your tasks.",
    created_at=datetime.utcnow(),
    tool_calls=json.dumps([
        {
            "tool": "add_task",
            "arguments": {"title": "buy milk"},
            "result": {"success": True, "task_id": "..."}
        }
    ])
)
```
