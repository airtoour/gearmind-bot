import asyncio

from telegram.bot import bot, dp
from telegram.handlers import routers_list

from loguru import logger


async def main():
    """Запуск Бота"""
    logger.info("Запуск..")

    dp.include_routers(*routers_list)
    logger.info("Добавили роутеры")

    logger.info("ГОУ")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.critical("Exiting bot...")
    finally:
        logger.info("Done")
