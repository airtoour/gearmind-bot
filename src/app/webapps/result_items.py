import ast

from fastapi import Request, APIRouter, Query
from fastapi.responses import HTMLResponse
from typing import List
from src.app.app import templates

result = APIRouter()

@result.get("/items/", response_class=HTMLResponse)
async def get_result(request: Request, query_params: list[str] = Query(...)):
    items_list = ast.literal_eval(query_params)
    items = [{"name": param} for param in items_list]
    return templates.TemplateResponse("items.html", {"request": request, "items": items})