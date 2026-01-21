"""
Supabase Client Utility
Provides a reusable Supabase client instance for the application.
"""
from typing import Optional
from supabase import create_client, Client
from app.config import settings

# Global Supabase client instance (lazy-initialized)
_supabase_client: Optional[Client] = None


def get_supabase_client() -> Client:
    """
    Get or create Supabase client instance.
    
    Returns:
        Supabase Client instance
        
    Raises:
        ValueError: If Supabase is not configured
    """
    global _supabase_client
    
    # Check if Supabase is configured
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise ValueError(
            "Supabase is not configured. Please set SUPABASE_URL and SUPABASE_KEY "
            "environment variables."
        )
    
    # Create client if it doesn't exist
    if _supabase_client is None:
        try:
            _supabase_client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_KEY
            )
            print(f"✅ Supabase client initialized: {settings.SUPABASE_URL}")
        except Exception as e:
            print(f"❌ Failed to initialize Supabase client: {e}")
            raise ValueError(f"Failed to initialize Supabase client: {str(e)}")
    
    return _supabase_client
