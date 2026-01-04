# Implementation Tasks: AI-Powered Conversational Task Manager

**Branch**: `002-ai-chatbot` | **Date**: 2025-12-31 | **Feature**: Phase III AI Chatbot
**Based On**: `specs/002-ai-chatbot/spec.md` and `plan.md`

## Task Groups Overview

| Group | Tasks | Dependencies |
|-------|-------|--------------|
| 1. Database Extensions | T001-T006 | None |
| 2. MCP Server & Tools | T007-T014 | T001-T006 |
| 3. OpenAI Agents Configuration | T015-T018 | T007-T014 |
| 4. Chat Endpoint | T019-T024 | T015-T018 |
| 5. Frontend Dependencies | T025-T027 | None (parallel with backend) |
| 6. ChatKit Integration | T028-T032 | T025-T027 |
| 7. Chat Page | T033-T036 | T028-T032 |
| 8. Error Handling & Polish | T037-T040 | T024, T036 |

---

## Group 1: Database Extensions

### T001 - Create Conversation SQLModel

**Description**: Create the Conversation SQLModel with user_id FK and timestamps.

**References**:
- Spec: Key Entities > Conversation
- Plan: Backend > Database Models
- Data Model: `data-model.md` > Conversation

**Preconditions**:
- Phase II User model exists
- SQLModel imported from Phase II

**Expected Output**:
- File: `backend/src/models/conversation.py`
- Model: `Conversation` with id, user_id, created_at, updated_at

**Acceptance Criteria**:
- [ ] Conversation SQLModel defined with UUID primary key
- [ ] user_id FK to User table with index
- [ ] created_at and updated_at timestamps with defaults
- [ ] Relationship to Message model defined
- [ ] Type hints and docstrings included

---

### T002 - Create Message SQLModel

**Description**: Create the Message SQLModel with conversation_id FK, role enum, content, and tool_calls.

**References**:
- Spec: Key Entities > Message
- Plan: Backend > Database Models
- Data Model: `data-model.md` > Message

**Preconditions**:
- T001 complete (Conversation model exists)
- MessageRole enum defined

**Expected Output**:
- File: `backend/src/models/message.py`
- Model: `Message` with id, conversation_id, role, content, created_at, tool_calls

**Acceptance Criteria**:
- [ ] Message SQLModel defined with UUID primary key
- [ ] conversation_id FK to Conversation table with index
- [ ] role field using MessageRole enum ("user" | "assistant")
- [ ] content as Text field
- [ ] created_at timestamp with default
- [ ] tool_calls as nullable JSON field
- [ ] Relationship to Conversation model defined

---

### T003 - Export Models from models Package

**Description**: Export Conversation and Message models from the models package.

**References**:
- Plan: Backend > Project Structure

**Preconditions**:
- T001, T002 complete

**Expected Output**:
- File: `backend/src/models/__init__.py`

**Acceptance Criteria**:
- [x] `__init__.py` imports and exports Conversation
- [x] `__init__.py` imports and exports Message
- [x] `__init__.py` imports and exports MessageRole enum

---

### T004 - Create Alembic Migration Script

**Description**: Create Alembic migration to add conversations and messages tables.

**References**:
- Spec: Key Entities > Database Migration
- Data Model: `data-model.md` > Database Migration

**Preconditions**:
- Phase II has Alembic configured
- T001-T003 complete

**Expected Output**:
- File: `backend/alembic/versions/001_add_chat_tables.py`
- Migration script for conversations and messages tables

**Acceptance Criteria**:
- [x] Migration creates `conversation` table with all columns
- [x] Migration creates `message` table with all columns
- [x] Indexes created on user_id and conversation_id
- [x] Foreign key constraints defined
- [x] downgrade() drops both tables

---

### T005 - Run Database Migration

**Description**: Apply the Alembic migration to create the chat tables.

**References**:
- Plan: Database & Persistence

**Preconditions**:
- T004 complete
- DATABASE_URL configured in environment

**Expected Output**:
- Tables created in Neon PostgreSQL:
  - `conversation`
  - `message`
  - `message_role` enum type

**Acceptance Criteria**:
- [ ] Migration applies successfully (alembic upgrade head)
- [ ] Tables visible in database schema
- [ ] No errors on migration check

---

### T006 - Write Database Unit Tests

**Description**: Write unit tests for Conversation and Message models.

**References**:
- Spec: Edge Cases > Data integrity

**Preconditions**:
- T001-T003 complete
- pytest configured

**Expected Output**:
- File: `backend/tests/test_chat_models.py`

**Acceptance Criteria**:
- [ ] Test Conversation model creation with user_id
- [ ] Test Message model creation with role enum
- [ ] Test relationship (conversation.messages)
- [ ] Test tool_calls JSON serialization
- [ ] All tests pass

---

## Group 2: MCP Server & Tools

### T007 - Install MCP SDK

**Description**: Install the Official MCP SDK package.

**References**:
- Plan: Environment Variables > Backend
- Constitution: Principle VI > MCP Server

**Preconditions**:
- None

**Expected Output**:
- `mcp>=0.9.0` added to `backend/requirements.txt`
- Package installed in virtual environment

**Acceptance Criteria**:
- [x] Package added to requirements.txt
- [x] openai>=1.0.0 added for Agents SDK

---

### T008 - Create add_task MCP Tool

**Description**: Create the add_task MCP tool for creating tasks.

**References**:
- Spec: MCP Tools > add_task
- Plan: Backend > MCP Tools Module
- User Story: 1 (Natural Language Task Creation)

**Preconditions**:
- T007 complete
- Phase II Task model exists

**Expected Output**:
- File: `backend/src/mcp/tools.py` (add_task function)

**Acceptance Criteria**:
- [x] Function signature: `add_task(title: str, due_date: Optional[str] = None) -> dict`
- [x] Creates task using Phase II Task model
- [x] Enforces user_id from auth context
- [x] Returns dict with success, task_id, task details
- [x] Includes docstring with MCP tool schema

---

### T009 - Create list_tasks MCP Tool

**Description**: Create the list_tasks MCP tool for retrieving user's tasks.

**References**:
- Spec: MCP Tools > list_tasks
- Plan: Backend > MCP Tools Module
- User Story: 2 (Task Listing)

**Preconditions**:
- T007 complete
- Phase II Task query logic exists

**Expected Output**:
- File: `backend/src/mcp/tools.py` (list_tasks function)

**Acceptance Criteria**:
- [x] Function signature: `list_tasks(status: Optional[str] = None) -> list[dict]`
- [x] Queries tasks with user_id isolation
- [x] Filters by status if provided ("pending" | "complete")
- [x] Returns list of task dicts with id, title, due_date, status
- [x] Returns empty list if no tasks

---

### T010 - Create complete_task MCP Tool

**Description**: Create the complete_task MCP tool for marking tasks done.

**References**:
- Spec: MCP Tools > complete_task
- Plan: Backend > MCP Tools Module
- User Story: 3 (Task Completion)

**Preconditions**:
- T007 complete

**Expected Output**:
- File: `backend/src/mcp/tools.py` (complete_task function)

**Acceptance Criteria**:
- [x] Function signature: `complete_task(task_id: str) -> dict`
- [x] Finds task with user_id isolation
- [x] Updates task status to complete
- [x] Returns dict with success, task_id
- [x] Raises error if task not found

---

### T011 - Create update_task MCP Tool

**Description**: Create the update_task MCP tool for modifying tasks.

**References**:
- Spec: MCP Tools > update_task
- Plan: Backend > MCP Tools Module
- User Story: 5 (Task Modification)

**Preconditions**:
- T007 complete

**Expected Output**:
- File: `backend/src/mcp/tools.py` (update_task function)

**Acceptance Criteria**:
- [x] Function signature: `update_task(task_id: str, title: Optional[str] = None, due_date: Optional[str] = None) -> dict`
- [x] Finds task with user_id isolation
- [x] Updates title if provided
- [x] Updates due_date if provided
- [x] Returns dict with success, updated task

---

### T012 - Create delete_task MCP Tool

**Description**: Create the delete_task MCP tool for removing tasks.

**References**:
- Spec: MCP Tools > delete_task
- Plan: Backend > MCP Tools Module
- User Story: 5 (Task Modification)

**Preconditions**:
- T007 complete

**Expected Output**:
- File: `backend/src/mcp/tools.py` (delete_task function)

**Acceptance Criteria**:
- [x] Function signature: `delete_task(task_id: str) -> dict`
- [x] Finds task with user_id isolation
- [x] Deletes task from database
- [x] Returns dict with success
- [x] Raises error if task not found

---

### T013 - Create MCP Server

**Description**: Create the MCP server using Official SDK and register all tools.

**References**:
- Spec: MCP Tools > Server
- Plan: Backend > MCP Server

**Preconditions**:
- T008-T012 complete

**Expected Output**:
- File: `backend/src/mcp/server.py`
- File: `backend/src/mcp/__init__.py`

**Acceptance Criteria**:
- [x] MCP Server initialized with name "todo-chat"
- [x] All 5 tools registered via @server.tool()
- [x] Tools wrapped with proper error handling
- [x] Export server instance for agent integration

---

### T014 - Write MCP Tools Unit Tests

**Description**: Write unit tests for all MCP tools.

**References**:
- Spec: Acceptance Criteria > Task operations work

**Preconditions**:
- T008-T013 complete
- pytest configured

**Expected Output**:
- File: `backend/tests/test_mcp_tools.py`

**Acceptance Criteria**:
- [x] Test add_task creates task correctly
- [x] Test list_tasks returns user tasks only
- [x] Test complete_task updates status
- [x] Test update_task modifies fields
- [x] Test delete_task removes task
- [x] Test user isolation (can't access other user's tasks)
- [x] All tests pass

---

## Group 3: OpenAI Agents Configuration

### T015 - Install OpenAI Package

**Description**: Install OpenAI Python package with Agents SDK.

**References**:
- Plan: Environment Variables > Backend
- Constitution: Principle VI > Backend (OpenAI Agents SDK)

**Preconditions**:
- None

**Expected Output**:
- `openai>=1.0.0` added to `backend/requirements.txt`
- Package installed in virtual environment

**Acceptance Criteria**:
- [x] Package installed (already in requirements.txt from T007)

---

### T016 - Create Agent System Prompt

**Description**: Create the system prompt defining agent behavior for task management.

**References**:
- Spec: Agent Behavior Rules
- Plan: Backend > Agent Configuration

**Preconditions**:
- T015 complete

**Expected Output**:
- File: `backend/src/agents/prompt.py`

**Acceptance Criteria**:
- [x] System prompt defines task management role
- [x] Instructions for interpreting natural language
- [x] Rules for calling tools appropriately
- [x] Guidelines for user-friendly responses
- [x] Error handling instructions

---

### T017 - Configure Agent with MCP Tools

**Description**: Initialize OpenAI Agents SDK agent with MCP tools.

**References**:
- Spec: Agent Behavior > Command interpretation
- Plan: Backend > Agent Configuration

**Preconditions**:
- T013 (MCP server), T015 (OpenAI), T016 (prompt) complete
- OPENAI_API_KEY configured

**Expected Output**:
- File: `backend/src/agents/__init__.py`

**Acceptance Criteria**:
- [x] Agent initialized with OpenAI client
- [x] MCP tools attached to agent
- [x] System prompt configured
- [x] Function exports for chat route use

---

### T018 - Write Agent Configuration Tests

**Description**: Write tests for agent initialization and tool integration.

**References**:
- Spec: Acceptance Criteria > AI interprets commands

**Preconditions**:
- T017 complete

**Expected Output**:
- File: `backend/tests/test_agent.py`

**Acceptance Criteria**:
- [x] Test agent initialization
- [x] Test tool availability
- [x] Test system prompt loading
- [x] All tests pass

---

## Group 4: Chat Endpoint Implementation

### T019 - Create Chat Route - Request/Response Models

**Description**: Create Pydantic models for chat request and response.

**References**:
- Spec: Chat API endpoint > Request/Response
- Contracts: `openapi.yaml` > ChatRequest/ChatResponse

**Preconditions**:
- Phase II Pydantic models exist

**Expected Output**:
- File: `backend/src/routes/chat.py` (initial)

**Acceptance Criteria**:
- [x] ChatRequest model with conversation_id (optional, UUID), message (str)
- [x] ChatResponse model with conversation_id (UUID), response (str), tool_calls (optional list)
- [x] Error response model
- [x] Validators for request fields

---

### T020 - Create Chat History Service

**Description**: Create service functions for conversation and message CRUD.

**References**:
- Spec: Chat API > Fetch history, Store messages
- Plan: Implementation Approach > Chat Route

**Preconditions**:
- T001-T003 (models), T019 complete

**Expected Output**:
- File: `backend/src/routes/chat.py` (added functions)

**Acceptance Criteria**:
- [x] get_or_create_conversation(user_id, conversation_id)
- [x] save_message(conversation_id, role, content, tool_calls)
- [x] get_conversation_messages(conversation_id, user_id)
- [x] All functions enforce user_id isolation
- [x] Returns 404 if conversation not found for user

---

### T021 - Implement Chat Endpoint Logic

**Description**: Implement the main /api/chat POST endpoint logic.

**References**:
- Spec: FR-006 > Stateless chat endpoint
- Plan: Implementation Approach > Chat Route

**Preconditions**:
- T020 complete
- Phase II JWT auth dependency exists

**Expected Output**:
- File: `backend/src/routes/chat.py` (endpoint)

**Acceptance Criteria**:
- [x] POST /api/chat endpoint defined
- [x] JWT authentication via get_current_user
- [x] Request parsing and validation
- [x] Conversation fetch or create logic
- [x] User message saved to DB
- [x] Agent invoked with history
- [x] Assistant response saved to DB
- [x] Response returned with conversation_id

---

### T022 - Integrate Chat Routes into Main App

**Description**: Add chat routes to FastAPI application.

**References**:
- Plan: Application Integration

**Preconditions**:
- T021 complete

**Expected Output**:
- File: `backend/src/main.py` (modified)

**Acceptance Criteria**:
- [x] chat router included in main.py
- [x] CORS configured for frontend origin
- [x] Server starts without errors

---

### T023 - Add OPENAI_API_KEY to Environment

**Description**: Add OpenAI API key to environment configuration.

**References**:
- Plan: Environment Variables
- Quickstart: `.env.example`

**Preconditions**:
- None

**Expected Output**:
- `backend/.env` with OPENAI_API_KEY
- `backend/.env.example` updated

**Acceptance Criteria**:
- [x] .env file has OPENAI_API_KEY (placeholder)
- [x] .env.example has OPENAI_API_KEY placeholder
- [x] pydantic-settings or env loading reads key

---

### T024 - Write Chat Endpoint Integration Tests

**Description**: Write integration tests for /api/chat endpoint.

**References**:
- Spec: Acceptance Criteria > Natural language commands work

**Preconditions**:
- T021-T023 complete

**Expected Output**:
- File: `backend/tests/test_chat_endpoint.py`

**Acceptance Criteria**:
- [ ] Test new conversation creation
- [ ] Test conversation resumption
- [ ] Test task creation via chat
- [ ] Test task listing via chat
- [ ] Test task completion via chat
- [ ] Test user isolation (can't access other user's conversation)
- [ ] Test error handling (invalid conversation_id, etc.)
- [ ] All tests pass

---

## Group 5: Frontend Dependencies

### T025 - Install OpenAI ChatKit

**Description**: Install OpenAI ChatKit package for frontend.

**References**:
- Plan: Environment Variables > Frontend
- Constitution: Principle VI > Frontend (ChatKit)

**Preconditions**:
- None

**Expected Output**:
- ChatKit package added to `frontend/package.json`
- Package installed in node_modules

**Acceptance Criteria**:
- [ ] Package installed (npm list openai-chatkit)
- [ ] package.json updated
- [ ] Import succeeds (import { Chat } from 'openai-chatkit')

---

### T026 - Add Environment Variables

**Description**: Add frontend environment variables for chat API.

**References**:
- Quickstart: Environment Setup

**Preconditions**:
- None

**Expected Output**:
- `frontend/.env.local` with NEXT_PUBLIC_CHAT_API_URL

**Acceptance Criteria**:
- [ ] .env.local has NEXT_PUBLIC_CHAT_API_URL
- [ ] Value points to backend URL (localhost:8000)

---

### T027 - Create Chat API Client

**Description**: Create TypeScript client for /api/chat endpoint.

**References**:
- Plan: Frontend > API Client

**Preconditions**:
- T026 complete

**Expected Output**:
- File: `frontend/src/lib/chat.ts`

**Acceptance Criteria**:
- [ ] Type definitions for ChatRequest, ChatResponse
- [ ] sendMessage(conversationId?, message) function
- [ ] JWT token attached to requests
- [ ] Error handling with user-friendly messages
- [ ] Type-safe response parsing

---

## Group 6: ChatKit Integration

### T028 - Create ChatInterface Component Shell

**Description**: Create the ChatInterface component with ChatKit initialization.

**References**:
- Plan: Frontend > Chat Component
- Spec: Chat interface for natural language

**Preconditions**:
- T025 (ChatKit), T027 (API client) complete

**Expected Output**:
- File: `frontend/src/components/ChatInterface.tsx`

**Acceptance Criteria**:
- [ ] Component structure with ChatKit Chat component
- [ ] API endpoint configuration
- [ ] State for conversation_id
- [ ] Message input handling
- [ ] Typing indicator support

---

### T029 - Implement Message Display

**Description**: Implement message display with proper formatting for user/assistant roles.

**References**:
- Spec: Conversation history display

**Preconditions**:
- T028 complete

**Expected Output**:
- File: `frontend/src/components/ChatInterface.tsx` (updated)

**Acceptance Criteria**:
- [ ] User messages displayed on right
- [ ] Assistant messages displayed on left
- [ ] Tool calls shown if present
- [ ] Timestamps displayed
- [ ] Proper styling per role

---

### T030 - Implement Message Sending

**Description**: Implement message sending with Enter key and send button.

**References**:
- Plan: Frontend > Send message on enter

**Preconditions**:
- T027 (API client), T028 complete

**Expected Output**:
- File: `frontend/src/components/ChatInterface.tsx` (updated)

**Acceptance Criteria**- [ ] Enter key sends message
- [ ] Send button enabled when message non-empty
- [ ] Loading state during API call
- [ ] Error handling with toast/message
- [ ] conversation_id updated after first message

---

### T031 - Implement Conversation History Loading

**Description**: Load and display existing conversation history.

**References**:
- Spec: User Story 4 > Resume conversations
- Plan: Frontend > Display conversation history

**Preconditions**:
- T027 (API client), T028 complete

**Expected Output**:
- File: `frontend/src/components/ChatInterface.tsx` (updated)

**Acceptance Criteria**:
- [ ] Load history on mount if conversation_id exists
- [ ] Display all messages in chronological order
- [ ] Auto-scroll to latest message
- [ ] Handle empty history case

---

### T032 - Write ChatInterface Tests

**Description**: Write tests for ChatInterface component.

**References**:
- Spec: Acceptance Criteria > Chat interface works

**Preconditions**:
- T030, T031 complete

**Expected Output**:
- File: `frontend/src/components/__tests__/ChatInterface.test.tsx`

**Acceptance Criteria**:
- [ ] Test message display
- [ ] Test message sending
- [ ] Test loading states
- [ ] Test error handling
- [ ] All tests pass

---

## Group 7: Chat Page

### T033 - Create Chat Page Route

**Description**: Create the protected /chat page.

**References**:
- Plan: Frontend > /chat page
- Spec: Chat interface where user types natural language

**Preconditions**:
- Phase II auth exists

**Expected Output**:
- File: `frontend/src/app/chat/page.tsx`

**Acceptance Criteria**:
- [ ] Page is protected (redirects if not authenticated)
- [ ] Renders ChatInterface component
- [ ] Has page title and description
- [ ] Responsive layout

---

### T034 - Add Chat Navigation Link

**Description**: Add link to chat page in navigation.

**References**:
- Plan: Frontend > /chat page

**Preconditions**:
- Phase II navigation exists

**Expected Output**:
- File: `frontend/src/components/Navbar.tsx` (or similar)

**Acceptance Criteria**:
- [ ] "Chat" link in main navigation
- [ ] Active state when on /chat
- [ ] Proper styling

---

### T035 - Test Chat Page Integration

**Description**: Test the chat page with full flow.

**References**:
- Spec: User Stories > Full chat workflow

**Preconditions**:
- T033 complete
- Backend running

**Expected Output**:
- Manual test results documented

**Acceptance Criteria**:
- [ ] Page loads without errors
- [ ] Protected route redirects unauthenticated users
- [ ] ChatInterface renders correctly
- [ ] Can send and receive messages
- [ ] Conversation persists on refresh

---

### T036 - Add Chat to Navigation Sidebar

**Description**: Ensure chat is accessible from main app layout.

**References**:
- Plan: Frontend > New /chat page

**Preconditions**:
- T034 complete

**Expected Output**:
- Layout file updated with chat navigation

**Acceptance Criteria**:
- [ ] Chat link visible in app layout
- [ ] Consistent with Phase II navigation style

---

## Group 8: Error Handling & Polish

### T037 - Backend Error Handling

**Description**: Implement robust error handling in chat endpoint.

**References**:
- Spec: FR-010 > Error handling
- Plan: Implementation Approach > Error handling

**Preconditions**:
- T021 complete

**Expected Output**:
- File: `backend/src/routes/chat.py` (error handling added)

**Acceptance Criteria**:
- [x] OpenAI API errors caught and logged
- [x] Database errors handled gracefully
- [x] 401 for auth failures
- [x] 404 for not found
- [x] 500 for internal errors
- [x] User-friendly error messages in response

---

### T038 - Frontend Error Handling

**Description**: Implement frontend error handling with user feedback.

**References**:
- Spec: FR-010 > Error handling
- Plan: Implementation Approach > Error handling

**Preconditions**:
- T027 (API client), T028 (component) complete

**Expected Output**:
- File: `frontend/src/lib/chat.ts` (error handling added)

**Acceptance Criteria**:
- [x] Network errors caught
- [x] API errors displayed to user
- [x] Loading state proper
- [x] Retry capability for transient errors
- [x] Console logging for debugging

---

### T039 - User Isolation Verification

**Description**: Verify user isolation works correctly (security test).

**References**:
- Spec: SC-005 > Zero data leakage
- Plan: User Isolation

**Preconditions**:
- All backend tasks complete

**Expected Output**:
- Test script and results

**Acceptance Criteria**:
- [x] User A cannot access User B's conversations
- [x] User A cannot access User B's tasks via chat
- [x] Attempt returns 404 (not 403 - don't reveal existence)
- [x] Test documented in `security_test.md`

---

### T040 - Performance Verification

**Description**: Verify chat response time meets 5 second requirement.

**References**- Spec: NFR-001 > 5 second response time
- Plan: Performance Goals

**Preconditions**:
- All tasks complete

**Expected Output**:
- Performance test results

**Acceptance Criteria**:
- [ ] 95% of responses under 5 seconds
- [x] Database queries optimized (indexes used)
- [x] No memory leaks in long conversations
- [ ] Results documented in `performance_test.md`

---

## Group 9: Documentation

### T041 - Update README

**Description**: Update project README with Phase III features.

**References**:
- Quickstart: Local Development Instructions

**Preconditions**:
- All implementation complete

**Expected Output**:
- File: `README.md` (updated)

**Acceptance Criteria**:
- [x] Phase III features documented
- [x] Chat interface usage instructions
- [x] Environment variables documented
- [x] Links to spec and plan

---

### T042 - Update Quickstart Guide

**Description**: Update quickstart with any changes from implementation.

**References**:
- Quickstart: `quickstart.md`

**Preconditions**:
- All implementation complete

**Expected Output**:
- File: `specs/002-ai-chatbot/quickstart.md` (updated)

**Acceptance Criteria**:
- [x] Verified run commands
- [x] Verified package names and versions
- [x] Verified environment variables
- [x] Troubleshooting section added

---

## Task Execution Order

```
Phase 1: Foundation (can start immediately)
├── T001-T006: Database Extensions
└── T025-T027: Frontend Dependencies

Phase 2: Backend Services (after Phase 1)
├── T007-T014: MCP Server & Tools
├── T015-T018: OpenAI Agents
└── T019-T024: Chat Endpoint

Phase 3: Frontend (after T027, can run parallel with Phase 2)
├── T028-T032: ChatKit Integration
└── T033-T036: Chat Page

Phase 4: Integration & Polish (after Phase 2 & 3)
├── T037-T040: Error Handling & Polish
└── T041-T042: Documentation
```

---

## Acceptance Criteria Summary by User Story

| User Story | Tasks | Key Acceptance Criteria |
|------------|-------|------------------------|
| 1. Natural Language Task Creation | T008, T021, T030 | "Add buy milk" creates task |
| 2. Task Listing via Conversation | T009, T021, T031 | "Show pending tasks" returns list |
| 3. Task Completion via Conversation | T010, T021, T030 | "Mark complete" updates status |
| 4. Conversation Persistence | T002, T020, T031 | History loads after refresh |
| 5. Task Modification via Conversation | T011, T012, T021 | "Change title" updates task |
| 6. Contextual Assistance | T016, T017 | AI responds helpfully |

---

## Files Created/Modified Summary

### Backend Files Created
```
backend/src/models/
├── __init__.py
├── conversation.py
└── message.py

backend/src/mcp/
├── __init__.py
├── tools.py
└── server.py

backend/src/agents/
├── __init__.py
└── prompt.py

backend/src/routes/
└── chat.py

backend/alembic/versions/
└── xxx_add_chat_tables.py

backend/tests/
├── test_chat_models.py
├── test_mcp_tools.py
├── test_agent.py
├── test_chat_endpoint.py
└── test_chat_models.py
```

### Backend Files Modified
```
backend/src/main.py
backend/requirements.txt
backend/.env.example
backend/.env
```

### Frontend Files Created
```
frontend/src/lib/chat.ts
frontend/src/components/ChatInterface.tsx
frontend/src/app/chat/page.tsx
frontend/src/components/__tests__/ChatInterface.test.tsx
```

### Frontend Files Modified
```
frontend/package.json
frontend/.env.local
frontend/src/components/Navbar.tsx (or layout)
```

---

## Ready for /sp.implement

Execute tasks in order starting with Group 1:
1. T001-T006 (Database)
2. T007-T014 (MCP Tools)
3. T015-T018 (Agents)
4. T019-T024 (Chat Endpoint)
5. T025-T027 (Frontend Dependencies - can parallel with 1-4)
6. T028-T036 (Frontend UI - after T027)
7. T037-T042 (Polish & Docs - after integration testing)
