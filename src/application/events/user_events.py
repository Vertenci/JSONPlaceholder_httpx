from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserEvent:
    event_type: str
    user_id: int
    timestamp: datetime
    data: dict


@dataclass
class UserCreatedEvent(UserEvent):
    event_type: str = "user.created"

    @classmethod
    def create(cls, user_id: int, email: str, username: str) -> "UserCreatedEvent":
        return cls(
            user_id=user_id,
            timestamp=datetime.now(),
            data={
                "email": email,
                "username": username,
            }
        )


@dataclass
class UserUpdatedEvent(UserEvent):
    event_type: str = "user.updated"

    @classmethod
    def create(
            cls,
            user_id: int,
            changes: dict
    ) -> "UserUpdatedEvent":
        return cls(
            user_id=user_id,
            timestamp=datetime.now(),
            data={"changes": changes}
        )


@dataclass
class UserDeletedEvent(UserEvent):
    event_type: str = "user.deleted"

    @classmethod
    def create(cls, user_id: int) -> "UserDeletedEvent":
        return cls(
            user_id=user_id,
            timestamp=datetime.now(),
            data={}
        )
