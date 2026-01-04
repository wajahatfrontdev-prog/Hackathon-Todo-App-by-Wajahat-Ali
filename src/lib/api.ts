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

// Helper function to get auth token
function getAuthToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('auth-token');
}

// Helper function to get auth headers
function getAuthHeaders(): Record<string, string> {
  const token = getAuthToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  return headers;
}

// 🔥 CORRECT BACKEND URL (working one with 52 tasks)
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'https://hackathon-todo-app-by-wajahat-ali-l.vercel.app';

function getApiBase(): string {
  return API_BASE.replace(/\/$/, '');
}

export async function getTasks(): Promise<TaskResponse[]> {
  const response = await fetch(`${getApiBase()}/api/tasks`, {
    headers: getAuthHeaders(),
  });
  
  if (!response.ok) {
    console.error('Tasks fetch failed:', response.status, await response.text());
    if (response.status === 401) {
      throw new Error('Please logout and login again to refresh your session.');
    }
    return [];
  }
  
  const data = await response.json();
  console.log('Fetched tasks:', data);
  return data.tasks || [];
}

export async function createTask(task: TaskCreate): Promise<TaskResponse> {
  const response = await fetch(`${getApiBase()}/api/tasks`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(task),
  });

  if (!response.ok) {
    console.error('Create failed:', response.status, await response.text());
    if (response.status === 401) {
      throw new Error('Please logout and login again to refresh your session.');
    }
    throw new Error('Failed to create task');
  }
  
  return response.json();
}

export async function updateTask(id: string, task: TaskUpdate): Promise<TaskResponse> {
  const response = await fetch(`${getApiBase()}/api/tasks/${id}`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(task),
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error('Please logout and login again to refresh your session.');
    }
    throw new Error('Failed to update task');
  }
  return response.json();
}

export async function deleteTask(id: string): Promise<void> {
  const response = await fetch(`${getApiBase()}/api/tasks/${id}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error('Please logout and login again to refresh your session.');
    }
    throw new Error('Failed to delete task');
  }
}

export async function toggleTaskComplete(id: string): Promise<TaskResponse> {
  const response = await fetch(`${getApiBase()}/api/tasks/${id}/complete`, {
    method: 'PATCH',
    headers: getAuthHeaders(),
    body: JSON.stringify({ completed: !true }), // Toggle logic
  });

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error('Please logout and login again to refresh your session.');
    }
    throw new Error('Failed to toggle task');
  }
  return response.json();
}
