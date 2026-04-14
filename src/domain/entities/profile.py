from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Profile:
    id: int | None
    user_id: int
    bio: str | None = None
    avatar_url: str | None = None
    phone: str | None = None
    address: str | None = None
    created_at: datetime | None = field(default_factory=datetime.now)
    updated_at: datetime | None = field(default_factory=datetime.now)

    @classmethod
    def create(cls, user_id: int) -> "Profile":
        return cls(
            id=None,
            user_id=user_id,
        )

    def update_bio(self, bio: str) -> None:
        self.bio=bio
        self.updated_at = datetime.now()

    def update_avatar(self, avatar_url: str) -> None:
        self.avatar_url = avatar_url
        self.updated_at = datetime.now()

    def update_contact(self, phone: str | None = None, address: str | None = None) -> None:
        if phone is not None:
            self.phone = phone
        if address is not None:
            self.address = address
        self.updated_at = datetime.now()
