import logging
from typing import Callable
from src.application.dtos.user_dto import CreateUserDTO, UserResponseDTO, UpdateUserDTO
from src.domain.entities.profile import Profile
from src.domain.entities.user import User
from src.domain.interfaces.unit_of_work import UnitOfWork
from src.infrastructure.external_apis.jsonplaceholder_client import JSONPlaceholderClient

logger = logging.getLogger(__name__)


class UserService:
    def __init__(
            self,
            uow_factory: Callable[[], UnitOfWork],
            external_api_client: JSONPlaceholderClient | None = None,
    ):
        self._uow_factory = uow_factory
        self._external_api = external_api_client

    async def create_user(self, create_dto: CreateUserDTO) -> UserResponseDTO:
        logger.info(f"Creating user with email {create_dto.email}")

        try:
            async with self._uow_factory() as uow:
                normalized_email = create_dto.email.strip().lower()

                if await uow.user_repository.exists_by_email(normalized_email):
                    raise ValueError(f"User with email {create_dto.email} already exists")

                user = User.create(
                    email=create_dto.email,
                    username=create_dto.username,
                    full_name=create_dto.full_name,
                )

                saved_user = await uow.user_repository.save(user)

                profile = Profile.create(saved_user.id)
                await uow.profile_repository.save(profile)

                await uow.commit()
                logger.info(f"User created successfully with id {saved_user.id}")

            if self._external_api:
                try:
                    await self._external_api.create_post(
                        saved_user.id,
                        "Welcome!",
                        f"Welcome {saved_user.username}!"
                    )
                    logger.info(f"Welcome post created for user {saved_user.id}")
                except Exception as e:
                    logger.error(f"Failed to sync with external API: {e}")

            return UserResponseDTO.from_entity(saved_user)

        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating user: {e}", exc_info=True)
            raise ValueError(f"Failed to create user: {str(e)}")

    async def get_user(self, user_id: int) -> UserResponseDTO | None:
        logger.info(f"Getting user {user_id}")

        async with self._uow_factory() as uow:
            user = await uow.user_repository.get_by_id(user_id)
            if not user:
                return None
            return UserResponseDTO.from_entity(user)

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> list[UserResponseDTO]:
        logger.info(f"Getting all users (skip={skip}, limit={limit})")

        async with self._uow_factory() as uow:
            users = await uow.user_repository.get_all(skip, limit)
            return [UserResponseDTO.from_entity(user) for user in users]

    async def update_user(self, user_id: int, update_dto: UpdateUserDTO) -> UserResponseDTO | None:
        logger.info(f"Updating user {user_id}")

        async with self._uow_factory() as uow:
            user = await uow.user_repository.get_by_id(user_id)
            if not user:
                return None

            if update_dto.email is not None:
                existing_user = await uow.user_repository.get_by_email(update_dto.email)
                if existing_user and existing_user.id != user_id:
                    raise ValueError(f"Email {update_dto.email} is already taken")
                user.change_email(update_dto.email)

            if update_dto.username is not None:
                user.change_username(update_dto.username)

            if update_dto.full_name is not None:
                user.change_name(update_dto.full_name)

            if update_dto.is_active is not None:
                if update_dto.is_active:
                    user.activate()
                else:
                    user.deactivate()

            updated_user = await uow.user_repository.update(user)
            await uow.commit()

            logger.info(f"User {user_id} updated successfully")
            return UserResponseDTO.from_entity(updated_user)

    async def delete_user(self, user_id: int) -> bool:
        logger.info(f"Deleting user {user_id}")

        async with self._uow_factory() as uow:
            await uow.profile_repository.delete(user_id)

            result = await uow.user_repository.delete(user_id)

            if result:
                await uow.commit()
                logger.info(f"User {user_id} deleted successfully")

            return result
