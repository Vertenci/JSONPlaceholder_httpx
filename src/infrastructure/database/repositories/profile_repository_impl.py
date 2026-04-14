import logging
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.profile import Profile
from src.domain.repositories.profile_repository import ProfileRepository
from src.infrastructure.database.models import ProfileModel

logger = logging.getLogger(__name__)


class ProfileRepositoryImpl(ProfileRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, profile_id: int) -> Profile | None:
        result = await self._session.execute(
            select(ProfileModel).where(ProfileModel.id == profile_id)
        )
        db_profile = result.scalar_one_or_none()
        return self._to_domain(db_profile) if db_profile is not None else None

    async def get_by_user_id(self, user_id: int) -> Profile | None:
        result = await self._session.execute(
            select(ProfileModel).where(ProfileModel.user_id == user_id)
        )
        db_profile = result.scalar_one_or_none()
        return self._to_domain(db_profile) if db_profile is not None else None

    async def save(self, profile: Profile) -> Profile:
        db_profile = ProfileModel(
            user_id=profile.user_id,
            bio=profile.bio,
            avatar_url=profile.avatar_url,
            phone=profile.phone,
            address=profile.address,
            created_at=profile.created_at,
        )
        self._session.add(db_profile)
        await self._session.flush()
        await self._session.refresh(db_profile)

        profile.id = db_profile.id
        profile.created_at = db_profile.created_at
        profile.updated_at = db_profile.updated_at
        return profile

    async def update(self, profile: Profile) -> Profile:
        result = await self._session.execute(
            select(ProfileModel).where(ProfileModel.id == profile.id)
        )
        db_profile = result.scalar_one_or_none()

        if db_profile:
            db_profile.bio = profile.bio
            db_profile.avatar_url = profile.avatar_url
            db_profile.phone = profile.phone
            db_profile.address = profile.address
            db_profile.updated_at = profile.updated_at

            await self._session.flush()
            await self._session.refresh(db_profile)

            profile.updated_at = db_profile.updated_at

        return profile

    async def delete(self, user_id: int) -> bool:
        result = await self._session.execute(
            delete(ProfileModel).where(ProfileModel.user_id == user_id)
        )
        await self._session.flush()
        return result.rowcount > 0

    def _to_domain(self, db_profile: ProfileModel) -> Profile:
        return Profile(
            id=db_profile.id,
            user_id=db_profile.user_id,
            bio=db_profile.bio,
            avatar_url=db_profile.avatar_url,
            phone=db_profile.phone,
            address=db_profile.address,
            created_at=db_profile.created_at,
            updated_at=db_profile.updated_at
        )
