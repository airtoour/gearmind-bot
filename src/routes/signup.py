from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from aiogram.types import Message

from pathlib import Path
from src.models import Users, Cities, Cars


DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(DIR, 'templates')))

signup = APIRouter(prefix="/signup")

@signup.get("/{user_id}", name='signup', response_class=HTMLResponse)
async def show_signup_form(user_id: int):
    return templates.TemplateResponse("signup.html", {
        "request": {
            "user_id": user_id
        }
    })


@signup.get("/{user_id}", name='signup', response_class=HTMLResponse)
async def register_user(request: Request, user_id: int,):
    try:
        first_name = request.query_params.get("first_name")
        phone_number = request.query_params.get("first_name")
        user_email = request.query_params.get("user_email")
        user_password = request.query_params.get("user_password")

        new_user = await Users.create(first_name=first_name,
                                      phone_number=phone_number,
                                      user_email=user_email)
        new_user.set_password(user_password)
        message = 'Пользователь успешно зарегистрирован!'
        return templates.TemplateResponse("signup_result.html", {
            "request": {
                "user_id": user_id
            },
            "message": message,
            "new_user": new_user
        })
    except Exception as e:
        message = f'Произошла ошибка: {e}'
        return templates.TemplateResponse("signup_result.html", {
            "request": request,
            "message": message
        })
