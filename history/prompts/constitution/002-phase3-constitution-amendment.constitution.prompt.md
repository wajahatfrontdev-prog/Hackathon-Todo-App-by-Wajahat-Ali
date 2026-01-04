---
id: "002"
title: "Phase III constitution amendment"
stage: "constitution"
date: "2025-12-31"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "user"
command: "sp.constitution"
labels: ["constitution","phase3","amendment"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - ".specify/memory/constitution.md"
tests:
  - "none"
---

## Prompt

Update the global constitution for "Evolution of Todo" to include Phase III.

Add:
1. Technology Additions for Phase III
   - Frontend: OpenAI ChatKit for conversational UI
   - Backend: OpenAI Agents SDK for AI logic
   - MCP Server: Official MCP SDK for tools
   - Persistence: Conversations and messages in Neon DB

2. Phase III Governance
   - Conversational interface for natural language task management
   - Stateless chat endpoint with DB persistence
   - MCP tools for CRUD operations
   - Agent behavior for command interpretation
   - No leakage from future phases (no K8s, Kafka)

3. Keep all Phase I/II rules intact

This constitution remains supreme.

## Response snapshot

Amended constitution to v1.1.0 with:
- Added Principle VI: Phase III Conversational AI Rules
- Added Phase III Technology Specifications section
- Updated Governance to cover all phases
- Preserved all Phase I/II rules unchanged

## Outcome

- ✅ Impact: Constitution updated with Phase III additions
- 🧪 Tests: N/A (documentation amendment)
- 📁 Files: 1 modified (.specify/memory/constitution.md)
- 🔁 Next prompts: None required
- 🧠 Reflection: Minor version bump appropriate for new principle addition

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
