# Research: Phase III AI Chatbot Technology

**Date**: 2025-12-31 | **Feature**: 002-ai-chatbot

## Technology Research

### OpenAI Agents SDK

**Decision**: Use OpenAI Agents SDK for agent behavior

- **Package**: `openai>=1.0.0` (Agents SDK included in openai Python package v1+)
- **Usage**: Creates agents with instructions and tools that can take actions
- **Key features**:
  - Structured agent loops with tool calling
  - Handoffs between agents
  - Guardrails for behavior control
  - Streaming responses

**Reference**: https://platform.openai.com/docs/agents-sdk

### Official MCP SDK

**Decision**: Use Official MCP SDK for tool definitions

- **Package**: `mcp>=0.9.0` (official SDK from Model Context Protocol)
- **Usage**: Defines tools that agents can call; runs as server
- **Key components**:
  - `Server` class for tool definitions
  - `Tool` decorator for function tools
  - Resource and prompt definitions

**Reference**: https://github.com/anthropics/mcp

### OpenAI ChatKit

**Decision**: Use OpenAI ChatKit for frontend conversational UI

- **Package**: `openai-chatkit` (verify exact npm package name)
- **Usage**: React components for chat interface
- **Key features**:
  - Pre-built chat UI components
  - Message threading
  - Typing indicators
  - Attachment support

**Reference**: https://platform.openai.com/docs/chatkit

### Integration Architecture

**Pattern**: MCP Server as tool provider to Agents SDK

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  ChatKit UI     │────▶│  /api/chat      │────▶│  OpenAI Agents  │
│  (Frontend)     │     │  (FastAPI)      │     │  SDK            │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Neon DB        │◀────│  SQLModel       │◀────│  MCP Server     │
│  (Persistence)  │     │  (ORM)          │     │  (Tool Defs)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

**Key Decisions**:
1. MCP server runs in-process with FastAPI (not separate process)
2. Agent receives tools from MCP server configuration
3. Full conversation history passed to agent on each request
4. Stateless design - no in-memory conversation state

---

## Decision Log

| Decision | Rationale | Alternatives Rejected |
|----------|-----------|----------------------|
| OpenAI Agents SDK | Constitution mandates; provides structured agent behavior | Custom LLM integration (violates constitution) |
| Official MCP SDK | Constitution mandates; standardizes tool interface | Custom tool abstraction (violates constitution) |
| ChatKit for UI | Constitution mandates; provides polished components | Custom chat UI (violates constitution, time-consuming) |
| In-process MCP server | Simpler deployment; shares FastAPI process | Separate MCP server process (adds complexity) |
| DB-backed persistence | Constitution requires stateless; reliable across restarts | In-memory sessions (violates stateless requirement) |
