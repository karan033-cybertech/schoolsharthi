-- Database Migration Script for AI Power Upgrades
-- Run this script to update your database schema

-- ============================================
-- Feature 1: Smart Language Engine
-- ============================================

-- Add detected_language field to doubts table
ALTER TABLE doubts 
ADD COLUMN IF NOT EXISTS detected_language VARCHAR(20) DEFAULT 'english';

-- Add index for faster language-based queries
CREATE INDEX IF NOT EXISTS idx_doubts_language ON doubts(detected_language);

-- ============================================
-- Feature 5: Exam Mode
-- ============================================

-- Create exams table
CREATE TABLE IF NOT EXISTS exams (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    subject VARCHAR(50) CHECK (subject IN ('physics', 'chemistry', 'biology', 'mathematics')),
    class_level VARCHAR(10) CHECK (class_level IN ('6', '7', '8', '9', '10', '11', '12')),
    exam_type VARCHAR(50) CHECK (exam_type IN ('boards', 'neet', 'jee_main', 'jee_advanced')),
    duration_minutes INTEGER DEFAULT 60,
    total_questions INTEGER DEFAULT 30,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'completed', 'submitted')),
    started_at TIMESTAMP WITH TIME ZONE,
    submitted_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create exam_questions table
CREATE TABLE IF NOT EXISTS exam_questions (
    id SERIAL PRIMARY KEY,
    exam_id INTEGER NOT NULL REFERENCES exams(id) ON DELETE CASCADE,
    question_number INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    options TEXT, -- JSON string: ["option1", "option2", ...]
    correct_answer VARCHAR(255),
    marks INTEGER DEFAULT 1,
    difficulty VARCHAR(20) DEFAULT 'medium' CHECK (difficulty IN ('easy', 'medium', 'hard')),
    CONSTRAINT unique_exam_question_number UNIQUE (exam_id, question_number)
);

-- Create exam_attempts table
CREATE TABLE IF NOT EXISTS exam_attempts (
    id SERIAL PRIMARY KEY,
    exam_id INTEGER NOT NULL REFERENCES exams(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL REFERENCES exam_questions(id) ON DELETE CASCADE,
    selected_answer VARCHAR(255),
    is_correct BOOLEAN DEFAULT FALSE,
    time_spent_seconds INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_exam_question_attempt UNIQUE (exam_id, question_id)
);

-- Create exam_results table
CREATE TABLE IF NOT EXISTS exam_results (
    id SERIAL PRIMARY KEY,
    exam_id INTEGER NOT NULL REFERENCES exams(id) ON DELETE CASCADE UNIQUE,
    total_questions INTEGER NOT NULL,
    correct_answers INTEGER DEFAULT 0,
    wrong_answers INTEGER DEFAULT 0,
    unanswered INTEGER DEFAULT 0,
    total_marks INTEGER DEFAULT 0,
    obtained_marks INTEGER DEFAULT 0,
    percentage INTEGER DEFAULT 0,
    weak_topics TEXT, -- JSON string of weak topics
    performance_analysis TEXT, -- AI-generated analysis
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_exams_user ON exams(user_id);
CREATE INDEX IF NOT EXISTS idx_exams_status ON exams(status);
CREATE INDEX IF NOT EXISTS idx_exam_questions_exam ON exam_questions(exam_id);
CREATE INDEX IF NOT EXISTS idx_exam_attempts_exam ON exam_attempts(exam_id);
CREATE INDEX IF NOT EXISTS idx_exam_attempts_question ON exam_attempts(question_id);
CREATE INDEX IF NOT EXISTS idx_exam_results_exam ON exam_results(exam_id);

-- Add comments for documentation
COMMENT ON TABLE exams IS 'Stores exam records for students';
COMMENT ON TABLE exam_questions IS 'Stores questions for each exam';
COMMENT ON TABLE exam_attempts IS 'Stores student answers for exam questions';
COMMENT ON TABLE exam_results IS 'Stores exam results and performance analytics';
COMMENT ON COLUMN doubts.detected_language IS 'Language detected from student question: hindi, hinglish, or english';

-- ============================================
-- Migration Complete
-- ============================================

-- Verify tables created
SELECT 
    table_name 
FROM 
    information_schema.tables 
WHERE 
    table_schema = 'public' 
    AND table_name IN ('exams', 'exam_questions', 'exam_attempts', 'exam_results')
ORDER BY 
    table_name;
