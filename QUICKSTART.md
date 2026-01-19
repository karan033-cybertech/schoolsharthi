# Quick Start Guide

Get SchoolSharthi up and running in 5 minutes!

## Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL (or use Docker)

## Option 1: Manual Setup (Recommended for Development)

### Step 1: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your settings (at minimum, set DATABASE_URL)

# Initialize database
python init_db.py

# Create admin user
python create_admin.py

# Start server
python run.py
```

Backend will run at `http://localhost:8000`

### Step 2: Frontend Setup

```bash
# Navigate to frontend (in a new terminal)
cd frontend

# Install dependencies
npm install

# Create .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start development server
npm run dev
```

Frontend will run at `http://localhost:3000`

### Step 3: Access the Application

1. Open `http://localhost:3000` in your browser
2. Register a new account or login with admin credentials:
   - Username: `admin`
   - Password: `admin123`

## Option 2: Docker Setup (Easier)

```bash
# Start all services
docker-compose up -d

# Initialize database (first time only)
docker-compose exec backend python init_db.py
docker-compose exec backend python create_admin.py

# View logs
docker-compose logs -f
```

Access:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

## First Steps After Setup

1. **Login as Admin**
   - Go to `/login`
   - Use credentials: `admin` / `admin123`
   - ⚠️ Change password immediately!

2. **Upload Your First Note**
   - Go to `/admin`
   - Click "Upload Note" tab
   - Fill in the form and upload a PDF/image

3. **Browse Notes**
   - Go to `/notes`
   - Filter by class, subject, or chapter
   - Download notes

4. **Test AI Features**
   - Go to `/ai-doubt` and ask a question
   - Go to `/career` for career guidance

## Troubleshooting

### Backend won't start
- Check PostgreSQL is running: `pg_isready`
- Verify DATABASE_URL in `.env`
- Check port 8000 is not in use

### Frontend won't start
- Check Node.js version: `node --version` (should be 18+)
- Delete `node_modules` and run `npm install` again
- Check port 3000 is not in use

### Database connection error
- Ensure PostgreSQL is running
- Check database exists: `psql -l | grep schoolsharthi`
- Verify credentials in DATABASE_URL

### CORS errors
- Ensure backend CORS allows `http://localhost:3000`
- Check NEXT_PUBLIC_API_URL matches backend URL

## Next Steps

- Read [SETUP.md](SETUP.md) for detailed configuration
- Read [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for architecture details
- Configure AWS S3 for file storage (see README.md)
- Configure OpenAI API for AI features (see README.md)

## Need Help?

- Check API documentation at `http://localhost:8000/docs`
- Review error logs in terminal
- Check database connection and tables
