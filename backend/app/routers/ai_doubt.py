from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Doubt, User
from app.schemas import (
    DoubtCreate, DoubtResponse,
    ImportantQuestionsRequest, ImportantQuestionsResponse,
    PYQPatternRequest, PYQPatternResponse,
    StepByStepSolutionRequest, StepByStepSolutionResponse
)
from app.auth import get_current_active_user
from app.services.ai_service import (
    solve_doubt,
    generate_important_questions,
    find_pyq_patterns,
    get_step_by_step_solution,
    detect_language
)

router = APIRouter()


# ============================================================
# 🧠 AI Doubt Solver (Language Aware)
# ============================================================

@router.post("/doubt", response_model=DoubtResponse)
async def ask_doubt(
    doubt: DoubtCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Detect language from question
    detected_lang = detect_language(doubt.question)

    # Save doubt
    db_doubt = Doubt(
        user_id=current_user.id,
        question=doubt.question,
        subject=doubt.subject,
        class_level=doubt.class_level,
        chapter=getattr(doubt, 'chapter', None),
        detected_language=detected_lang
    )
    db.add(db_doubt)
    db.commit()
    db.refresh(db_doubt)

    # Get AI response
    try:
        ai_response = await solve_doubt(
            doubt.question,
            doubt.subject,
            doubt.class_level,
            getattr(doubt, 'chapter', None),
            target_language=detected_lang
        )

        if ai_response:
            db_doubt.ai_response = ai_response
            db_doubt.is_resolved = True
        else:
            db_doubt.ai_response = "AI service is not configured properly."

        db.commit()
        db.refresh(db_doubt)

    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        print(f"AI service error ({error_type}): {error_msg}")

        db_doubt.ai_response = f"Error generating AI response: {error_msg}"
        db.commit()
        db.refresh(db_doubt)

    return db_doubt


# ============================================================
# 📚 Important Questions Generator
# ============================================================

@router.post("/important-questions", response_model=ImportantQuestionsResponse)
async def get_important_questions(
    request: ImportantQuestionsRequest,
    current_user: User = Depends(get_current_active_user)
):
    try:
        questions = await generate_important_questions(
            request.subject,
            request.class_level,
            request.chapter,
            request.count or 10
        )
        return ImportantQuestionsResponse(
            questions=questions,
            subject=request.subject,
            class_level=request.class_level,
            chapter=request.chapter
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# 📊 PYQ Pattern Finder
# ============================================================

@router.post("/pyq-patterns", response_model=PYQPatternResponse)
async def get_pyq_patterns(
    request: PYQPatternRequest,
    current_user: User = Depends(get_current_active_user)
):
    try:
        patterns = await find_pyq_patterns(
            request.exam_type.value,
            request.subject,
            request.year_range
        )
        return PYQPatternResponse(
            patterns=patterns,
            exam_type=request.exam_type,
            subject=request.subject
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# 📝 Step-by-Step Solver
# ============================================================

@router.post("/step-by-step", response_model=StepByStepSolutionResponse)
async def get_step_by_step(
    request: StepByStepSolutionRequest,
    current_user: User = Depends(get_current_active_user)
):
    try:
        solution = await get_step_by_step_solution(
            request.problem,
            request.subject
        )
        return StepByStepSolutionResponse(
            solution=solution,
            problem=request.problem
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# 📜 User Doubts History
# ============================================================

@router.get("/doubts", response_model=List[DoubtResponse])
def get_user_doubts(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    doubts = (
        db.query(Doubt)
        .filter(Doubt.user_id == current_user.id)
        .order_by(Doubt.created_at.desc())
        .all()
    )
    return doubts


@router.get("/doubts/{doubt_id}", response_model=DoubtResponse)
def get_doubt(
    doubt_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    doubt = (
        db.query(Doubt)
        .filter(Doubt.id == doubt_id, Doubt.user_id == current_user.id)
        .first()
    )
    if not doubt:
        raise HTTPException(status_code=404, detail="Doubt not found")

    return doubt
