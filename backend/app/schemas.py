from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models import ClassLevel, Subject, ExamType, UserRole


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = None  # Optional role, defaults to STUDENT if not provided


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


# Note Schemas
class NoteBase(BaseModel):
    title: str
    class_level: ClassLevel
    subject: Subject
    chapter: str
    description: Optional[str] = None


class NoteCreate(NoteBase):
    pass


class NoteResponse(NoteBase):
    id: int
    file_url: str
    thumbnail_url: Optional[str]
    uploaded_by: int
    views_count: int
    download_count: int
    is_approved: bool
    created_at: datetime

    class Config:
        from_attributes = True


# PYQ Schemas
class PYQBase(BaseModel):
    title: str
    exam_type: ExamType
    year: int
    class_level: Optional[ClassLevel] = None
    subject: Optional[Subject] = None


class PYQCreate(PYQBase):
    pass


class PYQResponse(PYQBase):
    id: int
    question_paper_url: Optional[str]
    answer_key_url: Optional[str]
    solution_url: Optional[str]
    uploaded_by: int
    views_count: int
    download_count: int
    is_approved: bool
    created_at: datetime

    class Config:
        from_attributes = True


# AI Doubt Schema
class DoubtCreate(BaseModel):
    question: str
    subject: Optional[Subject] = None
    class_level: Optional[ClassLevel] = None
    chapter: Optional[str] = None


class DoubtResponse(BaseModel):
    id: int
    question: str
    detected_language: Optional[str] = 'english'
    ai_response: Optional[str]
    is_resolved: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Important Questions Schema
class ImportantQuestionsRequest(BaseModel):
    subject: Subject
    class_level: ClassLevel
    chapter: str
    count: Optional[int] = 10


class ImportantQuestionsResponse(BaseModel):
    questions: str
    subject: Subject
    class_level: ClassLevel
    chapter: str


# PYQ Pattern Schema
class PYQPatternRequest(BaseModel):
    exam_type: ExamType
    subject: Optional[Subject] = None
    year_range: Optional[str] = None


class PYQPatternResponse(BaseModel):
    patterns: str
    exam_type: ExamType
    subject: Optional[Subject] = None


# Step-by-Step Solution Schema
class StepByStepSolutionRequest(BaseModel):
    problem: str
    subject: Optional[Subject] = None


class StepByStepSolutionResponse(BaseModel):
    solution: str
    problem: str


# Career Guidance Schema
class CareerQueryCreate(BaseModel):
    query: str
    guidance_type: Optional[str] = None  # stream_selection, career_roadmap_12th, neet_jee_strategy, govt_exams, skill_based


class CareerQueryResponse(BaseModel):
    id: int
    query: str
    ai_response: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
