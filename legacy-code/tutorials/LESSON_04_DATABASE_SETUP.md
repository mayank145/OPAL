# LESSON 4: Database Setup with PostgreSQL
## Connecting Your API to a Database

**Estimated Time**: 45-60 minutes  
**Difficulty**: Beginner-Intermediate  
**Prerequisites**: Lessons 1-3 completed

---

## 🎯 Learning Goals

By the end of this lesson, you will:
- Understand what databases are and why we need them
- Install PostgreSQL using Docker
- Connect FastAPI to PostgreSQL
- Use SQLAlchemy ORM (Object-Relational Mapping)
- Create your first database table
- Store and retrieve data from the database

---

## 📚 Background: Why Do We Need a Database?

**Current situation:**
- Your API returns hardcoded data
- When you restart the server, everything resets
- Can't save user data, logs, reservations, etc.

**With a database:**
- 💾 **Persist data** - Data survives server restarts
- 🔍 **Query data** - Find specific records quickly
- 🔐 **Data integrity** - Ensure data is valid and consistent
- 📊 **Relationships** - Connect related data (users, logs, cars)

**Think of it like:**
- Without database = Writing notes on paper, lose them when you close the app
- With database = Filing cabinet that permanently stores organized information

---

## 📝 Step 4.1: Start PostgreSQL with Docker

We'll use Docker to run PostgreSQL (no complicated installation needed!).

**Open a NEW terminal window** (keep your FastAPI server running if it is).

```bash
# Pull PostgreSQL image
docker pull postgres:15-alpine

# Run PostgreSQL container
docker run -d \
  --name opal-postgres \
  -e POSTGRES_USER=opal \
  -e POSTGRES_PASSWORD=opalpassword \
  -e POSTGRES_DB=opal \
  -p 5432:5432 \
  -v opal-postgres-data:/var/lib/postgresql/data \
  postgres:15-alpine
```

**💡 What you're learning:**

Let's break down this command:

- `docker run` = Start a new container
- `-d` = Detached mode (runs in background)
- `--name opal-postgres` = Give it a friendly name
- `-e POSTGRES_USER=opal` = Set username
- `-e POSTGRES_PASSWORD=opalpassword` = Set password
- `-e POSTGRES_DB=opal` = Create database named "opal"
- `-p 5432:5432` = Port mapping (host:container)
  - 5432 is PostgreSQL's default port
- `-v opal-postgres-data:/var/lib/postgresql/data` = Persistent volume
  - Data survives container restarts
- `postgres:15-alpine` = Image to use (Alpine = lightweight)

**🧪 Verify PostgreSQL is running:**

```bash
# Check running containers
docker ps

# Should see:
# CONTAINER ID   IMAGE                NAMES            STATUS
# xxxxx          postgres:15-alpine   opal-postgres    Up X seconds

# Check PostgreSQL logs
docker logs opal-postgres

# Should see: "database system is ready to accept connections"
```

**💡 What you're learning:**
- Docker containers are isolated environments
- PostgreSQL is now running on port 5432
- Data is stored in a Docker volume (persistent)

---

## 📝 Step 4.2: Test Database Connection

Let's verify we can connect to PostgreSQL.

```bash
# Connect to PostgreSQL using docker exec
docker exec -it opal-postgres psql -U opal -d opal

# You should see PostgreSQL prompt:
# opal=#
```

**Try some SQL commands:**

```sql
-- Show current database
SELECT current_database();

-- List all tables (should be empty)
\dt

-- Exit
\q
```

**💡 What you're learning:**
- `psql` is PostgreSQL's command-line tool
- `-U opal` = username
- `-d opal` = database name
- `\dt` = "describe tables" command
- `\q` = quit

**🎉 Success!** Your database is running and accepting connections!

---

## 📝 Step 4.3: Install Database Packages

Now let's add database support to our Python backend.

```bash
# Navigate to backend directory
cd ~/Desktop/opal-v2/backend

# Activate virtual environment
source venv/bin/activate

# Install database packages
pip install sqlalchemy asyncpg psycopg2-binary alembic

# Update requirements.txt
pip freeze > requirements.txt
```

**💡 What you're learning:**

**Packages installed:**
- **sqlalchemy** = ORM (Object-Relational Mapping)
  - Write Python instead of SQL
  - Handle database operations
- **asyncpg** = Async PostgreSQL driver
  - Fast, async database connections
- **psycopg2-binary** = PostgreSQL adapter
  - Fallback driver
- **alembic** = Database migrations
  - Track schema changes over time

**🧪 Verify installation:**

```bash
python -c "import sqlalchemy; print('SQLAlchemy version:', sqlalchemy.__version__)"
```

Should print: `SQLAlchemy version: 2.0.x`

---

## 📝 Step 4.4: Create Database Configuration

Let's configure the database connection.

```bash
# Make sure you're in backend/ directory
cd ~/Desktop/opal-v2/backend

# Create database configuration file
cat > app/core/config.py << 'EOF'
"""
Configuration settings for OPAL API
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings
    Loads from environment variables
    """
    
    # Application
    APP_NAME: str = "OPAL API"
    DEBUG: bool = True
    VERSION: str = "0.1.0"
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://opal:opalpassword@localhost:5432/opal"
    
    # Security (we'll use these later)
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
EOF
```

**💡 What you're learning:**

**Database URL format:**
```
postgresql+asyncpg://username:password@host:port/database
```

Breaking it down:
- `postgresql` = Database type
- `+asyncpg` = Driver to use
- `opal` = Username
- `opalpassword` = Password
- `localhost` = Host (your computer)
- `5432` = Port
- `opal` = Database name

**Pydantic Settings:**
- Automatically loads from `.env` file
- Type validation
- Default values
- Can override with environment variables

---

## 📝 Step 4.5: Create Database Connection

Now let's create the database connection module.

```bash
# Create database session file
cat > app/db/session.py << 'EOF'
"""
Database session management
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    future=True
)

# Create async session factory
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class for models
Base = declarative_base()


# Dependency to get database session
async def get_db():
    """
    Dependency for getting database session
    Automatically closes session after use
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
EOF
```

**💡 What you're learning:**

**Key concepts:**

1. **Engine** = Connection pool to database
   - Manages multiple connections
   - Reuses connections (efficient)

2. **Session** = "Conversation" with database
   - Start transaction
   - Make changes
   - Commit or rollback

3. **Base** = Parent class for all models
   - All database tables inherit from this

4. **get_db()** = Dependency injection
   - FastAPI will call this for each request
   - Automatically handles opening/closing sessions

**Session lifecycle:**
```
Request → get_db() → Open session → Your code → Commit → Close
```

---

## 📝 Step 4.6: Create __init__ Files

Make sure all directories are proper Python packages.

```bash
# Create __init__.py files
touch app/core/__init__.py
touch app/db/__init__.py
touch app/models/__init__.py

# Verify structure
ls -R app/
```

**💡 What you're learning:**
- `__init__.py` makes directories into packages
- Python can import from these directories
- Can be empty or contain initialization code

---

## 📝 Step 4.7: Create Your First Database Model

Let's create a "User" table to store user information.

```bash
# Create user model
cat > app/models/user.py << 'EOF'
"""
User database model
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.session import Base


class User(Base):
    """
    User table
    Stores user account information
    """
    __tablename__ = "users"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # User information
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100))
    
    # Password (we'll hash this later)
    hashed_password = Column(String(255), nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
EOF
```

**💡 What you're learning:**

**SQLAlchemy Model:**
- Python class = Database table
- Class attributes = Table columns
- Inherits from `Base`

**Column types:**
- `Integer` = Whole numbers (1, 2, 3...)
- `String(50)` = Text up to 50 characters
- `Boolean` = True/False
- `DateTime` = Date and time

**Column options:**
- `primary_key=True` = Unique identifier
- `unique=True` = No duplicates
- `index=True` = Faster searches
- `nullable=False` = Required field
- `default=True` = Default value

**Special columns:**
- `server_default=func.now()` = Database sets timestamp on insert
- `onupdate=func.now()` = Database updates timestamp on update

---

## 📝 Step 4.8: Create Database Tables

Now let's actually create the tables in PostgreSQL!

```bash
# Create init_db.py script
cat > app/db/init_db.py << 'EOF'
"""
Initialize database
Creates all tables
"""

import asyncio
from app.db.session import engine, Base
from app.models.user import User  # Import your models here


async def init_db():
    """
    Create all database tables
    """
    async with engine.begin() as conn:
        # Drop all tables (careful in production!)
        await conn.run_sync(Base.metadata.drop_all)
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Database tables created successfully!")


if __name__ == "__main__":
    print("Creating database tables...")
    asyncio.run(init_db())
EOF
```

**Run the script to create tables:**

```bash
# Make sure venv is activated and you're in backend/
python app/db/init_db.py
```

**You should see:**
```
Creating database tables...
✅ Database tables created successfully!
```

**🧪 Verify tables were created:**

```bash
# Connect to PostgreSQL
docker exec -it opal-postgres psql -U opal -d opal

# List tables
\dt

# Should see:
#          List of relations
#  Schema |  Name  | Type  | Owner 
# --------+--------+-------+-------
#  public | users  | table | opal

# Describe users table
\d users

# You'll see all the columns you defined!

# Exit
\q
```

**🎉 Success!** Your first database table exists!

**💡 What you're learning:**
- `Base.metadata.create_all()` creates all tables
- SQLAlchemy reads your models and generates SQL
- One command creates entire database schema
- Tables match your Python models

---

## 📝 Step 4.9: Create Database Schemas (Pydantic Models)

We need Pydantic models for request/response validation.

```bash
# Create user schemas
cat > app/schemas/user.py << 'EOF'
"""
User schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """
    Base user schema with common fields
    """
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """
    Schema for creating a new user
    Includes password
    """
    password: str


class UserUpdate(BaseModel):
    """
    Schema for updating a user
    All fields optional
    """
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    """
    Schema for user response
    What API returns to client
    """
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True  # Allows SQLAlchemy models
EOF
```

**Create __init__.py for schemas:**

```bash
touch app/schemas/__init__.py
```

**💡 What you're learning:**

**Two types of models:**

1. **SQLAlchemy Models** (app/models/)
   - Database tables
   - How data is stored
   
2. **Pydantic Models** (app/schemas/)
   - Request/response validation
   - What API accepts/returns

**Why separate?**
- Database might have hashed_password
- API response shouldn't include password
- Different fields for create vs update

---

## 📝 Step 4.10: Create User API Endpoints

Let's create endpoints to interact with the database!

```bash
# Create user endpoints
cat > app/api/v1/endpoints/users.py << 'EOF'
"""
User API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new user
    """
    # Check if username already exists
    result = await db.execute(
        select(User).where(User.username == user_data.username)
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Check if email already exists
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Create new user
    # TODO: Hash password (we'll do this in a later lesson)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=user_data.password  # Temporarily store plain text
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of all users
    """
    result = await db.execute(
        select(User).offset(skip).limit(limit)
    )
    users = result.scalars().all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific user by ID
    """
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
EOF
```

**💡 What you're learning:**

**Database operations:**

1. **Create** (INSERT):
   ```python
   new_user = User(...)
   db.add(new_user)
   await db.commit()
   ```

2. **Read** (SELECT):
   ```python
   result = await db.execute(select(User))
   users = result.scalars().all()
   ```

3. **Check existence**:
   ```python
   result.scalar_one_or_none()  # Returns user or None
   ```

**FastAPI features:**
- `Depends(get_db)` = Dependency injection (auto get database session)
- `response_model=UserResponse` = Validation for response
- `status_code=201` = HTTP 201 Created
- `HTTPException` = Return error responses

---

## 📝 Step 4.11: Register User Routes

Update main.py to include user routes.

```bash
# Update main.py to include user router
cat > app/main.py << 'EOF'
"""
OPAL API - Main Application
"""

from fastapi import FastAPI
from app.api.v1.endpoints import users

# Create FastAPI application
app = FastAPI(
    title="OPAL API",
    description="Modern Observatory Planning and Logging System",
    version="0.1.0"
)

# Include routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])


@app.get("/")
def read_root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to OPAL API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "OPAL API",
        "database": "connected"
    }
EOF
```

**💡 What you're learning:**
- `app.include_router()` = Add endpoints from another file
- `prefix="/api/v1/users"` = All routes start with this
- `tags=["users"]` = Groups endpoints in documentation

---

## 📝 Step 4.12: Test Your Database API!

**Start the FastAPI server:**

```bash
# Make sure you're in backend/ with venv activated
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Open the API documentation:**
```
http://localhost:8000/docs
```

You should see new **users** section with three endpoints!

---

### Test 1: Create a User

**In Swagger UI (http://localhost:8000/docs):**

1. Click on **POST /api/v1/users/**
2. Click "Try it out"
3. Enter this JSON:
```json
{
  "username": "alice",
  "email": "alice@example.com",
  "full_name": "Alice Johnson",
  "password": "secret123"
}
```
4. Click "Execute"

**You should see:** `201 Created` with the user data returned!

### Test 2: List All Users

1. Click on **GET /api/v1/users/**
2. Click "Try it out"
3. Click "Execute"

**You should see:** Array with your created user!

### Test 3: Get Specific User

1. Click on **GET /api/v1/users/{user_id}**
2. Click "Try it out"
3. Enter user_id: `1`
4. Click "Execute"

**You should see:** The user you created!

---

### Test 4: Verify in Database

```bash
# Connect to PostgreSQL
docker exec -it opal-postgres psql -U opal -d opal

# Query users table
SELECT * FROM users;

# You should see your user!

# Exit
\q
```

**🎉 CONGRATULATIONS!** You just:
- ✅ Created a database table
- ✅ Saved data to the database
- ✅ Retrieved data from the database
- ✅ All through a REST API!

---

## 📝 Step 4.13: Create Multiple Users

Let's add a few more users to test:

**In Swagger UI, create these users:**

```json
{
  "username": "bob",
  "email": "bob@example.com",
  "full_name": "Bob Smith",
  "password": "password123"
}
```

```json
{
  "username": "charlie",
  "email": "charlie@example.com",
  "full_name": "Charlie Brown",
  "password": "mypassword"
}
```

**Then list all users** - you should see 3 users!

---

## 🧪 LESSON 4 CHECKPOINT

Verify everything works:

### Database Running ✅
- [ ] PostgreSQL container running: `docker ps`
- [ ] Can connect to database
- [ ] Tables created: `\dt` shows "users"

### Code Structure ✅
- [ ] `app/core/config.py` exists
- [ ] `app/db/session.py` exists
- [ ] `app/models/user.py` exists
- [ ] `app/schemas/user.py` exists
- [ ] `app/api/v1/endpoints/users.py` exists

### API Working ✅
- [ ] Server starts without errors
- [ ] `/docs` shows user endpoints
- [ ] Can create users (POST)
- [ ] Can list users (GET)
- [ ] Can get specific user (GET with ID)

### Database Integration ✅
- [ ] Users saved in database
- [ ] Can query users in psql
- [ ] Data persists after API restart

**Complete test:**

```bash
# Create user via curl
curl -X POST http://localhost:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","full_name":"Test User","password":"test123"}'

# List users
curl http://localhost:8000/api/v1/users/

# Both should work!
```

---

## 📝 Step 4.14: Stop and Restart Everything

Let's make sure data persists!

```bash
# Stop FastAPI (Ctrl+C in server terminal)

# Stop PostgreSQL
docker stop opal-postgres

# Verify it's stopped
docker ps
```

**Now start everything again:**

```bash
# Start PostgreSQL
docker start opal-postgres

# Start FastAPI
cd ~/Desktop/opal-v2/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Visit http://localhost:8000/api/v1/users/**

**Your users are still there!** ✅ Data persisted!

---

## 📝 Step 4.15: Commit Your Changes

```bash
# Stop the server (Ctrl+C)
cd ~/Desktop/opal-v2

# Check status
git status

# Add files
git add .

# Commit
git commit -m "Add database integration with PostgreSQL

- Setup PostgreSQL with Docker
- Add SQLAlchemy ORM
- Create User model and table
- Add user API endpoints (create, list, get)
- Add Pydantic schemas for validation
- Configure database connection
- All CRUD operations working"

# View history
git log --oneline
```

---

## 🐛 Common Issues and Solutions

### Issue 1: "Connection refused" to PostgreSQL
**Problem:** Can't connect to database

**Solution:**
```bash
# Check if container is running
docker ps

# If not running, start it
docker start opal-postgres

# Check logs
docker logs opal-postgres
```

### Issue 2: "Table already exists"
**Problem:** Running init_db.py twice

**Solution:** The script drops and recreates tables, but if there's an error:
```bash
docker exec -it opal-postgres psql -U opal -d opal
DROP TABLE users;
\q
```

### Issue 3: ImportError
**Problem:** Can't import modules

**Solution:**
```bash
# Make sure all __init__.py files exist
find app -type d -exec touch {}/__init__.py \;

# Reinstall packages
pip install -r requirements.txt
```

### Issue 4: "asyncpg.exceptions.InvalidPasswordError"
**Problem:** Wrong database password

**Solution:** Check your DATABASE_URL in `app/core/config.py` matches the password you used when creating the container.

---

## 📝 Your Learning Journal - Lesson 4

### 1. What I learned:
```
- Databases store data permanently
- SQLAlchemy maps Python classes to tables
- Async database operations
- ...
```

### 2. Database concepts:
```
- Tables = collections of records
- Columns = fields in a record
- Primary key = unique identifier
- Foreign key = relationship to another table (coming later)
```

### 3. Commands I used:
```bash
docker run postgres         # Start database
docker exec -it psql       # Connect to database
python app/db/init_db.py   # Create tables
```

---

## 🎓 Key Concepts Learned

### Database Basics
- **PostgreSQL** = Relational database
- **Docker** = Easy way to run databases
- **Tables** = Store data in rows and columns
- **Persistence** = Data survives restarts

### SQLAlchemy ORM
- **Model** = Python class → Database table
- **Session** = Conversation with database
- **Query** = Retrieve data
- **ORM** = Object-Relational Mapping (Python objects ↔ Database rows)

### FastAPI + Database
- **Dependency injection** = `Depends(get_db)`
- **Async operations** = Non-blocking database calls
- **Auto commit/rollback** = Handle transactions automatically

---

## 🚀 What's Next?

In **Lesson 5**, you'll:
- Implement full CRUD operations (Create, Read, Update, Delete)
- Add password hashing for security
- Create relationships between tables
- Build more complex queries
- Add error handling

**Estimated Time**: 45-60 minutes

---

## ✅ Ready for Lesson 5?

Before continuing:
- ✅ PostgreSQL running in Docker
- ✅ Can create/read users from database
- ✅ Understand SQLAlchemy models
- ✅ Understand Pydantic schemas
- ✅ API documentation shows user endpoints
- ✅ Changes committed to Git

**When you're ready, tell me: "I finished Lesson 4"!**

---

## 💡 Extra Practice (Optional)

### Challenge 1: Add More User Fields

Add these fields to the User model:
```python
phone_number = Column(String(20))
department = Column(String(50))
```

Then run `init_db.py` again to recreate tables.

### Challenge 2: Query by Username

Add this endpoint to `users.py`:
```python
@router.get("/username/{username}", response_model=UserResponse)
async def get_user_by_username(
    username: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Challenge 3: Count Users

Add this endpoint:
```python
from sqlalchemy import func

@router.get("/stats/count")
async def count_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(func.count(User.id)))
    count = result.scalar()
    return {"total_users": count}
```

Try building these yourself! 🧪

---

**Congratulations on completing Lesson 4!** 

**You now have a database-powered API!** This is professional-grade development! 🎉

---

**Next**: Tell me "I finished Lesson 4" for Lesson 5: Full CRUD Operations

**Document Version**: 1.0  
**Last Updated**: October 8, 2025

