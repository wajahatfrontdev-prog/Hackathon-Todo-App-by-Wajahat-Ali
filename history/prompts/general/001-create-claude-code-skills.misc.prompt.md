---
id: "001"
title: "Create Claude Code Skills"
stage: "misc"
date: "2026-01-04"
surface: "agent"
model: "sonnet-4-5-20250929"
feature: "none"
branch: "unknown"
user: "Claude Code User"
command: "sp.implement"
labels: ["skills", "claude-code", "documentation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ".claude/skills/fastapi-backend-skill.SKILL.md"
  - ".claude/skills/nextjs-frontend-skill.SKILL.md"
  - ".claude/skills/openai-chatkit-skill.SKILL.md"
  - ".claude/skills/groq-inference-skill.SKILL.md"
  - ".claude/skills/mcp-tools-skill.SKILL.md"
  - ".claude/skills/sqlmodel-database-skill.SKILL.md"
  - ".claude/skills/better-auth-skill.SKILL.md"
  - ".claude/skills/spec-driven-workflow-skill.SKILL.md"
  - ".claude/skills/README.md"
tests: []
---

## Prompt

Create comprehensive Claude Code Skills for the Todo Web Application Hackathon project.

Create a .claude/skills/ directory in the project root with the following skills (each as a separate SKILL.md file):

1. fastapi-backend-skill
   - Description: Create and manage FastAPI routes, dependencies, and models
   - When to use: Adding new API endpoints, auth, database operations

2. nextjs-frontend-skill
   - Description: Build Next.js App Router pages, components with TypeScript and Tailwind
   - When to use: Creating new pages, UI components, responsive design

3. openai-chatkit-skill
   - Description: Integrate OpenAI ChatKit for conversational AI interface
   - When to use: Building chat UI, handling messages, tool calls display

4. groq-inference-skill
   - Description: Use Groq for fast LLM inference with OpenAI-compatible client
   - When to use: AI agent logic, natural language processing

5. mcp-tools-skill
   - Description: Define and implement MCP tools for task CRUD operations
   - When to use: Adding new task management capabilities for AI agent

6. sqlmodel-database-skill
   - Description: Define SQLModel models and manage Neon PostgreSQL schema
   - When to use: Adding new database tables or relationships

7. better-auth-skill
   - Description: Configure Better Auth with JWT for secure authentication
   - When to use: User signup, login, session management

8. spec-driven-workflow-skill
   - Description: Follow spec-driven development (constitution → spec → plan → tasks → implement)
   - When to use: Any new feature development

Each SKILL.md must follow exact format:
---
name: lowercase-with-hyphens
description: Clear description with when to use it
---
# Skill Title

## Instructions
Step-by-step guidance with examples

## Examples
Concrete code examples

Also create .claude/skills/README.md explaining:
- What skills are available
- How they enable the full AI-powered todo app
- How to use them in development

This will make the project a complete Claude Code skills lab example

## Response snapshot

Created comprehensive Claude Code Skills directory with 9 files:

1. **fastapi-backend-skill.SKILL.md** - FastAPI backend development with routes, dependencies, Pydantic models, error handling, and CORS configuration

2. **nextjs-frontend-skill.SKILL.md** - Next.js 14 App Router development with TypeScript, Tailwind CSS, component patterns, and API client integration

3. **openai-chatkit-skill.SKILL.md** - OpenAI ChatKit integration for conversational AI with chat window, message components, streaming support

4. **groq-inference-skill.SKILL.md** - Groq LLM inference using OpenAI-compatible client with task agent, planner agent, and streaming examples

5. **mcp-tools-skill.SKILL.md** - Model Context Protocol tools for task CRUD operations with tool definitions, server setup, and AI client integration

6. **sqlmodel-database-skill.SKILL.md** - SQLModel database development with Neon PostgreSQL, models, relationships, migrations, and service layer patterns

7. **better-auth-skill.SKILL.md** - JWT authentication with Better Auth including login, register, refresh tokens, and frontend auth hooks

8. **spec-driven-workflow-skill.SKILL.md** - Spec-Driven Development workflow guide covering constitution → spec → plan → tasks → implement → polish phases

9. **README.md** - Comprehensive skills documentation with architecture overview, tech stack mapping, usage examples, and learning path

## Outcome

- ✅ Impact: Created complete Claude Code Skills framework for the Todo Web Application Hackathon project
- 🧪 Tests: No tests required for documentation/skill files
- 📁 Files: 9 skill files created in .claude/skills/
- 🔁 Next prompts: Add skill-specific tests or extend with additional skills (e.g., testing-skill, deployment-skill)
- 🧠 Reflection: The skill system provides a comprehensive development guide enabling AI agents to build consistent, high-quality code following project standards

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Add interactive skill validation or create skill-specific code templates
