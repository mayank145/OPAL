# Virtual Machine Deployment Guide

This guide covers deploying the FATS (Fault Tracking System) on a Virtual Machine using Apache web server.

> **Note**: For detailed Apache configuration, see `deployment/apache/APACHE_SETUP_GUIDE.md`

## Prerequisites

- Ubuntu/Debian Linux VM (or similar)
- Python 3.9+ installed
- Node.js 16+ and npm installed
- MariaDB/MySQL installed and running
- Apache 2.4+ installed (for production frontend serving)

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

## Step 6: Configure Apache for Frontend

### 6.1 Install and Enable Apache Modules
```bash
# Install Apache (if not already installed)
sudo apt-get update
sudo apt-get install apache2

# Enable required modules
sudo a2enmod ssl
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod rewrite
sudo a2enmod headers
sudo a2enmod expires
```

### 6.2 Create Apache Configuration
```bash
# Copy the provided configuration
sudo cp /opt/opal-unified/deployment/apache/fats-frontend.conf /etc/apache2/sites-available/opal-fats.conf

# Edit configuration
sudo nano /etc/apache2/sites-available/opal-fats.conf
```

Update the following in the configuration file:
- `ServerName your-domain.com` - Replace with your domain or VM IP
- `DocumentRoot /path/to/opal-unified/frontend/build` - Replace with `/opt/opal-unified/frontend/build`
- SSL certificate paths (if using HTTPS)

### 6.3 Enable Site
```bash
# Test configuration
sudo apache2ctl configtest

# Enable site
sudo a2ensite opal-fats.conf

# Disable default site (optional)
sudo a2dissite 000-default.conf

# Restart Apache
sudo systemctl restart apache2
```

### 6.4 Alternative: Manual Configuration

If you prefer to create the configuration manually:

```bash
sudo nano /etc/apache2/sites-available/opal-fats.conf
```

Add this configuration:
```apache
<VirtualHost *:80>
    ServerName your-domain.com  # or vm-ip
    
    DocumentRoot /opt/opal-unified/frontend/build
    
    <Directory /opt/opal-unified/frontend/build>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
        
        # React Router - serve index.html for all routes
        RewriteEngine On
        RewriteBase /
        RewriteRule ^index\.html$ - [L]
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule . /index.html [L]
    </Directory>
    
    # Proxy API requests to backend
    ProxyPreserveHost On
    ProxyRequests Off
    
    ProxyPass /api http://127.0.0.1:8000/api
    ProxyPassReverse /api http://127.0.0.1:8000/api
    
    # Proxy /uploads for image serving
    ProxyPass /uploads http://127.0.0.1:8000/uploads
    ProxyPassReverse /uploads http://127.0.0.1:8000/uploads
    
    # Static file caching
    <LocationMatch "\.(js|css|png|jpg|jpeg|gif|ico|svg)$">
        ExpiresActive On
        ExpiresDefault "access plus 1 year"
        Header set Cache-Control "public, immutable"
    </LocationMatch>
    
    # Logging
    ErrorLog ${APACHE_LOG_DIR}/opal-fats-error.log
    CustomLog ${APACHE_LOG_DIR}/opal-fats-access.log combined
</VirtualHost>
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
# Install certbot for Apache
sudo apt install certbot python3-certbot-apache

# Get certificate
sudo certbot --apache -d your-domain.com -d www.your-domain.com

# Auto-renewal is configured automatically
sudo certbot renew --dry-run  # Test renewal
```

Certbot will automatically update your Apache configuration to:
- Enable HTTPS
- Redirect HTTP to HTTPS
- Configure SSL certificates

### Manual SSL Configuration

If using your own certificates, update the Apache configuration:

```apache
<VirtualHost *:443>
    ServerName your-domain.com
    
    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/your-domain.crt
    SSLCertificateKeyFile /etc/ssl/private/your-domain.key
    
    # ... rest of configuration ...
</VirtualHost>
```

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
# Check Apache logs
sudo tail -f /var/log/apache2/opal-fats-error.log
sudo tail -f /var/log/apache2/error.log

# Verify build directory exists
ls -la /opt/opal-unified/frontend/build/

# Check Apache configuration
sudo apache2ctl configtest

# Check if Apache is running
sudo systemctl status apache2

# Verify file permissions
sudo chown -R www-data:www-data /opt/opal-unified/frontend/build
sudo chmod -R 755 /opt/opal-unified/frontend/build
```

### Images Not Displaying
```bash
# Check file permissions
ls -la /opt/opal-unified/backend/uploads/fats/

# Check Apache can access files
sudo -u www-data ls /opt/opal-unified/backend/uploads/fats/

# Verify files exist
find /opt/opal-unified/backend/uploads/fats/ -name "2633_*" | head -5

# Check Apache error logs for permission issues
sudo tail -f /var/log/apache2/opal-fats-error.log

# Fix permissions if needed
sudo chown -R www-data:www-data /opt/opal-unified/backend/uploads/
sudo chmod -R 755 /opt/opal-unified/backend/uploads/
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

# Reload Apache (no downtime)
sudo systemctl reload apache2

# Or restart Apache (brief downtime)
sudo systemctl restart apache2
```

### View Logs
```bash
# Backend logs
sudo journalctl -u opal-backend -f

# Apache access logs
sudo tail -f /var/log/apache2/opal-fats-access.log
sudo tail -f /var/log/apache2/access.log

# Apache error logs
sudo tail -f /var/log/apache2/opal-fats-error.log
sudo tail -f /var/log/apache2/error.log

# Backend application logs
tail -f /opt/opal-unified/backend/logs/app.log
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

