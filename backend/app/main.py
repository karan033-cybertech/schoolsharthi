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
    allow_origins=settings.CORS_ORIGINS,
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
    if ".." in file_path:
        raise HTTPException(status_code=400, detail="Invalid path")

    full_path = Path(settings.LOCAL_STORAGE_PATH) / file_path

    if not full_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(full_path)
