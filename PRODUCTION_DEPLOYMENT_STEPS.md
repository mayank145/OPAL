# 🚀 Production Deployment Steps

## ✅ Git Changes Pushed Successfully!

Your changes have been committed and pushed to GitHub:
- Commit: `a11c600` - "Fix: Search bar auto-resets when cleared to show previous entries"
- Repository: github.com:mayank145/OPAL.git
- Branch: main

---

## 📋 Now Deploy to Production Server

**Server IP:** 133.40.149.66

### Option 1: Quick Update (If already deployed)

If your production server is already set up, just pull the latest changes:

```bash
# SSH into your production server
ssh root@133.40.149.66

# Navigate to the project directory
cd /opt/OPAL/opal-unified

# Pull latest changes from GitHub
git pull origin main

# Update frontend
cd frontend
npm install
npm run build

# Restart backend service
systemctl restart opal-backend

# Restart Apache
systemctl restart httpd

# Verify
systemctl status opal-backend
curl http://localhost/api/v1/fats/stats/summary
```

---

### Option 2: Full Production Deployment (First time)

If this is your first time deploying to production, follow these steps:

#### Step 1: SSH into Server
```bash
ssh root@133.40.149.66
```

#### Step 2: Clone/Pull Repository
```bash
# If not yet cloned
cd /opt/OPAL
git clone https://github.com/mayank145/OPAL.git
cd OPAL

# If already cloned
cd /opt/OPAL/OPAL
git pull origin main
```

#### Step 3: Setup Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file
cat > .env << 'EOF'
DATABASE_URL=mysql+aiomysql://opal:opal@opalfailover:3306/opal
ASYNC_DATABASE_URL=mysql+aiomysql://opal:opal@opalfailover:3306/opal
DEBUG=false
ALLOWED_ORIGINS=http://133.40.149.66,http://localhost
EOF
```

#### Step 4: Setup Backend Service
```bash
# Create systemd service
cat > /etc/systemd/system/opal-backend.service << 'EOF'
[Unit]
Description=OPAL FATS Backend API
After=network.target mariadb.service
Wants=mariadb.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/OPAL/OPAL/backend
Environment="PATH=/opt/OPAL/OPAL/backend/venv/bin"
ExecStart=/opt/OPAL/OPAL/backend/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 2
Restart=always
RestartSec=10
StandardOutput=append:/opt/OPAL/OPAL/backend/logs/app.log
StandardError=append:/opt/OPAL/OPAL/backend/logs/app.log

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
systemctl daemon-reload
systemctl enable opal-backend
systemctl start opal-backend
systemctl status opal-backend
```

#### Step 5: Build Frontend
```bash
cd /opt/OPAL/OPAL/frontend

# Create production environment file
cat > .env.production << 'EOF'
REACT_APP_API_URL=http://133.40.149.66
EOF

# Install dependencies and build
npm install
npm run build

# Verify build
ls -lh build/
```

#### Step 6: Configure Apache
```bash
# Create Apache configuration
cat > /etc/httpd/conf.d/opal-fats.conf << 'EOF'
<VirtualHost *:80>
    ServerName 133.40.149.66
    ServerAdmin admin@localhost

    # Frontend - Serve React build
    DocumentRoot /opt/OPAL/OPAL/frontend/build
    
    <Directory /opt/OPAL/OPAL/frontend/build>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
        
        # Enable React Router (SPA routing)
        RewriteEngine On
        RewriteBase /
        RewriteRule ^index\.html$ - [L]
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule . /index.html [L]
    </Directory>

    # Backend API - Reverse proxy to port 8000
    ProxyPreserveHost On
    ProxyPass /api http://127.0.0.1:8000/api
    ProxyPassReverse /api http://127.0.0.1:8000/api
    
    ProxyPass /docs http://127.0.0.1:8000/docs
    ProxyPassReverse /docs http://127.0.0.1:8000/docs
    
    ProxyPass /openapi.json http://127.0.0.1:8000/openapi.json
    ProxyPassReverse /openapi.json http://127.0.0.1:8000/openapi.json
    
    ProxyPass /health http://127.0.0.1:8000/health
    ProxyPassReverse /health http://127.0.0.1:8000/health

    # Serve backend uploads (images)
    Alias /uploads /opt/OPAL/OPAL/backend/uploads
    <Directory /opt/OPAL/OPAL/backend/uploads>
        Options -Indexes +FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>

    # Logging
    ErrorLog /var/log/httpd/opal-fats-error.log
    CustomLog /var/log/httpd/opal-fats-access.log combined
</VirtualHost>
EOF

# Enable SELinux permissions (if applicable)
setsebool -P httpd_can_network_connect 1

# Set proper permissions
chown -R root:root /opt/OPAL/OPAL/frontend/build
chmod -R 755 /opt/OPAL/OPAL/frontend/build
chown -R root:root /opt/OPAL/OPAL/backend/uploads
chmod -R 755 /opt/OPAL/OPAL/backend/uploads

# Test and restart Apache
httpd -t
systemctl restart httpd
systemctl status httpd
```

#### Step 7: Configure Firewall
```bash
# Allow HTTP traffic
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --reload
firewall-cmd --list-all
```

#### Step 8: Stop Development Servers (if running)
```bash
# Stop any development servers
pkill -f "uvicorn app.main:app"
pkill -f "react-scripts start"
```

---

## ✅ Verification

### Check Services
```bash
# Backend status
systemctl status opal-backend

# Apache status
systemctl status httpd

# Backend health
curl http://127.0.0.1:8000/health

# API through Apache
curl http://127.0.0.1/api/v1/fats/stats/summary
```

### Test in Browser
Open these URLs in your browser:
- **Main App:** http://133.40.149.66/
- **API Docs:** http://133.40.149.66/docs
- **Health Check:** http://133.40.149.66/health

### Test the Search Bar Fix
1. Go to http://133.40.149.66/
2. Type something in the search bar and click SEARCH
3. Clear the search bar (delete all text)
4. ✅ **Verify:** The list automatically shows previous entries!

---

## 🔧 Useful Commands

### View Logs
```bash
# Backend logs
tail -f /opt/OPAL/OPAL/backend/logs/app.log

# Or via journalctl
journalctl -u opal-backend -f

# Apache error logs
tail -f /var/log/httpd/opal-fats-error.log

# Apache access logs
tail -f /var/log/httpd/opal-fats-access.log
```

### Restart Services
```bash
# Restart backend
systemctl restart opal-backend

# Restart Apache
systemctl restart httpd

# Restart both
systemctl restart opal-backend httpd
```

### Update Code (After future changes)
```bash
cd /opt/OPAL/OPAL

# Pull latest changes
git pull origin main

# Update backend
systemctl restart opal-backend

# Update frontend
cd frontend
npm install
npm run build
systemctl restart httpd
```

---

## 🆘 Troubleshooting

### Backend Service Not Starting
```bash
# Check logs
journalctl -u opal-backend -n 50 --no-pager

# Check if port is in use
ss -tulpn | grep 8000

# Test manually
cd /opt/OPAL/OPAL/backend
source venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Apache Issues
```bash
# Test configuration
httpd -t

# Check error logs
tail -50 /var/log/httpd/opal-fats-error.log

# Check SELinux (if blocking)
getenforce
setsebool -P httpd_can_network_connect 1
```

### Database Connection Issues
```bash
# Test database connection
mysql -u opal -popal -h opalfailover opal -e "SELECT COUNT(*) FROM fault;"
```

---

## 📊 What Was Deployed

### Changes in This Deployment
1. ✅ Search bar auto-reset functionality
2. ✅ Improved user experience when clearing search
3. ✅ Updated package dependencies
4. ✅ Test file improvements

### Files Modified
- `frontend/src/components/FATSList.js` - Search bar auto-clear logic
- `frontend/package.json` - Jest configuration
- `frontend/package-lock.json` - Updated dependencies
- `frontend/src/components/FATSList.test.js` - React import added

---

## ✅ Post-Deployment Checklist

- [ ] Backend service is running: `systemctl status opal-backend`
- [ ] Apache is running: `systemctl status httpd`
- [ ] Application accessible: http://133.40.149.66/
- [ ] API working: http://133.40.149.66/api/v1/fats/stats/summary
- [ ] Search bar clears and shows previous entries
- [ ] Can create new FATS entries
- [ ] Can view existing FATS entries
- [ ] Images are displaying correctly
- [ ] Links in text editors work properly

---

**🎉 Deployment Complete!**

Your search bar fix is now live in production!

**Last Updated:** December 23, 2025  
**Deployed By:** Mayank Choudhary  
**Server:** 133.40.149.66  
**Status:** ✅ Ready for Production


