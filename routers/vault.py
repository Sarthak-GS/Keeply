from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from database.session import get_db
from auth.dependencies import get_current_user
from models.user import User
from schemas.vault_entry import VaultEntryCreate, VaultEntryUpdate
from services import vault_service, folder_service
from utils.password_generator import generate_strong_password

router = APIRouter(prefix="/vault", tags=["Vault"])
templates = Jinja2Templates(directory="templates")


# ── Dashboard ─────────────────────────────────────────────────────────────────
@router.get("/dashboard")
def dashboard(
    request: Request,
    search: Optional[str] = None,
    folder_id: Optional[int] = None,
    favorites: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    flash = request.session.pop("flash", None)
    entries = vault_service.get_all_entries(
        db,
        current_user.id,
        search=search,
        folder_id=folder_id,
        favorites_only=bool(favorites),
    )
    folders = folder_service.get_all_folders(db, current_user.id)
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


# ── New Entry ─────────────────────────────────────────────────────────────────
@router.get("/new")
def new_entry_page(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    folders = folder_service.get_all_folders(db, current_user.id)
    return templates.TemplateResponse(
        request, "vault/entry_form.html", {"user": current_user, "folders": folders, "entry": None}
    )


@router.post("/new")
async def create_entry(
    request: Request,
    title: str = Form(...),
    username: str = Form(""),
    password: str = Form(...),
    url: str = Form(""),
    notes: str = Form(""),
    folder_id: Optional[int] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not title.strip():
        folders = folder_service.get_all_folders(db, current_user.id)
        return templates.TemplateResponse(
            request,
            "vault/entry_form.html",
            {"user": current_user, "folders": folders, "entry": None,
             "error": "Title is required."},
        )
    entry_data = VaultEntryCreate(
        title=title, username=username, password=password,
        url=url, notes=notes, folder_id=folder_id
    )
    vault_service.create_entry(db, entry_data, current_user.id)
    request.session["flash"] = {"message": f'"{title}" saved to vault.', "type": "success"}
    return RedirectResponse(url="/vault/dashboard", status_code=302)


# ── View Entry ────────────────────────────────────────────────────────────────
@router.get("/{entry_id}")
def view_entry(
    entry_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entry = vault_service.get_entry_by_id(db, entry_id, current_user.id)
    if not entry:
        request.session["flash"] = {"message": "Entry not found.", "type": "error"}
        return RedirectResponse(url="/vault/dashboard", status_code=302)
    return templates.TemplateResponse(
        request, "vault/entry_detail.html", {"user": current_user, "entry": entry}
    )


# ── Edit Entry ────────────────────────────────────────────────────────────────
@router.get("/{entry_id}/edit")
def edit_entry_page(
    entry_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entry = vault_service.get_entry_by_id(db, entry_id, current_user.id)
    if not entry:
        return RedirectResponse(url="/vault/dashboard", status_code=302)
    folders = folder_service.get_all_folders(db, current_user.id)
    return templates.TemplateResponse(
        request, "vault/entry_form.html", {"user": current_user, "entry": entry, "folders": folders}
    )


@router.post("/{entry_id}/edit")
async def update_entry(
    entry_id: int,
    request: Request,
    title: str = Form(...),
    username: str = Form(""),
    password: str = Form(""),
    url: str = Form(""),
    notes: str = Form(""),
    folder_id: Optional[int] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entry = vault_service.get_entry_by_id(db, entry_id, current_user.id)
    if not entry:
        return RedirectResponse(url="/vault/dashboard", status_code=302)

    update_data = VaultEntryUpdate(
        title=title,
        username=username,
        password=password if password else None,
        url=url,
        notes=notes,
        folder_id=folder_id,
    )
    vault_service.update_entry(db, entry, update_data)
    request.session["flash"] = {"message": f'"{title}" updated.', "type": "success"}
    return RedirectResponse(url=f"/vault/{entry_id}", status_code=302)


# ── Delete Entry ──────────────────────────────────────────────────────────────
@router.post("/{entry_id}/delete")
async def delete_entry(
    entry_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entry = vault_service.get_entry_by_id(db, entry_id, current_user.id)
    if entry:
        title = entry.title
        vault_service.delete_entry(db, entry)
        request.session["flash"] = {"message": f'"{title}" deleted.', "type": "success"}
    return RedirectResponse(url="/vault/dashboard", status_code=302)


# ── Toggle Favorite ───────────────────────────────────────────────────────────
@router.post("/{entry_id}/favorite")
async def toggle_favorite(
    entry_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entry = vault_service.get_entry_by_id(db, entry_id, current_user.id)
    if entry:
        vault_service.toggle_favorite(db, entry)
    return RedirectResponse(url="/vault/dashboard", status_code=302)


# ── API: Get decrypted password (for clipboard copy) ─────────────────────────
# NOTE: these must be defined BEFORE /{entry_id} so FastAPI matches /api/... first
@router.get("/api/generate-password")
def api_generate_password(length: int = 16, symbols: bool = True):
    return {"password": generate_strong_password(length, symbols)}


@router.get("/api/entries/{entry_id}/password")
def get_password(
    entry_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    from fastapi import HTTPException
    entry = vault_service.get_entry_by_id(db, entry_id, current_user.id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return {"password": vault_service.get_decrypted_password(entry)}
