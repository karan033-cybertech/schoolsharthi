from typing import List, Optional
from pathlib import Path
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./schoolsharthi.db"

    # JWT
    SECRET_KEY: str = "change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # AWS S3
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "ap-south-1"
    S3_BUCKET_NAME: Optional[str] = None

    # Local storage
    USE_LOCAL_STORAGE: bool = True
    LOCAL_STORAGE_PATH: str = "uploads"
    API_BASE_URL: str = "http://localhost:8000"

    # AI Keys
    OPENAI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None

    # CORS (string from env)
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000,https://schoolsharthi.vercel.app"
    )

    # Environment
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    def cors_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


# Load settings
settings = Settings()

print("🌐 CORS ORIGINS STRING:", settings.CORS_ORIGINS)
print("🌐 CORS ORIGINS LIST:", settings.cors_list())
