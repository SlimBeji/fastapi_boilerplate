from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from backend.models.role.model import Role


class RoleBaseSchema(BaseModel):
    name: str
    level: int
    description: str


class RoleOverview(BaseModel):
    id: int
    name: str
    description: str


class RoleGet(RoleBaseSchema):
    id: int


class RoleSearch(RoleBaseSchema):
    id: Optional[int] = None
    name: Optional[str] = None
    level: Optional[int] = None
    description: Optional[str] = None


class RolePost(RoleBaseSchema):
    pass


class RolePut(RoleBaseSchema):
    pass


RoleInDB = pydantic_model_creator(Role, name="RoleInDB", exclude_readonly=True)
