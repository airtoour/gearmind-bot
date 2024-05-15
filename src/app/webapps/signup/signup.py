from fastapi import APIRouter, Request, responses, status
from sqlalchemy.exc import IntegrityError

from src.db.schemas.users import UserCreate
from src.db.repository.users import create

from src.app.webapps.signup.forms import UserCreateForm
from src.app.app import templates

signup = APIRouter(include_in_schema=False)


@signup.get("/signup/")
def register(request: Request):
    return templates.TemplateResponse("auth/signup.html", {"request": request})


@signup.post("/signup/")
async def register(request: Request):
    form = UserCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        user = UserCreate(
            username=form.username, email=form.email, password=form.password
        )
        try:
            user = create(user=user)
            return responses.RedirectResponse(
                "/?msg=Successfully-Registered", status_code=status.HTTP_302_FOUND
            )
        except IntegrityError:
            form.__dict__.get("errors").append("Duplicate username or email")
            return templates.TemplateResponse("auth/signup.html", form.__dict__)
    return templates.TemplateResponse("auth/signup.html", form.__dict__)