from cryptography.fernet import Fernet
from config.settings import settings

_fernet = Fernet(settings.ENCRYPTION_KEY.encode())


def encrypt_password(plain: str) -> str:
    """Encrypt a vault password for safe storage in the DB."""
    return _fernet.encrypt(plain.encode()).decode()


def decrypt_password(encrypted: str) -> str:
    """Decrypt a stored vault password for display to the user."""
    return _fernet.decrypt(encrypted.encode()).decode()
