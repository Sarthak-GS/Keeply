from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class VaultEntryCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200, description="Display name for the entry.")
    username: Optional[str] = Field(default="", max_length=200)
    password: str = Field(min_length=1, max_length=1000, description="The credential to store (encrypted at rest).")
    url: Optional[str] = Field(default="", max_length=2000)
    notes: Optional[str] = Field(default="", max_length=5000)
    folder_id: Optional[int] = None


class VaultEntryUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    username: Optional[str] = Field(default=None, max_length=200)
    password: Optional[str] = Field(default=None, min_length=1, max_length=1000)
    url: Optional[str] = Field(default=None, max_length=2000)
    notes: Optional[str] = Field(default=None, max_length=5000)
    folder_id: Optional[int] = None


class VaultEntryResponse(BaseModel):
    id: int
    title: str
    username: str
    url: str
    notes: str
    is_favorite: bool
    folder_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
