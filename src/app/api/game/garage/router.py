from fastapi import APIRouter


router = APIRouter(prefix="/garage")


@router.get("/status")
async def check_wash_car():
    return {"game": "ok"}
