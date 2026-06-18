from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from typing import Optional
import re


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
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def validate_passwords(self) -> "PasswordResetConfirm":
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match.")
        if len(self.password) < 8:
            raise ValueError("Password must be at least 8 characters.")
        if len(self.password) > 72:
            raise ValueError("Password cannot be longer than 72 characters.")
        if not re.search(r"[A-Z]", self.password):
            raise ValueError("Password needs at least one uppercase letter.")
        if not re.search(r"[0-9]", self.password):
            raise ValueError("Password needs at least one number.")
        return self


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

    @model_validator(mode="after")
    def validate_passwords(self) -> "PasswordChangeRequest":
        if self.new_password != self.confirm_password:
            raise ValueError("New passwords do not match.")
        if len(self.new_password) < 8:
            raise ValueError("New password must be at least 8 characters.")
        if len(self.new_password) > 72:
            raise ValueError("New password cannot be longer than 72 characters.")
        if not re.search(r"[A-Z]", self.new_password):
            raise ValueError("New password needs at least one uppercase letter.")
        if not re.search(r"[0-9]", self.new_password):
            raise ValueError("New password needs at least one number.")
        return self
