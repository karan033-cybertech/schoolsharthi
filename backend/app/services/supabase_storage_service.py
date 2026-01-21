"""
Supabase Storage Service
Handles file uploads to Supabase Storage bucket.
"""
from fastapi import UploadFile
from app.config import settings
from app.utils.supabase_client import get_supabase_client
import uuid
from typing import Optional


async def upload_file_to_supabase(file: UploadFile, folder_path: str) -> str:
    """
    Upload file to Supabase Storage bucket and return the public URL.
    
    Args:
        file: FastAPI UploadFile object
        folder_path: Folder path in the bucket (e.g., "notes/6/physics/chapter1/")
        
    Returns:
        Public URL of the uploaded file
        
    Raises:
        ValueError: If Supabase is not configured or upload fails
    """
    try:
        # Get Supabase client
        supabase = get_supabase_client()
        
        # Get bucket name from settings (default: "notes")
        bucket_name = settings.SUPABASE_BUCKET or "notes"
        
        # Generate unique filename
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'pdf'
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # Normalize folder path (remove leading/trailing slashes, ensure it ends with /)
        folder_path = folder_path.strip('/')
        if folder_path and not folder_path.endswith('/'):
            folder_path += '/'
        
        # Construct full path in bucket
        file_path = f"{folder_path}{unique_filename}"
        
        # Read file content
        file_content = await file.read()
        
        # Determine content type
        content_type = file.content_type or 'application/octet-stream'
        if file_extension.lower() == 'pdf':
            content_type = 'application/pdf'
        elif file_extension.lower() in ['jpg', 'jpeg']:
            content_type = 'image/jpeg'
        elif file_extension.lower() == 'png':
            content_type = 'image/png'
        
        # Upload to Supabase Storage
        # The upload method accepts bytes directly
        # Note: Supabase Storage uploads work with public buckets
        # For private buckets, use create_signed_url() instead of get_public_url()
        response = supabase.storage.from_(bucket_name).upload(
            path=file_path,
            file=file_content,
            file_options={
                "content-type": content_type,
                "cache-control": "3600",  # Cache for 1 hour
                "upsert": "false"  # Don't overwrite existing files
            }
        )
        
        # Upload response may be None on success or raise an exception on error
        # If we get here without exception, upload was successful
        print(f"✅ File uploaded to Supabase Storage: {file_path}")
        print(f"   File size: {len(file_content)} bytes")
        print(f"   Content type: {content_type}")
        
        # Get public URL
        # Supabase get_public_url() returns a string URL directly for public buckets
        # Format: https://{project_ref}.supabase.co/storage/v1/object/public/{bucket}/{path}
        public_url = supabase.storage.from_(bucket_name).get_public_url(file_path)
        
        # Handle response format variations
        if isinstance(public_url, dict):
            # Some versions return dict with 'publicUrl' key
            public_url = public_url.get('publicUrl') or public_url.get('public_url')
        
        if not public_url:
            raise ValueError(f"Failed to get public URL for uploaded file: {file_path}")
        
        # Ensure URL is a string
        public_url = str(public_url)
        
        print(f"   Public URL: {public_url}")
        
        return public_url
        
    except ValueError:
        # Re-raise ValueError (configuration errors)
        raise
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Supabase upload error: {error_msg}")
        raise ValueError(f"Failed to upload file to Supabase Storage: {error_msg}")


async def delete_file_from_supabase(file_path: str, bucket_name: Optional[str] = None) -> bool:
    """
    Delete a file from Supabase Storage bucket.
    
    Args:
        file_path: Path to the file in the bucket (relative to bucket root)
        bucket_name: Optional bucket name (defaults to settings.SUPABASE_BUCKET)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        supabase = get_supabase_client()
        bucket = bucket_name or settings.SUPABASE_BUCKET or "notes"
        
        # Remove file
        response = supabase.storage.from_(bucket).remove([file_path])
        
        print(f"✅ File deleted from Supabase Storage: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to delete file from Supabase Storage: {e}")
        return False
