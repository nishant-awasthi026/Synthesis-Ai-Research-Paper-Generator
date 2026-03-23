# 🔧 Troubleshooting Registration Failure

## Current Issue
The backend server is having trouble starting due to dependency issues.

## Quick Diagnosis

**Please check the following:**

1. **Is the backend running?**
   - Open: http://localhost:8000/docs
   - You should see the API documentation (Swagger UI)
   - If you see an error or "can't connect", the backend isn't running

2. **What error do you see in the browser?**
   - Open browser developer console (F12)
   - Try to register
   - Check the "Console" tab for JavaScript errors
   - Check the "Network" tab for failed HTTP requests
   - Share the error message you see

## Common Issues & Fixes

### Issue 1: "Cannot connect to localhost:8000"
**Cause:** Backend server not running

**Fix:**
```bash
# Kill all running Python processes
taskkill /F /IM python.exe

# Navigate to project root
cd "D:\Synthesis- Ai Research Paper Generator"

# Set Python path and start backend
$env:PYTHONPATH="D:\Synthesis- Ai Research Paper Generator"
python -m uvicorn backend.main:app --reload --port 8000
```

### Issue 2: "Network Error" or "CORS Error"
**Cause:** Frontend can't talk to backend

**Fix:** Check that:
- Backend is on port 8000
- Frontend is on port 5173
- Both are running

### Issue 3: "Module not found" errors in backend
**Cause:** Missing dependencies

**Fix:**
```bash
cd backend
pip install fastapi uvicorn[standard] sqlalchemy python-multipart pydantic pydantic-settings python-jose[cryptography] passlib[bcrypt] alembic jinja2 nbformat python-dotenv
```

## Manual Test

**Test 1: Check Backend Health**
```bash
curl http://localhost:8000/health
```
Expected: `{"status":"healthy"}`

**Test 2: Check API Docs**
Visit: http://localhost:8000/docs
Expected: Swagger UI interface

**Test 3: Test Registration Directly**
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123","full_name":"Test User"}'
```

## Need More Help?

Please share:
1. The exact error message from your browser
2. What you see when you visit http://localhost:8000/docs
3. Any error messages from the terminal running the backend

This will help me fix the specific issue you're experiencing!
