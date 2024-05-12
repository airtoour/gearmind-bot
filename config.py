from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    db_username: str
    db_password: str
    db_host:     str
    db_port:     int
    db_name:     str

@dataclass
class TgBot:
    token: str

@dataclass
class FlaskConfig:
    flask_host: str
    flask_port: int

@dataclass
class SSLCert:
    ssl_path: str
    ssl_cert: str
    ssl_key:  str

@dataclass
class Images:
    path: str

@dataclass
class CarUrl:
    path: str

@dataclass
class Config:
    tg_bot:  TgBot
    db:      DatabaseConfig
    flask:   FlaskConfig
    ssl:     SSLCert
    images:  Images
    car_url: CarUrl


env: Env = Env()
env.read_env()

config = Config(
    tg_bot = TgBot(
        token = env('TOKEN')
    ),
    db = DatabaseConfig(
        db_username = env('DB_NAME'),
        db_password = env('DB_PASSWORD'),
        db_host     = env('DB_HOST'),
        db_port     = env('DB_PORT'),
        db_name     = env('DB_NAME')
    ),
    flask = FlaskConfig(
        flask_host = env('FLASK_HOST'),
        flask_port = env('FLASK_PORT')
    ),
    ssl = SSLCert(
        ssl_path = env('SSL_PATH'),
        ssl_cert = env('SSL_CERT_FILE'),
        ssl_key  = env('SSL_KEY_FILE')
    ),
    images = Images(
        path = env('IMAGE_PATH')
    ),
    car_url = CarUrl(
        path = env('CARS_URL')
    )
)