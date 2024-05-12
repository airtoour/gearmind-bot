from src.db.db_app import app, db
from src.routes.login import login_bp
from src.routes.signup import signup_bp

from config import config

app.register_blueprint(signup_bp, url_prefix='/signup')
app.register_blueprint(login_bp, url_prefix='/login')
# app.register_blueprint(car, url_prefix='/car')

app.debug = True

if __name__ == '__main__':
    import ssl
    from pathlib import Path

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

    cert_dir = Path(str(config.ssl.ssl_path))

    certfile = cert_dir / config.ssl.ssl_cert
    keyfile = cert_dir / config.ssl.ssl_key

    ssl_context.load_cert_chain(certfile=str(certfile), keyfile=str(keyfile))

    with app.app_context():
        db.create_all()

    app.run(host=config.flask.flask_host,
            port=config.flask.flask_port,
            ssl_context=ssl_context)
