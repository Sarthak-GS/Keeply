import secrets
import string


def generate_strong_password(length: int = 16, use_symbols: bool = True) -> str:
    """
    Generate a cryptographically secure random password.
    Always includes at least one uppercase, lowercase, digit, and symbol.
    """
    length = max(8, min(length, 128))

    alphabet = string.ascii_letters + string.digits
    if use_symbols:
        alphabet += "!@#$%^&*()-_=+[]{}|;:,.<>?"

    # Guarantee at least one of each character type
    password_chars = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
    ]
    if use_symbols:
        password_chars.append(secrets.choice("!@#$%^&*()-_=+"))

    # Fill the rest
    while len(password_chars) < length:
        password_chars.append(secrets.choice(alphabet))

    # Shuffle so guaranteed chars aren't always at the start
    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)
