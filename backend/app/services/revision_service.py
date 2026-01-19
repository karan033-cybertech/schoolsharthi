"""
Smart Revision Mode Service
Generates comprehensive revision packs for exam preparation
"""
from app.services.ai_service import _call_ai, detect_language
from app.models import Subject, ClassLevel
from typing import Optional
import re


async def generate_revision_pack(
    query: str,
    subject: Optional[Subject] = None,
    class_level: Optional[ClassLevel] = None,
    language: Optional[str] = None
) -> dict:
    """
    Generate a complete revision pack based on student query
    Auto-detects subject and urgency from query like "Kal exam hai science ka"
    
    Returns:
    - One-page revision notes
    - Important formulas
    - 20 rapid-fire questions
    - 5 common mistakes
    - Quick tips
    """
    # Auto-detect language if not provided
    if not language:
        language = detect_language(query)
    
    # Auto-extract subject from query (Hindi/English/Hinglish)
    detected_subject = extract_subject_from_query(query, subject)
    
    # Auto-extract class level if present
    detected_class = extract_class_from_query(query, class_level)
    
    # Auto-detect exam urgency
    urgency = detect_exam_urgency(query)
    
    # Build system prompt based on language - SchoolSharthi teacher personality
    if language == 'hindi':
        system_prompt = """आप एक professional board exam teacher हैं। Exam mode में revision pack बनाओ।
Practical और marks-oriented। No fluff। Specific और actionable।"""
    elif language == 'hinglish':
        system_prompt = """You are a professional board exam teacher. Create exam-focused revision pack in Exam Mode.
Practical aur marks-oriented. No fluff. Specific aur actionable. Confident teacher ki tarah answer karo."""
    else:  # english
        system_prompt = """You are a professional board exam teacher. Create exam-focused revision pack in Exam Mode.
Practical and marks-oriented. No fluff. Specific and actionable. Answer as a confident teacher."""
    
    # Build revision prompt
    subject_name = detected_subject.value if detected_subject else "General"
    class_name = detected_class.value if detected_class else ""
    
    if language == 'hindi':
        prompt = f"""Exam Mode: Revision Commander (Professional teacher style):

Subject: {subject_name}
Class: {class_name}
Urgency: {urgency}

Query: {query}

इस exact format में provide करो:

1. 20 MOST IMPORTANT QUESTIONS
   - PYQ-based questions
   - Marks distribution (1/3/5 marks)
   - Expected answer length
   
2. 10 MUST-REMEMBER FORMULAS
   - सभी critical formulas
   - Application के साथ
   - Common mistakes in formula usage
   
3. 5 COMMON MISTAKES
   - Board exam में students क्या गलतियाँ करते हैं
   - कैसे avoid करें
   - Marks deduction कहाँ होता है
   
4. 3 SURE-SHOT CHAPTERS
   - High probability chapters
   - Focus करने वाले topics
   - Last minute strategy

Practical और marks-focused। Teacher की तरह confident answer।"""
    
    elif language == 'hinglish':
        prompt = f"""Exam Mode: Revision Commander (Professional teacher style):

Subject: {subject_name}
Class: {class_name}
Urgency: {urgency}

Query: {query}

Is exact format mein provide karo:

1. 20 MOST IMPORTANT QUESTIONS
   - PYQ-based questions
   - Marks distribution (1/3/5 marks)
   - Expected answer length
   
2. 10 MUST-REMEMBER FORMULAS
   - Sabhi critical formulas
   - Application ke sath
   - Common mistakes in formula usage
   
3. 5 COMMON MISTAKES
   - Board exam mein students kya mistakes karte hain
   - Kaise avoid kare
   - Marks deduction kahan hota hai
   
4. 3 SURE-SHOT CHAPTERS
   - High probability chapters
   - Focus karne wale topics
   - Last minute strategy

Practical aur marks-focused. Teacher ki tarah confident answer."""
    
    else:  # english
        prompt = f"""Exam Mode: Revision Commander (Professional teacher style):

Subject: {subject_name}
Class: {class_name}
Urgency: {urgency}

Query: {query}

Provide in this exact format:

1. 20 MOST IMPORTANT QUESTIONS
   - PYQ-based questions
   - Marks distribution (1/3/5 marks)
   - Expected answer length
   
2. 10 MUST-REMEMBER FORMULAS
   - All critical formulas
   - With application examples
   - Common mistakes in formula usage
   
3. 5 COMMON MISTAKES
   - What students do wrong in board exams
   - How to avoid them
   - Where marks are deducted
   
4. 3 SURE-SHOT CHAPTERS
   - High probability chapters
   - Topics to focus on
   - Last minute strategy

Practical and marks-focused. Answer as a confident teacher."""
    
    # Get AI response
    ai_response = await _call_ai(prompt, system_prompt)
    
    # Parse response into structured format
    structured_pack = parse_revision_response(ai_response, language)
    
    return {
        "revision_notes": structured_pack.get("revision_notes", ""),
        "formulas": structured_pack.get("formulas", ""),
        "rapid_fire_questions": structured_pack.get("rapid_fire_questions", ""),
        "common_mistakes": structured_pack.get("common_mistakes", ""),
        "quick_tips": structured_pack.get("quick_tips", ""),
        "full_response": ai_response or "",
        "subject": subject_name,
        "class_level": class_name,
        "urgency": urgency,
        "language": language
    }


def extract_subject_from_query(query: str, provided_subject: Optional[Subject]) -> Optional[Subject]:
    """Extract subject from query text"""
    if provided_subject:
        return provided_subject
    
    query_lower = query.lower()
    
    # Hindi subjects
    hindi_subjects = {
        'physics': ['physics', 'fiziks', 'फिजिक्स', 'भौतिकी'],
        'chemistry': ['chemistry', 'kemistri', 'केमिस्ट्री', 'रसायन', 'रसायन विज्ञान'],
        'biology': ['biology', 'bayology', 'बायोलॉजी', 'जीव विज्ञान'],
        'mathematics': ['math', 'maths', 'ganit', 'गणित', 'mathematics']
    }
    
    # Check for subject mentions
    for subject_enum, keywords in hindi_subjects.items():
        for keyword in keywords:
            if keyword in query_lower:
                return Subject[subject_enum.upper()] if hasattr(Subject, subject_enum.upper()) else None
    
    return None


def extract_class_from_query(query: str, provided_class: Optional[ClassLevel]) -> Optional[ClassLevel]:
    """Extract class level from query"""
    if provided_class:
        return provided_class
    
    # Look for class numbers
    class_match = re.search(r'\b(6|7|8|9|10|11|12)\b', query)
    if class_match:
        class_num = class_match.group(1)
        class_attr = f"CLASS_{class_num}"
        if hasattr(ClassLevel, class_attr):
            return getattr(ClassLevel, class_attr)
    
    return None


def detect_exam_urgency(query: str) -> str:
    """Detect exam urgency from query"""
    query_lower = query.lower()
    
    # Hindi/English urgency indicators
    urgent_keywords = ['kal', 'tomorrow', 'aaj', 'today', 'abhi', 'now', 'जल्दी', 'urgent']
    soon_keywords = ['week', 'hafte', 'month', 'mahine', 'days', 'din']
    
    if any(keyword in query_lower for keyword in urgent_keywords):
        return 'urgent'  # Exam tomorrow/today
    elif any(keyword in query_lower for keyword in soon_keywords):
        return 'soon'  # Exam in days/weeks
    else:
        return 'normal'  # General revision


def parse_revision_response(response: str, language: str) -> dict:
    """
    Parse AI response into structured sections
    Falls back to full response if parsing fails
    """
    if not response:
        return {}
    
    sections = {
        "revision_notes": "",
        "formulas": "",
        "rapid_fire_questions": "",
        "common_mistakes": "",
        "quick_tips": ""
    }
    
    # Try to extract sections by headings
    # Look for section markers
    section_markers = {
        "revision_notes": ["revision notes", "one-page", "summary", "notes", "संक्षिप्त नोट्स"],
        "formulas": ["formula", "formulae", "सूत्र"],
        "rapid_fire_questions": ["rapid-fire", "rapid fire", "questions", "प्रश्न"],
        "common_mistakes": ["common mistakes", "mistakes", "गलतियाँ"],
        "quick_tips": ["tips", "quick tips", "सुझाव"]
    }
    
    # Split by lines and try to identify sections
    lines = response.split('\n')
    current_section = None
    
    for line in lines:
        line_lower = line.lower()
        
        # Check if line contains a section marker
        for section_name, markers in section_markers.items():
            if any(marker in line_lower for marker in markers):
                current_section = section_name
                sections[section_name] = line + "\n"
                break
        else:
            # Add line to current section
            if current_section:
                sections[current_section] += line + "\n"
    
    # If no sections found, return full response in revision_notes
    if not any(sections.values()):
        sections["revision_notes"] = response
    
    return sections
