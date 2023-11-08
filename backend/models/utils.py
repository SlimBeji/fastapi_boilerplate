from typing import Dict, List

from fastapi_pagination import Page
from fastapi_pagination.ext.tortoise import (
    _generate_query,
    create_page,
    generic_query_apply_params,
    paginate,
    verify_params,
)
from tortoise.functions import Count
from tortoise.models import Model

from backend.dependencies import PaginationParams


async def filter_on_tags(
    m: Model, filters: Dict, tags: List[str], params: PaginationParams
) -> Page:
    base_query = m.filter(**filters).order_by("id").prefetch_related("tags")
    if tags:
        params, raw_params = verify_params(params, "limit-offset")
        base_query = (
            base_query.filter(tags__text__in=tags)
            .annotate(count=Count("id"))
            .filter(count=len(tags))
        )
        total_count = len(await base_query.values("count"))
        items = await generic_query_apply_params(
            _generate_query(base_query, False), raw_params
        ).all()
        result = create_page(items, total_count, params)

    else:
        result = await paginate(base_query, params)

    return result
