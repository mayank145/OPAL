# Next Steps After Database Migration

## ✅ Completed
- ✅ Database imported to VM
- ✅ Database and user created

## Step 1: Verify Database Import

```bash
# On VM
mysql -u opal -p -e "USE opal; SHOW TABLES;"
```

You should see:
- `fault`
- `fcomments`
- `fsection`
- `fstaff`
- `days`
- `items`
- `fats_images` (if exists)

```bash
# Check record counts
mysql -u opal -p -e "USE opal; SELECT COUNT(*) as total_faults FROM fault;"
mysql -u opal -p -e "USE opal; SELECT COUNT(*) as total_comments FROM fcomments;"
```

## Step 2: Configure Backend Environment

```bash
# On VM
cd /opt/OPAL/opal-unified/backend

# Create .env file from template
cp .env.production.example .env

# Edit .env file
nano .env
```

**Update these values in .env:**

```env
# Application
DEBUG=false
APP_NAME="OPAL Unified System"
APP_VERSION="1.0.0"

# Database (use the password you set for 'opal' user)
DATABASE_URL=mysql+aiomysql://opal:your_secure_password@localhost:3306/opal
ASYNC_DATABASE_URL=mysql+aiomysql://opal:your_secure_password@localhost:3306/opal

# Security (IMPORTANT: Generate a strong secret key)
SECRET_KEY=your-generated-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24

# CORS (update with your VM IP or domain)
# Get your VM IP first: hostname -I | awk '{print $1}'
ALLOWED_ORIGINS=http://YOUR_VM_IP,http://your-domain.com

# File Upload
UPLOAD_DIR=uploads
FATS_IMAGES_DIR=uploads/fats
MAX_UPLOAD_SIZE=10485760
```

**Generate Secret Key:**
```bash
cd /opt/OPAL/opal-unified/backend
source venv/bin/activate
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
# Copy the output and paste it as SECRET_KEY in .env
```

**Get VM IP:**
```bash
hostname -I | awk '{print $1}'
# Use this IP in ALLOWED_ORIGINS
```

## Step 3: Create Required Directories

```bash
# On VM
cd /opt/OPAL/opal-unified/backend

# Create uploads and logs directories
mkdir -p uploads/fats logs
chmod 755 uploads uploads/fats logs

# If you have images to copy, place them in uploads/fats/
# chmod 644 uploads/fats/*
```

## Step 4: Test Backend Connection

```bash
# On VM
cd /opt/OPAL/opal-unified/backend
source venv/bin/activate

# Test Python imports
python3 -c "from app.main import app; print('✅ Backend imports OK')"

# Test database connection
python3 -c "
from app.db.session import engine
import asyncio
async def test():
    async with engine.connect() as conn:
        result = await conn.execute('SELECT COUNT(*) as count FROM fault')
        row = result.fetchone()
        print(f'✅ Database connected! Found {row[0]} fault records')
asyncio.run(test())
"
```

## Step 5: Start Backend Manually (Test)

```bash
# On VM
cd /opt/OPAL/opal-unified/backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**In another terminal, test:**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy",...}

curl http://localhost:8000/api/v1/fats/?limit=1
# Should return JSON with FATS entries
```

Press `Ctrl+C` to stop the backend.

## Step 6: Set Up Backend as Systemd Service

```bash
# On VM
sudo nano /etc/systemd/system/opal-backend.service
```

**Paste this content:**
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

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable opal-backend
sudo systemctl start opal-backend
sudo systemctl status opal-backend
```

**Check logs:**
```bash
sudo journalctl -u opal-backend -f
```

## Step 7: Frontend Setup

```bash
# On VM
cd /opt/OPAL/opal-unified/frontend

# Install dependencies
npm install

# Get VM IP
VM_IP=$(hostname -I | awk '{print $1}')
echo "VM IP: $VM_IP"

# Create .env.production
cat > .env.production << EOF
REACT_APP_API_URL=http://${VM_IP}:8000
EOF

# Or if using domain:
# REACT_APP_API_URL=http://your-domain.com/api

# Build frontend
npm run build
```

This creates the `build/` directory with production files.

## Step 8: Configure Apache

```bash
# On VM
# Enable required Apache modules
sudo a2enmod ssl
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod rewrite
sudo a2enmod headers
sudo a2enmod expires

# Copy Apache configuration
sudo cp /opt/OPAL/opal-unified/deployment/apache/fats-frontend.conf /etc/apache2/sites-available/opal-fats.conf

# Edit configuration
sudo nano /etc/apache2/sites-available/opal-fats.conf
```

**Update these values:**
- `ServerName your-domain.com` → Your VM IP or domain
- `DocumentRoot /path/to/opal-unified/frontend/build` → `/opt/OPAL/opal-unified/frontend/build`

**Enable and restart:**
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

## Step 9: Configure Firewall

```bash
# On VM
# Allow HTTP
sudo ufw allow 80/tcp

# Allow HTTPS (if using SSL)
sudo ufw allow 443/tcp

# Backend API (8000) - usually not needed as Apache proxies to it
# sudo ufw allow 8000/tcp
```

## Step 10: Verify Everything Works

### Test Backend
```bash
# On VM
curl http://localhost:8000/health
# Should return: {"status":"healthy",...}

curl http://localhost:8000/api/v1/fats/?limit=1
# Should return JSON
```

### Test Frontend
```bash
# On VM
curl http://localhost/
# Should return HTML
```

### Test API Through Apache
```bash
# On VM
curl http://localhost/api/health
# Should return: {"status":"healthy",...}
```

### Test in Browser
Open your browser and go to:
- `http://YOUR_VM_IP/` - Should show FATS frontend
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

# Check file permissions
sudo chown -R www-data:www-data /opt/OPAL/opal-unified/frontend/build
sudo chmod -R 755 /opt/OPAL/opal-unified/frontend/build
```

### Database Connection Issues
```bash
# Test MySQL connection
mysql -u opal -p -e "SELECT 1;"

# Verify .env file has correct credentials
cat /opt/OPAL/opal-unified/backend/.env | grep DATABASE_URL
```

## Quick Checklist

- [ ] Database imported and verified
- [ ] Backend .env configured
- [ ] Backend directories created (uploads/fats, logs)
- [ ] Backend tested manually
- [ ] Backend systemd service created and running
- [ ] Frontend dependencies installed
- [ ] Frontend .env.production configured
- [ ] Frontend built (npm run build)
- [ ] Apache modules enabled
- [ ] Apache configuration updated
- [ ] Apache site enabled and restarted
- [ ] Firewall configured
- [ ] Everything tested and working

---

**You're almost done!** Follow these steps in order, and your FATS system will be fully deployed on the VM.



