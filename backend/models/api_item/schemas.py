from typing import List, Optional

from pydantic import BaseModel, validator
from tortoise.contrib.pydantic import pydantic_model_creator

from backend.models.api_item.model import ApiItem
from backend.utils.validators import domain_validation


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
    tags: List[str] = []

    @validator("tags", pre=True)
    def convert_tags(cls, v):
        result = [i.text for i in v if i.text]
        return result


class ApiItemSearch(ApiItemBaseSchema):
    label: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None


class ApiItemPost(ApiItemBaseSchema):
    tags: Optional[List[str]] = []

    @validator("url")
    def validate_url(cls, v):
        return domain_validation(v)

    @validator("tags")
    def strip_tags(cls, v):
        if v:
            return [t.strip() for t in v]


class ApiItemPut(ApiItemPost):
    label: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    tags: Optional[List[str]] = []


ApiItemInDB = pydantic_model_creator(ApiItem, name="ApiInDB")
