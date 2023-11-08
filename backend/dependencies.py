import re
from typing import List, Optional

from fastapi import HTTPException, Query, status
from fastapi_pagination import Params

from backend.config import settings
from backend.enums.regex import Regex
from backend.models import ApiItem


class PaginationParams(Params):
    page: int = Query(1, ge=1, description="Page number")
    size: int = Query(
        settings.MAX_ITEM_PER_RESPONSE, ge=1, le=100, description="Page size"
    )


async def comma_joined_tags(tags: Optional[str] = "") -> Optional[List[str]]:
    if tags:
        if re.match(Regex.TAGS.value, tags):
            return [t.strip() for t in tags.split(",")]
        else:
            detail = f"tags input '{tags}' is invalid. Tags must be joined by comma. Example 'football, stats'"
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
            )


async def apiitem_lookup(id) -> ApiItem:
    record = await ApiItem.search(id=id, first=True, prefetch=["tags"])
    if record:
        return record

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
