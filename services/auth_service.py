import secrets
import hashlib
from datetime import datetime, timezone, timedelta
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from models.password_reset import PasswordResetToken
from schemas.user import UserCreate
from auth.hashing import hash_password, verify_password
from utils.encryption import derive_kek, generate_dek, encrypt_dek, decrypt_dek, encrypt_dek_with_secret, decrypt_dek_with_secret
from config.settings import settings


async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    # Hash password for login verification
    hashed_pw = hash_password(user_data.password)
    
    # Generate DEK and derive KEK
    dek = generate_dek()
    kek = derive_kek(user_data.password)
    encrypted_dek = encrypt_dek(dek, kek)
    # Also store a server-side backup so password reset can recover the DEK
    server_encrypted_dek = encrypt_dek_with_secret(dek, settings.SECRET_KEY)

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pw,
        encrypted_dek=encrypted_dek,
        server_encrypted_dek=server_encrypted_dek,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> tuple[User, bytes] | None:
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    
    # Decrypt user's DEK for session use
    kek = derive_kek(password)
    try:
        dek = decrypt_dek(user.encrypted_dek, kek)
    except Exception:
        return None
        
    return user, dek


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    stmt = select(User).filter(User.email == email.lower())
    result = await db.execute(stmt)
    return result.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    stmt = select(User).filter(User.username == username)
    result = await db.execute(stmt)
    return result.scalars().first()


async def update_password(db: AsyncSession, user: User, current_password: str, new_password: str) -> bool:
    # Verify current password and decrypt DEK
    old_kek = derive_kek(current_password)
    try:
        dek = decrypt_dek(user.encrypted_dek, old_kek)
    except Exception:
        return False
        
    # Re-encrypt DEK with new KEK and update server backup
    new_kek = derive_kek(new_password)
    new_encrypted_dek = encrypt_dek(dek, new_kek)
    new_server_encrypted_dek = encrypt_dek_with_secret(dek, settings.SECRET_KEY)
    
    # Update user master password hash, new encrypted DEK, and server backup
    user.hashed_password = hash_password(new_password)
    user.encrypted_dek = new_encrypted_dek
    user.server_encrypted_dek = new_server_encrypted_dek
    await db.commit()
    await db.refresh(user)
    return True


async def delete_user(db: AsyncSession, user: User) -> None:
    await db.delete(user)
    await db.commit()


# ── Password Reset Methods ───────────────────────────────────────────────────

async def create_reset_token(db: AsyncSession, user_id: int) -> str:
    """Creates a password reset token. Saves a SHA-256 hash in the database, returns the raw token."""
    # 1. Generate a secure random token and set expiration to 60 minutes (timezone-naive UTC)
    raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
    expires_at = now_utc + timedelta(minutes=60)

    # 2. Check if there is an existing token for this user
    stmt = select(PasswordResetToken).filter(PasswordResetToken.user_id == user_id)
    result = await db.execute(stmt)
    existing_token = result.scalars().first()

    if existing_token:
        # Update existing record instead of deleting and recreating to prevent unique constraint failures
        existing_token.token_hash = token_hash
        existing_token.expires_at = expires_at
        existing_token.created_at = now_utc
    else:
        # Create a new record
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
    """Hashes the user-provided raw token and retrieves the matching valid db record."""
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    stmt = select(PasswordResetToken).filter(PasswordResetToken.token_hash == token_hash)
    result = await db.execute(stmt)
    reset_token = result.scalars().first()
    
    if not reset_token:
        return None

    # Check for expiration
    expires_at_utc = reset_token.expires_at.replace(tzinfo=timezone.utc)
    if expires_at_utc < datetime.now(timezone.utc):
        await db.delete(reset_token)
        await db.commit()
        return None

    return reset_token


async def reset_password_with_token(db: AsyncSession, reset_token: PasswordResetToken, new_password: str) -> None:
    """Resets user's master password, recovering the original DEK via the server backup
    so vault entries remain fully accessible after the reset."""
    stmt = select(User).filter(User.id == reset_token.user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if not user:
        return

    # 1. Recover the original DEK using the server-side backup
    if user.server_encrypted_dek:
        dek = decrypt_dek_with_secret(user.server_encrypted_dek, settings.SECRET_KEY)
    else:
        # Fallback for old accounts without server backup: generate new DEK
        dek = generate_dek()

    # 2. Re-encrypt the recovered DEK with the new KEK and refresh server backup
    new_kek = derive_kek(new_password)
    new_encrypted_dek = encrypt_dek(dek, new_kek)
    new_server_encrypted_dek = encrypt_dek_with_secret(dek, settings.SECRET_KEY)

    # 3. Update user credentials
    user.hashed_password = hash_password(new_password)
    user.encrypted_dek = new_encrypted_dek
    user.server_encrypted_dek = new_server_encrypted_dek

    # 4. Clean up the reset token
    await db.delete(reset_token)
    await db.commit()

