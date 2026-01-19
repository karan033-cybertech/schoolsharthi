from typing import List, Optional
from pathlib import Path
import os
import json

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./schoolsharthi.db"

    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # AWS S3
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "ap-south-1"
    S3_BUCKET_NAME: Optional[str] = None
    
    # Local Storage
    USE_LOCAL_STORAGE: bool = True
    LOCAL_STORAGE_PATH: str = "uploads"
    API_BASE_URL: str = "http://localhost:8000"

    # AI Keys
    OPENAI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None

    # Environment
    ENVIRONMENT: str = "development"

    # CORS
    CORS_ORIGINS: List[str] = Field(default_factory=list)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


def parse_cors(value: Optional[str]) -> List[str]:
    default = [
        "http://localhost:3000",
        "https://schoolsharthi.vercel.app"
    ]

    if not value:
        return default

    value = value.strip()

    # JSON array format
    if value.startswith("["):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return parsed
        except:
            return default

    # Comma separated
    return [v.strip() for v in value.split(",") if v.strip()]


# Load settings
settings = Settings()

# Load CORS safely
settings.CORS_ORIGINS = parse_cors(os.getenv("CORS_ORIGINS"))

print("✅ Settings Loaded")
print("🌐 CORS Origins:", settings.CORS_ORIGINS)
print("🌍 Environment:", settings.ENVIRONMENT)
