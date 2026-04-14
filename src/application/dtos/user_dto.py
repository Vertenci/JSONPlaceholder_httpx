from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateUserDTO:
    email: str
    username: str
    full_name: str


@dataclass
class UpdateUserDTO:
    email: str | None = None
    username: str | None = None
    full_name: str | None = None
    is_active: bool | None = None


@dataclass
class UserResponseDTO:
    id: int
    email: str
    username: str
    full_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, user):
        return cls(
            id=user.id if user.id is not None else 0,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
