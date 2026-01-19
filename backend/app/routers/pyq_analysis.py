"""
PYQ Analysis API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ExamType, Subject
from app.auth import get_current_active_user
from app.services.pyq_analyzer import PYQAnalyzer
from typing import Optional, List
from pydantic import BaseModel

router = APIRouter()


class MockTestRequest(BaseModel):
    exam_type: ExamType
    subject: Optional[Subject] = None
    num_questions: int = 30
    difficulty: str = "mixed"


@router.get("/repeated-questions")
def get_repeated_questions(
    exam_type: ExamType = Query(...),
    subject: Optional[Subject] = Query(None),
    years: Optional[str] = Query(None, description="Comma-separated years, e.g., '2020,2021,2022'"),
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Detect repeated questions across years"""
    try:
        year_list = [int(y.strip()) for y in years.split(',')] if years else None
        analyzer = PYQAnalyzer(db)
        result = analyzer.detect_repeated_questions(exam_type, subject, year_list)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing repeated questions: {str(e)}")


@router.get("/important-chapters")
def get_important_chapters(
    exam_type: ExamType = Query(...),
    subject: Optional[Subject] = Query(None),
    years: Optional[str] = Query(None),
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Find important chapters based on PYQ frequency"""
    try:
        year_list = [int(y.strip()) for y in years.split(',')] if years else None
        analyzer = PYQAnalyzer(db)
        result = analyzer.find_important_chapters(exam_type, subject, year_list)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding important chapters: {str(e)}")


@router.get("/weightage-prediction")
def get_weightage_prediction(
    exam_type: ExamType = Query(...),
    subject: Optional[Subject] = Query(None),
    years: Optional[str] = Query(None),
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Predict topic weightage based on historical data"""
    try:
        year_list = [int(y.strip()) for y in years.split(',')] if years else None
        analyzer = PYQAnalyzer(db)
        result = analyzer.predict_weightage(exam_type, subject, year_list)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting weightage: {str(e)}")


@router.post("/mock-test")
def generate_mock_test(
    request: MockTestRequest,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Generate mock test based on PYQ patterns"""
    try:
        analyzer = PYQAnalyzer(db)
        result = analyzer.generate_mock_test(
            request.exam_type,
            request.subject,
            request.num_questions,
            request.difficulty
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating mock test: {str(e)}")


@router.get("/full-analysis")
def get_full_analysis(
    exam_type: ExamType = Query(...),
    subject: Optional[Subject] = Query(None),
    years: Optional[str] = Query(None),
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get complete PYQ analysis"""
    try:
        year_list = [int(y.strip()) for y in years.split(',')] if years else None
        analyzer = PYQAnalyzer(db)
        
        return {
            'repeated_questions': analyzer.detect_repeated_questions(exam_type, subject, year_list),
            'important_chapters': analyzer.find_important_chapters(exam_type, subject, year_list),
            'weightage_prediction': analyzer.predict_weightage(exam_type, subject, year_list),
            'summary': {
                'exam_type': exam_type.value,
                'subject': subject.value if subject else 'All',
                'years_analyzed': year_list or 'All available years'
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing analysis: {str(e)}")
