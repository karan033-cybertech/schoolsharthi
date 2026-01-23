from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import PYQ, ExamType, ClassLevel, Subject
from app.schemas import PYQResponse
from app.utils.url_rewrite import rewrite_file_url

router = APIRouter()


def parse_enum(enum_cls, value: Optional[str]):
    """
    Converts string to Enum safely (case-insensitive).
    Example: physics -> Subject.PHYSICS
    """
    if not value:
        return None
    try:
        return enum_cls(value.upper())
    except Exception:
        return None


@router.get("/", response_model=List[PYQResponse])
def get_pyqs(
    exam_type: Optional[str] = Query(None),
    class_level: Optional[str] = Query(None),
    subject: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(PYQ).filter(PYQ.is_approved == True)

    # ✅ FIXED: string → enum safely
    exam_enum = parse_enum(ExamType, exam_type)
    class_enum = parse_enum(ClassLevel, class_level)
    subject_enum = parse_enum(Subject, subject)

    if exam_enum:
        query = query.filter(PYQ.exam_type == exam_enum)

    if class_enum:
        query = query.filter(PYQ.class_level == class_enum)

    if subject_enum:
        query = query.filter(PYQ.subject == subject_enum)

    if year:
        query = query.filter(PYQ.year == year)

    pyqs = (
        query
        .order_by(PYQ.year.desc(), PYQ.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    # Rewrite URLs
    for pyq in pyqs:
        if pyq.question_paper_url:
            pyq.question_paper_url = rewrite_file_url(pyq.question_paper_url)
        if pyq.answer_key_url:
            pyq.answer_key_url = rewrite_file_url(pyq.answer_key_url)
        if pyq.solution_url:
            pyq.solution_url = rewrite_file_url(pyq.solution_url)

    return pyqs
