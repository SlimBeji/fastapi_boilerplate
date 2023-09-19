from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from backend.config import templates

index_view_router = APIRouter(prefix="")


@index_view_router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("pages/index.j2", dict(request=request))
