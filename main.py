if __name__ == '__main__':
    import asyncio
    import uvicorn

    from src.telegram.bot import dp
    from src.routes.routes import app
    from get_env import get_env

    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling())
    uvicorn.run(app,
                host=f'{get_env("FASTAPI_HOST")}',
                port=int(get_env("FASTAPI_PORT")))
