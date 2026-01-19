# Database Setup Guide

## Quick Start (SQLite - Recommended for Development)

The application now defaults to **SQLite** for easy development. No setup required!

- Database file: `schoolsharthi.db` (created automatically in backend directory)
- No installation needed
- Works out of the box

## Using PostgreSQL (Production)

If you want to use PostgreSQL:

1. **Install PostgreSQL** (if not already installed)

2. **Create Database:**
   ```sql
   CREATE DATABASE schoolsharthi;
   ```

3. **Update `.env` file:**
   ```env
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/schoolsharthi
   ```

4. **Or update `backend/app/config.py`:**
   ```python
   DATABASE_URL: str = "postgresql://postgres:your_password@localhost:5432/schoolsharthi"
   ```

## Database Initialization

The database tables are created automatically when the server starts.

To manually initialize:
```bash
cd backend
.\venv\Scripts\activate
python init_db.py
```

## Create Admin User

After database is set up:
```bash
cd backend
.\venv\Scripts\activate
python create_admin.py
```

Default admin credentials:
- Username: `admin`
- Password: `admin123`
- ⚠️ Change password after first login!

## Troubleshooting

### SQLite Issues
- Database file is created automatically
- If you see permission errors, check write permissions in backend directory
- To reset: Delete `schoolsharthi.db` and restart server

### PostgreSQL Issues
- Verify PostgreSQL is running: `pg_isready`
- Check connection string format
- Verify database exists: `psql -l | grep schoolsharthi`
- Check username/password are correct

## Migration from SQLite to PostgreSQL

1. Export data from SQLite (if needed)
2. Update DATABASE_URL in `.env`
3. Run migrations: `python init_db.py`
4. Restart server
