---
id: "002"
title: "Create Phase II Technical Plan"
stage: "plan"
date: "2025-12-30"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "todo-app"
branch: "001-todo-app"
user: "human"
command: "/sp.plan"
labels: ["planning","phase2","technical-design"]
links:
  spec: "specs/001-todo-app/spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "specs/001-todo-app/plan.md"
  - "specs/001-todo-app/research.md"
  - "specs/001-todo-app/data-model.md"
  - "specs/001-todo-app/quickstart.md"
  - "specs/001-todo-app/contracts/openapi.yaml"
tests: []
---

## Prompt

Create the complete technical implementation plan for Phase II "Todo Web Application" based strictly on the approved specification and constitution.

Feature: 001-todo-app (specs/001-todo-app/spec.md)

Plan MUST include:

1. Monorepo Architecture Overview
   - /frontend → Next.js 16+ App Router project
   - /backend → FastAPI Python project
   - Shared .env for secrets

2. Backend Implementation Plan (FastAPI)
   - Project structure: main.py, models.py, routes/tasks.py, dependencies/auth.py, db.py
   - SQLModel models: Task with user_id foreign key
   - Database connection to Neon PostgreSQL via DATABASE_URL
   - JWT authentication dependency:
     - Use PyJWT to verify token from Authorization: Bearer header
     - Extract user_id from token payload
     - Raise 401 if invalid/missing
   - All task routes filter by current_user.id
   - CRUD + toggle complete endpoints exactly as specified

3. Frontend Implementation Plan (Next.js)
   - Project setup with TypeScript + Tailwind CSS
   - Install and configure Better Auth with JWT plugin enabled
   - Pages:
     - app/login/page.tsx
     - app/signup/page.tsx
     - app/page.tsx (protected dashboard with task list + form)
   - API client that automatically attaches JWT token to headers
   - Responsive task list with [ ] / [x] indicators
   - Forms for add/update tasks

4. Authentication Flow
   - Better Auth handles signup/signin → issues JWT
   - JWT stored in httpOnly cookie or localStorage (as per Better Auth default)
   - Every API call includes Bearer token
   - Backend verifies token → gets user_id → filters tasks

5. Environment Variables
   - BETTER_AUTH_SECRET (same in frontend and backend)
   - DATABASE_URL (Neon connection string)

6. Local Development Instructions
   - Backend: uvicorn main:app --reload
   - Frontend: npm run dev
   - How to set up .env files

Strict Constraints:
- ONLY use approved tech stack from constitution
- No manual coding yet — this is just the HOW plan
- No extra features beyond specification

This plan serves as the blueprint for task breakdown and implementation.

## Response snapshot

Created comprehensive technical plan at `specs/001-todo-app/`:
- plan.md: Full implementation blueprint with monorepo structure, constitution check, backend/frontend plans
- research.md: Technology decisions for Better Auth, FastAPI, SQLModel, PyJWT, Neon PostgreSQL
- data-model.md: Task entity with user_id FK, API data types, SQL migration
- quickstart.md: Development setup guide with environment configuration
- contracts/openapi.yaml: Complete OpenAPI 3.0 specification for all 6 endpoints

## Outcome

- Impact: Technical blueprint ready for task breakdown and implementation
- Files: 5 new planning artifacts created
- Next prompts: Ready for task generation via `/sp.tasks`
- Reflection: All constitution checks pass; no violations or clarifications needed

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results: PASS - all gates passed
- Prompt variant: N/A
- Next experiment: N/A
