import secrets
import hashlib
from datetime import datetime, timezone, timedelta
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from models.password_reset import PasswordResetToken
from schemas.user import UserCreate
from auth.hashing import hash_password, verify_password

async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    stmt = select(User).filter(User.email == email.lower())
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    stmt = select(User).filter(User.username == username)
    result = await db.execute(stmt)
    return result.scalars().first()

async def update_password(db: AsyncSession, user: User, current_password: str, new_password: str) -> bool:
    if not verify_password(current_password, user.hashed_password):
        return False
    user.hashed_password = hash_password(new_password)
    await db.commit()
    await db.refresh(user)
    return True

async def delete_user(db: AsyncSession, user: User) -> None:
    await db.delete(user)
    await db.commit()

async def create_reset_token(db: AsyncSession, user_id: int) -> str:
    raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
    expires_at = now_utc + timedelta(minutes=60)

    stmt = select(PasswordResetToken).filter(PasswordResetToken.user_id == user_id)
    result = await db.execute(stmt)
    existing_token = result.scalars().first()

    if existing_token:
        existing_token.token_hash = token_hash
        existing_token.expires_at = expires_at
        existing_token.created_at = now_utc
    else:
        reset_token = PasswordResetToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            created_at=now_utc,
        )
        db.add(reset_token)

    await db.commit()
    return raw_token

async def get_valid_reset_token(db: AsyncSession, raw_token: str) -> PasswordResetToken | None:
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    stmt = select(PasswordResetToken).filter(PasswordResetToken.token_hash == token_hash)
    result = await db.execute(stmt)
    reset_token = result.scalars().first()
    
    if not reset_token:
        return None

    expires_at_utc = reset_token.expires_at.replace(tzinfo=timezone.utc)
    if expires_at_utc < datetime.now(timezone.utc):
        await db.delete(reset_token)
        await db.commit()
        return None

    return reset_token

async def reset_password_with_token(db: AsyncSession, reset_token: PasswordResetToken, new_password: str) -> None:
    stmt = select(User).filter(User.id == reset_token.user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if not user:
        return

    user.hashed_password = hash_password(new_password)
    await db.delete(reset_token)
    await db.commit()
