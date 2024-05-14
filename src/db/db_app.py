from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import settings

app = Flask(__name__)
db = SQLAlchemy()

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{settings.DB_NAME}.db'

app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'cringe'

app.config['SERVER_NAME'] = f'{settings.FASTAPI_HOST}:{settings.FASTAPI_PORT}'
app.config['APPLICATION_ROOT'] = '/'
app.config['PREFERRED_URL_SCHEME'] = 'https'

db.init_app(app)