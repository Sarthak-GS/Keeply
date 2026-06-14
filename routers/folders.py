from typing import Annotated
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_db
from auth.dependencies import CurrentUser
from services import folder_service
from schemas.folder import FolderCreate

router = APIRouter(prefix="/folders", tags=["Folders"])
templates = Jinja2Templates(directory="templates")


@router.get("")
async def folders_page(
    request: Request,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    msg: str = "",
    msg_type: str = "",
):
    flash = {"message": msg, "type": msg_type} if msg else None
    folders = await folder_service.get_all_folders(db, current_user.id)
    return templates.TemplateResponse(
        request,
        "folders/folders.html",
        {"user": current_user, "folders": folders, "flash": flash},
    )


@router.post("/new")
async def create_folder(
    current_user: CurrentUser,
    folder_data: FolderCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    if folder_data.name.strip():
        await folder_service.create_folder(
            db,
            FolderCreate(name=folder_data.name.strip(), icon=folder_data.icon),
            current_user.id
        )
        return JSONResponse({"ok": True, "message": f'Folder "{folder_data.name}" created.'})
    return JSONResponse({"ok": False, "message": "Folder name is required."}, status_code=400)


@router.post("/{folder_id}/delete")
async def delete_folder(
    folder_id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    folder = await folder_service.get_folder_by_id(db, folder_id, current_user.id)
    if folder:
        await folder_service.delete_folder(db, folder)
        return JSONResponse({"ok": True, "message": "Folder deleted."})
    return JSONResponse({"ok": False, "message": "Folder not found."}, status_code=404)
