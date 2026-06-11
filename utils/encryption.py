import os
import base64
from cryptography.hazmat.primitives.kdf.argon2 import Argon2
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def derive_kek(master_password: str) -> bytes:
    # Static salt of 16 bytes (no separate user-specific salt table needed)
    salt = b"VaultyStaticSalt"
    kdf = Argon2(
        memory_cost=1024 * 64,
        time_cost=3,
        parallelism=4,
        hash_length=32,
        salt=salt
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
