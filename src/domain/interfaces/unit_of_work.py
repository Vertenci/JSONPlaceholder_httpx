from abc import ABC, abstractmethod
from src.domain.repositories.profile_repository import ProfileRepository
from src.domain.repositories.user_repository import UserRepository


class UnitOfWork(ABC):
    user_repository: UserRepository
    profile_repository: ProfileRepository

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
