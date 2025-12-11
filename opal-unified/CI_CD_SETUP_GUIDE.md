# CI/CD Setup Guide for OPAL Project

## 📚 Table of Contents
1. [What is CI/CD?](#what-is-cicd)
2. [How It Works](#how-it-works)
3. [Setup Instructions](#setup-instructions)
4. [GitHub Secrets Configuration](#github-secrets-configuration)
5. [Testing the Pipeline](#testing-the-pipeline)
6. [Precautions & Best Practices](#precautions--best-practices)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 What is CI/CD?

### Continuous Integration (CI)
**Automatically test your code every time you commit**

```
Without CI:                     With CI:
Developer commits → Wait        Developer commits → Instant feedback
Manual testing → Slow           Automated testing → Fast
Find bugs late → Expensive      Find bugs early → Cheap
```

### Continuous Deployment (CD)
**Automatically deploy code to production after tests pass**

```
Without CD:                     With CD:
Manual SSH → Error-prone        Automated → Reliable
Manual steps → Forgotten        Scripted → Consistent
Downtime → Users angry          Zero-downtime → Users happy
```

---

## 🔄 How It Works

### Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    DEVELOPER WORKFLOW                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 1. Write Code                                               │
│    - Add new feature                                        │
│    - Fix bug                                                │
│    - Refactor code                                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Commit & Push                                            │
│    git add .                                                │
│    git commit -m "Add delete image feature"                │
│    git push origin feature/delete-images                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. CI Pipeline Triggered (GitHub Actions)                   │
│    ✅ Checkout code                                         │
│    ✅ Install dependencies                                  │
│    ✅ Lint code (check quality)                            │
│    ✅ Run tests                                             │
│    ✅ Build application                                     │
│    ✅ Security scan                                         │
│                                                             │
│    Result: ✅ PASS or ❌ FAIL                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. If PASS: Create Pull Request                            │
│    - Review code                                            │
│    - Discuss changes                                        │
│    - Approve merge                                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Merge to Main Branch                                     │
│    - Code is now in production branch                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. CD Pipeline Triggered (Deployment)                       │
│    ✅ Build production version                              │
│    ✅ Create backup                                         │
│    ✅ Deploy to staging (test)                             │
│    ✅ Run smoke tests                                       │
│    ✅ Deploy to production                                  │
│    ✅ Health check                                          │
│    ✅ Monitor for errors                                    │
│                                                             │
│    Result: 🚀 DEPLOYED or ↩️ ROLLBACK                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. Production Live                                          │
│    - Users see new features                                 │
│    - No downtime                                            │
│    - Monitoring active                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Setup Instructions

### Step 1: Create GitHub Repository (If Not Already)

```bash
# Initialize git in your project
cd /opt/OPAL/opal-unified
git init
git add .
git commit -m "Initial commit"

# Create repository on GitHub (via web UI)
# Then link and push:
git remote add origin https://github.com/YOUR_USERNAME/opal-unified.git
git branch -M main
git push -u origin main
```

### Step 2: GitHub Workflows Already Created ✅

The CI/CD workflows are now in your project:
```
.github/workflows/
├── backend-ci.yml           # Tests backend on every push
├── frontend-ci.yml          # Tests frontend on every push
└── deploy-production.yml    # Deploys to VM when merged to main
```

### Step 3: Configure GitHub Secrets

**Required Secrets** (add these in GitHub):

1. Go to: `GitHub Repository → Settings → Secrets and variables → Actions`
2. Click: `New repository secret`
3. Add these secrets:

```
VM_SSH_KEY       = Your SSH private key (for connecting to VM)
VM_HOST          = opalfailover (your VM hostname)
VM_USER          = root (your VM username)
VM_PATH          = /opt/OPAL/opal-unified (project path on VM)
```

### Step 4: Setup SSH Key for GitHub Actions

```bash
# On your local machine:
ssh-keygen -t ed25519 -C "github-actions-opal" -f ~/.ssh/github_actions_opal
# Press Enter for no passphrase (required for automation)

# Copy the PRIVATE key:
cat ~/.ssh/github_actions_opal
# Copy entire output → Add to GitHub secret: VM_SSH_KEY

# Copy the PUBLIC key to VM:
ssh-copy-id -i ~/.ssh/github_actions_opal.pub root@opalfailover
# OR manually:
cat ~/.ssh/github_actions_opal.pub
# Then on VM:
echo "PASTE_PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
```

---

## 🔐 GitHub Secrets Configuration

### How to Add Secrets:

```
1. GitHub Repository → Settings
2. Left sidebar → Secrets and variables → Actions
3. Click "New repository secret"
4. Add each secret:

Name: VM_SSH_KEY
Value: (Paste entire private key)
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAA...
-----END OPENSSH PRIVATE KEY-----

Name: VM_HOST
Value: opalfailover

Name: VM_USER
Value: root

Name: VM_PATH
Value: /opt/OPAL/opal-unified
```

### Security Best Practices:

```
✅ NEVER commit secrets to Git
✅ Use GitHub Secrets for sensitive data
✅ Rotate SSH keys regularly
✅ Use separate deploy keys (not your personal SSH key)
✅ Limit VM user permissions (use deploy user, not root)
✅ Enable 2FA on GitHub
✅ Use branch protection rules
```

---

## 🧪 Testing the Pipeline

### Test 1: Backend CI

```bash
# Make a small change to backend
cd backend
echo "# Test comment" >> app/main.py

# Commit and push
git add .
git commit -m "Test backend CI"
git push origin main

# Check GitHub:
# Go to: Repository → Actions tab
# You should see: "Backend CI" workflow running
# Wait for: ✅ All checks passed
```

### Test 2: Frontend CI

```bash
# Make a small change to frontend
cd frontend/src
echo "// Test comment" >> App.js

# Commit and push
git add .
git commit -m "Test frontend CI"
git push origin main

# Check GitHub Actions:
# You should see: "Frontend CI" workflow running
```

### Test 3: Full Deployment

```bash
# Merge changes to main branch (via PR or direct push)
git checkout main
git pull origin main

# Deployment will trigger automatically
# Check: GitHub → Actions → "Deploy to Production"
# Monitor: VM logs for deployment progress
```

---

## ⚠️ Precautions & Best Practices

### 🔒 Security Precautions

#### 1. **NEVER Commit Sensitive Data**
```bash
# ❌ NEVER do this:
git add backend/.env
git commit -m "Add config"  # .env contains passwords!

# ✅ ALWAYS do this:
echo "backend/.env" >> .gitignore
git add .gitignore
git commit -m "Ignore environment files"
```

#### 2. **Use Environment Variables**
```bash
# ❌ BAD:
DATABASE_PASSWORD="my_secret_password"  # In code

# ✅ GOOD:
DATABASE_PASSWORD=${DATABASE_PASSWORD}  # From environment
```

#### 3. **Separate Environments**
```
Development → Your laptop (local DB)
Staging     → Test server (test DB)
Production  → Live server (production DB)

NEVER mix environments!
NEVER use production DB for testing!
```

### 🛡️ Branch Protection Rules

**Setup (Required):**
```
GitHub → Settings → Branches → Add rule

Branch name pattern: main

Enable:
✅ Require pull request reviews before merging
✅ Require status checks to pass (CI tests)
✅ Require branches to be up to date
✅ Include administrators
❌ Allow force pushes (NEVER!)
❌ Allow deletions (NEVER!)
```

**Why?**
```
✅ Prevents accidental direct commits to main
✅ Requires code review
✅ Requires all tests to pass
✅ Prevents force push (losing history)
✅ Protects production code
```

### 📊 Testing Requirements

**Before Deployment:**
```
✅ All unit tests pass
✅ All integration tests pass
✅ Code review approved
✅ No linter errors
✅ No security vulnerabilities
✅ Database migrations tested
✅ Smoke tests pass
```

### 🔄 Rollback Strategy

**If Deployment Fails:**
```
Option 1: Automatic Rollback
- CI/CD detects health check failure
- Automatically reverts to previous version
- Users see no downtime

Option 2: Manual Rollback
- SSH to VM
- Restore from backup
- Restart services

Option 3: Git Revert
- git revert HEAD
- Push revert commit
- CD deploys previous version
```

**Backup Strategy:**
```
Before every deployment:
✅ Backup database
✅ Backup code
✅ Backup configuration
✅ Store with timestamp
✅ Keep last 7 backups
✅ Test restore procedure
```

### 📈 Monitoring & Alerts

**What to Monitor:**
```
✅ Application health (/health endpoint)
✅ Error rate (log errors)
✅ Response time (API latency)
✅ Database connections
✅ Disk space
✅ Memory usage
✅ CPU usage
```

**Alert Conditions:**
```
⚠️  Error rate > 1%
⚠️  Response time > 3 seconds
⚠️  Disk usage > 90%
⚠️  Memory usage > 90%
⚠️  Health check fails
```

### 🗃️ Database Migration Precautions

**CRITICAL RULES:**
```
1. ✅ ALWAYS backup database before migration
2. ✅ Test migrations on staging first
3. ✅ Write rollback migrations
4. ✅ Never drop tables in production
5. ✅ Add columns (don't remove)
6. ✅ Make changes backward-compatible
7. ✅ Run migrations during low-traffic hours
```

**Example Migration Flow:**
```bash
# Step 1: Backup
mysqldump opal > backup-$(date +%Y%m%d).sql

# Step 2: Test on staging
ssh staging-server
mysql opal_staging < migration.sql
# Test application works

# Step 3: Run on production
ssh production-server
mysql opal < migration.sql
# Monitor for errors

# Step 4: If fails, rollback
mysql opal < rollback.sql
```

---

## 🚨 Common Pitfalls & How to Avoid

### 1. **Forgetting to Update Requirements**
```bash
# ❌ WRONG:
pip install new-package
# (Forget to update requirements.txt)
# CI fails because package missing

# ✅ CORRECT:
pip install new-package
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Add new-package dependency"
```

### 2. **Hard-coding Configuration**
```python
# ❌ WRONG:
DATABASE_URL = "mysql://localhost/opal"  # Won't work on VM!

# ✅ CORRECT:
import os
DATABASE_URL = os.getenv("DATABASE_URL")  # Works everywhere
```

### 3. **Not Testing Locally First**
```bash
# ❌ WRONG:
git commit -m "Quick fix"
git push
# CI fails, everyone sees red ❌

# ✅ CORRECT:
pytest tests/              # Run tests locally
npm test                   # Test frontend
git commit -m "Tested fix"
git push                   # CI passes ✅
```

### 4. **Committing Large Files**
```bash
# ❌ WRONG:
git add uploads/images/*.jpg  # 500MB of images!
# Repository becomes huge and slow

# ✅ CORRECT:
echo "uploads/" >> .gitignore  # Ignore uploads
# Store images on server, not in Git
```

### 5. **Breaking Changes Without Migration Path**
```python
# ❌ WRONG (Breaking Change):
# Old: user.name (string)
# New: user.first_name, user.last_name (requires data migration!)
# Deployed → All existing data breaks!

# ✅ CORRECT (Gradual Migration):
# Step 1: Add new fields (keep old)
# Step 2: Migrate data
# Step 3: Update code to use new fields
# Step 4: Remove old field (months later)
```

---

## 🔧 Troubleshooting

### CI Pipeline Fails

**Problem:** Tests fail in CI but pass locally
```bash
# Likely causes:
1. Missing dependency in requirements.txt
2. Different Python/Node version
3. Database not available
4. Environment variable missing

# Solution:
- Check CI logs for exact error
- Ensure requirements.txt is up-to-date
- Match Python/Node versions
- Add missing environment variables to GitHub Secrets
```

**Problem:** Build fails
```bash
# Frontend build fails:
cd frontend
npm run build  # Check for errors locally

# Backend build fails:
cd backend
python -m compileall app/  # Check for syntax errors
```

### Deployment Fails

**Problem:** SSH connection fails
```bash
# Check:
1. Is VM_SSH_KEY correct? (entire private key copied)
2. Is public key on VM? (check ~/.ssh/authorized_keys)
3. Is VM accessible? (ssh root@opalfailover)
4. Is firewall blocking? (check VM firewall rules)
```

**Problem:** Services won't start
```bash
# Check VM:
ssh root@opalfailover

# Backend:
cd /opt/OPAL/opal-unified/backend
tail -f /tmp/backend.log  # Check errors

# Frontend:
cd /opt/OPAL/opal-unified/frontend
tail -f /tmp/frontend.log  # Check errors
```

### Rollback Procedure

**If Deployment Breaks Production:**
```bash
# 1. Immediate: Revert Git commit
git log  # Find last good commit
git revert HEAD  # Revert bad commit
git push origin main  # Trigger re-deployment

# 2. Manual: Restore from backup
ssh root@opalfailover
cd /opt/OPAL/opal-unified
tar -xzf backup-YYYYMMDD-HHMMSS.tar.gz
# Restart services

# 3. Database: Restore if needed
mysql opal < backup-YYYYMMDD.sql
```

---

## 📅 Future Maintenance

### Daily
```
✅ Monitor CI/CD pipeline status
✅ Review failed builds
✅ Check application logs
```

### Weekly
```
✅ Review security scan results
✅ Update dependencies (npm audit fix, pip list --outdated)
✅ Check disk space on VM
✅ Review database backups
```

### Monthly
```
✅ Rotate SSH keys
✅ Update GitHub Actions workflows
✅ Review and clean old backups
✅ Performance testing
✅ Security audit
```

### Quarterly
```
✅ Upgrade Python/Node versions
✅ Major dependency updates
✅ Disaster recovery drill
✅ Review CI/CD pipeline efficiency
```

---

## 🎯 Quick Reference Commands

### Setup
```bash
# Add GitHub remote
git remote add origin https://github.com/USER/opal-unified.git

# Push to GitHub
git push -u origin main
```

### Daily Workflow
```bash
# 1. Create feature branch
git checkout -b feature/my-feature

# 2. Make changes
# ... edit files ...

# 3. Test locally
cd backend && pytest
cd frontend && npm test

# 4. Commit
git add .
git commit -m "Add my feature"

# 5. Push
git push origin feature/my-feature

# 6. Create Pull Request on GitHub
# Wait for CI to pass ✅

# 7. Merge to main
# Deployment happens automatically 🚀
```

### Emergency
```bash
# Rollback last commit
git revert HEAD
git push origin main

# Check VM status
ssh root@opalfailover
systemctl status opal-backend
systemctl status opal-frontend

# View logs
tail -f /var/log/opal/*.log
```

---

## ✅ Checklist Before Going Live

### Pre-Deployment
```
☐ All tests passing locally
☐ Code reviewed by teammate
☐ No console.log() or print() debug statements
☐ No hardcoded credentials
☐ Database backup created
☐ Rollback plan documented
☐ Monitoring enabled
☐ Alert recipients configured
```

### Post-Deployment
```
☐ Health check passed
☐ Smoke tests passed
☐ Key features tested manually
☐ No errors in logs
☐ Performance acceptable
☐ Users can access system
☐ Backup verified
☐ Monitoring shows green
```

---

## 📚 Additional Resources

- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **FastAPI Deployment:** https://fastapi.tiangolo.com/deployment/
- **React Deployment:** https://create-react-app.dev/docs/deployment/
- **CI/CD Best Practices:** https://www.atlassian.com/continuous-delivery/principles/continuous-integration-vs-delivery-vs-deployment

---

## 🆘 Support

If you encounter issues:
1. Check CI/CD logs in GitHub Actions
2. Check VM logs: `/tmp/backend.log`, `/tmp/frontend.log`
3. Review this guide's troubleshooting section
4. Contact DevOps team

---

**Remember:** CI/CD is about automation, but you're still in control. Start small, test thoroughly, and gradually increase automation as you gain confidence.

