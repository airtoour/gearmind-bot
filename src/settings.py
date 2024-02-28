from pydantic import BaseConfig


class Settings(BaseConfig):
    TOKEN: str

    DB_HOST: str
    DB_PORT: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str

    FASTAPI_HOST: str
    FASTAPI_PORT: int


settings = Settings()