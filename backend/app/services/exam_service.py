"""
Exam Mode Service
Generates exams, tracks performance, and analyzes results
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Exam, ExamQuestion, ExamAttempt, ExamResult, Subject, ClassLevel, ExamType, PYQ
from app.services.ai_service import _call_ai
from typing import List, Dict, Optional
from datetime import datetime
import json
import random


def create_exam(
    db: Session,
    user_id: int,
    subject: Optional[Subject] = None,
    class_level: Optional[ClassLevel] = None,
    exam_type: Optional[ExamType] = None,
    duration_minutes: int = 60,
    total_questions: int = 30,
    difficulty: str = "mixed"
) -> Exam:
    """
    Create a new exam with randomized questions
    """
    # Create exam record
    exam = Exam(
        user_id=user_id,
        title=f"{subject.value if subject else 'General'} Exam - {exam_type.value if exam_type else 'Practice'}",
        subject=subject,
        class_level=class_level,
        exam_type=exam_type,
        duration_minutes=duration_minutes,
        total_questions=total_questions,
        status="pending"
    )
    db.add(exam)
    db.commit()
    db.refresh(exam)
    
    # Generate questions (mock questions for now - can be enhanced with PYQ integration)
    questions = generate_exam_questions(
        exam.id,
        subject,
        class_level,
        exam_type,
        total_questions,
        difficulty
    )
    
    # Add questions to database
    for q in questions:
        db_question = ExamQuestion(
            exam_id=exam.id,
            question_number=q["question_number"],
            question_text=q["question_text"],
            options=json.dumps(q["options"]),
            correct_answer=q["correct_answer"],
            marks=q.get("marks", 1),
            difficulty=q.get("difficulty", "medium")
        )
        db.add(db_question)
        db.flush()  # Flush to get question ID
    
    db.commit()
    
    return exam


def generate_exam_questions(
    exam_id: int,
    subject: Optional[Subject],
    class_level: Optional[ClassLevel],
    exam_type: Optional[ExamType],
    total_questions: int,
    difficulty: str = "mixed"
) -> List[Dict]:
    """
    Generate exam questions (mock implementation)
    Can be enhanced to pull from PYQs or generate via AI
    """
    questions = []
    
    # Mock question generation - in production, this would pull from PYQs or AI
    for i in range(1, total_questions + 1):
        # Determine difficulty for this question
        if difficulty == "mixed":
            question_difficulty = random.choice(["easy", "medium", "hard"])
        else:
            question_difficulty = difficulty
        
        # Generate mock question
        questions.append({
            "question_number": i,
            "question_text": f"Question {i}: This is a sample question for {subject.value if subject else 'General'} exam. (Difficulty: {question_difficulty})",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": random.choice(["0", "1", "2", "3"]),  # Random option index
            "marks": 1,
            "difficulty": question_difficulty
        })
    
    return questions


def start_exam(db: Session, exam_id: int) -> Exam:
    """Start exam - set status and start time"""
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise ValueError("Exam not found")
    
    if exam.status != "pending":
        raise ValueError("Exam already started or completed")
    
    exam.status = "in_progress"
    exam.started_at = datetime.utcnow()
    db.commit()
    db.refresh(exam)
    
    return exam


def submit_answer(
    db: Session,
    exam_id: int,
    question_id: int,
    selected_answer: str,
    time_spent_seconds: int = 0
) -> ExamAttempt:
    """Submit answer for a question"""
    # Get question to check answer
    question = db.query(ExamQuestion).filter(ExamQuestion.id == question_id).first()
    if not question:
        raise ValueError("Question not found")
    
    # Check if correct
    is_correct = str(selected_answer).strip() == str(question.correct_answer).strip()
    
    # Create or update attempt
    attempt = db.query(ExamAttempt).filter(
        ExamAttempt.exam_id == exam_id,
        ExamAttempt.question_id == question_id
    ).first()
    
    if attempt:
        attempt.selected_answer = selected_answer
        attempt.is_correct = is_correct
        attempt.time_spent_seconds = time_spent_seconds
    else:
        attempt = ExamAttempt(
            exam_id=exam_id,
            question_id=question_id,
            selected_answer=selected_answer,
            is_correct=is_correct,
            time_spent_seconds=time_spent_seconds
        )
        db.add(attempt)
    
    db.commit()
    db.refresh(attempt)
    
    return attempt


def submit_exam(db: Session, exam_id: int) -> ExamResult:
    """Submit exam and calculate results"""
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise ValueError("Exam not found")
    
    if exam.status == "submitted":
        # Return existing result
        return db.query(ExamResult).filter(ExamResult.exam_id == exam_id).first()
    
    # Get all attempts
    attempts = db.query(ExamAttempt).filter(ExamAttempt.exam_id == exam_id).all()
    questions = db.query(ExamQuestion).filter(ExamQuestion.exam_id == exam_id).all()
    
    # Calculate results
    total_questions = len(questions)
    correct_answers = sum(1 for a in attempts if a.is_correct)
    wrong_answers = sum(1 for a in attempts if not a.is_correct)
    unanswered = total_questions - len(attempts)
    
    # Calculate marks
    total_marks = sum(q.marks for q in questions)
    obtained_marks = sum(q.marks for q, a in zip(questions, attempts) if a.is_correct)
    percentage = round((obtained_marks / total_marks * 100) if total_marks > 0 else 0)
    
    # Identify weak topics (questions with wrong answers)
    weak_questions = [a for a in attempts if not a.is_correct]
    weak_topics = {
        "wrong_questions": len(weak_questions),
        "difficulties": {}
    }
    
    # Count by difficulty
    for attempt in weak_questions:
        q = next((q for q in questions if q.id == attempt.question_id), None)
        if q:
            difficulty = q.difficulty
            weak_topics["difficulties"][difficulty] = weak_topics["difficulties"].get(difficulty, 0) + 1
    
    # Update exam status
    exam.status = "submitted"
    exam.submitted_at = datetime.utcnow()
    db.commit()
    
    # Create or update result
    result = db.query(ExamResult).filter(ExamResult.exam_id == exam_id).first()
    if result:
        result.total_questions = total_questions
        result.correct_answers = correct_answers
        result.wrong_answers = wrong_answers
        result.unanswered = unanswered
        result.total_marks = total_marks
        result.obtained_marks = obtained_marks
        result.percentage = percentage
        result.weak_topics = json.dumps(weak_topics)
    else:
        result = ExamResult(
            exam_id=exam_id,
            total_questions=total_questions,
            correct_answers=correct_answers,
            wrong_answers=wrong_answers,
            unanswered=unanswered,
            total_marks=total_marks,
            obtained_marks=obtained_marks,
            percentage=percentage,
            weak_topics=json.dumps(weak_topics)
        )
        db.add(result)
    
    db.commit()
    db.refresh(result)
    
    return result


async def analyze_exam_performance(
    db: Session,
    exam_id: int,
    language: str = "hinglish"
) -> str:
    """
    Generate AI-powered performance analysis
    """
    result = db.query(ExamResult).filter(ExamResult.exam_id == exam_id).first()
    if not result:
        return ""
    
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    weak_topics = json.loads(result.weak_topics) if result.weak_topics else {}
    
    # Build analysis prompt
    if language == 'hindi':
        system_prompt = """आप एक experienced teacher हैं। Student के exam performance का detailed analysis दो।"""
        prompt = f"""Exam Performance Analysis:

Total Questions: {result.total_questions}
Correct: {result.correct_answers}
Wrong: {result.wrong_answers}
Unanswered: {result.unanswered}
Percentage: {result.percentage}%

Subject: {exam.subject.value if exam.subject else 'General'}
Weak Topics: {weak_topics}

कृपया provide करो:
1. Overall performance का summary
2. Strong areas
3. Weak areas और improvements
4. Next steps और recommendations

Encouraging tone में response दो।"""
    elif language == 'hinglish':
        system_prompt = """You are an experienced teacher. Provide detailed analysis of student's exam performance."""
        prompt = f"""Exam Performance Analysis:

Total Questions: {result.total_questions}
Correct: {result.correct_answers}
Wrong: {result.wrong_answers}
Unanswered: {result.unanswered}
Percentage: {result.percentage}%

Subject: {exam.subject.value if exam.subject else 'General'}
Weak Topics: {weak_topics}

Please provide:
1. Overall performance ka summary
2. Strong areas
3. Weak areas aur improvements
4. Next steps aur recommendations

Encouraging tone mein response do in Hinglish."""
    else:  # english
        system_prompt = """You are an experienced teacher. Provide detailed analysis of student's exam performance."""
        prompt = f"""Exam Performance Analysis:

Total Questions: {result.total_questions}
Correct: {result.correct_answers}
Wrong: {result.wrong_answers}
Unanswered: {result.unanswered}
Percentage: {result.percentage}%

Subject: {exam.subject.value if exam.subject else 'General'}
Weak Topics: {weak_topics}

Please provide:
1. Overall performance summary
2. Strong areas
3. Weak areas and improvements
4. Next steps and recommendations

Keep it encouraging and actionable."""
    
    analysis = await _call_ai(prompt, system_prompt)
    
    # Save analysis
    if analysis:
        result.performance_analysis = analysis
        db.commit()
    
    return analysis or "Performance analysis generated."
