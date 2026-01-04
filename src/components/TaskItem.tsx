/**
 * TaskItem component for displaying and interacting with a single task.
 *
 * Features:
 * - Checkbox for completion toggle
 * - Title with strikethrough when completed
 * - Description display
 * - Edit functionality (inline form)
 * - Delete with confirmation
 * - Optimistic UI updates
 */

'use client';

import { useState } from 'react';
import {
  TaskResponse,
  updateTask,
  deleteTask,
  toggleTaskComplete,
} from '@/lib/api';

interface TaskItemProps {
  task: TaskResponse;
  onTaskUpdate: (task: TaskResponse) => void;
  onTaskDelete: (taskId: string) => void;
  disabled?: boolean;
}

export function TaskItem({
  task,
  onTaskUpdate,
  onTaskDelete,
  disabled = false,
}: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Optimistic toggle
  async function handleToggle() {
    if (disabled || loading) return;

    // Optimistic update
    const optimisticTask = { ...task, completed: !task.completed };
    onTaskUpdate(optimisticTask);

    try {
      const updated = await toggleTaskComplete(task.id);
      onTaskUpdate(updated);
    } catch (err) {
      // Revert on error
      onTaskUpdate(task);
      setError(err instanceof Error ? err.message : 'Failed to update task');
    }
  }

  // Start editing
  function handleEdit() {
    setEditTitle(task.title);
    setEditDescription(task.description || '');
    setIsEditing(true);
    setError(null);
  }

  // Cancel editing
  function handleCancel() {
    setIsEditing(false);
    setEditTitle(task.title);
    setEditDescription(task.description || '');
    setError(null);
  }

  // Save edits
  async function handleSave() {
    if (!editTitle.trim()) {
      setError('Title is required');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const updated = await updateTask(task.id, {
        title: editTitle.trim(),
        description: editDescription.trim() || undefined,
      });
      onTaskUpdate(updated);
      setIsEditing(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task');
    } finally {
      setLoading(false);
    }
  }

  // Delete with confirmation
  async function handleDelete() {
    if (!confirm('Are you sure you want to delete this task?')) return;

    setLoading(true);
    setError(null);

    try {
      await deleteTask(task.id);
      onTaskDelete(task.id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete task');
      setLoading(false);
    }
  }

  // Show inline edit form
  if (isEditing) {
    return (
      <div className="task-item flex-col gap-3">
        <div className="w-full">
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className="form-input w-full"
            placeholder="Task title"
            disabled={loading}
            autoFocus
          />
        </div>
        <div className="w-full">
          <textarea
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            className="form-input w-full min-h-[60px] resize-y"
            placeholder="Description (optional)"
            disabled={loading}
            rows={2}
          />
        </div>
        {error && (
          <p className="text-sm text-red-600">{error}</p>
        )}
        <div className="flex gap-2 justify-end">
          <button
            onClick={handleCancel}
            className="btn btn-secondary text-sm"
            disabled={loading}
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            className="btn btn-primary text-sm"
            disabled={loading || !editTitle.trim()}
          >
            {loading ? 'Saving...' : 'Save'}
          </button>
        </div>
      </div>
    );
  }

  // Show task display
  return (
    <li className={`task-item ${task.completed ? 'completed' : ''}`}>
      {/* Checkbox */}
      <input
        type="checkbox"
        checked={task.completed}
        onChange={handleToggle}
        className="task-checkbox"
        disabled={disabled || loading}
        aria-label={task.completed ? 'Mark as incomplete' : 'Mark as complete'}
      />

      {/* Task content */}
      <div className="flex-1 min-w-0">
        <span className="task-title font-medium text-gray-900 break-words">
          {task.title}
        </span>
        {task.description && (
          <p className="text-sm text-gray-500 mt-1 break-words">
            {task.description}
          </p>
        )}
      </div>

      {/* Action buttons */}
      <div className="flex items-center gap-2">
        {/* Edit button */}
        <button
          onClick={handleEdit}
          className="text-gray-400 hover:text-blue-600 transition-colors p-1"
          disabled={disabled || loading}
          aria-label="Edit task"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-5 w-5"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
          </svg>
        </button>

        {/* Delete button */}
        <button
          onClick={handleDelete}
          className="text-gray-400 hover:text-red-600 transition-colors p-1"
          disabled={disabled || loading}
          aria-label="Delete task"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-5 w-5"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fillRule="evenodd"
              d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
              clipRule="evenodd"
            />
          </svg>
        </button>
      </div>

      {/* Error message */}
      {error && (
        <div className="w-full mt-2 p-2 bg-red-50 border border-red-200 rounded">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}
    </li>
  );
}
