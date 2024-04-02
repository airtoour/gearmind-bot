from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from get_env import get_env

app = Flask(__name__)
db = SQLAlchemy()

app.config['SQLALCHEMY_DATABASE_URI'] = (f'postgresql://{get_env("DB_USERNAME")}:{get_env("DB_PASSWORD")}'
                                         f'@{get_env("DB_HOST")}:{get_env("DB_PORT")}/{get_env("DB_NAME")}')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'cringe'

db.init_app(app)