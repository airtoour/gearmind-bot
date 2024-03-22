if __name__ == '__main__':
    import uvicorn
    from src.db.config import app
    from get_env import get_env

    uvicorn.run(app,
                host=get_env("FASTAPI_HOST"),
                port=int(get_env("FASTAPI_PORT")),
                ssl_keyfile=None,
                ssl_certfile=None)