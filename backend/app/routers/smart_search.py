"""
Ultra Fast Smart Search Router
Google-style unified search across notes, PYQs, and chapters
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth import get_current_active_user
from app.services.smart_search_service import unified_search
from pydantic import BaseModel
from typing import Optional, List, Dict

router = APIRouter()


class SearchRequest(BaseModel):
    query: str  # e.g., "Class 10 physics numericals"
    search_type: Optional[str] = "all"  # "all", "notes", "pyqs", "chapters"
    limit: Optional[int] = 20


class SearchResponse(BaseModel):
    query: str
    keywords: List[str]
    notes: List[Dict]
    pyqs: List[Dict]
    chapters: List[Dict]
    ai_explanation: str
    total_results: int
    language: str


@router.post("/search", response_model=SearchResponse)
async def search(
    request: SearchRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Unified search across notes, PYQs, and chapters
    
    Search types:
    - "all": Search everything
    - "notes": Only notes
    - "pyqs": Only PYQs
    - "chapters": Only chapters
    
    Returns:
    - Matching notes with relevance scores
    - Matching PYQs
    - Matching chapters
    - AI-generated explanation
    - Keyword suggestions
    """
    try:
        if not request.query or len(request.query.strip()) < 2:
            raise HTTPException(status_code=400, detail="Query must be at least 2 characters")
        
        # Validate search_type
        if request.search_type not in ["all", "notes", "pyqs", "chapters"]:
            request.search_type = "all"
        
        results = await unified_search(
            query=request.query,
            db=db,
            search_type=request.search_type,
            limit=request.limit or 20
        )
        
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing search: {str(e)}")


@router.get("/quick")
async def quick_search(
    q: str = Query(..., description="Search query"),
    type: Optional[str] = Query("all", description="Search type: all, notes, pyqs, chapters"),
    limit: Optional[int] = Query(20, description="Max results"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Quick search endpoint - simpler GET interface
    Example: /api/search/quick?q=class 10 physics&type=notes
    """
    try:
        if not q or len(q.strip()) < 2:
            raise HTTPException(status_code=400, detail="Query parameter 'q' must be at least 2 characters")
        
        if type not in ["all", "notes", "pyqs", "chapters"]:
            type = "all"
        
        results = await unified_search(
            query=q,
            db=db,
            search_type=type,
            limit=limit or 20
        )
        
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing search: {str(e)}")
