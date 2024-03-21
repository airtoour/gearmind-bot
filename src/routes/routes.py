from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from src.exceptions import server_exceptions

app = FastAPI()

DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(DIR, 'templates')))


@app.get('/signup', name='signup', response_class=HTMLResponse)
async def index(request: Request, user_id: int):
    try:
        return templates.TemplateResponse('index.html', {
            "request": {
                "user_id": user_id
            }
            ,
        })
    except Exception as e:
        server_exceptions(status_code=422, detail=e)