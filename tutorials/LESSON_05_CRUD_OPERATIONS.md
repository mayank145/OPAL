# LESSON 5: Full CRUD Operations & Security
## Complete Database Operations with Password Hashing

**Estimated Time**: 45-60 minutes  
**Difficulty**: Intermediate  
**Prerequisites**: Lessons 1-4 completed

---

## 🎯 Learning Goals

By the end of this lesson, you will:
- Implement UPDATE operations (modify existing data)
- Implement DELETE operations (remove data)
- Hash passwords securely with bcrypt
- Add better error handling
- Implement pagination and filtering
- Understand complete CRUD operations
- Follow security best practices

---

## 📚 Background: What is CRUD?

**CRUD** = The four basic database operations

1. ✅ **C**reate - Add new records (Done in Lesson 4)
2. ✅ **R**ead - Retrieve records (Done in Lesson 4)
3. 🆕 **U**pdate - Modify existing records (Today!)
4. 🆕 **D**elete - Remove records (Today!)

**Why CRUD matters:**
- These are the foundation of ALL database applications
- Every app you use does CRUD (Facebook, Gmail, etc.)
- Master CRUD = Master database operations

**Security note:**
- NEVER store passwords in plain text
- Always hash passwords before storing
- Use proven algorithms (bcrypt)

---

## 📝 Step 5.1: Add Password Hashing Utilities

Let's create utilities for secure password handling.

```bash
# Make sure you're in backend/ with venv activated
cd ~/Desktop/opal-v2/backend
source venv/bin/activate  # or source .venv/bin/activate

# Create security utilities file
cat > app/core/security.py << 'EOF'
"""
Security utilities
Password hashing and verification
"""

from passlib.context import CryptContext

# Create password context for bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Stored hashed password
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


# Example usage (for testing)
if __name__ == "__main__":
    # Test hashing
    password = "mysecretpassword"
    hashed = hash_password(password)
    
    print(f"Original: {password}")
    print(f"Hashed: {hashed}")
    print(f"Verify correct: {verify_password(password, hashed)}")
    print(f"Verify wrong: {verify_password('wrongpassword', hashed)}")
EOF
```

**💡 What you're learning:**

**Password hashing:**
- **Plain text** = "password123" (NEVER store this!)
- **Hashed** = "$2b$12$KIX..." (Stored in database)
- **One-way** = Can't reverse the hash to get password
- **Bcrypt** = Industry-standard algorithm

**How it works:**
1. User enters password
2. Hash it with bcrypt
3. Store hash in database
4. To verify: Hash entered password, compare hashes

**🧪 Test the security utilities:**

```bash
python app/core/security.py
```

You should see:
```
Original: mysecretpassword
Hashed: $2b$12$... (long string)
Verify correct: True
Verify wrong: False
```

---

## 📝 Step 5.2: Create User Service Layer

Let's create a service layer for user operations (better organization).

```bash
# Create user service
cat > app/services/user.py << 'EOF'
"""
User service
Business logic for user operations
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List, Optional

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password


async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    """
    Create a new user with hashed password
    """
    # Hash the password
    hashed_password = hash_password(user_data.password)
    
    # Create user object
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    """
    Get user by ID
    """
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """
    Get user by username
    """
    result = await db.execute(
        select(User).where(User.username == username)
    )
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """
    Get user by email
    """
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()


async def get_users(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> List[User]:
    """
    Get list of users with pagination
    """
    result = await db.execute(
        select(User)
        .offset(skip)
        .limit(limit)
        .order_by(User.created_at.desc())
    )
    return result.scalars().all()


async def update_user(
    db: AsyncSession,
    user_id: int,
    user_data: UserUpdate
) -> Optional[User]:
    """
    Update user information
    """
    # Get existing user
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    
    # Update only provided fields
    update_data = user_data.dict(exclude_unset=True)
    
    # Hash password if provided
    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))
    
    # Update user attributes
    for field, value in update_data.items():
        setattr(user, field, value)
    
    await db.commit()
    await db.refresh(user)
    
    return user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    """
    Delete user
    Returns True if deleted, False if not found
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        return False
    
    await db.delete(user)
    await db.commit()
    
    return True


async def deactivate_user(db: AsyncSession, user_id: int) -> Optional[User]:
    """
    Soft delete: Deactivate user instead of deleting
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    
    user.is_active = False
    await db.commit()
    await db.refresh(user)
    
    return user
EOF
```

**Create services __init__.py:**
```bash
touch app/services/__init__.py
```

**💡 What you're learning:**

**Service Layer Pattern:**
- **Controllers** (endpoints) = Handle HTTP requests
- **Services** (this file) = Business logic
- **Models** = Database structure

**Benefits:**
- ✅ Reusable code (can call from multiple endpoints)
- ✅ Easier to test
- ✅ Cleaner separation of concerns
- ✅ Can change implementation without changing API

**Soft delete vs Hard delete:**
- **Hard delete** = Remove from database (gone forever)
- **Soft delete** = Mark as inactive (can recover)
- Use soft delete for user accounts (safety!)

---

## 📝 Step 5.3: Update User Endpoints

Now let's update the endpoints to use the service layer and add UPDATE/DELETE operations.

```bash
# Update user endpoints
cat > app/api/v1/endpoints/users.py << 'EOF'
"""
User API endpoints
Complete CRUD operations
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services import user as user_service

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new user
    
    - **username**: Unique username (3-50 characters)
    - **email**: Valid email address
    - **password**: Password (will be hashed)
    - **full_name**: Full name (optional)
    """
    # Check if username exists
    existing_user = await user_service.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email exists
    existing_email = await user_service.get_user_by_email(db, user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = await user_service.create_user(db, user_data)
    return user


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Max number of records to return"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of all users with pagination
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return (1-100)
    """
    users = await user_service.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific user by ID
    """
    user = await user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update user information
    
    All fields are optional - only provided fields will be updated
    """
    user = await user_service.update_user(db, user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a user (hard delete - removes from database)
    
    ⚠️ WARNING: This permanently deletes the user!
    """
    deleted = await user_service.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return None


@router.post("/{user_id}/deactivate", response_model=UserResponse)
async def deactivate_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Deactivate a user (soft delete - keeps in database but marks inactive)
    
    This is safer than deletion as it can be reversed
    """
    user = await user_service.deactivate_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user


@router.get("/username/{username}", response_model=UserResponse)
async def get_user_by_username(
    username: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get user by username
    """
    user = await user_service.get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username '{username}' not found"
        )
    return user
EOF
```

**💡 What you're learning:**

**HTTP Status Codes:**
- `200 OK` = Success (GET, PUT)
- `201 Created` = Resource created (POST)
- `204 No Content` = Success, no body returned (DELETE)
- `400 Bad Request` = Invalid input
- `404 Not Found` = Resource doesn't exist

**REST Conventions:**
- `GET /users` = List all
- `GET /users/{id}` = Get specific
- `POST /users` = Create new
- `PUT /users/{id}` = Update existing
- `DELETE /users/{id}` = Delete

**Query Parameters:**
- `Query(0, ge=0)` = Default 0, must be >= 0
- `Query(100, ge=1, le=100)` = Default 100, between 1-100
- Used for pagination, filtering

---

## 📝 Step 5.4: Test Your API!

**Start the server:**

```bash
# Make sure PostgreSQL is running
docker start opal-postgres

# Start FastAPI
cd ~/Desktop/opal-v2/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Open API documentation:**
```
http://localhost:8000/docs
```

You should now see MORE endpoints!

---

### Test 1: Create User with Hashed Password

**In Swagger UI:**

1. Go to **POST /api/v1/users/**
2. Try it out with:
```json
{
  "username": "john",
  "email": "john@example.com",
  "full_name": "John Doe",
  "password": "secret123"
}
```

3. Check the response - password is NOT shown! ✅
4. Check database:
```bash
docker exec -it opal-postgres psql -U opal -d opal
SELECT username, hashed_password FROM users WHERE username='john';
\q
```

The password is hashed! 🔒

---

### Test 2: Update User

1. Go to **PUT /api/v1/users/{user_id}**
2. Enter user_id: `1` (or the ID of a user you created)
3. Try it out with:
```json
{
  "full_name": "John Smith"
}
```

4. Check response - name is updated!
5. Try updating password:
```json
{
  "password": "newsecret456"
}
```

Password is hashed automatically! ✅

---

### Test 3: Get User by Username

1. Go to **GET /api/v1/users/username/{username}**
2. Enter username: `john`
3. Execute

You get the user! ✅

---

### Test 4: Pagination

1. Create a few more users first
2. Go to **GET /api/v1/users/**
3. Try with parameters:
   - `skip=0, limit=2` (first 2 users)
   - `skip=2, limit=2` (next 2 users)

Pagination works! ✅

---

### Test 5: Soft Delete (Deactivate)

1. Go to **POST /api/v1/users/{user_id}/deactivate**
2. Enter a user_id
3. Execute

User is deactivated (is_active = false) ✅

---

### Test 6: Hard Delete

1. Create a test user
2. Go to **DELETE /api/v1/users/{user_id}**
3. Enter the test user's ID
4. Execute

Returns 204 No Content - user is deleted! ✅

---

## 📝 Step 5.5: Add Active Users Filter

Let's add an endpoint to get only active users.

```bash
# Add to the END of app/api/v1/endpoints/users.py (before EOF)
cat >> app/api/v1/endpoints/users.py << 'EOF'


@router.get("/active/list", response_model=List[UserResponse])
async def list_active_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of only active users
    """
    from sqlalchemy import select
    from app.models.user import User
    
    result = await db.execute(
        select(User)
        .where(User.is_active == True)
        .offset(skip)
        .limit(limit)
        .order_by(User.created_at.desc())
    )
    users = result.scalars().all()
    return users
EOF
```

**Test it:**
- Create some users
- Deactivate one
- Call `/api/v1/users/active/list`
- Should only show active users! ✅

---

## 📝 Step 5.6: Add User Statistics Endpoint

Let's add an endpoint to get user statistics.

```bash
cat >> app/api/v1/endpoints/users.py << 'EOF'


@router.get("/stats/summary")
async def get_user_stats(db: AsyncSession = Depends(get_db)):
    """
    Get user statistics
    """
    from sqlalchemy import func, select
    from app.models.user import User
    
    # Total users
    total_result = await db.execute(select(func.count(User.id)))
    total_users = total_result.scalar()
    
    # Active users
    active_result = await db.execute(
        select(func.count(User.id)).where(User.is_active == True)
    )
    active_users = active_result.scalar()
    
    # Inactive users
    inactive_users = total_users - active_users
    
    # Admin users
    admin_result = await db.execute(
        select(func.count(User.id)).where(User.is_admin == True)
    )
    admin_users = admin_result.scalar()
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": inactive_users,
        "admin_users": admin_users,
        "percentage_active": round((active_users / total_users * 100) if total_users > 0 else 0, 2)
    }
EOF
```

**Test it:**
```
GET /api/v1/users/stats/summary
```

You'll see nice statistics! 📊

---

## 🧪 LESSON 5 CHECKPOINT

Verify everything works:

### CRUD Operations ✅
- [ ] CREATE: Can create users with hashed passwords
- [ ] READ: Can get users by ID, username, or list all
- [ ] UPDATE: Can update user fields (including password)
- [ ] DELETE: Can delete users (hard delete)

### Additional Features ✅
- [ ] Soft delete (deactivate) works
- [ ] Pagination works with skip/limit
- [ ] Active users filter works
- [ ] User statistics endpoint works
- [ ] Passwords are hashed in database

### Security ✅
- [ ] Passwords never returned in API responses
- [ ] Passwords stored as hashes, not plain text
- [ ] Can verify hashed passwords match

**Complete test:**

```bash
# Test password hashing
cd ~/Desktop/opal-v2/backend
python app/core/security.py

# Test all endpoints in Swagger UI
# http://localhost:8000/docs

# Verify passwords are hashed in database
docker exec -it opal-postgres psql -U opal -d opal
SELECT username, hashed_password FROM users LIMIT 3;
# Should see long hashed strings, not plain passwords
\q
```

---

## 📝 Step 5.7: Commit Your Changes

```bash
# Stop server (Ctrl+C)
cd ~/Desktop/opal-v2

# Check status
git status

# Add files
git add .

# Commit
git commit -m "Add full CRUD operations and security

- Implement UPDATE and DELETE operations
- Add password hashing with bcrypt
- Create user service layer for business logic
- Add pagination and filtering
- Add soft delete (deactivate users)
- Add user statistics endpoint
- Improve error handling with proper HTTP status codes
- All CRUD operations tested and working"

# View history
git log --oneline
```

---

## 🐛 Common Issues and Solutions

### Issue 1: "No module named 'passlib'"
**Solution:**
```bash
pip install passlib[bcrypt]
pip freeze > requirements.txt
```

### Issue 2: Update doesn't work
**Problem:** Sending empty JSON or wrong user_id

**Solution:**
```bash
# Make sure to:
# 1. Use correct user_id
# 2. Send at least one field to update
# 3. Check response for errors
```

### Issue 3: Can't delete user
**Problem:** User doesn't exist

**Solution:**
```bash
# First check if user exists
GET /api/v1/users/{user_id}

# Then delete
DELETE /api/v1/users/{user_id}
```

### Issue 4: Password verification fails
**Problem:** Comparing wrong values

**Solution:**
```python
# CORRECT:
verify_password("plain_password", user.hashed_password)

# WRONG:
verify_password(user.hashed_password, "plain_password")
# Order matters!
```

---

## 📝 Your Learning Journal - Lesson 5

### 1. What I learned:
```
- Complete CRUD operations
- Password hashing with bcrypt
- Service layer pattern
- Pagination
- ...
```

### 2. Security concepts:
```
- Never store plain passwords
- Hash passwords before storing
- Verify passwords by comparing hashes
- Use industry-standard algorithms
```

### 3. New patterns:
```
- Service layer separates business logic
- Soft delete vs hard delete
- Query parameters for filtering
- HTTP status codes
```

---

## 🎓 Key Concepts Learned

### CRUD Operations
- **Create** = POST - Add new records
- **Read** = GET - Retrieve records
- **Update** = PUT - Modify existing records
- **Delete** = DELETE - Remove records

### Security
- **Password hashing** = One-way transformation
- **Bcrypt** = Industry-standard algorithm
- **Salt** = Random data added to hash (bcrypt does this automatically)
- **Verification** = Compare hashes, not passwords

### Best Practices
- **Service layer** = Business logic separate from API
- **Soft delete** = Mark as inactive instead of deleting
- **Pagination** = Don't return all records at once
- **Status codes** = Use correct HTTP codes

---

## 🚀 What's Next?

In **Lesson 6**, you'll:
- Build relationships between tables
- Create the Summit Log system (with users)
- Implement foreign keys
- Query across multiple tables
- Build a real feature of OPAL

**Estimated Time**: 60 minutes

This is where it gets REALLY interesting - you'll start building actual OPAL features! 🎯

---

## ✅ Ready for Lesson 6?

Before continuing:
- ✅ All CRUD operations work
- ✅ Passwords are hashed
- ✅ Understand service layer pattern
- ✅ Pagination works
- ✅ Can soft delete and hard delete
- ✅ Changes committed to Git

**When you're ready, tell me: "I finished Lesson 5"!**

---

## 💡 Extra Practice (Optional)

### Challenge 1: Add Email Update Endpoint

Create a special endpoint just for updating email:

```python
@router.patch("/{user_id}/email", response_model=UserResponse)
async def update_user_email(
    user_id: int,
    new_email: EmailStr,
    db: AsyncSession = Depends(get_db)
):
    # Check if email already used
    # Update user's email
    # Return updated user
    pass
```

### Challenge 2: Search Users by Name

Add search functionality:

```python
@router.get("/search/", response_model=List[UserResponse])
async def search_users(
    q: str = Query(..., min_length=2),
    db: AsyncSession = Depends(get_db)
):
    from sqlalchemy import or_
    
    result = await db.execute(
        select(User).where(
            or_(
                User.username.ilike(f"%{q}%"),
                User.full_name.ilike(f"%{q}%")
            )
        )
    )
    return result.scalars().all()
```

### Challenge 3: Batch Delete

Delete multiple users at once:

```python
@router.delete("/batch/", status_code=status.HTTP_204_NO_CONTENT)
async def batch_delete_users(
    user_ids: List[int],
    db: AsyncSession = Depends(get_db)
):
    # Delete multiple users
    # Return count of deleted users
    pass
```

Try building these yourself! 🧪

---

**Congratulations on completing Lesson 5!**

**You now have a complete, secure CRUD API!** This is professional-level development! 🎉

You can:
- ✅ Create users with secure passwords
- ✅ Read users with pagination
- ✅ Update any user field
- ✅ Delete users (hard or soft)
- ✅ Get statistics
- ✅ Filter by status

---

**Next**: Tell me "I finished Lesson 5" for Lesson 6: Database Relationships & Summit Logs 

**Document Version**: 1.0  
**Last Updated**: October 8, 2025

