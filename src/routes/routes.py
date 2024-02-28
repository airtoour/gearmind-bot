from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pathlib import Path

app = FastAPI()

DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(DIR, 'templates')))


@app.get('/', response_class=HTMLResponse)
async def index(request: Request, user_id: int):
    return templates.TemplateResponse('index.html', {
        "request": {
            "user_id": user_id
        },
    })