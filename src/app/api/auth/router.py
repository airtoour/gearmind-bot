from fastapi import (
    APIRouter,
    HTTPException, Depends
)
from jose import jwt

from app.api.schemas.auth import AuthRequest
from app.dependencies import SECRET_KEY, verify_telegram_data, get_current_user

router = APIRouter(prefix="/auth", tags=["Авторизация"])


@router.post("/auth")
async def auth(request: AuthRequest):
    # Проверяем данные
    parsed_data = verify_telegram_data(request.init_data)
    if not parsed_data:
        raise HTTPException(401, detail="Неверные данные авторизации")

    # Извлекаем информацию о пользователе
    user_data = parsed_data.get("user", [{}])[0]
    user_id = user_data.get("id")

    # Создаем JWT-токен
    token = jwt.encode(
        {"user_id": user_id},
        SECRET_KEY,
        algorithm="HS256"
    )

    return {"access_token": token, "token_type": "bearer"}


@router.get("/protected")
async def protected_route(user: dict = Depends(get_current_user)):
    return {"message": f"Доступ разрешен для пользователя {user['user_id']}"}
