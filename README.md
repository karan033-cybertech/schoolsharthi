# SchoolSharthi - Indian Education Platform

A complete education platform for Indian school students (Class 6-12) with handwritten notes, PYQs, AI doubt solver, and career guidance.

## Features

- 📚 **Handwritten Notes**: Class-wise and chapter-wise topper notes for Class 6-12
- 📝 **PYQs**: Previous Year Questions for Boards, NEET, and JEE
- 🤖 **AI Doubt Solver**: Get instant answers to academic questions
- 💼 **Career Guidance**: AI-powered career counseling
- 👨‍💼 **Admin Panel**: Upload and manage notes and PYQs
- 🌐 **Rural-Friendly**: Optimized UI for slow connections

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Authentication**: JWT
- **Storage**: AWS S3
- **AI**: OpenAI (configurable)

### Frontend
- **Framework**: Next.js 14
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **API Client**: Axios
- **Forms**: React Hook Form

## Project Structure

```
schoolsharthi/
├── backend/
│   ├── app/
│   │   ├── routers/        # API routes
│   │   ├── services/        # Business logic
│   │   ├── models.py        # Database models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── auth.py          # Authentication utilities
│   │   ├── config.py        # Configuration
│   │   ├── database.py      # Database setup
│   │   └── main.py          # FastAPI app
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── app/                 # Next.js app directory
│   ├── lib/                 # Utilities and API client
│   ├── package.json
│   └── tailwind.config.js
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 12+
- AWS Account (for S3 storage)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
```

5. Update `.env` with your configuration:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/schoolsharthi
SECRET_KEY=your-secret-key-here
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
S3_BUCKET_NAME=schoolsharthi-notes
OPENAI_API_KEY=your-openai-key  # Optional
```

6. Create PostgreSQL database:
```sql
CREATE DATABASE schoolsharthi;
```

7. Run migrations (if using Alembic):
```bash
alembic upgrade head
```

8. Start the server:
```bash
python run.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local` file:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Start development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Notes
- `GET /api/notes/` - Get all notes (with filters)
- `GET /api/notes/{id}` - Get specific note
- `POST /api/notes/{id}/download` - Download note

### PYQs
- `GET /api/pyqs/` - Get all PYQs (with filters)
- `GET /api/pyqs/{id}` - Get specific PYQ
- `POST /api/pyqs/{id}/download` - Download PYQ

### Admin
- `POST /api/admin/notes/upload` - Upload note (Admin only)
- `POST /api/admin/pyqs/upload` - Upload PYQ (Admin only)
- `GET /api/admin/notes/pending` - Get pending notes
- `POST /api/admin/notes/{id}/approve` - Approve note

### AI Features
- `POST /api/ai/doubt` - Ask doubt
- `GET /api/ai/doubts` - Get user doubts
- `POST /api/career/query` - Ask career question
- `GET /api/career/queries` - Get career queries

## Database Schema

### Users
- id, email, username, hashed_password, full_name, role, is_active, created_at

### Notes
- id, title, class_level, subject, chapter, description, file_url, thumbnail_url, uploaded_by, views_count, download_count, is_approved, created_at

### PYQs
- id, title, exam_type, year, class_level, subject, question_paper_url, answer_key_url, solution_url, uploaded_by, views_count, download_count, is_approved, created_at

### Doubts
- id, user_id, question, subject, class_level, ai_response, is_resolved, created_at

### Career Queries
- id, user_id, query, ai_response, created_at

## Development

### Creating Admin User

You can create an admin user directly in the database:

```sql
INSERT INTO users (email, username, hashed_password, role, is_active)
VALUES ('admin@schoolsharthi.com', 'admin', '$2b$12$...', 'admin', true);
```

Or use the registration endpoint and manually update the role in the database.

## Production Deployment

1. Set up environment variables
2. Configure PostgreSQL database
3. Set up AWS S3 bucket with proper permissions
4. Configure CORS in FastAPI for your frontend domain
5. Build frontend: `npm run build`
6. Use a production WSGI server (e.g., Gunicorn) for FastAPI
7. Set up reverse proxy (Nginx) if needed

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
