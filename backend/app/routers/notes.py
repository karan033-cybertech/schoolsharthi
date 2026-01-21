from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Note, User, ClassLevel, Subject
from app.schemas import NoteResponse
from app.auth import get_current_active_user
from app.utils.url_rewrite import rewrite_file_url

router = APIRouter()


@router.get("/", response_model=List[NoteResponse])
def get_notes(
    class_level: Optional[str] = Query(None),
    subject: Optional[str] = Query(None),
    chapter: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Note).filter(Note.is_approved == True)
    
    # Parse and validate enum values only if provided and not empty
    if class_level and class_level.strip():
        try:
            class_level_enum = ClassLevel(class_level)
            query = query.filter(Note.class_level == class_level_enum)
        except ValueError:
            pass  # Ignore invalid enum values
    
    if subject and subject.strip():
        try:
            subject_enum = Subject(subject)
            query = query.filter(Note.subject == subject_enum)
        except ValueError:
            pass  # Ignore invalid enum values
    
    if chapter and chapter.strip():
        query = query.filter(Note.chapter.ilike(f"%{chapter}%"))
    
    notes = query.order_by(Note.created_at.desc()).offset(skip).limit(limit).all()
    
    # Rewrite localhost URLs to current BASE_URL
    for note in notes:
        if note.file_url:
            note.file_url = rewrite_file_url(note.file_url)
        if note.thumbnail_url:
            note.thumbnail_url = rewrite_file_url(note.thumbnail_url)
    
    return notes


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id, Note.is_approved == True).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # Increment view count
    note.views_count += 1
    db.commit()
    db.refresh(note)
    
    # Rewrite localhost URLs to current BASE_URL
    if note.file_url:
        note.file_url = rewrite_file_url(note.file_url)
    if note.thumbnail_url:
        note.thumbnail_url = rewrite_file_url(note.thumbnail_url)
    
    return note


@router.post("/{note_id}/download")
def download_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id, Note.is_approved == True).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # Check if file URL is valid (not a placeholder)
    if not note.file_url or "placeholder.com" in note.file_url:
        raise HTTPException(
            status_code=503,
            detail="File is not available. The note was uploaded before storage was configured. "
                   "Please contact an administrator to re-upload this note."
        )
    
    # Increment download count
    note.download_count += 1
    db.commit()
    
    # Rewrite localhost URL to current BASE_URL
    file_url = rewrite_file_url(note.file_url) if note.file_url else None
    
    return {"file_url": file_url}
