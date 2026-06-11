from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from auth.hashing import hash_password, verify_password
from utils.encryption import derive_kek, generate_dek, encrypt_dek, decrypt_dek


def create_user(db: Session, user_data: UserCreate) -> User:
    # Hash password for login verification
    hashed_pw = hash_password(user_data.password)
    
    # Generate DEK and derive KEK
    dek = generate_dek()
    kek = derive_kek(user_data.password)
    encrypted_dek = encrypt_dek(dek, kek)

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pw,
        encrypted_dek=encrypted_dek,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, email: str, password: str) -> tuple[User, bytes] | None:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    
    # Decrypt user's DEK for session use
    kek = derive_kek(password)
    try:
        dek = decrypt_dek(user.encrypted_dek, kek)
    except Exception:
        return None
        
    return user, dek


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def update_password(db: Session, user: User, current_password: str, new_password: str) -> bool:
    # Verify current password and decrypt DEK
    old_kek = derive_kek(current_password)
    try:
        dek = decrypt_dek(user.encrypted_dek, old_kek)
    except Exception:
        return False
        
    # Re-encrypt DEK with new KEK
    new_kek = derive_kek(new_password)
    new_encrypted_dek = encrypt_dek(dek, new_kek)
    
    # Update user master password hash and new encrypted DEK
    user.hashed_password = hash_password(new_password)
    user.encrypted_dek = new_encrypted_dek
    db.commit()
    db.refresh(user)
    return True
