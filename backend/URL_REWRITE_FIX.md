# URL Rewrite Fix - Localhost to Production URLs

## Problem
Even after setting `BASE_URL` environment variable, existing database records still contained `localhost:8000` URLs, causing download failures in production.

## Solution
Added automatic URL rewriting that converts localhost URLs to the current `BASE_URL` on-the-fly when returning API responses.

## Implementation

### 1. Created URL Rewrite Utility (`backend/app/utils/url_rewrite.py`)
- `rewrite_file_url()` - Rewrites localhost URLs to current BASE_URL
- Detects patterns: `http://localhost:8000`, `http://127.0.0.1:8000`
- Preserves S3 URLs (doesn't rewrite them)
- Preserves URLs that already use correct BASE_URL

### 2. Applied to All Routes
- ✅ `GET /api/notes/` - List notes
- ✅ `GET /api/notes/{id}` - Get single note
- ✅ `POST /api/notes/{id}/download` - Download note
- ✅ `GET /api/pyqs/` - List PYQs
- ✅ `GET /api/pyqs/{id}` - Get single PYQ
- ✅ `POST /api/pyqs/{id}/download` - Download PYQ
- ✅ Search service - Notes and PYQs in search results

## How It Works

1. **Database stores original URL** (may be localhost)
2. **API response rewrites URL** using current BASE_URL
3. **User receives production URL** in API response
4. **Download works** from production domain

## Example

**Before (in database):**
```
http://localhost:8000/api/files/notes/11/physics/2/abc123.pdf
```

**After (in API response):**
```
https://your-backend.onrender.com/api/files/notes/11/physics/2/abc123.pdf
```

## Benefits

1. ✅ **No database migration needed** - Works immediately
2. ✅ **Backward compatible** - Old URLs automatically fixed
3. ✅ **Future-proof** - New uploads use correct BASE_URL
4. ✅ **No data loss** - Original URLs preserved in database

## Testing

After deployment:
1. Check startup logs show correct BASE_URL
2. Call `GET /api/notes/` - URLs should use production domain
3. Download a file - should work from production
4. Check browser network tab - file URL should be production domain

## Files Modified

1. `backend/app/utils/url_rewrite.py` - NEW - URL rewriting utility
2. `backend/app/utils/__init__.py` - NEW - Utils package init
3. `backend/app/routers/notes.py` - Apply URL rewriting
4. `backend/app/routers/pyqs.py` - Apply URL rewriting
5. `backend/app/services/smart_search_service.py` - Apply URL rewriting

## Status

✅ **FIXED** - All file URLs are now rewritten to use production BASE_URL

---

**Note:** This fix works alongside the BASE_URL configuration. Make sure `BASE_URL` environment variable is set in production!
