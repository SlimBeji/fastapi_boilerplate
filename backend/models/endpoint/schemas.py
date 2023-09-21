from typing import List, Optional

from pydantic import BaseModel, constr, validator
from tortoise.contrib.pydantic import pydantic_model_creator

from backend.enums.http import HttpMethod
from backend.enums.regex import Regex
from backend.models import Endpoint
from backend.models.api_item import ApiItemOverview


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
    tags: Optional[List[str]]

    @validator("tags", pre=True)
    def convert_tags(cls, v):
        result = [i.get("text") for i in v if i.get("text")]
        return result


class EndpointSearch(EndpointBaseSchema):
    url: Optional[str]
    label: Optional[str]
    description: Optional[str]
    http_method: Optional[HttpMethod]
    tags: Optional[constr(regex=Regex.TAGS.value)]


class EndpointPost(EndpointBaseSchema):
    tags: Optional[List[str]]


class EndpointPut(EndpointBaseSchema):
    url: Optional[str]
    label: Optional[str]
    description: Optional[str]
    http_method: Optional[HttpMethod]
    tags: Optional[List[str]]


EndpointInDb = pydantic_model_creator(Endpoint, name="EndpointInDB")
