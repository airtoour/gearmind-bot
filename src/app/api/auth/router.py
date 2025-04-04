from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.auth import AuthResponse, AuthInfo
from app.dependencies import create_access_token, decode_access_token
from db.db_config import get_session_app

from logger import logger


router = APIRouter(prefix="/auth", tags=["Авторизация"])


@router.post("/login", response_model=AuthResponse)
async def login(tg_user_id: int, session: AsyncSession = Depends(get_session_app)):
    try:
        access_data = await create_access_token(tg_user_id, session)
        return {
            "access_token": access_data["access_token"],
            "token_type": "bearer",
            "first_login_time": access_data["first_login_time"]
        }
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/me", response_model=AuthInfo)
async def get_current_user(token_data: dict = Depends(decode_access_token)):
    return token_data
