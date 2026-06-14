from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime


    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetConfirm(BaseModel):
    token: str
    password: str = Field(..., min_length=8, max_length=72)
    confirm_password: str



class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str



