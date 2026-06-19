from typing import Annotated
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_db
from auth.dependencies import CurrentUser, _invalidate_user_cache
from services import auth_service
from schemas.user import PasswordChangeRequest

router = APIRouter(prefix="/profile", tags=["Profile"])
templates = Jinja2Templates(directory="templates")


@router.get("")
async def profile_page(
    request: Request,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    msg: str = "",
    msg_type: str = "",
):
    flash = {"message": msg, "type": msg_type} if msg else None
    return templates.TemplateResponse(
        request, "profile/profile.html", {"user": current_user, "flash": flash}
    )


@router.post("/change-password")
async def change_password(
    current_user: CurrentUser,
    data: PasswordChangeRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):


    success = await auth_service.update_password(
        db, current_user, data.current_password, data.new_password
    )
    if not success:
        raise HTTPException(status_code=400, detail="Current password is incorrect.")
    _invalidate_user_cache(current_user.id)

    # Return JSON — client-side JS will clear localStorage and redirect
    return JSONResponse({
        "ok": True,
        "message": "Password successfully changed. Please log in again.",
        "redirect": "/login",
    })


@router.post("/delete")
async def delete_account(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    _invalidate_user_cache(current_user.id)
    await auth_service.delete_user(db, current_user)
    # Return JSON — client-side JS will clear localStorage and redirect
    return JSONResponse({
        "ok": True,
        "message": "Account deleted.",
        "redirect": "/signup",
    })
