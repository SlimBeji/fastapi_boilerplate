from typing import List, Optional

from pydantic import BaseModel, constr, validator
from tortoise.contrib.pydantic import pydantic_model_creator

from backend.enums.regex import Regex
from backend.models.api_item.model import ApiItem


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
    label: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    tags: Optional[constr(pattern=Regex.TAGS.value)] = None


class ApiItemPost(ApiItemBaseSchema):
    tags: Optional[List[str]] = None


class ApiItemPut(ApiItemBaseSchema):
    label: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str]  = None
    tags: Optional[List[str]] = None


ApiItemInDB = pydantic_model_creator(ApiItem, name="ApiInDB")
