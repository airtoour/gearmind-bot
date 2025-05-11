from db.db_config import async_session_maker
from db.models.users_tasks.repository import UsersTasksRepository

from logger import logger


async def reset_daily_tasks_task():
    """Задача на сброс ежедневных заданий"""
    try:
        async with async_session_maker() as session:
            dropped = await UsersTasksRepository.reset_daily(session)
            logger.info(f"[Scheduler] Ежедневных заданий обновлено: {len(dropped) if dropped else 0}")
    except Exception as e:
        logger.error(f"Ошибка при выполнении таски на сброс дэйли-заданий: {e}")
