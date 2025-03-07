from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    rolId: int
    adscripcionId: int

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    rolId: int
    adscripcionId: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

