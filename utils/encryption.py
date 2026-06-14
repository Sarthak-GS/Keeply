import os
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from config.settings import settings

def _get_encryption_key() -> bytes:
    return hashlib.sha256(settings.SECRET_KEY.encode("utf-8")).digest()

def encrypt_password(plain: str) -> str:
    key = _get_encryption_key()
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plain.encode("utf-8"), None)
    return base64.b64encode(nonce + ciphertext).decode("utf-8")

def decrypt_password(encrypted: str) -> str:
    key = _get_encryption_key()
    combined = base64.b64decode(encrypted.encode("utf-8"))
    nonce, ciphertext = combined[:12], combined[12:]
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None).decode("utf-8")
