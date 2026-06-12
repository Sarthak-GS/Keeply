import re
import base64
from typing import Annotated
from fastapi import APIRouter, Depends, Form, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_db
from services import auth_service
from auth.jwt_handler import create_access_token
from schemas.user import UserCreate, UserResponse, Token
from auth.dependencies import CurrentUser

router = APIRouter(tags=["Authentication"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
def landing(request: Request):
    # Retrieve token from secure server session instead of cookies
    token = request.session.get("access_token")
    if token:
        from auth.jwt_handler import decode_token
        payload = decode_token(token)
        if payload:
            return RedirectResponse(url="/vault/dashboard", status_code=302)
    return templates.TemplateResponse(request, "index.html", {"page_title": "Vaultify"})


@router.get("/signup")
def signup_page(request: Request):
    flash = request.session.pop("flash", None)
    return templates.TemplateResponse(request, "auth/signup.html", {"flash": flash})


@router.post("/signup")
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
    if await auth_service.get_user_by_email(db, email):
        errors.append("Email is already registered.")
    if await auth_service.get_user_by_username(db, username):
        errors.append("Username is already taken.")

    if errors:
        return templates.TemplateResponse(
            request,
            "auth/signup.html",
            {"errors": errors, "username": username, "email": email},
        )

    await auth_service.create_user(db, UserCreate(username=username, email=email, password=password))
    request.session["flash"] = {"message": "Account created! Please log in.", "type": "success"}
    return RedirectResponse(url="/login", status_code=302)


@router.get("/login")
def login_page(request: Request):
    flash = request.session.pop("flash", None)
    return templates.TemplateResponse(request, "auth/login.html", {"flash": flash})


@router.post("/login")
async def login(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
    email: str = Form(...),
    password: str = Form(...),
):
    if len(password) > 72:
        return templates.TemplateResponse(
            request, "auth/login.html", {"error": "Invalid email or password."},
        )

    auth_result = await auth_service.authenticate_user(db, email, password)
    if not auth_result:
        return templates.TemplateResponse(
            request, "auth/login.html", {"error": "Invalid email or password."},
        )

    user, dek = auth_result
    request.session["dek"] = base64.b64encode(dek).decode("utf-8")

    token = create_access_token(data={"sub": str(user.id)})
    
    # Store access token in secure server session instead of cookies
    request.session["access_token"] = token

    return RedirectResponse(url="/vault/dashboard", status_code=302)


# ── OAuth2 Token Exchange endpoint ───────────────────────────────────────────
@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    auth_result = await auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not auth_result:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    user, _ = auth_result
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


# ── Current User endpoint ────────────────────────────────────────────────────
@router.get("/api/auth/me", response_model=UserResponse)
async def get_me(current_user: CurrentUser):
    return current_user
