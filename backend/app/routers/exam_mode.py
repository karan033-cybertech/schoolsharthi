"""
Exam Mode Router
Real exam simulation with timer, scoring, and analytics
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Exam, ExamQuestion, ExamAttempt, ExamResult, Subject, ClassLevel, ExamType
from app.auth import get_current_active_user
from app.services.exam_service import (
    create_exam, start_exam, submit_answer, submit_exam,
    analyze_exam_performance
)
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

router = APIRouter()


class CreateExamRequest(BaseModel):
    subject: Optional[Subject] = None
    class_level: Optional[ClassLevel] = None
    exam_type: Optional[ExamType] = None
    duration_minutes: int = 60
    total_questions: int = 30
    difficulty: str = "mixed"  # easy, medium, hard, mixed


class SubmitAnswerRequest(BaseModel):
    question_id: int
    selected_answer: str
    time_spent_seconds: Optional[int] = 0


class ExamResponse(BaseModel):
    id: int
    title: str
    subject: Optional[str]
    class_level: Optional[str]
    exam_type: Optional[str]
    duration_minutes: int
    total_questions: int
    status: str
    started_at: Optional[datetime]
    submitted_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionResponse(BaseModel):
    id: int
    question_number: int
    question_text: str
    options: List[str]
    marks: int
    difficulty: str

    class Config:
        from_attributes = True


class ResultResponse(BaseModel):
    id: int
    exam_id: int
    total_questions: int
    correct_answers: int
    wrong_answers: int
    unanswered: int
    total_marks: int
    obtained_marks: int
    percentage: int
    weak_topics: Optional[Dict]
    performance_analysis: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("/create", response_model=ExamResponse)
def create_new_exam(
    request: CreateExamRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new exam with randomized questions
    """
    try:
        exam = create_exam(
            db=db,
            user_id=current_user.id,
            subject=request.subject,
            class_level=request.class_level,
            exam_type=request.exam_type,
            duration_minutes=request.duration_minutes,
            total_questions=request.total_questions,
            difficulty=request.difficulty
        )
        return exam
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating exam: {str(e)}")


@router.post("/{exam_id}/start", response_model=ExamResponse)
def start_exam_route(
    exam_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Start an exam - sets status to in_progress and records start time
    """
    try:
        # Verify exam belongs to user
        exam = db.query(Exam).filter(Exam.id == exam_id, Exam.user_id == current_user.id).first()
        if not exam:
            raise HTTPException(status_code=404, detail="Exam not found")
        
        exam = start_exam(db, exam_id)
        return exam
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting exam: {str(e)}")


@router.get("/{exam_id}/questions", response_model=List[QuestionResponse])
def get_exam_questions(
    exam_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all questions for an exam
    """
    # Verify exam belongs to user
    exam = db.query(Exam).filter(Exam.id == exam_id, Exam.user_id == current_user.id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    questions = db.query(ExamQuestion).filter(ExamQuestion.exam_id == exam_id).order_by(ExamQuestion.question_number).all()
    
    # Parse options from JSON
    result = []
    import json
    for q in questions:
        options = json.loads(q.options) if q.options else []
        result.append({
            "id": q.id,
            "question_number": q.question_number,
            "question_text": q.question_text,
            "options": options,
            "marks": q.marks,
            "difficulty": q.difficulty
        })
    
    return result


@router.post("/{exam_id}/answer")
def submit_answer_route(
    exam_id: int,
    request: SubmitAnswerRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Submit an answer for a question
    """
    try:
        # Verify exam belongs to user and is in progress
        exam = db.query(Exam).filter(Exam.id == exam_id, Exam.user_id == current_user.id).first()
        if not exam:
            raise HTTPException(status_code=404, detail="Exam not found")
        
        if exam.status != "in_progress":
            raise HTTPException(status_code=400, detail="Exam is not in progress")
        
        attempt = submit_answer(
            db=db,
            exam_id=exam_id,
            question_id=request.question_id,
            selected_answer=request.selected_answer,
            time_spent_seconds=request.time_spent_seconds or 0
        )
        
        return {
            "success": True,
            "is_correct": attempt.is_correct,
            "message": "Answer submitted successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting answer: {str(e)}")


@router.post("/{exam_id}/submit", response_model=ResultResponse)
def submit_exam_route(
    exam_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Submit exam and calculate results
    """
    try:
        # Verify exam belongs to user
        exam = db.query(Exam).filter(Exam.id == exam_id, Exam.user_id == current_user.id).first()
        if not exam:
            raise HTTPException(status_code=404, detail="Exam not found")
        
        result = submit_exam(db, exam_id)
        
        # Parse weak_topics from JSON
        import json
        weak_topics = json.loads(result.weak_topics) if result.weak_topics else None
        
        return {
            "id": result.id,
            "exam_id": result.exam_id,
            "total_questions": result.total_questions,
            "correct_answers": result.correct_answers,
            "wrong_answers": result.wrong_answers,
            "unanswered": result.unanswered,
            "total_marks": result.total_marks,
            "obtained_marks": result.obtained_marks,
            "percentage": result.percentage,
            "weak_topics": weak_topics,
            "performance_analysis": result.performance_analysis,
            "created_at": result.created_at
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting exam: {str(e)}")


@router.get("/{exam_id}/result", response_model=ResultResponse)
def get_exam_result(
    exam_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get exam result and performance analysis
    """
    # Verify exam belongs to user
    exam = db.query(Exam).filter(Exam.id == exam_id, Exam.user_id == current_user.id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    result = db.query(ExamResult).filter(ExamResult.exam_id == exam_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Exam not yet submitted")
    
    # Parse weak_topics from JSON
    import json
    weak_topics = json.loads(result.weak_topics) if result.weak_topics else None
    
    return {
        "id": result.id,
        "exam_id": result.exam_id,
        "total_questions": result.total_questions,
        "correct_answers": result.correct_answers,
        "wrong_answers": result.wrong_answers,
        "unanswered": result.unanswered,
        "total_marks": result.total_marks,
        "obtained_marks": result.obtained_marks,
        "percentage": result.percentage,
        "weak_topics": weak_topics,
        "performance_analysis": result.performance_analysis,
        "created_at": result.created_at
    }


@router.get("/{exam_id}/analysis")
async def get_exam_analysis(
    exam_id: int,
    language: Optional[str] = "hinglish",
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get AI-powered performance analysis for exam
    """
    # Verify exam belongs to user
    exam = db.query(Exam).filter(Exam.id == exam_id, Exam.user_id == current_user.id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    if language not in ['hindi', 'hinglish', 'english']:
        language = 'hinglish'
    
    analysis = await analyze_exam_performance(db, exam_id, language)
    
    return {
        "exam_id": exam_id,
        "analysis": analysis,
        "language": language
    }


@router.get("/list")
def list_user_exams(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    List all exams for the current user
    """
    exams = db.query(Exam).filter(Exam.user_id == current_user.id).order_by(Exam.created_at.desc()).all()
    return exams


@router.get("/{exam_id}", response_model=ExamResponse)
def get_exam(
    exam_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get exam details
    """
    exam = db.query(Exam).filter(Exam.id == exam_id, Exam.user_id == current_user.id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam
