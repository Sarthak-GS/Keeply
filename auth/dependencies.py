from typing import Annotated
from fastapi import Request, Depends, HTTPException
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
    # Look for token in Authorization header or in secure server-side session
    actual_token = token or request.session.get("access_token")
    if not actual_token:
        raise HTTPException(
            status_code=307,
            headers={"Location": "/login"},
            detail="Not authenticated",
        )

    payload = decode_token(actual_token)
    if payload is None:
        raise HTTPException(
            status_code=307,
            headers={"Location": "/login"},
            detail="Invalid or expired token",
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=307, headers={"Location": "/login"})

    stmt = select(User).filter(User.id == int(user_id))
    result = await db.execute(stmt)
    user = result.scalars().first()
    if not user or not user.is_active:
        raise HTTPException(status_code=307, headers={"Location": "/login"})

    return user


# Dependency alias using typing.Annotated for clean injection
CurrentUser = Annotated[User, Depends(get_current_user)]
