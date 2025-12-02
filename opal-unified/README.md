# Fault Tracking System (FATS)

## 🎯 Overview

The Fault Tracking System (FATS) is a modern web application for managing faults, accidents, troubles, and solutions at the Subaru Telescope. It provides a user-friendly interface for tracking, managing, and resolving operational issues.

## ✨ Key Features

### Core Functionality
- **FATS Management** - Create, view, edit, and delete fault entries
- **Advanced Search** - Search by IDNo, description, section, or status
- **Comments System** - Add comments to track resolution progress
- **Image Upload** - Attach multiple images to fault entries
- **Image Viewer** - View images with zoom and navigation
- **Status Tracking** - Track fault status (Active/Canceled)
- **Section Filtering** - Filter faults by section
- **Statistics Dashboard** - View summary statistics

### Modern Features
- **Single Page Application** - Fast, responsive React-based interface
- **RESTful API** - Modern FastAPI backend with async support
- **Real-time Updates** - Live data synchronization
- **Responsive Design** - Works on desktop and mobile devices
- **Production Ready** - Proper logging, error handling, and security
- **Performance Optimized** - Fast loading with optimized queries

## 🏗️ Architecture

### Backend
- **FastAPI** - Modern Python web framework
- **MariaDB** - Database (keeping existing data)
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation and serialization

### Frontend
- **React 18** - Modern UI framework
- **Material-UI (MUI)** - Professional component library
- **Axios** - HTTP client for API communication
- **Tiptap** - Rich text editor for descriptions

### Deployment
- **Virtual Machine** - Direct deployment on VM (recommended)
- **Nginx** - Reverse proxy and static file serving
- **systemd** - Service management for backend
- **Python Virtual Environment** - Isolated Python dependencies

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+** - For backend
- **Node.js 16+** - For frontend development
- **MariaDB/MySQL** - Database server
- **Nginx** - For production deployment (optional for development)

### Development Setup

1. **Backend Setup**:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy and configure environment
cp .env.production.example .env
# Edit .env with your database credentials
# Set DEBUG=true for development

# Create logs directory
mkdir -p logs

# Start backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

2. **Frontend Setup**:
```bash
cd frontend
npm install

# Copy and configure environment
cp .env.production.example .env
# Edit .env with your backend URL (default: http://localhost:8000)

# Start frontend
npm start
```

3. **Access the application**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## 📊 API Endpoints

### FATS Management
- `GET /api/v1/fats/` - List all FATS entries (with pagination, search, filters)
- `GET /api/v1/fats/{id}` - Get single FATS entry by ID
- `GET /api/v1/fats/search/{idno}` - Search by IDNo
- `POST /api/v1/fats/` - Create new FATS entry
- `PUT /api/v1/fats/{id}` - Update FATS entry
- `DELETE /api/v1/fats/{id}` - Delete FATS entry

### Comments
- `POST /api/v1/fats/{id}/comments` - Add comment to FATS entry
- `GET /api/v1/fats/{id}/comments` - Get all comments for FATS entry

### Images
- `POST /api/v1/fats/{id}/images` - Upload single image
- `POST /api/v1/fats/{id}/images/bulk` - Upload multiple images
- `GET /api/v1/fats/{id}/images` - Get all images for FATS entry
- `GET /api/v1/fats/images/{filename}/file` - Get image file
- `DELETE /api/v1/fats/images/{filename}` - Delete image

### Statistics
- `GET /api/v1/fats/stats/summary` - Get FATS statistics summary

### Reference Data
- `GET /api/v1/reference/sections` - Get all sections
- `GET /api/v1/reference/staff` - Get all staff members

### Health Checks
- `GET /health` - Application health check
- `GET /health/db` - Database health check

## 🗄️ Database Schema

### Main Tables
- **`fault`** - Main FATS entries table (legacy table, enhanced)
  - Key fields: `idno`, `issue`, `section`, `section2`, `operator`, `status`, `datein`, `dateout`
  - Status values: `Active`, `Canceled`

### Supporting Tables
- **`fcomments`** - Comments on FATS entries (legacy table)
  - Fields: `faultidno`, `sdescribe`, `operator`, `todo`, `solution`, `date`
- **`fsection`** - Section reference data
- **`fstaff`** - Staff/operator reference data

### Image Storage
- Images are stored in the filesystem at `uploads/fats/`
- Filename pattern: `{fats_id}_{original_filename}.{ext}`
- No database table for images (filesystem-only approach)

## 🔧 Configuration

### Backend Environment Variables

Create `backend/.env` file (use `.env.production.example` as template):

```bash
# Application
DEBUG=false  # Set to true for development
APP_NAME="OPAL Unified System"
APP_VERSION="1.0.0"

# Database
DATABASE_URL=mysql+aiomysql://opal:your_password@localhost:3306/opal
ASYNC_DATABASE_URL=mysql+aiomysql://opal:your_password@localhost:3306/opal

# Security (IMPORTANT: Generate a strong secret key for production)
SECRET_KEY=your-generated-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24

# CORS (comma-separated list of allowed origins)
ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com

# File Upload
UPLOAD_DIR=uploads
FATS_IMAGES_DIR=uploads/fats
MAX_UPLOAD_SIZE=10485760  # 10MB
```

### Frontend Environment Variables

Create `frontend/.env.production` file:

```bash
REACT_APP_API_URL=https://api.your-domain.com
```

For development, create `frontend/.env`:

```bash
REACT_APP_API_URL=http://localhost:8000
```

### Generate Secret Key

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 🚀 Production Deployment

### VM Deployment (Recommended)

For detailed production deployment instructions, see:
- **`PRODUCTION_DEPLOYMENT_CHECKLIST.md`** - Complete production deployment guide
- **`VM_DEPLOYMENT_GUIDE.md`** - Step-by-step VM deployment instructions

### Quick Production Setup

1. **Backend**:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.production.example .env
# Edit .env with production values
mkdir -p logs
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

2. **Frontend**:
```bash
cd frontend
npm install
cp .env.production.example .env.production
# Edit .env.production with production API URL
npm run build
# Serve build/ directory with Nginx
```

3. **Nginx Configuration**:
See `PRODUCTION_DEPLOYMENT_CHECKLIST.md` for complete Nginx configuration.

### Systemd Service

Create `/etc/systemd/system/opal-backend.service`:

```ini
[Unit]
Description=OPAL Unified System Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/opal-unified/backend
Environment="PATH=/path/to/opal-unified/backend/venv/bin"
ExecStart=/path/to/opal-unified/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
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
```

## 🧪 Testing

### Manual Testing
1. **Health Checks**:
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:8000/health/db
   ```

2. **API Testing**:
   ```bash
   # List FATS entries
   curl http://localhost:8000/api/v1/fats/?limit=5
   
   # Get statistics
   curl http://localhost:8000/api/v1/fats/stats/summary
   ```

3. **Frontend Testing**:
   - Open http://localhost:3000
   - Test creating, editing, and viewing FATS entries
   - Test image upload and viewing
   - Test comment functionality

## 📈 Performance

### Optimizations
- **Pagination** - Default limit of 20 entries per request
- **Query Optimization** - Optimized database queries with proper indexing
- **Async Operations** - Async/await for non-blocking I/O
- **Request Timeout** - 25-second timeout for all requests
- **Image Caching** - Efficient image serving from filesystem

### Monitoring
- **Health Checks**: `/health` and `/health/db` endpoints
- **Logging**: Structured logging to `logs/app.log`
- **Request Timing**: `X-Process-Time` header on all responses
- **Error Tracking**: Comprehensive error logging with stack traces

## 🔒 Security

### Implemented Security Features
- **Input Validation** - Pydantic schemas for all API inputs
- **SQL Injection Prevention** - SQLAlchemy ORM with parameterized queries
- **CORS Protection** - Configurable allowed origins
- **Error Handling** - Secure error messages (no sensitive data exposure)
- **Environment Variables** - Sensitive data in `.env` files (not committed)
- **Production Mode** - Debug mode disabled in production
- **Logging** - Comprehensive logging without exposing sensitive data

### Production Security Checklist
- [ ] Strong `SECRET_KEY` generated and set
- [ ] `DEBUG=false` in production
- [ ] CORS origins restricted to production domain(s)
- [ ] Database credentials secured
- [ ] HTTPS/SSL enabled
- [ ] Firewall configured
- [ ] Regular backups scheduled

## 📝 Development

### Code Quality
- **Logging** - Proper logging system (not print statements)
- **Error Handling** - Comprehensive error handling with logging
- **Type Hints** - Python type hints for better code quality
- **Code Organization** - Clean separation of concerns (API, Services, Models)

### Project Structure
```
opal-unified/
├── backend/
│   ├── app/
│   │   ├── api/v1/        # API endpoints
│   │   ├── core/          # Configuration and logging
│   │   ├── db/            # Database session
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   └── services/      # Business logic
│   ├── logs/              # Application logs
│   ├── uploads/fats/     # Image storage
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   └── services/      # API client
│   └── package.json
└── docs/                  # Documentation files
```

## 📚 Documentation

### Available Documentation
- **`PRODUCTION_DEPLOYMENT_CHECKLIST.md`** - Complete production deployment guide
- **`PRODUCTION_READY_SUMMARY.md`** - Summary of production-ready changes
- **`VM_DEPLOYMENT_GUIDE.md`** - Detailed VM deployment instructions
- **`FAULT_MANAGEMENT_SYSTEM_DOCUMENTATION.md`** - Comprehensive system documentation
- **API Documentation** - Available at `/docs` endpoint (Swagger UI)

### Key Features Documentation
- **Image Management** - Filesystem-based image storage
- **Comments System** - Legacy-compatible comment handling
- **Search & Filtering** - Advanced search capabilities
- **Status Management** - Active/Canceled status tracking

## 🔍 Troubleshooting

### Common Issues

1. **Backend not starting**:
   - Check database connection in `.env`
   - Verify virtual environment is activated
   - Check logs in `logs/app.log`

2. **Frontend not connecting to backend**:
   - Verify `REACT_APP_API_URL` in `.env`
   - Check CORS settings in backend
   - Verify backend is running on correct port

3. **Images not loading**:
   - Check `uploads/fats/` directory exists and is writable
   - Verify file permissions
   - Check image filename pattern matches `{fats_id}_*`

4. **Timeout errors**:
   - Check database connection
   - Verify query performance
   - Check logs for slow queries

## 📞 Support

For deployment and configuration help:
- **Production Deployment**: See `PRODUCTION_DEPLOYMENT_CHECKLIST.md`
- **VM Deployment**: See `VM_DEPLOYMENT_GUIDE.md`
- **API Documentation**: http://localhost:8000/docs
- **Health Checks**: http://localhost:8000/health

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ for the Subaru Telescope Observatory**

**Fault Tracking System (FATS) - Production Ready**
