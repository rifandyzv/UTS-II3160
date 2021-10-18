from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class LoginSchema(BaseModel):
    username: str
    password: str


class MenuItem(BaseModel):
    name: str
