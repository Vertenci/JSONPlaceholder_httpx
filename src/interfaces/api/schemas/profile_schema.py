from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl


class UpdateProfileRequest(BaseModel):
    bio: str | None = Field(None, max_length=500)
    avatar_url: HttpUrl | None = None
    phone: str | None = Field(None, pattern=r'^\+?[1-9]\d{1,14}$')
    address: str | None = None

class ProfileResponse(BaseModel):
    id: int
    user_id: int
    bio: str | None
    avatar_url: str | None
    phone: str | None
    address: str | None
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
