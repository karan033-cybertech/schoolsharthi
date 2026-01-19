"""
Adaptive Learning Service
Tracks student doubt patterns and generates personalized recommendations
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models import Doubt, Subject, ClassLevel
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import json


def analyze_student_performance(db: Session, user_id: int) -> Dict:
    """
    Analyze student doubt patterns to identify weak topics
    Returns:
    - Most asked subjects
    - Most asked chapters per subject
    - Weak topics (high doubt frequency)
    - Doubt frequency statistics
    """
    # Get all doubts for the student
    doubts = db.query(Doubt).filter(Doubt.user_id == user_id).all()
    
    if not doubts:
        return {
            "total_doubts": 0,
            "subjects": {},
            "chapters": {},
            "weak_topics": [],
            "recommendations": []
        }
    
    # Count doubts by subject
    subject_counts = defaultdict(int)
    chapter_counts = defaultdict(int)  # key: "subject_chapter"
    class_level_counts = defaultdict(int)
    
    for doubt in doubts:
        if doubt.subject:
            subject_counts[doubt.subject.value] += 1
            if doubt.chapter:
                key = f"{doubt.subject.value}_{doubt.chapter}"
                chapter_counts[key] += 1
        if doubt.class_level:
            class_level_counts[doubt.class_level.value] += 1
    
    # Identify weak topics (top 3 subjects and chapters with most doubts)
    sorted_subjects = sorted(subject_counts.items(), key=lambda x: x[1], reverse=True)
    sorted_chapters = sorted(chapter_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Build weak topics list
    weak_topics = []
    
    # Add top 3 subjects with doubt counts
    for subject, count in sorted_subjects[:3]:
        weak_topics.append({
            "type": "subject",
            "name": subject,
            "doubt_count": count,
            "percentage": round((count / len(doubts)) * 100, 1)
        })
    
    # Add top 5 chapters with doubt counts
    for chapter_key, count in sorted_chapters[:5]:
        subject, chapter = chapter_key.split("_", 1)
        weak_topics.append({
            "type": "chapter",
            "subject": subject,
            "name": chapter,
            "doubt_count": count,
            "percentage": round((count / len(doubts)) * 100, 1)
        })
    
    # Build chapter breakdown by subject
    chapters_by_subject = defaultdict(dict)
    for chapter_key, count in chapter_counts.items():
        subject, chapter = chapter_key.split("_", 1)
        chapters_by_subject[subject][chapter] = count
    
    # Generate personalized recommendations
    recommendations = generate_recommendations(sorted_subjects, sorted_chapters, len(doubts))
    
    return {
        "total_doubts": len(doubts),
        "subjects": dict(subject_counts),
        "chapters": dict(chapters_by_subject),
        "weak_topics": weak_topics[:8],  # Top 8 weak topics
        "recommendations": recommendations,
        "class_levels": dict(class_level_counts)
    }


def generate_recommendations(
    sorted_subjects: List[Tuple[str, int]], 
    sorted_chapters: List[Tuple[str, int]], 
    total_doubts: int
) -> List[Dict]:
    """
    Generate personalized recommendations based on doubt patterns
    """
    recommendations = []
    
    if not sorted_subjects:
        return recommendations
    
    # Get top weak subject and chapter
    top_subject, top_subject_count = sorted_subjects[0] if sorted_subjects else (None, 0)
    
    if sorted_chapters:
        top_chapter_key, top_chapter_count = sorted_chapters[0]
        top_subject_from_chapter, top_chapter = top_chapter_key.split("_", 1)
        
        # Recommendation for weak chapter
        recommendations.append({
            "type": "weak_chapter",
            "priority": "high",
            "message_hindi": f"आप {top_chapter} chapter में weak हो — ye 5 PYQ solve karo aur detailed notes padho",
            "message_english": f"You are weak in {top_chapter} chapter — solve these 5 PYQs and read detailed notes",
            "message_hinglish": f"Tum {top_chapter} chapter me weak ho — ye 5 PYQ solve karo aur notes padho",
            "subject": top_subject_from_chapter,
            "chapter": top_chapter,
            "action": "practice_pyqs",
            "count": 5
        })
    
    # Recommendation for weak subject
    if top_subject:
        subject_name_hindi = {
            "physics": "Physics",
            "chemistry": "Chemistry",
            "biology": "Biology",
            "mathematics": "Mathematics"
        }.get(top_subject, top_subject)
        
        recommendations.append({
            "type": "weak_subject",
            "priority": "high" if top_subject_count > total_doubts * 0.4 else "medium",
            "message_hindi": f"{subject_name_hindi} में आपको ज्यादा doubts आ रहे हैं — रोज 1-2 concepts revise करो",
            "message_english": f"You have most doubts in {subject_name_hindi} — revise 1-2 concepts daily",
            "message_hinglish": f"{subject_name_hindi} me tumhe jyada doubts aa rahe hain — roz 1-2 concepts revise karo",
            "subject": top_subject,
            "action": "daily_revision",
            "target": "1-2 concepts daily"
        })
    
    # General recommendation for consistency
    if total_doubts > 10:
        recommendations.append({
            "type": "general",
            "priority": "medium",
            "message_hindi": "अच्छा progress हो रहा है! रोजाना doubt solve करते रहो",
            "message_english": "Great progress! Keep solving doubts daily",
            "message_hinglish": "Acha progress ho raha hai! Rozana doubt solve karte raho",
            "action": "continue_practice"
        })
    
    return recommendations


def get_student_weak_topics_summary(db: Session, user_id: int, language: str = 'hinglish') -> str:
    """
    Get a personalized summary message about weak topics in specified language
    """
    performance = analyze_student_performance(db, user_id)
    
    if performance["total_doubts"] == 0:
        if language == 'hindi':
            return "अभी तक कोई doubts नहीं हैं। पढ़ाई शुरू करो और doubts पूछो!"
        elif language == 'english':
            return "No doubts yet. Start studying and ask questions!"
        else:  # hinglish
            return "Abhi tak koi doubts nahi hain. Padhai shuru karo aur doubts pucho!"
    
    weak_topics = performance["weak_topics"]
    
    if not weak_topics:
        return "Great! Keep practicing consistently."
    
    # Get top weak topic
    top_topic = weak_topics[0]
    
    if top_topic["type"] == "chapter":
        if language == 'hindi':
            return f"आप {top_topic['name']} chapter में weak हो — ye {top_topic['doubt_count']} doubts solve karo"
        elif language == 'english':
            return f"You are weak in {top_topic['name']} chapter — solve these {top_topic['doubt_count']} doubts"
        else:  # hinglish
            return f"Tum {top_topic['name']} chapter me weak ho — ye {top_topic['doubt_count']} PYQ solve karo"
    
    elif top_topic["type"] == "subject":
        if language == 'hindi':
            return f"{top_topic['name']} में आपको {top_topic['doubt_count']} doubts आए हैं — regular revision करो"
        elif language == 'english':
            return f"You have {top_topic['doubt_count']} doubts in {top_topic['name']} — do regular revision"
        else:  # hinglish
            return f"{top_topic['name']} me tumhe {top_topic['doubt_count']} doubts aaye hain — regular revision karo"
    
    return "Keep practicing!"
