if __name__ == '__main__':
    import uvicorn
    import os

    from src.db.config import app
    from get_env import get_env

    path_to_cert = "C:/cert"

    ssl_keyfile_name = 'privateKey.key'
    ssl_certfile_name = 'certificate.crt'

    ssl_keyfile = os.path.join(path_to_cert, ssl_keyfile_name)
    ssl_certfile = os.path.join(path_to_cert, ssl_certfile_name)

    if ssl_keyfile and ssl_certfile:
        uvicorn.run(app,
                    host=get_env("FASTAPI_HOST"),
                    port=int(get_env("FASTAPI_PORT")),
                    ssl_keyfile=ssl_keyfile,
                    ssl_certfile=ssl_certfile)
    else:
        print('NOT')