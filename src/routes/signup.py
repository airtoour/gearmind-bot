from fastapi import Request, APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from aiogram.types import Message

from pathlib import Path
from src.models import Users


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


@signup.post("/{user_id}", name='register_user_post', response_class=HTMLResponse)
async def register_user_post(request: Request,
                             user_id: int,
                             first_name: str = Form(...),
                             phone_number: str = Form(...),
                             user_email: str = Form(...),
                             user_password: str = Form(...),
                             session,
                             city_id: int | None,
                             car_id: int | None,
                             card_id: int | None,
                             is_vip: str | None,
                             message: Message | None):
    try:
        new_user = await Users.create(session=session,
                                      first_name=first_name,
                                      phone_number=phone_number,
                                      user_email=user_email,
                                      user_password=user_password,
                                      city_id=city_id,
                                      car_id=car_id,
                                      card_id=card_id,
                                      is_vip=is_vip,
                                      message=message)
        message = 'Пользователь успешно зарегистрирован!'
        return templates.TemplateResponse("signup.html", {
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
