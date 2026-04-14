from dataclasses import dataclass


@dataclass(frozen=True)
class UserId:
    value: int

    def __post_init__(self):
        if not isinstance(self.value, int):
            raise ValueError(f"User ID must be integer, got {type(self.value)}")
        if self.value <= 0:
            raise ValueError("Invalid user ID")
