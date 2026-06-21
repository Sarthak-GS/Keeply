import urllib.parse
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    
    user: Optional[str] = None
    password: Optional[str] = None
    host: Optional[str] = None
    port: str = "5432"
    dbname: Optional[str] = None

    SECRET_KEY: str = "change-this-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = ""
    SMTP_USE_TLS: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True
    )

    @property
    def async_database_url(self) -> str:
        if self.DATABASE_URL:
            url = self.DATABASE_URL
            if url.startswith("postgresql://"):
                url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
            return url
        
        # Validate that we have the minimum required individual database parameters
        if not self.host or not self.user:
            raise ValueError(
                "Database configuration is missing. "
                "Please configure either DATABASE_URL or the individual database parameters "
                "(host, user, password, dbname) in your environment or .env file."
            )
        
        user_val = self.user
        pass_val = self.password
        if pass_val:
            pass_val = urllib.parse.quote_plus(pass_val)
        
        host_val = self.host
        port_val = self.port
        dbname_val = self.dbname or "postgres"
        return f"postgresql+asyncpg://{user_val}:{pass_val}@{host_val}:{port_val}/{dbname_val}"


settings = Settings()
