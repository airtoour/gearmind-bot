import hmac
import urllib
from typing import Optional

from jose import jwt, JWTError
from datetime import datetime, timedelta
from hashlib import sha256
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import GameProgressUsersRepository, UsersRepository
from db.models.users.schemas import UsersRoles

from config import settings
from logger import logger


SECRET_KEY = sha256(settings.TOKEN.encode()).digest()
security = HTTPBearer()


def verify_telegram_data(init_data: str) -> Optional[dict]:
    """
    Проверяет подлинность данных из Telegram WebApp.
    Возвращает распарсенные данные, если проверка успешна.
    """
    try:
        # Разбиваем данные на параметры
        parsed_data = urllib.parse.parse_qs(init_data)

        # Извлекаем хэш и удаляем его из данных
        received_hash = parsed_data.pop('hash', [None])[0]
        if not received_hash:
            return None

        # Сортируем параметры и формируем строку для проверки
        data_check_string = "\n".join(
            f"{key}={value[0]}"
            for key, value in sorted(parsed_data.keys())
        )

        # Создаем HMAC-SHA256 хэш
        computed_hash = hmac.new(
            SECRET_KEY,
            msg=data_check_string.encode(),
            digestmod=sha256
        ).hexdigest()

        # Сравниваем хэши
        if computed_hash == received_hash:
            return parsed_data

        return None
    except Exception as e:
        print(f"Ошибка проверки: {e}")
        return None


async def get_current_user(token: str = Depends(security)) -> dict:
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])
        return {"user_id": payload["user_id"]}
    except JWTError:
        raise HTTPException(401, detail="Неверный токен")
