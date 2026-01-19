# SchoolSharthi Project Structure

## Overview

Complete Indian education platform with backend (FastAPI) and frontend (Next.js).

## Directory Structure

```
schoolsharthi/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI application entry point
│   │   ├── config.py           # Configuration and environment variables
│   │   ├── database.py         # Database connection and session management
│   │   ├── models.py           # SQLAlchemy database models
│   │   ├── schemas.py          # Pydantic schemas for request/response
│   │   ├── auth.py             # Authentication utilities (JWT, password hashing)
│   │   ├── routers/            # API route handlers
│   │   │   ├── __init__.py
│   │   │   ├── auth.py         # Authentication routes (register, login)
│   │   │   ├── notes.py        # Notes CRUD operations
│   │   │   ├── pyqs.py         # PYQs CRUD operations
│   │   │   ├── admin.py        # Admin routes (upload, approve, delete)
│   │   │   ├── ai_doubt.py     # AI doubt solver routes
│   │   │   └── career_guidance.py  # Career guidance routes
│   │   └── services/           # Business logic services
│   │       ├── __init__.py
│   │       ├── s3_service.py   # AWS S3 file upload service
│   │       └── ai_service.py   # AI integration (OpenAI)
│   ├── requirements.txt        # Python dependencies
│   ├── run.py                 # Development server runner
│   ├── init_db.py             # Database initialization script
│   ├── create_admin.py        # Admin user creation script
│   ├── alembic.ini            # Alembic configuration (migrations)
│   └── Dockerfile             # Docker configuration for backend
│
├── frontend/                   # Next.js Frontend
│   ├── app/                    # Next.js 14 App Router
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Home page
│   │   ├── globals.css        # Global styles
│   │   ├── providers.tsx     # React Query provider
│   │   ├── login/             # Login page
│   │   ├── register/         # Registration page
│   │   ├── dashboard/         # User dashboard
│   │   ├── notes/             # Notes browsing page
│   │   ├── pyqs/              # PYQs browsing page
│   │   ├── ai-doubt/          # AI doubt solver page
│   │   ├── career/            # Career guidance page
│   │   └── admin/             # Admin panel
│   ├── lib/
│   │   ├── api.ts             # API client (Axios)
│   │   └── store.ts            # Zustand state management
│   ├── package.json           # Node.js dependencies
│   ├── tsconfig.json          # TypeScript configuration
│   ├── tailwind.config.js     # Tailwind CSS configuration
│   ├── next.config.js         # Next.js configuration
│   └── Dockerfile             # Docker configuration for frontend
│
├── database_schema.sql        # PostgreSQL schema SQL
├── docker-compose.yml         # Docker Compose configuration
├── README.md                  # Main project documentation
├── SETUP.md                   # Setup instructions
└── .gitignore                # Git ignore rules

```

## Key Components

### Backend (FastAPI)

#### Models (`app/models.py`)
- **User**: User accounts (student/admin)
- **Note**: Handwritten notes with metadata
- **PYQ**: Previous Year Questions
- **Doubt**: Student doubts with AI responses
- **CareerQuery**: Career guidance queries

#### Routers
- **auth.py**: User registration, login, JWT token management
- **notes.py**: Browse, filter, and download notes
- **pyqs.py**: Browse, filter, and download PYQs
- **admin.py**: Upload notes/PYQs, approve/reject content
- **ai_doubt.py**: Submit doubts, get AI responses
- **career_guidance.py**: Submit career queries, get AI guidance

#### Services
- **s3_service.py**: Handles file uploads to AWS S3
- **ai_service.py**: Integrates with OpenAI for AI features

### Frontend (Next.js)

#### Pages
- **Home**: Landing page with features overview
- **Login/Register**: Authentication pages
- **Dashboard**: User dashboard with navigation
- **Notes**: Browse and filter handwritten notes
- **PYQs**: Browse and filter previous year questions
- **AI Doubt**: Submit questions, view AI responses
- **Career**: Submit career queries, view guidance
- **Admin**: Upload and manage content (admin only)

#### State Management
- **Zustand**: Global auth state
- **React Query**: Server state and caching

## Database Schema

### Tables
1. **users**: User accounts and authentication
2. **notes**: Handwritten notes metadata
3. **pyqs**: Previous year questions metadata
4. **doubts**: Student doubts and AI responses
5. **career_queries**: Career guidance queries and responses

### Relationships
- Notes → Users (uploaded_by)
- PYQs → Users (uploaded_by)
- Doubts → Users (user_id)
- Career Queries → Users (user_id)

## API Endpoints

### Public Endpoints
- `GET /` - API health check
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

### Protected Endpoints (Require JWT)
- `GET /api/auth/me` - Get current user
- `GET /api/notes/` - List notes (with filters)
- `GET /api/notes/{id}` - Get note details
- `POST /api/notes/{id}/download` - Download note
- `GET /api/pyqs/` - List PYQs (with filters)
- `GET /api/pyqs/{id}` - Get PYQ details
- `POST /api/pyqs/{id}/download` - Download PYQ
- `POST /api/ai/doubt` - Submit doubt
- `GET /api/ai/doubts` - Get user doubts
- `POST /api/career/query` - Submit career query
- `GET /api/career/queries` - Get career queries

### Admin Endpoints (Require Admin Role)
- `POST /api/admin/notes/upload` - Upload note
- `POST /api/admin/pyqs/upload` - Upload PYQ
- `GET /api/admin/notes/pending` - Get pending notes
- `POST /api/admin/notes/{id}/approve` - Approve note
- `DELETE /api/admin/notes/{id}` - Delete note

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Relational database
- **JWT**: Authentication tokens
- **Boto3**: AWS SDK for S3
- **OpenAI**: AI integration (optional)

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type safety
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client
- **React Query**: Data fetching and caching
- **Zustand**: State management
- **Lucide React**: Icon library

## Development Workflow

1. **Backend Development**
   - Start PostgreSQL database
   - Set up virtual environment
   - Install dependencies
   - Configure `.env`
   - Initialize database
   - Run development server

2. **Frontend Development**
   - Install Node.js dependencies
   - Configure `.env.local`
   - Run development server
   - Connect to backend API

3. **Database Migrations**
   - Use Alembic for migrations
   - Or run `init_db.py` for initial setup

4. **Testing**
   - Test API endpoints with FastAPI docs (`/docs`)
   - Test frontend in browser
   - Verify authentication flow
   - Test file uploads (if S3 configured)

## Deployment Considerations

1. **Environment Variables**: Set all required env vars
2. **Database**: Use managed PostgreSQL service
3. **S3**: Configure AWS S3 bucket with proper permissions
4. **CORS**: Update CORS settings for production domain
5. **Security**: Use strong SECRET_KEY, enable HTTPS
6. **Scaling**: Consider using Redis for caching, load balancer for multiple instances
