# How to Run SchoolSharthi

## Quick Start

### Option 1: Using Batch Files (Windows)

1. **Start Backend:**
   - Double-click `start_backend.bat`
   - Or run: `start_backend.bat` in terminal
   - Backend will run at: http://localhost:8000

2. **Start Frontend:**
   - Open a NEW terminal window
   - Double-click `start_frontend.bat`
   - Or run: `start_frontend.bat` in terminal
   - Frontend will run at: http://localhost:3000

### Option 2: Manual Start

#### Backend:
```powershell
cd backend
.\venv\Scripts\activate
python run.py
```

#### Frontend (in a new terminal):
```powershell
cd frontend
npm run dev
```

## Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## First Time Setup

### 1. Database Setup

If you haven't set up PostgreSQL yet:

**Option A: Using SQLite (for quick testing)**
- The app will create tables automatically on first run
- No additional setup needed

**Option B: Using PostgreSQL**
1. Install PostgreSQL
2. Create database:
   ```sql
   CREATE DATABASE schoolsharthi;
   ```
3. Update `backend/.env`:
   ```
   DATABASE_URL=postgresql://postgres:password@localhost:5432/schoolsharthi
   ```
4. Run migrations:
   ```powershell
   cd backend
   .\venv\Scripts\activate
   python init_db.py
   ```

### 2. Create Admin User

After database is set up:
```powershell
cd backend
.\venv\Scripts\activate
python create_admin.py
```

Default admin credentials:
- Username: `admin`
- Password: `admin123`
- ⚠️ Change password after first login!

### 3. Environment Variables

Create `backend/.env` file:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/schoolsharthi
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=ap-south-1
S3_BUCKET_NAME=schoolsharthi-notes
OPENAI_API_KEY=
```

**Note:** For local development, AWS and OpenAI keys are optional. The app will work with placeholder responses.

## Troubleshooting

### Backend won't start
- Check if port 8000 is available
- Verify Python virtual environment is activated
- Check `backend/.env` file exists
- View error messages in terminal

### Frontend won't start
- Check if port 3000 is available
- Verify `node_modules` exists (run `npm install`)
- Check `frontend/.env.local` exists with:
  ```
  NEXT_PUBLIC_API_URL=http://localhost:8000
  ```

### Database connection error
- Verify PostgreSQL is running
- Check DATABASE_URL in `.env`
- Ensure database exists

### CORS errors
- Verify backend CORS allows `http://localhost:3000`
- Check `NEXT_PUBLIC_API_URL` matches backend URL

## Testing the Application

1. **Register a new user:**
   - Go to http://localhost:3000/register
   - Create an account

2. **Login:**
   - Go to http://localhost:3000/login
   - Use your credentials

3. **Explore features:**
   - Dashboard: http://localhost:3000/dashboard
   - Notes: http://localhost:3000/notes
   - PYQs: http://localhost:3000/pyqs
   - AI Doubt Solver: http://localhost:3000/ai-doubt
   - AI Assistant: http://localhost:3000/ai-assistant
   - Career Guidance: http://localhost:3000/career

4. **Admin Panel:**
   - Login as admin
   - Go to http://localhost:3000/admin
   - Upload notes and PYQs

## API Testing

Visit http://localhost:8000/docs for interactive API documentation (Swagger UI)

## Stopping the Servers

- Press `Ctrl+C` in each terminal window
- Or close the terminal windows

## Next Steps

- Configure AWS S3 for file uploads (optional)
- Add OpenAI API key for AI features (optional)
- Set up production database
- Deploy to AWS/Vercel (see DEPLOYMENT_PLAN.md)

## Need Help?

- Check API docs: http://localhost:8000/docs
- Review error messages in terminal
- Check logs in backend terminal
- Verify all environment variables are set
