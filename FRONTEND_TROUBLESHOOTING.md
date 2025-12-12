# Frontend Troubleshooting Guide

## Current Status
- ✅ Backend: Running on http://localhost:8000
- ✅ Frontend: Running on http://localhost:3000
- ✅ API Endpoints: All responding correctly

## If You See a Blank Page

### Step 1: Check Browser Console
1. Open your browser (Chrome/Firefox/Safari)
2. Navigate to: `http://localhost:3000`
3. Open Developer Tools:
   - **Chrome/Edge**: Press `F12` or `Ctrl+Shift+I` (Windows) / `Cmd+Option+I` (Mac)
   - **Firefox**: Press `F12` or `Ctrl+Shift+I` (Windows) / `Cmd+Option+I` (Mac)
   - **Safari**: Enable Developer menu first, then `Cmd+Option+I`
4. Check the **Console** tab for any red errors
5. Check the **Network** tab to see if API calls are failing

### Step 2: Common Issues and Fixes

#### Issue 1: "Failed to fetch" or Network Errors
**Symptom**: Console shows CORS errors or network failures

**Fix**: 
- Verify backend is running: `curl http://localhost:8000/health`
- Check `.env` file in `frontend/` directory has: `REACT_APP_API_URL=http://localhost:8000`
- Restart frontend after changing `.env`

#### Issue 2: "Cannot read property of undefined"
**Symptom**: JavaScript errors in console

**Fix**: 
- Hard refresh browser: `Ctrl+Shift+R` (Windows) / `Cmd+Shift+R` (Mac)
- Clear browser cache
- Check if backend is returning data correctly

#### Issue 3: Blank White Page
**Symptom**: Page loads but shows nothing

**Possible Causes**:
1. React app not rendering
2. API calls failing silently
3. JavaScript errors preventing render

**Fix**:
1. Check browser console for errors
2. Verify `http://localhost:3000` shows HTML with `<div id="root"></div>`
3. Check Network tab - are API calls being made?
4. Try accessing API directly: `http://localhost:8000/api/v1/fats/?limit=5`

### Step 3: Verify Services

#### Check Backend
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy",...}
```

#### Check Frontend
```bash
curl http://localhost:3000
# Should return HTML with <div id="root"></div>
```

#### Check API from Browser
Open in browser: `http://localhost:8000/api/v1/fats/?limit=5`
Should see JSON data.

### Step 4: Restart Everything

If still not working:

```bash
# Kill all processes
pkill -9 -f uvicorn
pkill -9 -f react-scripts

# Restart backend
cd opal-unified/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &

# Restart frontend
cd opal-unified/frontend
npm start &
```

### Step 5: Check Browser Compatibility

- Use a modern browser (Chrome, Firefox, Edge, Safari latest versions)
- Disable browser extensions that might block JavaScript
- Try incognito/private mode

## Expected Behavior

When working correctly, you should see:
1. **Header**: "Fault Tracking System" at the top
2. **Create Button**: "+ Create New FATS" button on the right
3. **Table**: List of FATS entries with columns:
   - IDNo
   - Issue
   - Section
   - Status
   - Operator
   - Date
   - Actions (View, Edit, Comment buttons)
4. **Filters**: Search bar and dropdown filters for Section and Status

## Debug Information

If you see errors in console, note:
- Error message
- Which API endpoint failed
- Network request status codes
- Any CORS errors

## Quick Test

1. Open browser to `http://localhost:3000`
2. Open Developer Console (F12)
3. Look for:
   - ✅ Green checkmarks = API calls succeeded
   - ❌ Red X marks = API calls failed
   - Console errors in red

## Still Not Working?

1. **Check if frontend compiled successfully**
   - Look for "Compiled successfully!" message in terminal
   - Check for any compilation errors

2. **Verify file structure**
   ```bash
   ls -la frontend/src/
   # Should see: App.js, index.js, components/, services/
   ```

3. **Check for missing dependencies**
   ```bash
   cd frontend
   npm install
   ```

4. **Clear browser cache completely**
   - Chrome: Settings > Privacy > Clear browsing data
   - Or use incognito mode

5. **Check backend logs**
   - Look at terminal where backend is running
   - Check for any error messages

---

**Need More Help?**
- Check browser console for specific error messages
- Verify both services are running
- Test API endpoints directly in browser

