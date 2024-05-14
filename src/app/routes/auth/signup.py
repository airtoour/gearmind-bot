from fastapi import APIRouter
from fastapi.responses import HTMLResponse


signup = APIRouter()

@signup.route('/signup', response_class=HTMLResponse)
async def signup():
    ...