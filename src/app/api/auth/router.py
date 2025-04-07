from fastapi import (
    APIRouter,
    HTTPException,
    status
)
from jose import jwt

from app.api.schemas.auth import AuthRequest
from app.dependencies import SECRET_KEY, verify_telegram_data


router = APIRouter(prefix="/auth", tags=["Авторизация"])


@router.post("/auth")
async def auth(request: AuthRequest):
    # Проверяем данные
    parsed_data = verify_telegram_data(request.init_data)

    if not parsed_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные данные авторизации"
        )

    # Извлекаем информацию о пользователе
    user_data = parsed_data.get("user", {})
    tg_user_id = user_data.get("id")

    token = jwt.encode(
        {"tg_user_id": tg_user_id},
        SECRET_KEY,
        algorithm="HS256"
    )

    return {"access_token": token, "token_type": "bearer"}
