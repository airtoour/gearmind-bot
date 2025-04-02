from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from logger import logger

router = APIRouter(prefix="/api")


@router.get("")
async def base():
    try:
        return {"status": "ok"}
    except HTTPException as e:
        logger.error(e)
        return {"error": str(e)}
