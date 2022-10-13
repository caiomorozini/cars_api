from typing import Optional
from pydantic import BaseModel
from pydantic.networks import EmailStr
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class NewUser(BaseModel):
    email: EmailStr
    password: str


class ResponseNewUser(BaseModel):
    id: str
    email: EmailStr
    created_at = datetime.now()
    class Config:
        orm_mode = True
