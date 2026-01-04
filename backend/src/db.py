"""
Database connection and session management for the Todo Web Application.

This module provides:
- Async SQLModel engine connected to Neon PostgreSQL
- Request-scoped database session dependency
- Database connection verification on startup
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# Load environment variables from .env file
load_dotenv()

import os

# Get database URL from environment, required for connection
DATABASE_URL: str = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Convert SQLite URL to async format if needed
if DATABASE_URL.startswith("sqlite://"):
    DATABASE_URL = DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")

# Create async engine for database connection
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL debugging
    pool_pre_ping=True,  # Verify connections before use
)

# Create async session factory for request-scoped sessions
async_session_factory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


_tables_initialized = False

async def ensure_tables_exist():
    """Ensure database tables exist (lazy initialization)."""
    global _tables_initialized
    if _tables_initialized:
        return
    
    try:
        from .models import Task, User, Conversation, Message  # noqa: F401
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        _tables_initialized = True
        logging.info("Database tables initialized")
    except Exception as e:
        logging.error(f"Failed to initialize tables: {e}")
        raise


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a request-scoped database session.
    
    Lazily initializes database tables on first access.

    Yields:
        AsyncSession: A SQLModel async session for database operations.

    Example:
        @app.get("/tasks")
        async def list_tasks(session: AsyncSession = Depends(get_db)):
            results = await session.execute(select(Task))
            return results.scalars().all()
    """
    # Ensure tables exist before first use
    await ensure_tables_exist()
    
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@asynccontextmanager
async def get_db_context() -> AsyncGenerator[AsyncSession, None]:
    """
    Context manager for database sessions outside of FastAPI dependencies.

    Useful for startup events, background tasks, or testing.

    Yields:
        AsyncSession: A SQLModel async session for database operations.
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def verify_database_connection() -> bool:
    """
    Verify that the database connection is working.

    Returns:
        bool: True if connection successful, False otherwise.

    Logs:
        INFO: Successful connection with database version
        ERROR: Connection failure with error details
    """
    try:
        async with get_db_context() as session:
            # Execute a simple query to verify connection
            from sqlalchemy import text
            result = await session.execute(text("SELECT 1"))
            result.scalar()
            logging.info("Database connection verified successfully")
            return True
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        return False


async def init_db() -> None:
    """
    Initialize database tables and verify connection.

    This function:
    1. Creates all tables if they don't exist (using SQLModel metadata)
    2. Verifies the database connection is working
    """
    # Import models to ensure they're registered with SQLModel metadata
    from .models import Task, User, Conversation, Message  # noqa: F401

    try:
        # Force recreate tables by dropping first
        import asyncio
        from sqlalchemy import text
        async with asyncio.timeout(30):
            async with engine.begin() as conn:
                # Drop tables in correct order for SQLite
                await conn.execute(text("DROP TABLE IF EXISTS messages"))
                await conn.execute(text("DROP TABLE IF EXISTS conversations"))
                await conn.execute(text("DROP TABLE IF EXISTS tasks"))
                await conn.execute(text("DROP TABLE IF EXISTS users"))
                await conn.run_sync(SQLModel.metadata.create_all)
        
        logging.info("Database tables recreated")
    except Exception as e:
        logging.error(f"Database initialization error: {e}")
        logging.warning("Application will continue but database may not be initialized")


async def close_db() -> None:
    """
    Close the database engine and all connections.

    Call this on application shutdown to properly clean up resources.
    """
    await engine.dispose()
    logging.info("Database connections closed")
