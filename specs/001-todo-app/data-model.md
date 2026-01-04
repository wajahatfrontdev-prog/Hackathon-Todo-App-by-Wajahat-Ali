# Data Model: Todo Web Application

**Feature**: 001-todo-app | **Date**: 2025-12-30

## Entities

### User

**Note**: User management is handled by Better Auth. The User entity is defined and managed by Better Auth internally. Backend only needs to interact with JWT tokens for user identification.

**Attributes** (managed by Better Auth):
- `id`: UUID primary key
- `email`: Unique email address
- `password_hash`: Bcrypt hashed password
- `created_at`: Timestamp of registration

**Relationships**:
- One-to-many with Task (via user_id foreign key)

### Task

Represents a todo item owned by an authenticated user.

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key | Unique task identifier |
| `user_id` | UUID | Foreign Key, Not Null | Owner of the task |
| `title` | String | Not Null, 1-500 chars | Task title (required) |
| `description` | String | Nullable, max 5000 chars | Optional task details |
| `completed` | Boolean | Default: False | Completion status |
| `created_at` | DateTime | Auto-generated | Creation timestamp |
| `updated_at` | DateTime | Auto-generated | Last modification timestamp |

**Relationships**:
- Many-to-one with User (Task belongs to User)
- FK constraint: `fk_task_user` references `users.id`

**Validation Rules**:
- Title must be non-empty string after stripping whitespace
- Description can be null or non-empty string
- Completed is boolean, defaults to False

**State Transitions**:
- `completed`: False → True (toggle), True → False (toggle)

## Schema Diagram

```
┌─────────────────────────────────────┐
│              users                  │
│  (managed by Better Auth)           │
├─────────────────────────────────────┤
│ id: UUID (PK)                       │
│ email: String (unique)              │
│ password_hash: String               │
│ created_at: DateTime                │
└─────────────────────────────────────┘
              │ 1
              │
              │ user_id
              ▼ N
┌─────────────────────────────────────┐
│              tasks                  │
├─────────────────────────────────────┤
│ id: UUID (PK)                       │
│ user_id: UUID (FK → users.id)       │
│ title: String (1-500 chars)         │
│ description: String (nullable)      │
│ completed: Boolean (default: false) │
│ created_at: DateTime                │
│ updated_at: DateTime                │
└─────────────────────────────────────┘
```

## SQL Migration

```sql
-- Tasks table creation
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for user queries (common operation)
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Index for sorting by created_at
CREATE INDEX idx_tasks_created_at ON tasks(user_id, created_at DESC);
```

## API Data Types

### TaskResponse (GET /api/tasks)

```typescript
interface TaskResponse {
  id: string;           // UUID as string
  user_id: string;      // UUID as string
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;   // ISO 8601 timestamp
  updated_at: string;   // ISO 8601 timestamp
}
```

### CreateTaskRequest (POST /api/tasks)

```typescript
interface CreateTaskRequest {
  title: string;        // Required, 1-500 chars
  description?: string; // Optional, max 5000 chars
}
```

### UpdateTaskRequest (PUT /api/tasks/{id})

```typescript
interface UpdateTaskRequest {
  title?: string;       // Optional, 1-500 chars
  description?: string; // Optional, max 5000 chars
}
```

### TaskListResponse (GET /api/tasks)

```typescript
interface TaskListResponse {
  tasks: TaskResponse[];
  total: number;
}
```

## Error Responses

```typescript
interface ErrorResponse {
  detail: string;       // Human-readable error message
  // Common errors:
  // - "Authentication required"
  // - "Not authorized to access this task"
  // - "Task not found"
  // - "Title is required"
}
```
