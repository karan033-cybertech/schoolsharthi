from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from sqlalchemy import text

from app.routers import (
    auth, notes, pyqs, admin, ai_doubt, career_guidance,
    pyq_analysis, adaptive_learning, revision_mode, smart_search, exam_mode
)

from app.database import engine
from app.config import settings
from app.services.ai_service import initialize_ai_client
from app.database_migrations import sync_database_schema
from app.middleware import SecurityHeadersMiddleware, RequestLoggingMiddleware


# ---------------- INIT ----------------

print("🚀 Starting SchoolSharthi Backend...")

# Sync DB
sync_database_schema()

# Init AI
initialize_ai_client()

# Create uploads folder
if settings.USE_LOCAL_STORAGE:
    Path(settings.LOCAL_STORAGE_PATH).mkdir(parents=True, exist_ok=True)

# ---------------- APP ----------------

app = FastAPI(
    title="SchoolSharthi API",
    description="Indian Education Platform API",
    version="1.0.0"
)

# ---------------- CORS ----------------


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list(),   # 👈 now always list
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- MIDDLEWARE ----------------

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

# ---------------- ROUTERS ----------------

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(notes.router, prefix="/api/notes", tags=["Notes"])
app.include_router(pyqs.router, prefix="/api/pyqs", tags=["PYQs"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(ai_doubt.router, prefix="/api/ai", tags=["AI"])
app.include_router(career_guidance.router, prefix="/api/career", tags=["Career"])
app.include_router(pyq_analysis.router, prefix="/api/pyq-analysis", tags=["PYQ Analysis"])
app.include_router(adaptive_learning.router, prefix="/api/learning", tags=["Learning"])
app.include_router(revision_mode.router, prefix="/api/revision", tags=["Revision"])
app.include_router(smart_search.router, prefix="/api/search", tags=["Search"])
app.include_router(exam_mode.router, prefix="/api/exam", tags=["Exam"])

# ---------------- ROUTES ----------------

@app.get("/")
def root():
    return {"message": "SchoolSharthi API is running 🚀"}


@app.get("/health")
def health_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = str(e)

    return {
        "status": "ok",
        "database": db_status,
        "environment": settings.ENVIRONMENT,
        "cors_origins": settings.CORS_ORIGINS
    }


@app.get("/api/files/{file_path:path}")
def serve_file(file_path: str):
    """
    Serve files from local storage.
    Security: Prevents directory traversal attacks.
    """
    # Security: Prevent directory traversal
    if ".." in file_path or file_path.startswith("/"):
        raise HTTPException(status_code=400, detail="Invalid path")
    
    # Normalize path separators
    file_path = file_path.replace("\\", "/")
    
    # Construct full path
    full_path = Path(settings.LOCAL_STORAGE_PATH) / file_path
    
    # Security: Ensure the resolved path is within the storage directory
    try:
        full_path = full_path.resolve()
        storage_path = Path(settings.LOCAL_STORAGE_PATH).resolve()
        if not str(full_path).startswith(str(storage_path)):
            raise HTTPException(status_code=403, detail="Access denied")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid path")

    if not full_path.exists() or not full_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    # Determine content type based on file extension
    content_type = "application/octet-stream"
    if file_path.endswith(".pdf"):
        content_type = "application/pdf"
    elif file_path.endswith((".jpg", ".jpeg")):
        content_type = "image/jpeg"
    elif file_path.endswith(".png"):
        content_type = "image/png"
    
    return FileResponse(
        full_path,
        media_type=content_type,
        filename=full_path.name,
        headers={
            "Content-Disposition": f'inline; filename="{full_path.name}"',
            "Cache-Control": "public, max-age=3600"  # Cache for 1 hour
        }
    )
