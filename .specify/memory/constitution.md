<!--
================================================================================
SYNC IMPACT REPORT - Constitution Amendment for Phase III
================================================================================
Version change: 1.0.0 → 1.1.0 (MINOR - new principles added, expanded guidance)
Modified principles: None renamed; all Phase I/II rules preserved
Added sections:
  - Principle VI: Phase III Conversational AI
  - Phase III Technology Stack Additions
  - Phase III Governance rules
Removed sections: None
Templates requiring updates: ✅ All templates reviewed and compatible
Follow-up TODOs: None

This amendment adds Phase III "Evolution of Todo - Conversational AI" with:
- OpenAI ChatKit for frontend conversational UI
- OpenAI Agents SDK for AI logic
- MCP Server for tool definitions
- Neon DB persistence for conversations
================================================================================
-->

# Evolution of Todo - Full Stack Web App Constitution

## Core Principles

### I. Mandatory Spec-Driven Development

All development MUST follow the Spec-Driven Development (SDD) lifecycle:
- Constitution → Specs → Plan → Tasks → Implement
- No manual coding outside of approved implementation tasks
- All changes traceable to approved specifications
- Every feature begins with a written specification

**Rationale**: Ensures alignment between stakeholders, prevents scope creep, and creates auditable decision records.

### II. Agent Rules

Agents operating on this codebase MUST adhere to:
- No feature invention: Agents MUST NOT add functionality not specified in approved specs
- Refinement only at spec level: Questions, clarifications, and improvements MUST be proposed as spec amendments, not implemented directly
- No deviation from approved specs: Implementation MUST match specifications exactly; any discrepancy requires spec update and approval

**Rationale**: Prevents agent-driven scope expansion and ensures human oversight of all feature decisions.

### III. Phase II Specific Rules

This Phase II monorepo extends Phase I concepts with multi-user capabilities:
- Multi-user web application with persistent authentication
- Each user MUST see only their own tasks (data isolation)
- JWT-based authentication between frontend and backend
- All user data operations require authentication context

**Rationale**: Phase I MVP was single-user; Phase II requires proper user isolation and authentication.

### IV. Technology Stack

The following technologies are MANDATORY and MUST NOT be substituted:

**Frontend:**
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- Better Auth with JWT plugin enabled

**Backend:**
- FastAPI
- SQLModel
- PyJWT

**Database:**
- Neon Serverless PostgreSQL

**Secrets:**
- BETTER_AUTH_SECRET: Shared secret for JWT token signing

**Rationale**: Consistent stack ensures maintainability, enables cloud-native deployment, and matches team expertise.

### V. Quality Principles

All code MUST meet these non-negotiable standards:
- Clean architecture: Separation of concerns, testable components, minimal coupling
- Secure JWT handling: Tokens MUST be validated on every request, proper expiration, no sensitive data in payload
- Responsive UI: Mobile-first design, accessible to all users
- Cloud-native readiness: 12-factor app principles, environment-based configuration, container-friendly

**Rationale**: These principles ensure production-ready, maintainable, and secure software.

### VI. Phase III Conversational AI Rules

This Phase III extension adds conversational interface capabilities for natural language task management:

**Technology Additions:**
- **Frontend**: OpenAI ChatKit for conversational UI
- **Backend**: OpenAI Agents SDK for AI logic
- **MCP Server**: Official MCP SDK for tool definitions
- **Persistence**: Conversations and messages stored in Neon DB

**Governance Rules:**
- Conversational interface for natural language task management
- Stateless chat endpoint with database-backed persistence
- MCP tools for CRUD operations on tasks and lists
- Agent behavior for command interpretation and execution
- No leakage from future phases: Kubernetes, Kafka, and similar technologies are explicitly OUT OF SCOPE for Phase III

**Rationale**: Phase III enables users to interact with their tasks through natural language while maintaining strict data isolation and following SDD principles.

## Technology Stack Requirements

### Frontend Specifications
- Framework: Next.js 16+ with App Router directory structure
- Language: TypeScript with strict mode enabled
- Styling: Tailwind CSS for all styling needs
- Authentication: Better Auth library with JWT plugin configured
- API Communication: Type-safe fetch with proper error handling

### Backend Specifications
- Framework: FastAPI with type annotations
- ORM: SQLModel for type-safe database operations
- Authentication: PyJWT for JWT token creation and validation
- CORS: Properly configured for frontend origin
- Environment: All secrets via environment variables (no hardcoding)

### Database Specifications
- Provider: Neon Serverless PostgreSQL
- Connection: Via environment variable DATABASE_URL
- Schema: Version-controlled migrations (Alembic or similar)
- Isolation: Row-level security per user (user_id foreign key on all task tables)

### Shared Configuration
- BETTER_AUTH_SECRET: Required for JWT signing/verification
- All secrets loaded from environment at runtime
- .env.example for required variables (no actual secrets)

### Phase III Technology Specifications

**Frontend (ChatKit):**
- OpenAI ChatKit for conversational UI components
- Integration with existing Next.js frontend
- Chat history persistence via API

**Backend (Agents SDK):**
- OpenAI Agents SDK for AI command interpretation
- Stateless chat endpoint design
- User authentication context passed to agent

**MCP Server:**
- Official MCP SDK for tool definitions
- CRUD tools for tasks and lists
- Proper error handling and response formatting

**Database (Phase III Extensions):**
- conversations table for chat sessions
- messages table for individual messages
- user_id isolation enforced via foreign key relationships

## Development Workflow

### Spec-Driven Development Cycle

1. **Constitution**: Establishes non-negotiable rules and technology stack
2. **Specification**: User describes feature; agent creates spec.md with user stories and acceptance criteria
3. **Plan**: Agent researches and creates plan.md with technical approach
4. **Tasks**: Agent generates tasks.md from plan, organized by user story
5. **Implementation**: Agent executes tasks following Red-Green-Refactor where tests are requested

### Agent Compliance
- All PRs/reviews MUST verify spec compliance
- Complexity deviations from constitution MUST be justified in plan.md
- Use `.specify/memory/constitution.md` for runtime guidance
- Refer to `.specify/templates/` for artifact formats

### Code Quality Gates
- Linting passes (ESLint for TS, Ruff for Python)
- Type checking passes (TypeScript, mypy)
- Tests pass (if tests exist for the feature)
- No unresolved placeholder tokens in generated files

## Governance

This constitution is the supreme and stable document for all phases. It establishes binding rules that all agents and contributors MUST follow. Phase III amendments extend and do not supersede Phase I/II rules.

### Amendment Procedure
1. Amendments MUST be proposed as changes to this file
2. Major changes (principle additions/removals) require explicit user approval
3. Minor clarifications (expanded guidance) may be made with documentation
4. All amendments MUST update the version number and last amended date

### Versioning Policy
- **MAJOR**: Backward incompatible governance changes, principle removals or redefinitions
- **MINOR**: New principles added, materially expanded guidance
- **PATCH**: Clarifications, wording fixes, non-semantic refinements

### Compliance Review
- Every implementation task MUST reference the applicable constitution principle
- Plan reviews MUST verify all constitution gates pass
- Architecture decisions MUST cite relevant principles

**Version**: 1.1.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2025-12-31
