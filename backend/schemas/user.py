from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str = ""
    last_name: str = ""
    privacy_consent: bool = False


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar_url: str
    description: str
    status: str
    role: str = "user"
    privacy_consent: bool = False
    privacy_consent_version: str = ""
    privacy_consent_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
