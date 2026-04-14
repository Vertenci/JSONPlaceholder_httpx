from dataclasses import dataclass


@dataclass
class PostResponseDTO:
    id: int
    user_id: int
    title: str
    body: str
