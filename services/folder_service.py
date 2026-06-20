from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from models.folder import Folder
from schemas.folder import FolderCreate
from typing import List, Optional


async def create_folder(db: AsyncSession, folder_data: FolderCreate, user_id: int) -> Folder:
    folder = Folder(
        name=folder_data.name,
        icon=folder_data.icon or "📁",
        user_id=user_id,
    )
    db.add(folder)
    await db.commit()
    await db.refresh(folder)
    return folder


async def get_all_folders(db: AsyncSession, user_id: int) -> List[Folder]:
    stmt = select(Folder).options(selectinload(Folder.vault_entries)).filter(Folder.user_id == user_id).order_by(Folder.name)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_folder_by_id(db: AsyncSession, folder_id: int, user_id: int) -> Optional[Folder]:
    stmt = select(Folder).filter(Folder.id == folder_id, Folder.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalars().first()


async def delete_folder(db: AsyncSession, folder: Folder) -> None:
    await db.delete(folder)
    await db.commit()
