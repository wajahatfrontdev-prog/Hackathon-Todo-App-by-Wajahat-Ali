---
id: "001"
title: "Phase III technical plan creation"
stage: "plan"
date: "2025-12-31"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "ai-chatbot"
branch: "002-ai-chatbot"
user: "user"
command: "sp.plan"
labels: ["phase3","technical-plan","architecture","mcp","agents-sdk"]
links:
  spec: "specs/002-ai-chatbot/spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "specs/002-ai-chatbot/plan.md"
  - "specs/002-ai-chatbot/research.md"
  - "specs/002-ai-chatbot/data-model.md"
  - "specs/002-ai-chatbot/quickstart.md"
  - "specs/002-ai-chatbot/contracts/openapi.yaml"
tests:
  - "none"
---

## Prompt

Create the complete technical implementation plan for Phase III "AI-Powered Conversational Task Manager".

Feature: 002-ai-chatbot (specs/002-ai-chatbot/spec.md)

Plan MUST include:

1. Architecture Overview
   - Extend existing monorepo (Phase II backend + frontend)
   - New /chat page with OpenAI ChatKit
   - New /api/chat endpoint in FastAPI
   - OpenAI Agents SDK for agent logic
   - Official MCP SDK for tool server

2. Backend Implementation Plan
   - New models: Conversation and Message (SQLModel)
   - MCP tools module with 5 tools (add_task, list_tasks, update_task, delete_task, complete_task)
   - OpenAI Agents configuration with MCP tools
   - Stateless /api/chat endpoint:
     - Fetch history from DB
     - Run agent with tools
     - Store user + assistant messages
     - Return response
   - Reuse Phase II JWT auth (user_id from token)

3. Frontend Implementation Plan
   - New /chat page (protected)
   - Integrate OpenAI ChatKit
   - Connect to /api/chat endpoint
   - Display conversation history
   - Send message on enter

4. Database & Persistence
   - Add conversations and messages tables
   - User isolation via user_id FK
   - Conversation resume via conversation_id

5. Environment & Dependencies
   - OPENAI_API_KEY
   - New packages: openai, mcp (official SDK), openai-chatkit

6. Local Development Instructions
   - Backend run command
   - Frontend ChatKit config

Strict Constraints:
- Build directly on Phase II (reuse tasks, auth, DB models)
- Stateless server (no in-memory conversation state)
- Use only approved SDKs from constitution

## Response snapshot

Created comprehensive technical implementation plan with:
- Architecture overview matching constitution requirements
- Backend design with Conversation/Message models and MCP tools
- Frontend design with ChatKit integration
- Data model with SQLModel definitions and migration
- OpenAPI contract for /api/chat endpoint
- Quickstart guide for local development
- Constitution check passing all 6 principles

## Outcome

- ✅ Impact: Complete Phase III technical plan ready for tasks
- 🧪 Tests: N/A (planning phase)
- 📁 Files: 5 created (plan.md, research.md, data-model.md, quickstart.md, contracts/openapi.yaml)
- 🔁 Next prompts: /sp.tasks to generate implementation tasks
- 🧠 Reflection: All design choices align with constitution; no violations requiring justification

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): Constitution check passes all gates
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
