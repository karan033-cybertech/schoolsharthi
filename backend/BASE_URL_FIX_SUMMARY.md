# BASE_URL Fix Summary - Production File URLs

## Problem Fixed
The backend was generating file download URLs with hardcoded `http://localhost:8000`, causing production users to fail when downloading PDF notes and other files.

## Changes Made

### 1. Configuration (`backend/app/config.py`)
- ✅ Changed `API_BASE_URL` to `BASE_URL` with environment variable support
- ✅ Added `API_BASE_URL` as a property that:
  - Reads from `BASE_URL` environment variable
  - Defaults to `http://localhost:8000` for local development
  - Warns if HTTP is used in production
  - Automatically removes trailing slashes

### 2. File URL Generation (`backend/app/services/s3_service.py`)
- ✅ Updated `_upload_to_local_storage()` to use `settings.API_BASE_URL` property
- ✅ Added logging to show the generated URL and BASE_URL being used

### 3. File Serving Route (`backend/app/main.py`)
- ✅ Enhanced `/api/files/{file_path:path}` endpoint with:
  - Better security (directory traversal protection)
  - Path normalization
  - Proper content-type detection
  - Cache headers for performance
  - Security headers

### 4. Documentation
- ✅ Created `PRODUCTION_BASE_URL_SETUP.md` with deployment instructions

## Files Modified

1. `backend/app/config.py` - Dynamic BASE_URL configuration
2. `backend/app/services/s3_service.py` - Use dynamic BASE_URL for file URLs
3. `backend/app/main.py` - Enhanced file serving security
4. `backend/PRODUCTION_BASE_URL_SETUP.md` - Deployment guide (NEW)

## How to Deploy

### Step 1: Set Environment Variable
```bash
# In your production environment (Render, Railway, VPS, etc.)
BASE_URL=https://your-backend.onrender.com
ENVIRONMENT=production
```

### Step 2: Verify
After deployment, check startup logs:
```
🌐 BASE_URL: https://your-backend.onrender.com
🌐 API_BASE_URL (for file URLs): https://your-backend.onrender.com
```

### Step 3: Test
1. Upload a file through admin panel
2. Check the `file_url` in API response - should use production URL
3. Download the file - should work from production

## Security Improvements

1. **Directory Traversal Protection** - Prevents `../` attacks
2. **Path Validation** - Ensures files are within storage directory
3. **Content-Type Detection** - Proper MIME types for downloads
4. **HTTPS Enforcement Warning** - Warns if HTTP is used in production

## Backward Compatibility

- ✅ Local development still works (defaults to localhost:8000)
- ✅ Existing code using `settings.API_BASE_URL` continues to work
- ✅ No breaking changes to API responses

## Testing Checklist

- [ ] Set `BASE_URL` environment variable in production
- [ ] Restart backend server
- [ ] Verify startup logs show correct BASE_URL
- [ ] Upload a new file
- [ ] Check file_url in response uses production domain
- [ ] Download file from production - should work
- [ ] Verify old files (if any) still work

## Example URLs

**Before (Broken):**
```
http://localhost:8000/api/files/notes/11/physics/2/abc123.pdf
```

**After (Fixed):**
```
https://your-backend.onrender.com/api/files/notes/11/physics/2/abc123.pdf
```

---

**Status:** ✅ **FIXED** - Ready for production deployment
