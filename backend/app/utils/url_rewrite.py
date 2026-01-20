"""
Utility to rewrite localhost URLs to production BASE_URL
This fixes existing database records that have localhost URLs
"""
from app.config import settings
import re


def rewrite_file_url(url: str) -> str:
    """
    Rewrite localhost URLs to use the current BASE_URL.
    This fixes existing database records without needing a migration.
    
    Args:
        url: The file URL (may contain localhost)
        
    Returns:
        URL with localhost replaced by current BASE_URL
    """
    if not url:
        return url
    
    # If it's already using the correct BASE_URL, return as-is
    if url.startswith(settings.API_BASE_URL):
        return url
    
    # If it's an S3 URL, return as-is (don't rewrite S3 URLs)
    if url.startswith("https://") and ".s3." in url:
        return url
    
    # Pattern to match localhost URLs (http://localhost:8000 or http://127.0.0.1:8000)
    localhost_pattern = r'https?://(localhost|127\.0\.0\.1)(:\d+)?'
    
    # Check if URL contains localhost
    if re.search(localhost_pattern, url):
        # Extract the path part after the domain
        path_match = re.search(r'https?://[^/]+(/.*)', url)
        if path_match:
            path = path_match.group(1)
            # Rewrite to use current BASE_URL
            new_url = f"{settings.API_BASE_URL}{path}"
            print(f"🔄 Rewrote URL: {url} → {new_url}")
            return new_url
    
    # If no localhost found, return original URL
    return url


def rewrite_file_urls_in_dict(data: dict, url_fields: list = None) -> dict:
    """
    Rewrite file URLs in a dictionary.
    
    Args:
        data: Dictionary containing file URLs
        url_fields: List of field names that contain URLs (default: common field names)
        
    Returns:
        Dictionary with rewritten URLs
    """
    if url_fields is None:
        url_fields = ['file_url', 'thumbnail_url', 'question_paper_url', 
                     'answer_key_url', 'solution_url']
    
    result = data.copy() if isinstance(data, dict) else data
    
    if isinstance(data, dict):
        for field in url_fields:
            if field in data and data[field]:
                result[field] = rewrite_file_url(data[field])
    elif isinstance(data, list):
        result = [rewrite_file_urls_in_dict(item, url_fields) for item in data]
    
    return result
