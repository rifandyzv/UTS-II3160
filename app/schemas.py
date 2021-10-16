from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    full_name: Optional[str] = None
    password: str


class LoginSchema(BaseModel):
    username: str
    password: str


class MenuItem(BaseModel):
    name: str
