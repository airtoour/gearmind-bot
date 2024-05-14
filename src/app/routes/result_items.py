from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse

from src.app.app import templates

result = APIRouter()

@result.get('/items', response_class=HTMLResponse)
async def get_result(request: Request):
    items = [{'name': 'Товар 1', 'description': 'Описание 1', 'price': 100},
             {'name': 'Товар 2', 'description': 'Описание 2', 'price': 200},
             {'name': 'Товар 3', 'description': 'Описание 3', 'price': 300}]
    return templates.TemplateResponse("items.html", {"request": request, "items": items})