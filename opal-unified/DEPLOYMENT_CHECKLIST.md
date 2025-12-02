# Deployment Checklist for Virtual Machine

## Pre-Deployment Cleanup ✅

All unnecessary files have been removed:
- ✅ Temporary documentation files
- ✅ Migration scripts (migration complete)
- ✅ Test scripts and test directories
- ✅ Temporary shell scripts
- ✅ Windows batch files
- ✅ Postman collections
- ✅ Python virtual environment (will be recreated)
- ✅ Node modules (will be reinstalled)
- ✅ Build directory (will be rebuilt)

## Files Structure

```
opal-unified/
├── backend/
│   ├── app/                    # Core application code
│   │   ├── api/               # API endpoints
│   │   ├── core/              # Configuration
│   │   ├── db/                # Database session
│   │   ├── models/            # Database models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   └── main.py            # FastAPI app
│   ├── uploads/
│   │   └── fats/              # Image files (181 files)
│   ├── Dockerfile
│   ├── env.example            # Environment template
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/                   # React source code
│   │   ├── components/        # React components
│   │   ├── services/          # API service
│   │   └── App.js            # Main app
│   ├── public/
│   │   └── index.html
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json          # Node dependencies
│   └── package-lock.json
├── deployment/
│   ├── nginx/                # Nginx configuration
│   └── init-scripts/         # Database init scripts (optional)
├── FAULT_MANAGEMENT_SYSTEM_DOCUMENTATION.md
├── HOSTING_GUIDE.md
├── README.md
└── .deploymentignore         # Files to exclude when deploying
```

## Deployment Steps

### 1. Transfer Files to VM
```bash
# Using SCP
scp -r opal-unified/ user@vm-ip:/path/to/destination/

# Or using rsync (excludes node_modules, venv, etc.)
rsync -av --exclude-from=.deploymentignore opal-unified/ user@vm-ip:/path/to/destination/
```

### 2. Backend Setup
```bash
cd opal-unified/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
cp env.example .env
# Edit .env with your database credentials

# Ensure uploads directory exists
mkdir -p uploads/fats
chmod 755 uploads/fats
```

### 3. Frontend Setup
```bash
cd opal-unified/frontend

# Install dependencies
npm install

# Build for production
npm run build

# Or use development mode
npm start
```

### 4. Database Setup
- Ensure MariaDB is running
- Database should already exist with tables:
  - `fault`
  - `fcomments`
  - `fsection`
  - `fstaff`
- Update database credentials in `.env`

### 5. Start Services

#### Backend (Development)
```bash
cd opal-unified/backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Backend (Production with systemd)
Create `/etc/systemd/system/opal-backend.service`:
```ini
[Unit]
Description=OPAL FATS Backend API
After=network.target

[Service]
User=your-user
WorkingDirectory=/path/to/opal-unified/backend
Environment="PATH=/path/to/opal-unified/backend/venv/bin"
ExecStart=/path/to/opal-unified/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable opal-backend
sudo systemctl start opal-backend
```

#### Frontend (Production Build)
```bash
cd opal-unified/frontend
npm install
npm run build
```

#### Frontend (Serve with Nginx)
Configure Nginx to serve the `frontend/build` directory and proxy API requests to backend on port 8000.

### 6. Verify Deployment
- Backend health: `http://vm-ip:8000/health`
- Frontend: `http://vm-ip:3000` (dev) or `http://vm-ip` (production)
- API docs: `http://vm-ip:8000/docs`

## Important Notes

### Image Files
- 181 image files in `backend/uploads/fats/`
- Total size: ~60MB
- Files follow pattern: `{fats_id}_{original_filename}.{ext}`
- Ensure proper file permissions: `chmod 644 uploads/fats/*`

### Environment Variables
Required in `backend/.env`:
```
DATABASE_URL=mysql+aiomysql://user:password@host:3306/opal
UPLOAD_DIR=uploads
FATS_IMAGES_DIR=uploads/fats
MAX_UPLOAD_SIZE=10485760
DEBUG=False
```

### Frontend Environment
Create `frontend/.env`:
```
REACT_APP_API_URL=http://vm-ip:8000
```

### File Permissions
```bash
# Backend uploads directory
chmod 755 backend/uploads
chmod 755 backend/uploads/fats
chmod 644 backend/uploads/fats/*

# Python files
chmod 644 backend/app/**/*.py

# Frontend build
chmod 755 frontend/build
```

## Size Information
- Total project size: ~61MB
- Backend: ~60MB (includes 181 images)
- Frontend: ~840KB (source code only, before npm install)

## What Was Removed
- ✅ 70+ temporary documentation files
- ✅ Migration scripts (already completed)
- ✅ Test scripts and directories
- ✅ Python virtual environment (recreate on server)
- ✅ Node modules (reinstall on server)
- ✅ Build directory (rebuild on server)
- ✅ Temporary shell scripts
- ✅ Windows batch files
- ✅ Postman collections

## What Was Kept
- ✅ Core application code
- ✅ Configuration files
- ✅ Nginx configuration (for production)
- ✅ Essential documentation (4 files)
- ✅ Image files (181 files)
- ✅ Database init scripts (optional)

## Next Steps
1. Transfer files to VM
2. Set up environment variables
3. Install dependencies
4. Start services
5. Verify functionality

---

**Ready for deployment!** 🚀

