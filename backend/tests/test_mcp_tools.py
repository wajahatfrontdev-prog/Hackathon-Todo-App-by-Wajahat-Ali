"""
Unit tests for Phase III MCP Tools.

Tests for task CRUD operations via MCP tools with user isolation.
"""

import pytest
from datetime import datetime
from uuid import uuid4, UUID
from unittest.mock import AsyncMock, MagicMock, patch


class TestAddTask:
    """Tests for add_task MCP tool."""

    @pytest.mark.asyncio
    async def test_add_task_success(self):
        """Test successful task creation."""
        from ..src.mcp.tools import add_task

        # Create mock database session
        mock_db = AsyncMock()
        mock_db.add = MagicMock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        user_id = uuid4()
        title = "Buy milk"

        result = await add_task(
            db=mock_db,
            user_id=user_id,
            title=title,
        )

        assert result["success"] is True
        assert "task_id" in result
        assert "task" in result
        assert result["task"]["title"] == title
        assert result["task"]["user_id"] == str(user_id)
        assert result["task"]["completed"] is False

    @pytest.mark.asyncio
    async def test_add_task_with_due_date(self):
        """Test task creation with due date."""
        from ..src.mcp.tools import add_task

        mock_db = AsyncMock()
        mock_db.add = MagicMock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        user_id = uuid4()
        title = "Finish report"
        due_date = "2025-01-15"

        result = await add_task(
            db=mock_db,
            user_id=user_id,
            title=title,
            due_date=due_date,
        )

        assert result["success"] is True
        assert result["task"]["due_date"] is not None
        assert "2025-01-15" in result["task"]["due_date"]

    @pytest.mark.asyncio
    async def test_add_task_empty_title_raises(self):
        """Test that empty title raises ValueError."""
        from ..src.mcp.tools import add_task

        mock_db = AsyncMock()
        user_id = uuid4()

        with pytest.raises(ValueError, match="Task title is required"):
            await add_task(
                db=mock_db,
                user_id=user_id,
                title="",
            )

    @pytest.mark.asyncio
    async def test_add_task_whitespace_title_raises(self):
        """Test that whitespace-only title raises ValueError."""
        from ..src.mcp.tools import add_task

        mock_db = AsyncMock()
        user_id = uuid4()

        with pytest.raises(ValueError, match="Task title is required"):
            await add_task(
                db=mock_db,
                user_id=user_id,
                title="   ",
            )


class TestListTasks:
    """Tests for list_tasks MCP tool."""

    @pytest.mark.asyncio
    async def test_list_tasks_empty(self):
        """Test listing tasks when user has none."""
        from ..src.mcp.tools import list_tasks

        mock_db = AsyncMock()
        mock_db.execute = AsyncMock()
        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute.return_value = mock_result

        user_id = uuid4()
        result = await list_tasks(db=mock_db, user_id=user_id)

        assert isinstance(result, list)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_list_tasks_with_results(self):
        """Test listing tasks returns serialized tasks."""
        from ..src.mcp.tools import list_tasks
        from ..src.models import Task

        mock_db = AsyncMock()
        mock_db.execute = AsyncMock()

        user_id = uuid4()
        task1 = Task(
            id=uuid4(),
            user_id=user_id,
            title="Task 1",
            completed=False,
        )
        task2 = Task(
            id=uuid4(),
            user_id=user_id,
            title="Task 2",
            completed=True,
        )

        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = [task1, task2]
        mock_db.execute.return_value = mock_result

        result = await list_tasks(db=mock_db, user_id=user_id)

        assert len(result) == 2
        assert result[0]["title"] == "Task 1"
        assert result[1]["title"] == "Task 2"

    @pytest.mark.asyncio
    async def test_list_tasks_filters_by_status(self):
        """Test list_tasks respects status filter."""
        from ..src.mcp.tools import list_tasks

        mock_db = AsyncMock()
        mock_db.execute = AsyncMock()

        user_id = uuid4()

        # Call with "pending" filter
        result = await list_tasks(
            db=mock_db,
            user_id=user_id,
            status="pending"
        )

        # Verify execute was called with filtered query
        mock_db.execute.assert_called_once()
        call_args = mock_db.execute.call_args[0][0]
        # Query should include pending filter
        assert "where" in str(call_args).lower() or "filter" in str(call_args).lower()


class TestCompleteTask:
    """Tests for complete_task MCP tool."""

    @pytest.mark.asyncio
    async def test_complete_task_success(self):
        """Test successful task completion."""
        from ..src.mcp.tools import complete_task
        from ..src.models import Task

        mock_db = AsyncMock()
        mock_db.execute = AsyncMock()

        user_id = uuid4()
        task_id = uuid4()
        task = Task(
            id=task_id,
            user_id=user_id,
            title="Test task",
            completed=False,
        )

        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = task
        mock_db.execute.return_value = mock_result

        result = await complete_task(
            db=mock_db,
            user_id=user_id,
            task_id=str(task_id),
        )

        assert result["success"] is True
        assert result["task"]["completed"] is True

    @pytest.mark.asyncio
    async def test_complete_task_not_found(self):
        """Test completing non-existent task raises error."""
        from ..src.mcp.tools import complete_task

        mock_db = AsyncMock()
        mock_db.execute = AsyncMock()

        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result

        user_id = uuid4()
        task_id = str(uuid4())

        with pytest.raises(ValueError, match="Task not found"):
            await complete_task(
                db=mock_db,
                user_id=user_id,
                task_id=task_id,
            )

    @pytest.mark.asyncio
    async def test_complete_task_invalid_id(self):
        """Test completing with invalid ID raises error."""
        from ..src.mcp.tools import complete_task

        mock_db = AsyncMock()
        user_id = uuid4()

        with pytest.raises(ValueError, match="Invalid task_id format"):
            await complete_task(
                db=mock_db,
                user_id=user_id,
                task_id="not-a-uuid",
            )


class TestUpdateTask:
    """Tests for update_task MCP tool."""

    @pytest.mark.asyncio
    async def test_update_task_title(self):
        """Test updating task title."""
        from ..src.mcp.tools import update_task
        from ..src.models import Task

        mock_db = AsyncMock()
        mock_db.execute = AsyncMock()

        user_id = uuid4()
        task_id = uuid4()
        task = Task(
            id=task_id,
            user_id=user_id,
            title="Old title",
            completed=False,
        )

        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = task
        mock_db.execute.return_value = mock_result

        result = await update_task(
            db=mock_db,
            user_id=user_id,
            task_id=str(task_id),
            title="New title",
        )

        assert result["success"] is True
        assert result["task"]["title"] == "New title"

    @pytest.mark.asyncio
    async def test_update_task_due_date(self):
        """Test updating task due date."""
        from ..src.mcp.tools import update_task
        from ..src.models import Task

        mock_db = AsyncMock()
        mock_db.execute = AsyncMock()

        user_id = uuid4()
        task_id = uuid4()
        task = Task(
            id=task_id,
            user_id=user_id,
            title="Task",
            completed=False,
        )

        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = task
        mock_db.execute.return_value = mock_result

        result = await update_task(
            db=mock_db,
            user_id=user_id,
            task_id=str(task_id),
            due_date="2025-02-01",
        )

        assert result["success"] is True
        assert result["task"]["due_date"] is not None


class TestDeleteTask:
    """Tests for delete_task MCP tool."""

    @pytest.mark.asyncio
    async def test_delete_task_success(self):
        """Test successful task deletion."""
        from ..src.mcp.tools import delete_task
        from ..src.models import Task

        mock_db = AsyncMock()
        mock_db.execute = AsyncMock()
        mock_db.delete = AsyncMock()
        mock_db.commit = AsyncMock()

        user_id = uuid4()
        task_id = uuid4()
        task = Task(
            id=task_id,
            user_id=user_id,
            title="Task to delete",
            completed=False,
        )

        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = task
        mock_db.execute.return_value = mock_result

        result = await delete_task(
            db=mock_db,
            user_id=user_id,
            task_id=str(task_id),
        )

        assert result["success"] is True
        assert result["task_id"] == str(task_id)
        mock_db.delete.assert_called_once_with(task)

    @pytest.mark.asyncio
    async def test_delete_task_not_found(self):
        """Test deleting non-existent task raises error."""
        from ..src.mcp.tools import delete_task

        mock_db = AsyncMock()
        mock_db.execute = AsyncMock()

        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result

        user_id = uuid4()
        task_id = str(uuid4())

        with pytest.raises(ValueError, match="Task not found"):
            await delete_task(
                db=mock_db,
                user_id=user_id,
                task_id=task_id,
            )


class TestUserIsolation:
    """Tests for user isolation enforcement."""

    @pytest.mark.asyncio
    async def test_list_tasks_enforces_user_filter(self):
        """Test list_tasks only returns user's own tasks."""
        from ..src.mcp.tools import list_tasks

        mock_db = AsyncMock()
        mock_db.execute = AsyncMock()

        user_id = uuid4()
        other_user_id = uuid4()

        # Execute query
        await list_tasks(db=mock_db, user_id=user_id)

        # Verify query includes user_id filter
        mock_db.execute.assert_called_once()
        call_args = mock_db.execute.call_args[0][0]
        query_str = str(call_args)
        assert str(user_id) in query_str

    @pytest.mark.asyncio
    async def test_complete_task_user_isolation(self):
        """Test complete_task cannot complete another user's task."""
        from ..src.mcp.tools import complete_task

        mock_db = AsyncMock()
        mock_db.execute = AsyncMock()

        # Return None (task belongs to different user)
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result

        user_id = uuid4()
        task_id = str(uuid4())

        with pytest.raises(ValueError, match="Task not found"):
            await complete_task(
                db=mock_db,
                user_id=user_id,
                task_id=task_id,
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
