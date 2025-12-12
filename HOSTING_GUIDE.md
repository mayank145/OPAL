# Fault Tracking System - Complete Hosting Guide

## 📋 Table of Contents
1. [Overview](#overview)
2. [What Changed from Legacy](#what-changed-from-legacy)
3. [Prerequisites](#prerequisites)
4. [Option 1: Docker Deployment (Recommended)](#option-1-docker-deployment-recommended)
5. [Option 2: Manual Deployment](#option-2-manual-deployment)
6. [Database Migration](#database-migration)
7. [Configuration Changes](#configuration-changes)
8. [Production Deployment](#production-deployment)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

The new Fault Tracking System uses a **modern architecture**:
- **Backend**: FastAPI (Python) - REST API
- **Frontend**: React - Single Page Application
- **Database**: MariaDB/MySQL (same as legacy)
- **Deployment**: Docker containers or manual setup

---

## 🔄 What Changed from Legacy

### Legacy System (Old)
- ❌ CGI scripts (fatsone.py, fatslist.py)
- ❌ Apache with mod_cgi
- ❌ Server-side HTML generation
- ❌ New process per request
- ❌ Direct SQL queries (security risk)

### New System (Modern)
- ✅ FastAPI REST API
- ✅ React frontend (client-side rendering)
- ✅ Docker containers
- ✅ Connection pooling
- ✅ Parameterized queries (secure)

### Key Differences

| Aspect | Legacy | New System |
|--------|--------|------------|
| **Web Server** | Apache + mod_cgi | Nginx (reverse proxy) or direct |
| **Backend** | Python CGI scripts | FastAPI (Python 3.11+) |
| **Frontend** | Server-rendered HTML | React SPA |
| **Ports** | Port 80 (Apache) | Port 3000 (Frontend), 8000 (Backend) |
| **Database** | Direct MySQLdb | SQLAlchemy with connection pooling |
| **File Structure** | `/var/www/html/opal/` | Docker containers or custom paths |

---

## 📦 Prerequisites

### Required Software

1. **Docker & Docker Compose** (for Docker deployment)
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install docker.io docker-compose
   
   # macOS
   brew install docker docker-compose
   
   # Windows
   Download Docker Desktop from docker.com
   ```

2. **OR Manual Setup Requirements**:
   - Python 3.9+ (for backend)
   - Node.js 18+ (for frontend)
   - MariaDB/MySQL (database)
   - Nginx (optional, for production)

### Server Requirements

- **CPU**: 2+ cores recommended
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 10GB+ free space
- **OS**: Linux (Ubuntu 20.04+), macOS, or Windows

---

## 🐳 Option 1: Docker Deployment (Recommended)

### Step 1: Prepare the Server

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
sudo apt-get install -y docker.io docker-compose

# Add user to docker group (optional)
sudo usermod -aG docker $USER
newgrp docker
```

### Step 2: Clone/Copy Project Files

```bash
# Navigate to project directory
cd /path/to/opal-unified

# Or if using git
git clone <repository-url>
cd opal-unified
```

### Step 3: Configure Environment

```bash
cd deployment

# Create .env file
cat > .env << EOF
# Database Configuration
MYSQL_ROOT_PASSWORD=your_secure_root_password
MYSQL_PASSWORD=your_secure_opal_password

# Optional: Custom ports
# FRONTEND_PORT=3000
# BACKEND_PORT=8000
# DATABASE_PORT=3306
EOF

# Edit with your passwords
nano .env
```

### Step 4: Update Database Connection (if using existing database)

Edit `deployment/docker-compose.yml`:

```yaml
backend:
  environment:
    # If using external database (not Docker container)
    DATABASE_URL: mysql+aiomysql://opal:password@host.docker.internal:3306/opal
    ASYNC_DATABASE_URL: mysql+aiomysql://opal:password@host.docker.internal:3306/opal
```

**OR** if using the Docker MariaDB container, it's already configured.

### Step 5: Import Existing Database (if migrating from legacy)

```bash
# Export from legacy system
mysqldump -u opal -p opal > opal_backup.sql

# Import into new system
# Option A: If using Docker MariaDB
docker exec -i opal-mariadb mysql -u opal -popal_password opal < opal_backup.sql

# Option B: If using external database
mysql -u opal -p opal < opal_backup.sql
```

### Step 6: Start the System

```bash
cd deployment

# Build and start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Step 7: Verify Deployment

```bash
# Check backend
curl http://localhost:8000/health

# Check frontend
curl http://localhost:3000

# Check database connection
curl http://localhost:8000/health/db
```

### Step 8: Access the Application

- **Frontend**: http://your-server-ip:3000
- **Backend API**: http://your-server-ip:8000
- **API Docs**: http://your-server-ip:8000/docs

---

## 🛠️ Option 2: Manual Deployment

### Step 1: Install Prerequisites

```bash
# Install Python 3.9+
sudo apt-get install python3.9 python3.9-venv python3-pip

# Install Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install MariaDB
sudo apt-get install mariadb-server
```

### Step 2: Setup Database

```bash
# Secure MariaDB installation
sudo mysql_secure_installation

# Create database and user
sudo mysql -u root -p
```

```sql
CREATE DATABASE opal CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'opal'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON opal.* TO 'opal'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Step 3: Import Legacy Database

```bash
# Export from legacy system
mysqldump -u opal -p opal > opal_backup.sql

# Import to new database
mysql -u opal -p opal < opal_backup.sql
```

### Step 4: Setup Backend

```bash
cd opal-unified/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DATABASE_URL=mysql+aiomysql://opal:your_password@localhost:3306/opal
ASYNC_DATABASE_URL=mysql+aiomysql://opal:your_password@localhost:3306/opal
DEBUG=false
SECRET_KEY=your-secret-key-change-this
EOF

# Test connection
python3 -c "from app.db.session import engine; print('Database connection OK')"
```

### Step 5: Setup Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Create .env file (optional)
cat > .env << EOF
REACT_APP_API_URL=http://localhost:8000
EOF
```

### Step 6: Start Backend

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Step 7: Start Frontend (in new terminal)

```bash
cd frontend
npm start
```

### Step 8: Configure Nginx (Production)

```bash
sudo apt-get install nginx

# Create nginx config
sudo nano /etc/nginx/sites-available/fault-tracking
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/fault-tracking /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔧 Configuration Changes

### 1. Database Connection

**File**: `backend/app/core/config.py` or `.env`

```python
# For local database
DATABASE_URL=mysql+aiomysql://opal:password@localhost:3306/opal

# For remote database
DATABASE_URL=mysql+aiomysql://opal:password@192.168.1.100:3306/opal
```

### 2. CORS Settings

**File**: `backend/app/core/config.py`

```python
allowed_origins: List[str] = [
    "http://localhost:3000",
    "http://your-domain.com",
    "https://your-domain.com"
]
```

### 3. Frontend API URL

**File**: `frontend/src/services/api.js` or `.env`

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

### 4. File Upload Directory

**File**: `backend/app/core/config.py`

```python
upload_dir: str = "/var/www/uploads"  # Production path
fats_images_dir: str = "/var/www/uploads/fats"
```

**Create directory**:
```bash
sudo mkdir -p /var/www/uploads/fats
sudo chown -R www-data:www-data /var/www/uploads
```

---

## 🚀 Production Deployment

### Using Systemd (Linux)

**Backend Service** (`/etc/systemd/system/fault-tracking-backend.service`):

```ini
[Unit]
Description=Fault Tracking System Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/fault-tracking/backend
Environment="PATH=/opt/fault-tracking/backend/venv/bin"
ExecStart=/opt/fault-tracking/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable fault-tracking-backend
sudo systemctl start fault-tracking-backend
```

**Frontend** (build and serve with nginx):

```bash
cd frontend
npm run build
sudo cp -r build/* /var/www/html/
```

### Using PM2 (Node.js process manager)

```bash
# Install PM2
npm install -g pm2

# Start frontend
cd frontend
pm2 start npm --name "fault-tracking-frontend" -- start

# Save PM2 configuration
pm2 save
pm2 startup
```

---

## 🔄 Database Migration

### Step 1: Export Legacy Data

```bash
# From legacy server
mysqldump -u opal -p opal fault fcomments fsection fstaff > legacy_export.sql
```

### Step 2: Import to New System

```bash
# To new system
mysql -u opal -p opal < legacy_export.sql
```

### Step 3: Verify Data

```bash
# Check record counts
mysql -u opal -p opal -e "SELECT COUNT(*) FROM fault;"
mysql -u opal -p opal -e "SELECT COUNT(*) FROM fcomments;"
```

---

## 🔐 Security Checklist

- [ ] Change default passwords in `.env`
- [ ] Set `DEBUG=false` in production
- [ ] Use strong `SECRET_KEY`
- [ ] Configure firewall (allow only 80, 443, 22)
- [ ] Enable HTTPS/SSL certificates
- [ ] Restrict database access (bind to localhost)
- [ ] Set proper file permissions
- [ ] Configure CORS for specific domains only
- [ ] Enable rate limiting in Nginx
- [ ] Regular database backups

---

## 🐛 Troubleshooting

### Backend won't start

```bash
# Check logs
docker-compose logs backend
# OR
journalctl -u fault-tracking-backend -f

# Check database connection
cd backend
source venv/bin/activate
python3 -c "from app.db.session import engine; import asyncio; asyncio.run(engine.connect())"
```

### Frontend can't connect to backend

1. Check CORS settings in `backend/app/core/config.py`
2. Verify backend is running: `curl http://localhost:8000/health`
3. Check frontend API URL in `frontend/src/services/api.js`

### Database connection errors

```bash
# Test connection
mysql -u opal -p -h localhost opal

# Check if MariaDB is running
sudo systemctl status mariadb

# Check firewall
sudo ufw status
```

### Port conflicts

```bash
# Check what's using port 8000
sudo lsof -i :8000

# Change port in docker-compose.yml or uvicorn command
```

---

## 📊 Monitoring

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Database health
curl http://localhost:8000/health/db

# Frontend
curl http://localhost:3000
```

### Logs

**Docker**:
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

**Manual**:
```bash
# Backend logs (if using systemd)
journalctl -u fault-tracking-backend -f

# Frontend logs (if using PM2)
pm2 logs fault-tracking-frontend
```

---

## ✅ Deployment Checklist

- [ ] Server prepared (Docker or manual setup)
- [ ] Database created and configured
- [ ] Legacy data imported (if applicable)
- [ ] Backend configured and running
- [ ] Frontend configured and running
- [ ] CORS settings updated
- [ ] File upload directory created
- [ ] Nginx configured (production)
- [ ] SSL certificates installed (production)
- [ ] Firewall configured
- [ ] Monitoring setup
- [ ] Backup strategy in place

---

## 📞 Support

If you encounter issues:
1. Check logs (see Troubleshooting section)
2. Verify all prerequisites are installed
3. Test database connection separately
4. Check network connectivity
5. Review configuration files

---

## 🎉 Success!

Once deployed, your new Fault Tracking System will be available at:
- **Frontend**: http://your-server:3000
- **Backend API**: http://your-server:8000
- **API Documentation**: http://your-server:8000/docs

The system is now ready for use! 🚀

