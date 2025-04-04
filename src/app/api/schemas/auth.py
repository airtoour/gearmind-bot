from pydantic import BaseModel


class AuthRequest(BaseModel):
    init_data: str
