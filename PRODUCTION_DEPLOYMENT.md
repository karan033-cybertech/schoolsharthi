# 🚀 Production Deployment Guide - SchoolSharthi

## Pre-Deployment Checklist

### ✅ Frontend (Next.js)
- [x] TypeScript compilation passes
- [x] ESLint warnings fixed (Image components)
- [x] SEO meta tags added
- [x] Security headers configured
- [x] Production Dockerfile created
- [x] Environment variables documented

### ✅ Backend (FastAPI)
- [x] Security headers middleware added
- [x] CORS configured for production
- [x] Health check endpoint enhanced
- [x] Request logging middleware added
- [x] Rate limiting framework added (slowapi)
- [x] Database connection validation in health check
- [x] Production Dockerfile reviewed

### ⚠️ Security
- [x] Hardcoded API key removed (setup_groq_key.py deleted)
- [x] Secrets validation (SECRET_KEY check)
- [x] CORS origins configurable via environment
- [x] Security headers middleware
- [ ] **TODO: Add rate limiting to all auth endpoints** (framework ready, needs decoration)
- [ ] **TODO: Add input sanitization middleware**
- [ ] **TODO: Enable HTTPS/TLS in production**

### ⚠️ Database
- [ ] **TODO: Verify all migrations are applied**
- [ ] **TODO: Create database backup script**
- [ ] **TODO: Verify indexes on frequently queried columns**
- [ ] **TODO: Set up connection pooling**

### ⚠️ Performance
- [x] Pagination implemented in API routes
- [ ] **TODO: Add Redis caching for frequently accessed data**
- [ ] **TODO: Enable query result caching**
- [ ] **TODO: Optimize database queries (add indexes)**

---

## Environment Configuration

### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/schoolsharthi

# JWT - MUST CHANGE IN PRODUCTION
SECRET_KEY=generate-strong-random-key-here-minimum-32-characters

# CORS - Add your frontend domain
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Environment
ENVIRONMENT=production

# AWS S3 (if using file uploads)
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_REGION=ap-south-1
S3_BUCKET_NAME=your-bucket

# AI Keys (optional)
GROQ_API_KEY=your-key
OPENAI_API_KEY=your-key
```

### Frontend (.env.production)
```bash
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

---

## Deployment Steps

### Option 1: Vercel (Frontend) + Render/VPS (Backend)

#### Frontend (Vercel)
```bash
cd frontend

# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod

# Set environment variable in Vercel dashboard:
# NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

#### Backend (Render/VPS)

**Using Render:**
1. Connect GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables in Render dashboard
5. Set `ENVIRONMENT=production`

**Using VPS with Docker:**
```bash
# Build and run
cd backend
docker build -f Dockerfile.prod -t schoolsharthi-backend .
docker run -d \
  --name schoolsharthi-backend \
  -p 8000:8000 \
  --env-file .env \
  schoolsharthi-backend

# With Docker Compose (production)
docker-compose -f docker-compose.prod.yml up -d
```

### Option 2: Full Docker Deployment

```bash
# Clone repository
git clone <repo-url>
cd schoolsharthi

# Create .env files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# Edit .env files with production values

# Build and run
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

---

## Health Checks

### Backend
```bash
# Basic health
curl https://api.yourdomain.com/health

# Expected response:
{
  "status": "healthy",
  "database": "healthy",
  "environment": "production"
}
```

### Frontend
```bash
# Check if frontend is accessible
curl -I https://yourdomain.com
```

---

## Post-Deployment Verification

1. **Test Authentication**
   - Register new user
   - Login
   - Access protected routes

2. **Test API Endpoints**
   - GET /api/notes/
   - GET /api/pyqs/
   - POST /api/ai/doubt (if AI configured)

3. **Check Security Headers**
   ```bash
   curl -I https://api.yourdomain.com
   # Verify: X-Content-Type-Options, X-Frame-Options, etc.
   ```

4. **Monitor Logs**
   ```bash
   # Backend logs (Render/VPS)
   # Check for errors, slow requests (>1s)
   ```

5. **Database Connection**
   - Verify connection pooling
   - Check query performance
   - Monitor connection count

---

## Production Commands

### Backend

```bash
# Start production server (single worker)
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Start with multiple workers (recommended)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# With gunicorn (alternative)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend

```bash
# Build for production
npm run build

# Start production server (standalone mode)
npm start

# Or use Docker
docker build -f Dockerfile.prod -t schoolsharthi-frontend .
docker run -p 3000:3000 --env-file .env.production schoolsharthi-frontend
```

---

## Monitoring & Maintenance

### Logs
- Backend: Check application logs for errors
- Frontend: Check Vercel deployment logs
- Database: Monitor connection pool and query times

### Performance
- Monitor API response times
- Check database query performance
- Review slow request logs (>1s)

### Security
- Regular security updates
- Monitor for suspicious activity
- Review CORS origins regularly
- Rotate SECRET_KEY periodically

---

## Troubleshooting

### Backend not starting
1. Check DATABASE_URL is correct
2. Verify PostgreSQL is accessible
3. Check SECRET_KEY is set
4. Review logs for errors

### CORS errors
1. Verify CORS_ORIGINS includes frontend URL
2. Check frontend NEXT_PUBLIC_API_URL
3. Ensure credentials are set correctly

### Database connection issues
1. Verify DATABASE_URL format
2. Check network connectivity
3. Verify database exists and user has permissions
4. Check connection pool settings

### Frontend build errors
1. Check TypeScript errors: `npm run build`
2. Verify environment variables
3. Check Next.js configuration

---

## Important Security Notes

⚠️ **CRITICAL:**
1. **NEVER** commit `.env` files
2. **CHANGE** default SECRET_KEY before production
3. **LIMIT** CORS_ORIGINS to your domains only
4. **USE** HTTPS/TLS in production (not HTTP)
5. **ENABLE** rate limiting on all public endpoints
6. **VALIDATE** all user inputs
7. **KEEP** dependencies updated

---

## Next Steps (Recommended)

1. Set up CI/CD pipeline (GitHub Actions)
2. Add monitoring (Sentry, DataDog, etc.)
3. Enable database backups (automated)
4. Set up SSL certificates (Let's Encrypt)
5. Configure CDN for static assets
6. Add automated testing
7. Set up staging environment

---

**Last Updated:** $(date)
**Version:** 1.0.0
