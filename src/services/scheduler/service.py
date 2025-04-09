import asyncio
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from services.scheduler.tasks import reset_daily_tasks_task

from logger import logger


async def start_scheduler():
    """Планировщик заданий для автоматизации процессов"""
    scheduler = AsyncIOScheduler()

    try:
        scheduler.add_job(
            func=reset_daily_tasks_task,
            trigger=CronTrigger(hour=0, minute=0),
            id="reset_daily_tasks_task",
            name="Сброс ежедневных заданий",
            replace_existing=True
        )

        scheduler.start()
        logger.info(f"Планировщик запущен в {datetime.now()}")

        while True:
            await asyncio.sleep(10)
    except Exception as e:
        logger.error(f"Ошибка в запуске планировщика:\n{e}")
        logger.info("Попытка перезапуска планировщика через 5 секунд...")

        await asyncio.sleep(5)
        await start_scheduler()
    finally:
        logger.info("Остановка планировщика...")
        await scheduler.shutdown()


if __name__ == "__main__":
    async def main():
        try:
            logger.info("Запуск планировщика...")
            await start_scheduler()
        except KeyboardInterrupt:
            logger.info("Остановка вручную..")

    asyncio.run(main())
