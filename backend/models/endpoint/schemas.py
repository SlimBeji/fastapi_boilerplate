from typing import List, Optional

from pydantic import BaseModel, field_validator
from tortoise.contrib.pydantic import pydantic_model_creator

from backend.enums.http import HttpMethod
from backend.models.api_item.schemas import ApiItemOverview
from backend.models.endpoint.model import Endpoint


class EndpointBaseSchema(BaseModel):
    url: str
    label: str
    description: str
    http_method: HttpMethod


class EndpointOverview(BaseModel):
    id: int
    url: str
    label: str


class EndpointGet(EndpointBaseSchema):
    id: int
    api_item: ApiItemOverview
    tags: List[str] = []

    @field_validator("tags", mode="before")
    def convert_tags(cls, v):
        result = [i.text for i in v if i.text]
        return result


class EndpointSearch(EndpointBaseSchema):
    url: Optional[str] = None
    label: Optional[str] = None
    description: Optional[str] = None
    http_method: Optional[HttpMethod] = None


class EndpointPost(EndpointBaseSchema):
    tags: Optional[List[str]] = []


class EndpointPut(EndpointBaseSchema):
    url: Optional[str] = None
    label: Optional[str] = None
    description: Optional[str] = None
    http_method: Optional[HttpMethod] = None
    tags: Optional[List[str]] = []


EndpointInDb = pydantic_model_creator(Endpoint, name="EndpointInDB")
