from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.database import db_manager


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in db_manager.get_session():
        yield session
