from sqlalchemy.orm import Session
from models.folder import Folder
from schemas.folder import FolderCreate
from typing import List, Optional


def create_folder(db: Session, folder_data: FolderCreate, user_id: int) -> Folder:
    folder = Folder(
        name=folder_data.name,
        icon=folder_data.icon or "📁",
        user_id=user_id,
    )
    db.add(folder)
    db.commit()
    db.refresh(folder)
    return folder


def get_all_folders(db: Session, user_id: int) -> List[Folder]:
    return db.query(Folder).filter(Folder.user_id == user_id).order_by(Folder.name).all()


def get_folder_by_id(db: Session, folder_id: int, user_id: int) -> Optional[Folder]:
    return (
        db.query(Folder)
        .filter(Folder.id == folder_id, Folder.user_id == user_id)
        .first()
    )


def delete_folder(db: Session, folder: Folder) -> None:
    db.delete(folder)
    db.commit()
