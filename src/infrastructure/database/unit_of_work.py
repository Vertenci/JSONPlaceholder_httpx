import logging
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.domain.interfaces.unit_of_work import UnitOfWork
from src.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from src.infrastructure.database.repositories.profile_repository_impl import ProfileRepositoryImpl

logger = logging.getLogger(__name__)


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: async_sessionmaker):
        self._session_factory = session_factory
        self._session: AsyncSession | None = None
        self._is_committed = False

    async def __aenter__(self):
        self._session = self._session_factory()
        self.user_repository = UserRepositoryImpl(self._session)
        self.profile_repository = ProfileRepositoryImpl(self._session)
        self._is_committed = False
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
            logger.error(f"Transaction rolled back due to: {exc_type.__name__}: {exc_val}")
        elif not self._is_committed:
            await self.rollback()
            logger.debug("Transaction rolled back (no commit requested)")

        if self._session is not None:
            await self._session.close()

    async def commit(self):
        if self._session is not None:
            await self._session.commit()
            self._is_committed = True
            logger.debug("Transaction committed")

    async def rollback(self):
        if self._session is not None:
            await self._session.rollback()
            self._is_committed = False
            logger.debug("Transaction rolled back")
