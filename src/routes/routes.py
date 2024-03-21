from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from src.exceptions import server_exceptions
from src.db.config import session
from src.models import Users, Cities, Cars

app = FastAPI()

DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(DIR, 'templates')))


@app.route('/signup', methods=['GET', 'POST'], name='signup', response_class=HTMLResponse)
async def index(request: Request, user_id: int):
    from aiogram.types import Message as message
    try:
        user = session.query(Users).filter_by(tg_user_id=user_id)

        if not user:
            new_user = Users.create(tg_user_id=user_id,
                                    tg_username=message.from_user.username,
                                    first_name=first_name,
                                    last_name=last_name,
                                    phone_number=phone_number,
                                    city_id=session.query(Cities.city_id).filter_by(Cities.city_name).first(),
                                    car_id=session.query(Cars.car_id).filter_by(Cars.car_name).first())
            session.add(new_user)
            session.commit()
        else:

        return templates.TemplateResponse('index.html', {
            "request": {
                "user_id": user_id
            }
            ,
        })
    except Exception as e:
        server_exceptions(status_code=422, detail=e)