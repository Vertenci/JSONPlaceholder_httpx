from pydantic import BaseModel, Field


class CreatePostRequest(BaseModel):
    user_id: int = Field(..., gt=0, description="User ID")
    title: str = Field(..., min_length=1, max_length=200)
    body: str = Field(..., min_length=1)


class PostResponse(BaseModel):
    id: int
    user_id: int
    title: str
    body: str

    model_config = {"from_attributes": True}
