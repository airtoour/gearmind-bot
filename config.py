from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TOKEN: str

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    CARS_URL: str

    class Config:
        env_file = 'C:/Users/Артур/Desktop/diplom-diplomych/backend/.env'


settings = Settings()
