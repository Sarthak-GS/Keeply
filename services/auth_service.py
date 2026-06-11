from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from auth.hashing import hash_password, verify_password


def create_user(db: Session, user_data: UserCreate) -> User:
    """Create a new user with a hashed password."""
    hashed_pw = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pw,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """Verify email+password and return the user, or None on failure."""
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def update_password(db: Session, user: User, new_password: str) -> User:
    """Update a user's hashed password."""
    user.hashed_password = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return user
