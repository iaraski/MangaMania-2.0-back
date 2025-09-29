from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    avatar_url:Optional[str] = None
    avatar_public_id: Optional[str] = None
    class Config:
        from_attributes = True


class   Token(BaseModel):
    token: str
    user: UserOut

class TokenData(BaseModel):
    username: Optional[str] = None  # "sub" в токене JWT


class AuthResponse(BaseModel):
    token: str
    user: UserOut