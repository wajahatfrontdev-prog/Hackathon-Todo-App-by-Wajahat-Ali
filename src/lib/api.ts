// api.ts - Updated for HACKATHON DEMO (No Auth Required)

export interface TaskResponse {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
}

// 🔥 FIXED: Correct backend URL (latest working one with tasks)
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'https://hackathon-todo-app-by-wajahat-ali-l.vercel.app';

function getApiBase(): string {
  return API_BASE.replace(/\/$/, '');
}

// 🔥 NO AUTH HEADER — Backend me auth bypass hai demo ke liye
export async function getTasks(): Promise<TaskResponse[]> {
  const response = await fetch(`${getApiBase()}/api/tasks`);
  
  if (!response.ok) {
    console.error('Fetch tasks failed:', response.status, await response.text());
    return []; // Empty array on error — dashboard empty nahi dikhaayega error
  }
  
  const data = await response.json();
  return data.tasks || [];
}

export async function createTask(task: TaskCreate): Promise<TaskResponse> {
  const response = await fetch(`${getApiBase()}/api/tasks`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // NO Authorization header — auth bypassed
    },
    body: JSON.stringify(task),
  });

  if (!response.ok) {
    console.error('Create task failed:', response.status, await response.text());
    throw new Error('Failed to create task');
  }
  
  return response.json();
}

export async function updateTask(id: string, task: TaskUpdate): Promise<TaskResponse> {
  const response = await fetch(`${getApiBase()}/api/tasks/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(task),
  });

  if (!response.ok) throw new Error('Failed to update task');
  return response.json();
}

export async function deleteTask(id: string): Promise<void> {
  const response = await fetch(`${getApiBase()}/api/tasks/${id}`, {
    method: 'DELETE',
  });

  if (!response.ok) throw new Error('Failed to delete task');
}

export async function toggleTaskComplete(id: string): Promise<TaskResponse> {
  const response = await fetch(`${getApiBase()}/api/tasks/${id}/complete`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ completed: true }), // Toggle logic backend me hai
  });

  if (!response.ok) throw new Error('Failed to toggle task');
  return response.json();
}
