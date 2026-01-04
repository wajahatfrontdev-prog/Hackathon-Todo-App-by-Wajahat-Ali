---
description: "Task list template for feature implementation"
---

# Tasks: Todo Web Application

**Input**: Design documents from `/specs/001-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Project Setup (Shared Infrastructure)

**Purpose**: Monorepo initialization and basic structure

- [ ] T001 Create monorepo root files: .env.example, requirements.txt (backend deps), package.json (frontend deps)
- [ ] T002 [P] Initialize backend/ directory with FastAPI project structure and requirements.txt
- [ ] T003 [P] Initialize frontend/ directory with Next.js 16+ App Router and Tailwind CSS

---

## Phase 2: Backend Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

### Backend: Database Connection

- [X] T010 Create backend/src/db.py with SQLModel async engine connecting to Neon PostgreSQL
- [X] T011 Define get_db dependency for request-scoped database sessions
- [X] T012 Add startup event to verify database connection

### Backend: Task Model

- [X] T013 Create backend/src/models.py with Task SQLModel (id, user_id, title, description, completed, created_at, updated_at)
- [X] T014 Add Pydantic schemas for TaskCreate, TaskUpdate, TaskResponse
- [X] T015 Configure user_id as required foreign key reference

### Backend: JWT Authentication

- [X] T016 Create backend/src/dependencies/auth.py with get_current_user dependency
- [X] T017 Implement JWT verification using PyJWT with BETTER_AUTH_SECRET
- [X] T018 Extract user_id from token payload and return for task ownership filtering
- [X] T019 Raise HTTPException(401) for missing/invalid Authorization header

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: Backend Task API Routes

**Purpose**: Implement all task CRUD endpoints with JWT authentication

**All endpoints use get_current_user dependency and filter by user_id**

### Task Routes - Read Operations

- [X] T020 [P] [US5] Implement GET /api/tasks endpoint (list all user's tasks)
- [X] T021 [P] [US5] Implement GET /api/tasks/{task_id} endpoint (get single task)

### Task Routes - Create Operation

- [X] T022 [P] [US4] Implement POST /api/tasks endpoint (create task with title, optional description)
- [X] T023 Add title validation (required, 1-500 chars)
- [X] T024 Associate new task with current_user.id

### Task Routes - Update Operation

- [X] T025 [P] [US6] Implement PUT /api/tasks/{task_id} endpoint (update task title/description)
- [X] T026 Add ownership check - return 403 if task.user_id != current_user.id
- [X] T027 Add title validation (required on update, 1-500 chars)

### Task Routes - Delete Operation

- [X] T028 [P] [US7] Implement DELETE /api/tasks/{task_id} endpoint (delete task)
- [X] T029 Add ownership check - return 403 if task.user_id != current_user.id

### Task Routes - Toggle Completion

- [X] T030 [P] [US8] Implement PATCH /api/tasks/{task_id}/complete endpoint (toggle completion)
- [X] T031 Add ownership check - return 403 if task.user_id != current_user.id

### Health Check

- [X] T032 [P] Implement GET /health endpoint for service health verification

**Checkpoint**: All backend endpoints complete (T010-T032) - Ready for Phase 4 frontend foundation

---

## Phase 4: Frontend Foundational (Blocking Prerequisites)

**Purpose**: Frontend infrastructure before authentication pages

### Better Auth Setup

- [X] T040 Install Better Auth and JWT plugin in frontend/
- [X] T041 Create frontend/src/lib/auth.ts with Better Auth configuration
- [X] T042 Configure JWT plugin with BETTER_AUTH_SECRET matching backend
- [X] T043 Export auth client for use across the application

### API Client

- [X] T044 Create frontend/src/lib/api.ts with type-safe fetch wrapper
- [X] T045 Implement automatic JWT token attachment from Better Auth session
- [X] T046 Handle 401 errors by redirecting to /login
- [X] T047 Create API functions: getTasks, getTask, createTask, updateTask, deleteTask, toggleComplete

**Checkpoint**: Frontend foundation ready - authentication pages can now be built

---

## Phase 5: Frontend Authentication Pages

**Purpose**: Login and Signup pages using Better Auth

### Reusable Auth Components

- [X] T050 [P] Create frontend/src/components/AuthForm.tsx (reusable for login/signup)
- [X] T051 Add email and password input fields with validation
- [X] T052 Display error messages from Better Auth responses
- [X] T053 Handle form submission with proper loading states

### Login Page

- [X] T054 [P] [US2] Create frontend/src/app/login/page.tsx
- [X] T055 Integrate AuthForm with signIn action
- [X] T056 Redirect to / on successful signin
- [X] T057 Show "Don't have an account?" link to /signup

### Signup Page

- [X] T058 [P] [US1] Create frontend/src/app/signup/page.tsx
- [X] T059 Integrate AuthForm with signUp action
- [X] T060 Redirect to / on successful signup
- [X] T061 Show "Already have an account?" link to /login

### Signout

- [X] T062 [US3] Create signout functionality (can be component or button)
- [X] T063 Call Better Auth signOut on user action
- [X] T064 Clear local state and redirect to /login

**Checkpoint**: Authentication pages complete (T040-T064) - Ready for Phase 6 dashboard

---

## Phase 6: Frontend Dashboard (Protected Route)

**Purpose**: Main task management dashboard with authentication guard

### Dashboard Layout

- [X] T070 [P] [US5] Create frontend/src/app/page.tsx (root page acts as dashboard)
- [X] T071 Add authentication guard - redirect to /login if not signed in
- [X] T072 Display user welcome message and sign out button
- [X] T073 Create responsive layout for task list and add form

### Add Task Form

- [X] T074 [P] [US4] Create frontend/src/components/TaskForm.tsx
- [X] T075 Add title input (required, validation)
- [X] T076 Add description textarea (optional)
- [X] T077 Call createTask API and refresh task list on success
- [X] T078 Show validation errors for empty title

### Task List Component

- [X] T079 [P] [US5] Create frontend/src/components/TaskList.tsx
- [X] T080 Display all tasks with completion status [ ] / [x]
- [X] T081 Render empty state when user has no tasks
- [X] T082 Call getTasks on component mount and after mutations

### Task Item Component

- [X] T083 [P] [US8] Create TaskItem.tsx for individual task display
- [X] T084 Show checkbox for completion toggle
- [X] T085 Display title (strikethrough if completed)
- [X] T086 Show description if present
- [X] T087 Add edit and delete buttons

### Task Edit/Delete

- [X] T088 [P] [US6] Implement edit functionality in TaskItem
- [X] T089 Show inline edit form or modal for title/description
- [X] T090 Call updateTask API and refresh on success
- [X] T091 [P] [US7] Implement delete button in TaskItem
- [X] T092 Call deleteTask API and remove from list on success
- [X] T093 Add confirmation before delete (simple confirm dialog)

### Toggle Completion

- [X] T094 [P] [US8] Implement checkbox toggle in TaskItem
- [X] T095 Call toggleComplete API and update local state
- [X] T096 Optimistic UI update for better UX

**Checkpoint**: Dashboard complete with all CRUD operations (T070-T096)

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

### Styling & Responsive Design

- [X] T100 Apply Tailwind CSS for mobile-first responsive layout
- [X] T101 Ensure task list works on mobile (320px+) and desktop (1024px+)
- [X] T102 Add visual polish: spacing, colors, typography

### Error Handling

- [X] T110 Display user-friendly error messages for API failures
- [X] T111 Handle network errors gracefully
- [X] T112 Show loading states during API calls

### Documentation

- [X] T120 Create README.md with project overview, setup instructions
- [X] T121 Document environment variables in .env.example comments
- [X] T122 Verify quickstart.md accuracy

### Final Integration Test

- [ ] T130 Test complete user flow: signup → create task → view task → edit → toggle → delete
- [ ] T131 Verify user isolation (create two users, confirm they see only own tasks)
- [ ] T132 Test authentication: verify 401 on unauthenticated API calls

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (Backend Foundation)**: Depends on Phase 1 completion - BLOCKS all user stories
- **Phase 3 (Backend Routes)**: Depends on Phase 2 completion
- **Phase 4 (Frontend Foundation)**: Depends on Phase 1 completion - can run in parallel with Phase 2
- **Phase 5 (Auth Pages)**: Depends on Phase 4 completion
- **Phase 6 (Dashboard)**: Depends on Phase 4 and Phase 5 completion
- **Phase 7 (Polish)**: Depends on all previous phases

### Parallel Opportunities

- T002 and T003 can run in parallel (backend and frontend setup)
- T010, T011, T012 can run in parallel (database setup)
- T013, T014, T015 can run in parallel (models and schemas)
- T016-T019 can run in parallel (auth dependency)
- T020-T021, T022-T024, T025-T027, T028-T029, T030-T031 can run in parallel (task routes)
- T040-T043 can run in parallel (auth setup)
- T044-T047 can run in parallel (API client)
- T050-T053 can run in parallel (reusable components)
- T054-T059 can run in parallel (login and signup pages)
- T070, T074, T079 can run in parallel (dashboard, form, list)
- T083-T087, T088-T090, T091-T092, T094-T096 can run in parallel (task item features)

### Within Each Phase

- Database setup before models
- Models before routes
- Auth dependency before routes
- API client before components
- Components before page integration

---

## Implementation Strategy

### Recommended Order (Single Developer)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Backend Foundation (T010-T019) - CRITICAL
3. Complete Phase 3: Backend Routes (T020-T032)
4. Complete Phase 4: Frontend Foundation (T040-T047)
5. Complete Phase 5: Auth Pages (T050-T064)
6. Complete Phase 6: Dashboard (T070-T096)
7. Complete Phase 7: Polish (T100-T132)

### Parallel Team Strategy

With two developers:

- Developer A: Phases 1-3 (Backend)
- Developer B: Phases 1, 4-5 (Frontend foundation + auth)
- Once Phase 2 complete: Developer B starts Phase 6
- Once Phases 3 and 5 complete: Both work on Phase 6 integration

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (if tests requested)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
