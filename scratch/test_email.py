import asyncio
import sys
import os

# Add parent directory to path so we can import models and config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.email_utils import send_password_reset_email
from config.settings import settings

async def main():
    print("Settings configuration:")
    print("Host:", settings.SMTP_HOST)
    print("Port:", settings.SMTP_PORT)
    print("Username:", settings.SMTP_USERNAME)
    print("Password:", "********" if settings.SMTP_PASSWORD else "(empty)")
    print("Use TLS:", settings.SMTP_USE_TLS)
    print("From email:", settings.SMTP_FROM_EMAIL)

    print("\nAttempting to send email...")
    try:
        await send_password_reset_email("test@example.com", "TestUser", "http://localhost:8000/reset-password?token=test")
        print("Done trying to send email.")
    except Exception as e:
        print("Caught Exception:", e)

if __name__ == "__main__":
    asyncio.run(main())
