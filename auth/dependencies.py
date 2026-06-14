from typing import Annotated
from fastapi import Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_db
from models.user import User
from auth.jwt_handler import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token", auto_error=False)


async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Authenticate user from:
      1. Authorization: Bearer <token> header  → JS fetch() calls
      2. access_token cookie                   → browser page navigation

    NOTE: This uses request.cookies (plain HTTP cookie reading),
    NOT request.session (no SessionMiddleware needed).
    """
    actual_token = token or request.cookies.get("access_token")
    if not actual_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_token(actual_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    stmt = select(User).filter(User.id == int(user_id))
    result = await db.execute(stmt)
    user = result.scalars().first()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user


# Dependency alias using typing.Annotated for clean injection
CurrentUser = Annotated[User, Depends(get_current_user)]
