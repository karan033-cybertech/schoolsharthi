# Production BASE_URL Configuration Guide

## Problem
The backend was generating file download URLs using `http://localhost:8000` in production, causing download failures for production users.

## Solution
The backend now uses the `BASE_URL` environment variable to generate file URLs dynamically.

## Configuration

### Environment Variable
Set the `BASE_URL` environment variable to your production backend URL:

```bash
BASE_URL=https://your-backend.onrender.com
# OR
BASE_URL=https://api.yourdomain.com
```

### Examples by Platform

#### Render.com
```bash
# In Render dashboard → Environment Variables
BASE_URL=https://your-app-name.onrender.com
ENVIRONMENT=production
```

#### Railway
```bash
# In Railway dashboard → Variables
BASE_URL=https://your-app.up.railway.app
ENVIRONMENT=production
```

#### VPS/Server
```bash
# In .env file or systemd service
BASE_URL=https://api.yourdomain.com
ENVIRONMENT=production
```

#### Docker
```bash
# In docker-compose.yml or docker run command
environment:
  - BASE_URL=https://api.yourdomain.com
  - ENVIRONMENT=production
```

## Important Notes

1. **Always use HTTPS in production** - The system will warn if HTTP is used in production mode
2. **No trailing slash** - The system automatically removes trailing slashes
3. **Must be accessible** - The BASE_URL must be publicly accessible for file downloads to work

## Verification

After setting BASE_URL, check the startup logs:
```
🌐 BASE_URL: https://your-backend.onrender.com
🌐 API_BASE_URL (for file URLs): https://your-backend.onrender.com
```

## File URL Format

Files stored locally will be served at:
```
{BASE_URL}/api/files/{path}
```

Example:
```
https://your-backend.onrender.com/api/files/notes/11/physics/2/abc123.pdf
```

## Testing

1. Upload a file through the admin panel
2. Check the returned `file_url` in the API response
3. Verify it uses your production BASE_URL, not localhost
4. Test downloading the file - it should work from production

## Troubleshooting

### Files still showing localhost URLs
- Check that `BASE_URL` environment variable is set
- Restart the backend server after setting the variable
- Verify in startup logs that BASE_URL is correct

### Downloads failing
- Verify BASE_URL is publicly accessible
- Check that the file serving route `/api/files/{path}` is accessible
- Ensure CORS is configured to allow your frontend domain

### HTTPS warnings
- In production, always use `https://` not `http://`
- The system will warn but still work with HTTP (not recommended)
