# Virtual Machine Deployment Guide

## Prerequisites

- Ubuntu/Debian Linux VM (or similar)
- Python 3.9+ installed
- Node.js 16+ and npm installed
- MariaDB/MySQL installed and running
- Nginx installed (for production frontend serving)

## Step 1: Transfer Files to VM

### Using SCP
```bash
# From your local machine
scp -r opal-unified/ user@vm-ip:/opt/opal-unified/
```

### Using rsync (Recommended)
```bash
# Excludes unnecessary files automatically
rsync -av --exclude='node_modules' --exclude='venv' --exclude='__pycache__' \
  opal-unified/ user@vm-ip:/opt/opal-unified/
```

## Step 2: Backend Setup

### 2.1 Navigate to Backend Directory
```bash
cd /opt/opal-unified/backend
```

### 2.2 Create Python Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2.3 Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 2.4 Configure Environment Variables
```bash
cp env.example .env
nano .env  # or use your preferred editor
```

Edit `.env` with your database credentials:
```env
DATABASE_URL=mysql+aiomysql://opal:your_password@localhost:3306/opal
ASYNC_DATABASE_URL=mysql+aiomysql://opal:your_password@localhost:3306/opal
UPLOAD_DIR=uploads
FATS_IMAGES_DIR=uploads/fats
MAX_UPLOAD_SIZE=10485760
DEBUG=False
SECRET_KEY=your-secret-key-change-this
```

### 2.5 Set Up Uploads Directory
```bash
mkdir -p uploads/fats
chmod 755 uploads
chmod 755 uploads/fats
# If images were transferred, ensure proper permissions
chmod 644 uploads/fats/* 2>/dev/null || true
```

### 2.6 Test Backend Connection
```bash
source venv/bin/activate
python3 -c "from app.main import app; print('✅ Backend imports successfully')"
```

## Step 3: Frontend Setup

### 3.1 Navigate to Frontend Directory
```bash
cd /opt/opal-unified/frontend
```

### 3.2 Install Node Dependencies
```bash
npm install
```

### 3.3 Configure Environment Variables
```bash
cat > .env << EOF
REACT_APP_API_URL=http://vm-ip:8000
EOF
```

Replace `vm-ip` with your VM's IP address or domain name.

### 3.4 Build for Production
```bash
npm run build
```

This creates a `build/` directory with optimized production files.

## Step 4: Database Setup

### 4.1 Verify Database Connection
```bash
mysql -u opal -p -e "USE opal; SHOW TABLES;"
```

You should see:
- `fault`
- `fcomments`
- `fsection`
- `fstaff`

### 4.2 Verify Data
```bash
mysql -u opal -p -e "USE opal; SELECT COUNT(*) FROM fault;"
```

## Step 5: Start Backend Service

### Option A: Manual Start (Testing)
```bash
cd /opt/opal-unified/backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Option B: Systemd Service (Production)

Create service file:
```bash
sudo nano /etc/systemd/system/opal-backend.service
```

Add this content:
```ini
[Unit]
Description=OPAL FATS Backend API
After=network.target mysql.service

[Service]
Type=simple
User=your-username
WorkingDirectory=/opt/opal-unified/backend
Environment="PATH=/opt/opal-unified/backend/venv/bin"
ExecStart=/opt/opal-unified/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable opal-backend
sudo systemctl start opal-backend
sudo systemctl status opal-backend
```

## Step 6: Configure Nginx for Frontend

### 6.1 Create Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/opal-fats
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # or vm-ip

    # Serve frontend build files
    root /opt/opal-unified/frontend/build;
    index index.html;

    # Frontend routes
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Proxy API requests to backend
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Serve uploaded images
    location /uploads/ {
        alias /opt/opal-unified/backend/uploads/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### 6.2 Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/opal-fats /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

## Step 7: Firewall Configuration

### Allow Required Ports
```bash
# Allow HTTP (80)
sudo ufw allow 80/tcp

# Allow HTTPS (443) if using SSL
sudo ufw allow 443/tcp

# Backend API (8000) - only if needed externally
# sudo ufw allow 8000/tcp
```

## Step 8: Verify Deployment

### 8.1 Check Backend
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy",...}
```

### 8.2 Check Frontend
```bash
curl http://localhost/
# Should return HTML
```

### 8.3 Check API
```bash
curl http://localhost/api/v1/fats/?limit=5
# Should return JSON array
```

### 8.4 Check Images
```bash
curl http://localhost/api/v1/fats/2633/images
# Should return image list
```

## Step 9: SSL/HTTPS (Optional but Recommended)

### Using Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

Update Nginx config to redirect HTTP to HTTPS.

## Troubleshooting

### Backend Not Starting
```bash
# Check logs
sudo journalctl -u opal-backend -f

# Check if port is in use
sudo netstat -tlnp | grep 8000

# Test database connection
cd /opt/opal-unified/backend
source venv/bin/activate
python3 -c "from app.db.session import engine; import asyncio; asyncio.run(engine.connect())"
```

### Frontend Not Loading
```bash
# Check Nginx logs
sudo tail -f /var/log/nginx/error.log

# Verify build directory exists
ls -la /opt/opal-unified/frontend/build/

# Check Nginx configuration
sudo nginx -t
```

### Images Not Displaying
```bash
# Check file permissions
ls -la /opt/opal-unified/backend/uploads/fats/

# Check Nginx can access files
sudo -u www-data ls /opt/opal-unified/backend/uploads/fats/

# Verify files exist
find /opt/opal-unified/backend/uploads/fats/ -name "2633_*" | head -5
```

### Database Connection Issues
```bash
# Test MySQL connection
mysql -u opal -p -e "SELECT 1;"

# Check if database exists
mysql -u opal -p -e "SHOW DATABASES LIKE 'opal';"

# Verify user permissions
mysql -u root -p -e "SHOW GRANTS FOR 'opal'@'localhost';"
```

## Maintenance

### Update Backend
```bash
cd /opt/opal-unified/backend
source venv/bin/activate
pip install -r requirements.txt --upgrade
sudo systemctl restart opal-backend
```

### Update Frontend
```bash
cd /opt/opal-unified/frontend
npm install
npm run build
sudo systemctl reload nginx
```

### View Logs
```bash
# Backend logs
sudo journalctl -u opal-backend -f

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

### Backup
```bash
# Backup database
mysqldump -u opal -p opal > backup_$(date +%Y%m%d).sql

# Backup images
tar -czf images_backup_$(date +%Y%m%d).tar.gz /opt/opal-unified/backend/uploads/fats/
```

## Security Recommendations

1. **Change default passwords** in `.env`
2. **Use strong SECRET_KEY** for JWT (if implemented)
3. **Restrict database user permissions** to only necessary operations
4. **Enable firewall** and only open necessary ports
5. **Use HTTPS** with SSL certificates
6. **Regular updates**: Keep system and dependencies updated
7. **File permissions**: Ensure proper ownership and permissions
8. **Log monitoring**: Monitor logs for suspicious activity

## File Permissions

```bash
# Backend files
sudo chown -R your-user:your-user /opt/opal-unified/backend
chmod 644 /opt/opal-unified/backend/app/**/*.py
chmod 755 /opt/opal-unified/backend/uploads
chmod 755 /opt/opal-unified/backend/uploads/fats
chmod 644 /opt/opal-unified/backend/uploads/fats/*

# Frontend files
sudo chown -R your-user:your-user /opt/opal-unified/frontend
chmod 755 /opt/opal-unified/frontend/build
```

---

**Deployment Complete!** 🎉

Your Fault Management System should now be accessible at:
- Frontend: `http://your-vm-ip/` or `http://your-domain.com/`
- API: `http://your-vm-ip:8000/api/v1/`
- API Docs: `http://your-vm-ip:8000/docs`

