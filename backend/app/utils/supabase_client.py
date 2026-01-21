"""
Supabase Client Utility
Provides a reusable Supabase client instance for the application.
Production-safe: Handles proxy settings and ensures clean initialization.
"""
from typing import Optional
import os

# CRITICAL: Remove proxy environment variables BEFORE importing ANYTHING that uses httpx
# Render injects HTTP_PROXY and HTTPS_PROXY which Supabase Python SDK does not support
# This must happen before "from supabase import" to prevent proxy conflicts
# Also set NO_PROXY to ensure httpx doesn't try to use proxies
proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 
              'ALL_PROXY', 'all_proxy', 'NO_PROXY', 'no_proxy']
for var in proxy_vars:
    os.environ.pop(var, None)

# Explicitly disable proxy detection by httpx
# Set NO_PROXY to * to prevent any proxy usage
os.environ['NO_PROXY'] = '*'
os.environ['no_proxy'] = '*'

# Now safe to import Supabase
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
            # Final check: ensure proxy vars are explicitly disabled
            # Remove any proxy settings
            for var in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY', 'all_proxy']:
                os.environ.pop(var, None)
            
            # Explicitly disable proxies with NO_PROXY
            os.environ['NO_PROXY'] = '*'
            os.environ['no_proxy'] = '*'
            
            # Initialize Supabase client with standard parameters only
            # The proxy env vars are disabled, so httpx won't use them
            _supabase_client = create_client(
                settings.SUPABASE_URL,
                service_key
            )
            print(f"✅ Supabase client initialized: {settings.SUPABASE_URL}")
            print(f"   Bucket: {settings.SUPABASE_BUCKET}")
            print(f"   Proxy settings: Disabled (NO_PROXY=*)")
                    
        except TypeError as e:
            if "proxy" in str(e).lower():
                # This is likely a version incompatibility issue with gotrue/httpx
                # Check installed versions
                import sys
                import subprocess
                try:
                    result = subprocess.run(
                        [sys.executable, '-m', 'pip', 'show', 'supabase', 'gotrue', 'httpx'],
                        capture_output=True,
                        text=True
                    )
                    versions_info = result.stdout
                except:
                    versions_info = "Unable to check versions"
                
                error_msg = (
                    f"Supabase client initialization failed: {e}\n"
                    f"This is likely a version incompatibility between supabase-py, gotrue, and httpx.\n"
                    f"Current versions:\n{versions_info}\n"
                    f"Solution: This may require downgrading gotrue or updating supabase-py.\n"
                    f"Proxy environment variables are already disabled (NO_PROXY=*)."
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
