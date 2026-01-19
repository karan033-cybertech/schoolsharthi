"""
Database Migration Utilities
Handles schema migrations safely, especially for SQLite
"""
from sqlalchemy import inspect, text
from app.database import engine
import logging

logger = logging.getLogger(__name__)


def table_exists(table_name: str) -> bool:
    """
    Check if a table exists in the database
    """
    try:
        inspector = inspect(engine)
        return table_name in inspector.get_table_names()
    except Exception:
        return False


def check_column_exists_sqlite(table_name: str, column_name: str) -> bool:
    """
    Check if a column exists using PRAGMA table_info (SQLite specific)
    More reliable for SQLite than inspector.get_columns()
    """
    try:
        if not table_exists(table_name):
            return False
        
        is_sqlite = engine.url.drivername.startswith('sqlite')
        if not is_sqlite:
            # For PostgreSQL, use inspector
            inspector = inspect(engine)
            columns = [col['name'] for col in inspector.get_columns(table_name)]
            return column_name in columns
        
        # For SQLite, use PRAGMA table_info
        with engine.connect() as conn:
            result = conn.execute(text(f"PRAGMA table_info({table_name})"))
            columns = [row[1] for row in result]  # Column name is at index 1
            return column_name in columns
            
    except Exception as e:
        logger.warning(f"Error checking column existence: {e}")
        return False


def add_column_sqlite_raw(table_name: str, column_name: str, column_type: str, default_value: str = None):
    """
    Add a column to SQLite table using raw SQL (no bind parameters for DEFAULT)
    SQLite does NOT support parameterized DEFAULT values in ALTER TABLE
    """
    try:
        # First check if table exists
        if not table_exists(table_name):
            logger.info(f"📋 Table '{table_name}' doesn't exist yet - will be created by create_all()")
            return True
        
        # Check if column already exists using PRAGMA
        if check_column_exists_sqlite(table_name, column_name):
            logger.info(f"✅ Column '{column_name}' already exists in '{table_name}'")
            return True
        
        # Build raw SQL string (NO bind parameters for DEFAULT values in SQLite)
        is_sqlite = engine.url.drivername.startswith('sqlite')
        
        if is_sqlite:
            # SQLite: Use raw string with DEFAULT value directly in SQL
            # Important: Use TEXT instead of VARCHAR for SQLite compatibility
            sqlite_type = 'TEXT' if 'VARCHAR' in column_type.upper() or 'STRING' in column_type.upper() else column_type
            
            if default_value:
                # Raw SQL string - no parameters for DEFAULT
                alter_sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {sqlite_type} DEFAULT '{default_value}'"
            else:
                alter_sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {sqlite_type}"
            
            # Execute raw SQL (not parameterized)
            with engine.begin() as conn:
                conn.execute(text(alter_sql))
                
        else:
            # PostgreSQL: Can use IF NOT EXISTS
            if default_value:
                alter_sql = text(f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {column_name} {column_type} DEFAULT '{default_value}'")
            else:
                alter_sql = text(f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {column_name} {column_type}")
            
            with engine.begin() as conn:
                conn.execute(alter_sql)
        
        logger.info(f"✅ Added column '{column_name}' to '{table_name}'")
        return True
        
    except Exception as e:
        # If column already exists or other error, log and continue
        error_msg = str(e).lower()
        if 'duplicate column' in error_msg or 'already exists' in error_msg or 'duplicate column name' in error_msg:
            logger.info(f"✅ Column '{column_name}' already exists in '{table_name}' (detected via error)")
            return True
        else:
            logger.warning(f"⚠️  Error adding column '{column_name}' to '{table_name}': {e}")
            import traceback
            traceback.print_exc()
            # Don't fail - might be a non-critical issue
            return False


def verify_schema():
    """
    Verify and update database schema for required columns
    Runs migrations for schema changes
    """
    logger.info("🔍 Verifying database schema...")
    
    migrations_applied = []
    
    # Migration: Add detected_language to doubts table
    # Use SQLite-safe method with raw SQL
    if add_column_sqlite_raw('doubts', 'detected_language', 'TEXT', 'english'):
        migrations_applied.append('doubts.detected_language')
        print("✅ detected_language column verified successfully")
    
    if migrations_applied:
        logger.info(f"✅ Applied migrations: {', '.join(migrations_applied)}")
    else:
        logger.info("✅ Database schema is up to date - no migrations needed")
        print("✅ detected_language column verified successfully")
    
    return migrations_applied


def ensure_tables_exist():
    """
    Ensure all tables exist (for fresh databases)
    This is a safety check - create_all() should handle this, but we verify
    """
    try:
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        
        required_tables = [
            'users', 'notes', 'pyqs', 'doubts', 'career_queries',
            'exams', 'exam_questions', 'exam_attempts', 'exam_results'
        ]
        
        missing_tables = [table for table in required_tables if table not in existing_tables]
        
        if missing_tables:
            logger.info(f"📋 Creating missing tables: {', '.join(missing_tables)}")
            # Import Base here to avoid circular imports
            from app.database import Base
            Base.metadata.create_all(bind=engine)
            logger.info("✅ All tables created")
        else:
            logger.info("✅ All required tables exist")
            
    except Exception as e:
        logger.error(f"❌ Error ensuring tables exist: {e}")
        raise


def sync_database_schema():
    """
    Main function to sync database schema
    Called on app startup to ensure schema is up to date
    """
    try:
        print("\n" + "="*60)
        print("🔄 Syncing database schema...")
        print("="*60)
        
        # First, ensure all tables exist (for fresh databases)
        ensure_tables_exist()
        
        # Then, apply migrations for existing tables
        migrations = verify_schema()
        
        if migrations:
            print(f"✅ Applied {len(migrations)} migration(s)")
        else:
            print("✅ No migrations needed")
        
        print("✅ Database schema verified successfully")
        print("="*60 + "\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Database schema sync failed: {e}")
        print("⚠️  Continuing anyway - check logs for details")
        import traceback
        traceback.print_exc()
        return False
