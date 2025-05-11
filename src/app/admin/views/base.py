from fastapi.params import Depends
from sqladmin import BaseView, expose
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from db.db_config import get_session_app
from db.models.users.repository import UsersRepository


class AdminBaseView(BaseView):
    # todo Сделать на главной странице график эффективности ответов
    #  Как придумать график эффективности? Исходя из оценок?

    name = "Главная страница"
    icon = "fa-solid fa-chart-line"

    @expose("/", methods=["GET"])
    async def base_view(self, request: Request, session: AsyncSession = Depends(get_session_app)):
        users = await UsersRepository.find_all(session)
        return {"request": request, "users": users}
