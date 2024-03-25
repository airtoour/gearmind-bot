from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from aiogram.types import Message as message

from pathlib import Path
from src.models import Users


DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(DIR, 'templates')))

signup = APIRouter(prefix="/signup")


@signup.get("/", name='signup', response_class=HTMLResponse)
async def show_signup_form():
    return templates.TemplateResponse("signup.html", {
        "request": {}
    })


@signup.post("/", name='register_user', response_class=HTMLResponse)
async def register_user_post(request: Request,
                             first_name: str = Form(...),
                             phone_number: int = Form(...),
                             user_email: str = Form(...),
                             user_password: str = Form(...)):
    try:
        new_user = await Users.create(
            first_name=first_name,
            phone_number=phone_number,
            user_email=user_email,
            user_password=user_password
        )
        print(new_user.__dict__)
        result_message = 'Пользователь успешно зарегистрирован!'
        return templates.TemplateResponse("signup_result.html", {
            "request": request,
            "result_message": result_message
        })
    except Exception as e:
        result_message = f'Произошла ошибка: {e}'
        return templates.TemplateResponse("signup_result.html", {
            "request": request,
            "result_message": result_message
        })
