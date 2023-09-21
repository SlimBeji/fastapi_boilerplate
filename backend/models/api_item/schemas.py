from typing import List, Optional

from pydantic import BaseModel, constr, validator
from tortoise.contrib.pydantic import pydantic_model_creator

from backend.enums.regex import Regex
from backend.models import ApiItem


class ApiItemBaseSchema(BaseModel):
    label: str
    description: str
    url: str


class ApiItemOverview(BaseModel):
    id: int
    url: str
    label: str


class ApiItemGet(ApiItemBaseSchema):
    id: int
    tags: Optional[List[str]]

    @validator("tags", pre=True)
    def convert_tags(cls, v):
        result = [i.get("text") for i in v if i.get("text")]
        return result


class ApiItemSearch(ApiItemBaseSchema):
    label: Optional[str]
    description: Optional[str]
    url: Optional[str]
    tags: Optional[constr(regex=Regex.TAGS.value)]


class ApiItemPost(ApiItemBaseSchema):
    tags: Optional[List[str]]


class ApiItemPut(ApiItemBaseSchema):
    label: Optional[str]
    description: Optional[str]
    url: Optional[str]
    tags: Optional[List[str]]


ApiItemInDB = pydantic_model_creator(ApiItem, name="ApiInDB")
