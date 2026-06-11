from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FolderCreate(BaseModel):
    name: str
    icon: Optional[str] = "📁"


class FolderResponse(BaseModel):
    id: int
    name: str
    icon: str
    created_at: datetime

    class Config:
        from_attributes = True
