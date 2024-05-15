from fastapi import FastAPI
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory="webapps/templates")


if __name__ == '__main__':
    from config import settings
    from pathlib import Path
    import uvicorn

    from src.app.webapps.signup.signup import signup
    from src.app.webapps.auth.login import login
    from src.app.webapps.result_items import result

    app.include_router(signup)  # Регистрация роутера регистрации
    app.include_router(login)   # Регистрация роутера входа пользователя

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
