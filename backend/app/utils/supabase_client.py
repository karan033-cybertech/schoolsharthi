"""
Supabase Client Utility
Provides a reusable Supabase client instance for the application.
Production-safe: Handles proxy settings and ensures clean initialization.
"""
from typing import Optional
import os
from supabase import create_client, Client
from app.config import settings

# Global Supabase client instance (lazy-initialized)
_supabase_client: Optional[Client] = None


def get_supabase_client() -> Client:
    """
    Get or create Supabase client instance.
    Production-safe: Temporarily removes proxy env vars to prevent conflicts.
    
    Returns:
        Supabase Client instance
        
    Raises:
        ValueError: If Supabase is not configured
    """
    global _supabase_client
    
    # Get service key (support both SUPABASE_KEY and SUPABASE_SERVICE_KEY)
    service_key = settings.SUPABASE_SERVICE_KEY or settings.SUPABASE_KEY
    
    # Check if Supabase is configured
    if not settings.SUPABASE_URL or not service_key:
        raise ValueError(
            "Supabase is not configured. Please set SUPABASE_URL and "
            "SUPABASE_KEY (or SUPABASE_SERVICE_KEY) environment variables."
        )
    
    # Create client if it doesn't exist
    if _supabase_client is None:
        try:
            # Temporarily remove proxy environment variables to prevent httpx conflicts
            # This prevents "unexpected keyword argument 'proxy'" errors on Render
            proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 
                         'ALL_PROXY', 'all_proxy', 'NO_PROXY', 'no_proxy']
            saved_proxies = {}
            
            for var in proxy_vars:
                if var in os.environ:
                    saved_proxies[var] = os.environ.pop(var)
            
            try:
                # Initialize Supabase client with standard parameters only
                # Do NOT pass proxy or any custom httpx options to avoid conflicts
                _supabase_client = create_client(
                    settings.SUPABASE_URL,
                    service_key
                )
                print(f"✅ Supabase client initialized: {settings.SUPABASE_URL}")
                print(f"   Bucket: {settings.SUPABASE_BUCKET}")
            finally:
                # Restore proxy vars if they were set (for other parts of the app)
                for var, value in saved_proxies.items():
                    os.environ[var] = value
                    
        except TypeError as e:
            if "proxy" in str(e).lower():
                error_msg = (
                    f"Supabase client initialization failed due to proxy configuration: {e}. "
                    "This is often caused by proxy environment variables. "
                    "Ensure no proxy variables are set for Supabase operations."
                )
            else:
                error_msg = f"Failed to initialize Supabase client: {str(e)}"
            print(f"❌ {error_msg}")
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Failed to initialize Supabase client: {str(e)}"
            print(f"❌ {error_msg}")
            raise ValueError(error_msg)
    
    return _supabase_client
