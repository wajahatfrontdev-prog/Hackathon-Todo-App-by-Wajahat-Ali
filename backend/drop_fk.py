"""
Drop foreign key constraint from conversations table
"""
from sqlalchemy import text
from src.db import engine
import asyncio

async def migrate():
    async with engine.begin() as conn:
        # Drop the foreign key constraint
        await conn.execute(text("""
            ALTER TABLE IF EXISTS conversations 
            DROP CONSTRAINT IF EXISTS conversations_user_id_fkey;
        """))
        print("Foreign key constraint dropped successfully")

if __name__ == "__main__":
    asyncio.run(migrate())
