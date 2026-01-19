from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CareerQuery, User
from app.schemas import CareerQueryCreate, CareerQueryResponse
from app.auth import get_current_active_user
from app.services.ai_service import get_career_guidance
from typing import List

router = APIRouter()


@router.post("/query", response_model=CareerQueryResponse)
async def ask_career_question(
    query: CareerQueryCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Create career query record
    db_query = CareerQuery(
        user_id=current_user.id,
        query=query.query
    )
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    
    # Get AI response with guidance type
    try:
        ai_response = await get_career_guidance(query.query, query.guidance_type)
        if ai_response:
            db_query.ai_response = ai_response
        else:
            # If AI service returns None (no API key configured), set a helpful message
            db_query.ai_response = "AI service is not configured. Please configure GROQ_API_KEY or OPENAI_API_KEY in the admin panel."
        db.commit()
        db.refresh(db_query)
    except NameError as e:
        # Handle undefined name errors (like _call_openai)
        error_msg = str(e)
        print(f"AI service NameError: {error_msg}")
        import traceback
        traceback.print_exc()
        db_query.ai_response = f"AI service configuration error: {error_msg}. Please restart the server or check the AI service code."
        db.commit()
        db.refresh(db_query)
    except Exception as e:
        # If AI service fails, set error message
        error_type = type(e).__name__
        error_msg = str(e)
        print(f"AI service error ({error_type}): {error_msg}")
        import traceback
        traceback.print_exc()
        db_query.ai_response = f"Error generating AI response ({error_type}): {error_msg}. Please check if the API key is configured correctly."
        db.commit()
        db.refresh(db_query)
    
    return db_query


@router.get("/guidance-types")
def get_guidance_types():
    """Get available career guidance types"""
    return {
        "guidance_types": [
            {
                "type": "stream_selection",
                "title": "Stream Selection (10th के बाद)",
                "description": "Science, Commerce, या Arts - कौन सा stream choose करें?"
            },
            {
                "type": "career_roadmap_12th",
                "title": "Career Roadmap (12th के बाद)",
                "description": "12th के बाद क्या करें? Degree, Diploma, या Skill courses?"
            },
            {
                "type": "neet_jee_strategy",
                "title": "NEET/JEE Strategy",
                "description": "Medical या Engineering के लिए preparation strategy"
            },
            {
                "type": "govt_exams",
                "title": "Government Exams",
                "description": "SSC, Railway, Banking जैसे government jobs की तैयारी"
            },
            {
                "type": "skill_based",
                "title": "Skill-Based Careers",
                "description": "ITI, Vocational courses, और skill-based career options"
            }
        ]
    }


@router.get("/queries", response_model=List[CareerQueryResponse])
def get_user_queries(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    queries = db.query(CareerQuery).filter(CareerQuery.user_id == current_user.id).order_by(CareerQuery.created_at.desc()).all()
    return queries


@router.get("/queries/{query_id}", response_model=CareerQueryResponse)
def get_query(
    query_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    query = db.query(CareerQuery).filter(CareerQuery.id == query_id, CareerQuery.user_id == current_user.id).first()
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    return query
