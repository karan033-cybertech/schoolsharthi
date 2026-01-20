"""
Ultra Fast Smart Search Service
Google-style education search across notes, PYQs, and chapters
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.models import Note, PYQ, Subject, ClassLevel, ExamType
from app.services.ai_service import _call_ai, detect_language
from typing import List, Dict, Optional
import re


async def unified_search(
    query: str,
    db: Session,
    search_type: str = "all",  # "all", "notes", "pyqs", "chapters"
    limit: int = 20
) -> Dict:
    """
    Unified search across notes, PYQs, and chapters
    
    Returns:
    - Notes matching query
    - PYQs matching query
    - AI-generated explanation/summary
    - Keyword highlighting suggestions
    """
    query_lower = query.lower()
    detected_language = detect_language(query)
    
    # Extract search keywords
    keywords = extract_keywords(query)
    
    results = {
        "query": query,
        "keywords": keywords,
        "notes": [],
        "pyqs": [],
        "chapters": [],
        "ai_explanation": "",
        "total_results": 0,
        "language": detected_language
    }
    
    # Search Notes
    if search_type in ["all", "notes"]:
        notes = search_notes(db, query, keywords, limit)
        results["notes"] = notes
    
    # Search PYQs
    if search_type in ["all", "pyqs"]:
        pyqs = search_pyqs(db, query, keywords, limit)
        results["pyqs"] = pyqs
    
    # Search Chapters (from notes and PYQs)
    if search_type in ["all", "chapters"]:
        chapters = search_chapters(db, query, keywords, limit)
        results["chapters"] = chapters
    
    # Calculate total results
    results["total_results"] = len(results["notes"]) + len(results["pyqs"]) + len(results["chapters"])
    
    # Generate AI explanation/summary
    if results["total_results"] > 0:
        ai_explanation = await generate_search_explanation(query, results, detected_language)
        results["ai_explanation"] = ai_explanation
    
    return results


def extract_keywords(query: str) -> List[str]:
    """Extract important keywords from search query"""
    # Remove common words
    stop_words = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'as', 'are', 'was', 'were', 
                  'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                  'ka', 'ki', 'ke', 'ko', 'me', 'se', 'par', 'aur', 'ya', 'lekin', 'agar',
                  'hai', 'hain', 'ho', 'hoga', 'hogaa'}
    
    # Extract words
    words = re.findall(r'\b\w+\b', query.lower())
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    
    return keywords[:10]  # Top 10 keywords


def search_notes(db: Session, query: str, keywords: List[str], limit: int) -> List[Dict]:
    """Search notes by title, chapter, subject, class"""
    query_lower = query.lower()
    
    # Build search conditions
    conditions = []
    
    # Search in title and chapter
    for keyword in keywords:
        conditions.append(
            or_(
                Note.title.ilike(f'%{keyword}%'),
                Note.chapter.ilike(f'%{keyword}%'),
                Note.description.ilike(f'%{keyword}%') if Note.description else None
            )
        )
    
    # Also search for exact phrase
    conditions.append(
        or_(
            Note.title.ilike(f'%{query_lower}%'),
            Note.chapter.ilike(f'%{query_lower}%')
        )
    )
    
    # Query notes
    notes_query = db.query(Note).filter(
        Note.is_approved == True,
        or_(*conditions) if conditions else None
    ).limit(limit)
    
    notes = notes_query.all()
    
    # Format results
    from app.utils.url_rewrite import rewrite_file_url
    
    return [{
        "id": note.id,
        "title": note.title,
        "subject": note.subject.value if note.subject else None,
        "class_level": note.class_level.value if note.class_level else None,
        "chapter": note.chapter,
        "description": note.description,
        "file_url": rewrite_file_url(note.file_url) if note.file_url else None,
        "views_count": note.views_count,
        "matched_keywords": [kw for kw in keywords if kw in (note.title + " " + note.chapter).lower()],
        "relevance_score": calculate_relevance(note.title + " " + note.chapter, query, keywords)
    } for note in notes]


def search_pyqs(db: Session, query: str, keywords: List[str], limit: int) -> List[Dict]:
    """Search PYQs by exam type, year, subject, title"""
    query_lower = query.lower()
    
    conditions = []
    
    # Search in title
    for keyword in keywords:
        conditions.append(PYQ.title.ilike(f'%{keyword}%'))
    
    # Search for exam types (boards, neet, jee, etc.)
    exam_types = {
        'neet': 'neet',
        'jee': 'jee_main',
        'jee advanced': 'jee_advanced',
        'board': 'boards',
        'boards': 'boards'
    }
    
    for exam_keyword, exam_type in exam_types.items():
        if exam_keyword in query_lower:
            conditions.append(PYQ.exam_type == ExamType[exam_type.upper()])
            break
    
    # Query PYQs
    pyqs_query = db.query(PYQ).filter(
        PYQ.is_approved == True,
        or_(*conditions) if conditions else None
    ).limit(limit)
    
    pyqs = pyqs_query.all()
    
    from app.utils.url_rewrite import rewrite_file_url
    
    return [{
        "id": pyq.id,
        "title": pyq.title,
        "exam_type": pyq.exam_type.value if pyq.exam_type else None,
        "year": pyq.year,
        "subject": pyq.subject.value if pyq.subject else None,
        "class_level": pyq.class_level.value if pyq.class_level else None,
        "question_paper_url": rewrite_file_url(pyq.question_paper_url) if pyq.question_paper_url else None,
        "views_count": pyq.views_count,
        "matched_keywords": [kw for kw in keywords if kw in pyq.title.lower()],
        "relevance_score": calculate_relevance(pyq.title, query, keywords)
    } for pyq in pyqs]


def search_chapters(db: Session, query: str, keywords: List[str], limit: int) -> List[Dict]:
    """Search chapters across notes and PYQs"""
    query_lower = query.lower()
    
    # Get unique chapters from notes
    notes = db.query(Note.chapter, Note.subject, Note.class_level).filter(
        Note.is_approved == True
    ).distinct().all()
    
    chapters = []
    seen_chapters = set()
    
    for note in notes:
        chapter_lower = note.chapter.lower() if note.chapter else ""
        
        # Check if query matches chapter
        matches = any(kw in chapter_lower for kw in keywords) or query_lower in chapter_lower
        
        if matches and note.chapter:
            key = f"{note.subject.value if note.subject else ''}_{note.chapter}"
            if key not in seen_chapters:
                chapters.append({
                    "name": note.chapter,
                    "subject": note.subject.value if note.subject else None,
                    "class_level": note.class_level.value if note.class_level else None,
                    "type": "note",
                    "matched_keywords": [kw for kw in keywords if kw in chapter_lower],
                    "relevance_score": calculate_relevance(note.chapter, query, keywords)
                })
                seen_chapters.add(key)
    
    # Sort by relevance
    chapters.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    return chapters[:limit]


def calculate_relevance(text: str, query: str, keywords: List[str]) -> float:
    """Calculate relevance score for search result"""
    text_lower = text.lower()
    query_lower = query.lower()
    
    score = 0.0
    
    # Exact phrase match (highest priority)
    if query_lower in text_lower:
        score += 10.0
    
    # Keyword matches
    for keyword in keywords:
        if keyword in text_lower:
            score += 2.0
    
    # Position bonus (earlier = more relevant)
    first_match_pos = text_lower.find(query_lower)
    if first_match_pos >= 0:
        position_bonus = max(0, 5.0 - (first_match_pos / 10))
        score += position_bonus
    
    return score


async def generate_search_explanation(
    query: str,
    search_results: Dict,
    language: str
) -> str:
    """
    Generate AI-powered explanation/summary of search results
    Helps students understand what they found
    """
    total = search_results["total_results"]
    notes_count = len(search_results["notes"])
    pyqs_count = len(search_results["pyqs"])
    chapters_count = len(search_results["chapters"])
    
    if language == 'hindi':
        system_prompt = """आप एक helpful search assistant हैं। Search results का summary दो और students को guide करो।"""
        prompt = f"""Search Query: {query}

Results found:
- {notes_count} notes
- {pyqs_count} PYQs
- {chapters_count} chapters

कृपया provide करो:
1. Search results का brief summary
2. सबसे relevant results क्या हैं
3. Student को कैसे use करना चाहिए
4. Related topics या suggestions

Short और helpful answer दो (2-3 sentences)।"""
    
    elif language == 'hinglish':
        system_prompt = """You are a helpful search assistant. Summarize search results and guide students."""
        prompt = f"""Search Query: {query}

Results found:
- {notes_count} notes
- {pyqs_count} PYQs
- {chapters_count} chapters

Please provide:
1. Brief summary of search results
2. Most relevant results kya hain
3. Student ko kaise use karna chahiye
4. Related topics ya suggestions

Short aur helpful answer do (2-3 sentences) in Hinglish."""
    
    else:  # english
        system_prompt = """You are a helpful search assistant. Summarize search results and guide students."""
        prompt = f"""Search Query: {query}

Results found:
- {notes_count} notes
- {pyqs_count} PYQs
- {chapters_count} chapters

Please provide:
1. Brief summary of search results
2. Most relevant results
3. How students should use these
4. Related topics or suggestions

Keep it short and helpful (2-3 sentences)."""
    
    explanation = await _call_ai(prompt, system_prompt)
    
    return explanation or f"Found {total} results for '{query}'. Check notes, PYQs, and chapters above."
