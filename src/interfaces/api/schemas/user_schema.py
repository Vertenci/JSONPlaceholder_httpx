import re
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator


class CreateUserRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=2, max_length=255)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Username cannot be empty or contain only spaces")

        if not re.match(r'^[A-Za-zА-Яа-я0-9_*+. -]+$', v):
            raise ValueError("Username must contain only letters, (English/Russian), numbers, and symbols: _ * + . -")

        return v.strip()

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Full name cannot be empty or contain only spaces")

        if not re.match(r'^[A-Za-zА-Яа-я0-9_*+. -]+$', v):
            raise ValueError("Full name must contain only letters, (English/Russian), numbers, and symbols: _ * + . -")

        return v.strip()


class UpdateUserRequest(BaseModel):
    email: EmailStr | None = None
    username: str | None = Field(None, min_length=3, max_length=50)
    full_name: str | None = Field(None, min_length=2, max_length=255)
    is_active: bool | None = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str | None) -> str | None:
        if v is not None:
            if not v or not v.strip():
                raise ValueError("Username cannot be empty or contain only spaces")

            if not re.match(r'^[A-Za-zА-Яа-я0-9_*+. -]+$', v):
                raise ValueError("Username must contain only letters (English/Russian), numbers, and symbols: _ * + .")

            return v.strip()
        return v

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v: str | None) -> str | None:
        if v is not None:
            if not v or not v.strip():
                raise ValueError("Full name cannot be empty or contain only spaces")

            if not re.match(r'^[A-Za-zА-Яа-я0-9_*+. -]+$', v):
                raise ValueError("Full name must contain only letters (English/Russian), numbers, and symbols: _ * + .")

            return v.strip()
        return v


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
