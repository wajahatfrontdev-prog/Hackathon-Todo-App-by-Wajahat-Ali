# Claude Code Skills for Todo Web Application

This directory contains comprehensive Claude Code Skills that enable AI-powered development for the Todo Web Application Hackathon project.

## What Are Skills?

Skills are specialized knowledge modules that provide AI agents with step-by-step guidance, examples, and best practices for specific development tasks. Each skill focuses on a particular technology or workflow, enabling consistent, high-quality implementation across the project.

## Available Skills

| Skill | Description | When to Use |
|-------|-------------|-------------|
| [fastapi-backend-skill](./fastapi-backend-skill.SKILL.md) | Create and manage FastAPI routes, dependencies, and models | Adding new API endpoints, auth, database operations |
| [nextjs-frontend-skill](./nextjs-frontend-skill.SKILL.md) | Build Next.js App Router pages, components with TypeScript and Tailwind | Creating new pages, UI components, responsive design |
| [openai-chatkit-skill](./openai-chatkit-skill.SKILL.md) | Integrate OpenAI ChatKit for conversational AI interface | Building chat UI, handling messages, tool calls display |
| [groq-inference-skill](./groq-inference-skill.SKILL.md) | Use Groq for fast LLM inference with OpenAI-compatible client | AI agent logic, natural language processing |
| [mcp-tools-skill](./mcp-tools-skill.SKILL.md) | Define and implement MCP tools for task CRUD operations | Adding new task management capabilities for AI agent |
| [sqlmodel-database-skill](./sqlmodel-database-skill.SKILL.md) | Define SQLModel models and manage Neon PostgreSQL schema | Adding new database tables or relationships |
| [better-auth-skill](./better-auth-skill.SKILL.md) | Configure Better Auth with JWT for secure authentication | User signup, login, session management |
| [spec-driven-workflow-skill](./spec-driven-workflow-skill.SKILL.md) | Follow spec-driven development (constitution → spec → plan → tasks → implement) | Any new feature development |

## How Skills Enable the AI-Powered Todo App

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Todo Web Application                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐     ┌──────────────────┐              │
│  │   Next.js Front  │◄───►│  FastAPI Backend │              │
│  │      (React)     │     │    (Python)      │              │
│  └────────┬─────────┘     └────────┬─────────┘              │
│           │                        │                        │
│           │    ┌──────────────────┐                        │
│           └───►│   PostgreSQL     │                        │
│                │   (Neon)         │                        │
│                └──────────────────┘                        │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              AI Integration Layer                  │    │
│  ├──────────────┬──────────────┬─────────────────────┤    │
│  │ OpenAI       │ Groq         │ MCP Tools           │    │
│  │ ChatKit      │ Inference    │ (Task Operations)   │    │
│  └──────────────┴──────────────┴─────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              Better Auth (JWT)                     │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Skill |
|-------|------------|-------|
| Frontend | Next.js 14, TypeScript, Tailwind CSS | nextjs-frontend-skill |
| Backend | FastAPI, Python 3.11+ | fastapi-backend-skill |
| Database | Neon PostgreSQL, SQLModel | sqlmodel-database-skill |
| Authentication | Better Auth, JWT | better-auth-skill |
| AI Chat | OpenAI ChatKit | openai-chatkit-skill |
| AI Inference | Groq (Llama 3, Mixtral) | groq-inference-skill |
| Agent Tools | MCP (Model Context Protocol) | mcp-tools-skill |

## How to Use Skills in Development

### 1. Adding a New API Endpoint

When you need to create a new backend endpoint:

1. Reference **fastapi-backend-skill.SKILL.md**
2. Follow the pattern for routes, dependencies, and error handling
3. Use SQLModel for database interactions (sqlmodel-database-skill.SKILL.md)
4. Add authentication where needed (better-auth-skill.SKILL.md)

```python
# Example: Following the skill pattern
from fastapi import APIRouter, Depends, HTTPException
from auth.dependencies import get_current_user
from models.task import TaskCreate, TaskResponse
from service import create_task

router = APIRouter()

@router.post("/tasks", response_model=TaskResponse)
async def create_task_endpoint(
    task: TaskCreate,
    current_user = Depends(get_current_user)
):
    return await create_task(db, task, current_user.id)
```

### 2. Building a New Frontend Page

When creating a new page or component:

1. Reference **nextjs-frontend-skill.SKILL.md**
2. Follow the App Router structure
3. Use TypeScript for type safety
4. Apply Tailwind CSS for styling

```tsx
// Example: Following the skill pattern
'use client'

import { useState } from 'react'
import { useTasks } from '@/hooks/useTasks'
import { Button } from '@/components/ui/Button'

export default function TasksPage() {
  const { tasks, isLoading, addTask } = useTasks()
  // Component implementation
}
```

### 3. Extending AI Capabilities

When adding new AI-powered features:

1. Reference **openai-chatkit-skill.SKILL.md** for chat UI
2. Reference **groq-inference-skill.SKILL.md** for agent logic
3. Reference **mcp-tools-skill.SKILL.md** for tool definitions

```typescript
// Example: Extending chat capabilities
const response = await createGroqCompletion(messages, {
  model: 'llama3-70b-8192',
  temperature: 0.7,
})
```

### 4. Database Changes

When modifying the data model:

1. Reference **sqlmodel-database-skill.SKILL.md**
2. Create SQLModel classes
3. Handle relationships properly
4. Create migrations if needed

```python
# Example: New model following the skill pattern
class Category(SQLModel, TimestampMixin, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(unique=True, nullable=False)
    color: str = Field(default="#3B82F6")
    user_id: int = Field(foreign_key="users.id")
```

### 5. Authentication Features

When implementing auth:

1. Reference **better-auth-skill.SKILL.md**
2. Follow JWT patterns
3. Use dependencies for protected routes

```python
# Example: Protected route
@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user.to_response()
```

## Skill File Format

Each skill follows this structure:

```markdown
---
name: skill-name
description: Brief description of the skill
when-to-use: When to apply this skill
---
# Skill Title

## Instructions
Step-by-step guidance with examples

## Examples
Concrete code examples showing common patterns
```

## Following the Spec-Driven Development Workflow

Use **spec-driven-workflow-skill.SKILL.md** for any new feature:

1. **Constitution** → Review project principles
2. **Spec** → Define feature requirements
3. **Plan** → Design architecture
4. **Tasks** → Break into implementable steps
5. **Implement** → Code with TDD approach (RED → GREEN → REFACTOR)
6. **Polish** → Finalize and document

## Skills and Project Artifacts

| Artifact | Related Skills |
|----------|----------------|
| `specs/<feature>/spec.md` | spec-driven-workflow-skill |
| `specs/<feature>/plan.md` | fastapi-backend-skill, sqlmodel-database-skill, better-auth-skill |
| `specs/<feature>/tasks.md` | spec-driven-workflow-skill |
| `specs/<feature>/data-model.md` | sqlmodel-database-skill |
| `backend/*.py` | fastapi-backend-skill, sqlmodel-database-skill, better-auth-skill, mcp-tools-skill |
| `src/**/*.{ts,tsx}` | nextjs-frontend-skill, openai-chatkit-skill |
| `src/lib/*.ts` (AI) | openai-chatkit-skill, groq-inference-skill |

## Integration Examples

### Complete Feature: Task Labels

To add a labels feature to tasks:

1. **Plan**: Use `spec-driven-workflow-skill` to define requirements
2. **Database**: Use `sqlmodel-database-skill` to create Label model and association table
3. **Backend**: Use `fastapi-backend-skill` to create label CRUD endpoints
4. **Auth**: Use `better-auth-skill` to protect label endpoints
5. **Frontend**: Use `nextjs-frontend-skill` to create label management UI
6. **AI Tools**: Use `mcp-tools-skill` to add label operations for AI agent

### Complete Feature: AI Task Suggestions

To add AI-powered task suggestions:

1. **AI Logic**: Use `groq-inference-skill` to create suggestion agent
2. **Chat UI**: Use `openai-chatkit-skill` to build chat interface
3. **Backend**: Use `fastapi-backend-skill` to create suggestion endpoints
4. **MCP Tools**: Use `mcp-tools-skill` to expose task analysis tools

## Learning Path

For new developers:

1. Start with **[spec-driven-workflow-skill](./spec-driven-workflow-skill.SKILL.md)** to understand the development process
2. Learn **[nextjs-frontend-skill](./nextjs-frontend-skill.SKILL.md)** for frontend development
3. Study **[fastapi-backend-skill](./fastapi-backend-skill.SKILL.md)** for backend development
4. Explore **[sqlmodel-database-skill](./sqlmodel-database-skill.SKILL.md)** for data modeling
5. Understand **[better-auth-skill](./better-auth-skill.SKILL.md)** for authentication
6. Dive into **[openai-chatkit-skill](./openai-chatkit-skill.SKILL.md)** and **[groq-inference-skill](./groq-inference-skill.SKILL.md)** for AI features
7. Master **[mcp-tools-skill](./mcp-tools-skill.SKILL.md)** for extending AI capabilities

## Contributing New Skills

To add a new skill:

1. Create a new `.SKILL.md` file in this directory
2. Follow the standard format with YAML frontmatter
3. Include instructions and concrete examples
4. Update this README with the new skill
5. Add to the skill matrix table

## Resources

- [Project Constitution](../.specify/memory/constitution.md)
- [SDD Workflow Guide](./spec-driven-workflow-skill.SKILL.md)
- [Feature Specifications](../specs/)
- [Command Reference](../.claude/commands/)
