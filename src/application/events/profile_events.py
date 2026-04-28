from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProfileEvent:
    event_type: str
    user_id: int
    timestamp: datetime
    data: dict


@dataclass
class ProfileUpdatedEvent(ProfileEvent):
    event_type: str = "profile.updated"

    @classmethod
    def create(
            cls,
            user_id: int,
            changes: dict
    ) -> "ProfileUpdatedEvent":
        return cls(
            user_id=user_id,
            timestamp=datetime.now(),
            data={"changes": changes}
        )
