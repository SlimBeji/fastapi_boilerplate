from enum import Enum


class Regex(Enum):
    TAGS = r"^\w*(,\w*)*$"
