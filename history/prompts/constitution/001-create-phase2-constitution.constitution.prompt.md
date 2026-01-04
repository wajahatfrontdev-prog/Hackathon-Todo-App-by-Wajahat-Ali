---
id: "001"
title: "Create Phase II Constitution"
stage: "constitution"
date: "2025-12-30"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "master"
user: "human"
command: "/sp.constitution"
labels: ["constitution","governance","phase2"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - ".specify/memory/constitution.md"
tests: []
---

## Prompt

Create or update the global constitution for the new Phase II project "Evolution of Todo - Full Stack Web App".

This is a fresh monorepo project building on Phase I concepts.

Define:
1. Mandatory Spec-Driven Development
   - No manual coding allowed
   - Follow: Constitution → Specs → Plan → Tasks → Implement

2. Agent Rules
   - No feature invention
   - Refinement only at spec level
   - No deviation from approved specs

3. Phase II Specific Rules
   - Multi-user web application with authentication
   - Persistent Neon PostgreSQL database
   - Data isolation: each user sees only their tasks
   - JWT-based authentication between frontend and backend

4. Technology Stack (STRICT)
   - Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS
   - Backend: FastAPI, SQLModel, PyJWT
   - Database: Neon Serverless PostgreSQL
   - Auth: Better Auth with JWT plugin enabled
   - Shared secret: BETTER_AUTH_SECRET

5. Quality Principles
   - Clean architecture
   - Secure JWT handling
   - Responsive UI
   - Cloud-native readiness

This constitution is supreme and stable for Phase II.

## Response snapshot

Created initial constitution at `.specify/memory/constitution.md` with:
- 5 Core Principles (SDD lifecycle, Agent Rules, Phase II Rules, Technology Stack, Quality Principles)
- Technology Stack Requirements section with detailed specs for Frontend, Backend, Database
- Development Workflow section documenting the SDD cycle
- Governance section with amendment procedure and versioning policy
- Version: 1.0.0 (initial creation)

## Outcome

- Impact: Constitution established as supreme document for Phase II development
- Files: .specify/memory/constitution.md
- Next prompts: Ready for feature specification via `/sp.specify`
- Reflection: Constitution provides clear guardrails for agent behavior and technology choices

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results: PASS - all template validations passed
- Prompt variant: N/A
- Next experiment: N/A
