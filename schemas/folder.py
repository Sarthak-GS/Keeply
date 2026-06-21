from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class FolderCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Folder display name.")
    icon: Optional[str] = Field(default="📁", max_length=10)


class FolderResponse(BaseModel):
    id: int
    name: str
    icon: str
    created_at: datetime

    model_config = {"from_attributes": True}
