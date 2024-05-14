from fastapi import FastAPI
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory="routes/templates")


if __name__ == '__main__':
    from config import settings
    from pathlib import Path
    import uvicorn

    from src.app.routes.result_items import result
    from src.app.routes.auth.signup import signup

    app.include_router(signup)  # Регистрация роутера регистрации
    app.include_router(result)  # Регистрация роутера результирующего набора

    cert_dir = Path(settings.SSL_PATH)

    certfile = cert_dir / settings.SSL_CERT_FILE
    keyfile = cert_dir / settings.SSL_KEY_FILE

    uvicorn.run(
        app,
        host=settings.FASTAPI_HOST,
        port=settings.FASTAPI_PORT,
        ssl_certfile=certfile,
        ssl_keyfile=keyfile
    )
