# OPAL FATS - Production Deployment Instructions

## 📋 Overview

This document provides step-by-step instructions to deploy the OPAL FATS application in production mode with systemd services, Apache reverse proxy, and automated backups.

**Server IP:** 133.40.149.66  
**Current Status:** Development mode (running on ports 3000 and 8000)  
**Target:** Production mode (running on port 80 via Apache)

---

## 🎯 What This Deployment Will Achieve

- ✅ Backend runs as systemd service (auto-starts on boot)
- ✅ Frontend production build served via Apache
- ✅ Apache reverse proxy for backend API
- ✅ Security hardening (DEBUG=false, proper CORS)
- ✅ Firewall configuration
- ✅ Automated daily database and file backups
- ✅ Backup retention (keeps last 7 days)

---

## ⚠️ Prerequisites

- Root access to the server
- Apache (httpd) installed and running
- Current development servers running on ports 3000 and 8000
- Database credentials: user=opal, password=opal, database=opal

---

## 📦 Part 1: Production Deployment

### Step 1: Stop Development Servers

```bash
# Stop the development backend server
pkill -f "uvicorn app.main:app"

# Stop the development frontend server
pkill -f "react-scripts start"

# Verify they're stopped
ps aux | grep -E "(uvicorn|react-scripts)" | grep -v grep
# Should return nothing
```

### Step 2: Update Backend Configuration for Production

```bash
# Edit the backend .env file
nano /opt/OPAL/opal-unified/backend/.env
```

**Update these lines:**
```bash
# Change DEBUG to false
DEBUG=false

# Update CORS to include your actual domain (update with your domain)
ALLOWED_ORIGINS=http://133.40.149.66,http://localhost:3000
```

**Save and exit** (Ctrl+X, Y, Enter)

### Step 3: Create Backend Systemd Service

```bash
# Create the systemd service file
nano /etc/systemd/system/opal-backend.service
```

**Paste this content:**
```ini
[Unit]
Description=OPAL FATS Backend API
After=network.target mariadb.service
Wants=mariadb.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/OPAL/opal-unified/backend
Environment="PATH=/opt/OPAL/opal-unified/backend/venv/bin"
ExecStart=/opt/OPAL/opal-unified/backend/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 2
Restart=always
RestartSec=10
StandardOutput=append:/opt/OPAL/opal-unified/backend/logs/backend.log
StandardError=append:/opt/OPAL/opal-unified/backend/logs/backend.log

[Install]
WantedBy=multi-user.target
```

**Save and exit** (Ctrl+X, Y, Enter)

```bash
# Reload systemd and enable the service
systemctl daemon-reload
systemctl enable opal-backend
systemctl start opal-backend

# Check status
systemctl status opal-backend

# Should show "active (running)"
```

### Step 4: Build Frontend for Production

```bash
cd /opt/OPAL/opal-unified/frontend

# Create production environment file
cat > .env.production << 'EOF'
REACT_APP_API_URL=http://133.40.149.66
EOF

# Build the production frontend
npm run build

# Verify build was created
ls -lh build/
# Should show build directory with static files
```

### Step 5: Configure Apache Reverse Proxy

```bash
# Create Apache configuration file
nano /etc/httpd/conf.d/opal-fats.conf
```

**Paste this content:**
```apache
<VirtualHost *:80>
    ServerName 133.40.149.66
    ServerAdmin admin@localhost

    # Frontend - Serve React build
    DocumentRoot /opt/OPAL/opal-unified/frontend/build
    
    <Directory /opt/OPAL/opal-unified/frontend/build>
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
    Alias /uploads /opt/OPAL/opal-unified/backend/uploads
    <Directory /opt/OPAL/opal-unified/backend/uploads>
        Options -Indexes +FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>

    # Logging
    ErrorLog /var/log/httpd/opal-fats-error.log
    CustomLog /var/log/httpd/opal-fats-access.log combined
</VirtualHost>
```

**Save and exit** (Ctrl+X, Y, Enter)

```bash
# Enable required Apache modules
a2enmod proxy proxy_http rewrite 2>/dev/null || echo "Modules may already be enabled"

# On RHEL/CentOS, ensure SELinux allows httpd network connections
setsebool -P httpd_can_network_connect 1

# Set proper permissions
chown -R root:root /opt/OPAL/opal-unified/frontend/build
chmod -R 755 /opt/OPAL/opal-unified/frontend/build
chown -R root:root /opt/OPAL/opal-unified/backend/uploads
chmod -R 755 /opt/OPAL/opal-unified/backend/uploads

# Test Apache configuration
httpd -t
# Should return "Syntax OK"

# Restart Apache
systemctl restart httpd
systemctl status httpd
```

### Step 6: Configure Firewall

```bash
# Allow HTTP traffic
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --reload

# Verify firewall rules
firewall-cmd --list-all
```

### Step 7: Verify Production Deployment

```bash
# Check backend service
systemctl status opal-backend
curl http://127.0.0.1:8000/health

# Check frontend via Apache
curl -I http://127.0.0.1/

# Check API via Apache
curl http://127.0.0.1/api/v1/fats/stats/summary

# Check from external access (replace with actual IP)
curl http://133.40.149.66/health
```

**Open in browser:**
- Main Application: `http://133.40.149.66/`
- API Docs: `http://133.40.149.66/docs`

---

## 📦 Part 2: Backup Configuration

### Step 1: Create Backup Directory

```bash
mkdir -p /opt/backups/opal-fats/{database,files}
chmod 700 /opt/backups/opal-fats
```

### Step 2: Create Database Backup Script

```bash
nano /opt/backups/opal-fats/backup-database.sh
```

**Paste this content:**
```bash
#!/bin/bash
# OPAL FATS Database Backup Script

BACKUP_DIR="/opt/backups/opal-fats/database"
DB_USER="opal"
DB_PASS="opal"
DB_NAME="opal"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/opal_db_${DATE}.sql.gz"
RETENTION_DAYS=7

# Create backup directory if it doesn't exist
mkdir -p "${BACKUP_DIR}"

# Perform database backup
echo "Starting database backup: ${BACKUP_FILE}"
mysqldump -u ${DB_USER} -p${DB_PASS} ${DB_NAME} | gzip > "${BACKUP_FILE}"

if [ $? -eq 0 ]; then
    echo "✅ Database backup completed successfully"
    ls -lh "${BACKUP_FILE}"
else
    echo "❌ Database backup failed"
    exit 1
fi

# Remove backups older than RETENTION_DAYS
echo "Cleaning up old backups (keeping last ${RETENTION_DAYS} days)..."
find "${BACKUP_DIR}" -name "opal_db_*.sql.gz" -type f -mtime +${RETENTION_DAYS} -delete

echo "Backup process completed"
echo "Current backups:"
ls -lh "${BACKUP_DIR}"
```

**Save and exit** (Ctrl+X, Y, Enter)

```bash
# Make script executable
chmod +x /opt/backups/opal-fats/backup-database.sh

# Test the backup script
/opt/backups/opal-fats/backup-database.sh
```

### Step 3: Create Files Backup Script

```bash
nano /opt/backups/opal-fats/backup-files.sh
```

**Paste this content:**
```bash
#!/bin/bash
# OPAL FATS Files Backup Script (Images and Uploads)

BACKUP_DIR="/opt/backups/opal-fats/files"
SOURCE_DIR="/opt/OPAL/opal-unified/backend/uploads"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/opal_files_${DATE}.tar.gz"
RETENTION_DAYS=7

# Create backup directory if it doesn't exist
mkdir -p "${BACKUP_DIR}"

# Perform files backup
echo "Starting files backup: ${BACKUP_FILE}"
tar -czf "${BACKUP_FILE}" -C "$(dirname ${SOURCE_DIR})" "$(basename ${SOURCE_DIR})"

if [ $? -eq 0 ]; then
    echo "✅ Files backup completed successfully"
    ls -lh "${BACKUP_FILE}"
else
    echo "❌ Files backup failed"
    exit 1
fi

# Remove backups older than RETENTION_DAYS
echo "Cleaning up old backups (keeping last ${RETENTION_DAYS} days)..."
find "${BACKUP_DIR}" -name "opal_files_*.tar.gz" -type f -mtime +${RETENTION_DAYS} -delete

echo "Backup process completed"
echo "Current backups:"
ls -lh "${BACKUP_DIR}"
```

**Save and exit** (Ctrl+X, Y, Enter)

```bash
# Make script executable
chmod +x /opt/backups/opal-fats/backup-files.sh

# Test the backup script
/opt/backups/opal-fats/backup-files.sh
```

### Step 4: Create Combined Backup Script

```bash
nano /opt/backups/opal-fats/backup-all.sh
```

**Paste this content:**
```bash
#!/bin/bash
# OPAL FATS - Complete Backup Script

echo "================================================"
echo "OPAL FATS Backup - $(date)"
echo "================================================"
echo ""

# Run database backup
echo "1. Backing up database..."
/opt/backups/opal-fats/backup-database.sh
echo ""

# Run files backup
echo "2. Backing up files..."
/opt/backups/opal-fats/backup-files.sh
echo ""

echo "================================================"
echo "Backup completed - $(date)"
echo "================================================"
```

**Save and exit** (Ctrl+X, Y, Enter)

```bash
# Make script executable
chmod +x /opt/backups/opal-fats/backup-all.sh

# Test the combined backup
/opt/backups/opal-fats/backup-all.sh
```

### Step 5: Set Up Automated Daily Backups (Cron)

```bash
# Edit crontab
crontab -e
```

**Add this line at the end:**
```cron
# OPAL FATS Daily Backup - Runs at 2:00 AM every day
0 2 * * * /opt/backups/opal-fats/backup-all.sh >> /opt/backups/opal-fats/backup.log 2>&1
```

**Save and exit** (in vi: press Esc, type :wq, press Enter)

```bash
# Verify cron job was added
crontab -l | grep opal-fats
```

### Step 6: Create Restore Scripts

**Database Restore Script:**
```bash
nano /opt/backups/opal-fats/restore-database.sh
```

**Paste this content:**
```bash
#!/bin/bash
# OPAL FATS Database Restore Script

BACKUP_DIR="/opt/backups/opal-fats/database"
DB_USER="opal"
DB_PASS="opal"
DB_NAME="opal"

# Check if backup file is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <backup_file.sql.gz>"
    echo ""
    echo "Available backups:"
    ls -lh "${BACKUP_DIR}"/opal_db_*.sql.gz
    exit 1
fi

BACKUP_FILE="$1"

# Check if file exists
if [ ! -f "${BACKUP_FILE}" ]; then
    echo "Error: Backup file not found: ${BACKUP_FILE}"
    exit 1
fi

# Confirm restore
echo "⚠️  WARNING: This will replace the current database!"
echo "Backup file: ${BACKUP_FILE}"
echo ""
read -p "Are you sure you want to restore? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Restore cancelled"
    exit 0
fi

# Restore database
echo "Restoring database from ${BACKUP_FILE}..."
gunzip < "${BACKUP_FILE}" | mysql -u ${DB_USER} -p${DB_PASS} ${DB_NAME}

if [ $? -eq 0 ]; then
    echo "✅ Database restored successfully"
else
    echo "❌ Database restore failed"
    exit 1
fi
```

**Save and exit** (Ctrl+X, Y, Enter)

```bash
chmod +x /opt/backups/opal-fats/restore-database.sh
```

**Files Restore Script:**
```bash
nano /opt/backups/opal-fats/restore-files.sh
```

**Paste this content:**
```bash
#!/bin/bash
# OPAL FATS Files Restore Script

BACKUP_DIR="/opt/backups/opal-fats/files"
RESTORE_DIR="/opt/OPAL/opal-unified/backend"

# Check if backup file is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <backup_file.tar.gz>"
    echo ""
    echo "Available backups:"
    ls -lh "${BACKUP_DIR}"/opal_files_*.tar.gz
    exit 1
fi

BACKUP_FILE="$1"

# Check if file exists
if [ ! -f "${BACKUP_FILE}" ]; then
    echo "Error: Backup file not found: ${BACKUP_FILE}"
    exit 1
fi

# Confirm restore
echo "⚠️  WARNING: This will replace current files!"
echo "Backup file: ${BACKUP_FILE}"
echo ""
read -p "Are you sure you want to restore? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Restore cancelled"
    exit 0
fi

# Restore files
echo "Restoring files from ${BACKUP_FILE}..."
tar -xzf "${BACKUP_FILE}" -C "${RESTORE_DIR}"

if [ $? -eq 0 ]; then
    echo "✅ Files restored successfully"
    chown -R root:root "${RESTORE_DIR}/uploads"
    chmod -R 755 "${RESTORE_DIR}/uploads"
else
    echo "❌ Files restore failed"
    exit 1
fi
```

**Save and exit** (Ctrl+X, Y, Enter)

```bash
chmod +x /opt/backups/opal-fats/restore-files.sh
```

---

## ✅ Verification Checklist

### Production Deployment
- [ ] Backend systemd service is running: `systemctl status opal-backend`
- [ ] Frontend build exists: `ls /opt/OPAL/opal-unified/frontend/build/`
- [ ] Apache is serving the application: `curl http://133.40.149.66/`
- [ ] API is accessible: `curl http://133.40.149.66/api/v1/fats/stats/summary`
- [ ] Can access in browser: `http://133.40.149.66/`
- [ ] DEBUG is false: `grep DEBUG /opt/OPAL/opal-unified/backend/.env`

### Backup Configuration
- [ ] Backup directory exists: `ls -la /opt/backups/opal-fats/`
- [ ] Database backup script works: `/opt/backups/opal-fats/backup-database.sh`
- [ ] Files backup script works: `/opt/backups/opal-fats/backup-files.sh`
- [ ] Cron job is configured: `crontab -l | grep opal-fats`
- [ ] Backups exist: `ls -lh /opt/backups/opal-fats/database/ /opt/backups/opal-fats/files/`

---

## 🔧 Useful Commands

### Service Management
```bash
# Check backend status
systemctl status opal-backend

# Restart backend
systemctl restart opal-backend

# View backend logs
journalctl -u opal-backend -f

# Or view log file
tail -f /opt/OPAL/opal-unified/backend/logs/backend.log

# Restart Apache
systemctl restart httpd
```

### Manual Backups
```bash
# Backup everything
/opt/backups/opal-fats/backup-all.sh

# Backup database only
/opt/backups/opal-fats/backup-database.sh

# Backup files only
/opt/backups/opal-fats/backup-files.sh

# List backups
ls -lh /opt/backups/opal-fats/database/
ls -lh /opt/backups/opal-fats/files/
```

### Restore
```bash
# List available database backups
ls -lh /opt/backups/opal-fats/database/

# Restore database
/opt/backups/opal-fats/restore-database.sh /opt/backups/opal-fats/database/opal_db_YYYYMMDD_HHMMSS.sql.gz

# Restore files
/opt/backups/opal-fats/restore-files.sh /opt/backups/opal-fats/files/opal_files_YYYYMMDD_HHMMSS.tar.gz
```

---

## 🆘 Troubleshooting

### Backend service won't start
```bash
# Check logs
journalctl -u opal-backend -n 50

# Check if port 8000 is in use
ss -tulpn | grep 8000

# Test backend manually
cd /opt/OPAL/opal-unified/backend
source venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Apache not serving files
```bash
# Check Apache status
systemctl status httpd

# Check Apache error logs
tail -f /var/log/httpd/opal-fats-error.log

# Test configuration
httpd -t

# Check SELinux (if applicable)
getenforce
setsebool -P httpd_can_network_connect 1
```

### Backup script fails
```bash
# Check permissions
ls -la /opt/backups/opal-fats/

# Test database connection
mysql -u opal -popal opal -e "SELECT 1;"

# Check disk space
df -h
```

---

## 📞 Support

If you encounter issues:
1. Check the logs in `/opt/OPAL/opal-unified/backend/logs/`
2. Check Apache logs in `/var/log/httpd/`
3. Use `systemctl status opal-backend` to check service status
4. Verify database connection with `mysql -u opal -popal opal`

---

**Document Version:** 1.0  
**Last Updated:** December 5, 2025  
**Application:** OPAL FATS - Fault Tracking System

