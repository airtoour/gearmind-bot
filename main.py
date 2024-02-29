if __name__ == '__main__':
    import asyncio
    import uvicorn

    from src.telegram.bot import dp
    from src.routes.routes import app

    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling())
    uvicorn.run(app, host='127.0.0.1', port=8000)
