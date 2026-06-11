import re
import base64
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database.session import get_db
from services import auth_service
from auth.jwt_handler import create_access_token
from schemas.user import UserCreate

router = APIRouter(tags=["Authentication"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
def landing(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
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
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db),
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
    if auth_service.get_user_by_email(db, email):
        errors.append("Email is already registered.")
    if auth_service.get_user_by_username(db, username):
        errors.append("Username is already taken.")

    if errors:
        return templates.TemplateResponse(
            request,
            "auth/signup.html",
            {"errors": errors, "username": username, "email": email},
        )

    auth_service.create_user(db, UserCreate(username=username, email=email, password=password))
    request.session["flash"] = {"message": "Account created! Please log in.", "type": "success"}
    return RedirectResponse(url="/login", status_code=302)


@router.get("/login")
def login_page(request: Request):
    flash = request.session.pop("flash", None)
    return templates.TemplateResponse(request, "auth/login.html", {"flash": flash})


@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    if len(password) > 72:
        return templates.TemplateResponse(
            request,
            "auth/login.html",
            {"error": "Invalid email or password."},
        )

    auth_result = auth_service.authenticate_user(db, email, password)
    if not auth_result:
        return templates.TemplateResponse(
            request,
            "auth/login.html",
            {"error": "Invalid email or password."},
        )

    user, dek = auth_result
    
    # Store decrypted DEK in session (base64 string)
    request.session["dek"] = base64.b64encode(dek).decode("utf-8")

    token = create_access_token(data={"sub": str(user.id)})
    response = RedirectResponse(url="/vault/dashboard", status_code=302)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,   # Set True in production (HTTPS)
        samesite="lax",
        max_age=3600,
    )
    return response


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("access_token")
    return response
