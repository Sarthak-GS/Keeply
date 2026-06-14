from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.vault_entry import VaultEntry
from schemas.vault_entry import VaultEntryCreate, VaultEntryUpdate
from utils.encryption import encrypt_password, decrypt_password
from typing import List, Optional

async def create_entry(db: AsyncSession, entry_data: VaultEntryCreate, user_id: int) -> VaultEntry:
    encrypted_pw = encrypt_password(entry_data.password)
    entry = VaultEntry(
        title=entry_data.title,
        username=entry_data.username or "",
        encrypted_password=encrypted_pw,
        url=entry_data.url or "",
        notes=entry_data.notes or "",
        folder_id=entry_data.folder_id,
        user_id=user_id,
    )
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry

async def get_all_entries(
    db: AsyncSession,
    user_id: int,
    search: Optional[str] = None,
    folder_id: Optional[int] = None,
    favorites_only: bool = False,
) -> List[VaultEntry]:
    stmt = select(VaultEntry).filter(VaultEntry.user_id == user_id)
    if search:
        stmt = stmt.filter(
            VaultEntry.title.ilike(f"%{search}%")
            | VaultEntry.username.ilike(f"%{search}%")
            | VaultEntry.url.ilike(f"%{search}%")
        )
    if folder_id is not None:
        stmt = stmt.filter(VaultEntry.folder_id == folder_id)
    if favorites_only:
        stmt = stmt.filter(VaultEntry.is_favorite == True)
    
    result = await db.execute(stmt.order_by(VaultEntry.title))
    return list(result.scalars().all())

async def get_entry_by_id(db: AsyncSession, entry_id: int, user_id: int) -> Optional[VaultEntry]:
    stmt = select(VaultEntry).filter(VaultEntry.id == entry_id, VaultEntry.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def update_entry(
    db: AsyncSession, entry: VaultEntry, entry_data: VaultEntryUpdate
) -> VaultEntry:
    if entry_data.title is not None:
        entry.title = entry_data.title
    if entry_data.username is not None:
        entry.username = entry_data.username
    if entry_data.password is not None:
        entry.encrypted_password = encrypt_password(entry_data.password)
    if entry_data.url is not None:
        entry.url = entry_data.url
    if entry_data.notes is not None:
        entry.notes = entry_data.notes
    if entry_data.folder_id is not None:
        entry.folder_id = entry_data.folder_id
    await db.commit()
    await db.refresh(entry)
    return entry

async def delete_entry(db: AsyncSession, entry: VaultEntry) -> None:
    await db.delete(entry)
    await db.commit()

async def toggle_favorite(db: AsyncSession, entry: VaultEntry) -> VaultEntry:
    entry.is_favorite = not entry.is_favorite
    await db.commit()
    await db.refresh(entry)
    return entry

def get_decrypted_password(entry: VaultEntry) -> str:
    return decrypt_password(entry.encrypted_password)
