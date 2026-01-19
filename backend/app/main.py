from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pathlib import Path
from app.routers import auth, notes, pyqs, admin, ai_doubt, career_guidance, pyq_analysis, adaptive_learning, revision_mode, smart_search, exam_mode
from app.database import engine, Base
from app.config import settings
from app.services.ai_service import initialize_ai_client
from app.database_migrations import sync_database_schema
from app.middleware import SecurityHeadersMiddleware, RequestLoggingMiddleware
from sqlalchemy import text

# Sync database schema (creates tables and applies migrations)
sync_database_schema()

# Check AI configuration on startup and auto-initialize
def check_ai_config():
    print("\n" + "="*60)
    print("🔍 Checking AI Configuration...")
    print("="*60)
    if settings.GROQ_API_KEY:
        print(f"✅ Groq API key found (Length: {len(settings.GROQ_API_KEY)} chars)")
    elif settings.OPENAI_API_KEY:
        print(f"✅ OpenAI API key found (Length: {len(settings.OPENAI_API_KEY)} chars)")
    else:
        print("⚠️  No AI API key configured!")
        print("   AI features will use placeholder responses.")
        print("   To fix: Add GROQ_API_KEY or OPENAI_API_KEY to .env file")
        print("   Or use Admin Panel → AI Settings to configure")
    
    # Auto-initialize AI client
    print("\n🔄 Initializing AI client...")
    ai_initialized = initialize_ai_client()
    if ai_initialized:
        print("✅ AI client ready!")
    else:
        print("⚠️  AI client not initialized - features will use placeholders")
    print("="*60 + "\n")

check_ai_config()

# Check storage configuration on startup
def check_storage_config():
    print("\n" + "="*60)
    print("🔍 Checking Storage Configuration...")
    print("="*60)
    s3_configured = bool(settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY and settings.S3_BUCKET_NAME)
    
    if s3_configured:
        print(f"✅ S3 storage configured (Bucket: {settings.S3_BUCKET_NAME})")
    elif settings.USE_LOCAL_STORAGE:
        # Create uploads directory if it doesn't exist
        upload_dir = Path(settings.LOCAL_STORAGE_PATH)
        upload_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Local file storage enabled")
        print(f"   Storage path: {upload_dir.absolute()}")
        print(f"   Files will be served at: {settings.API_BASE_URL}/api/files/")
    else:
        print("⚠️  No storage configured!")
        print("   File uploads will fail.")
        print("   To fix: Configure S3 or set USE_LOCAL_STORAGE=true")
    print("="*60 + "\n")

check_storage_config()

# Check CORS configuration on startup
def check_cors_config():
    print("\n" + "="*60)
    print("🌐 Checking CORS Configuration...")
    print("="*60)
    print(f"✅ CORS Origins configured: {settings.CORS_ORIGINS}")
    print(f"   Environment: {settings.ENVIRONMENT}")
    if not settings.CORS_ORIGINS:
        print("⚠️  WARNING: No CORS origins configured! Frontend requests will be blocked!")
    print("="*60 + "\n")

check_cors_config()

app = FastAPI(
    title="SchoolSharthi API",
    description="Indian Education Platform API",
    version="1.0.0"
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware MUST be added FIRST (executes last in request pipeline)
# This ensures CORS headers are added after all other processing
# FastAPI middleware executes in reverse order (last added = first executed)
# So CORS should be added first to execute last and add headers to all responses
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # List of allowed origins
    allow_credentials=True,  # Allow cookies/auth headers
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],  # Include HEAD for preflight
    allow_headers=["*"],  # Allow all headers (Authorization, Content-Type, etc.)
    expose_headers=["*"],  # Expose all headers to frontend
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Security and logging middleware (added after CORS, so they execute first)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(notes.router, prefix="/api/notes", tags=["Notes"])
app.include_router(pyqs.router, prefix="/api/pyqs", tags=["PYQs"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(ai_doubt.router, prefix="/api/ai", tags=["AI Doubt Solver"])
app.include_router(career_guidance.router, prefix="/api/career", tags=["Career Guidance"])
app.include_router(pyq_analysis.router, prefix="/api/pyq-analysis", tags=["PYQ Analysis"])
app.include_router(adaptive_learning.router, prefix="/api/learning", tags=["Adaptive Learning"])
app.include_router(revision_mode.router, prefix="/api/revision", tags=["Smart Revision Mode"])
app.include_router(smart_search.router, prefix="/api/search", tags=["Smart Search"])
app.include_router(exam_mode.router, prefix="/api/exam", tags=["Exam Mode"])


@app.get("/")
async def root():
    return {"message": "SchoolSharthi API is running"}


@app.get("/health")
async def health_check():
    """Enhanced health check endpoint"""
    try:
        # Check database connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "database": db_status,
        "environment": settings.ENVIRONMENT,
        "cors_origins": settings.CORS_ORIGINS,  # Debug: show CORS config
    }


@app.get("/api/cors-test")
async def cors_test():
    """Test endpoint to verify CORS is working"""
    return {
        "message": "CORS is working!",
        "cors_origins": settings.CORS_ORIGINS,
        "environment": settings.ENVIRONMENT
    }


@app.get("/api/files/{file_path:path}")
async def serve_file(file_path: str):
    """Serve files from local storage"""
    # Security: prevent directory traversal
    if ".." in file_path or file_path.startswith("/"):
        raise HTTPException(status_code=400, detail="Invalid file path")
    
    file_full_path = Path(settings.LOCAL_STORAGE_PATH) / file_path
    
    # Check if file exists
    if not file_full_path.exists() or not file_full_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Determine media type based on extension
    media_type = "application/octet-stream"
    if file_path.endswith(".pdf"):
        media_type = "application/pdf"
    elif file_path.endswith((".jpg", ".jpeg")):
        media_type = "image/jpeg"
    elif file_path.endswith(".png"):
        media_type = "image/png"
    
    return FileResponse(
        path=file_full_path,
        media_type=media_type,
        filename=file_full_path.name
    )
