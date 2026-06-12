from typing import Annotated
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_db
from auth.dependencies import CurrentUser
from services import auth_service

router = APIRouter(prefix="/profile", tags=["Profile"])
templates = Jinja2Templates(directory="templates")


@router.get("")
async def profile_page(
    request: Request,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    flash = request.session.pop("flash", None)
    return templates.TemplateResponse(
        request, "profile/profile.html", {"user": current_user, "flash": flash}
    )


@router.post("/change-password")
async def change_password(
    request: Request,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
):
    errors = []
    if len(new_password) < 8:
        errors.append("New password must be at least 8 characters.")
    if len(new_password) > 72:
        errors.append("New password cannot be longer than 72 characters.")
    if new_password != confirm_password:
        errors.append("New passwords do not match.")

    if errors:
        return templates.TemplateResponse(
            request,
            "profile/profile.html",
            {"user": current_user, "errors": errors},
        )

    success = await auth_service.update_password(
        db, current_user, current_password, new_password
    )
    if not success:
        return templates.TemplateResponse(
            request,
            "profile/profile.html",
            {"user": current_user, "errors": ["Current password is incorrect."]},
        )

    request.session.clear()
    request.session["flash"] = {
        "message": "Password successfully changed. Please log in again.",
        "type": "success",
    }
    return RedirectResponse(url="/login", status_code=302)


@router.post("/delete")
async def delete_account(
    request: Request,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    await auth_service.delete_user(db, current_user)
    request.session.clear()
    return RedirectResponse(url="/signup", status_code=302)
