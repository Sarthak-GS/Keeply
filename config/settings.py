import os
from typing import Optional
import urllib.parse
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env
load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    
    # Read individual connection parameters
    user: Optional[str] = os.getenv("user")
    password: Optional[str] = os.getenv("password")
    host: Optional[str] = os.getenv("host")
    port: str = os.getenv("port", "5432")
    dbname: Optional[str] = os.getenv("dbname")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-secret-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    # SMTP for Password Reset
    SMTP_HOST: str = os.getenv("SMTP_HOST", "localhost")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM_EMAIL: str = os.getenv("SMTP_FROM_EMAIL", "")
    SMTP_USE_TLS: bool = os.getenv("SMTP_USE_TLS", "True").lower() in ("true", "1", "yes")

    @property
    def async_database_url(self) -> str:
        if self.DATABASE_URL:
            url = self.DATABASE_URL
            if url.startswith("postgresql://"):
                url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
            return url
        
        # Build URL from individual parameters
        user_val = self.user
        pass_val = self.password
        if pass_val:
            # Safely url-encode password to handle special characters like '#'
            pass_val = urllib.parse.quote_plus(pass_val)
        
        host_val = self.host
        port_val = self.port
        dbname_val = self.dbname
        return f"postgresql+asyncpg://{user_val}:{pass_val}@{host_val}:{port_val}/{dbname_val}"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
