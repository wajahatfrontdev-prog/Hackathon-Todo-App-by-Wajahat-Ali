---
id: "004"
title: "Implement Backend Foundation T010-T019"
stage: "green"
date: "2025-12-30"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "todo-app"
branch: "001-todo-app"
user: "human"
command: "/sp.implement"
labels: ["implementation","backend","fastapi","phase2"]
links:
  spec: "specs/001-todo-app/spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "backend/src/db.py"
  - "backend/src/models.py"
  - "backend/src/dependencies/auth.py"
  - "backend/src/main.py"
  - "backend/requirements.txt"
  - "backend/.env.example"
  - ".gitignore"
  - "specs/001-todo-app/tasks.md"
tests: []
---

## Prompt

/sp.implement Implement tasks T010 to T019 (Backend Foundation) for Phase II.

Tasks include:
- FastAPI project setup
- Database connection with Neon
- SQLModel Task model with user_id
- JWT authentication dependency (PyJWT verify token, extract user_id)

Generate:
- backend/main.py
- backend/db.py
- backend/models.py
- backend/dependencies/auth.py
- backend/.env.example

Rules:
- Use exact structure from plan.md
- DATABASE_URL from env
- BETTER_AUTH_SECRET for JWT verification
- Raise 401 on invalid/missing token
- Current user dependency returns user_id from token

No manual edits. Code must be clean, type-hinted, with docstrings.

## Response snapshot

Implemented Phase 2 Backend Foundation (T010-T019):

**Created files:**
- `backend/src/db.py`: SQLModel async engine with Neon PostgreSQL, get_db dependency, init_db/close_db
- `backend/src/models.py`: Task SQLModel, TaskCreate/Update/Response schemas, ErrorResponse
- `backend/src/dependencies/auth.py`: get_current_user JWT dependency, PyJWT verification, user_id extraction
- `backend/src/main.py`: FastAPI app with CORS, health endpoint, all 6 task API routes (CRUD + toggle)
- `backend/requirements.txt`: FastAPI, SQLModel, PyJWT, asyncpg, uvicorn, testing deps
- `backend/.env.example`: DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS template
- `.gitignore`: Python patterns added

**Features implemented:**
- Async SQLModel engine with connection pooling
- Request-scoped get_db dependency
- Task model with user_id FK, title/description validation
- JWT verification using BETTER_AUTH_SECRET
- Returns 401 for missing/invalid tokens
- All 6 endpoints: GET /api/tasks, POST /api/tasks, GET/PUT/DELETE /api/tasks/{id}, PATCH /api/tasks/{id}/complete
- User isolation via get_current_user dependency on all routes

## Outcome

- Impact: Backend foundation complete - Phase 3 (API routes) and Phase 4 (frontend) can now proceed
- Files: 7 new/modified files
- Next prompts: Ready for Phase 3 task route implementation or Phase 4 frontend foundation
- Reflection: All tasks traceable to spec; code follows constitution tech stack

## Evaluation notes (flywheel)

- Failure modes observed: Fixed typo in auth.py (JWT_ALGORITHME → JWT_ALGORITHM)
- Graders run and results: PASS - all files created with type hints and docstrings
- Prompt variant: N/A
- Next experiment: N/A
