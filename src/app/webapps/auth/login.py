from src.app.apis.v1.login import login_for_access_token
from fastapi import APIRouter, HTTPException, Request

from src.app.webapps.auth.forms import LoginForm
from src.app.app import templates


login = APIRouter(include_in_schema=False)


@login.get("/login/")
def login_get(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@login.post("/login/")
async def login_user(request: Request):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login Successful :)")
            response = templates.TemplateResponse("auth/login.html", form.__dict__)
            login_for_access_token(response=response, form_data=form)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("auth/login.html", form.__dict__)
    return templates.TemplateResponse("auth/login.html", form.__dict__)