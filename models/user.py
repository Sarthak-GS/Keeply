from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    encrypted_dek = Column(Text, nullable=False)
    # Server-side backup of the DEK — allows password reset without losing vault entries
    server_encrypted_dek = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    vault_entries = relationship(
        "VaultEntry", back_populates="owner", cascade="all, delete-orphan"
    )
    folders = relationship(
        "Folder", back_populates="owner", cascade="all, delete-orphan"
    )

