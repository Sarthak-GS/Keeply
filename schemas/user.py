import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


_PASSWORD_MIN = 8
_PASSWORD_MAX = 72


def _validate_password_strength(password: str) -> str:
    if len(password) < _PASSWORD_MIN:
        raise ValueError(f"Password must be at least {_PASSWORD_MIN} characters.")
    if len(password) > _PASSWORD_MAX:
        raise ValueError(f"Password cannot be longer than {_PASSWORD_MAX} characters.")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password needs at least one uppercase letter.")
    if not re.search(r"[0-9]", password):
        raise ValueError("Password needs at least one number.")
    return password


# ── User schemas ──────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserRegister(BaseModel):

    username: str = Field(
        min_length=3,
        max_length=50,
        description="3–50 characters; letters, digits and underscores only.",
    )
    email: EmailStr = Field(max_length=120)
    password: str = Field(min_length=_PASSWORD_MIN, max_length=_PASSWORD_MAX)
    confirm_password: str

    @field_validator("username")
    @classmethod
    def username_chars(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username can only contain letters, numbers, and underscores.")
        return v

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        return _validate_password_strength(v)

    @model_validator(mode="after")
    def passwords_match(self) -> "UserRegister":
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match.")
        return self


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(default=None, min_length=3, max_length=50)

    @field_validator("username")
    @classmethod
    def username_chars(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username can only contain letters, numbers, and underscores.")
        return v


class Token(BaseModel):
    access_token: str
    token_type: str


# ── Password reset ────────────────────────────────────────────────────────────

class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    password: str = Field(min_length=_PASSWORD_MIN, max_length=_PASSWORD_MAX)
    confirm_password: str

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        return _validate_password_strength(v)

    @model_validator(mode="after")
    def passwords_match(self) -> "PasswordResetConfirm":
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match.")
        return self


# ── Password change ───────────────────────────────────────────────────────────

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=_PASSWORD_MIN, max_length=_PASSWORD_MAX)
    confirm_password: str

    @field_validator("new_password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        return _validate_password_strength(v)

    @model_validator(mode="after")
    def passwords_match(self) -> "PasswordChangeRequest":
        if self.new_password != self.confirm_password:
            raise ValueError("New passwords do not match.")
        return self
