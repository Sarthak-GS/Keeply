from sqlalchemy.orm import Session
from models.vault_entry import VaultEntry
from schemas.vault_entry import VaultEntryCreate, VaultEntryUpdate
from utils.encryption import encrypt_password, decrypt_password
from typing import List, Optional


def create_entry(db: Session, entry_data: VaultEntryCreate, user_id: int) -> VaultEntry:
    """Create a new vault entry with the password encrypted."""
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
    db.commit()
    db.refresh(entry)
    return entry


def get_all_entries(
    db: Session,
    user_id: int,
    search: Optional[str] = None,
    folder_id: Optional[int] = None,
    favorites_only: bool = False,
) -> List[VaultEntry]:
    """Return filtered list of vault entries for a user."""
    query = db.query(VaultEntry).filter(VaultEntry.user_id == user_id)
    if search:
        query = query.filter(
            VaultEntry.title.ilike(f"%{search}%")
            | VaultEntry.username.ilike(f"%{search}%")
            | VaultEntry.url.ilike(f"%{search}%")
        )
    if folder_id is not None:
        query = query.filter(VaultEntry.folder_id == folder_id)
    if favorites_only:
        query = query.filter(VaultEntry.is_favorite == True)
    return query.order_by(VaultEntry.title).all()


def get_entry_by_id(db: Session, entry_id: int, user_id: int) -> Optional[VaultEntry]:
    """Get a single entry — enforces ownership (IDOR protection)."""
    return (
        db.query(VaultEntry)
        .filter(VaultEntry.id == entry_id, VaultEntry.user_id == user_id)
        .first()
    )


def update_entry(
    db: Session, entry: VaultEntry, entry_data: VaultEntryUpdate
) -> VaultEntry:
    """Update a vault entry's fields."""
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
    db.commit()
    db.refresh(entry)
    return entry


def delete_entry(db: Session, entry: VaultEntry) -> None:
    """Delete a vault entry."""
    db.delete(entry)
    db.commit()


def toggle_favorite(db: Session, entry: VaultEntry) -> VaultEntry:
    """Toggle the is_favorite flag on an entry."""
    entry.is_favorite = not entry.is_favorite
    db.commit()
    db.refresh(entry)
    return entry


def get_decrypted_password(entry: VaultEntry) -> str:
    """Decrypt and return the stored password."""
    return decrypt_password(entry.encrypted_password)
