# ⚡ Quick Deployment Guide - 5 Minutes

This is a simplified version for experienced developers. For detailed explanations, see `DEPLOYMENT_AUDIT_AND_ROADMAP.md`.

## Prerequisites
- GitHub account
- Render account (free) - render.com
- Vercel account (free) - vercel.com

## Steps

### 1. Push to GitHub (2 min)
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2. Deploy Database (1 min)
1. Render → New PostgreSQL
2. Copy Internal Database URL

### 3. Deploy Backend (2 min)
1. Render → New Web Service
2. Connect GitHub repo
3. Settings:
   - Root Directory: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Environment Variables:
   ```
   DATABASE_URL=<from-step-2>
   SECRET_KEY=<generate-random-32-chars>
   CORS_ORIGINS=https://your-frontend.vercel.app
   ENVIRONMENT=production
   USE_LOCAL_STORAGE=true
   API_BASE_URL=https://your-backend.onrender.com
   ```
5. Deploy → Copy URL

### 4. Deploy Frontend (1 min)
1. Vercel → Import Git Repository
2. Root Directory: `frontend`
3. Environment Variable:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
   ```
4. Deploy → Copy URL

### 5. Update CORS (1 min)
1. Render → Backend → Environment
2. Update `CORS_ORIGINS` with frontend URL
3. Redeploy

### 6. Test
- Backend: `curl https://your-backend.onrender.com/health`
- Frontend: Open in browser, test login

## Done! 🎉

Your app is live at: `https://your-frontend.vercel.app`

## Generate SECRET_KEY
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
