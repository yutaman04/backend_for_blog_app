import strawberry
from enum import IntEnum


@strawberry.enum
class ArticleTypeEnum(IntEnum):
    NORMAL = 1
    FIXED = 2
