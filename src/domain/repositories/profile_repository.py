from abc import ABC, abstractmethod
from src.domain.entities.profile import Profile


class ProfileRepository(ABC):
    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> Profile | None:
        pass

    @abstractmethod
    async def save(self, profile: Profile) -> Profile:
        pass

    @abstractmethod
    async def update(self, profile: Profile) -> Profile | None:
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        pass
