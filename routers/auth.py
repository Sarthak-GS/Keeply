import re
import base64
from typing import Annotated
from fastapi import APIRouter, Depends, Form, Request, HTTPException, BackgroundTasks
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_db
from services import auth_service
from auth.jwt_handler import create_access_token
from schemas.user import UserCreate, UserResponse, Token, PasswordResetConfirm
from auth.dependencies import CurrentUser
from utils.email_utils import send_password_reset_email

router = APIRouter(tags=["Authentication"])
templates = Jinja2Templates(directory="templates")


# ── Landing Page ──────────────────────────────────────────────────────────────
@router.get("/", include_in_schema=False)
def landing(request: Request):
    return templates.TemplateResponse(request, "index.html", {"page_title": "Vaultify"})


# ── Signup ────────────────────────────────────────────────────────────────────
@router.get("/signup", include_in_schema=False)
def signup_page(request: Request, msg: str = "", msg_type: str = ""):
    flash = {"message": msg, "type": msg_type} if msg else None
    return templates.TemplateResponse(request, "auth/signup.html", {"flash": flash})


@router.post("/signup", include_in_schema=False)
async def signup(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
):
    errors = []

    if len(username) < 3 or len(username) > 50:
        errors.append("Username must be 3–50 characters.")
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        errors.append("Username can only contain letters, numbers, and underscores.")
    if len(password) < 8:
        errors.append("Password must be at least 8 characters.")
    if len(password) > 72:
        errors.append("Password cannot be longer than 72 characters.")
    if password != confirm_password:
        errors.append("Passwords do not match.")
    if not re.search(r"[A-Z]", password):
        errors.append("Password needs at least one uppercase letter.")
    if not re.search(r"[0-9]", password):
        errors.append("Password needs at least one number.")
    if await auth_service.get_user_by_email(db, email.lower()):
        errors.append("Email is already registered.")
    if await auth_service.get_user_by_username(db, username):
        errors.append("Username is already taken.")

    if errors:
        return templates.TemplateResponse(
            request,
            "auth/signup.html",
            {"errors": errors, "username": username, "email": email},
        )

    await auth_service.create_user(db, UserCreate(username=username, email=email.lower(), password=password))
    return RedirectResponse(
        url="/login?msg=Account+created!+Please+log+in.&msg_type=success",
        status_code=302,
    )


# ── Login (page only — auth is via JS fetch to /token) ───────────────────────
@router.get("/login", include_in_schema=False)
def login_page(request: Request, msg: str = "", msg_type: str = ""):
    flash = {"message": msg, "type": msg_type} if msg else None
    return templates.TemplateResponse(request, "auth/login.html", {"flash": flash})


# ── OAuth2 Token Exchange endpoint ───────────────────────────────────────────
@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    user = await auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token(data={"sub": str(user.id)})
    return {
        "access_token": token,
        "token_type": "bearer",
    }


# ── Current User endpoint ────────────────────────────────────────────────────
@router.get("/api/auth/me", response_model=UserResponse)
async def get_me(current_user: CurrentUser):
    return current_user


# ── Password Reset Flow ───────────────────────────────────────────────────────

@router.get("/forgot-password", include_in_schema=False)
def forgot_password_page(request: Request, msg: str = "", msg_type: str = ""):
    flash = {"message": msg, "type": msg_type} if msg else None
    return templates.TemplateResponse(request, "auth/forgot_password.html", {"flash": flash})


@router.post("/forgot-password", include_in_schema=False)
async def process_forgot_password(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Annotated[AsyncSession, Depends(get_db)],
    email: str = Form(...),
):
    import logging
    _log = logging.getLogger(__name__)
    try:
        user = await auth_service.get_user_by_email(db, email.lower())
        if user:
            # Save plain values NOW — after db.commit() inside create_reset_token,
            # the ORM object is expired and accessing .email/.username would trigger
            # a lazy reload that fails in async (MissingGreenlet).
            user_email = user.email
            user_username = user.username

            # Generate / refresh reset token (commits internally)
            token = await auth_service.create_reset_token(db, user.id)

            # Build the absolute reset link
            base = str(request.base_url).rstrip("/")
            reset_link = f"{base}/reset-password?token={token}"

            # Enqueue email in background so response is not blocked
            background_tasks.add_task(
                send_password_reset_email,
                to_email=user_email,
                username=user_username,
                reset_link=reset_link,
            )
    except Exception as exc:
        _log.exception("Forgot-password error: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to process reset request. Check server logs.")

    # Generic message prevents user enumeration
    return RedirectResponse(
        url="/login?msg=If+the+email+is+registered,+a+password+reset+link+has+been+sent.&msg_type=success",
        status_code=302,
    )


@router.get("/reset-password", include_in_schema=False)
async def reset_password_page(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
    token: str,
):
    reset_token = await auth_service.get_valid_reset_token(db, token)
    if not reset_token:
        return RedirectResponse(
            url="/forgot-password?msg=The+password+reset+link+is+invalid+or+has+expired.&msg_type=error",
            status_code=302,
        )

    return templates.TemplateResponse(
        request, "auth/reset_password.html", {"token": token}
    )


@router.post("/reset-password")
async def process_reset_password(
    data: PasswordResetConfirm,
    db: Annotated[AsyncSession, Depends(get_db)],
):

    # Validate token
    reset_token = await auth_service.get_valid_reset_token(db, data.token)
    if not reset_token:
        raise HTTPException(
            status_code=400,
            detail="The password reset link is invalid or has expired."
        )

    # Perform Reset (Updates password, generates new DEK, deletes token)
    await auth_service.reset_password_with_token(db, reset_token, data.password)

    from fastapi.responses import JSONResponse
    return JSONResponse({
        "ok": True,
        "message": "Password reset successful! Please log in with your new password."
    })
