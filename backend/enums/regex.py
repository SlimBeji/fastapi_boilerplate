from enum import Enum


class Regex(Enum):
    TAGS = r"^\w*(,\s*\w*)*$"
