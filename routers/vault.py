import asyncio
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_db
from auth.dependencies import CurrentUser
from schemas.vault_entry import VaultEntryCreate, VaultEntryUpdate
from services import vault_service, folder_service
from utils.password_generator import generate_strong_password

router = APIRouter(prefix="/vault", tags=["Vault"])
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard", include_in_schema=False)
async def dashboard(
    request: Request,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    search: Optional[str] = None,
    folder_id: Optional[int] = None,
    favorites: Optional[bool] = None,
    msg: str = "",
    msg_type: str = "",
):
    flash = {"message": msg, "type": msg_type} if msg else None
    entries = await vault_service.get_all_entries(
        db,
        current_user.id,
        search=search,
        folder_id=folder_id,
        favorites_only=bool(favorites),
    )
    folders = await folder_service.get_all_folders(db, current_user.id)
    return templates.TemplateResponse(
        request,
        "vault/dashboard.html",
        {
            "user": current_user,
            "entries": entries,
            "folders": folders,
            "search": search or "",
            "active_folder": folder_id,
            "favorites": favorites,
            "flash": flash,
        },
    )

@router.get("/new", include_in_schema=False)
async def new_entry_page(
    request: Request,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    folders = await folder_service.get_all_folders(db, current_user.id)
    return templates.TemplateResponse(
        request, "vault/entry_form.html", {"user": current_user, "folders": folders, "entry": None}
    )

@router.post("/new")
async def create_entry(
    current_user: CurrentUser,
    entry_data: VaultEntryCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    if not entry_data.title.strip():
        raise HTTPException(status_code=400, detail="Title is required.")

    await vault_service.create_entry(db, entry_data, current_user.id)
    return JSONResponse({"ok": True, "message": f'"{entry_data.title}" saved to vault.'})

@router.get("/api/generate-password")
def api_generate_password(length: int = 16, symbols: bool = True):
    return {"password": generate_strong_password(length, symbols)}

@router.get("/api/entries/{entry_id}/password")
async def get_entry_password(
    entry_id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    entry = await vault_service.get_entry_by_id(db, entry_id, current_user.id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    plain = vault_service.get_decrypted_password(entry)
    return {"password": plain}

@router.get("/{entry_id}", include_in_schema=False)
async def view_entry(
    entry_id: int,
    request: Request,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    entry = await vault_service.get_entry_by_id(db, entry_id, current_user.id)
    if not entry:
        return RedirectResponse(url="/vault/dashboard", status_code=302)
    return templates.TemplateResponse(
        request, "vault/entry_detail.html", {"user": current_user, "entry": entry}
    )

@router.get("/{entry_id}/edit", include_in_schema=False)
async def edit_entry_page(
    entry_id: int,
    request: Request,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    entry = await vault_service.get_entry_by_id(db, entry_id, current_user.id)
    if not entry:
        return RedirectResponse(url="/vault/dashboard", status_code=302)
    folders = await folder_service.get_all_folders(db, current_user.id)
    return templates.TemplateResponse(
        request, "vault/entry_form.html", {"user": current_user, "entry": entry, "folders": folders}
    )

@router.post("/{entry_id}/edit")
async def update_entry(
    entry_id: int,
    current_user: CurrentUser,
    update_data: VaultEntryUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    if update_data.title is not None and not update_data.title.strip():
        raise HTTPException(status_code=400, detail="Title is required.")

    entry = await vault_service.get_entry_by_id(db, entry_id, current_user.id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    await vault_service.update_entry(db, entry, update_data)
    return JSONResponse({"ok": True, "message": f'"{entry.title}" updated.'})

@router.post("/{entry_id}/delete")
async def delete_entry(
    entry_id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    entry = await vault_service.get_entry_by_id(db, entry_id, current_user.id)
    if entry:
        await vault_service.delete_entry(db, entry)
        return JSONResponse({"ok": True, "message": f'"{entry.title}" deleted.'})
    raise HTTPException(status_code=404, detail="Entry not found")

@router.post("/{entry_id}/favorite")
async def toggle_favorite(
    entry_id: int,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    entry = await vault_service.get_entry_by_id(db, entry_id, current_user.id)
    if entry:
        await vault_service.toggle_favorite(db, entry)
        return JSONResponse({"ok": True})
    raise HTTPException(status_code=404, detail="Entry not found")
