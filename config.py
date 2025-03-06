<<<<<<< HEAD:config.py
from typing import Literal

=======
<<<<<<< HEAD:src/config.py
=======
from typing import Literal

>>>>>>> dev:config.py
>>>>>>> 617c386 (Merge branch 'dev'):src/config.py
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

<<<<<<< HEAD:config.py
=======
<<<<<<< HEAD:src/config.py
    class Config:
        env_file = "D:/my-project/diplom-diplomych/.env"
=======
>>>>>>> 617c386 (Merge branch 'dev'):src/config.py
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    model_config = ConfigDict(from_attributes=True)
<<<<<<< HEAD:config.py
=======
>>>>>>> dev:config.py
>>>>>>> 617c386 (Merge branch 'dev'):src/config.py


settings = Settings()
