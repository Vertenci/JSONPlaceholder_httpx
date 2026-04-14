import logging
from sqlalchemy import select, delete, exists
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.database.models import UserModel

logger = logging.getLogger(__name__)


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        db_user = result.scalar_one_or_none()
        return self._to_domain(db_user) if db_user is not None else None

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        db_user = result.scalar_one_or_none()
        return self._to_domain(db_user) if db_user is not None else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        result = await self._session.execute(
            select(UserModel)
            .order_by(UserModel.email)
            .offset(skip)
            .limit(limit)
        )
        db_users = result.scalars().all()
        return [self._to_domain(user) for user in db_users]

    async def save(self, user: User) -> User:
        db_user = UserModel(
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
        )
        self._session.add(db_user)
        await self._session.flush()
        await self._session.refresh(db_user)

        user.id = db_user.id
        user.created_at = db_user.created_at
        user.updated_at = db_user.updated_at
        return user

    async def update(self, user: User) -> User:
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user.id)
        )
        db_user = result.scalar_one_or_none()

        if db_user:
            db_user.email = user.email
            db_user.username = user.username  # БЕЗ ЗАПЯТОЙ!
            db_user.full_name = user.full_name
            db_user.is_active = user.is_active
            db_user.updated_at = user.updated_at

            await self._session.flush()
            await self._session.refresh(db_user)

            user.updated_at = db_user.updated_at

        return user

    async def delete(self, user_id: int) -> bool:
        result = await self._session.execute(
            delete(UserModel).where(UserModel.id == user_id)
        )
        await self._session.flush()
        return result.rowcount > 0

    async def exists_by_email(self, email: str) -> bool:
        result = await self._session.execute(
            select(exists().where(UserModel.email == email))
        )
        return result.scalar() or False

    def _to_domain(self, db_user: UserModel) -> User:
        return User(
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            full_name=db_user.full_name,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )
