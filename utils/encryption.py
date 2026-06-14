import os
import hashlib
import base64
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

_STATIC_SALT = b"VaultyStaticSalt"  # 16 bytes


def derive_kek(master_password: str) -> bytes:
    kdf = Argon2id(
        salt=_STATIC_SALT,
        length=32,
        iterations=3,
        lanes=4,
        memory_cost=64 * 1024,
    )
    return kdf.derive(master_password.encode("utf-8"))


def generate_dek() -> bytes:
    return os.urandom(32)


def encrypt_dek(dek: bytes, kek: bytes) -> str:
    aesgcm = AESGCM(kek)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, dek, None)
    combined = nonce + ciphertext
    return base64.b64encode(combined).decode("utf-8")


def decrypt_dek(encrypted_dek: str, kek: bytes) -> bytes:
    combined = base64.b64decode(encrypted_dek.encode("utf-8"))
    nonce = combined[:12]
    ciphertext = combined[12:]
    aesgcm = AESGCM(kek)
    return aesgcm.decrypt(nonce, ciphertext, None)


def _server_key(secret: str) -> bytes:
    """Derive a 32-byte AES key from the app SECRET_KEY using SHA-256."""
    return hashlib.sha256(secret.encode("utf-8")).digest()


def encrypt_dek_with_secret(dek: bytes, secret: str) -> str:
    """Encrypt the DEK using the app SECRET_KEY for server-side recovery."""
    key = _server_key(secret)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, dek, None)
    return base64.b64encode(nonce + ciphertext).decode("utf-8")


def decrypt_dek_with_secret(encrypted: str, secret: str) -> bytes:
    """Decrypt the DEK using the app SECRET_KEY (used during password reset)."""
    key = _server_key(secret)
    combined = base64.b64decode(encrypted.encode("utf-8"))
    nonce, ciphertext = combined[:12], combined[12:]
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)


def encrypt_password(plain: str, dek: bytes) -> str:
    aesgcm = AESGCM(dek)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plain.encode("utf-8"), None)
    combined = nonce + ciphertext
    return base64.b64encode(combined).decode("utf-8")


def decrypt_password(encrypted: str, dek: bytes) -> str:
    combined = base64.b64decode(encrypted.encode("utf-8"))
    nonce = combined[:12]
    ciphertext = combined[12:]
    aesgcm = AESGCM(dek)
    return aesgcm.decrypt(nonce, ciphertext, None).decode("utf-8")

