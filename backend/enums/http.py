from enum import Enum


class HttpMethod(str, Enum):
    GET = "get"
    POST = "post"
    patch = "patch"
    put = "push"


class ParamLocation(str, Enum):
    HEADER = "header"
    PATH = "path"
    QUERY = "query"
    Body = "body"


class TypeParam(str, Enum):
    INTEGER = "integer"
    STRING = "string"
    FLOAT = "float"
