from dataclasses import dataclass
from datetime import datetime


@dataclass
class UpdateProfileDTO:
    bio: str | None = None
    avatar_url: str | None = None
    phone: str | None = None
    address: str | None = None


@dataclass
class ProfileResponseDTO:
    id: int
    user_id: int
    bio: str | None
    avatar_url: str | None
    phone: str | None
    address: str | None
    created_at: datetime
    updated_at: datetime | None

    @classmethod
    def from_entity(cls, profile):
        return cls(
            id=profile.id if profile.id is not None else 0,
            user_id=profile.user_id.value,
            bio=profile.bio,
            avatar_url=profile.avatar_url,
            phone=profile.phone,
            address=profile.address,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
        )
