from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_config import get_session_app
from db.models import TasksRepository

from .schemas import TaskInfo


router = APIRouter(prefix="/sprav")


@router.get("/all")
async def get_full_sprav(session: AsyncSession = Depends(get_session_app)):
    """Запрос всего справочника заданий"""
    sprav = await TasksRepository.find_all(session, is_active=True)
    return sprav


@router.post("/create")
async def create_task(data: TaskInfo, session: AsyncSession = Depends(get_session_app)):
    """Запрос создания задания в справочнике"""
    add_task = await TasksRepository.add(session, **data.model_dump(mode="json"))
    return add_task
