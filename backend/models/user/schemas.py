from typing import Optional

from pydantic import BaseModel, validator
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

    @validator("role", pre=True)
    def convert_role(cls, v):
        if v:
            return v.name
        return ""


class UserSearch(UserBaseSchema):
    id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    active: Optional[bool]
    role_name: Optional[str]


class UserPost(UserBaseSchema):
    role_name: Optional[str]


class UserPut(UserBaseSchema):
    role_name: Optional[str]


UserInDB = pydantic_model_creator(User, name="User", exclude_readonly=True)
