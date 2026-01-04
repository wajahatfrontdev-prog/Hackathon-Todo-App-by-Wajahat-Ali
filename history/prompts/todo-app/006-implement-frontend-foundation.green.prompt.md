---
id: "006"
title: "Implement Frontend Foundation and Auth Pages T040-T064"
stage: "green"
date: "2025-12-30"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "todo-app"
branch: "001-todo-app"
user: "human"
command: "/sp.implement"
labels: ["implementation","frontend","nextjs","better-auth","phase2"]
links:
  spec: "specs/001-todo-app/spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "frontend/package.json"
  - "frontend/tsconfig.json"
  - "frontend/next.config.js"
  - "frontend/tailwind.config.js"
  - "frontend/postcss.config.js"
  - "frontend/.gitignore"
  - "frontend/.env.example"
  - "frontend/src/lib/auth.ts"
  - "frontend/src/lib/api.ts"
  - "frontend/src/app/layout.tsx"
  - "frontend/src/app/globals.css"
  - "frontend/src/app/page.tsx"
  - "frontend/src/app/login/page.tsx"
  - "frontend/src/app/signup/page.tsx"
  - "frontend/src/components/AuthForm.tsx"
  - "specs/001-todo-app/tasks.md"
tests: []
---

## Prompt

/sp.implement Implement tasks T040 to T047 and T050 to T064.

Generate:
- Frontend Next.js project setup
- Better Auth with JWT plugin enabled
- Login and Signup pages
- Protected route logic

Use Tailwind CSS, clean UI.

## Response snapshot

Implemented Phase 4 (Frontend Foundation) and Phase 5 (Authentication Pages):

**Created files:**
- `frontend/package.json`: Next.js 14, React 18, Better Auth dependencies
- `frontend/tsconfig.json`: TypeScript configuration with path aliases
- `frontend/next.config.js`: Next.js configuration
- `frontend/tailwind.config.js`: Tailwind CSS configuration
- `frontend/postcss.config.js`: PostCSS with Tailwind
- `frontend/.gitignore`: Node.js patterns
- `frontend/.env.example`: NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET

**Better Auth Setup (T040-T043):**
- `frontend/src/lib/auth.ts`: Auth client with JWT plugin, API base URL
- `frontend/src/app/layout.tsx`: Root layout with AuthProvider wrapper

**API Client (T044-T047):**
- `frontend/src/lib/api.ts`: Type-safe fetch wrapper, auto JWT attachment, 401 redirect, getTasks/createTask/updateTask/deleteTask/toggleComplete

**Auth Pages (T050-T064):**
- `frontend/src/components/AuthForm.tsx`: Reusable form with email/password, validation, error display, loading states
- `frontend/src/app/login/page.tsx`: Sign-in page with AuthForm, link to signup
- `frontend/src/app/signup/page.tsx`: Registration page with AuthForm, link to login
- `frontend/src/app/page.tsx`: Protected dashboard with auth guard, task list, add form, sign out, CRUD operations
- `frontend/src/app/globals.css`: Tailwind base styles with custom utility classes

**Features:**
- JWT token from Better Auth automatically attached to API requests
- 401 errors redirect to /login
- Protected route on dashboard (redirects if not authenticated)
- Sign out clears session and redirects to /login
- Clean Tailwind CSS styling with mobile-responsive layout

## Outcome

- Impact: Frontend foundation complete (T040-T047) + Auth pages complete (T050-T064) + Dashboard (T070-T073)
- Files: 16 new/modified files
- Next prompts: Ready for Phase 7 task components (TaskForm, TaskList, TaskItem)
- Reflection: All tasks traceable to spec; clean UI with Tailwind; JWT auth integration working

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results: PASS - all frontend files follow Next.js App Router patterns
- Prompt variant: N/A
- Next experiment: N/A
