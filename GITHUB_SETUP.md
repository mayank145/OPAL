# GitHub Setup Guide

## Initial Setup

### 1. Initialize Git Repository (if not already initialized)

```bash
cd opal-unified
git init
```

### 2. Add All Files

```bash
git add .
```

### 3. Create Initial Commit

```bash
git commit -m "Initial commit: FATS System - Production Ready"
```

### 4. Create GitHub Repository

1. Go to GitHub.com
2. Click "New repository"
3. Name it: `fats-system` or `fault-tracking-system`
4. **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

### 5. Add Remote and Push

```bash
# Add remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Or if using SSH:
# git remote add origin git@github.com:YOUR_USERNAME/REPO_NAME.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Important Notes

### Files NOT Committed (Protected by .gitignore)

- ✅ `.env` files (contains sensitive credentials)
- ✅ `venv/` directory (virtual environment)
- ✅ `node_modules/` directory (npm packages)
- ✅ `logs/` directory (log files)
- ✅ `uploads/fats/` directory contents (user-uploaded images)
- ✅ `build/` directory (compiled frontend)
- ✅ IDE configuration files

### Files That ARE Committed

- ✅ `.env.production.example` (template files)
- ✅ `requirements.txt` (Python dependencies)
- ✅ `package.json` (Node.js dependencies)
- ✅ All source code
- ✅ Documentation files
- ✅ Configuration templates

## For Your Colleagues

### Cloning the Repository

```bash
git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
cd REPO_NAME
```

### Setting Up Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.production.example .env

# Edit .env with your database credentials
# nano .env  # or use your preferred editor

# Create logs directory
mkdir -p logs
```

### Setting Up Frontend

```bash
cd frontend

# Install dependencies
npm install

# Copy environment template
cp .env.production.example .env

# Edit .env with your backend URL
# nano .env  # or use your preferred editor
```

### Running the Application

**Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm start
```

## Repository Structure

```
fats-system/
├── .gitignore              # Git ignore rules
├── README.md               # Main documentation
├── PRODUCTION_DEPLOYMENT_CHECKLIST.md
├── VM_DEPLOYMENT_GUIDE.md
├── PRODUCTION_READY_SUMMARY.md
├── FAULT_MANAGEMENT_SYSTEM_DOCUMENTATION.md
├── backend/
│   ├── .env.production.example
│   ├── requirements.txt
│   ├── app/
│   ├── logs/              # Empty (gitkeep)
│   └── uploads/fats/      # Empty (gitkeep)
└── frontend/
    ├── .env.production.example
    ├── package.json
    └── src/
```

## Security Reminders

⚠️ **IMPORTANT**: Never commit:
- `.env` files
- Database passwords
- Secret keys
- API keys
- Personal credentials

Always use `.env.production.example` as a template and let each developer create their own `.env` file.

## Branch Strategy (Optional)

For collaborative development, consider using branches:

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push branch
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

## Updating the Repository

When you make changes:

```bash
# Check status
git status

# Add changes
git add .

# Commit
git commit -m "Description of changes"

# Push
git push origin main
```

## Troubleshooting

### If you accidentally committed .env file:

```bash
# Remove from git (but keep local file)
git rm --cached backend/.env
git rm --cached frontend/.env

# Add to .gitignore (already done)
# Commit the removal
git commit -m "Remove .env files from repository"

# Push
git push origin main
```

### If you need to update .gitignore:

```bash
# Edit .gitignore
# Then:
git add .gitignore
git commit -m "Update .gitignore"
git push origin main
```

## Next Steps

1. ✅ Create GitHub repository
2. ✅ Push code to GitHub
3. ✅ Share repository URL with colleagues
4. ✅ Ensure colleagues have access (add as collaborators if private repo)
5. ✅ Share this guide with colleagues

---

**Ready to push!** Follow the steps above to get your code on GitHub.

