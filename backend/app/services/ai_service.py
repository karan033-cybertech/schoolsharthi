from app.config import settings
from app.models import Subject, ClassLevel
from typing import Optional
import os

# Disable proxy environment variables to prevent conflicts
# These can cause issues with client initialization on Render
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)

# Initialize AI client (Groq preferred, fallback to OpenAI)
ai_client = None
ai_provider = None


def initialize_ai_client():
    """Initialize AI client - can be called to reload after API key update"""
    global ai_client, ai_provider
    
    # Reset client
    ai_client = None
    ai_provider = None
    
    # Try Groq first (free and fast)
    if settings.GROQ_API_KEY:
        try:
            import groq
            # Ensure no proxy environment variables are set before initialization
            # This prevents httpx from trying to use proxies
            proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY', 'all_proxy']
            saved_proxies = {}
            for var in proxy_vars:
                if var in os.environ:
                    saved_proxies[var] = os.environ.pop(var)
            
            # Initialize Groq client - it will use httpx internally
            # httpx >=0.24,<0.26 (compatible with supabase 2.3.4) supports proxies argument if needed, but we've removed env vars
            ai_client = groq.Groq(api_key=settings.GROQ_API_KEY)
            ai_provider = "groq"
            print(f"✅ Groq AI client initialized successfully")
            
            # Restore proxy vars if they were set (for other parts of the app)
            for var, value in saved_proxies.items():
                os.environ[var] = value
                
            return True
        except ImportError:
            print("❌ Groq package not installed. Run: pip install groq")
            ai_client = None
        except Exception as e:
            print(f"❌ Failed to initialize Groq client: {e}")
            print(f"   Error type: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            ai_client = None
    
    # Fallback to OpenAI if Groq not available
    if not ai_client and settings.OPENAI_API_KEY:
        try:
            import openai
            # For openai 0.28.1, use the older API style
            openai.api_key = settings.OPENAI_API_KEY
            ai_client = openai
            ai_provider = "openai"
            print(f"✅ OpenAI client initialized successfully")
            return True
        except ImportError:
            print("❌ OpenAI package not installed. Run: pip install openai")
            ai_client = None
        except Exception as e:
            print(f"❌ Failed to initialize OpenAI client: {e}")
            ai_client = None
    
    if not ai_client:
        print("⚠️  No AI client initialized. Configure GROQ_API_KEY or OPENAI_API_KEY in .env file")
        print(f"   Current GROQ_API_KEY: {'Set' if settings.GROQ_API_KEY else 'Not set'}")
        print(f"   Current OPENAI_API_KEY: {'Set' if settings.OPENAI_API_KEY else 'Not set'}")
    
    return ai_client is not None


# Initialize on module load
initialize_ai_client()


async def _call_ai(prompt: str, system_prompt: str = None) -> Optional[str]:
    """
    Helper function to call AI API (Groq or OpenAI)
    
    Uses latest Groq models:
    - Primary: llama-3.3-70b-versatile (replacement for deprecated llama-3.1-70b-versatile)
    - Fallback: llama-3.1-8b-instant (faster, lighter alternative)
    """
    if not ai_client:
        print("⚠️ AI client not initialized. Please configure GROQ_API_KEY or OPENAI_API_KEY.")
        return None
    
    try:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        if ai_provider == "groq":
            # Try latest Groq model (llama-3.3-70b-versatile released Dec 2024)
            # This replaces the deprecated llama-3.1-70b-versatile
            groq_models = [
                "llama-3.3-70b-versatile",  # Latest 70B model (128K context)
                "llama-3.1-8b-instant"       # Fallback: faster 8B model
            ]
            
            last_error = None
            for model in groq_models:
                try:
                    response = ai_client.chat.completions.create(
                        model=model,
                        messages=messages,
                        temperature=0.7,
                        max_tokens=2000
                    )
                    return response.choices[0].message.content
                except Exception as model_error:
                    last_error = model_error
                    # If model is decommissioned or unavailable, try next one
                    error_str = str(model_error).lower()
                    if "decommissioned" in error_str or "not found" in error_str or "invalid" in error_str:
                        print(f"⚠️ Model {model} unavailable, trying fallback...")
                        continue
                    else:
                        # For other errors (rate limit, auth, etc.), don't retry
                        raise
            
            # If all models failed, raise the last error
            if last_error:
                raise last_error
                
        else:
            # Use OpenAI API (version 0.28.1 style)
            import openai
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
            
    except Exception as e:
        print(f"❌ AI API error ({ai_provider}): {e}")
        print(f"Error details: {type(e).__name__}: {str(e)}")
        return None


def detect_language(text: str) -> str:
    """
    Detect if text is primarily Hindi, Hinglish, or English
    Returns: 'hindi', 'hinglish', or 'english'
    """
    # Simple detection based on Devanagari script
    devanagari_chars = sum(1 for char in text if '\u0900' <= char <= '\u097F')
    total_chars = len([c for c in text if c.isalpha()])
    
    if total_chars == 0:
        return 'english'
    
    devanagari_ratio = devanagari_chars / total_chars if total_chars > 0 else 0
    
    if devanagari_ratio > 0.3:
        return 'hindi'
    elif devanagari_ratio > 0.1:
        return 'hinglish'
    else:
        return 'english'


async def solve_doubt(
    question: str, 
    subject: Optional[Subject] = None, 
    class_level: Optional[ClassLevel] = None, 
    chapter: Optional[str] = None,
    target_language: Optional[str] = None
) -> str:
    """
    Professional Indian exam-focused teacher AI.
    Strict, exam-oriented, no jokes or motivational speeches.
    Responds in the SAME language as the input (Hindi/Hinglish/English).
    """
    # Detect input language if not provided
    detected_lang = target_language or detect_language(question)
    print(f"Detected language: {detected_lang}")
    
    # Strict study mode: Reject vague questions without chapter/subject
    is_vague = not chapter and not subject
    vague_keywords = ['samajh nahi aa raha', 'nahi aa raha', 'confuse', 'pata nahi', 'kya hai', 'kaise kare']
    is_vague_query = any(keyword in question.lower() for keyword in vague_keywords)
    
    if is_vague and is_vague_query:
        if detected_lang == 'hindi':
            return "अध्याय specify करो। General doubts allowed नहीं हैं। Board exam ke liye specific question पूछो।"
        elif detected_lang == 'hinglish':
            return "Chapter specify karo. General doubts allowed nahi hain. Board exam ke liye specific question pucho."
        else:
            return "Specify the chapter. General doubts are not allowed. Ask specific questions for board exam preparation."
    
    # Professional exam-focused teacher system prompt
    if detected_lang == 'hindi':
        system_prompt = """आप एक professional Indian board exam teacher और examiner हैं। छात्र की भाषा में उत्तर दें।

नियम:
- हमेशा exam-oriented उत्तर दो
- जोक्स या motivation नहीं
- केवल marks, rank, और performance
- Board checking pattern based
- Strict और professional tone
- Emojis नहीं
- Practical preparation advice

Format: Concept, Formula, Stepwise solution, Final answer, Exam tip"""
        
        prompt = f"""Board exam ke liye professional teacher ki tarah doubt solve karo (Hindi mein):

प्रश्न: {question}
विषय: {subject.value if subject else 'निर्दिष्ट नहीं'}
कक्षा: {class_level.value if class_level else 'निर्दिष्ट नहीं'}
अध्याय: {chapter if chapter else 'निर्दिष्ट नहीं'}

इस exact format में उत्तर दो (Teacher personality):

1. Concept Explanation (संक्षिप्त लेकिन clear)
2. Formula / Rule (यदि applicable - with notation)
3. Example या PYQ Link (इससे similar PYQ कहाँ से आता है)
4. Exam Tip (Board checking में क्या देखेंगे, marks कैसे मिलेंगे)
5. Student Advice (इस topic को कैसे revise करें, कौन सी mistakes avoid करें)

Confident teacher की तरह answer करो। No "AI language model" talk।"""
        
    elif detected_lang == 'hinglish':
        system_prompt = """You are a professional Indian board exam teacher and examiner. Reply in student's language.

Rules:
- Always exam-oriented
- No jokes or motivation
- Only marks, rank, performance
- Board checking pattern based
- Strict professional tone
- No emojis
- Practical preparation advice

Format: Concept, Formula, Stepwise solution, Final answer, Exam tip"""
        
        prompt = f"""Board exam ke liye professional teacher ki tarah doubt solve karo (Hinglish mein):

Question: {question}
Subject: {subject.value if subject else 'Not specified'}
Class: {class_level.value if class_level else 'Not specified'}
Chapter: {chapter if chapter else 'Not specified'}

Is exact format mein answer do (Teacher personality):

1. Concept Explanation (Clear but short)
2. Formula / Rule (If applicable - with proper notation)
3. Example ya PYQ Link (Isse similar PYQ kahan se aata hai)
4. Exam Tip (Board checking mein kya dekhenge, marks kaise milenge)
5. Student Advice (Is topic ko kaise revise kare, kaun si mistakes avoid kare)

Confident teacher ki tarah answer karo. No "AI language model" talk."""
        
    else:  # English
        system_prompt = """You are a professional Indian board exam teacher and examiner. Reply in student's language.

Rules:
- Always exam-oriented
- No jokes or motivational speeches
- Only marks, rank, and performance
- Board checking pattern based
- Strict professional tone
- No emojis
- Practical preparation advice

Format: Concept, Formula, Stepwise solution, Final answer, Exam tip"""

        prompt = f"""Solve this doubt as a professional board exam teacher (English):

Question: {question}
Subject: {subject.value if subject else 'Not specified'}
Class: {class_level.value if class_level else 'Not specified'}
Chapter: {chapter if chapter else 'Not specified'}

Provide answer in this exact format (Teacher personality):

1. Concept Explanation (Clear but concise)
2. Formula / Rule (If applicable - with proper notation)
3. Example or PYQ Link (Where similar PYQ comes from)
4. Exam Tip (What board examiner checks, how marks are awarded)
5. Student Advice (How to revise this topic, which mistakes to avoid)

Answer as a confident teacher. No "AI language model" disclaimers."""

    response = await _call_ai(prompt, system_prompt)
    
    if response:
        # Verify response language matches detected language
        response_lang = detect_language(response)
        
        # If language doesn't match, log for debugging (system prompt should handle it)
        if response_lang != detected_lang and detected_lang != 'english':
            print(f"⚠️ Language mismatch: Expected {detected_lang}, got {response_lang}")
        
        return response
    
    # Fallback response in detected language (professional teacher tone)
    if detected_lang == 'hindi':
        return f"""प्रश्न: {question}

{subject.value if subject else 'विषय'}, कक्षा {class_level.value if class_level else ''} - {chapter if chapter else 'अध्याय निर्दिष्ट नहीं'}

[AI service configure करें। GROQ_API_KEY या OPENAI_API_KEY required।]

Board exam format:
1. Concept
2. Formula (if applicable)
3. Stepwise Solution
4. Final Answer
5. Exam Tip"""
    elif detected_lang == 'hinglish':
        return f"""Question: {question}

{subject.value if subject else 'Subject'}, Class {class_level.value if class_level else ''} - {chapter if chapter else 'Chapter not specified'}

[AI service configure karo. GROQ_API_KEY or OPENAI_API_KEY required.]

Board exam format:
1. Concept
2. Formula (if applicable)
3. Stepwise Solution
4. Final Answer
5. Exam Tip"""
    else:  # English
        return f"""Question: {question}

{subject.value if subject else 'Subject'}, Class {class_level.value if class_level else ''} - {chapter if chapter else 'Chapter not specified'}

[AI service not configured. Configure GROQ_API_KEY or OPENAI_API_KEY.]

Board exam format:
1. Concept
2. Formula (if applicable)
3. Stepwise Solution
4. Final Answer
5. Exam Tip"""


async def generate_important_questions(
    subject: Subject, 
    class_level: ClassLevel, 
    chapter: str, 
    count: int = 10
) -> str:
    """
    Generate important PYQ-based questions for exam preparation
    Exam-focused, board pattern based
    """
    try:
        subject_value = subject.value if hasattr(subject, 'value') else str(subject)
        class_level_value = class_level.value if hasattr(class_level, 'value') else str(class_level)
    except (AttributeError, TypeError) as e:
        print(f"Error accessing enum values: {e}")
        subject_value = str(subject)
        class_level_value = str(class_level)
    
    system_prompt = """You are a professional board exam teacher and paper setter. Generate exam-focused questions based on PYQ patterns.
No jokes. Only marks-oriented questions. Board checking pattern."""

    prompt = f"""Generate {count} important board exam questions (PYQ pattern based):

Subject: {subject_value}
Class: {class_level_value}
Chapter: {chapter}

Requirements:
1. Questions repeatedly asked in board exams
2. High weightage topics
3. Numerical problems (if applicable)
4. Application-based questions
5. Questions matching board paper pattern

Format each question with:
- Question number
- Question type (1 mark / 3 marks / 5 marks)
- Expected answer length
- Marks distribution

No motivation. Only exam-focused questions."""

    response = await _call_ai(prompt, system_prompt)
    
    if response:
        return response
    
    return f"""Important Questions - {subject_value}, Class {class_level_value}, Chapter: {chapter}

[AI-generated PYQ-based questions would appear here. Configure GROQ_API_KEY or OPENAI_API_KEY.]

Format: Question type, marks, expected answer length"""


async def find_pyq_patterns(
    exam_type: str, 
    subject: Optional[Subject] = None, 
    year_range: Optional[str] = None
) -> str:
    """
    PYQ Intelligence System - Analyze patterns for exam prediction
    Exam-focused, pattern-based analysis
    """
    system_prompt = """You are a professional board examiner analyzing PYQ patterns. Identify repeated concepts, high weightage chapters, and exam trends.
No motivational content. Only marks-oriented analysis."""

    prompt = f"""PYQ Pattern Analysis (Board Examiner Perspective):

Exam: {exam_type}
Subject: {subject.value if subject else 'All subjects'}
Year Range: {year_range if year_range else 'Last 5 years'}

Provide analysis in this format:

1. Chapter Importance: High / Medium / Low
2. Times Asked Earlier (frequency count)
3. Probability in Next Exam (percentage)
4. Preparation Strategy (specific action items)

For each topic:
- Chapter name
- Importance level
- Frequency count
- Prediction for next exam
- How to prepare (specific steps)

No general tips. Only exam-focused strategies."""

    response = await _call_ai(prompt, system_prompt)
    
    if response:
        return response
    
    return f"""PYQ Pattern Analysis - {exam_type}

[Pattern analysis would appear here. Configure GROQ_API_KEY or OPENAI_API_KEY.]

Format: Chapter importance, frequency, probability, preparation strategy"""


async def get_step_by_step_solution(
    problem: str, 
    subject: Optional[Subject] = None
) -> str:
    """
    Professional teacher providing step-by-step solution
    Exam-oriented with PYQ connections
    """
    system_prompt = """You are a professional Indian exam teacher. Provide step-by-step solutions with exam focus.
Never say "as an AI" or "I think". Answer as a confident teacher who knows board patterns."""

    prompt = f"""Solve this problem step-by-step (Board exam teacher style):

Problem: {problem}
Subject: {subject.value if subject else 'Not specified'}

Provide in this format:

1. Concept Explanation (What concept is used)
2. Formula / Rule (With notation)
3. Given Information (दिया गया / Given)
4. What to Find (ज्ञात करना है / To Find)
5. Step-by-Step Solution (Clear steps with reasoning)
6. Final Answer
7. PYQ Connection (Similar question appeared in which exam, year)
8. Exam Tip (How board examiner checks this type)

Answer confidently as a teacher. No disclaimers."""

    response = await _call_ai(prompt, system_prompt)
    
    if response:
        return response
    
    return f"""Step-by-Step Solution:

Problem: {problem}

[Detailed solution will appear here. Configure GROQ_API_KEY or OPENAI_API_KEY.]

Format: Concept → Formula → Steps → Answer → PYQ Link → Exam Tip"""


async def get_career_guidance(
    query: str, 
    guidance_type: Optional[str] = None
) -> str:
    """
    Professional career counselor - SchoolSharthi style
    Always includes: Eligibility → Preparation → Time → Salary → Strategy
    """
    detected_lang = detect_language(query)
    
    system_prompt = """You are a professional Indian career counselor with deep knowledge of:
- Government schemes and scholarships
- Exam patterns (NEET, JEE, SSC, Railway, Banking)
- Career paths for rural and urban students
- Financial constraints and solutions

Answer as a confident counselor. Never say "as an AI" or "I think". Give specific, actionable guidance."""

    guidance_contexts = {
        "stream_selection": "Stream selection after 10th: Science vs Commerce vs Arts. Include eligibility, career scope, and government colleges.",
        "career_roadmap_12th": "Career roadmap after 12th: Degree vs Diploma vs Skill courses. Include time, cost, and job prospects.",
        "neet_jee_strategy": "NEET/JEE strategy: Preparation timeline, important topics, free resources, government colleges, cutoffs, alternative paths.",
        "govt_exams": "Government exams: SSC, Railway, Banking. Include eligibility, age limits, syllabus, preparation time, salary, growth.",
        "skill_based": "Skill-based careers: ITI, vocational courses. Include duration, cost, job opportunities, government schemes, local scope."
    }
    
    context = guidance_contexts.get(guidance_type, "") if guidance_type else ""
    
    if detected_lang == 'hindi':
        prompt = f"""Career Guidance (Hindi mein professional counselor ki tarah):

Query: {query}
{context}

इस exact format में answer दो:

1. Eligibility (क्या criteria चाहिए - age, qualification, percentage)
2. Preparation Path (कैसे तैयारी करें - step by step)
3. Time Required (कितना समय लगेगा - months/years)
4. Salary Scope (कितना package मिल सकता है - starting और growth)
5. Best Strategy (सबसे अच्छा रास्ता क्या है - specific action plan)

Government schemes, scholarships, और free resources भी बताओ।
Confident counselor की तरह answer करो।"""
    elif detected_lang == 'hinglish':
        prompt = f"""Career Guidance (Hinglish mein professional counselor ki tarah):

Query: {query}
{context}

Is exact format mein answer do:

1. Eligibility (Kya criteria chahiye - age, qualification, percentage)
2. Preparation Path (Kaise preparation kare - step by step)
3. Time Required (Kitna time lagega - months/years)
4. Salary Scope (Kitna package mil sakta hai - starting aur growth)
5. Best Strategy (Sabse achha rasta kya hai - specific action plan)

Government schemes, scholarships, aur free resources bhi batao.
Confident counselor ki tarah answer karo."""
    else:
        prompt = f"""Career Guidance (Professional counselor style):

Query: {query}
{context}

Provide answer in this exact format:

1. Eligibility (Required criteria - age, qualification, percentage)
2. Preparation Path (How to prepare - step by step)
3. Time Required (Duration needed - months/years)
4. Salary Scope (Package range - starting and growth potential)
5. Best Strategy (Optimal path - specific action plan)

Include government schemes, scholarships, and free resources.
Answer as a confident counselor with specific guidance."""

    response = await _call_ai(prompt, system_prompt)
    
    if response:
        return response
    
    if detected_lang == 'hindi':
        return f"""Career Guidance: {query}

[Detailed guidance यहाँ appear होगी। GROQ_API_KEY या OPENAI_API_KEY configure करें।]

Format: Eligibility → Preparation → Time → Salary → Strategy"""
    elif detected_lang == 'hinglish':
        return f"""Career Guidance: {query}

[Detailed guidance yahan appear hogi. GROQ_API_KEY or OPENAI_API_KEY configure karo.]

Format: Eligibility → Preparation → Time → Salary → Strategy"""
    else:
        return f"""Career Guidance: {query}

[Detailed guidance will appear here. Configure GROQ_API_KEY or OPENAI_API_KEY.]

Format: Eligibility → Preparation → Time → Salary → Strategy"""
