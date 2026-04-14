import logging
from typing import Callable
from src.application.dtos.profile_dto import ProfileResponseDTO, UpdateProfileDTO
from src.domain.interfaces.unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)


class ProfileService:
    def __init__(self, uow_factory: Callable[[], UnitOfWork]):
        self._uow_factory = uow_factory

    async def get_profile(self, user_id: int) -> ProfileResponseDTO | None:
        logger.info(f"Getting profile for user {user_id}")

        async with self._uow_factory() as uow:
            profile = await uow.profile_repository.get_by_user_id(user_id)
            if not profile:
                return None
            return ProfileResponseDTO.from_entity(profile)

    async def update_profile(self, user_id: int, update_dto: UpdateProfileDTO) -> ProfileResponseDTO | None:
        logger.info(f"Updating profile for user {user_id}")

        async with self._uow_factory() as uow:
            profile = await uow.profile_repository.get_by_user_id(user_id)
            if not profile:
                return None

            # Применяем изменения
            if update_dto.bio is not None:
                profile.update_bio(update_dto.bio)

            if update_dto.avatar_url is not None:
                profile.update_avatar(update_dto.avatar_url)

            if update_dto.phone is not None or update_dto.address is not None:
                profile.update_contact(update_dto.phone, update_dto.address)

            # Сохраняем изменения
            updated_profile = await uow.profile_repository.update(profile)
            await uow.commit()

            logger.info(f"Profile for user {user_id} updated successfully")
            return ProfileResponseDTO.from_entity(updated_profile)