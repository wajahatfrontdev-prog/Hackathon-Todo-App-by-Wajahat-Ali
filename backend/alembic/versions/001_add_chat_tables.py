"""
Add chat tables migration.

Revision ID: 001
Revises:
Create Date: 2025-12-31

This migration adds conversations and messages tables for Phase III AI Chatbot.
"""

from typing import UUID
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Create conversations and messages tables."""
    # Create conversations table
    op.create_table(
        "conversation",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_conversation_user_id", "conversation", ["user_id"])

    # Create message_role enum type
    op.execute("CREATE TYPE message_role AS ENUM ('user', 'assistant')")

    # Create messages table
    op.create_table(
        "message",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("conversation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role", postgresql.ENUM("user", "assistant", name="message_role"), nullable=False),
        sa.Column("content", sa.TEXT(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=False),
        sa.Column("tool_calls", postgresql.JSON(), nullable=True),
        sa.ForeignKeyConstraint(["conversation_id"], ["conversation.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_message_conversation_id", "message", ["conversation_id"])


def downgrade():
    """Drop conversations and messages tables."""
    op.drop_index("ix_message_conversation_id", table_name="message")
    op.drop_table("message")
    op.execute("DROP TYPE message_role")
    op.drop_index("ix_conversation_user_id", table_name="conversation")
    op.drop_table("conversation")
