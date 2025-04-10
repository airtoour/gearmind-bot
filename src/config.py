from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    TOKEN: str
    BOT_ID: int

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int

    YANDEX_TOKEN: str
    YANDEX_CATALOG: str
    YANDEX_MODEL: str

    CARS_URL: str
    GEAR_URL: str
    ADMIN_URL: str

    model_config = ConfigDict(from_attributes=True)

    @property
    def DATABASE_URL(self):
        """Возвращает ссылку на подключение к БД"""
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def REDIS_URL(self):
        """Возвращает ссылку на подключение к Redis"""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    def get_webhook_url(self) -> str:
        """Возвращает ссылку на endpoint Webhook`ов"""
        return f"{self.GEAR_URL}/webhook"


settings = Settings()  # type: ignore
