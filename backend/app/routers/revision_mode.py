"""
Smart Revision Mode Router
Generates comprehensive revision packs for exam preparation
"""
from fastapi import APIRouter, Depends, HTTPException
from app.models import User, Subject, ClassLevel
from app.auth import get_current_active_user
from app.services.revision_service import generate_revision_pack
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class RevisionRequest(BaseModel):
    query: str  # e.g., "Kal exam hai science ka" or "Tomorrow physics exam"
    subject: Optional[Subject] = None
    class_level: Optional[ClassLevel] = None
    language: Optional[str] = None  # 'hindi', 'hinglish', 'english'


class RevisionResponse(BaseModel):
    revision_notes: str
    formulas: str
    rapid_fire_questions: str
    common_mistakes: str
    quick_tips: str
    full_response: str
    subject: str
    class_level: str
    urgency: str
    language: str


@router.post("/generate", response_model=RevisionResponse)
async def generate_revision(
    request: RevisionRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Generate comprehensive revision pack for exam preparation
    
    Auto-detects:
    - Subject from query
    - Exam urgency (tomorrow, soon, normal)
    - Language (Hindi/Hinglish/English)
    
    Returns:
    - One-page revision notes
    - Important formulas
    - 20 rapid-fire questions
    - 5 common mistakes
    - Quick tips
    """
    try:
        # Validate language
        if request.language and request.language not in ['hindi', 'hinglish', 'english']:
            request.language = None  # Auto-detect instead
        
        revision_pack = await generate_revision_pack(
            query=request.query,
            subject=request.subject,
            class_level=request.class_level,
            language=request.language
        )
        
        return revision_pack
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating revision pack: {str(e)}")


@router.get("/quick")
async def quick_revision(
    subject: str,
    class_level: Optional[str] = None,
    language: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
):
    """
    Quick revision endpoint - simpler interface
    Example: /api/revision/quick?subject=physics&class_level=11
    """
    try:
        # Convert string to enum if valid
        subject_enum = None
        class_enum = None
        
        try:
            subject_enum = Subject[subject.upper()]
        except (KeyError, AttributeError):
            pass
        
        try:
            if class_level:
                class_attr = f"CLASS_{class_level}"
                class_enum = getattr(ClassLevel, class_attr) if hasattr(ClassLevel, class_attr) else None
        except (AttributeError, ValueError):
            pass
        
        query = f"{subject} revision"
        if class_level:
            query += f" class {class_level}"
        
        revision_pack = await generate_revision_pack(
            query=query,
            subject=subject_enum,
            class_level=class_enum,
            language=language
        )
        
        return revision_pack
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating revision: {str(e)}")
