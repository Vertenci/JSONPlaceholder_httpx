from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    id: int | None
    email: str
    username: str
    full_name: str
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @classmethod
    def create(cls, email: str, username: str, full_name: str) -> "User":
        return cls(
            id=None,
            email=email,
            username=username,
            full_name=full_name,
            is_active=True,
        )

    def activate(self) -> None:
        if not self.is_active:
            self.is_active = True
            self.updated_at = datetime.now()

    def deactivate(self) -> None:
        if self.is_active:
            self.is_active = False
            self.updated_at = datetime.now()

    def change_email(self, new_email: str) -> None:
        self.email = new_email
        self.updated_at = datetime.now()

    def change_username(self, new_username: str) -> None:
        self.username = new_username
        self.updated_at = datetime.now()

    def change_name(self, new_full_name: str) -> None:
        self.full_name = new_full_name
        self.updated_at = datetime.now()
