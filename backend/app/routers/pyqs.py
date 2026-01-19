from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import PYQ, ExamType, ClassLevel, Subject
from app.schemas import PYQResponse

router = APIRouter()


@router.get("/", response_model=List[PYQResponse])
def get_pyqs(
    exam_type: Optional[ExamType] = Query(None),
    class_level: Optional[ClassLevel] = Query(None),
    subject: Optional[Subject] = Query(None),
    year: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(PYQ).filter(PYQ.is_approved == True)
    
    if exam_type:
        query = query.filter(PYQ.exam_type == exam_type)
    if class_level:
        query = query.filter(PYQ.class_level == class_level)
    if subject:
        query = query.filter(PYQ.subject == subject)
    if year:
        query = query.filter(PYQ.year == year)
    
    pyqs = query.order_by(PYQ.year.desc(), PYQ.created_at.desc()).offset(skip).limit(limit).all()
    return pyqs


@router.get("/{pyq_id}", response_model=PYQResponse)
def get_pyq(pyq_id: int, db: Session = Depends(get_db)):
    pyq = db.query(PYQ).filter(PYQ.id == pyq_id, PYQ.is_approved == True).first()
    if not pyq:
        raise HTTPException(status_code=404, detail="PYQ not found")
    
    # Increment view count
    pyq.views_count += 1
    db.commit()
    db.refresh(pyq)
    
    return pyq


@router.post("/{pyq_id}/download")
def download_pyq(pyq_id: int, db: Session = Depends(get_db)):
    pyq = db.query(PYQ).filter(PYQ.id == pyq_id, PYQ.is_approved == True).first()
    if not pyq:
        raise HTTPException(status_code=404, detail="PYQ not found")
    
    # Check if any file URL is valid (not a placeholder)
    urls = {
        "question_paper_url": pyq.question_paper_url,
        "answer_key_url": pyq.answer_key_url,
        "solution_url": pyq.solution_url
    }
    
    # Check for placeholder URLs
    for key, url in urls.items():
        if url and "placeholder.com" in url:
            raise HTTPException(
                status_code=503,
                detail=f"File is not available. The {key.replace('_', ' ')} was uploaded before S3 storage was configured. "
                       "Please contact an administrator to re-upload this PYQ."
            )
    
    # If no question paper URL is available, return error
    if not pyq.question_paper_url:
        raise HTTPException(
            status_code=503,
            detail="No files are available for this PYQ. Please contact an administrator."
        )
    
    # Increment download count
    pyq.download_count += 1
    db.commit()
    
    return urls
