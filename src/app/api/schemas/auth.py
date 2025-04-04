from typing import Optional
from pydantic import BaseModel


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    first_login_time: Optional[float]


class AuthInfo(BaseModel):
    tg_user_id: int
    first_login_time: Optional[float]
    role: str