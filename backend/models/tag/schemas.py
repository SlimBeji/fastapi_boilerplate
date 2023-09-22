from typing import List, Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from backend.models.api_item.schemas import ApiItemOverview
from backend.models.endpoint.schemas import EndpointOverview
from backend.models.tag.model import Tag


class TagBaseSchema(BaseModel):
    text: str


class TagOverview(BaseModel):
    id: int
    text: str


class TagGet(TagBaseSchema):
    id: int
    api_items: Optional[List[ApiItemOverview]]
    endpoints: Optional[List[EndpointOverview]]


class TagSearch(TagBaseSchema):
    text: Optional[str]
    api_item_id: Optional[int]
    endpoint_id: Optional[int]


class TagPost(TagBaseSchema):
    pass


class TagPut(TagBaseSchema):
    pass


TagInDB = pydantic_model_creator(Tag, name="Tag", exclude_readonly=True)
