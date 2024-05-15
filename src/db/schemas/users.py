from fastapi import Form
from pydantic import BaseModel


class UserCreateForm:
    def __init__(self,
                 first_name: str = Form(...),
                 phone_number: str = Form(...),
                 city_name: str = Form(...),
                 password: str = Form(...)):
        self.first_name = first_name
        self.phone_number = phone_number
        self.city_name = city_name
        self.password = password


class UserCreate(BaseModel):
    first_name: str
    phone_number: str
    city_name: str
    password: str


class ShowUser(BaseModel):
    username:  str
    phone_number: str
    city_name: str

    class Config:
        orm_mode = True