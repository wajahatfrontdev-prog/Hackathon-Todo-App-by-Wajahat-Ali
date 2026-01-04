/**
 * TaskList component for displaying a list of tasks.
 *
 * Features:
 * - Renders empty state when no tasks exist
 * - Displays all tasks with completion status indicators
 * - Calls getTasks on component mount
 * - Propagates updates and deletions to parent
 */

'use client';

import { useEffect } from 'react';
import { TaskResponse, getTasks } from '@/lib/api';
import { TaskItem } from './TaskItem';

interface TaskListProps {
  tasks: TaskResponse[];
  loading: boolean;
  onTaskUpdate: (task: TaskResponse) => void;
  onTaskDelete: (taskId: string) => void;
  onTasksLoad: (tasks: TaskResponse[]) => void;
}

export function TaskList({
  tasks,
  loading,
  onTaskUpdate,
  onTaskDelete,
  onTasksLoad,
}: TaskListProps) {
  // Load tasks on mount
  useEffect(() => {
    async function load() {
      try {
        const response = await getTasks();
        onTasksLoad(response);
      } catch (error) {
        console.error('Failed to load tasks:', error);
      }
    }
    load();
  }, [onTasksLoad]);

  // Loading state
  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p className="text-gray-600 mt-4">Loading tasks...</p>
      </div>
    );
  }

  // Empty state
  if (tasks.length === 0) {
    return (
      <div className="card text-center py-12">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-16 w-16 mx-auto text-gray-300 mb-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
          />
        </svg>
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          No tasks yet
        </h3>
        <p className="text-gray-500">
          Add your first task above to get started
        </p>
      </div>
    );
  }

  // Task list
  return (
    <ul className="space-y-3">
      {Array.isArray(tasks) && tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onTaskUpdate={onTaskUpdate}
          onTaskDelete={onTaskDelete}
        />
      ))}
    </ul>
  );
}
