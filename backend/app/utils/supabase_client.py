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
    Production-safe: Proxy environment variables are removed at application startup.
    
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
            # Ensure proxy vars are not set (they should be removed at startup)
            # Double-check to prevent "unexpected keyword argument 'proxy'" errors on Render
            proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 
                         'ALL_PROXY', 'all_proxy', 'NO_PROXY', 'no_proxy']
            for var in proxy_vars:
                if var in os.environ:
                    del os.environ[var]
            
            # Initialize Supabase client with standard parameters only
            # Do NOT pass proxy or any custom httpx options to avoid conflicts
            _supabase_client = create_client(
                settings.SUPABASE_URL,
                service_key
            )
            print(f"✅ Supabase client initialized: {settings.SUPABASE_URL}")
            print(f"   Bucket: {settings.SUPABASE_BUCKET}")
                    
        except TypeError as e:
            if "proxy" in str(e).lower():
                error_msg = (
                    f"Supabase client initialization failed due to proxy configuration: {e}. "
                    "Proxy environment variables detected. They should be removed at startup. "
                    "Check that HTTP_PROXY and HTTPS_PROXY are not set."
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
