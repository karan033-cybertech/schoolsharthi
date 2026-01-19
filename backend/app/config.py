from typing import List, Optional
from pathlib import Path
import os
import json

from pydantic import Field, model_validator
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
    S3_BUCKET_NAME: str = "schoolsharthi-notes"
    
    # Local File Storage (fallback when S3 is not configured)
    USE_LOCAL_STORAGE: bool = True  # Set to False to require S3
    LOCAL_STORAGE_PATH: str = "uploads"  # Directory for local file storage
    API_BASE_URL: str = "http://localhost:8000"  # Base URL for serving local files

    # AI API Keys
    OPENAI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    
    # CORS - Store as string to avoid pydantic-settings auto-parsing issues
    # Will be converted to List[str] in model_validator
    cors_origins_env: Optional[str] = Field(
        default=None,
        alias="CORS_ORIGINS",
        description="Comma-separated or JSON array string of allowed CORS origins"
    )
    
    # Actual CORS_ORIGINS list (computed from cors_origins_env)
    CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "https://schoolsharthi.vercel.app",
        ]
    )

    # Environment
    ENVIRONMENT: str = "development"  # development, staging, production

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        populate_by_name=True,  # Allow both field name and alias
    )

    @model_validator(mode="after")
    def parse_cors_origins(self):
        """Parse CORS origins from string after model initialization."""
        default_origins = [
            "http://localhost:3000",
            "https://schoolsharthi.vercel.app",
        ]
        
        # Parse from cors_origins_env if set
        if self.cors_origins_env:
            self.CORS_ORIGINS = self._parse_cors_string(self.cors_origins_env)
        elif os.getenv("CORS_ORIGINS"):
            # Fallback: parse directly from environment
            self.CORS_ORIGINS = self._parse_cors_string(os.getenv("CORS_ORIGINS"))
        else:
            # Use defaults
            self.CORS_ORIGINS = default_origins
        
        return self
    
    @staticmethod
    def _parse_cors_string(value: str) -> List[str]:
        """Parse CORS origins from string (comma-separated or JSON)."""
        default_origins = [
            "http://localhost:3000",
            "https://schoolsharthi.vercel.app",
        ]
        
        if not value or not isinstance(value, str):
            return default_origins
        
        value = value.strip()
        
        # Handle empty string
        if not value:
            return default_origins
        
        # Handle JSON array format: ["url1", "url2"]
        if value.startswith("[") and value.endswith("]"):
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    origins = [origin.strip() for origin in parsed if origin and origin.strip()]
                    return origins if origins else default_origins
            except (json.JSONDecodeError, TypeError, ValueError):
                # If JSON parsing fails, fall through to comma-separated parsing
                pass
        
        # Handle comma-separated string: "url1,url2"
        origins = [origin.strip() for origin in value.split(",") if origin.strip()]
        return origins if origins else default_origins


# Auto load .env
env_path = Path(".env")
if not env_path.exists():
    env_path = Path(__file__).parent.parent / ".env"

if env_path.exists():
    settings = Settings(_env_file=str(env_path))
    print(f"✅ Loaded .env from: {env_path}")
else:
    settings = Settings()
    print("⚠️ .env file not found, using system env vars")

# Ensure CORS_ORIGINS is set (model_validator should handle this, but double-check)
if not settings.CORS_ORIGINS or (os.getenv("CORS_ORIGINS") and settings.cors_origins_env != os.getenv("CORS_ORIGINS")):
    if os.getenv("CORS_ORIGINS"):
        settings.CORS_ORIGINS = Settings._parse_cors_string(os.getenv("CORS_ORIGINS"))

# Set environment
if os.getenv("ENVIRONMENT"):
    settings.ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Debug: Print CORS configuration
print(f"🌐 CORS Origins: {settings.CORS_ORIGINS}")
