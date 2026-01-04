export interface ChatResponse {
  conversation_id: string;
  response: string;
  tool_calls?: Array<{
    tool: string;
    arguments: Record<string, unknown>;
    result?: Record<string, unknown>;
  }>;
}

export async function sendChatMessage(
  message: string,
  conversationId?: string
): Promise<ChatResponse> {
  // Get the actual auth token from localStorage
  const token = localStorage.getItem('auth-token');
  
  if (!token) {
    throw new Error('Please logout and login again to refresh your session.');
  }
  
  const CHAT_API_URL = process.env.NEXT_PUBLIC_CHAT_API_URL || 'https://hackathon-todo-app-by-wajahat-ali-l.vercel.app/api/chat';
  
  const response = await fetch(CHAT_API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({
      message,
      conversation_id: conversationId,
    }),
  });
  
  if (!response.ok) {
    if (response.status === 401) {
      throw new Error('Please logout and login again to refresh your session.');
    }
    throw new Error(`API error: ${response.status}`);
  }
  
  return await response.json();
}
