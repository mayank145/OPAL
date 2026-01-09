# 🚀 Production Deployment Commands

## ✅ Correct Production Path
```
/opt/OPAL/opal-unified
```

## 📋 Step-by-Step Deployment

You're already connected to the server. Run these commands:

```bash
# 1. Check current directory (you should already be here)
pwd
# Should show: /opt/OPAL/opal-unified

# 2. Check if this is a git repository
git status

# 3. Check remote repository
git remote -v

# 4. Pull latest changes
git pull origin main

# 5. Update backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
cd ..

# 6. Update frontend
cd frontend
npm install
npm run build
cd ..

# 7. Restart services
systemctl restart opal-backend
systemctl restart httpd

# 8. Verify deployment
sleep 5
curl http://localhost:8000/health
curl http://localhost/ | head -10

# 9. Check logs if needed
tail -50 /var/log/httpd/error_log
journalctl -u opal-backend -n 50
```

## 🔍 If Git Repository Check Fails

If `git status` shows "not a git repository", you'll need to:

### Option A: Clone from GitHub
```bash
cd /opt/OPAL
mv opal-unified opal-unified-backup
git clone https://github.com/mayank145/OPAL.git opal-unified
cd opal-unified
# Then continue with steps 5-8 above
```

### Option B: Initialize and connect to GitHub
```bash
git init
git remote add origin https://github.com/mayank145/OPAL.git
git fetch origin
git reset --hard origin/main
# Then continue with steps 5-8 above
```

## ✅ Success Indicators

After deployment, you should see:
- ✅ Backend health check returns: `{"status":"healthy","service":"OPAL Unified System","database":"MariaDB"}`
- ✅ Frontend returns HTML with "Fault Tracking System"
- ✅ No errors in logs

## 🧪 Test the New Features

1. Open: http://opalfailover.subaru.nao.ac.jp
2. Edit a fault
3. Look for 🏷️ button in editor
4. Click it and enter fault ID
5. Save and test the link


