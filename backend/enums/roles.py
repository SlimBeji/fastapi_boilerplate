from enum import Enum


class SuperUser(str, Enum):
    NAME = "superuser"
    LEVEL = 0
    DESCRIPTION = "Can do everything"
