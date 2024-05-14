from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse


signup = APIRouter()

@signup.route('/signup', response_class=HTMLResponse)
async def signup(request: Request):
    ...