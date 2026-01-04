interface User {
  id: string;
  email: string;
}

interface Session {
  user: User;
  token: string;
}

export async function signIn(email: string, password: string): Promise<Session> {
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  if (password.length < 8) {
    throw new Error('Password must be at least 8 characters');
  }
  
  const session = {
    user: { id: '1', email },
    token: 'mock-jwt-token'
  };
  
  localStorage.setItem('session', JSON.stringify(session));
  return session;
}

export async function signUp(email: string, password: string): Promise<Session> {
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  if (password.length < 8) {
    throw new Error('Password must be at least 8 characters');
  }
  
  const session = {
    user: { id: '1', email },
    token: 'mock-jwt-token'
  };
  
  localStorage.setItem('session', JSON.stringify(session));
  return session;
}

export async function getSession(): Promise<Session | null> {
  try {
    const stored = localStorage.getItem('session');
    return stored ? JSON.parse(stored) : null;
  } catch {
    return null;
  }
}

export async function signOut(): Promise<void> {
  localStorage.removeItem('session');
  window.location.href = '/';
}