from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from backend.enums.http import ParamLocation, TypeParam
from backend.models.endpoint.schemas import EndpointOverview
from backend.models.query_param.model import QueryParam


class QueryParamBaseSchema(BaseModel):
    label: str
    type: TypeParam
    description: str
    default: Optional[str]
    required: bool
    location: ParamLocation


class QueryParamOverview(BaseModel):
    id: int
    label: str
    location: ParamLocation
    required: bool


class QueryParamGet(QueryParamBaseSchema):
    id: int
    endpoint: EndpointOverview


class QueryParamSearch(QueryParamBaseSchema):
    label: Optional[str]
    type: Optional[TypeParam]
    description: Optional[str]
    default: Optional[str]
    required: Optional[bool]
    location: Optional[ParamLocation]


class QueryParamPost(QueryParamBaseSchema):
    pass


class QueryParamPut(QueryParamBaseSchema):
    label: Optional[str]
    type: Optional[TypeParam]
    description: Optional[str]
    default: Optional[str]
    required: Optional[bool]
    location: Optional[ParamLocation]


QueryParamInDB = pydantic_model_creator(QueryParam, name="QueryParmInDB")
