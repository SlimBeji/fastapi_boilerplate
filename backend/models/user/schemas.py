from typing import Optional

from pydantic import BaseModel, field_validator
from tortoise.contrib.pydantic import pydantic_model_creator

from backend.models.user.model import User


class UserBaseSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    active: bool


class UserOverview(BaseModel):
    id: int
    email: str


class UserGet(UserBaseSchema):
    id: int
    role: str

    @field_validator("role", mode="before")
    def convert_role(cls, v):
        if v:
            return v.name
        return ""


class UserSearch(UserBaseSchema):
    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    active: Optional[bool] = None
    role_name: Optional[str] = None


class UserPost(UserBaseSchema):
    role_name: Optional[str] = None


class UserPut(UserBaseSchema):
    role_name: Optional[str] = None


UserInDB = pydantic_model_creator(User, name="UserInDB", exclude_readonly=True)
