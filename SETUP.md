# SchoolSharthi Setup Guide

## Quick Start

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python init_db.py

# Run server
python run.py
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local
cp .env.local.example .env.local

# Run development server
npm run dev
```

### 3. Database Setup

#### Option A: Using PostgreSQL directly

```bash
# Create database
createdb schoolsharthi

# Run schema
psql schoolsharthi < database_schema.sql
```

#### Option B: Using Docker

```bash
docker run --name schoolsharthi-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=schoolsharthi \
  -p 5432:5432 \
  -d postgres:15
```

### 4. Create Admin User

After setting up the database, create an admin user:

```python
# Run in Python shell or create a script
from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash

db = SessionLocal()
admin = User(
    email="admin@schoolsharthi.com",
    username="admin",
    hashed_password=get_password_hash("admin123"),
    role="admin",
    is_active=True
)
db.add(admin)
db.commit()
```

Or use SQL:

```sql
INSERT INTO users (email, username, hashed_password, role, is_active)
VALUES ('admin@schoolsharthi.com', 'admin', '$2b$12$...', 'admin', true);
```

Note: You'll need to hash the password using bcrypt. Use the Python script above for proper password hashing.

## Environment Variables

### Backend (.env)

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/schoolsharthi
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AWS S3 (Optional - will use placeholder URLs if not configured)
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_REGION=ap-south-1
S3_BUCKET_NAME=schoolsharthi-notes

# OpenAI (Optional - will use placeholder responses if not configured)
OPENAI_API_KEY=your-openai-key
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Testing the Setup

1. Start backend: `cd backend && python run.py`
2. Start frontend: `cd frontend && npm run dev`
3. Visit `http://localhost:3000`
4. Register a new user
5. Login and explore the dashboard

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify database exists: `psql -l | grep schoolsharthi`

### Port Already in Use
- Backend: Change port in `run.py` (default: 8000)
- Frontend: Change port in `package.json` scripts (default: 3000)

### CORS Issues
- Update CORS origins in `backend/app/main.py`
- Ensure frontend URL matches NEXT_PUBLIC_API_URL

### S3 Upload Issues
- If S3 is not configured, placeholder URLs will be used
- For production, configure AWS credentials properly

### AI Features Not Working
- AI features will work with placeholder responses if OpenAI is not configured
- To enable full AI features, add OPENAI_API_KEY to .env
