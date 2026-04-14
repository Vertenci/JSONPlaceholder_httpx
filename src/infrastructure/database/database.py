import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine, AsyncSession
from ..config.settings import settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._async_session_maker: async_sessionmaker | None = None

    async def initialize(self):
        logger.info("Initializing database connection...")

        connect_args = {}

        if settings.DB_DRIVER == "postgresql":
            server_settings = {
                "application_name": settings.APP_NAME,
                "timezone": settings.APP_TIMEZONE,
                "statement_timeout": str(settings.DB_STATEMENT_TIMEOUT),
            }

            connect_args = {
                "server_settings": server_settings,
                "timeout": getattr(settings, 'DB_CONNECT_TIMEOUT', 10),
                "command_timeout": getattr(settings, 'DB_COMMAND_TIMEOUT', 30),
            }

        self._engine = create_async_engine(
            str(settings.DATABASE_URL),
            echo=settings.DB_ECHO,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
            pool_pre_ping=True,
            pool_recycle=settings.DB_POOL_RECYCLE,
            pool_timeout=settings.DB_POOL_TIMEOUT,
            connect_args=connect_args,
        )

        self._async_session_maker = async_sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )

        logger.info("Database connection initialized")

    async def close(self):
        if self._engine:
            await self._engine.dispose()
            logger.info("Database connection closed")

    def get_session_factory(self) -> async_sessionmaker:
        if not self._async_session_maker:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        return self._async_session_maker

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        if not self._async_session_maker:
            raise RuntimeError("Database not initialized")

        async with self._async_session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise


db_manager = DatabaseManager()
