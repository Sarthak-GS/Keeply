from fastapi import Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database.session import get_db
from models.user import User
from auth.jwt_handler import decode_token


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """
    FastAPI dependency that reads the JWT from an HTTP-only cookie,
    validates it, and returns the current User object.
    Redirects to /login on any auth failure.
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=307,
            headers={"Location": "/login"},
            detail="Not authenticated",
        )

    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=307,
            headers={"Location": "/login"},
            detail="Invalid or expired token",
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=307, headers={"Location": "/login"})

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=307, headers={"Location": "/login"})

    return user


def get_optional_user(request: Request, db: Session = Depends(get_db)) -> User | None:
    """Returns the current user if authenticated, else None (for public pages)."""
    token = request.cookies.get("access_token")
    if not token:
        return None
    payload = decode_token(token)
    if not payload:
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    return db.query(User).filter(User.id == int(user_id)).first()
