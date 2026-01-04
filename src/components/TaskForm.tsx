/**
 * TaskForm component for creating new tasks.
 *
 * Features:
 * - Title input (required with validation)
 * - Description textarea (optional)
 * - API integration with createTask
 * - Error display and loading states
 */

'use client';

import { useState } from 'react';
import { createTask, TaskResponse } from '@/lib/api';

interface TaskFormProps {
  /**
   * Callback when a new task is created.
   * Used to refresh the task list.
   */
  onTaskCreated: (task: TaskResponse) => void;
}

export function TaskForm({ onTaskCreated }: TaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    // Validate title
    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    try {
      setLoading(true);
      const task = await createTask({
        title: title.trim(),
        description: description.trim() || undefined,
      });
      onTaskCreated(task);
      // Reset form
      setTitle('');
      setDescription('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create task');
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Title input */}
      <div>
        <label htmlFor="task-title" className="form-label">
          Title
        </label>
        <input
          id="task-title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="What needs to be done?"
          className="form-input"
          disabled={loading}
          aria-required="true"
        />
      </div>

      {/* Description input */}
      <div>
        <label htmlFor="task-description" className="form-label">
          Description <span className="text-gray-400">(optional)</span>
        </label>
        <textarea
          id="task-description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Add more details..."
          className="form-input min-h-[80px] resize-y"
          disabled={loading}
          rows={3}
        />
      </div>

      {/* Error message */}
      {error && (
        <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      {/* Submit button */}
      <button
        type="submit"
        className="btn btn-primary w-full"
        disabled={loading || !title.trim()}
      >
        {loading ? 'Creating...' : 'Add Task'}
      </button>
    </form>
  );
}
