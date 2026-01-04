# Research: Todo Web Application

**Feature**: 001-todo-app | **Date**: 2025-12-30

## Technology Research

### Better Auth with JWT Plugin

**Decision**: Use Better Auth with JWT plugin enabled
- **Rationale**: Constitution mandates Better Auth. JWT plugin issues tokens compatible with PyJWT backend verification. Better Auth handles all user management (signup, signin, signout) automatically.
- **Alternatives considered**: Custom auth implementation (violates constitution), session-based auth (incompatible with API-centric design)
- **Key findings**:
  - Better Auth provides React hooks for client-side auth state
  - JWT plugin issues Bearer tokens in standard format
  - Tokens are signed with BETTER_AUTH_SECRET (shared with backend)

### FastAPI + SQLModel Integration

**Decision**: Use SQLModel as ORM with FastAPI
- **Rationale**: Constitution mandates SQLModel. SQLModel combines SQLAlchemy's ORM capabilities with Pydantic's validation.
- **Alternatives considered**: Raw SQL (no type safety), raw SQLAlchemy (more verbose than needed)
- **Key findings**:
  - SQLModel models inherit from both Table and Pydantic BaseModel
  - Async support via SQLAlchemy async engine
  - Neon PostgreSQL supports async connections

### PyJWT Token Verification

**Decision**: Use PyJWT for token verification on backend
- **Rationale**: Standard Python JWT library, widely used and well-documented
- **Key findings**:
  - PyJWT.decode() verifies signature using same secret as Better Auth
  - Token expiration (exp claim) automatically validated
  - Custom claims (user_id) accessible in payload

### Neon PostgreSQL Connection

**Decision**: Use async psycopg connection string from DATABASE_URL
- **Rationale**: Neon provides connection strings optimized for serverless
- **Key findings**:
  - Connection pooling configured automatically by Neon
  - Use asyncpg driver for best performance
  - DATABASE_URL contains all connection parameters

## Best Practices

### JWT Security

- Token expiration: Set to 7 days for reasonable UX
- Always verify signature with secret
- Never store sensitive data in token payload
- Return 401 on missing/invalid tokens

### User Data Isolation

- Every Task must have user_id foreign key
- ALL queries must filter by current_user.id
- Check ownership before update/delete operations
- Return 403 if user attempts to access others' tasks

### Responsive Design

- Mobile-first approach (320px minimum)
- Use Tailwind CSS utility classes
- Flexbox/Grid for layout
- Test on actual devices during development

## Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Auth library | Better Auth | Constitution mandate |
| Auth tokens | JWT with BETTER_AUTH_SECRET | Backend compatibility |
| Backend framework | FastAPI | Constitution mandate |
| ORM | SQLModel | Constitution mandate |
| Database | Neon PostgreSQL | Constitution mandate |
| JWT verification | PyJWT | Standard Python library |
| Frontend framework | Next.js 16+ | Constitution mandate |
| Styling | Tailwind CSS | Constitution mandate |

## Open Questions Resolved

- **Q**: How does Better Auth share user data with backend?
  - **A**: JWT contains user_id; backend extracts from token payload

- **Q**: What format does Better Auth use for tokens?
  - **A**: Standard JWT (JWS) with Bearer token in Authorization header

- **Q**: How to handle token expiration?
  - **A**: Better Auth manages client-side; PyJWT validates exp claim

- **Q**: What validation for task title?
  - **A**: Required, non-empty string, max 500 characters
