# Next Steps for VM Deployment

Based on your current progress, here are the next steps to complete the FATS system deployment:

## Current Status ✅
- ✅ Python 3 + virtual environment installed
- ✅ Node.js and npm installed
- ✅ Apache HTTP server installed
- ✅ MariaDB installed and running
- ✅ Repository extracted to `/opt/OPAL/opal-unified`
- ✅ Backend virtual environment created
- ✅ Backend requirements installed

## Step 1: Database Setup

### 1.1 Create Database and User
```bash
# Login to MariaDB as root
sudo mysql -u root -p

# In MySQL prompt, run:
CREATE DATABASE IF NOT EXISTS opal;
CREATE USER IF NOT EXISTS 'opal'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON opal.* TO 'opal'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 1.2 Import Database Schema (if you have existing data)
```bash
# If you have a database dump
mysql -u opal -p opal < your_database_dump.sql

# Or if you need to create tables from scratch, check:
ls -la /opt/OPAL/opal-unified/deployment/init-scripts/
```

### 1.3 Verify Database
```bash
mysql -u opal -p -e "USE opal; SHOW TABLES;"
```

You should see tables like:
- `fault`
- `fcomments`
- `fsection`
- `fstaff`

## Step 2: Configure Backend Environment

### 2.1 Create Environment File
```bash
cd /opt/OPAL/opal-unified/backend
cp .env.production.example .env
nano .env
```

### 2.2 Update .env with your settings:
```env
# Application
DEBUG=false
APP_NAME="OPAL Unified System"
APP_VERSION="1.0.0"

# Database (use the password you set above)
DATABASE_URL=mysql+aiomysql://opal:your_secure_password@localhost:3306/opal
ASYNC_DATABASE_URL=mysql+aiomysql://opal:your_secure_password@localhost:3306/opal

# Security (IMPORTANT: Generate a strong secret key)
SECRET_KEY=your-generated-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24

# CORS (update with your domain or IP)
ALLOWED_ORIGINS=http://your-vm-ip,http://your-domain.com

# File Upload
UPLOAD_DIR=uploads
FATS_IMAGES_DIR=uploads/fats
MAX_UPLOAD_SIZE=10485760
```

### 2.3 Generate Secret Key
```bash
cd /opt/OPAL/opal-unified/backend
source venv/bin/activate
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
# Copy the output and paste it as SECRET_KEY in .env
```

### 2.4 Create Uploads Directory
```bash
cd /opt/OPAL/opal-unified/backend
mkdir -p uploads/fats
chmod 755 uploads uploads/fats

# If you have images to copy, place them in uploads/fats/
```

### 2.5 Create Logs Directory
```bash
mkdir -p logs
chmod 755 logs
```

## Step 3: Test Backend

### 3.1 Test Backend Connection
```bash
cd /opt/OPAL/opal-unified/backend
source venv/bin/activate
python3 -c "from app.main import app; print('✅ Backend imports successfully')"
```

### 3.2 Test Database Connection
```bash
# Still in backend directory with venv activated
python3 -c "
from app.db.session import engine
import asyncio
async def test():
    async with engine.connect() as conn:
        print('✅ Database connection successful')
asyncio.run(test())
"
```

### 3.3 Start Backend Manually (for testing)
```bash
cd /opt/OPAL/opal-unified/backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

In another terminal, test:
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy",...}
```

Press Ctrl+C to stop the backend.

## Step 4: Set Up Backend as Systemd Service

### 4.1 Create Service File
```bash
sudo nano /etc/systemd/system/opal-backend.service
```

### 4.2 Add this content:
```ini
[Unit]
Description=OPAL FATS Backend API
After=network.target mysql.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/OPAL/opal-unified/backend
Environment="PATH=/opt/OPAL/opal-unified/backend/venv/bin"
ExecStart=/opt/OPAL/opal-unified/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 4.3 Enable and Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable opal-backend
sudo systemctl start opal-backend
sudo systemctl status opal-backend
```

### 4.4 Check Logs
```bash
sudo journalctl -u opal-backend -f
```

## Step 5: Frontend Setup

### 5.1 Navigate to Frontend
```bash
cd /opt/OPAL/opal-unified/frontend
```

### 5.2 Install Dependencies
```bash
npm install
```

### 5.3 Create Environment File
```bash
# Get your VM IP address
hostname -I | awk '{print $1}'

# Create .env.production
cat > .env.production << EOF
REACT_APP_API_URL=http://YOUR_VM_IP:8000
EOF

# Or if using domain:
# REACT_APP_API_URL=http://your-domain.com/api
```

Replace `YOUR_VM_IP` with your actual VM IP address.

### 5.4 Build Frontend
```bash
npm run build
```

This creates the `build/` directory with production files.

## Step 6: Configure Apache

### 6.1 Enable Required Apache Modules
```bash
sudo a2enmod ssl
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod rewrite
sudo a2enmod headers
sudo a2enmod expires
```

### 6.2 Copy Apache Configuration
```bash
sudo cp /opt/OPAL/opal-unified/deployment/apache/fats-frontend.conf /etc/apache2/sites-available/opal-fats.conf
```

### 6.3 Edit Configuration
```bash
sudo nano /etc/apache2/sites-available/opal-fats.conf
```

Update these values:
- `ServerName your-domain.com` → Your domain or VM IP
- `DocumentRoot /path/to/opal-unified/frontend/build` → `/opt/OPAL/opal-unified/frontend/build`

### 6.4 Enable Site
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

## Step 7: Firewall Configuration

### 7.1 Allow Required Ports
```bash
# Allow HTTP
sudo ufw allow 80/tcp

# Allow HTTPS (if using SSL)
sudo ufw allow 443/tcp

# Backend API (8000) - only if needed externally
# Usually not needed as Apache proxies to it
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

### 8.3 Check API Through Apache
```bash
curl http://localhost/api/health
# Should return: {"status":"healthy",...}
```

### 8.4 Access in Browser
Open your browser and go to:
- `http://YOUR_VM_IP/` - Should show the FATS frontend
- `http://YOUR_VM_IP/api/docs` - API documentation

## Troubleshooting

### Backend Not Starting
```bash
# Check service status
sudo systemctl status opal-backend

# Check logs
sudo journalctl -u opal-backend -f

# Check if port is in use
sudo netstat -tlnp | grep 8000
```

### Frontend Not Loading
```bash
# Check Apache logs
sudo tail -f /var/log/apache2/opal-fats-error.log

# Verify build directory exists
ls -la /opt/OPAL/opal-unified/frontend/build/

# Check Apache configuration
sudo apache2ctl configtest

# Check file permissions
sudo chown -R www-data:www-data /opt/OPAL/opal-unified/frontend/build
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

## Next Steps After Deployment

1. ✅ Set up SSL/HTTPS (Let's Encrypt)
2. ✅ Configure backups
3. ✅ Set up monitoring
4. ✅ Test all functionality
5. ✅ Document your specific configuration

---

**You're almost there!** Follow these steps in order, and you'll have the FATS system running on your VM.



