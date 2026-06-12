from typing import Annotated
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
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
):
    flash = request.session.pop("flash", None)
    folders = await folder_service.get_all_folders(db, current_user.id)
    return templates.TemplateResponse(
        request,
        "folders/folders.html",
        {"user": current_user, "folders": folders, "flash": flash},
    )


@router.post("/new")
async def create_folder(
    request: Request,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    name: str = Form(...),
    icon: str = Form("📁"),
):
    if name.strip():
        await folder_service.create_folder(db, FolderCreate(name=name.strip(), icon=icon), current_user.id)
        request.session["flash"] = {"message": f'Folder "{name}" created.', "type": "success"}
    return RedirectResponse(url="/folders", status_code=302)


@router.post("/{folder_id}/delete")
async def delete_folder(
    folder_id: int,
    request: Request,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    folder = await folder_service.get_folder_by_id(db, folder_id, current_user.id)
    if folder:
        await folder_service.delete_folder(db, folder)
        request.session["flash"] = {"message": "Folder deleted.", "type": "success"}
    return RedirectResponse(url="/folders", status_code=302)
