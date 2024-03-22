from fastapi import Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from src.db.config import app
from src.models import Users, Cities, Cars


DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(DIR, 'templates')))


@app.get("/signup/", response_class=HTMLResponse)
async def show_signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup/", response_class=HTMLResponse)
async def register_user(request: Request, user_data: Users.SignUp):
    try:
        new_user = await Users.create(**user_data.model_dump())
        message = 'Пользователь успешно зарегистрирован!'
        return templates.TemplateResponse("signup_result.html", {
            "request": request,
            "message": message,
            "new_user": new_user
        })
    except Exception as e:
        message = f'Произошла ошибка: {e}'
        return templates.TemplateResponse("signup_result.html", {
            "request": request,
            "message": message
        })
