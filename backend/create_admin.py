"""
Script to create an admin user
Usage: python create_admin.py
"""
from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash

def create_admin():
    db = SessionLocal()
    
    # Check if admin already exists
    existing_admin = db.query(User).filter(User.username == "admin").first()
    if existing_admin:
        print("Admin user already exists!")
        db.close()
        return
    
    # Create admin user
    admin = User(
        email="admin@schoolsharthi.com",
        username="admin",
        hashed_password=get_password_hash("admin123"),  # Change this password!
        role="admin",
        is_active=True,
        full_name="Admin User"
    )
    
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    print("Admin user created successfully!")
    print(f"Username: admin")
    print(f"Password: admin123")
    print("⚠️  Please change the password after first login!")
    
    db.close()

if __name__ == "__main__":
    create_admin()
