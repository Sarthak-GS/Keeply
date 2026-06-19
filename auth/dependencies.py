import time
from typing import Annotated
from fastapi import Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.session import get_db
from models.user import User
from auth.jwt_handler import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token", auto_error=False)

# In-memory user cache to avoid DB round-trips
_user_cache: dict[int, tuple[User, float]] = {}
_CACHE_TTL = 120  # seconds


def _invalidate_user_cache(user_id: int) -> None:
    _user_cache.pop(user_id, None)


async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
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

    user_id_str = payload.get("sub")
    if user_id_str is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user_id = int(user_id_str)
    now = time.monotonic()

    # Check cache
    cached = _user_cache.get(user_id)
    if cached:
        user, ts = cached
        if now - ts < _CACHE_TTL:
            return user

    # Cache miss
    stmt = select(User).filter(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if not user or not user.is_active:
        _user_cache.pop(user_id, None)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    _user_cache[user_id] = (user, now)
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
