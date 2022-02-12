from typing import Optional

from pydantic import Field
from tortoise.contrib.pydantic import pydantic_model_creator

from postman.models import (
    ApiItem,
    Endpoint,
    HttpMethod,
    ParamLocation,
    QueryParam,
    Tag,
)

from .tools import fix_enum_validation, wrap_schema_class

# ============Tag related classes=============

TagPydanticBase = pydantic_model_creator(Tag, name="Tag", exclude_readonly=True)

# ============Api related classess=============

ApiItemPydanticBase = pydantic_model_creator(
    ApiItem, name="Api", exclude_readonly=True
)


@wrap_schema_class("ApiGet")
class ApiItemPydanticGet(ApiItemPydanticBase):
    id: int
    tags: list[TagPydanticBase]


@wrap_schema_class("ApiPost")
class ApiItemPydanticPost(ApiItemPydanticBase):
    pass


@wrap_schema_class("ApiPut")
class ApiItemPydanticPut(ApiItemPydanticBase):
    label: Optional[str]
    description: Optional[str]
    url: Optional[str]


# ============Endpoint related classess=============

EndpointPydanticBase = pydantic_model_creator(
    Endpoint, name="Endpoint", exclude_readonly=True, exclude=["api_item_id"]
)


@wrap_schema_class("EndpointGet")
class EndpointPydanticGet(EndpointPydanticBase):
    id: int
    api_item_id: int
    tags: list[TagPydanticBase]


@wrap_schema_class("EndpointPost")
@fix_enum_validation(HttpMethod, "http_method")
class EndpointPydanticPost(EndpointPydanticBase):
    tags: Optional[str] = Field(..., regex=r"^\w*(,\w*)*$")


@wrap_schema_class("EndpointPut")
@fix_enum_validation(HttpMethod, "http_method")
class EndpointPydanticPut(EndpointPydanticBase):
    label: Optional[str]
    description: Optional[str]
    url: Optional[str]
    http_method: Optional[HttpMethod]


# ============QueryParams related classess=============

QueryParamPydanticBase = pydantic_model_creator(
    QueryParam, name="Parameter", exclude_readonly=True, exclude=["endpoint_id"]
)


@wrap_schema_class("ParameterGet")
class QueryParamPydanticGet(QueryParamPydanticBase):
    id: int
    endpoint_id: int


@wrap_schema_class("ParameterPost")
@fix_enum_validation(ParamLocation, "location")
class QueryParamPydanticPost(QueryParamPydanticBase):
    pass


@wrap_schema_class("ParameterPut")
@fix_enum_validation(ParamLocation, "location")
class QueryParamPydanticPut(QueryParamPydanticBase):
    label: Optional[str]
    type: Optional[str]
    default: Optional[str]
    location: Optional[ParamLocation]
    description: Optional[str]
