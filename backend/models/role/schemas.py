from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from backend.models.role import Role


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
    id: Optional[int]
    name: Optional[str]
    level: Optional[int]
    description: Optional[str]


class RolePost(RoleBaseSchema):
    pass


class RolePut(RoleBaseSchema):
    pass


RoleInDB = pydantic_model_creator(Role, name="Role", exclude_readonly=True)
