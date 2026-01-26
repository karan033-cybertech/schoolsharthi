from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Note, PYQ, User
from app.schemas import NoteCreate, NoteResponse, PYQCreate, PYQResponse
from app.auth import get_current_admin_user
from app.services.supabase_storage_service import upload_file_to_supabase
from app.models import ClassLevel, Subject, ExamType

router = APIRouter()


@router.post("/notes/upload", response_model=NoteResponse)
async def upload_note(
    title: str = Form(...),
    class_level: str = Form(...),
    subject: str = Form(...),
    chapter: str = Form(...),
    description: str = Form(None),
    file: UploadFile = File(...),
    thumbnail: UploadFile = File(None),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    # Log received values for debugging
    print(f"📝 Upload Note Request:")
    print(f"   Title: {title}")
    print(f"   Class Level: {class_level} (type: {type(class_level)})")
    print(f"   Subject: {subject} (type: {type(subject)})")
    print(f"   Chapter: {chapter}")
    
    # Validate and convert enum types
    # Normalize subject to lowercase for enum matching
    subject_normalized = subject.lower().strip() if subject else ""
    print(f"   Subject normalized: '{subject_normalized}'")
    
    try:
        class_level_enum = ClassLevel(class_level)
        print(f"   ✅ Class level validated: {class_level_enum}")
    except ValueError as e:
        print(f"   ❌ Class level validation failed: {e}")
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid class_level: '{class_level}'. Valid values: {[c.value for c in ClassLevel]}"
        )
    
    try:
        subject_enum = Subject(subject_normalized)
        print(f"   ✅ Subject validated: {subject_enum}")
    except ValueError as e:
        print(f"   ❌ Subject validation failed: {e}")
        print(f"   Available subjects: {[s.value for s in Subject]}")
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid subject: '{subject}'. Valid values: {[s.value for s in Subject]}. Received (normalized): '{subject_normalized}'"
        )
    
    # Upload file to Supabase Storage
    try:
        print(f"   📤 Uploading file to Supabase...")
        file_url = await upload_file_to_supabase(file, f"notes/{class_level}/{subject}/{chapter}/")
        print(f"   ✅ File uploaded successfully: {file_url}")
    except ValueError as e:
        print(f"   ❌ File upload failed: {e}")
        raise HTTPException(status_code=503, detail=f"File upload failed: {str(e)}")
    except Exception as e:
        print(f"   ❌ Unexpected error during file upload: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=503, detail=f"File upload error: {str(e)}")
    
    thumbnail_url = None
    if thumbnail:
        try:
            print(f"   📤 Uploading thumbnail to Supabase...")
            thumbnail_url = await upload_file_to_supabase(thumbnail, f"thumbnails/{class_level}/{subject}/{chapter}/")
            print(f"   ✅ Thumbnail uploaded successfully: {thumbnail_url}")
        except ValueError as e:
            print(f"   ❌ Thumbnail upload failed: {e}")
            raise HTTPException(status_code=503, detail=f"Thumbnail upload failed: {str(e)}")
        except Exception as e:
            print(f"   ❌ Unexpected error during thumbnail upload: {e}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=503, detail=f"Thumbnail upload error: {str(e)}")
    
    # Create note record
    # Use enum values (not enum objects) to ensure correct database storage
    note = Note(
        title=title,
        class_level=class_level_enum.value,  # Use .value to get the string value
        subject=subject_enum.value,  # Use .value to get the string value (e.g., "science" not "SCIENCE")
        chapter=chapter,
        description=description,
        file_url=file_url,
        thumbnail_url=thumbnail_url,
        uploaded_by=current_user.id,
        is_approved=True  # Auto-approve for admin
    )
    
    db.add(note)
    db.commit()
    db.refresh(note)
    
    return note


@router.post("/pyqs/upload", response_model=PYQResponse)
async def upload_pyq(
    title: str = Form(...),
    exam_type: str = Form(...),
    year: int = Form(...),
    class_level: str = Form(None),
    subject: str = Form(None),
    question_paper: UploadFile = File(None),
    answer_key: UploadFile = File(None),
    solution: UploadFile = File(None),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    # Validate and convert enum types
    try:
        exam_type_enum = ExamType(exam_type)
    except ValueError as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid exam_type: '{exam_type}'. Valid values: {[e.value for e in ExamType]}"
        )
    
    class_level_enum = None
    if class_level:
        try:
            class_level_enum = ClassLevel(class_level)
        except ValueError as e:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid class_level: '{class_level}'. Valid values: {[c.value for c in ClassLevel]}"
            )
    
    subject_enum = None
    if subject:
        # Normalize subject to lowercase for enum matching
        subject_normalized = subject.lower().strip()
        try:
            subject_enum = Subject(subject_normalized)
        except ValueError as e:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid subject: '{subject}'. Valid values: {[s.value for s in Subject]}. Received (normalized): '{subject_normalized}'"
            )
    
    question_paper_url = None
    answer_key_url = None
    solution_url = None
    
    try:
        if question_paper:
            question_paper_url = await upload_file_to_supabase(
                question_paper, f"pyqs/{exam_type}/{year}/"
            )
        if answer_key:
            answer_key_url = await upload_file_to_supabase(
                answer_key, f"pyqs/{exam_type}/{year}/"
            )
        if solution:
            solution_url = await upload_file_to_supabase(
                solution, f"pyqs/{exam_type}/{year}/"
            )
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    
    pyq = PYQ(
        title=title,
        exam_type=exam_type_enum.value,  # Use .value to get the string value
        year=year,
        class_level=class_level_enum.value if class_level_enum else None,  # Use .value if not None
        subject=subject_enum.value if subject_enum else None,  # Use .value if not None
        question_paper_url=question_paper_url,
        answer_key_url=answer_key_url,
        solution_url=solution_url,
        uploaded_by=current_user.id,
        is_approved=True
    )
    
    db.add(pyq)
    db.commit()
    db.refresh(pyq)
    
    return pyq


@router.get("/notes/pending", response_model=List[NoteResponse])
def get_pending_notes(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    notes = db.query(Note).filter(Note.is_approved == False).offset(skip).limit(limit).all()
    return notes


@router.post("/notes/{note_id}/approve")
def approve_note(
    note_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    note.is_approved = True
    db.commit()
    db.refresh(note)
    
    return {"message": "Note approved successfully"}


@router.delete("/notes/{note_id}")
def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(note)
    db.commit()
    
    return {"message": "Note deleted successfully"}


@router.get("/notes/all", response_model=List[NoteResponse])
def get_all_notes(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    notes = db.query(Note).order_by(Note.created_at.desc()).offset(skip).limit(limit).all()
    return notes


@router.get("/pyqs/all", response_model=List[PYQResponse])
def get_all_pyqs(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    pyqs = db.query(PYQ).order_by(PYQ.created_at.desc()).offset(skip).limit(limit).all()
    return pyqs


@router.delete("/pyqs/{pyq_id}")
def delete_pyq(
    pyq_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    pyq = db.query(PYQ).filter(PYQ.id == pyq_id).first()
    if not pyq:
        raise HTTPException(status_code=404, detail="PYQ not found")
    
    db.delete(pyq)
    db.commit()
    
    return {"message": "PYQ deleted successfully"}


@router.post("/pyqs/{pyq_id}/approve")
def approve_pyq(
    pyq_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    pyq = db.query(PYQ).filter(PYQ.id == pyq_id).first()
    if not pyq:
        raise HTTPException(status_code=404, detail="PYQ not found")
    
    pyq.is_approved = True
    db.commit()
    db.refresh(pyq)
    
    return {"message": "PYQ approved successfully"}


@router.get("/users/all")
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    users = db.query(User).order_by(User.created_at.desc()).offset(skip).limit(limit).all()
    return users


@router.post("/users/{user_id}/toggle-active")
def toggle_user_active(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot deactivate yourself")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = not user.is_active
    db.commit()
    db.refresh(user)
    
    return {"message": f"User {'activated' if user.is_active else 'deactivated'} successfully", "user": user}


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete related records first to avoid foreign key constraint errors
    from app.models import Doubt, CareerQuery, Note, PYQ
    
    # Delete user's doubts
    db.query(Doubt).filter(Doubt.user_id == user_id).delete()
    
    # Delete user's career queries
    db.query(CareerQuery).filter(CareerQuery.user_id == user_id).delete()
    
    # Delete user's notes (optional - you might want to keep notes but remove uploader reference)
    # db.query(Note).filter(Note.uploaded_by == user_id).delete()
    
    # Delete user's PYQs (optional - you might want to keep PYQs but remove uploader reference)
    # db.query(PYQ).filter(PYQ.uploaded_by == user_id).delete()
    
    # Now delete the user
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}


@router.post("/users/{user_id}/make-admin")
def make_user_admin(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    from app.models import UserRole
    user.role = UserRole.ADMIN
    db.commit()
    db.refresh(user)
    
    return {"message": "User promoted to admin successfully", "user": user}


@router.post("/settings/ai-key")
def update_ai_key(
    api_key: str = Form(...),
    provider: str = Form("groq"),  # "groq" or "openai"
    current_user: User = Depends(get_current_admin_user),
):
    from app.config import settings
    import os
    from pathlib import Path
    
    # Find .env file
    env_file = Path(".env")
    if not env_file.exists():
        env_file = Path(__file__).parent.parent / ".env"
    
    key_name = "GROQ_API_KEY" if provider == "groq" else "OPENAI_API_KEY"
    
    # Update or create .env file
    if env_file.exists():
        # Read current .env
        content = env_file.read_text()
        
        # Update or add API key
        lines = content.split("\n")
        new_lines = []
        key_found = False
        for line in lines:
            if line.startswith(f"{key_name}="):
                new_lines.append(f"{key_name}={api_key}")
                key_found = True
            elif line.startswith("GROQ_API_KEY=") or line.startswith("OPENAI_API_KEY="):
                # Keep other provider's key
                new_lines.append(line)
            elif line.strip():  # Keep non-empty lines
                new_lines.append(line)
        
        if not key_found:
            new_lines.append(f"{key_name}={api_key}")
        
        env_file.write_text("\n".join(new_lines))
    else:
        # Create new .env file
        env_file.write_text(f"{key_name}={api_key}\n")
    
    # Update environment variable
    os.environ[key_name] = api_key
    
    # Update settings object directly
    if provider == "groq":
        settings.GROQ_API_KEY = api_key
    else:
        settings.OPENAI_API_KEY = api_key
    
    # Try to reload AI client
    try:
        from app.services.ai_service import initialize_ai_client
        success = initialize_ai_client()
        if success:
            return {"message": f"✅ {provider.upper()} API key updated and AI client reloaded successfully! Ready to use."}
        else:
            return {"message": f"⚠️ {provider.upper()} API key saved but client initialization failed. Please check the API key and restart server."}
    except Exception as e:
        return {"message": f"⚠️ {provider.upper()} API key saved. Error reloading client: {str(e)}. Please restart server."}


@router.get("/settings/ai-key")
def get_ai_key_status(
    current_user: User = Depends(get_current_admin_user),
):
    from app.config import settings
    
    has_groq = bool(settings.GROQ_API_KEY)
    has_openai = bool(settings.OPENAI_API_KEY)
    
    groq_preview = None
    if has_groq:
        groq_preview = settings.GROQ_API_KEY[:10] + "..." if len(settings.GROQ_API_KEY) > 10 else "***"
    
    openai_preview = None
    if has_openai:
        openai_preview = settings.OPENAI_API_KEY[:10] + "..." if len(settings.OPENAI_API_KEY) > 10 else "***"
    
    return {
        "has_groq": has_groq,
        "has_openai": has_openai,
        "groq_preview": groq_preview,
        "openai_preview": openai_preview,
        "configured": has_groq or has_openai,
        "provider": "groq" if has_groq else ("openai" if has_openai else None)
    }
