# Fault Management System (FATS) - Complete Documentation

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Core Features](#core-features)
5. [Database Schema](#database-schema)
6. [API Endpoints](#api-endpoints)
7. [Image Management](#image-management)
8. [Frontend Components](#frontend-components)
9. [Deployment](#deployment)
10. [Migration from Legacy System](#migration-from-legacy-system)

---

## Overview

The Fault Management System (FATS) is a modern web-based application designed to track, manage, and resolve faults/issues at the Subaru Telescope. It replaces the legacy CGI-based system with a modern, responsive interface built using React and FastAPI.

### Key Objectives
- **Fault Tracking**: Record and track faults from creation to resolution
- **Image Management**: Attach images to fault entries for documentation
- **Comment System**: Add comments, todos, and solutions to fault entries
- **Search & Filter**: Quickly find faults by ID, section, status, or keywords
- **User-Friendly Interface**: Modern, responsive UI for better user experience

---

## System Architecture

### High-Level Architecture

```
┌─────────────────┐
│   React Frontend │  (Port 3000)
│   - FATSList     │
│   - FATSDetail   │
│   - CommentDialog│
└────────┬─────────┘
         │ HTTP/REST API
         │
┌────────▼─────────┐
│  FastAPI Backend  │  (Port 8000)
│  - REST Endpoints │
│  - Business Logic │
│  - Data Validation│
└────────┬─────────┘
         │
┌────────▼─────────┐
│   MariaDB        │  (Port 3306)
│   - fault table  │
│   - fcomments    │
│   - fsection     │
│   - fstaff       │
└──────────────────┘
         │
┌────────▼─────────┐
│  Filesystem      │
│  - uploads/fats/ │
│  - Image storage │
└──────────────────┘
```

### Component Flow

1. **Frontend (React)**
   - User interacts with React components
   - Components make API calls via Axios
   - State management using React hooks

2. **Backend (FastAPI)**
   - Receives HTTP requests
   - Validates data using Pydantic schemas
   - Processes business logic via service layer
   - Queries database using SQLAlchemy ORM
   - Returns JSON responses

3. **Database (MariaDB)**
   - Stores fault entries, comments, and reference data
   - Uses existing legacy table structure for compatibility

4. **Filesystem**
   - Stores images in `uploads/fats/` directory
   - Uses legacy naming pattern: `{fats_id}_{original_filename}.{ext}`

---

## Technology Stack

### Frontend
- **React 18**: UI framework
- **Material-UI (MUI)**: Component library
- **Tiptap**: Rich text editor for descriptions
- **Axios**: HTTP client for API calls
- **React Router**: Navigation (if needed)

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server
- **aiomysql**: Async MySQL/MariaDB driver

### Database
- **MariaDB**: Relational database
- **Legacy Tables**: 
  - `fault` - Main fault entries
  - `fcomments` - Comments on faults
  - `fsection` - Section reference data
  - `fstaff` - Staff reference data

### Development Tools
- **Python 3.9+**: Backend runtime
- **Node.js 16+**: Frontend build tool
- **Docker** (optional): Containerization
- **Git**: Version control

---

## Core Features

### 1. Fault Entry Management

#### Create New Fault
- **Fields**:
  - Issue (text)
  - Issue Describe (rich text editor)
  - Solution (text)
  - Solution Describe (rich text editor)
  - Section & Section2 (dropdowns)
  - Operator (dropdown)
  - Status (Active/Canceled)
  - Assigned To (dropdown)
  - To Do (text)
- **Validation**: Required fields validated before submission
- **Confirmation**: Popup confirmation before creating

#### View/Edit Fault
- View all fault details in a dialog
- Edit mode allows modification of all fields
- Rich text editing for descriptions
- Real-time validation

#### Delete Blank Faults
- Automatic detection of blank entries (all N/A or empty)
- Bulk deletion capability
- Safety checks before deletion

### 2. Search & Filter

#### Search by ID
- Direct ID search shows exact match first
- Then displays other entries sorted by date

#### Filter Options
- **By Section**: Filter faults by section
- **By Status**: Active or Canceled
- **By Keywords**: Search in issue field
- **Combined Filters**: Multiple filters can be applied simultaneously

#### Pagination
- Default limit: 20 entries per page
- Skip parameter for pagination
- Maximum skip capped at 500 for performance

### 3. Comment System

#### Add Comments
- **Fields**:
  - Description (rich text)
  - To Do (optional)
  - Solution (optional)
  - Operator (auto-filled or manual)
- **Timestamps**: Automatic date/time tracking
- **Linked to Fault**: Comments are associated with fault ID

#### View Comments
- Display all comments for a fault entry
- Chronological ordering
- Shows operator, date, and content

### 4. Image Management

#### Upload Images
- **Multiple Upload**: Select and upload multiple images at once
- **Supported Formats**: JPEG, PNG, GIF, WebP
- **File Size Limit**: 10MB per image
- **Validation**: File type and size validation before upload

#### Image Storage
- **Location**: `uploads/fats/` directory
- **Naming Pattern**: `{fats_id}_{original_filename}.{ext}`
- **Filesystem-Only**: No database table, uses filesystem scanning
- **Fast Retrieval**: Uses `glob` pattern matching for quick lookup

#### Image Display
- **Thumbnail Grid**: Images displayed in 3-column grid
- **Full-Size Preview**: Click to view full-size image
- **Navigation**: Previous/Next buttons to browse multiple images
- **Zoom Functionality**: 
  - Zoom in/out buttons
  - Double-click to zoom
  - Mouse wheel zoom (Ctrl/Cmd + scroll)
  - Pan when zoomed in
- **Delete**: Remove images from fault entries

### 5. Reference Data

#### Sections
- Loaded from `fsection` table
- Used in dropdown filters and form fields
- Distinct values for performance

#### Staff/Operators
- Loaded from `fstaff` table
- Used in operator and assigned_to fields
- Distinct values for performance

---

## Database Schema

### fault Table (Main Fault Entries)

```sql
CREATE TABLE fault (
    idno INT PRIMARY KEY AUTO_INCREMENT,
    issue VARCHAR(500),
    idescribe TEXT,
    solution VARCHAR(500),
    sdescribe TEXT,
    todo VARCHAR(80),
    section VARCHAR(100),
    section2 VARCHAR(30),
    operator VARCHAR(20),
    datein DATETIME,
    status VARCHAR(20) DEFAULT 'Active',
    assigned_to VARCHAR(100),
    created_by VARCHAR(100),
    resolved_at DATETIME,
    updated_at DATETIME,
    views INT DEFAULT 0,
    likes INT DEFAULT 0,
    dislikes INT DEFAULT 0,
    is_blank BOOLEAN DEFAULT FALSE
);
```

**Key Fields:**
- `idno`: Primary key, auto-incrementing
- `status`: 'Active' or 'Canceled'
- `datein`: Creation timestamp
- `idescribe` / `sdescribe`: Rich text descriptions

### fcomments Table (Comments)

```sql
CREATE TABLE fcomments (
    idno INT PRIMARY KEY AUTO_INCREMENT,
    faultidno INT,
    sdescribe TEXT,
    todo VARCHAR(80),
    solution VARCHAR(500),
    operator VARCHAR(20),
    datein DATETIME
);
```

**Key Fields:**
- `faultidno`: Foreign key to `fault.idno`
- `sdescribe`: Comment description
- `datein`: Comment timestamp

### Reference Tables

#### fsection
- Stores section names and codes
- Used for filtering and form dropdowns

#### fstaff
- Stores staff/operator names
- Used for operator and assigned_to fields

---

## API Endpoints

### Base URL
```
http://localhost:8000/api/v1/fats
```

### Endpoints

#### 1. List Faults
```
GET /api/v1/fats/
Query Parameters:
  - skip: int (default: 0)
  - limit: int (default: 20, max: 100)
  - search: string (optional)
  - section: string (optional)
  - status: string (optional)
Response: List[FATSEntryResponse]
```

#### 2. Get Fault by ID
```
GET /api/v1/fats/{fats_id}
Response: FATSEntryResponse
```

#### 3. Search Fault by ID
```
GET /api/v1/fats/search/{idno}
Response: List[FATSEntryResponse] (exact match first)
```

#### 4. Create Fault
```
POST /api/v1/fats/
Body: FATSEntryCreate
Response: FATSEntryResponse
```

#### 5. Update Fault
```
PUT /api/v1/fats/{fats_id}
Body: FATSEntryUpdate
Response: FATSEntryResponse
```

#### 6. Delete Blank Faults
```
DELETE /api/v1/fats/blank
Response: {"deleted_count": int}
```

#### 7. Get Fault Statistics
```
GET /api/v1/fats/stats/summary
Response: {
  "total": int,
  "active": int,
  "canceled": int,
  "by_section": dict
}
```

#### 8. Get Images for Fault
```
GET /api/v1/fats/{fats_id}/images
Response: List[ImageInfo]
```

#### 9. Upload Image(s)
```
POST /api/v1/fats/{fats_id}/images
POST /api/v1/fats/{fats_id}/images/bulk
Body: multipart/form-data (file/files)
Response: List[ImageInfo]
```

#### 10. Get Image File
```
GET /api/v1/fats/images/{filename}/file
Response: File (image/jpeg, image/png, etc.)
```

#### 11. Delete Image
```
DELETE /api/v1/fats/images/{filename}
Response: 204 No Content
```

#### 12. Get Comments
```
GET /api/v1/fats/{fats_id}/comments
Response: List[FATSCommentResponse]
```

#### 13. Add Comment
```
POST /api/v1/fats/{fats_id}/comments
Body: FATSCommentCreate
Response: FATSCommentResponse
```

### Reference Data Endpoints

#### Get Sections
```
GET /api/v1/reference/sections
Response: List[SectionInfo]
```

#### Get Staff
```
GET /api/v1/reference/staff
Response: List[StaffInfo]
```

---

## Image Management

### Storage Strategy

The system uses a **filesystem-only approach** for image storage, following Unix philosophy where "the directory structure is a database."

#### File Naming Pattern
```
{fats_id}_{original_filename}.{ext}
```

**Examples:**
- `2633_9M133_Kornet_AT-14.jpg`
- `2633_Picture 5.jpg`
- `4764_Screenshot 2025-10-07 at 9.52.07 AM.png`

#### Directory Structure
```
uploads/
└── fats/
    ├── 2633_9M133_Kornet_AT-14.jpg
    ├── 2633_NewAO188MainGUI.jpg
    ├── 2633_Picture 5.jpg
    ├── 4764_Screenshot.png
    └── ...
```

### Image Retrieval

#### Filesystem Scanning
```python
# Pattern matching using glob
pattern = f"{fats_images_dir}/{fats_id}_*"
image_files = glob.glob(pattern)
```

**Performance:**
- Fast directory operations (~3ms for 177 files)
- No database overhead
- Direct file access

#### Image Metadata
- File size: Retrieved from filesystem `stat()`
- MIME type: Guessed from file extension
- Upload date: File modification time
- Filename: Original filename preserved in pattern

### Image Service Methods

```python
class ImageService:
    def get_images_for_fats(fats_id: int) -> List[Dict]
    def upload_image(fats_id: int, file: UploadFile) -> Dict
    def upload_multiple_images(fats_id: int, files: List[UploadFile]) -> List[Dict]
    def delete_image(filename: str) -> bool
    def get_image_file_path(filename: str) -> Path
    def get_image_url(filename: str) -> str
```

### Image Validation

- **File Types**: JPEG, PNG, GIF, WebP
- **File Size**: Maximum 10MB per image
- **Minimum Size**: 100 bytes (prevents empty files)
- **Content Type**: Validated from file headers

---

## Frontend Components

### FATSList Component

**Location**: `frontend/src/components/FATSList.js`

**Features:**
- Displays list of fault entries in a table
- Search bar for keyword search
- Filter dropdowns (Section, Status)
- Pagination controls
- Click to view/edit fault details
- "Create New FATS" button

**State Management:**
- `fats`: List of fault entries
- `sections`: Available sections for filter
- `loading`: Loading state
- `error`: Error messages
- `searchTerm`, `sectionFilter`, `statusFilter`: Filter states

### FATSDetail Component

**Location**: `frontend/src/components/FATSDetail.js`

**Features:**
- View/Edit/Create fault dialog
- Rich text editors for descriptions
- Image upload and display
- Comment section
- Form validation
- Save/Cancel actions

**Modes:**
- `view`: Read-only mode
- `edit`: Edit existing fault
- `create`: Create new fault

**Image Features:**
- Thumbnail grid display
- Full-size preview modal
- Navigation between images
- Zoom and pan functionality
- Delete images

### CommentDialog Component

**Location**: `frontend/src/components/CommentDialog.js`

**Features:**
- Add new comments
- Display existing comments
- Rich text editor for comment description
- Optional todo and solution fields
- Operator selection

### API Service

**Location**: `frontend/src/services/api.js`

**Functions:**
- `fatsAPI.getAll()`: Get all faults with filters
- `fatsAPI.getById()`: Get single fault
- `fatsAPI.create()`: Create new fault
- `fatsAPI.update()`: Update fault
- `fatsAPI.getImages()`: Get images for fault
- `fatsAPI.uploadImages()`: Upload multiple images
- `fatsAPI.deleteImage()`: Delete image
- `fatsAPI.getComments()`: Get comments
- `fatsAPI.addComment()`: Add comment
- `referenceAPI.getSections()`: Get sections
- `referenceAPI.getStaff()`: Get staff

---

## Deployment

### Development Setup

#### Backend
```bash
cd opal-unified/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd opal-unified/frontend
npm install
npm start
```

### Production Deployment

#### Using Docker
```bash
docker-compose up -d
```

#### Manual Deployment
1. Build frontend: `npm run build`
2. Serve static files via Nginx
3. Run backend with Gunicorn/Uvicorn
4. Configure reverse proxy

### Environment Variables

**Backend (.env)**
```
DATABASE_URL=mysql+aiomysql://user:pass@host:3306/opal
UPLOAD_DIR=uploads
FATS_IMAGES_DIR=uploads/fats
MAX_UPLOAD_SIZE=10485760
DEBUG=False
```

**Frontend (.env)**
```
REACT_APP_API_URL=http://localhost:8000
```

---

## Migration from Legacy System

### Legacy System Architecture

- **CGI Scripts**: Perl/Python scripts
- **Apache Web Server**: Serves static files and executes CGI
- **Direct MySQL**: No ORM, direct SQL queries
- **File Storage**: Images in `/var/www/html/fats/pix/`
- **Naming Pattern**: `{idno}_{filename}` (first 4 digits of ID)

### Migration Process

#### 1. Database Migration
- Legacy tables preserved (`fault`, `fcomments`)
- No schema changes required
- Direct compatibility with existing data

#### 2. Image Migration
- Copied images from legacy `pix/` directory
- Renamed to match new pattern: `{fats_id}_{original_filename}`
- Filesystem-only storage (no database table)

#### 3. Data Compatibility
- All existing fault entries accessible
- Comments preserved
- Reference data maintained

### Migration Scripts

**Location**: `backend/scripts/`

- `migrate_legacy_images_standalone.py`: Migrate images from legacy system
- `rename_images_to_legacy_pattern.py`: Rename UUID files to legacy pattern
- `check_fats_images.py`: Verify image migration

---

## Performance Optimizations

### Backend
- **Query Limits**: Default 20 entries, max 100
- **Pagination**: Skip capped at 500
- **Connection Pooling**: SQLAlchemy pool size 10
- **Async Operations**: All database operations are async
- **Timeout Middleware**: 25-second request timeout

### Frontend
- **Lazy Loading**: Images loaded on demand
- **Pagination**: Load 20 entries at a time
- **Debounced Search**: Search input debounced
- **Image Optimization**: Thumbnails for grid, full-size on click

### Filesystem
- **Fast Scanning**: `glob` pattern matching (~3ms for 177 files)
- **Direct File Access**: No database overhead
- **Efficient Lookup**: Pattern `{fats_id}_*` for quick filtering

---

## Security Considerations

### Input Validation
- Pydantic schemas validate all inputs
- File type validation for uploads
- File size limits enforced
- SQL injection prevention via ORM

### File Upload Security
- File type whitelist (JPEG, PNG, GIF, WebP)
- File size limits (10MB max)
- Filename sanitization
- Path traversal prevention

### CORS Configuration
- Allowed origins configured
- Credentials support
- Method and header restrictions

---

## Future Enhancements

### Planned Features
1. **User Authentication**: JWT-based authentication
2. **Role-Based Access**: Different permissions for different roles
3. **Email Notifications**: Notify on fault creation/updates
4. **Advanced Search**: Full-text search across all fields
5. **Export Functionality**: Export faults to CSV/PDF
6. **Dashboard**: Statistics and charts
7. **Mobile App**: Native mobile application

### Technical Improvements
1. **Caching**: Redis for frequently accessed data
2. **CDN**: Image serving via CDN
3. **Database Indexing**: Additional indexes for performance
4. **API Versioning**: Versioned API endpoints
5. **Documentation**: OpenAPI/Swagger documentation

---

## Troubleshooting

### Common Issues

#### Backend Not Responding
- Check if port 8000 is in use
- Verify database connection
- Check backend logs for errors

#### Images Not Loading
- Verify files exist in `uploads/fats/`
- Check filename pattern matches `{fats_id}_*`
- Verify file permissions

#### Timeout Errors
- Check database connection pool
- Verify query performance
- Increase timeout if needed

#### Frontend Not Loading
- Check if backend is running
- Verify API URL in `.env`
- Check browser console for errors

---

## Support & Maintenance

### Logging
- Backend logs: Console output
- Frontend logs: Browser console
- Error tracking: Exception handlers

### Monitoring
- Health check endpoint: `/health`
- Database health: `/health/db`
- Request timing: X-Process-Time header

### Backup
- Database: Regular MySQL dumps
- Images: Backup `uploads/fats/` directory
- Configuration: Version control (Git)

---

## Conclusion

The Fault Management System provides a modern, efficient solution for tracking and managing faults at the Subaru Telescope. It maintains compatibility with the legacy system while offering improved usability, performance, and maintainability.

The filesystem-only approach for images leverages Unix filesystem efficiency, providing fast operations without database overhead. The system is designed to scale and can be extended with additional features as needed.

---

**Document Version**: 1.0  
**Last Updated**: December 2024  
**Maintained By**: OPAL Development Team

