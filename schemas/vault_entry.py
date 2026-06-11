from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class VaultEntryCreate(BaseModel):
    title: str
    username: Optional[str] = ""
    password: str
    url: Optional[str] = ""
    notes: Optional[str] = ""
    folder_id: Optional[int] = None


class VaultEntryUpdate(BaseModel):
    title: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    url: Optional[str] = None
    notes: Optional[str] = None
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

    class Config:
        from_attributes = True
