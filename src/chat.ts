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
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  const msg = message.toLowerCase();
  
  if (msg.includes('add')) {
    const task = message.replace(/add/i, '').trim();
    
    const tasks = JSON.parse(localStorage.getItem('chatbot-tasks') || '[]');
    tasks.push(task);
    localStorage.setItem('chatbot-tasks', JSON.stringify(tasks));
    
    const savedTasks = JSON.parse(localStorage.getItem('dashboard-tasks') || '[]');
    const newTask = {
      id: Date.now(),
      title: task,
      description: 'Added via AI Assistant',
      completed: false,
      priority: 'medium',
      category: 'personal',
      dueDate: '',
      recurring: 'none'
    };
    savedTasks.push(newTask);
    localStorage.setItem('dashboard-tasks', JSON.stringify(savedTasks));
    
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('chatbot-task', {
        detail: { action: 'add', task }
      }));
    }
    
    return {
      conversation_id: conversationId || crypto.randomUUID(),
      response: `✅ I've added '${task}' to your task list!`,
      tool_calls: [{
        tool: 'add_task',
        arguments: { title: task },
        result: { success: true, title: task }
      }]
    };
  }
  
  if (msg.includes('show') || msg.includes('list') || msg.includes('tasks')) {
    const tasks = JSON.parse(localStorage.getItem('chatbot-tasks') || '[]');
    
    if (tasks.length === 0) {
      return {
        conversation_id: conversationId || crypto.randomUUID(),
        response: "📝 You don't have any tasks yet. Try adding one!",
      };
    }
    
    const taskList = tasks.map((task: string, i: number) => `${i + 1}. ⏳ ${task}`).join('\\n');
    
    return {
      conversation_id: conversationId || crypto.randomUUID(),
      response: `📋 **Your Tasks:**\\n${taskList}`,
    };
  }
  
  if (msg.includes('delete') || msg.includes('remove')) {
    const taskToDelete = message.replace(/delete|remove/i, '').trim();
    
    const tasks = JSON.parse(localStorage.getItem('chatbot-tasks') || '[]');
    const updatedTasks = tasks.filter((task: string) => !task.toLowerCase().includes(taskToDelete.toLowerCase()));
    localStorage.setItem('chatbot-tasks', JSON.stringify(updatedTasks));
    
    const dashboardTasks = JSON.parse(localStorage.getItem('dashboard-tasks') || '[]');
    const updatedDashboardTasks = dashboardTasks.filter((task: any) => !task.title.toLowerCase().includes(taskToDelete.toLowerCase()));
    localStorage.setItem('dashboard-tasks', JSON.stringify(updatedDashboardTasks));
    
    return {
      conversation_id: conversationId || crypto.randomUUID(),
      response: `🗑️ I've deleted tasks containing '${taskToDelete}'!`,
    };
  }
  
  if (msg.includes('hi') || msg.includes('hello') || msg.includes('hey')) {
    return {
      conversation_id: conversationId || crypto.randomUUID(),
      response: "Hello! 👋 I'm your AI task assistant.\\n\\nTry:\\n• 'Add [task name]'\\n• 'Show my tasks'\\n• 'Mark complete'",
    };
  }
  
  return {
    conversation_id: conversationId || crypto.randomUUID(),
    response: "I can help with tasks! Try 'Add [task]' or 'Show tasks'.",
  };
}