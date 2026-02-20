from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import UserRole

class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str
    role: Optional[UserRole] = UserRole.CUSTOMER

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token:str
    token_type: str = "bearer"