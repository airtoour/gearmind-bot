from pydantic import BaseModel


class NewLevelReturnSchema(BaseModel):
    level: int
    experience: int
    upped: bool
