from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./vaultify.db"
    SECRET_KEY: str = "change-this-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # SMTP Configuration for Password Reset Email
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = ""
    SMTP_USE_TLS: bool = True

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
