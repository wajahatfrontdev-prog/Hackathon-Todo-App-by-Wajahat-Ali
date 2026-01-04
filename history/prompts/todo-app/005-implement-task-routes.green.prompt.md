---
id: "005"
title: "Implement Backend Task API Routes T020-T032"
stage: "green"
date: "2025-12-30"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "todo-app"
branch: "001-todo-app"
user: "human"
command: "/sp.implement"
labels: ["implementation","backend","api-routes","phase2"]
links:
  spec: "specs/001-todo-app/spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "backend/src/routes/tasks.py"
  - "backend/src/main.py"
  - "specs/001-todo-app/tasks.md"
tests: []
---

## Prompt

/sp.implement Implement tasks T020 to T032 (Backend Task API Routes).

Generate:
- backend/routes/tasks.py with all 6 endpoints
- Integrate with auth dependency
- Filter all queries by current_user.id
- Full CRUD + toggle complete
- Proper HTTP exceptions

Follow OpenAPI contract exactly.

## Response snapshot

Implemented Phase 3 Task API Routes (T020-T032):

**Created/modified files:**
- `backend/src/routes/tasks.py`: New router module with all 6 task endpoints
- `backend/src/main.py`: Refactored to import and include tasks router
- `specs/001-todo-app/tasks.md`: Marked T020-T032 as complete

**Endpoints implemented (follows OpenAPI contract):**
- GET /api/tasks - List all user's tasks (filtered by user_id)
- POST /api/tasks - Create task (title validation, associate with user)
- GET /api/tasks/{task_id} - Get single task (403 if not owner)
- PUT /api/tasks/{task_id} - Update task (title validation, 403 if not owner)
- DELETE /api/tasks/{task_id} - Delete task (403 if not owner)
- PATCH /api/tasks/{task_id}/complete - Toggle completion (403 if not owner)
- GET /health - Health check

**Key features:**
- All endpoints use get_current_user dependency for JWT auth
- All queries filtered by current_user.id for user isolation
- Proper HTTP exceptions: 400 (validation), 401 (auth), 403 (ownership), 404 (not found)
- Router pattern for modular code organization
- Type-annotated with Annotated[] for dependencies

## Outcome

- Impact: All backend endpoints complete (T010-T032) - Phase 2 and 3 done
- Files: 2 modified, 1 new
- Next prompts: Ready for Phase 4 frontend foundation (T040-T047)
- Reflection: Code follows OpenAPI contract exactly; clean architecture with router pattern

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results: PASS - all endpoints follow OpenAPI spec
- Prompt variant: N/A
- Next experiment: N/A
