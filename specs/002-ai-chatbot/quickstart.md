# Quickstart: Phase III AI Chatbot Development

**Date**: 2025-12-31 | **Feature**: 002-ai-chatbot

## Prerequisites

1. **Phase II Development Environment**
   - Frontend: `npm run dev` (Next.js on port 3000)
   - Backend: `uvicorn main:app --reload` (FastAPI on port 8000)
   - Database: Neon PostgreSQL connection configured

2. **OpenAI API Key**
   - Get API key from https://platform.openai.com/api-keys
   - Requires GPT-4o or compatible model access

## Environment Setup

### Backend

1. **Install new dependencies**

```bash
cd backend

# Install OpenAI package (includes Agents SDK)
pip install openai>=1.0.0

# Install Official MCP SDK
pip install mcp>=0.9.0

# Update requirements.txt
echo "openai>=1.0.0" >> requirements.txt
echo "mcp>=0.9.0" >> requirements.txt
```

2. **Add environment variables**

Update `backend/.env.example`:

```bash
# Phase III - AI Chat (add these)
OPENAI_API_KEY=sk-...
```

Add to `.env`:
```bash
OPENAI_API_KEY=sk-your-openai-api-key
```

### Frontend

1. **Install Frontend Dependencies**

```bash
cd frontend

# Install OpenAI (for potential client-side usage) and UI libraries
npm install openai framer-motion lucide-react

# The following are already in package.json:
# - next: ^14.2.0
# - react: ^18.2.0
# - tailwindcss: ^3.4.1
```

2. **Add environment variables**

Update `.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CHAT_API_URL=http://localhost:8000/api/chat
```

## Running Development Servers

### Start Backend

```bash
cd backend

# Start FastAPI with auto-reload
uvicorn main:app --reload --port 8000

# Output should show:
# INFO:     Uvicorn running on http://localhost:8000 (Press CTRL+C to quit)
```

### Start Frontend

```bash
cd frontend

# Start Next.js development server
npm run dev

# Output should show:
# Ready on http://localhost:3000
```

## Accessing the Chat Interface

1. Navigate to http://localhost:3000
2. Sign in or register (Phase II auth)
3. Navigate to http://localhost:3000/chat
4. Start typing natural language commands

## Testing Commands

Try these commands to verify the chat works:

```text
User: "Add buy milk"
User: "Show my pending tasks"
User: "Mark buy milk as complete"
User: "What do I need to do?"
```

## Troubleshooting

### OpenAI API Errors

- **401 Unauthorized**: Check OPENAI_API_KEY is valid
- **429 Rate Limited**: Reduce request frequency
- **400 Bad Request**: Verify request format matches OpenAPI spec

### Database Errors

- **Connection failed**: Verify DATABASE_URL in .env
- **Missing tables**: Run Alembic migration:
  ```bash
  cd backend
  alembic upgrade head
  ```

### MCP Tool Errors

- **Tool not found**: Verify MCP server initialized correctly
- **Tool call failed**: Check backend logs for tool execution errors

## Verifying User Isolation

1. Create user A, add some tasks via chat
2. Create user B in incognito window
3. User B should NOT see user A's conversations or tasks
4. User B should be able to access their own empty chat

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   └── chat/
│   │       └── page.tsx          # Chat page (protected)
│   ├── components/
│   │   ├── ChatInterface.tsx     # Chat UI component with animations
│   │   └── Navbar.tsx            # Updated with Chat link
│   └── lib/
│       └── chat.ts               # Chat API client
│
backend/
├── src/
│   ├── models/
│   │   ├── conversation.py       # Conversation SQLModel
│   │   └── message.py            # Message SQLModel
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── tools.py              # 5 CRUD tools
│   │   └── server.py             # MCP server
│   ├── agents/
│   │   ├── prompt.py             # Agent system prompt
│   │   └── __init__.py           # ChatAgent class
│   └── routes/
│       └── chat.py               # /api/chat endpoint
```
