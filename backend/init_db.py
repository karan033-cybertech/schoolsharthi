"""
Database initialization script
Run this to create all tables
"""
from app.database import engine, Base
from app.models import User, Note, PYQ, Doubt, CareerQuery

def init_db():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()


