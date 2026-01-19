from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    STUDENT = "student"
    ADMIN = "admin"


class ClassLevel(str, enum.Enum):
    CLASS_6 = "6"
    CLASS_7 = "7"
    CLASS_8 = "8"
    CLASS_9 = "9"
    CLASS_10 = "10"
    CLASS_11 = "11"
    CLASS_12 = "12"


class Subject(str, enum.Enum):
    PHYSICS = "physics"
    CHEMISTRY = "chemistry"
    BIOLOGY = "biology"
    MATHEMATICS = "mathematics"


class ExamType(str, enum.Enum):
    BOARDS = "boards"
    NEET = "neet"
    JEE_MAIN = "jee_main"
    JEE_ADVANCED = "jee_advanced"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(SQLEnum(UserRole), default=UserRole.STUDENT)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    class_level = Column(SQLEnum(ClassLevel), nullable=False)
    subject = Column(SQLEnum(Subject), nullable=False)
    chapter = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    file_url = Column(String, nullable=False)  # S3 URL
    thumbnail_url = Column(String, nullable=True)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    views_count = Column(Integer, default=0)
    download_count = Column(Integer, default=0)
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    uploader = relationship("User", backref="notes")


class PYQ(Base):
    __tablename__ = "pyqs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    exam_type = Column(SQLEnum(ExamType), nullable=False)
    year = Column(Integer, nullable=False)
    class_level = Column(SQLEnum(ClassLevel), nullable=True)
    subject = Column(SQLEnum(Subject), nullable=True)
    question_paper_url = Column(String, nullable=True)  # S3 URL
    answer_key_url = Column(String, nullable=True)  # S3 URL
    solution_url = Column(String, nullable=True)  # S3 URL
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    views_count = Column(Integer, default=0)
    download_count = Column(Integer, default=0)
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    uploader = relationship("User", backref="pyqs")


class Doubt(Base):
    __tablename__ = "doubts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question = Column(Text, nullable=False)
    subject = Column(SQLEnum(Subject), nullable=True)
    class_level = Column(SQLEnum(ClassLevel), nullable=True)
    chapter = Column(String, nullable=True)
    detected_language = Column(String, default='english')  # 'hindi', 'hinglish', 'english'
    ai_response = Column(Text, nullable=True)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="doubts")


class CareerQuery(Base):
    __tablename__ = "career_queries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    query = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="career_queries")


class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    subject = Column(SQLEnum(Subject), nullable=True)
    class_level = Column(SQLEnum(ClassLevel), nullable=True)
    exam_type = Column(SQLEnum(ExamType), nullable=True)
    duration_minutes = Column(Integer, default=60)  # Exam duration in minutes
    total_questions = Column(Integer, default=30)
    status = Column(String, default="pending")  # pending, in_progress, completed, submitted
    started_at = Column(DateTime(timezone=True), nullable=True)
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="exams")


class ExamQuestion(Base):
    __tablename__ = "exam_questions"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    question_number = Column(Integer, nullable=False)
    question_text = Column(Text, nullable=False)
    options = Column(Text, nullable=True)  # JSON string: ["option1", "option2", ...]
    correct_answer = Column(String, nullable=True)  # Option index or text
    marks = Column(Integer, default=1)
    difficulty = Column(String, default="medium")  # easy, medium, hard

    exam = relationship("Exam", backref="questions")


class ExamAttempt(Base):
    __tablename__ = "exam_attempts"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("exam_questions.id"), nullable=False)
    selected_answer = Column(String, nullable=True)
    is_correct = Column(Boolean, default=False)
    time_spent_seconds = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    exam = relationship("Exam", backref="attempts")
    question = relationship("ExamQuestion", backref="attempts")


class ExamResult(Base):
    __tablename__ = "exam_results"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False, unique=True)
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, default=0)
    wrong_answers = Column(Integer, default=0)
    unanswered = Column(Integer, default=0)
    total_marks = Column(Integer, default=0)
    obtained_marks = Column(Integer, default=0)
    percentage = Column(Integer, default=0)
    weak_topics = Column(Text, nullable=True)  # JSON string of weak topics
    performance_analysis = Column(Text, nullable=True)  # AI-generated analysis
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    exam = relationship("Exam", backref="result", uselist=False)
