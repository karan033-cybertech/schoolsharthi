from fastapi import UploadFile
from app.config import settings
import uuid
from pathlib import Path
from typing import Optional

# Lazy-initialized S3 client (only created when needed and if AWS is configured)
_s3_client = None


def _get_s3_client():
    """Get or create S3 client lazily"""
    global _s3_client
    
    # Return None if AWS is not configured
    if not settings.AWS_ACCESS_KEY_ID or not settings.AWS_SECRET_ACCESS_KEY or not settings.S3_BUCKET_NAME:
        return None
    
    # Create client if it doesn't exist
    if _s3_client is None:
        try:
            import boto3
            _s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
        except Exception as e:
            print(f"⚠️ Failed to initialize S3 client: {e}")
            return None
    
    return _s3_client


async def _upload_to_local_storage(file: UploadFile, folder_path: str) -> str:
    """Upload file to local storage and return the URL."""
    # Create uploads directory structure
    upload_dir = Path(settings.LOCAL_STORAGE_PATH) / folder_path.strip('/')
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'pdf'
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = upload_dir / unique_filename
    
    # Save file
    file_content = await file.read()
    with open(file_path, 'wb') as f:
        f.write(file_content)
    
    # Return URL that will be served by the file serving endpoint
    # Remove leading/trailing slashes and normalize path
    relative_path = f"{folder_path.strip('/')}/{unique_filename}".replace('\\', '/')
    url = f"{settings.API_BASE_URL}/api/files/{relative_path}"
    
    print(f"✅ File saved locally: {file_path}")
    print(f"   URL: {url}")
    
    return url


async def upload_file_to_s3(file: UploadFile, folder_path: str) -> str:
    """Upload file to S3 and return the URL. Falls back to local storage if S3 is not configured."""
    s3_client = _get_s3_client()
    
    # If S3 is not configured, use local storage if enabled
    if not s3_client:
        if settings.USE_LOCAL_STORAGE:
            return await _upload_to_local_storage(file, folder_path)
        else:
            raise ValueError(
                "S3 storage is not configured. Please set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, "
                "and S3_BUCKET_NAME environment variables to enable file uploads, or set USE_LOCAL_STORAGE=true "
                "to use local file storage."
            )
    
    try:
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'pdf'
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        s3_key = f"{folder_path}{unique_filename}"
        
        # Read file content
        file_content = await file.read()
        
        # Upload to S3
        s3_client.put_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key=s3_key,
            Body=file_content,
            ContentType=file.content_type or 'application/octet-stream'
        )
        
        # Return public URL
        url = f"https://{settings.S3_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{s3_key}"
        return url
    except Exception as e:
        print(f"❌ S3 upload error: {e}")
        # Re-raise the error instead of returning placeholder
        raise ValueError(f"Failed to upload file to S3: {str(e)}")
