-- SchoolSharthi Database Schema
-- PostgreSQL Database Schema

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'student' CHECK (role IN ('student', 'admin')),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Notes Table
CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    class_level VARCHAR(10) NOT NULL CHECK (class_level IN ('6', '7', '8', '9', '10', '11', '12')),
    subject VARCHAR(50) NOT NULL CHECK (subject IN ('physics', 'chemistry', 'biology', 'mathematics')),
    chapter VARCHAR(255) NOT NULL,
    description TEXT,
    file_url VARCHAR(500) NOT NULL,
    thumbnail_url VARCHAR(500),
    uploaded_by INTEGER REFERENCES users(id),
    views_count INTEGER DEFAULT 0,
    download_count INTEGER DEFAULT 0,
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- PYQs Table
CREATE TABLE IF NOT EXISTS pyqs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    exam_type VARCHAR(50) NOT NULL CHECK (exam_type IN ('boards', 'neet', 'jee_main', 'jee_advanced')),
    year INTEGER NOT NULL,
    class_level VARCHAR(10) CHECK (class_level IN ('6', '7', '8', '9', '10', '11', '12')),
    subject VARCHAR(50) CHECK (subject IN ('physics', 'chemistry', 'biology', 'mathematics')),
    question_paper_url VARCHAR(500),
    answer_key_url VARCHAR(500),
    solution_url VARCHAR(500),
    uploaded_by INTEGER REFERENCES users(id),
    views_count INTEGER DEFAULT 0,
    download_count INTEGER DEFAULT 0,
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Doubts Table
CREATE TABLE IF NOT EXISTS doubts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    question TEXT NOT NULL,
    subject VARCHAR(50) CHECK (subject IN ('physics', 'chemistry', 'biology', 'mathematics')),
    class_level VARCHAR(10) CHECK (class_level IN ('6', '7', '8', '9', '10', '11', '12')),
    chapter VARCHAR(255),
    ai_response TEXT,
    is_resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Career Queries Table
CREATE TABLE IF NOT EXISTS career_queries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    query TEXT NOT NULL,
    ai_response TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_notes_class_subject ON notes(class_level, subject);
CREATE INDEX IF NOT EXISTS idx_notes_approved ON notes(is_approved);
CREATE INDEX IF NOT EXISTS idx_pyqs_exam_year ON pyqs(exam_type, year);
CREATE INDEX IF NOT EXISTS idx_pyqs_approved ON pyqs(is_approved);
CREATE INDEX IF NOT EXISTS idx_doubts_user ON doubts(user_id);
CREATE INDEX IF NOT EXISTS idx_career_queries_user ON career_queries(user_id);
