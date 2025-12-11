# LESSON 2: Project Structure
## Setting Up Your Workspace

**Estimated Time**: 45 minutes  
**Difficulty**: Beginner  
**Prerequisites**: Lesson 1 completed

---

## 🎯 Learning Goals

By the end of this lesson, you will:
- Understand how to organize a full-stack project
- Create a proper directory structure
- Initialize a Git repository
- Set up Python virtual environments
- Create configuration files
- Understand the purpose of each directory

---

## 📚 Background: Why Project Structure Matters

Think of your project like a house:
- 🏠 **Good structure** = Easy to find things, easy to maintain
- 🗑️ **Bad structure** = Chaos, hard to work with, bugs

A well-organized project:
- Makes it easy to find code
- Separates concerns (backend vs frontend)
- Makes collaboration easier
- Follows industry standards

**Our Project Structure:**
```
opal-v2/                    # Root directory
├── backend/                # Python/FastAPI code
│   ├── app/               # Application code
│   ├── tests/             # Backend tests
│   └── requirements.txt   # Python dependencies
├── frontend/              # React/TypeScript code
│   ├── src/              # Source code
│   ├── public/           # Static files
│   └── package.json      # JavaScript dependencies
├── docs/                  # Documentation
└── README.md             # Project overview
```

---

## 📝 Step 2.1: Create Main Project Directory

Let's start fresh with a clean structure.

**Navigate to your workspace:**
```bash
# Go to where you want your project
cd ~/Desktop

# Create the main project directory
mkdir opal-v2
cd opal-v2

# Verify you're in the right place
pwd
```

**Expected output**: `/Users/yourname/Desktop/opal-v2`

**💡 What you're learning:**
- `mkdir` creates a new directory
- `cd` changes your current directory
- `pwd` shows your current location
- We use `opal-v2` to distinguish from the legacy OPAL

**🧪 Test it:**
```bash
# List directory contents (should be empty)
ls -la
```

---

## 📝 Step 2.2: Initialize Git Repository

Git will track all changes to your code.

```bash
# Initialize a new Git repository
git init

# Check status
git status
```

**Expected output:**
```
Initialized empty Git repository in /Users/yourname/Desktop/opal-v2/.git/
On branch main
No commits yet
```

**💡 What you're learning:**
- `git init` creates a hidden `.git` folder
- This folder tracks all your changes
- `git status` shows the current state
- You're on the "main" branch (the primary version)

**Create initial README:**
```bash
# Create README file
cat > README.md << 'EOF'
# OPAL v2 - Modern Observatory Management System

A modernized version of the OPAL system for Subaru Telescope operations.

## Technology Stack

- **Backend**: Python 3.11, FastAPI, PostgreSQL
- **Frontend**: React, TypeScript, Material-UI
- **Infrastructure**: Docker, Redis, Celery

## Getting Started

See individual README files in `backend/` and `frontend/` directories.

## Documentation

- [Technical Stack](../TECH_STACK.md)
- [Modernization Plan](../MODERNIZATION_PLAN.md)

## Development Status

🚧 Under Development
EOF

# View what you created
cat README.md
```

**💡 What you're learning:**
- `cat > file << 'EOF'` creates a file with multiple lines
- Everything between `<< 'EOF'` and `EOF` goes into the file
- README.md is written in Markdown format
- GitHub/GitLab display README.md on the project page

---

## 📝 Step 2.3: Create .gitignore File

`.gitignore` tells Git which files to ignore (don't track).

```bash
# Create .gitignore file
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
*.egg-info/
dist/
build/

# Node
node_modules/
npm-debug.log
yarn-error.log
.pnp/
.pnp.js

# Environment variables
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Database
*.db
*.sqlite
*.sqlite3

# Logs
*.log
logs/

# Testing
.coverage
htmlcov/
.pytest_cache/

# Build outputs
*.pyc
dist/
build/
EOF

# View it
cat .gitignore
```

**💡 What you're learning:**
- `.gitignore` prevents tracking unwanted files
- Lines starting with `#` are comments
- `__pycache__/` = Python compiled files (don't need to track)
- `node_modules/` = JavaScript dependencies (huge, don't track)
- `.env` = secrets (NEVER commit this!)
- `.DS_Store` = macOS system files (ignore)

**🧪 Test it:**
```bash
# Create a test file that should be ignored
mkdir __pycache__
touch __pycache__/test.pyc

# Check git status
git status
```

You should NOT see `__pycache__` listed! ✅

```bash
# Clean up test
rm -rf __pycache__
```

---

## 📝 Step 2.4: Create Backend Directory Structure

Now let's create the backend (API) structure.

```bash
# Create backend directory and subdirectories
mkdir -p backend/app/api/v1/endpoints
mkdir -p backend/app/core
mkdir -p backend/app/db
mkdir -p backend/app/models
mkdir -p backend/app/schemas
mkdir -p backend/app/services
mkdir -p backend/tests

# View the structure
tree backend -L 3
# If tree is not installed: brew install tree (macOS) or sudo apt install tree (Linux)
# Windows: use `dir /s backend` instead
```

**💡 What you're learning:**
- `mkdir -p` creates parent directories if they don't exist
- `-p` prevents errors if directory already exists
- Backend structure follows FastAPI best practices:
  - `app/` = main application code
  - `api/v1/` = API version 1 endpoints
  - `core/` = configuration, security, utilities
  - `db/` = database connection
  - `models/` = database models (tables)
  - `schemas/` = request/response validation
  - `services/` = business logic
  - `tests/` = test files

**Create backend README:**
```bash
cat > backend/README.md << 'EOF'
# OPAL Backend

FastAPI-based REST API for OPAL v2.

## Setup

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Run Development Server

```bash
uvicorn app.main:app --reload
```

API will be available at: http://localhost:8000

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
EOF
```

---

## 📝 Step 2.5: Setup Python Virtual Environment

Virtual environments isolate Python packages for your project.

```bash
# Navigate to backend
cd backend

# Create virtual environment
python3.11 -m venv venv

# Activate it
source venv/bin/activate
# On Windows: venv\Scripts\activate
```

**Your prompt should change to show `(venv)` at the beginning!**

Example: `(venv) yourname@computer:~/Desktop/opal-v2/backend$`

**💡 What you're learning:**
- Virtual environments prevent package conflicts
- Each project can have its own package versions
- `venv` is the virtual environment directory
- When activated, `pip install` only affects this environment
- Always activate before working on the project

**🧪 Test it:**
```bash
# Check Python location (should be inside venv)
which python
# Should show: /Users/yourname/Desktop/opal-v2/backend/venv/bin/python

# Check pip location
which pip
# Should show: /Users/yourname/Desktop/opal-v2/backend/venv/bin/pip
```

✅ If both show paths inside `venv`, you're good!

---

## 📝 Step 2.6: Create requirements.txt

This file lists all Python packages we need.

```bash
# Make sure you're in backend/ and venv is activated
# Create requirements.txt
cat > requirements.txt << 'EOF'
# Core Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Database
sqlalchemy==2.0.23
asyncpg==0.29.0
alembic==1.12.1

# Validation
pydantic==2.5.0
pydantic-settings==2.1.0

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Utilities
python-dotenv==1.0.0
httpx==0.25.2

# Development
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.11.0
EOF

# View it
cat requirements.txt
```

**💡 What you're learning:**
- Each line is a package with version number
- `==` means exact version (ensures consistency)
- `[standard]` or `[bcrypt]` are "extras" (optional features)
- Comments start with `#`
- This file makes it easy to install everything at once

**Install the packages:**
```bash
# Make sure venv is activated!
pip install -r requirements.txt
```

This will take 2-3 minutes. Watch the progress!

**🧪 Test it:**
```bash
# Check installed packages
pip list

# Should see fastapi, uvicorn, sqlalchemy, etc.
```

---

## 📝 Step 2.7: Create Environment Variables File

Create `.env.example` (template for configuration):

```bash
cat > .env.example << 'EOF'
# Application
APP_NAME=OPAL API
DEBUG=True

# Database
DATABASE_URL=postgresql+asyncpg://opal:password@localhost:5432/opal

# Redis
REDIS_URL=redis://localhost:6379

# Security (CHANGE THESE IN PRODUCTION!)
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480

# LDAP
LDAP_SERVER=ldap://your-ldap-server
LDAP_BASE_DN=dc=example,dc=com
LDAP_BIND_DN=cn=admin,dc=example,dc=com
LDAP_BIND_PASSWORD=changeme

# Email
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASSWORD=changeme
SMTP_FROM_EMAIL=noreply@example.com

# Weather APIs
WEATHER_API_URL=https://www.naoj.org/Weather/data/SensorDump.json
WEATHER_API_FALLBACK=http://mkwc.ifa.hawaii.edu/current/
EOF

# Copy to actual .env file
cp .env.example .env
```

**💡 What you're learning:**
- `.env` stores configuration and secrets
- `.env.example` is a template (committed to Git)
- `.env` is NOT committed (contains real secrets)
- Applications read these values instead of hardcoding
- Format: `KEY=value`

**⚠️ IMPORTANT:** Never commit `.env` to Git! (Already in `.gitignore`)

---

## 📝 Step 2.8: Create Frontend Directory Structure

Return to project root and create frontend structure:

```bash
# Go back to project root
cd ..

# We'll use Vite to create the frontend structure
# (We'll do this properly in Lesson 16, but let's reserve the space)

mkdir -p frontend/src
mkdir -p frontend/public
mkdir -p docs
```

**Create frontend placeholder:**
```bash
cat > frontend/README.md << 'EOF'
# OPAL Frontend

React + TypeScript frontend for OPAL v2.

## Setup (Coming in Lesson 16)

We'll use Vite to create the React application.

```bash
npm create vite@latest . -- --template react-ts
npm install
```

## Development

```bash
npm run dev
```

Frontend will be available at: http://localhost:5173
EOF
```

---

## 📝 Step 2.9: First Git Commit

Let's save our progress to Git!

```bash
# Make sure you're in project root
cd ~/Desktop/opal-v2

# Check what we've created
git status
```

You'll see many "untracked files". Let's add them:

```bash
# Add all files
git add .

# Check status again
git status
```

Now they're "staged" (ready to commit).

```bash
# Create your first commit
git commit -m "Initial project structure

- Created backend and frontend directories
- Setup Python virtual environment
- Added requirements.txt with dependencies
- Created .gitignore and .env.example
- Added README files"

# View commit history
git log
```

**💡 What you're learning:**
- `git add .` stages all changes
- `git commit -m "message"` saves a snapshot
- Commit messages should be descriptive
- Multi-line messages: first line = summary, rest = details
- `git log` shows history

---

## 📝 Step 2.10: Verify Your Structure

Let's make sure everything is correct:

```bash
# View overall structure
tree -L 3 -a
# Or just: ls -R

# Should look like this:
# opal-v2/
# ├── .git/
# ├── .gitignore
# ├── README.md
# ├── backend/
# │   ├── .env
# │   ├── .env.example
# │   ├── README.md
# │   ├── app/
# │   │   ├── api/
# │   │   ├── core/
# │   │   ├── db/
# │   │   ├── models/
# │   │   ├── schemas/
# │   │   └── services/
# │   ├── requirements.txt
# │   ├── tests/
# │   └── venv/
# ├── docs/
# └── frontend/
#     ├── README.md
#     ├── public/
#     └── src/
```

**Check your virtual environment:**
```bash
cd backend
source venv/bin/activate  # Should see (venv) in prompt
python --version  # Should be 3.11+
pip list  # Should see installed packages
deactivate  # Exit virtual environment
```

---

## 🧪 LESSON 2 CHECKPOINT

Before moving on, verify you have:

### File Structure ✅
- [ ] `opal-v2/` root directory exists
- [ ] `backend/` with subdirectories (app, tests, venv)
- [ ] `frontend/` with placeholders
- [ ] `.gitignore` file exists
- [ ] README.md files in each directory

### Git Setup ✅
- [ ] Git repository initialized (`ls -la .git` shows directory)
- [ ] First commit made (`git log` shows commit)
- [ ] All files committed (`git status` shows clean)

### Python Environment ✅
- [ ] Virtual environment created (`backend/venv/` exists)
- [ ] Can activate venv (`source backend/venv/bin/activate`)
- [ ] Packages installed (`pip list` shows fastapi, etc.)
- [ ] `.env` file created (not committed)

**Test everything:**
```bash
# From project root
cd ~/Desktop/opal-v2

# Test Git
git log --oneline
# Should show your commit

# Test Python environment
cd backend
source venv/bin/activate
python -c "import fastapi; print('FastAPI version:', fastapi.__version__)"
# Should print: FastAPI version: 0.104.1
deactivate
```

---

## 🐛 Common Issues and Solutions

### Issue 1: "venv activation not working"
**Problem**: Prompt doesn't show `(venv)`

**Solution:**
```bash
# Make sure you're in backend/
cd backend

# Try explicit path
source ./venv/bin/activate

# On Windows, use:
venv\Scripts\activate

# Verify it worked
which python  # Should show path inside venv
```

### Issue 2: "pip install fails"
**Problem**: Can't install packages

**Solution:**
```bash
# Update pip first
pip install --upgrade pip

# Try again
pip install -r requirements.txt

# If still fails, check you have internet connection
ping google.com
```

### Issue 3: "Permission denied"
**Problem**: Can't create directories

**Solution:**
```bash
# Check you're in the right location
pwd

# Make sure you have write permissions
ls -la ..

# Use sudo only if necessary (not recommended for project files)
```

### Issue 4: "Git commit says 'nothing to commit'"
**Problem**: No changes staged

**Solution:**
```bash
# Check status
git status

# If files are untracked:
git add .

# Then commit
git commit -m "Your message"
```

---

## 📝 Your Learning Journal - Lesson 2

Take notes:

### 1. What I learned:
```
- Directory structure for full-stack projects
- How to use virtual environments
- Git basics (init, add, commit)
- ...
```

### 2. New commands I used:
```bash
mkdir -p       # Create directories with parents
git init       # Initialize repository
git add .      # Stage all changes
git commit -m  # Save a snapshot
python -m venv # Create virtual environment
source venv/bin/activate  # Activate venv
pip install -r # Install from file
```

### 3. Questions I have:
```
- Why separate backend and frontend?
- What is a virtual environment really doing?
- ...
```

### 4. What I want to explore:
```
- Learn more about Git branches
- Understand project structure patterns
- ...
```

---

## 🎓 Key Concepts Learned

### Project Organization
- **Separation of concerns**: Backend and frontend separate
- **Virtual environments**: Isolated Python packages
- **Configuration files**: `.env` for secrets
- **Version control**: Git tracks everything

### Best Practices
- ✅ Never commit secrets (`.env` in `.gitignore`)
- ✅ Use virtual environments (avoid "works on my machine")
- ✅ Write good README files (help others understand)
- ✅ Commit often with descriptive messages

### Directory Structure
- **backend/app/**: Main application code
- **backend/tests/**: Test files
- **backend/venv/**: Virtual environment (not committed)
- **frontend/src/**: React source code
- **docs/**: Documentation

---

## 🚀 What's Next?

In **Lesson 3**, you'll:
- Create your first FastAPI application
- Write "Hello World" endpoint
- Start the development server
- Test the API in your browser
- Understand how FastAPI works

**Estimated Time**: 30-45 minutes

This is where it gets exciting - you'll see your first API running! 🎉

---

## ✅ Ready for Lesson 3?

Before continuing, make sure:
- ✅ Project structure is created correctly
- ✅ Git repository is initialized
- ✅ Virtual environment is working
- ✅ All packages are installed
- ✅ You understand the directory structure
- ✅ You've made notes in your learning journal

**When you're ready, tell me: "I finished Lesson 2" and I'll create Lesson 3!**

---

## 💡 Extra Practice (Optional)

Try these experiments:

### Experiment 1: Create a Test File
```bash
cd backend/app
echo "print('Hello from OPAL!')" > test.py
python test.py
git status  # See that Git noticed the new file
rm test.py  # Clean up
```

### Experiment 2: View Git History
```bash
git log --oneline --graph --all
# This shows your commit history visually
```

### Experiment 3: Practice Git
```bash
# Make a change
echo "## Installation" >> README.md

# Check what changed
git diff

# Stage and commit
git add README.md
git commit -m "Update README"

# View history
git log --oneline
```

### Experiment 4: Virtual Environment
```bash
cd backend
source venv/bin/activate

# Install a package
pip install requests

# See it in the list
pip list | grep requests

# Deactivate
deactivate

# Try to import (should fail now)
python -c "import requests"  # Error!

# Activate again and it works
source venv/bin/activate
python -c "import requests; print('Success!')"
```

These experiments will help solidify your understanding! 🧪

---

**Great job completing Lesson 2! You now have a professional project structure! 🎉**

**Next**: When ready, say "I finished Lesson 2" for Lesson 3: Hello World with FastAPI

---

**Document Version**: 1.0  
**Last Updated**: October 8, 2025

