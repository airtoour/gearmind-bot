if __name__ == '__main__':
    from src.telegram.bot import dp, bot

    import uvicorn

    from src.db.config import app
    from get_env import get_env

    dp.run_polling(bot)
    #uvicorn.run(app,
    #            host=get_env("FASTAPI_HOST"),
    #            port=int(get_env("FASTAPI_PORT")))
