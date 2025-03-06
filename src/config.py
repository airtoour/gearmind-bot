<<<<<<< HEAD:src/config.py
=======
from typing import Literal

>>>>>>> dev:config.py
from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    TOKEN: str

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    CARS_URL: str

<<<<<<< HEAD:src/config.py
    class Config:
        env_file = "D:/my-project/diplom-diplomych/.env"
=======
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    model_config = ConfigDict(from_attributes=True)
>>>>>>> dev:config.py


settings = Settings()
