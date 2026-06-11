from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database.session import get_db
from auth.dependencies import get_current_user
from auth.hashing import verify_password
from models.user import User
from services import auth_service

router = APIRouter(prefix="/profile", tags=["Profile"])
templates = Jinja2Templates(directory="templates")


@router.get("")
def profile_page(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    flash = request.session.pop("flash", None)
    return templates.TemplateResponse(
        request, "profile/profile.html", {"user": current_user, "flash": flash}
    )


@router.post("/change-password")
async def change_password(
    request: Request,
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    errors = []
    if len(current_password) > 72:
        errors.append("Current password is incorrect.")
    elif not verify_password(current_password, current_user.hashed_password):
        errors.append("Current password is incorrect.")
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

    auth_service.update_password(db, current_user, new_password)
    request.session["flash"] = {"message": "Password changed successfully.", "type": "success"}
    return RedirectResponse(url="/profile", status_code=302)
