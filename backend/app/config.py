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

    # Supabase Storage
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None  # Service role key for storage operations
    SUPABASE_SERVICE_KEY: Optional[str] = None  # Alternative name for service key
    SUPABASE_BUCKET: str = "notes"  # Default bucket name

    # AWS S3 (deprecated - use Supabase Storage instead)
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "ap-south-1"
    S3_BUCKET_NAME: Optional[str] = None

    # Local storage (deprecated - use Supabase Storage instead)
    USE_LOCAL_STORAGE: bool = False  # Disabled by default - use Supabase Storage
    LOCAL_STORAGE_PATH: str = "uploads"
    # Base URL for file serving - MUST be set in production
    # Example: https://api.yourdomain.com or https://your-backend.onrender.com
    BASE_URL: str = Field(
        default="http://localhost:8000",
        description="Base URL of the API server for generating file download URLs"
    )

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
    
    @property
    def API_BASE_URL(self) -> str:
        """Get API base URL, ensuring it doesn't end with a slash"""
        url = self.BASE_URL.rstrip('/')
        # In production, ensure HTTPS is used
        if self.ENVIRONMENT == "production" and url.startswith("http://"):
            print("⚠️  WARNING: BASE_URL uses HTTP in production. Consider using HTTPS for security.")
        return url


# Load settings
settings = Settings()

print("🌐 CORS ORIGINS STRING:", settings.CORS_ORIGINS)
print("🌐 CORS ORIGINS LIST:", settings.cors_list())
print(f"🌐 BASE_URL: {settings.BASE_URL}")
print(f"🌐 API_BASE_URL (for file URLs): {settings.API_BASE_URL}")
if settings.ENVIRONMENT == "production" and not settings.BASE_URL.startswith("https://"):
    print("⚠️  WARNING: BASE_URL should use HTTPS in production!")

# Supabase Storage configuration check
service_key = settings.SUPABASE_SERVICE_KEY or settings.SUPABASE_KEY
if not settings.SUPABASE_URL or not service_key:
    print("⚠️  WARNING: Supabase Storage is not configured!")
    print("   Please set SUPABASE_URL and SUPABASE_KEY (or SUPABASE_SERVICE_KEY) environment variables.")
    print("   File uploads will fail without Supabase Storage configuration.")
else:
    print(f"✅ Supabase Storage configured: {settings.SUPABASE_URL}")
    print(f"   Bucket: {settings.SUPABASE_BUCKET}")
    print(f"   Service key: {'Set' if service_key else 'Not set'}")
