from pydantic import BaseModel

class CarCreate(BaseModel):
    brand: str
    model: str
    gen: str
    year: int

class CarShow(BaseModel):
    brand: str
    model: str
    gen: str
    year: int

    class Config:
        orm_mode = True