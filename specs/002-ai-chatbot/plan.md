# Implementation Plan: AI-Powered Conversational Task Manager

**Branch**: `002-ai-chatbot` | **Date**: 2025-12-31 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-ai-chatbot/spec.md`

## Summary

Extend the Evolution of Todo web application with a conversational AI interface enabling natural language task management. The system uses OpenAI Agents SDK for AI command interpretation, Official MCP SDK for tool definitions, and OpenAI ChatKit for the frontend chat UI. Conversation history and messages persist in Neon PostgreSQL with full user isolation. The chat endpoint is stateless, maintaining conversation context through database lookups rather than server-side memory.

## Technical Context

**Language/Version**: TypeScript 5.x (frontend), Python 3.11+ (backend)
**Primary Dependencies**: Next.js 16+ (App Router), FastAPI, SQLModel, OpenAI Agents SDK, Official MCP SDK, OpenAI ChatKit
**Storage**: Neon Serverless PostgreSQL via SQLModel (existing) + conversations/messages tables (new)
**Testing**: pytest (Python), Jest/Vitest (TypeScript)
**Target Platform**: Web browsers (mobile + desktop responsive)
**Project Type**: Monorepo extending Phase II frontend/backend
**Performance Goals**: AI responses under 5 seconds p95, stateless endpoint with DB-backed context
**Constraints**: Must use OpenAI Agents SDK + Official MCP SDK per constitution; stateless design; user isolation mandatory
**Scale/Scope**: Single-tenant web app, extends Phase II user base, conversational interface per user

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status | Evidence |
|-----------|-------------|--------|----------|
| I. SDD Lifecycle | Follow Constitution → Specs → Plan → Tasks → Implement | PASS | This plan follows approved spec at specs/002-ai-chatbot/spec.md |
| II. Agent Rules | No feature invention, refinement only at spec level | PASS | Implementation matches spec exactly; no additions |
| III. Phase II Rules | Multi-user, data isolation, JWT auth | PASS | User isolation via user_id FK on conversations/messages; Phase II auth reused |
| IV. Tech Stack | Next.js 16+, FastAPI, SQLModel, Better Auth, Neon PostgreSQL | PASS | All base technologies match constitution |
| V. Quality Principles | Clean architecture, secure JWT, responsive UI | PASS | JWT validation on every request; stateless endpoint design |
| VI. Phase III Rules | ChatKit frontend, Agents SDK backend, MCP tools, Neon DB persistence | PASS | Plan specifies ChatKit, Agents SDK, MCP SDK, database-backed persistence |

## Project Structure

### Documentation (this feature)

```text
specs/002-ai-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (technology research)
├── data-model.md        # Phase 1 output (database schema)
├── quickstart.md        # Phase 1 output (development guide)
├── contracts/           # Phase 1 output (API specifications)
│   └── openapi.yaml     # OpenAPI 3.0 specification
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
.
├── frontend/                    # Next.js 16+ App Router project (Phase II)
│   ├── src/
│   │   ├── app/
│   │   │   ├── chat/
│   │   │   │   └── page.tsx     # NEW: Chat interface page (protected)
│   │   │   └── ...
│   │   ├── components/
│   │   │   └── ChatInterface.tsx # NEW: ChatKit integration component
│   │   └── lib/
│   │       └── chat.ts          # NEW: Chat API client
│   └── package.json
│
├── backend/                     # FastAPI Python project (Phase II)
│   ├── src/
│   │   ├── models/
│   │   │   ├── conversation.py  # NEW: Conversation SQLModel
│   │   │   └── message.py       # NEW: Message SQLModel
│   │   ├── mcp/
│   │   │   ├── __init__.py      # MCP tools module
│   │   │   ├── tools.py         # NEW: 5 CRUD tools (add_task, list_tasks, etc.)
│   │   │   └── server.py        # NEW: MCP server using Official SDK
│   │   ├── agents/
│   │   │   └── __init__.py      # NEW: Agent configuration with tools
│   │   ├── routes/
│   │   │   └── chat.py          # NEW: /api/chat endpoint
│   │   └── main.py
│   ├── requirements.txt
│   └── .env.example
│
├── .env.example                 # Shared environment template (update)
└── README.md
```

**Structure Decision**: Extend existing Phase II monorepo structure. Backend adds `mcp/` and `agents/` modules plus `chat.py` route. Frontend adds `chat/` page and ChatKit component. All new code follows Phase II patterns.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | All design choices align with constitution requirements | N/A |

---

## Phase 0: Research

### Technology Decisions

**Decision**: Use OpenAI Agents SDK for AI command interpretation
- **Rationale**: Constitution mandates OpenAI Agents SDK for AI logic; provides structured agent behavior with tool calling
- **Alternatives considered**: Custom LLM integration (rejected - violates constitution, more complex)

**Decision**: Use Official MCP SDK for tool definitions
- **Rationale**: Constitution mandates Official MCP SDK for tool server; standardizes tool interface between agent and backend
- **Alternatives considered**: Custom tool abstraction (rejected - violates constitution, less maintainable)

**Decision**: Use OpenAI ChatKit for frontend conversational UI
- **Rationale**: Constitution mandates ChatKit for conversational UI; provides polished chat components out of box
- **Alternatives considered**: Custom chat UI (rejected - violates constitution, time-consuming)

**Decision**: Stateless chat endpoint with DB-backed conversation persistence
- **Rationale**: Constitution requires stateless design; Neon DB provides reliable persistence for conversations/messages
- **Alternatives considered**: In-memory session storage (rejected - violates stateless requirement, loses context on restart)

**Decision**: Reuse Phase II JWT authentication for user identification
- **Rationale**: Consistent with Phase II; token contains user_id needed for isolation
- **Alternatives considered**: Separate chat auth (rejected - inconsistent, adds complexity)

### Integration Patterns

**Chat Request Flow**:
1. Frontend sends POST /api/chat with { conversation_id?, message } + JWT
2. Backend validates JWT, extracts user_id
3. If conversation_id provided, fetch conversation + messages from DB
4. If not provided, create new conversation
5. Append user message to history
6. Run OpenAI Agents SDK with MCP tools and conversation history
7. Agent interprets intent, may call MCP tools for CRUD operations
8. Store assistant response as message with tool_calls metadata
9. Return { conversation_id, response, tool_calls }

**MCP Tool Integration**:
1. MCP server initialized with 5 task CRUD tools
2. Each tool wraps existing Phase II task operations
3. Tools enforce user_id filtering for isolation
4. Tool responses returned to agent for natural language synthesis

**User Isolation**:
- All conversation queries include WHERE user_id = :current_user_id
- All message queries filter by conversation + user ownership
- Attempting to access another user's conversation returns 404
- Task operations via MCP tools use existing Phase II user isolation

---

## Phase 1: Design & Contracts

### Data Model

See `data-model.md` for detailed entity definitions.

### API Contracts

See `/contracts/openapi.yaml` for OpenAPI 3.0 specification.

### Quickstart Guide

See `quickstart.md` for development setup instructions.

---

## Implementation Approach

### Backend (FastAPI)

1. **Database Models** (`models/conversation.py`, `models/message.py`)
   - Conversation SQLModel with user_id FK, timestamps
   - Message SQLModel with conversation_id FK, role enum, content, tool_calls JSON
   - Add relationships for conversation → messages

2. **MCP Tools Module** (`mcp/tools.py`)
   - `add_task(title: str, due_date?: datetime) -> dict` - Creates task, returns confirmation
   - `list_tasks(status?: str) -> list[dict]` - Returns user's tasks filtered by status
   - `update_task(task_id: str, title?: str, due_date?: datetime) -> dict` - Modifies task
   - `delete_task(task_id: str) -> dict` - Removes task, returns confirmation
   - `complete_task(task_id: str) -> dict` - Marks task complete, returns updated task

3. **MCP Server** (`mcp/server.py`)
   - Initialize Official MCP SDK server
   - Register 5 task CRUD tools
   - Export tools for OpenAI Agents SDK integration

4. **Agent Configuration** (`agents/__init__.py`)
   - Initialize OpenAI Agents SDK agent
   - Attach MCP tools to agent
   - Configure system prompt for task management behavior

5. **Chat Route** (`routes/chat.py`)
   - POST /api/chat endpoint
   - JWT authentication via Phase II dependency
   - Conversation fetch/create logic
   - Message persistence
   - Agent invocation with history

6. **Application Integration** (`main.py`)
   - Include chat routes
   - Startup MCP server
   - CORS for frontend origin

### Frontend (Next.js)

1. **Chat Page** (`app/chat/page.tsx`)
   - Protected route (redirect if not authenticated)
   - ChatInterface component
   - Conversation history display
   - Message input with enter-to-send

2. **Chat Component** (`components/ChatInterface.tsx`)
   - Initialize OpenAI ChatKit
   - Configure for /api/chat endpoint
   - Handle send message, display responses
   - Manage conversation_id state

3. **Chat API Client** (`lib/chat.ts`)
   - Type-safe fetch to /api/chat
   - Attach JWT from auth context
   - Handle conversation_id persistence
   - Error handling with user-friendly messages

---

## Environment Variables

### Backend (add to requirements.txt)
```
openai>=1.0.0
mcp>=0.9.0  # Official MCP SDK
```

### Frontend (add to package.json)
```
openai-chatkit  # ChatKit package name (verify exact package)
```

### .env.example additions
```
# Phase III - AI Chat
OPENAI_API_KEY=sk-...
```

---

## Next Steps

After this plan is approved:
1. Run `/sp.tasks` to generate implementation tasks organized by user story
2. Execute tasks following the Red-Green-Refactor cycle
3. Verify each user story works independently before moving to next
4. Test conversation persistence across page refreshes
5. Validate user isolation through security testing
