from src.db.config import app, db
from src.routes.login import login_bp
from src.routes.signup import signup_bp
from get_env import get_env

app.register_blueprint(signup_bp, url_prefix='/signup')
app.register_blueprint(login_bp, url_prefix='/login')

app.debug = True

if __name__ == '__main__':
    import ssl
    from pathlib import Path

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

    cert_dir = Path('C:/cert')

    certfile = cert_dir / 'certificate.crt'
    keyfile = cert_dir / 'privateKey.key'

    ssl_context.load_cert_chain(certfile=str(certfile), keyfile=str(keyfile))

    with app.app_context():
        db.create_all()
    app.run(host=str(get_env("FLASK_HOST")),
            port=get_env("FLASK_PORT"),
            ssl_context=ssl_context)
