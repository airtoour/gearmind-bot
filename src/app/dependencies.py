from jose import jwt
from datetime import datetime, timedelta

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import GameProgressUsersRepository, UsersRepository
from db.models.users.schemas import UsersRoles

from config import settings
from logger import logger


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def authenticate_user(tg_user_id: int, session: AsyncSession):
    user = await UsersRepository.find_one_or_none(session, tg_user_id=tg_user_id)

    if not user:
        return None
    if user.role == UsersRoles.BOT:
        raise ValueError("Bot access forbidden")
    return user


def create_jwt_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def create_access_token(tg_user_id: int, session: AsyncSession) -> dict:
    try:
        user = await authenticate_user(tg_user_id, session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        progress = await GameProgressUsersRepository.get_user(session, tg_user_id)
        new_progress = None

        if not progress:
            new_progress = await GameProgressUsersRepository.add_progress(
                session, tg_id=tg_user_id, first_login_time=datetime.now()
            )
        elif not progress.first_login_time:
            new_progress = await GameProgressUsersRepository.update(
                session,
                GameProgressUsersRepository.model.user_id == user.id,
                first_login_time=datetime.now(),
            )

        first_login_time = progress.first_login_time if progress else new_progress.first_login_time
        first_login_timestamp = int(first_login_time.timestamp()) if first_login_time else None

        payload = {
            "sub": str(tg_user_id),
            "tg_id": tg_user_id,
            "first_login": first_login_timestamp,
            "role": user.role.value
        }

        return {
            "access_token": create_jwt_token(payload),
            "first_login_time": first_login_timestamp
        }

    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Token creation error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


def decode_access_token(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return {
        "tg_user_id": int(payload.get("tg_id")),
        "first_login_time": payload.get("first_login"),
        "role": payload.get("role")
    }
