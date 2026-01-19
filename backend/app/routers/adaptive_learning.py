"""
Adaptive Learning Router
Provides personalized learning recommendations based on student doubt patterns
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth import get_current_active_user
from app.services.adaptive_learning_service import (
    analyze_student_performance,
    get_student_weak_topics_summary
)
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class PerformanceResponse(BaseModel):
    total_doubts: int
    subjects: dict
    chapters: dict
    weak_topics: list
    recommendations: list
    class_levels: dict


class WeakTopicsSummaryResponse(BaseModel):
    summary: str
    language: str


@router.get("/performance", response_model=PerformanceResponse)
def get_student_performance(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive student performance analysis
    - Total doubts asked
    - Doubt frequency by subject and chapter
    - Weak topics identification
    - Personalized recommendations
    """
    try:
        performance = analyze_student_performance(db, current_user.id)
        return performance
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing performance: {str(e)}")


@router.get("/weak-topics-summary")
def get_weak_topics_summary(
    language: Optional[str] = 'hinglish',
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a personalized summary message about weak topics
    Language options: 'hindi', 'hinglish', 'english'
    """
    try:
        if language not in ['hindi', 'hinglish', 'english']:
            language = 'hinglish'
        
        summary = get_student_weak_topics_summary(db, current_user.id, language)
        return WeakTopicsSummaryResponse(summary=summary, language=language)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")


@router.get("/recommendations")
def get_recommendations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get personalized learning recommendations
    Returns actionable recommendations based on student's doubt patterns
    """
    try:
        performance = analyze_student_performance(db, current_user.id)
        return {
            "recommendations": performance["recommendations"],
            "total_doubts": performance["total_doubts"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")
