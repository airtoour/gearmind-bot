import hmac
import hashlib

from typing import Optional
from urllib.parse import parse_qsl

from jose import jwt, JWTError
from hashlib import sha256

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_config import get_session_app
from db.models import UsersRepository

from config import settings
from logger import logger


SECRET_KEY = sha256(settings.TOKEN.encode()).digest()
SECURITY = HTTPBearer()


def verify_telegram_data(init_data: str) -> Optional[dict]:
    """
    Проверяет подлинность данных из Telegram WebApp.
    Возвращает распарсенные данные, если проверка успешна.
    """
    try:
        # Парсим данные
        parsed_data = dict(parse_qsl(init_data))

        # Получаем хеш из данных
        received_hash = parsed_data.pop("hash")

        # Генерируем секретный ключ
        secret_key = hashlib.sha256(settings.BOT_TOKEN.encode()).digest()

        # Создаем строку для проверки
        data_check = "\n".join(
            [f"{k}={v}" for k, v in sorted(parsed_data.items())]
        )

        # Вычисляем хеш
        computed_hash = hmac.new(
            secret_key,
            data_check.encode(),
            hashlib.sha256
        ).hexdigest()

        return parsed_data if computed_hash == received_hash else None

    except Exception as e:
        logger.error(e)
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(SECURITY),
    session: AsyncSession = Depends(get_session_app)
):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        tg_user_id = payload.get("tg_user_id")

        user = await UsersRepository.find_one_or_none(session, tg_user_id=tg_user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        logger.debug(token)
        logger.debug(payload)
        logger.debug(tg_user_id)
        logger.debug(user)

        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")