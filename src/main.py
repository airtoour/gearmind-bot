import asyncio

from telegram.bot import bot, dp
from telegram.filters.menu import set_main_menu

from telegram.handlers import routers_list

from loguru import logger


async def main():
    """Запуск Бота"""
    logger.info("Запуск..")

    await set_main_menu(bot)
    logger.info("Определили команды..")

    dp.include_routers(*routers_list)
    logger.info("Добавили роутеры")

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logger.info("Запуск бота..")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.critical("Exiting bot...")
    finally:
        logger.info("Done")
