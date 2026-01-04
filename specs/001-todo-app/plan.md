# Implementation Plan: Todo Web Application

**Branch**: `001-todo-app` | **Date**: 2025-12-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-app/spec.md`

## Summary

Build a multi-user todo web application with JWT-based authentication. Users can register, sign in, and manage their personal tasks through a responsive web interface. Task data persists in Neon PostgreSQL with strict user isolation ensuring each user sees only their own tasks.

## Technical Context

**Language/Version**: TypeScript 5.x (frontend), Python 3.11+ (backend)
**Primary Dependencies**: Next.js 16+ (App Router), FastAPI, SQLModel, Better Auth, PyJWT
**Storage**: Neon Serverless PostgreSQL via SQLModel
**Testing**: pytest (Python), Jest/Vitest (TypeScript)
**Target Platform**: Web browsers (mobile + desktop responsive)
**Project Type**: Monorepo with separate frontend/backend projects
**Performance Goals**: API responses under 200ms p95, task operations under 2 seconds
**Constraints**: JWT auth required, user data isolation mandatory, no extra features
**Scale/Scope**: Single-tenant web app, dozens to hundreds of users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status | Evidence |
|-----------|-------------|--------|----------|
| I. SDD Lifecycle | Follow Constitution → Specs → Plan → Tasks → Implement | PASS | This plan follows approved spec |
| II. Agent Rules | No feature invention, refinement only at spec level | PASS | Implementation matches spec exactly |
| III. Phase II Rules | Multi-user, data isolation, JWT auth | PASS | User isolation enforced via user_id foreign key |
| IV. Tech Stack | Next.js 16+, FastAPI, SQLModel, Better Auth, Neon PostgreSQL | PASS | All technologies match constitution |
| V. Quality Principles | Clean architecture, secure JWT, responsive UI | PASS | JWT validation on every request, mobile-first CSS |

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-app/
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
├── frontend/                    # Next.js 16+ App Router project
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx       # Root layout with auth provider
│   │   │   ├── page.tsx         # Dashboard (protected)
│   │   │   ├── login/
│   │   │   │   └── page.tsx     # Sign in page
│   │   │   └── signup/
│   │   │       └── page.tsx     # Registration page
│   │   ├── components/
│   │   │   ├── TaskList.tsx     # Task list with toggle
│   │   │   ├── TaskForm.tsx     # Add task form
│   │   │   └── AuthForm.tsx     # Reusable auth form
│   │   └── lib/
│   │       └── api.ts           # API client with JWT attachment
│   ├── package.json
│   └── tailwind.config.js
│
├── backend/                     # FastAPI Python project
│   ├── src/
│   │   ├── main.py              # FastAPI application entry
│   │   ├── models.py            # SQLModel Task and User models
│   │   ├── db.py                # Database connection
│   │   ├── dependencies/
│   │   │   └── auth.py          # JWT authentication dependency
│   │   └── routes/
│   │       └── tasks.py         # Task CRUD endpoints
│   ├── requirements.txt
│   └── .env.example
│
├── .env.example                 # Shared environment template
└── README.md
```

**Structure Decision**: Monorepo with `frontend/` (Next.js) and `backend/` (FastAPI) at repository root. Shared `.env` file in root for local development convenience.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | All design choices align with constitution requirements | N/A |

---

## Phase 0: Research

### Technology Decisions

**Decision**: Use Better Auth with JWT plugin for frontend authentication
- **Rationale**: Constitution mandates Better Auth; JWT plugin enables seamless integration with backend PyJWT validation
- **Alternatives considered**: Custom auth solution (rejected - violates constitution)

**Decision**: Use SQLModel for database operations
- **Rationale**: Type-safe ORM that combines SQLAlchemy and Pydantic; constitution mandates SQLModel
- **Alternatives considered**: Raw SQL (rejected - no type safety), Prisma (rejected - wrong stack)

**Decision**: Use PyJWT for token verification on backend
- **Rationale**: Standard Python JWT library; Better Auth issues tokens that PyJWT can verify
- **Alternatives considered**: python-jose (functionally equivalent, PyJWT more widely used)

**Decision**: Store JWT in httpOnly cookie for Better Auth
- **Rationale**: Better Auth default; provides XSS protection while allowing server validation
- **Alternatives considered**: localStorage (rejected - vulnerable to XSS)

### Integration Patterns

**Better Auth to Backend JWT Flow**:
1. Better Auth signs JWT with BETTER_AUTH_SECRET on signup/signin
2. JWT included in API requests via Authorization: Bearer header
3. Backend extracts Bearer token, verifies with PyJWT using same secret
4. Token payload contains user_id for task ownership filtering

**User Isolation Strategy**:
- Every Task record has required user_id foreign key
- All query operations include WHERE user_id = :current_user_id
- Attempting to access tasks not owned by user returns 403

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

1. **Database Setup** (`db.py`)
   - Create async database engine connecting to Neon PostgreSQL
   - Define get_db dependency for request-scoped sessions

2. **Models** (`models.py`)
   - Define Task SQLModel with all required fields
   - User model handled by Better Auth (frontend-managed)
   - Add relationship for user → tasks

3. **Authentication** (`dependencies/auth.py`)
   - Create get_current_user dependency
   - Extract and verify JWT from Authorization header
   - Return user_id or raise HTTPException(401)

4. **Task Routes** (`routes/tasks.py`)
   - CRUD endpoints with current_user dependency
   - Automatic task filtering by user_id
   - Proper error handling (401, 403, 404)

5. **Application** (`main.py`)
   - FastAPI app with CORS configuration
   - Include task routes
   - Startup event for database connection

### Frontend (Next.js)

1. **Project Setup**
   - Initialize Next.js with TypeScript and Tailwind CSS
   - Install Better Auth with JWT plugin

2. **Authentication Pages**
   - `/login/page.tsx`: Sign in form
   - `/signup/page.tsx`: Registration form
   - Use Better Auth hooks for auth state

3. **Dashboard** (`app/page.tsx`)
   - Protected route (redirect to login if not authenticated)
   - Task list component
   - Add task form

4. **API Client** (`lib/api.ts`)
   - Type-safe fetch wrapper
   - Automatically attach Authorization: Bearer token
   - Handle auth errors (redirect to login on 401)

5. **Components**
   - TaskList: Render tasks with [ ] / [x] indicators
   - TaskForm: Create/edit task with validation
   - AuthForm: Reusable form for login/signup

---

## Next Steps

After this plan is approved:
1. Run `/sp.tasks` to generate implementation tasks organized by user story
2. Execute tasks following the Red-Green-Refactor cycle
3. Verify each user story works independently before moving to next
