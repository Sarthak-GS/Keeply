import secrets
import string


def generate_strong_password(length: int = 16, use_symbols: bool = True) -> str:
 
    length = max(8, min(length, 128))

    alphabet = string.ascii_letters + string.digits
    if use_symbols:
        alphabet += "!@#$%^&*()-_=+[]{}|;:,.<>?"

    password_chars = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
    ]
    if use_symbols:
        password_chars.append(secrets.choice("!@#$%^&*()-_=+"))

    while len(password_chars) < length:
        password_chars.append(secrets.choice(alphabet))

    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)
